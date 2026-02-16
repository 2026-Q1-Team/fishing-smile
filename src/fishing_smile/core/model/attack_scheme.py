from typing import (
    Annotated,
    List,
    Literal,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
)

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
    components: List[AnyAttackComponent] = []
