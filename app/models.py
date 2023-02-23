import datetime

from app import db

posts_collection = db.posts


# Post API DB Model
class PostImage(db.EmbeddedDocument):
    image_path = db.ImageField(required=True)
    alt_text = db.StringField(max_length=50)


class PostFile(db.EmbeddedDocument):
    file = db.FileField(required=True)
    alt_name = db.StringField(max_length=50)


class PostContent(db.EmbeddedDocument):
    title = db.StringField(max_length=120, required=True)
    subtitle = db.StringField(max_length=240)
    introduction = db.StringField(max_length=1000)
    content = db.StringField()
    images = db.EmbeddedDocumentListField(document_type=PostImage)
    files = db.EmbeddedDocumentListField(document_type=PostFile)
    tags = db.ListField(field=db.StringField(max_length=30), required=True)


class Post(db.Document):
    post_id = db.IntField(primary_key=True)
    content = db.EmbeddedDocumentField(document_type=PostContent, required=True)
    date_created = db.DateTimeField(default=datetime.datetime.utcnow, required=True)
    date_modified = db.DateTimeField(default=datetime.datetime.utcnow)
    active = db.BooleanField(default=True, required=True)
