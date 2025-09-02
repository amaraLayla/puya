from algosdk.v2client import algod
from algosdk.transaction import wait_for_confirmation
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
)
from algosdk import account, mnemonic
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.abi import Method
import json

# === CONFIG ===
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""
MNEMONIC = "junk frame cram pattern midnight include rice morning spoil family bright detect immune absent ugly acid seek busy hazard gift choice enrich camp absorb duty"
APP_ID = 745191814


# === SETUP ===
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
private_key = mnemonic.to_private_key(MNEMONIC)
sender = account.address_from_private_key(private_key)
signer = AccountTransactionSigner(private_key)

# === LOAD ABI ===
with open("templates/GitHubBoxContract.arc56.json") as f:
    contract_json = json.load(f)

method_json = json.dumps(contract_json["methods"][0])
method = Method.from_json(method_json)


# === BUILD CALL ===
atc = AtomicTransactionComposer()
atc.add_method_call(
    app_id=APP_ID,
    method=method,
    sender=sender,
    signer=signer,
    sp=client.suggested_params(),
    method_args=["ayzel-dev"],
)

# === EXECUTE ===
result = atc.execute(client, 4)
print(f"✅ deposit() called successfully. Return value: {result.abi_results[0].return_value}")
