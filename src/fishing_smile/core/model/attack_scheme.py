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
    name: str
    components: List[AnyAttackComponent] = []
