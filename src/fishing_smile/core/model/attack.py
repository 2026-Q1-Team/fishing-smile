from functools import cached_property

from sqlalchemy import CHAR
from sqlmodel import Field, Relationship

from fishing_smile.database.sqlmodel import SQLModel
from .attack_scheme import AttackScheme


class Attack(SQLModel):
    id: int | None = Field(
        default = None,
        primary_key = True,
    )
    external_id: str = Field(
        unique = True,
        min_length = 32,
        max_length = 32,
        sa_type = CHAR(32),
    )
    scheme_name: str = Field(
        max_length = 32,
        index = True,
    )
    # TODO: should be able to create in-memeory Attack
    # referencing in-memory target without ID
    target_id: int = Field(
        foreign_key = 'target_profile.id',
        ondelete = 'CASCADE',
    )

    @cached_property
    def scheme(self) -> AttackScheme:
        # TODO: Validate scheme_name on construction of Attack?
        # TODO: Do we allow assignment of AttackScheme object on this property?
        return AttackScheme.get(self.scheme_name)


class AttackTable(Attack, table = True):
    target: 'TargetProfileTable' = Relationship(back_populates = 'attacks')
    events: list['EventTable'] = Relationship(back_populates = 'parent_attack')
