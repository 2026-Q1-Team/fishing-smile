import logging
_logger = logging.getLogger(__name__)
from pathlib import Path
from functools import cached_property
from typing import Callable
import weakref

from pydantic import (
    BaseModel,
    Field,
)
from jinja2 import (
    Environment,
    FunctionLoader,
)

from fishing_smile.settings import get_settings
from .attack_scheme import AttackScheme
from .always_equal import AlwaysEqual


class SchemeMeta(BaseModel):
    source: Path
    cache: AttackScheme | None = None
    cache_mtime: float | None = Field(
        None,
        description = (
            'mtime of source file when current cache is obtained.'
            ' Set to None to mark cache as stale.'
            ' Must be None when cache is None.'
        ),
    )

    @property
    def scheme(self) -> AttackScheme:
        # NOTE: To future maintainers, consider removing autoreloading feature if it is getting too complicated.
        # This is a feature used only in development.
        if (
            get_settings().deployment_mode != 'development'
            and self.cache is not None
        ):
            return self.cache

        self.refresh()
        return self.cache

    def refresh(self) -> None:
        """Reloads scheme from source if out-of-date"""
        current_mtime = self.source.stat().st_mtime
        if (
            self.cache is not None
            and self.cache_mtime == current_mtime
        ):
            return

        self.cache = AttackScheme.from_file(self.source)
        self.cache_mtime = current_mtime


def _make_mtime_checker(
    path: Path,
    previous_mtime: float | None = None,
) -> Callable[[], bool]:
    if previous_mtime is None:
        previous_mtime = path.stat().st_mtime
    def checker():
        return previous_mtime == path.stat().st_mtime
    return checker


class AttackSchemeCollection(BaseModel):
    schemes: dict[str, SchemeMeta] = {}

    def index_schemes(self, base: Path) -> None:
        """Index all attack scheme files found inside given base directory.

        Schemes with duplicated name will be replaced.
        """
        self.schemes.update(
            (self.scheme_name_from_path(path), SchemeMeta(source = path))
            for path in base.glob('**/*.yaml')
        )

    @staticmethod
    def scheme_name_from_path(path: Path) -> str:
        """Guess the scheme name from its file path.

        The real scheme name is contained within its file content.
        This only works if the path follows the following convention:

        - File stem must match the scheme name.
        - Unless if file stem is `scheme`, then its parent directory name must match the scheme name.

        Following this convention allows schemes to be indexed without reading file content.
        """
        return (
            path.stem
            if path.stem != 'scheme' else
            path.parent.name
        )

    def get_meta(self, scheme_name: str) -> SchemeMeta:
        meta = self.schemes.get(scheme_name, None)
        if meta is None:
            raise ValueError(f'Attack scheme {scheme_name} is not indexed in the collection')
        return meta

    def get(self, scheme_name: str) -> AttackScheme:
        meta = self.get_meta(scheme_name)
        if meta.scheme.name != scheme_name:
            _logger.warning(f'Scheme named {meta.scheme.name} is unconventionally stored at {meta.source}')
        for component in meta.scheme.components:
            for template_name, template_spec in component.templates.items():
                template_spec._jinja = AlwaysEqual(
                    lambda
                        env = weakref.proxy(self.jinja_env),
                        name = f'{scheme_name}/{component.kind}/{component.name}/{template_name}':
                    env.get_template(name)
                )
        return meta.scheme

    @cached_property
    def jinja_env(self) -> Environment:
        def loader(name: str):
            try:
                (scheme_name, component_kind, component_name, template_name) = name.split('/')
            except ValueError as e:
                e.add_note('Template name must follow {scheme_name}/{component_kind}/{component_name}/{template_name} format')
                raise

            template_spec = (
                self.get(scheme_name)
                    .components.first(kind = component_kind, name = component_name)
                    .templates[template_name]
            )
            scheme_meta = self.get_meta(scheme_name)
            # FIXME: The work of checking souce current mtime is repeated by both `loader`
            # and `SchemeMeta.refresh` / `TemplateSpec.value`.
            match template_spec.kind:
                case 'file':
                    uptodate = _make_mtime_checker(template_spec._effective_path)
                    filename = template_spec._effective_path
                case 'string':
                    uptodate = _make_mtime_checker(
                        scheme_meta.source,
                        scheme_meta.cache_mtime,
                    )
                    # NOTE: String template within same scheme.yaml will share filename.
                    # This should work if it's only used for "traceback display" as jinja doc said.
                    filename = scheme_meta.source
                case _:
                    uptodate = lambda: True
                    filename = None
            return (template_spec.value, filename, uptodate)
        return Environment(
            loader = FunctionLoader(loader),
            auto_reload = get_settings().deployment_mode == 'development',
            # TODO: set bytecode_cache to persistent location
        )


STANDARD_COLLECTION_PATH = Path(__file__).parent / 'attack_schemes'
standard_schemes = AttackSchemeCollection()
standard_schemes.index_schemes(STANDARD_COLLECTION_PATH)
