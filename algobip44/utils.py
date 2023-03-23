from typing import Union
from algosdk import account
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError
import nacl.hash
from nacl.public import PublicKey

HASHER = nacl.hash.sha256

def nacl_sha256(b: bytes) -> bytes:
    #h = keccak.new(data=b, digest_bits=256)
    generated_hash = HASHER(msg=b, encoder=nacl.encoding.HexEncoder)
    return generated_hash



# Generate/Recover ALGO Accounts & convert to checksum
# ALGO accounts(24 words + 1 checksum)
def convert_ALGO_account_to_checksum():
    """
    Convert generated ALGO account to checksum address

    Returns:
        
    """
    private_key, address = algosdk.generate_account()

    # get checksum address from below
    address_hash = nacl_sha256(address.encode()).hex()

    res = []
    for a, h in zip(address, address_hash):
        if int(h, 16) >= 8:
            res.append(a.upper())
        else:
            res.append(a)

    return "0x" + "".join(res)


# Get ALGO Account Address
def get_ALGO_addr(pk: Union[str, bytes]) -> str:
    """
    Return the address for the ALGO account.

    Args:
        private_key (str): private key of the account in base64

    Returns:
        str: address of the account
    """
    pk = algosdk.address_from_private_key()
    #OR
    # get/hardcode already generated account details for this example
    
    pk_bytes = bytes.fromhex(pk) if isinstance(pk, str) else pk

    if len(pk_bytes) != 64:
        pk_bytes = PublicKey(pk_bytes).format(False)[1:]

    return convert_ALGO_account_to_checksum(f"0x{nacl_sha256((pk_bytes)[-20:].hex())}")
    #(f"0x{keccak_256(pk_bytes)[-20:].hex()}")
