from typing import (
    Annotated,
    Union,
)

import yaml
from pydantic import (
    BaseModel,
    Field,
)

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


class AttackScheme(BaseModel):
    name: str = Field(description = 'short, snake_case, unique name')
    description: str | None = Field(None, description = 'longer, human readable explanation')
    components: SearchList[AnyAttackComponent] = SearchList()

    @classmethod
    def from_file(cls, path: Path):
        try:
            with path.open() as f:
                doc = yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f'Can not load scheme from {path}') from e

        return cls.model_validate(doc, context = {'base_directory': path.parent})
