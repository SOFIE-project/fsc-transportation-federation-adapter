import base64
import json

from django.conf import settings
from django.utils.functional import cached_property
from indy import wallet, IndyError, did, crypto
from indy.error import ErrorCode

from api.decorators import try_sync
from api.eth import EthereumClient


class IndyClient:
    """Indy client wrapper
    """
    client = {
        'wallet_config': json.dumps({'id': 'wallet', "storage_config": {"path": settings.INDY_WALLET_PATH}}),
        'wallet_credentials': json.dumps({'key': settings.INDY_WALLET_PASSWORD}),
    }

    @cached_property
    def did(self):
        return self.get_or_create_wallet_did()

    @try_sync
    async def get_or_create_wallet_did(self):
        """ Gets or creates the wallet, did & verification did of the given F.A.

        Returns:
            tuple - the did, verkey pair
        """
        eth_client = EthereumClient()
        wallet_address = eth_client.signer_address

        client_seed = wallet_address[2:] + '000000000000000000000000'

        try:
            await wallet.create_wallet(self.client['wallet_config'], self.client['wallet_credentials'])
        except IndyError as ex:
            if ex.error_code == ErrorCode.WalletAlreadyExistsError:
                pass

        wallet_handle = await wallet.open_wallet(self.client['wallet_config'], self.client['wallet_credentials'])
        client_did, client_verkey = await did.create_and_store_my_did(
            wallet_handle, json.dumps({'seed': client_seed}))
        await wallet.close_wallet(wallet_handle)
        return client_did, client_verkey

    @try_sync
    async def sing_challenge(self, challenge):
        """Signs the given challenge payload

        Args:
            challenge (str): the payload to sign

        Returns:
            str - the signed signature in base64 form
        """
        _, verkey = self.did
        wallet_handle = await wallet.open_wallet(self.client['wallet_config'], self.client['wallet_credentials'])
        signature = await crypto.crypto_sign(wallet_handle, verkey, challenge.encode())
        signature64 = base64.b64encode(signature)
        await wallet.close_wallet(wallet_handle)
        return signature64
