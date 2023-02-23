from quart import Blueprint, render_template, request

bp = Blueprint("home", __name__, template_folder="templates")


@bp.route("/")
async def home():
    return await render_template("index.html")
