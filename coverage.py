import cv2
import os
from Pipeline import GripPipeline
from pprint import PrettyPrinter
gp = GripPipeline()
pp = PrettyPrinter()
returns = {}
for i in os.listdir("test_images"):
	cap = cv2.imread("test_images/" + i)
	gp.process(cap)
	returns[i] = gp.filter_contours_output
pp.pprint(returns)