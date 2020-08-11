import json

from api.eth import EthereumClient
from api.pds import PDSClient


class EthereumHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.eth_client = EthereumClient()

    def __call__(self, request):
        api_call = False

        # If its an api call
        if '/api' in request.path:
            api_call = True

        response = self.get_response(request)

        # If api call was valid, append ethereum signature headers
        if api_call and response.status_code == 200:
            signed_data = self.eth_client.sign_message(json.dumps(response.data))
            response['X-signature'] = signed_data.signature.hex()
            response['X-hash'] = signed_data.messageHash.hex()
        return response


class PdsJwtMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.pds_client = PDSClient()

    def __call__(self, request):
        api_call = False

        # If its an api call
        if '/api' in request.path:
            api_call = True

        response = self.get_response(request)

        # If api call was valid, append pds jwt token
        if api_call and response.status_code == 200:
            jwt = self.pds_client.jwt
            response['Authorization'] = 'Token {}'.format(jwt)
        return response
