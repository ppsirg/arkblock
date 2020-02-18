# -*- coding: utf-8 -*-

import os
import time
import hashlib
import json
import base64
import ecdsa
from concensus.directions import generate_ECDSA_keys, get_ECDSA_keys
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPClient
from tinydb import TinyDB
from settings import PEER_NODES, get_config


# good
class Block(object):
    def __init__(self, *args, **kwargs):
        """Returns a new Block object. Each block is "chained" to its previous
        by calling its unique hash.

        Args:
            index (int): Block number.
            timestamp (int): Block creation timestamp.
            data (str): Data to be sent.
            previous_hash(str): String representing previous block unique hash.

        Attrib:
            index (int): Block number.
            timestamp (int): Block creation timestamp.
            data (str): Data to be sent.
            previous_hash(str): String representing previous block unique hash.
            hash(str): Current block unique hash.

        """
        if len(args) == 4:
            index, timestamp, data, previous_hash = args
            self.index = int(index)
            self.timestamp = timestamp
            self.data = data
            self.data_str = json.dumps(data)
            self.previous_hash = previous_hash
            self.hash = self.hash_block()
        elif len(args) == 1:
            self.index = int(args[0]['index'])
            self.timestamp = args[0]['timestamp']
            # import pdb; pdb.set_trace()
            self.data_str = json.dumps(args[0]['data'])
            self.data = args[0]['data']
            self.previous_hash = args[0]['previous_hash']
            self.hash = self.hash_block()
        else:
            raise ValueError('arguments are not valid')

    def hash_block(self):
        """Creates the unique hash for the block. It uses sha256."""
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + self.data_str + str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()

    def dict_repr(self):
        return {
            "index": str(self.index),
            "timestamp": str(self.timestamp),
            "data": self.data,
            "hash": self.hash,
            "previous_hash": self.previous_hash,
        }

# good
def create_genesis_block():
    """To create each block, it needs the hash of the previous one. First
    block has no previous, so it must be created manually (with index zero
     and arbitrary previous hash)"""
    genesis_block = Block(0, time.time(), {
        "proof-of-work": 9,
        "transactions": None},
        "0")
    return genesis_block

# good
def proof_of_work(last_proof, blockchain):
    # Creates a variable that we will use to find our next proof of work
    incrementer = last_proof + 1
    # Keep incrementing the incrementer until it's equal to a number divisible by 9
    # and the proof of work of the previous block in the chain
    start_time = time.time()
    while not (incrementer % 7919 == 0 and incrementer % last_proof == 0):
        incrementer += 1
        # Check if any node found the solution every 60 seconds
        if int((time.time()-start_time) % 60) == 0:
            # If any other node got the proof, stop searching
            new_blockchain = consensus(blockchain)
            if new_blockchain:
                # (False: another node got proof first, new blockchain)
                return False, new_blockchain
    # Once that number is found, we can return it as a proof of our work
    return incrementer, blockchain

# # refactor this!!!
# def find_new_chains():
#     # Get the blockchains of every other node
#     other_chains = []
#     for node_url in PEER_NODES:
#         # Get their chains using a GET request
#         block = requests.get(node_url + "/blocks").content
#         # Convert the JSON object to a Python dictionary
#         block = block.decode('utf8')
#         print(block)
#         block = json.loads(block)
#         # Verify other node block is correct
#         validated = validate_blockchain(block)
#         if validated:
#             # Add it to our list
#             other_chains.append(block)
#     return other_chains
#

# refactor this!!!
def consensus(blockchain):
    # Get the blocks from other nodes
    other_chains = [] # find_new_chains()
    # If our chain isn't longest, then we store the longest chain
    BLOCKCHAIN = blockchain
    longest_chain = BLOCKCHAIN
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    # If the longest chain wasn't ours, then we set our chain to the longest
    if longest_chain == BLOCKCHAIN:
        # Keep searching for proof
        return False
    else:
        # Give up searching proof, update chain and start over again
        BLOCKCHAIN = longest_chain
        return BLOCKCHAIN

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
                db.insert(genesis_block.dict_repr())
            else:
                resp_data = json.loads(response.body.decode(encoding='utf-8'))
                if not resp_data['blocks']:
                    # si otro nodo no tiene nada, crear genesis_block
                    genesis_block = create_genesis_block()
                    db.insert(genesis_block.dict_repr())
                else:
                    # si tiene blques, poner los bloques en mi almacenamiento
                    db.insert_multiple(resp_data['blocks'])



class NodeBlockChain(object):
    """BlockChain que pertenece al nodo, empaquetando el
    servicio web p2p para que lo consuma el cliente.
    """

    def __init__(self, node_name):
        MINER_CONFIG = json.loads(get_config(node_name))
        MINER_NODE_URL = 'http://{host}:{port}'.format(**MINER_CONFIG)
        self.node_url = MINER_NODE_URL

    async def blocks(self, qs='all'):
        """all, last, n1-n2, n1-
        """
        url = f'{self.node_url}/blocks/' + qs if qs != 'all' else ''
        http_client = AsyncHTTPClient()
        try:
            res = await http_client.fetch(url)
            res_data = json.loads(res.body.decode(encoding='utf-8'))
            print(res_data)
            resp_blocks = [Block(a) for a in res_data['blocks']]
            if qs == 'last':
                return resp_blocks[0]
        except Exception as e:
            print(f'something wrong on async blocks: {e}')
            return None

    async def add_to_chain(self, block):
        """Add block to local chain
        """
        add_request = HTTPRequest(
            f'{self.node_url}/blocks/', method='POST',
            headers={"Content-Type": "application/json"},
            body=json.dumps(block.dict_repr())
            )
        http_client = AsyncHTTPClient()
        try:
            resp = await http_client.fetch(add_request)
            print(f'=> add to chain response was: {resp}')
        except Exception as err:
            print(f'=> something wrong on async add_to_chain: {err}')
        else:
            pass


    async def transactions(self, qs='pending', data=None):
        """pending, send
        """
        url = f'{self.node_url}/txion/' + qs if qs != 'pending' else ''
        http_client = AsyncHTTPClient()
        try:
            res = await http_client.fetch(url)
            res_data = json.loads(res.body.decode(encoding='utf-8'))
            print(res_data)
            return res_data
        except Exception as e:
            print(f'something wrong on async transactions: {e}')
            return None
