import base64
import os

import requests
from flask import Request
from requests import Response


class Oauth:

    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.login_server_base = None

    def authorize(self):
        redirect_uri = os.getenv("REDIRECT_URI")
        scopes = os.getenv("SCOPES")

        # todo -> add state
        url = f"{self.login_server_base}/oauth/authorize?response_type=code&redirect_uri={redirect_uri}&client_id={self.get_client_id()}&scope={scopes}"

        requests.get(url)

    def callback(self, request: Request):
        access_code = self.get_code_from_callback_uri(request)
        access_token = self.get_access_token(access_code)

    def get_code_from_callback_uri(self, request: Request) -> str:
        args = request.args
        if "code" not in args:
            # todo -> look at Flask error handling
            raise RuntimeError()
        return args["code"]

    def get_access_token(self, access_code: str) -> str:
        """
        Get the access token.
        Only lasts for 20 minutes.
        :param access_code:
        :return:
        """
        response = self.request_oauth_token(access_code)
        return response.json()["access_token"]

    def request_oauth_token(self, access_code: str) -> Response:
        url = f"{self.get_login_server_base()}/oauth/token"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.construct_auth_code()
        }
        payload = {
            "grant_type": "authorization_code",
            "code": access_code
        }
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response

    def get_login_server_base(self) -> str:
        if not self.login_server_base:
            self.login_server_base = os.getenv("LOGIN_SERVER_BASE")
        return self.login_server_base

    def get_client_id(self) -> str:
        if not self.client_id:
            self.client_id = os.getenv("CLIENT_ID")
        return self.client_id

    def get_client_secret(self) -> str:
        if not self.client_secret:
            self.client_secret = os.getenv("CLIENT_SECRET")
        return self.client_secret

    def construct_auth_code(self) -> str:
        return base64.b64encode(f"Basic{self.get_client_id()}:{self.get_client_secret()}")
