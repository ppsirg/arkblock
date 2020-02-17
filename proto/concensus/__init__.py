# -*- coding: utf-8 -*-
import os
import re
from tinydb import TinyDB
from tornado.web import Application, RequestHandler
# from concensus.directions import *
from concensus.blocks import start_db
from concensus.utilities import build_filesytem

class chainBaseHandler(RequestHandler):
    """Clase base."""

    def initialize(self, params, *args, **kwargs):
        print(args)
        print(kwargs)
        self.node_name = params['name']
        self.dirname = params['folder']
        self.db_file = os.path.join(self.dirname, f'{self.node_name}.json')
        self.__range_qs__ = {
            'closed_range': re.compile(r'\d+-\d+'),
            'punctual_block': re.compile(r'\d+'),
            'bigger_than': re.compile(r'\d+-'),
            'less_than': re.compile(r'-\d+'),
        }

class blockHandler(chainBaseHandler):
    """docstring for blockHandler."""

    def get_block(self, query=None):
        """retorna bloques del registro, puede retornar: todos, uno por id,
        y en un rango cerrado"""
        print(f'=> abriendo base de datos en: {self.db_file}')
        with TinyDB(self.db_file) as db:
            if not query:
                data = db.all()
                return data
            else:
                if self.__range_qs__['closed_range'].match(query):
                    pass
                return None

    def get(self, *args, **kwargs):
        print(args)
        print(kwargs)
        # serializar blockchain
        response = self.get_block()
        self.write({'blocks': response})


class transactionHandler(chainBaseHandler):
    """docstring for blockHandler."""

    def get(self, *args, **kwargs):
        """Retorna transacciones sin procesar"""
        print(args)
        print(kwargs)
        self.write({'response': 'got it'})

    def post(self, *args, **kwargs):
        """Recibe transacciones de otros nodos de la red"""
        print(args)
        print(kwargs)
        self.write({'response': 'posted it'})

# # Node's blockchain copy
# BLOCKCHAIN = [create_genesis_block()]
#
# """ Stores the transactions that this node has in a list.
# If the node you sent the transaction adds a block
# it will get accepted, but there is a chance it gets
# discarded and your transaction goes back as if it was never
# processed"""
# NODE_PENDING_TRANSACTIONS = []


def make_blockchain_app(node_name):
    # construye sistema de archivos
    params = build_filesytem(node_name)
    start_db(params)
    return Application([
        (r"/blocks/(.*)?", blockHandler, {'params': params}),
        (r"/txion/", transactionHandler, {'params': params}),
    ])
