# -*- coding: utf-8 -*-
import os
from settings import BASE_DIR


def build_filesytem(node_name):
    """construye carpetas para los archivos del nodo"""
    dirname = os.path.join(BASE_DIR, 'node_name')
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    return dirname
