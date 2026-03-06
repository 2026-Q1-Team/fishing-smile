import logging
_logger = logging.getLogger(__name__)
from pathlib import Path
from functools import cached_property
from typing import Callable

from pydantic import (
    BaseModel,
    Field,
)
from jinja2 import (
    Environment,
    FunctionLoader,
)

from .attack_scheme import AttackScheme


class SchemeMeta(BaseModel):
    source: Path
    cache: AttackScheme | None = None
    cache_mtime: float | None = None


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
        current_mtime = meta.source.stat().st_mtime
        if (
            meta.cache is not None
            and meta.cache_mtime == current_mtime
        ):
            return meta.cache

        meta.cache = AttackScheme.from_file(meta.source)
        meta.cache_mtime = current_mtime
        if meta.cache.name != scheme_name:
            _logger.warning(f'Scheme named {meta.cache.name} is unconventionally stored at {meta.source}')
        return meta.cache

    @cached_property
    def jinja_env(self) -> Environment:
        def loader(name: str):
            try:
                (scheme_name, component_name, template_name) = name.split('/')
            except ValueError as e:
                # FIXME: component_name is not unique within scheme
                e.add_note('Template name must follow {scheme_name}/{component_name}/{template_name} format')
                raise

            template_spec = self.get(scheme_name).components.first(name = component_name).templates[template_name]
            scheme_meta = self.get_meta(scheme_name)
            # FIXME: The work of checking souce current mtime is repeated by both `loader`
            # and `AttackSchemeCollection.get` / `TemplateSpec.value`.
            # Maybe, jinja's uptodate function should invalidate underlying cache too.
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
            # TODO: set bytecode_cache to persistent location
        )


STANDARD_COLLECTION_PATH = Path(__file__).parent / 'attack_schemes'
standard_schemes = AttackSchemeCollection()
standard_schemes.index_schemes(STANDARD_COLLECTION_PATH)
