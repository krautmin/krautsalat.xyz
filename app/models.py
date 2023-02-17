import datetime

from flask_mongoengine import MongoEngine

db = MongoEngine()


class PostModel(db.Document):
    class TypeChoices(db.Enum):
        NEWS = "news"
        PROJECT = "project"
        PAGE = "page"

    class CategoryChoices(db.Enum):
        NEWS = "news"
        PROJECT = "project"
        PAGE = "page"

    type = db.EnumField(TypeChoices, default=TypeChoices.NEWS)
    title = db.StringField(max_length=255, required=True)
    subtitle = db.StringField(max_length=255)

    description = db.StringField(max_length=1500)
    content = db.StringField()
    frontpage = db.BooleanField(required=True, default=False)
    pub_date = db.DateTimeField(default=datetime.datetime.now)
