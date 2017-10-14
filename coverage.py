import cv2, os, sys, json, datetime, base64
from Pipeline import GripPipeline
from colorama import init, Fore
def percentage(part, whole):
	return int(100 * int(part) / int(whole))
init()
gp = GripPipeline()
now = datetime.datetime.now()
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
		report[x] = [False, "data:image/jpeg;base64," + str(base64.b64encode(cv2.imencode(".jpg", cv2.imread("test_images/" + x))[1]), "utf-8")]
	else:
		new = cv2.imread("test_images/" + x)
		cv2.drawContours(new, y, -1, (0, 255, 0), 3)
		img = cv2.imencode(".jpg", new)
		report[x] = [True, "data:image/jpeg;base64," + str(base64.b64encode(img[1]), "utf-8")]
		passes = passes + 1
# Add stats to JSON.
report["stats"] = {
	"passes": passes,
	"fails": total - passes,
	"total": total,
	"percentage": percentage(passes, total),
	"timestamp": now.strftime("%Y-%m-%d %H:%M")
}
# Below we generate a coverage report as `cvcov.json`.
with open("cvcov.json", "w") as file:
	file.write(json.dumps(report, sort_keys=True))
print("\n" + Fore.GREEN + "Passes\t" + str(passes))
print(Fore.RED + "Fails\t" + str(total - passes))
print(Fore.BLUE + "Total\t" + str(total))
print(Fore.YELLOW + "Coverage reports written as `cvcov.json`.")
sys.exit(0)