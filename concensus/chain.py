import json
from time import time
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from settings import PEER_NODES, get_config
from concensus.data_structure import Block


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
        url = f'{self.node_url}/blocks/' + qs if qs != 'pending' else ''
        http_client = AsyncHTTPClient()
        try:
            res = await http_client.fetch(url)
            res_data = json.loads(res.body.decode(encoding='utf-8'))
            resp_blocks = [Block(a) for a in res_data['blocks']]
            if qs == 'last':
                return resp_blocks[-1]
        except Exception as e:
            print(f'something wrong on async blocks: {e}')
            return None

    async def add_to_chain(self, block):
        """Add block to local chain
        """
        add_request = HTTPRequest(
            f'{self.node_url}/blocks/', method='POST',
            headers={"Content-Type": "application/json"},
            body=block.json_repr
            )
        http_client = AsyncHTTPClient()
        try:
            resp = await http_client.fetch(add_request)
            print(f'=> add to chain response was: {resp.code}')
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
            return res_data
        except Exception as e:
            print(f'something wrong on async transactions: {e}')
            return None


# good
def create_genesis_block():
    """To create each block, it needs the hash of the previous one. First
    block has no previous, so it must be created manually (with index zero
     and arbitrary previous hash)"""
    block_genesis_info = {
        'index': 0,
        'timestamp': time(),
        'data': {
            "proof-of-work": 9,
            "transactions": None
            },
        'previous_hash': '0'
    }
    genesis_block = Block(block_genesis_info)
    return genesis_block


# good
def proof_of_work(last_proof, blockchain):
    # Creates a variable that we will use to find our next proof of work
    incrementer = last_proof + 1
    # Keep incrementing the incrementer until it's equal to a number divisible by 9
    # and the proof of work of the previous block in the chain
    start_time = time()
    while not (incrementer % 7919 == 0 and incrementer % last_proof == 0):
        incrementer += 1
        # Check if any node found the solution every 60 seconds
        if int((time()-start_time) % 60) == 0:
            # If any other node got the proof, stop searching
            new_blockchain = consensus(blockchain)
            if new_blockchain:
                # (False: another node got proof first, new blockchain)
                return False, new_blockchain
    # Once that number is found, we can return it as a proof of our work
    return incrementer, blockchain


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