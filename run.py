from flask import Flask, render_template
from flask.helpers import get_root_path

from pymongo import monitoring
from waitress import serve
from whitenoise import WhiteNoise

from flask_htmx import HTMX
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_mongoengine.panels import mongo_command_logger
from flask_mongorest import MongoRest


app = Flask(__name__)

app.config.from_object("config.Config")
if app.config["DEPLOYED"]:
    app.config.from_object("config.ProdConfig")
else:
    from flask_debugtoolbar import DebugToolbarExtension

    app.config.from_object("config.DevConfig")
    DebugToolbarExtension(app)

db = MongoEngine()
db.init_app(app)

api = MongoRest(app)

app.session_interface = MongoEngineSessionInterface(db)
app.url_map.strict_slashes = False
app.wsgi_app = WhiteNoise(app.wsgi_app, root=get_root_path("run") + "/static/")
monitoring.register(mongo_command_logger)

htmx = HTMX(app)


@app.route("/")
def home():
    if htmx:
        return render_template("partials/part_index.html")
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
