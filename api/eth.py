import json

from django.conf import settings
from django.utils.functional import cached_property
from eth_account import Account
from web3 import Web3


class Singleton(type):
    """Simple singleton implementation."""

    _instances = {}

    def __call__(cls, *args, **kwargs):  # noqa: N805
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EthereumClient(metaclass=Singleton):
    def __init__(self):
        self.web3 = Web3()
        self.keyfile = settings.ETHEREUM_WALLET_PATH

    @cached_property
    def signer_address(self):
        """Retrieves the public key from the keystore file

        Returns:
            str: the wallet address in hexstring form
        """
        with open(self.keyfile) as f:
            data = json.load(f)

        return Web3.toChecksumAddress(data['address'])

    @cached_property
    def signer_password(self):
        """Retrieves the password of the keyfile

        Returns:
            str: the secret password
        """
        with open(settings.ETHEREUM_WALLET_PASSWORD_PATH) as f:
            data = f.read().rstrip('\n')

        return data

    @cached_property
    def signer_key(self):
        """Decrypts the private key from keystore file using the password provider or the password.

        If both exist, the password will be used to unlock the targeted keystore file.

        Returns:
            bytes: the private key

        Raises:
            ValueError: if the password used from decryption is invalid
        """
        with open(self.keyfile) as f:
            data = json.load(f)

        return Account.decrypt(data, self.signer_password)

    def sign_message(self, message):
        """Signs a text message.

        Args:
            message: the text message to sign

        Returns:
            AttrDict: the signed message details
            {
                messageHash (HexBytes): keccak256 of the text message
                signature (HexBytes): signing signature
                r (int): the `r` part of the ECDSA signature
                s (int): the `s` part of the ECDSA signature
                v (int): the recovery id
            }
        """
        if not isinstance(message, str):
            raise TypeError('Message must be of type <str>')

        hash = Web3.sha3(text=message)
        signed_hash = self.web3.eth.account.signHash(hash, self.signer_key)

        return signed_hash
