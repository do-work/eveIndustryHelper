import base64
import os

import requests
from flask import Request
from requests import Response


class Oauth:

    def __init__(self, config: dict):
        self.config = config

    def authorize(self) -> Response:
        url = self.get_authorize_endpoint()
        return requests.get(url)

    def get_authorize_endpoint(self) -> str:
        redirect_uri = os.getenv("REDIRECT_URI")
        scopes = os.getenv("SCOPES")

        # todo -> add state
        return f"{self.config['LOGIN_SERVER_BASE']}/oauth/authorize?response_type=code&redirect_uri={redirect_uri}" \
               f"&client_id={self.config['CLIENT_ID']}&scope={scopes}"

    def callback(self, request: Request):
        response = self.request_oauth_token(self.get_access_token_payload(self.get_code_from_callback_uri(request)))
        access_token = self.get_access_token(response)
        refresh_token = self.get_refresh_token(response)

    def get_code_from_callback_uri(self, request: Request) -> str:
        args = request.args
        if "code" not in args:
            # todo -> look at Flask error handling
            raise RuntimeError()
        return args["code"]

    def get_access_token(self, response: Response) -> str:
        """
        Get the access token.
        Only lasts for 20 minutes.
        :param response:
        :return:
        """
        return response.json()["access_token"]

    def get_refresh_token(self, response: Response) -> str:
        return response.json()["refresh_token"]

    def request_oauth_token(self, payload: dict) -> Response:
        url = f"{self.config['LOGIN_SERVER_BASE']}/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": self.construct_auth_code()
        }
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response

    def construct_auth_code(self) -> str:
        auth_code_raw = f"{self.config['CLIENT_ID']}:{self.config['CLIENT_SECRET']}"
        return f"Basic {base64.b64encode(auth_code_raw.encode()).decode()}"

    def get_access_token_payload(self, access_code: str) -> dict:
        return {
            "grant_type": "authorization_code",
            "code": access_code
        }

    def get_refresh_token_payload(self) -> dict:
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.config['REFRESH_TOKEN']
        }

    def get_refreshed_access_token(self) -> str:
        response = self.request_oauth_token(self.get_refresh_token_payload())
        return self.get_access_token(response)
