import cv2
import os
import sys
import json
from Pipeline import GripPipeline
from pprint import PrettyPrinter
from colorama import init, Fore
def percentage(part, whole):
	return int(100 * int(part) / int(whole))
init()
gp = GripPipeline()
pp = PrettyPrinter()
returns = {}
report = {}
passes = 0
total = 0
for i in os.listdir("test_images"):
	total = total + 1
	cap = cv2.imread("test_images/" + i)
	gp.process(cap)
	returns[i] = gp.filter_contours_output
print(Fore.YELLOW + "Running CVCov...")
for x, y in returns.items():
	if y == []:
		report[x] = False
	else:
		report[x] = True
		passes = passes + 1
# Below we generate a coverage report as `cvcov.json`.
with open("cvcov.json", "w") as file:
	file.write(json.dumps(report, sort_keys=True))
with open("badge.svg", "w") as file:
	file.write("<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"94\" height=\"20\"><linearGradient id=\"b\" x2=\"0\" y2=\"100%\"><stop offset=\"0\" stop-color=\"#bbb\" stop-opacity=\".1\"/><stop offset=\"1\" stop-opacity=\".1\"/></linearGradient><clipPath id=\"a\"><rect width=\"94\" height=\"20\" rx=\"3\" fill=\"#fff\"/></clipPath><g clip-path=\"url(#a)\"><path fill=\"#555\" d=\"M0 0h59v20H0z\"/><path fill=\"#4c1\" d=\"M59 0h35v20H59z\"/><path fill=\"url(#b)\" d=\"M0 0h94v20H0z\"/></g><g fill=\"#fff\" text-anchor=\"middle\" font-family=\"DejaVu Sans,Verdana,Geneva,sans-serif\" font-size=\"11\"><text x=\"29.5\" y=\"15\" fill=\"#010101\" fill-opacity=\".3\">cvcov</text><text x=\"29.5\" y=\"14\">cvcov</text><text x=\"75.5\" y=\"15\" fill=\"#010101\" fill-opacity=\".3\">" + str(percentage(passes, total)) + "%</text><text x=\"75.5\" y=\"14\">" + str(percentage(passes, total)) + "%</text></g></svg>")
print("\n" + Fore.GREEN + "Passes\t" + str(passes))
print(Fore.RED + "Fails\t" + str(total - passes))
print(Fore.BLUE + "Total\t" + str(total))
print(Fore.YELLOW + "Coverage report written as `cvcov.json`.")
print(Fore.YELLOW + "Badge written as `badge.svg`.")
sys.exit(0)