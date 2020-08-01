import sys
from flask import Flask, jsonify
from flask import request
from controllers.oauth import Oauth
from eveAPI import EveAPI
from services.corpAssets import CorpAssets
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
    result = Oauth(app.config).get_authorize_endpoint()
    return jsonify(result)


@app.route("/oauth-callback", methods=["GET"])
def callback():
    refresh_token = Oauth(app.config).callback(request)
    return jsonify({"refresh_token": refresh_token})


@app.route("/restock", methods=["POST"])
def restock():
    _restock = Restock(EveAPI(Oauth(app.config), config=app.config), ItemLookup(app.config))
    restock_results = _restock.run(request.json["payload"])
    output_param = request.args.get("output")
    if output_param and output_param == 'text':
        restock_results = _restock.format_for_clipboard(restock_results)
        sys.stdout.write(str(restock_results))
    return jsonify(restock_results)


if __name__ == "__main__":
    app.run()
