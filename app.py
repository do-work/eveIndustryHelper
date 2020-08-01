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


@app.route("/corp/contracts", methods=["GET"])
def corp_contracts():
    results = EveAPI(Oauth(app.config), config=app.config).get_corp_contracts(98098444)
    return jsonify(list(results))


@app.route("/asset/locations",  methods=["GET"])
def asset_locations():
    corp_assets = CorpAssets(EveAPI(Oauth(app.config), config=app.config), ItemLookup(app.config))
    corp_asset_locations = corp_assets.get_location_ids_for_all_corp_assets(98098444)
    return jsonify(list(corp_asset_locations))


@app.route("/asset/<int:item_id>/locate", methods=["GET"])
def asset_location_by_structure_location(item_id: int):
    corp_assets = CorpAssets(EveAPI(Oauth(app.config), config=app.config), ItemLookup(app.config))
    asset_results = corp_assets.get_corp_assets(98098444)
    corp_asset_locations = corp_assets.get_items_location_ids_from_assets(asset_results, item_id)

    return jsonify(list(corp_asset_locations))


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
