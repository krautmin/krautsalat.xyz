import datetime
from typing import List, Optional

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, SecretStr, root_validator
from pymongo import DESCENDING, ASCENDING, TEXT
from slugify import slugify


beanie_init_list = [
    "app.documents.PostDocument",
    "app.documents.UserDocument",
    "app.documents.ContactMessageDocument",
]


class ContactMessageDocument(Document):
    name: str
    email: str
    message: str
    created_at: datetime.datetime
    send_at: Optional[datetime.datetime] = None


class UserDocument(Document):
    uname: Indexed(str, TEXT, unique=True)
    password: str
    registered_at: datetime.datetime


class PostContentEmbedded(BaseModel):
    introduction: str
    body: Optional[str] = None


class PostDocument(Document):
    title: Indexed(str, TEXT, unique=True)
    subtitle: Optional[str] = None
    content: PostContentEmbedded
    tags: List[str] = []
    slug: Optional[str] = None
    publish: bool
    created_at: datetime.datetime
    modified_at: Optional[datetime.datetime] = None

    @root_validator(pre=True)
    def generate_slug(cls, values):
        if values.get("slug") is not None:
            return values
        title = values.get("title")
        slug = slugify(title)
        values["slug"] = slug
        return values

    class Config:
        collection = "posts"
