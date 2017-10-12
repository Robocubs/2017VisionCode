import cv2
import os
import sys
from Pipeline import GripPipeline
from pprint import PrettyPrinter
from colorama import init, Fore
init()
gp = GripPipeline()
pp = PrettyPrinter()
returns = {}
for i in os.listdir("test_images"):
	cap = cv2.imread("test_images/" + i)
	gp.process(cap)
	returns[i] = gp.filter_contours_output
for x, y in returns.items():
	if y == []:
		print(Fore.RED + "✘ " + x)
	else:
		print(Fore.GREEN + "✔ " + x)
print(Fore.YELLOW + "Generating coverage report...")
sys.exit(0)