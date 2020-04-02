# -*- coding: utf-8 -*-
"""
corrutina de minería
"""
import json
from pprint import pprint
from time import time
from tornado import gen
from datetime import datetime
from concensus.directions import get_ECDSA_keys
from concensus.chain import NodeBlockChain, proof_of_work
from concensus.data_structure import Block


async def mining_process(node_name, *args, **kwargs):
    """proceso de minería
    """
    new_block_interval = 100
    BLOCKCHAIN = NodeBlockChain(node_name)
    block_number = 0
    NODE_KEYS = get_ECDSA_keys(node_name)
    MINER_ADDRESS = NODE_KEYS['data']['public_key']
    NODE_PENDING_TRANSACTIONS = {'pending':[]}

    while True:
        """Mining is the only way that new coins can be created.
        In order to prevent too many coins to be created, the process
        is slowed down by a proof of work algorithm.
        """
        start_dt = datetime.now()
        await gen.sleep(3)
        # Get the last proof of work
        last_block = await BLOCKCHAIN.blocks(qs='last')
        if not last_block:
            await gen.sleep(0.5)
            continue
        block_number = last_block.index
        last_proof = last_block.data['proof-of-work']
        # Find the proof of work for the current block being mined
        # Note: The program will hang here until a new proof of work is found
        proof = proof_of_work(last_proof, BLOCKCHAIN)
        # If we didn't guess the proof, start mining again
        if not proof[0]:
            # Update blockchain and save it to file
            BLOCKCHAIN = proof[1]
            # a.send(BLOCKCHAIN)
            continue
        else:
            # Once we find a valid proof of work, we know we can mine a block so
            # ...we reward the miner by adding a transaction
            # First we load all pending transactions sent to the node server
            # NODE_PENDING_TRANSACTIONS = '{"pending": []}'
            # Then we add the mining reward
            NODE_PENDING_TRANSACTIONS['pending'].append({
                "from": "network",
                "to": MINER_ADDRESS,
                "amount": 1})
            # Now we can gather the data needed to create the new block
            new_block_data = {
                "proof-of-work": proof[0],
                "transactions": NODE_PENDING_TRANSACTIONS['pending']
            }
            new_block_index = last_block.index + 1
            new_block_timestamp = time()
            last_block_hash = last_block.hash
            # Empty transaction list
            NODE_PENDING_TRANSACTIONS['pending'] = []
            # Now create the new block
            mined_block = Block(
                {
                    'index':new_block_index, 
                    'timestamp': new_block_timestamp, 
                    'data': new_block_data, 
                    'previous_hash': last_block_hash
                    }
            )
            await BLOCKCHAIN.add_to_chain(mined_block)
            # Let the client know this node mined a block
            pprint(mined_block.dict_repr)
            elapsed_dt = datetime.now() - start_dt
            to_wait = new_block_interval - elapsed_dt.seconds
            await gen.sleep(to_wait if to_wait > 0 else 1)
            
            
