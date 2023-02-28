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
from quart_schema import DataSource, validate_request
from werkzeug.security import check_password_hash, generate_password_hash

from .documents import UserDocument
from .schemas import UserBase


bp = Blueprint("auth", __name__)


def api_key_required(f):
    @functools.wraps(f)
    async def decorator(*args, **kwargs):
        token = None
        # ensure the api key is passed with the headers
        if "x-api-key" in request.headers:
            token = request.headers["x-api-key"]
        if not token:  # throw error if no token provided
            return {"message": "A valid token is missing!"}, 401
        elif token != current_app.config["API_KEY"]:
            return {"message": "Invalid token!"}, 401
        return await f(*args, **kwargs)

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
        g.user = await UserDocument.get(user_id)


@bp.route("/register", methods=["GET", "POST"])
@validate_request(UserBase, source=DataSource.FORM)
async def register(data):
    if request.method == "POST":
        email = data.email
        password = data.password
        user = UserDocument(
            email=email,
            password=generate_password_hash(password),
            registered_at=datetime.datetime.now(),
        )
        if await UserDocument.find_one(UserDocument.email == email) is None:
            await user.insert()
        else:
            error = f"Email '{email}' is already registered."
        await flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
@validate_request(UserBase, source=DataSource.FORM)
async def login(data: UserBase):
    if request.method == "POST":
        email = data.email
        password = data.password
        user = await UserDocument.find_one(UserDocument.email == email)
        if user is None:
            error = "Incorrect email."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        await flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home.index"))
