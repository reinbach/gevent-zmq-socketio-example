from flask import Flask, render_template

import gevent
from gevent.pywsgi import WSGIServer
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
import zmq

app = Flask(__name__)
app.debug = True

#===============================================================================
class SocketIOApp(object):
    """Handle socketio requests and assigned to relevant class"""
    #---------------------------------------------------------------------------
    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/socket.io'):
            socketio_manage(environ, {'': SineWave});

#===============================================================================
class SineWave(BaseNamespace, BroadcastMixin):
    """Steam sine values"""
         
    #---------------------------------------------------------------------------
    def on_stream(self, msg):
        context = zmq.Context()
        sock = context.socket(zmq.SUB)
        sock.setsockopt(zmq.SUBSCRIBE, "")
        sock.connect('inproc://queue')
        while True:
            msg = sock.recv()
            self.broadcast_event('message', msg)

#---------------------------------------------------------------------------
def sine_server():
    """Funnel stream from external tcp socket and pass off to inproc socket"""
    print "Sine server running, waiting for data..."
    context = zmq.Context()
    sock_incoming = context.socket(zmq.SUB)
    sock_incoming.bind("tcp://*:5000")
    sock_incoming.setsockopt(zmq.SUBSCRIBE, "")

    sock_outgoing = context.socket(zmq.PUB)
    sock_outgoing.bind("inproc://queue")
    
    while True:
        msg = sock_incoming.recv()
        sock_outgoing.send(msg)

#---------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

#---------------------------------------------------------------------------
def main():
    # setup server to handle webserver requests
    http_server = WSGIServer(('', 8000), app)

    # setup server to handle websocket requests
    sio_server = SocketIOServer(
        ('', 9999), SocketIOApp(),
        namespace="socket.io",
        policy_server=False
    )

    gevent.joinall([
        gevent.spawn(http_server.serve_forever),
        gevent.spawn(sio_server.serve_forever),
        gevent.spawn(sine_server),
    ])

if __name__ == "__main__":
    main()