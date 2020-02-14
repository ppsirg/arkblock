# -*- coding: utf-8 -*-
from tornado.ioloop import IOLoop
import tornado.web
from tornado import gen


async def my_background_task(*args, **kwargs):
    lapsed = 1
    while True:
        print(f'im here {lapsed}')
        lapsed += 1
        await gen.sleep(2)


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
    current = IOLoop.current()
    current.spawn_callback(my_background_task)
    current.start()
