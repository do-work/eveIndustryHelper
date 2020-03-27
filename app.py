from flask import Flask, jsonify
from flask import request

from controllers.oauth import Oauth
from eveAPI import EveAPI
from services.restock import Restock

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


@app.route("/corp/assets", methods=["GET"])
def corp_assets():
    corp_assets_results = Restock(EveAPI(Oauth())).run()

    return jsonify(corp_assets_results)


if __name__ == "__main__":
    app.run()
