from flask import Flask, jsonify
from flask import request

from controllers.oauth import Oauth
from eveAPI import EveAPI
from services.itemLookup import ItemLookup
from services.restock import Restock
from settings import Config


app = Flask(__name__)
app.config.from_object(Config())


@app.route("/", methods=["GET"])
def index():
    return "Eve Market Helper"


@app.route("/oauth/authorize", methods=["GET"])
def authorize():
    # todo -> add redirect
    return Oauth(app.config).get_authorize_endpoint()


@app.route("/oauth-callback", methods=["GET"])
def callback():
    return jsonify(Oauth(app.config).callback(request))


@app.route("/restock", methods=["POST"])
def restock():
    payload = request.json["payload"]
    restock_results = Restock(EveAPI(Oauth()), ItemLookup()).run(payload)

    return jsonify(restock_results)


if __name__ == "__main__":
    app.run()
