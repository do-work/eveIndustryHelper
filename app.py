from flask import Flask

from controllers.oauth import Oauth

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "Eve Market Helper"


@app.route("/oauth/authorize", methods=["GET"])
def oauth():
    Oauth().authorize()


if __name__ == "__main__":
    app.run()
