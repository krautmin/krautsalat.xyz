import datetime

from bson.json_util import dumps

from quart import Blueprint, request
from quart_schema import validate_request, validate_querystring, DataSource
from werkzeug.security import generate_password_hash

from .auth import api_key_required
from .documents import PostDocument, UserDocument
from .schemas import PostAddSchema, PostUpdate, PostIDQuery, PostMotor, UserBase


bp = Blueprint("api", __name__)


@bp.post("/user/add")
@api_key_required
@validate_request(UserBase)
async def register(data):
    if request.method == "POST":
        uname = data.uname
        password = data.password
        user = UserDocument(
            uname=uname,
            password=generate_password_hash(password),
            registered_at=datetime.datetime.now(),
        )
        if await UserDocument.find_one(UserDocument.uname == uname) is None:
            await user.insert()
        else:
            return {"message": f"Username '{uname}' is already registered."}
        return {"message": f"successfully registered user '{uname}'"}


@bp.route("/post/add", methods=["POST"])
@api_key_required
@validate_request(PostAddSchema)
async def add_post(data):
    document = PostDocument(
        title=data.title,
        content=data.content,
        slug=data.slug,
        tags=data.tags,
        publish=data.publish,
        created_at=datetime.datetime.now(),
    )
    await document.insert()
    return dumps(document), 201


@bp.route("/post/update/", methods=["PUT"])
@api_key_required
@validate_querystring(PostIDQuery)
@validate_request(PostUpdate)
async def update_post(query_args, data):
    if not query_args.id:
        return {"message": "You didn't provide a post id to update."}, 400
    post_id = query_args.id
    old_document = await PostDocument.get(post_id)
    if not old_document:
        return {"message": "The provided post id couldn't be found."}, 404
    doc_id = old_document["_id"]
    created_at = old_document["date_created"]
    new_document = PostMotor(
        id=post_id,
        content=data.content,
        publish=data.publish,
        date_created=created_at,
        date_modified=datetime.datetime.now(),
    )
    # await db.posts.replace_one({"_id": doc_id}, new_document.dict())
    return new_document, 201


@bp.route("/post/delete/", methods=["DELETE"])
@api_key_required
@validate_querystring(PostIDQuery)
async def delete_post(query_args):
    if not query_args.id:
        return {"message": "You didn't provide a post id to delete."}, 400
    post_id = query_args.id
    # old_document = await db.posts.find_one_and_delete({"id": post_id})
    return {"message": f"The post with id={post_id} has been deleted."}, 201
