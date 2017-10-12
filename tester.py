import cv2
import sys
from Pipeline import GripPipeline
gp = GripPipeline()
cap = cv2.imread(sys.argv[1])
gp.process(cap)
print(gp.filter_contours_output)
