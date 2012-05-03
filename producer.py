import json
import math
import time
import zmq

#---------------------------------------------------------------------------
def sine_producer():
    """Produce time series sine wave"""
    print "Sine producer running, generating sine wave..."
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:5000")
    
    while True:
        x = time.time()
        y = 2.5 * (1 + math.sin(x))
        socket.send(json.dumps(dict(x=x, y=y)))
        time.sleep(0.1)

if __name__ == "__main__":
    sine_producer()
