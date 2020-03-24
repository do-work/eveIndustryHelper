from flask import Flask
from flask import request

from controllers.oauth import Oauth

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "Eve Market Helper"


@app.route("/oauth/authorize", methods=["GET"])
def authorize():
    Oauth().authorize()


@app.route("/oauth-callback", methods=["GET"])
def callback():
    Oauth().callback(request)


if __name__ == "__main__":
    app.run()
