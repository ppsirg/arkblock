# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web


class probeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        print(args)
        print(kwargs)
        self.write({'response': 'got it'})

    def post(self, *args, **kwargs):
        print(args)
        print(kwargs)
        self.write({'response': 'posted it'})

def make_app():
    return tornado.web.Application([
        (r"/", probeHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
