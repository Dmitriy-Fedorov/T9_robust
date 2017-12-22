import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import os
import json
from Desk import T9Desk


class T9Handler(tornado.websocket.WebSocketHandler):

    def initialize(self):
        # Initialize game parameters.
        self.env = T9Desk()

    def open(self):
        print("WebSocket opened")
        self.initialize()
        # self.write_message(u"Dimas sends greetings!")
        print(self.env.state_json())
        self.write_message(self.env.state_json())

    def on_message(self, message):
        data = json.loads(message)
        print('MESSAGE:', message)
        print('DATA:', data)
        # print('DATA:', data[0], data[1])
        # self.env.tuzdyk = {'p1': 1, 'p2': 2}
        # self.write_message(u"Your message was: " + message)
        if data[0] == 'action':
            action = data[1]
            who_moves = self.env.who_move
            if (action > 10) & who_moves:
                action -= 10
            elif (action < 10) & who_moves:
                action += 10
            if action < 10:
                self.env.step(action)
                self.write_message(self.env.state_json())

    def on_close(self):
        print("WebSocket closed")


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("First.html")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/ws', T9Handler)
        ]
        APP_DIR = os.path.dirname(os.path.realpath(__file__))
        print(APP_DIR)
        settings = {
            "template_path": os.path.join(APP_DIR, "templates"),
            "static_path": os.path.join(APP_DIR, "static")
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
