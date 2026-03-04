import logging
_logger = logging.getLogger(__name__)
from pathlib import Path

from pydantic import (
    BaseModel,
    Field,
)

from .attack_scheme import AttackScheme


class SchemeMeta(BaseModel):
    source: Path
    cache: AttackScheme | None = None


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

    def get(self, scheme_name: str) -> AttackScheme:
        meta = self.schemes.get(scheme_name, None)
        if meta is None:
            raise ValueError(f'Attack scheme {scheme_name} is not indexed in the collection')

        if meta.cache is not None:
            return meta.cache

        meta.cache = AttackScheme.from_file(meta.source)
        if meta.cache.name != scheme_name:
            _logger.warning(f'Scheme named {meta.cache.name} is unconventionally stored at {meta.source}')
        return meta.cache


STANDARD_COLLECTION_PATH = Path(__file__).parent / 'attack_schemes'
standard_schemes = AttackSchemeCollection()
standard_schemes.index_schemes(STANDARD_COLLECTION_PATH)
