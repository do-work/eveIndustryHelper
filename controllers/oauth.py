import os


class Oauth:

    def authorize(self):
        redirect_uri = os.getenv("REDIRECT_URI")
        client_id = os.getenv("CLIENT_ID")
        scopes = os.getenv("SCOPES")

        # todo -> add state
        url = f"https://login.eveonline.com/oauth/authorize?response_type=code&redirect_uri={redirect_uri}&client_id={client_id}&scope={scopes}"
