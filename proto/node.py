# -*- coding: utf-8 -*-
import logging

# tornado imports
import tornado
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue
from tornado.locks import Event
from tornado.options import define, parse_command_line, options


from concensus import make_blockchain_app
from concensus.mining import mining_process


# define ports input to be set by command line argument
define('port', default=5230, help='port to raise service')
define('ip', default='127.0.0.1', help='ipv4 addr to raise service')
define('node_name', help='name for node')

@gen.coroutine
def main():
    # get port from commandline
    parse_command_line()
    # configuration
    host = options.ip
    port = options.port
    node_name = options.node_name
    app = make_blockchain_app(node_name)
    http_server = tornado.httpserver.HTTPServer(app)
    # launch listener server
    http_server.listen(port)
    logging.warning(f"Listening http on {host}:{port}...")
    # launch services
    current = IOLoop.current()
    current.spawn_callback(mining_process, node_name)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
