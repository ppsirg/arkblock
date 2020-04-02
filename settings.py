# -*- coding: utf-8 -*-
"""Configuraciones del nodo.
"""
import os
import json


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Store the url data of every other node in the network
# so that we can communicate with them
PEER_NODES = ['https://localhost:8888']

# base_url = 'http://emdyp.pythonanywhere.com'
# base_url = 'http://localhost:5000'
# # Write your node url or ip. If you are running it localhost use default
# MINER_NODE_URL = "http://localhost:5000"
#
#
# # Write your generated adress here. All coins mined will go to this address
# MINER_KEY = 'lol'
#
# with open(MINER_KEY + '.key', 'r') as f:
#     key_data = json.load(f)
#
# MINER_ADDRESS = key_data['public_key']


def save_config(node_name, host, port):
    filename = os.path.join(BASE_DIR, node_name, f'config_{node_name}.json')
    if not os.path.exists(filename):
        with open(filename, 'a+') as f:
            config = {'node_name':node_name, 'host': host, 'port': port}
            json.dump(config, f)


def get_config(node_name):
    with open(os.path.join(BASE_DIR, node_name, f'config_{node_name}.json'), 'r') as f:
        info = f.read()
        print(info)
    return info
