# -*- coding: utf-8 -*-

"""This is going to be your wallet. Here you can do several things:
- Generate a new address (public and private key). You are going
to use this address (public key) to send or receive any transactions. You can
have as many addresses as you wish, but keep in mind that if you
lose its credential data, you will not be able to retrieve it.

- Send coins to another address
- Retrieve the entire blockchain and check your balance

If this is your first time using this script don't forget to generate
a new address and edit miner config file with it (only if you are
going to mine).

Timestamp in hashed message. When you send your transaction it will be received
by several nodes. If any node mine a block, your transaction will get added to the
blockchain but other nodes still will have it pending. If any node see that your
transaction with same timestamp was added, they should remove it from the
node_pending_transactions list to avoid it get processed more than 1 time.
"""

import time
import base64
import ecdsa
import json
from pprint import pprint
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

# =============================================================================
# auxiliar function


def allowed_characters(key):
    banned = [b'+', b'/']
    return True if set(banned).intersection(set(key)) else False


def sign_ECDSA_msg(private_key):
    """Sign the message to be sent
    private_key: must be hex

    return
    signature: base64 (to make it shorter)
    message: str
    """
    # Get timestamp, round it, make it into a string and encode it to bytes
    message = str(round(time.time()))
    bmessage = message.encode()
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    signature = base64.b64encode(sk.sign(bmessage))
    return signature, message

# =============================================================================
# key management

def generate_ECDSA_keys(key_name):
    """This function takes care of creating your private and public (your address) keys.
    It's very important you don't lose any of them or those wallets will be lost
    forever. If someone else get access to your private key, you risk losing your coins.

    private_key: str
    public_ley: base64 (to make it shorter)
    """
    filename =  f"{key_name}.key"
    while True:
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) #this is your sign (private key)
        private_key = sk.to_string().hex() #convert your private key to hex
        vk = sk.get_verifying_key() #this is your verification key (public key)
        public_key = vk.to_string().hex()
        #we are going to encode the public key to make it shorter
        public_key = base64.b64encode(bytes.fromhex(public_key))
        if allowed_characters(public_key):
            break

    with open(filename, "w") as f:
        key_data = {
            'private_key': private_key,
            'public_key': public_key.decode()
        }
        json.dump(key_data, f, sort_keys=True, indent=4)
        print(f"Private key: {private_key}\nWallet address / Public key: {public_key.decode()}")
    print(f"Your new address and private key are now in the file {filename}")
    return filename


def send_transaction_ui(destination_node, key_name, addr_to, amount):
    """Send transaction user interface.
    """
    key_filename = key_name + '.key'
    with open(key_filename + '.key', 'r') as f:
        key_data = json.load(f)
    addr_from = key_data['public_key']
    private_key = key_data['private_key']
    print(f'your key {key_name} was loaded')
    pprint(key_data)
    print(f"From: {addr_from}\nPrivate Key: {private_key}\nTo: {addr_to}\nAmount: {amount}\n")
    send_transaction(destination_node, addr_from, private_key, addr_to, amount)


# =============================================================================
# transactions


async def send_transaction(destination_node, addr_from, private_key, addr_to, amount):
    """Sends your transaction to different nodes. Once any of the nodes manage
    to mine a block, your transaction will be added to the blockchain. Despite
    that, there is a low chance your transaction gets canceled due to other nodes
    having a longer chain. So make sure your transaction is deep into the chain
    before claiming it as approved!
    """
    if len(private_key) == 64:
        signature, message = sign_ECDSA_msg(private_key)
        url = destination_node + '/txion'
        payload = {"from": addr_from,
                   "to": addr_to,
                   "amount": amount,
                   "signature": signature.decode(),
                   "message": message}
        headers = {"Content-Type": "application/json"}
        http_client = AsyncHTTPClient()
        request = HTTPRequest(
            url, method='POST', headers=headers, body=json.dumps(payload)
            )
        try:
            res = await http_client.fetch(request)
            print(res.body)
        except Exception as e:
            print(f'something wrong on send transaction: {e}')
            return None
        else:
            print(res.body)
            return res.body
    else:
        print("Wrong address or key length! Verify and try again.")
        return None
