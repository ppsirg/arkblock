"""
python tornado.testing concensus.tests
"""
import json
from random import randint
from datetime import datetime
from tornado.testing import AsyncHTTPTestCase
from tornado.ioloop import IOLoop
from concensus import make_blockchain_app
from tornado.curl_httpclient import CurlAsyncHTTPClient


class txion_testcase(AsyncHTTPTestCase):
    
    def setUp(self):
        super().setUp()
        self.__port = self.get_http_port()
        self._app = self.get_app()
        self.http_server = self.get_http_server()
        self.http_server.listen(self.__port)
        self.http_client = CurlAsyncHTTPClient()
        self.transactions = [{
            'from': 'xxx', 'to': 'yyy', 'amount': 1, 
            'payload': {'id': f'fj{a}', 'choice': randint(1,3)}
            } for a in range(20)
            ]

    def tearDown(self):
        super().tearDown()

    def test_txion_endpoint(self):
        # send 20 txions
        for tx in self.transactions:
            resp = self.fetch('/txion/', method='POST', body=json.dumps(tx))
            info = json.loads(resp.body)
            self.assertEqual(info, {'response': 'posted it'})
        # get 20 txions
        resg = self.fetch('/txion/')
        data = json.loads(resg.body)
        self.assertIn('pending', data)
        self.assertEqual(len(data['pending']), 20)

    def get_app(self):
        return make_blockchain_app('testingNode')
    
    def get_http_port(self):
        return 9009

    def get_url(self, path):
        port = self.get_http_port()
        return f'http://localhost:{port}{path}'