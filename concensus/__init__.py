# -*- coding: utf-8 -*-
import os
import re
import json
from pprint import pprint
from tinydb import TinyDB
from tornado.web import Application, RequestHandler
from settings import get_config
from concensus.validations import start_db
from concensus.utilities import build_filesytem


class chainBaseHandler(RequestHandler):
    """Base clase to manage requests."""

    def initialize(self, params, *args, **kwargs):
        self.node_name = params['name']
        self.dirname = params['folder']
        self.db_file = os.path.join(self.dirname, f'{self.node_name}.json')
        self.__range_qs__ = {
            'closed_range': re.compile(r'\d+-\d+'),
            'punctual_block': re.compile(r'\d+'),
            'bigger_than': re.compile(r'\d+-'),
            'less_than': re.compile(r'-\d+'),
        }

    def set_default_headers(self, *args, **kwargs):
        super().set_default_headers()
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header(
            "Access-Control-Allow-Headers",
            "content-type, crsf-header, file-length, "
            "file-token, file-duration, x-csrftoken, "
        )


class blockHandler(chainBaseHandler):
    """Maneja peticiones de los bloques."""

    def get_block(self, query=None):
        """retorna bloques del registro, puede retornar: todos, uno por id,
        y en un rango cerrado"""
        print(f'=> abriendo base de datos en: {self.db_file} para leer')
        with TinyDB(self.db_file) as db:
            if not query:
                data = db.all()
                return data
            else:
                if self.__range_qs__['closed_range'].match(query):
                    pass
                return None

    def add_block(self, block_dict):
        """agrega registro a la base de datos
        """
        print(f'=> abriendo base de datos en: {self.db_file} para agregar')
        with TinyDB(self.db_file) as db:
            db.insert(block_dict)

    def get(self, *args, **kwargs):
        # serializar blockchain
        response = self.get_block()
        self.write({'blocks': response})

    def post(self, *args, **kwargs):
        block_dict = json.loads(self.request.body)
        self.add_block(block_dict)
        self.write({'status': 'block_added'})


class transactionHandler(chainBaseHandler):
    """Maneja las transacciones."""

    def get(self, *args, **kwargs):
        """Retorna transacciones sin procesar"""
        self.write({'response': 'got it'})

    def post(self, *args, **kwargs):
        """Recibe transacciones de otros nodos de la red"""
        self.write({'response': 'posted it'})


def make_blockchain_app(node_name):
    # construye sistema de archivos
    params = build_filesytem(node_name)
    start_db(params)
    return Application([
        (r"/blocks/(.*)?", blockHandler, {'params': params}),
        (r"/txion/", transactionHandler, {'params': params}),
    ])
