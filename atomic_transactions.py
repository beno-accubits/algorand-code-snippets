import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from algosdk.v2client import algod
from algosdk import mnemonic, account
from algosdk.future.transaction import PaymentTxn,calculate_group_id
from helper import wait_for_confirmation
mnemonic1 = os.getenv('mnemonic1')
mnemonic2 = os.getenv('mnemonic2')
mnemonic3 = os.getenv('mnemonic3')

accounts = {}
counter = 1

for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)

print("Account 1 address: {}".format(accounts[1]['pk']))
print("Account 2 address: {}".format(accounts[2]['pk']))
print("Account 3 address: {}".format(accounts[3]['pk']))


params = algod_client.suggested_params()

# from account 1 to account 3
txn_1 = PaymentTxn(accounts[1]['pk'], params, accounts[3]['pk'], 1000000)
print("Transaction 1: {}".format(txn_1))
# from account 2 to account 1
txn_2 = PaymentTxn(accounts[2]['pk'], params, accounts[1]['pk'], 2000000)
print("Transaction 2: {}".format(txn_2))
# get group id and assign it to transactions

gid = calculate_group_id([txn_1, txn_2])
txn_1.group = gid
txn_2.group = gid
print("Group ID: {}".format(gid))

# sign transactions
stxn_1 = txn_1.sign(accounts[1]['sk'])    
stxn_2 = txn_2.sign(accounts[2]['sk'])

# assemble transaction group
signed_group =  [stxn_1, stxn_2]

tx_id = algod_client.send_transactions(signed_group)
print("Transaction ID: {}".format(tx_id))

# wait for confirmation
wait_for_confirmation(algod_client, tx_id) 