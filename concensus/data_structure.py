import hashlib
import json


class Block(object):
    """Implement a block of blockchain"""
    def __init__(self, block_info, **kwargs):
        self.index = block_info['index']
        self.timestamp = block_info['timestamp']
        self.data = block_info['data']
        self.previous_hash = block_info['previous_hash']
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(
            (str(self.index) + str(self.timestamp) + self.data_str + str(self.previous_hash)).encode('utf-8')
            )
        return sha.hexdigest()

    def __str__(self):
        return f'{self.index}. {self.hash} [{self.timestamp}]'

    @property
    def data_str(self):
        return json.dumps(self.data)

    @property
    def dict_repr(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash,
            "previous_hash": self.previous_hash,
        }
    
    @property
    def json_repr(self):
        return json.dumps(self.dict_repr)