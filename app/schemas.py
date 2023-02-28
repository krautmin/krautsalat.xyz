import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, SecretStr


# Contact Form Schemas
class ContactMessage(BaseModel):
    fname: str
    lname: str
    email: EmailStr
    message: str


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    password: SecretStr


# Post Schemas
class PostContentNested(BaseModel):
    introduction: str
    body: str | None


class PostAddSchema(BaseModel):
    title: str
    subtitle: str | None
    content: PostContentNested
    slug: str | None
    tags: List[str] = []
    publish: bool


class PostUpdate(BaseModel):
    content: PostContentNested
    publish: bool


class PostIDQuery(BaseModel):
    id: int | None


class PostMotor(BaseModel):
    id: int
    publish: bool
    content: PostContentNested
    date_created: datetime.datetime
    date_modified: datetime.datetime | None
