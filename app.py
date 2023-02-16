from flask import Flask
from flask import render_template
from flask_htmx import HTMX

app = Flask(__name__)
htmx = HTMX(app)


@app.route("/")
def home():
    if htmx:
        return render_template("partials/part_index.html")
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
