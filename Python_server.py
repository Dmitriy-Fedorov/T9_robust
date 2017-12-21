import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import os


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")
        # pass

    def on_message(self, message):
        self.write_message(u"Your message was: " + message)

    def on_close(self):
        pass


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("First.html")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/ws', WebSocketHandler)
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