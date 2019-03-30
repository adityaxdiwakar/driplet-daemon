import auth
import en_us

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import tornado.options

import functools
import asyncio
import subprocess
import threading
import time
import sys
import os
import json

class ChannelHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def on_open(self):
        pass

    def on_message(self, message):
        try:
            request = json.loads(message)
        except:
            self.write_message("Malformed request.")
            return

        if "authentication" not in request or "log_command" not in request:
            self.write_message("Malformed request.")
            return

        auth_status = auth.verify(
            request['authentication']['client_id'], request['authentication']['token'])
        if not auth_status:
            self.write_message(en_us.AUTH_FAILED)
            return

        self.write_message("Authentication was successful.")
        threading.Thread(target=self.bind, args=[
                         request['log_command']]).start()

    def bind(self, command):
        # will eventually become place for ZMQ binding point 
        asyncio.set_event_loop(asyncio.new_event_loop())
        p = subprocess.Popen(
            command, stdout=subprocess.PIPE, bufsize=1, shell=True)
        while True:
            self.write_message(p.stdout.readline())


def main():
    asyncio.set_event_loop(asyncio.new_event_loop())
    # Create tornado application and supply URL routes
    application = tornado.web.Application([
        (r'/', ChannelHandler)
    ])

    # Setup HTTP Server
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(3142, "127.0.0.1")

    # Start IO/Event loop
    tornado.ioloop.IOLoop.instance().start()


main()