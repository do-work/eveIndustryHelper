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
1. Select the following scopes:
    1. esi-assets.read_assets.v1 
    1. esi-markets.read_character_orders.v1 
    1. esi-assets.read_corporation_assets.v1
1. Create `.env` file and populate with keys from `.env.example`
1. Add the provided `Client ID` and `Secret Key` values to your `.env` file.

### SSO (one time only)
GET `/oauth/authorize`  
Authorize on CCP server the first time.  
Debug into the app to get the refresh token and save token to .`env` file.

## Run
`python app.py`


## Reference
ESI-Docs: https://github.com/esi/esi-docs  
Quick "Item Id" lookup: https://eve-files.com/chribba/typeid.txt  
Eve data dump (SDE - static data export): https://developers.eveonline.com/resource/resources  
Fuzzworks data dump: https://www.fuzzwork.co.uk/dump/latest/