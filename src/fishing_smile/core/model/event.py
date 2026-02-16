from datetime import datetime

from sqlalchemy import JSON
from sqlmodel import Field, Relationship

from fishing_smile.database.sqlmodel import SQLModel


class Event(SQLModel):
    id: int | None = Field(
        default = None,
        primary_key = True,
    )
    parent_attack_id:  int | None = Field(
        default = None,
        foreign_key = 'attack.id',
        ondelete = 'CASCADE',
    )
    # TODO: create custome string type that can split into
    # - kind.component (nullable for events not associated with attack itself
    #   but not any particular component)
    # - and kind.what which indicate kind of event unique within each component.
    kind: str = Field(
        max_length = 64,
        index = True,
    )
    # TODO: Config default to NOW in database too.
    # The default is only apply to python side currently
    time: datetime = Field(
        default_factory = datetime.now,
        index = True,
    )
    detail: dict | None = Field(
        default = None,
        sa_type = JSON,
    )


class EventTable(Event, table = True):
    parent_attack: 'AttackTable' = Relationship(back_populates = 'events')
