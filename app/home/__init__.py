import datetime

from quart import current_app, Blueprint, redirect, render_template, send_from_directory
from quart_schema import DataSource, validate_request

from app.documents import ContactMessageDocument, PostDocument
from app.schemas import ContactMessage
from app.utils import send_mail

bp = Blueprint(
    "home",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@bp.context_processor
def inject_today_date():
    return {"date": datetime.date.today()}


@bp.route("/")
async def index():
    posts = await PostDocument.find(PostDocument.publish == True).to_list()
    return await render_template(
        "index.html",
        posts=posts,
    )


@bp.get("/media/<path:path>")
async def send_media(path):
    """
    :param path: a path like "posts/<int:post_id>/<filename>"
    """

    return await send_from_directory(
        directory=current_app.config["UPLOAD_FOLDER"],
        file_name=path,
        as_attachment=True,
    )


@bp.route("/message", methods=["POST"])
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
    return redirect("home:index")
