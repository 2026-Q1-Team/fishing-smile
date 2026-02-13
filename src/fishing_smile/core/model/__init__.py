from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


#Python Classes

class RedFlag(BaseModel):
    kind: str
    name: str
    explanation: str

class AttackComponent(BaseModel):
    kind: str
    name: str
    red_flags: List[RedFlag] = Field(default_factory=list)

class EmailComponent(AttackComponent):
    email_template: str

class HTMLComponent(AttackComponent):
    url: str
    html_template: str

class APIComponent(AttackComponent):
    url: str


class AttackScheme(BaseModel):
    name: str
    components: List[Union[EmailComponent, HTMLComponent, APIComponent]] = Field(default_factory=list)


#Database Tables

class TargetProfile(BaseModel):
    id: Optional[str] = Field(None, alias="UniqueID")
    name: str
    email: EmailStr
    phone_number: str | None = None
    company: str | None = None
    job_title: str | None = None

class Event(BaseModel):
    id: Optional[str] = Field(None, alias="UniqueID")
    part_of_which_attack: str
    kind: str
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[dict] = None

class Attack(BaseModel):
    id: Optional[str] = Field(None, alias="UniqueID")
    unique_random_code: str 
    scheme: str  # AttackScheme
    target: str  # TargetProfile?