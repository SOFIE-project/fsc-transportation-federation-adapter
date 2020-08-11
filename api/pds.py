import logging
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.utils.functional import cached_property

from api.indy import IndyClient

log = logging.getLogger(__name__)


class PDSClient:
    """PDS client wrapper.

    Performs the challenge <> response component flow.
    """
    endpoints = {
        'token': '/gettoken'
    }

    def __init__(self):
        self.base_uri = settings.PDS_URI
        self.indy_client = IndyClient()

    @cached_property
    def jwt(self):
        return self.retrieve_jwt()

    def retrieve_jwt(self):
        """Performs the PDS challenge <> response flow

        Returns:
            str - the generated JWT token or None if any error occurred
        """
        did, verkey = self.indy_client.did

        # Challenge
        endpoint = urljoin(self.base_uri, self.endpoints['token'])
        payload = {'grant-type': 'DID', 'grant': did}

        try:
            r = requests.post(endpoint, data=payload)

            if r.status_code == 401:
                response = r.json()
                challenge = response['challenge']
            else:
                log.error('Received status_code={} and response={} while generating challenge for did={}'.format(
                    r.status_code, r.text, did
                ))
                return None
        except Exception as e:
            log.error('Exception while generating challenge for did={}. Reason: {}'.format(
                did, str(e)
            ), exc_info=True)
            return None

        # Sign the challenge
        signature64 = self.indy_client.sing_challenge(challenge)

        # Send back the challenge
        payload = {'grant-type': 'DID', 'grant': did, 'challenge': challenge, 'proof': signature64}

        try:
            r = requests.post(endpoint, data=payload)

            if r.status_code == 200:
                response = r.json()
                jwt = response['message']
            else:
                log.error('Received status_code={} and response={} while sending challenge for did={}'.format(
                    r.status_code, r.text, did
                ))
                return None
        except Exception as e:
            log.error('Exception while sending challenge for did={}. Reason: {}'.format(
                did, str(e)
            ), exc_info=True)
            return None
        return jwt
