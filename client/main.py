import os
import yaml
import json

from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, Transaction, TransactionInstruction
from solana import system_program
from solana.rpc.commitment import Finalized
# from client_util import create_keypair_from_file

from construct import Int32ul
from construct import Struct as cStruct


SOLANA_NETWORK = 'https://api.devnet.solana.com'



def create_keypair_from_file(file_path : str) -> Keypair:
    ## Generate a account (keypair) to transact with our program
    with open(file_path, 'r') as f:
        secret_key = json.load(f)
    return Keypair.from_secret_key(bytes(secret_key))


def send_lamports(_from : Keypair, _to : PublicKey, _amount : int):
    instruction_data = _amount.to_bytes(8,'little')
    inx = TransactionInstruction(
            keys= [
                AccountMeta(pubkey= _from.public_key, is_signer= True, is_writable= False), 
                AccountMeta(pubkey= _to, is_signer= False, is_writable= True), 
                AccountMeta(pubkey= system_program.SYS_PROGRAM_ID, is_signer = False, is_writable= False)
                ], 
            program_id = program_id, 
            data = instruction_data
            )
    txn = Transaction().add(inx)
    resp = connection.send_transaction(txn, _from)
    connection.confirm_transaction(resp.value, commitment= Finalized)
    print("Sucessfully Sended!")


if __name__ == '__main__':
    global program_id
    global program_keypair
    global connection

    global ringo_keypair
    global george_keypair
    global paul_keypair
    global john_keypair

    program_keypair = create_keypair_from_file(os.getcwd() + '/dist/program/program-keypair.json')
    program_id = program_keypair.public_key 
    print(f"program is is {program_id}")

    connection = Client(SOLANA_NETWORK)
    if connection is not None:
        print(f"Connected to ${SOLANA_NETWORK}")

    ringo_keypair = create_keypair_from_file(os.getcwd() + '/accounts/ringo.json')
    george_keypair = create_keypair_from_file(os.getcwd() + '/accounts/george.json')
    paul_keypair = create_keypair_from_file(os.getcwd() + '/accounts/paul.json')
    john_keypair = create_keypair_from_file(os.getcwd() + '/accounts/john.json')

    print("Sending lamports")

    send_lamports(george_keypair, john_keypair.public_key, 500000000)


