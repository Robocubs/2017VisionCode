import cv2
import sys
import os
from pprint import PrettyPrinter
from Pipeline import GripPipeline
gp = GripPipeline()
pp = PrettyPrinter()
cap = cv2.imread(sys.argv[1])
gp.process(cap)
print(gp.filter_contours_output)
