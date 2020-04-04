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
        
## Run
1. `python app.py`
1. `POST /restock`
    1. Use the sample request at `/tests/http/restock.http`

## Reference
ESI-Docs: https://github.com/esi/esi-docs  
Quick "Item Id" lookup: https://eve-files.com/chribba/typeid.txt  
Eve data dump (SDE - static data export): https://developers.eveonline.com/resource/resources  
Fuzzworks data dump: https://www.fuzzwork.co.uk/dump/latest/