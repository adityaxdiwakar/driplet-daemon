import auth

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

from zeroless import (Server, Client)

pub = Server(port=9876).pub()


class ChannelHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def on_open(self):
        pass

    def on_message(self, message):
        data = json.loads(message)
        #except:
        #    self.write_message("Malformed request.")
        #    return

        if "credentials" not in data or "payload" not in data:
            self.write_message("Malformed request.")    
            return

        status = auth.verify(
            data["credentials"]["client_id"],
            data["credentials"]["token"]
        )
        if not status:
            self.write_message("Authorization failed.")
            return
        
        else:
            self.write_message("recv")
            pub(data["payload"].encode('utf-8'))

def main():
    asyncio.set_event_loop(asyncio.new_event_loop())
    # Create tornado application and supply URL routes
    application = tornado.web.Application([
        (r'/', ChannelHandler)
    ])

    # Setup HTTP Server
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(3143, "127.0.0.1")

    # Start IO/Event loop
    tornado.ioloop.IOLoop.instance().start()


main()