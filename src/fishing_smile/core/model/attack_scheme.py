from typing import (
    Annotated,
    List,
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
    components: List[AnyAttackComponent] = []

    @staticmethod
    @cache
    def list() -> list[str]:
        return [
            path.stem
            for path in SCHEMES_PATH.glob('*.yaml')
        ]

    @staticmethod
    @cache
    def get(scheme_name: str) -> AttackScheme:
        with open(SCHEMES_PATH / f'{scheme_name}.yaml') as f:
            doc = yaml.safe_load(f)
        return AttackScheme.model_validate(doc)

    def find_component(
        self,
        name: str = None,
        kind: str = None,
    ) -> AttackComponent:
        """Find the first component statisfying search condition"""
        for component in self.components:
            if (
                (name is None or component.name == name)
                and (kind is None or component.kind == kind)
            ):
                return component
        raise ValueError(f'Search with {name=} and {kind=} does not match any AttackComponent')
