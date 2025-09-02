from algosdk.v2client import algod
from algosdk.transaction import ApplicationCreateTxn, StateSchema, OnComplete, wait_for_confirmation
from algosdk import account, mnemonic

# === CONFIG ===
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""  # No token needed for Algonode
MNEMONIC = "junk frame cram pattern midnight include rice morning spoil family bright detect immune absent ugly acid seek busy hazard gift choice enrich camp absorb duty"

# === SETUP ===
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
private_key = mnemonic.to_private_key(MNEMONIC)
sender = account.address_from_private_key(private_key)

# === LOAD COMPILED TEAL ===
with open("templates/GitHubBoxContract.approval.teal") as f:
    approval_program = f.read()

with open("templates/GitHubBoxContract.clear.teal") as f:
    clear_program = f.read()

import base64

# === COMPILE TEAL ===
approval_compiled = base64.b64decode(client.compile(approval_program)["result"])
clear_compiled = base64.b64decode(client.compile(clear_program)["result"])


# === DEFINE STATE SCHEMA ===
global_schema = StateSchema(num_uints=0, num_byte_slices=1)
local_schema = StateSchema(num_uints=0, num_byte_slices=0)

# === CREATE APPLICATION ===
params = client.suggested_params()
txn = ApplicationCreateTxn(
    sender=sender,
    sp=params,
    on_complete=OnComplete.NoOpOC,
    approval_program=approval_compiled,
    clear_program=clear_compiled,
    global_schema=global_schema,
    local_schema=local_schema,
)

# === SIGN AND SEND ===
signed_txn = txn.sign(private_key)
txid = client.send_transaction(signed_txn)
print(f"📤 Sent transaction: {txid}")

# === WAIT FOR CONFIRMATION ===
response = wait_for_confirmation(client, txid, 4)
app_id = response["application-index"]
print(f"✅ Deployed to Testnet! Application ID: {app_id}")
