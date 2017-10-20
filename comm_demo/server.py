"""
ZeroMQ-based server for OpenCV. Does the following:

1. Import OpenCV, PrettyPrinter, ZeroMQ, and GRIP.
2. Initialize the above items.
3. Create a ZeroMQ context and socket.
4. Bind the context to a local address.
5. Run the pipeline.
6. Await connections and return vision results when needed.

Each step is annotated with the number of the above list.
"""
import cv2 # Step 1
import sys
import os
from pprint import PrettyPrinter
import zmq
from .. import Pipeline
os.system("clear")
print("Welcome to 127.0.0.1.")
gp = Pipeline.GripPipeline() # Step 2
pp = PrettyPrinter()
cap = cv2.VideoCapture(0)
context = zmq.Context() # Step 3
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5678") # Step 4
try:
    while True:
        ret, frame = cap.read()
        gp.process(frame) # Step 5
        message = socket.recv() # Step 6
        print("Recieved request: ", message)
        pp.pprint(gp.filter_contours_output)
        socket.send_json(gp.filter_contours_output)
except KeyboardInterrupt:
    pass
os.system("clear")
print("Exiting. Thank you for playing Wing Commander!")
context.destroy()
cap.release()
sys.exit(0)
