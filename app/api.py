import datetime

from quart import Blueprint, request

from marshmallow import Schema
from webargs import fields, validate
from .utils.auth import api_key_required
from .utils.caching import aio_cache
from .utils.quartparser import use_args, use_kwargs


bp = Blueprint("api", __name__)


class PostsGetSchema(Schema):
    date_start = fields.Date(missing=datetime.date.today())
    date_end = fields.Date()
    drafts = fields.Bool()


@bp.route("/posts", methods=["GET"])
@api_key_required
@aio_cache(timeout=5 * 60)
@use_args(PostsGetSchema(), location="json")
async def get_posts(args):
    """Posts detail view.
    ---
    get:
      parameters:
      - in: path
        schema: PostsGetSchema
      responses:
        200:
          content:
            application/json:
              schema: PostSchema
    """
    return {"schema": "lol"}
