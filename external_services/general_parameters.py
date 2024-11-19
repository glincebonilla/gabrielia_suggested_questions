import os
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json

class GeneralParametersController:
    def __init__(self):
        self.email = os.getenv('EMAIL_COROMBO')
        self.password = os.getenv('PASSWORD_COROMBO')
        self.token = ""

    def post_request(self, url, payload):
        session = requests.session()
        session.verify=False

        headers = {
            'Content-Type': 'application/json'
        }

        response = session.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
        response.raise_for_status()
        return response

    def get_request(self, url, headers):
        session = requests.session()
        session.verify=False

        response = session.request("GET", url, headers=headers)
        response.raise_for_status()
        return response
    
    def get_authorization_token(self):
        url = os.getenv("URL_TOKEN_AUTORIZATION_COROMBO")

        payload = {
            "email": self.email,
            "password": self.password
        }

        response = self.post_request(url, payload)
        response_object = json.loads(response.text)
        return response_object.get("token")

    def update_token(self):
        self.token = self.get_authorization_token()

    def get_general_parameters(self):
        url = os.getenv("URL_GENERAL_PARAMETERS_COROMBO")

        if not self.token:
            self.update_token()

        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        try:
            response = self.get_request(url, headers)
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                self.update_token()
                headers = {
                    'Authorization': f'Bearer {self.token}'
                }
                response = self.get_request(url, headers)
            else:
                raise

        return json.loads(response.text)

