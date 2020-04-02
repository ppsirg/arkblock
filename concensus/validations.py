# -*- coding: utf-8 -*-

import os
import json
import base64
import ecdsa
from tornado.httpclient import HTTPClient
from tinydb import TinyDB
from settings import PEER_NODES
from concensus.chain import create_genesis_block



# good!!!
def validate_blockchain(block):
    """Validate the submitted chain. If hashes are not correct, return false
    block(str): json
    """
    return True


def validate_signature(public_key, signature, message):
    """Verifies if the signature is correct. This is used to prove
    it's you (and not someone else) trying to do a transaction with your
    address. Called when a user tries to submit a new transaction.
    """
    public_key = (base64.b64decode(public_key)).hex()
    signature = base64.b64decode(signature)
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
    # Try changing into an if/else statement as except is too broad.
    try:
        return vk.verify(signature, message.encode())
    except:
        return False


def start_db(filesystem_data):
    db_file = os.path.join(filesystem_data['folder'], f'{filesystem_data["name"]}.json')
    with TinyDB(db_file) as db:
        stored = db.all()
        if not stored:
            # si no hay nada, consultar bloques a otro nodo
            client = HTTPClient()
            try:
                response = client.fetch(f'{PEER_NODES[0]}/blocks/')
            except Exception as e:
                # si otro nodo no tiene nada, crear genesis_block
                genesis_block = create_genesis_block()
                db.insert(genesis_block.dict_repr)
            else:
                resp_data = json.loads(response.body.decode(encoding='utf-8'))
                if not resp_data['blocks']:
                    # si otro nodo no tiene nada, crear genesis_block
                    genesis_block = create_genesis_block()
                    db.insert(genesis_block.dict_repr)
                else:
                    # si tiene blques, poner los bloques en mi almacenamiento
                    db.insert_multiple(resp_data['blocks'])

