from typing import Iterable, Tuple, Union

# As a BIP44Wallet is an improvement on BIP22 Wallets, we therefore have to import BIP32 so as to create a BIP44 BIP44Wallet
from bip32 import BIP32, HARDENED_INDEX

# mnemonic library is used to import BIP39 multi-language passphrase functionality
# https://pypi.org/project/mnemonic/
from mnemonic import Mnemonic
#algosdk does not have multi-language passphrase functionality for its mnemonics/passphrases
#from algosdk import mnemonic

from .coins import COIN_PATHS, coin_path_by_index

__all__ = ("BIP44Wallet")


class BIP44Wallet:
    def __init__(self, mnemonic: str, language: str = "english", passphrase: str = ""):
        """
        BIP44 HD BIP44Wallet with a master mnemonic.
        :param mnemonic (str): The master mnemonic to derive keys
        :param language (str, optional): The mnemonic's language, default: "english", 
        others are -> "french", "chinese_simplified", "chinese_traditional", "italian", "japanese"
        "korean", and finally "spanish"
        :param passphrase (str, optional): The mnemonic's passphrase, default: ""
        """
        self._seed = Mnemonic(language).to_seed(mnemonic, passphrase)
        self._bip32 = BIP32.from_seed(self._seed)

    def _derive_secret(self, path: Union[str, Iterable[int]]) -> bytes:
        return self._bip32.get_privkey_from_path(path)

    def _derive_public(self, path: Union[str, Iterable[int]]) -> bytes:
        return self._bip32.get_pubkey_from_path(path)

    def derive_secret_key(self, path: str) -> bytes:
        """
        Derive secret key from path.
        Args:
            :param path (str): Key path, e.g. m/44'/0'/0'/0/0
        Returns:
            bytes: Bytes of secret/private key
        """
        return self._derive_secret(path)

    def derive_public_key(self, path: str) -> bytes:
        """
        Derive public key from path.
        Args:
            :param path (str): Key path, e.g. m/44'/0'/0'/0/0
        Returns:
            bytes: Bytes of public key, compressed format
        """
        return self._derive_public(path)

    def derive_account(
        self,
        coin: Union[str, int],
        account: int = 0,
        change: int = 0,
        address_index: int = 0,
    ) -> Tuple[bytes, bytes]:
        """
        Derive secret and public key of account, following BIP44 standard like `m / purpose' / coin_type' / account' / change / address_index`.
        Args:
            :param coin (Union[str, int]): e.g. BTC, ALGO/ASAs or ETH, respectively, 0, 283 or 60 in index
            :param account (int, optional): Account index, each user should have one
            :param change (int, optional): 0 for receiving payments and 1 for receiving changes, see BIP44 for details
            :param address_index (int, optional): Starting from 0
        Returns:
            Tuple[bytes, bytes]: Secret key and public key
        """
        if isinstance(coin, str):
            coin_path = COIN_PATHS[coin.upper()]
        else:
            coin_path = coin_path_by_index(coin)

        account_path = (account + HARDENED_INDEX, change, address_index)
        path = coin_path + account_path
        return (self._derive_secret(path), self._derive_public(path))