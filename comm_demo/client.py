import zmq
from pprint import PrettyPrinter
import json
pp = PrettyPrinter()
print("Connecting...")
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5678")
for request in range(1,10000):
    print("Sending request ", request, "...")
    socket.send_string("Hello")
    message = json.loads(socket.recv())
    pp.pprint(message)