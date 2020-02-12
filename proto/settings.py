# -*- coding: utf-8 -*-
"""Configuraciones del nodo.
"""
import json
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
base_url = 'http://emdyp.pythonanywhere.com'
base_url = 'http://localhost:5000'
# Write your node url or ip. If you are running it localhost use default
MINER_NODE_URL = "http://localhost:5000"

# Store the url data of every other node in the network
# so that we can communicate with them
PEER_NODES = []

# Write your generated adress here. All coins mined will go to this address
MINER_KEY = 'lol'

with open(MINER_KEY + '.key', 'r') as f:
    key_data = json.load(f)

MINER_ADDRESS = key_data['public_key']
