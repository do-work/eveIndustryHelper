# EVE Industry Helper
EVE Online industry and market helper.

## Requirements
- Python 3.7
- poetry
- virtualenv

## Install
1. `mkdir venv`
1. `virtualenv venv`
1. `source venv/bin/activate`
1. `poetry install`

## Setup
1. Create new app at https://developers.eveonline.com/applications
    1. Any "Name" and "description" will work.
    1. Connection Type = "Authentication & API Access".
    1. Permissions = Select the following scopes:
        1. esi-assets.read_assets.v1 
        1. esi-markets.read_character_orders.v1 
        1. esi-assets.read_corporation_assets.v1
    1. Callback URL = `http:localhost:9001/oauth-callback`
1. Copy `/config/env.example` as `/config/config.env` and populate the missing keys as follows:
    1. CLIENT_ID = From the eve app page
    1. CLIENT_SECRET = From the eve app page
    1. REFRESH_TOKEN =
        1. GET `/oauth/authorize`
        1. Authorize on CCP server which should redirect back to /oauth-callback containing the refresh token.
1. Get corporation_id
1. Get character_id
1. Get "location_id" of the station or structure
    1. If your location is not listed in reference#5 then create a corp contract to your location and GET /corp/contracts
1. Get "container_id" where your mats are stored at the location above         

## Run
1. `python app.py`
1. `POST /restock`
    1. Use the sample request at `/tests/http/restock.http`

## Note
If you need to change your scopes you will need to get a new refresh token. 

## Reference
1. ESI-Docs: https://github.com/esi/esi-docs  
1. Quick "Item Id" lookup: https://eve-files.com/chribba/typeid.txt  
1. Eve data dump (SDE - static data export): https://developers.eveonline.com/resource/resources  
1. Fuzzworks data dump: https://www.fuzzwork.co.uk/dump/latest/
1. Location_ids: https://www.adam4eve.eu/info_stations.php