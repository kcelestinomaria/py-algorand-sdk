import base64
import os
from utils import get_algod_client, get_accounts
from algosdk import transaction
from algosdk import encoding

# example: CODEC_ADDRESS
address = "4H5UNRBJ2Q6JENAXQ6HNTGKLKINP4J4VTQBEPK5F3I6RDICMZBPGNH6KD4"
pk = encoding.decode_address(address)
addr = encoding.encode_address(pk)

assert addr == address
# example: CODEC_ADDRESS

# example: CODEC_BASE64
encoded_str = "SGksIEknbSBkZWNvZGVkIGZyb20gYmFzZTY0"
decoded_str = base64.b64decode(encoded_str).decode("utf-8")
print(decoded_str)
# example: CODEC_BASE64

# example: CODEC_UINT64
val = 1337
encoded_uint = val.to_bytes(8, "big")
decoded_uint = int.from_bytes(encoded_uint, byteorder="big")
assert decoded_uint == val
# example: CODEC_UINT64


algod_client = get_algod_client()
acct = get_accounts().pop()
# example: CODEC_TRANSACTION_UNSIGNED
sp = algod_client.suggested_params()
pay_txn = transaction.PaymentTxn(acct.address, sp, acct.address, 10000)

# Write message packed transaction to disk
with open("pay.txn", "w") as f:
    f.write(encoding.msgpack_encode(pay_txn))

# Read message packed transaction and decode it to a Transaction object
with open("pay.txn", "r") as f:
    recovered_txn = encoding.msgpack_decode(f.read())

print(recovered_txn.dictify())
# example: CODEC_TRANSACTION_UNSIGNED

os.remove("pay.txn")

# example: CODEC_TRANSACTION_SIGNED
# Sign transaction
spay_txn = pay_txn.sign(acct.private_key)
# write message packed signed transaction to disk
with open("signed_pay.txn", "w") as f:
    f.write(encoding.msgpack_encode(spay_txn))

# read message packed signed transaction into a SignedTransaction object
with open("signed_pay.txn", "r") as f:
    recovered_signed_txn = encoding.msgpack_decode(f.read())

print(recovered_signed_txn.dictify())
# example: CODEC_TRANSACTION_SIGNED


os.remove("signed_pay.txn")

# example: CODEC_BLOCK
# example: CODEC_BLOCK
