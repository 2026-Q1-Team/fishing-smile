from typing import (
    Annotated,
    Literal,
    Union,
)
from pathlib import Path
from functools import cache

from pydantic import (
    BaseModel,
    Field,
)
import yaml

from .search_list import SearchList
from .attack_component import (
    EmailComponent,
    HTMLComponent,
    APIComponent,
)


AnyAttackComponent = Annotated[
    Union[EmailComponent, HTMLComponent, APIComponent],
    Field(discriminator = 'kind'),
]


SCHEMES_PATH = Path(__file__).parent / 'attack_schemes'


class AttackScheme(BaseModel):
    name: str = Field(description = 'short, snake_case, unique name')
    description: str | None = Field(None, description = 'longer, human readable explanation')
    components: SearchList[AnyAttackComponent] = []

    @staticmethod
    @cache
    def list() -> list[str]:
        """List of attack scheme names available in the standard collection"""
        return [
            path.stem
            for path in SCHEMES_PATH.glob('*.yaml')
        ]

    @staticmethod
    @cache
    def get(scheme_name: str) -> AttackScheme:
        """Retrieve attack scheme from the standard collection by name"""
        try:
            with open(SCHEMES_PATH / f'{scheme_name}.yaml') as f:
                doc = yaml.safe_load(f)
        except FileNotFoundError:
            raise ValueError(f'{scheme_name} is not a valid attack scheme name') from None
        return AttackScheme.model_validate(doc)
