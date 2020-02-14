# -*- coding: utf-8 -*-
import os
from settings import BASE_DIR
from tinydb import TinyDB
from concensus.directions import generate_ECDSA_keys, get_ECDSA_keys


def build_filesytem(node_name):
    """construye carpetas para los archivos del nodo"""
    dirname = os.path.join(BASE_DIR, node_name)
    # crear llave por defecto
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        data = generate_ECDSA_keys(node_name)
    else:
        data = get_ECDSA_keys(node_name)
    return data
