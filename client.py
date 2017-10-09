import zmq
from pprint import PrettyPrinter
pp = PrettyPrinter()
print("Connecting...")
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5678")
for request in range(1,1000):
    print("Sending request ", request, "...")
    socket.send_string("Hello")
    message = socket.recv()
    pp.pprint(message)