import datetime
from pathlib import Path

import aiofiles
from markdown import markdown

from quart import (
    current_app,
    Blueprint,
    redirect,
    render_template,
    request,
    send_from_directory,
)
from quart_schema import DataSource, validate_request, hide

from app.documents import ContactMessageDocument, PostDocument
from app.schemas import ContactMessage
from app.utils import send_mail

bp = Blueprint("home", __name__, template_folder="templates")


@bp.get("/")
@hide
async def index():
    posts = (
        await PostDocument.find(PostDocument.publish == True)
        .sort(-PostDocument.created_at)
        .to_list()
    )
    return await render_template(
        "index.html",
        posts=posts,
    )


@bp.get("/about")
@hide
async def page_about():
    async with aiofiles.open(
        f"{Path(__file__).resolve().parent.parent.parent}/README.md", mode="r"
    ) as f:
        content = await f.read()
    return await render_template(
        "page_about.html",
        markdown=markdown(content),
    )


@bp.get("/media/<path:path>")
@hide
async def send_media(path):
    """
    :param path: a path like "posts/<int:post_id>/<filename>"
    """

    return await send_from_directory(
        directory=current_app.config["UPLOAD_FOLDER"],
        file_name=path,
        as_attachment=True,
    )


@bp.post("/message")
@hide
@validate_request(ContactMessage, source=DataSource.FORM)
async def send_message(data):
    message = ContactMessageDocument(
        name=f"{data.lname}, {data.fname}",
        email=data.email,
        message=data.message,
        created_at=datetime.datetime.now(),
    )
    await message.save()
    await send_mail(
        subject="New message sent via krautsalat.xyz!",
        content=f"From: {message.name}\nReply to: {message.email}\nMessage:\n'{message.message}'\nTimestamp: {message.created_at}",
    )
    return await render_template("partials/part_contact_success.html")


@bp.get("/message/new")
@hide
async def new_message():
    if request.headers.get("HX-Request"):
        return await render_template("partials/part_contact.html")
    return redirect("home.index")


@bp.get("/posts/add")
@hide
async def post_add():
    return await render_template("post_add.html")

