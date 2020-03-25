import requests
from flask import Flask, jsonify
from flask import request

from controllers.oauth import Oauth
from settings import LOGIN_SERVER_BASE

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "Eve Market Helper"


@app.route("/oauth/authorize", methods=["GET"])
def authorize():
    # todo -> add redirect
    return Oauth().get_authorize_endpoint()


@app.route("/oauth-callback", methods=["GET"])
def callback():
    return jsonify(Oauth().callback(request))


@app.route("/toon_test", methods=["GET"])
def testing():
    # temporary endpoint for testing
    access_token = Oauth().get_refreshed_access_token()
    headers = {"authorization": f"Bearer {access_token}"}
    response = requests.get(f"{LOGIN_SERVER_BASE}/oauth/verify", headers=headers)
    return jsonify(response.json())


if __name__ == "__main__":
    app.run()
