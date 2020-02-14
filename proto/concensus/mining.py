# -*- coding: utf-8 -*-
"""
corrutina de minería
"""
# from tornado import gen
import json
from time import time
from tornado import gen
from datetime import datetime
from concensus.blocks import create_genesis_block, Block, proof_of_work, NodeBlockChain
from concensus.utilities import build_filesytem


async def mining_process(node_name, *args, **kwargs):
    """proceso de minería
    """
    new_block_interval = 30
    BLOCKCHAIN = NodeBlockChain(node_name)
    while True:
        """Mining is the only way that new coins can be created.
        In order to prevent too many coins to be created, the process
        is slowed down by a proof of work algorithm.
        """
        start_dt = datetime.now()
        print(f'=> doing {block_number} block')
        block_number += 1
        # Get the last proof of work
        last_block = await BLOCKCHAIN.blocks(qs='last')
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
            NODE_PENDING_TRANSACTIONS = []# requests.get(MINER_NODE_URL + "/txion?update=" + MINER_ADDRESS).content
            try:
                NODE_PENDING_TRANSACTIONS = json.loads(NODE_PENDING_TRANSACTIONS)
                print(f'successfully load pending transactions {NODE_PENDING_TRANSACTIONS}')
            except Exception as e:
                print(f'can load NODE_PENDING_TRANSACTIONS because of {e}')
                NODE_PENDING_TRANSACTIONS = []
            # Then we add the mining reward
            NODE_PENDING_TRANSACTIONS.append({
                "from": "network",
                "to": MINER_ADDRESS,
                "amount": 1})
            # Now we can gather the data needed to create the new block
            new_block_data = {
                "proof-of-work": proof[0],
                "transactions": list(NODE_PENDING_TRANSACTIONS)
            }
            new_block_index = last_block.index + 1
            new_block_timestamp = time()
            last_block_hash = last_block.hash
            # Empty transaction list
            NODE_PENDING_TRANSACTIONS = []
            # Now create the new block
            mined_block = Block(new_block_index, new_block_timestamp, new_block_data, last_block_hash)
            BLOCKCHAIN.append(mined_block)
            # Let the client know this node mined a block
            print({
              "index": new_block_index,
              "timestamp": str(new_block_timestamp),
              "data": new_block_data,
              "hash": last_block_hash
            })
            elapsed_dt = datetime.now() - start_dt
            to_wait = new_block_interval - elapsed_dt.seconds
            await gen.sleep(to_wait if to_wait > 0 else 1)
            # a.send(BLOCKCHAIN)
            # requests.get(MINER_NODE_URL + "/blocks?update=" + MINER_ADDRESS)
