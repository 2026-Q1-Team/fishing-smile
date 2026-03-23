from typing import (
    Annotated,
    Union,
)

import yaml
from pydantic import (
    BaseModel,
    Field,
    model_validator,
)

from .attack_component import (
    EmailComponent,
    HTMLComponent,
    APIComponent,
)
from .search_list import SearchList

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

    @model_validator(mode = 'after')
    # TODO -- fix typo, change "unqiue" to "unique"
    def components_have_unqiue_kind_name_pair(self):
        seen = set()
        for component in self.components:
            key = (component.kind, component.name)
            if key in seen:
                raise ValueError(f'components within a scheme must have unique kind-name pair but {key} is duplicated')
            seen.add(key)
        return self
