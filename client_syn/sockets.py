import auth
import en_us
import db

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
import ssl
import os
import json

from zeroless import (Client)

class ChannelHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def on_open(self):
        print("connection made")

    def on_message(self, message):
        try:
            request = json.loads(message)
        except:
            self.write_message("Malformed request.")
            return

        if "authentication" not in request or "serviceid" not in request:
            self.write_message("Malformed request.")
            return

        auth_status = auth.verify(
            request['authentication']['client_id'], request['authentication']['token'])
        if not auth_status:
            self.write_message(en_us.AUTH_FAILED)
            return

        self.write_message("Authentication was successful.")

        logs = db.last_50(request['serviceid'])
        for x in range(len(logs)):
            tw = {
                "service_id": request["serviceid"],
                "content": logs[x],
                "type": "Log Provider"
            }
            self.write_message(json.loads(tw).decode('utf-8'))

        x = threading.Thread(target=self.bind, args=[
                         request['serviceid']])
        x.start()

    def bind(self, serviceid):
        asyncio.set_event_loop(asyncio.new_event_loop())
        client = Client()
        client.connect_local(port=9876)
        listen = client.sub()
        for item in listen:
            data = json.loads(item.decode('utf-8'))
            if data["service_id"] == serviceid and not db.is_dupe(serviceid, data["content"]):
                self.write_message(data)

def main():
    asyncio.set_event_loop(asyncio.new_event_loop())
    # Create tornado application and supply URL routes
    application = tornado.web.Application([
        (r'/', ChannelHandler)
    ])

    # Setup HTTP Server
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(3142, "0.0.0.0")

    # Start IO/Event loop
    tornado.ioloop.IOLoop.instance().start()


main()