from bson.json_util import dumps, loads
import datetime
import functools
from uuid import uuid4

from quart import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from quart_schema import hide
from werkzeug.security import check_password_hash

from .documents import UserDocument
from .schemas import UserBase
from secrets import compare_digest

bp = Blueprint("auth", __name__, template_folder="templates")


def api_key_required(view):
    @functools.wraps(view)
    async def decorator(*args, **kwargs):
        token = None
        # ensure the api key is passed with the headers
        if "x-api-key" in request.headers:
            token = request.headers["x-api-key"]
        if not token:  # throw error if no token provided
            return {"message": "A valid token is missing!"}, 401
        elif not compare_digest(token, current_app.config["API_KEY"]):
            return {"message": "Invalid token!"}, 401
        return await view(*args, **kwargs)

    return decorator


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
async def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = await UserDocument.get(loads(user_id))


@bp.route("/login", methods=["GET", "POST"])
@hide
async def login():
    if request.method == "POST":
        uname = (await request.form)["uname"]
        password = (await request.form)["password"]
        user = await UserDocument.find_one(UserDocument.uname == uname)
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."
        else:
            session.clear()
            session["user_id"] = dumps(user.id)
            return redirect(url_for("home.index"))
        await flash(error)

    return await render_template("login.html")


@bp.route("/logout")
@hide
def logout():
    session.clear()
    return redirect(url_for("home.index"))
