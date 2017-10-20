import cv2, os, sys, datetime, base64
from Pipeline import GripPipeline
from colorama import init, Fore
from yattag import Doc
def percentage(part, whole):
    return int(100 * int(part) / int(whole))
init()
gp1 = GripPipeline(True)
gp2 = GripPipeline(False)
now = datetime.datetime.now()
returns = {}
report = {}
passes = 0
total = 0
for i in os.listdir("test_images"):
    total = total + 1
    cap = cv2.imread("test_images/" + i)
    if i.startswith("red_"):
        gp2.process(cap)
        returns[i] = gp2.filter_contours_output
    else:
        gp1.process(cap)
        returns[i] = gp1.filter_contours_output
print(Fore.YELLOW + "Running CVCov...")
for x, y in returns.items():
    if y == []:
        report[x] = [False, "data:image/jpeg;base64," + str(base64.b64encode(cv2.imencode(".jpg", cv2.imread("test_images/" + x))[1]), "utf-8"), False]
    elif x.endswith("_prob.jpg"):
        new = cv2.imread("test_images/" + x)
        cv2.drawContours(new, y, -1, (0, 255, 0), 3)
        img = cv2.imencode(".jpg", new)
        report[x] = [True, "data:image/jpeg;base64," + str(base64.b64encode(img[1]), "utf-8"), True]
        passes = passes + 1
    else:
        new = cv2.imread("test_images/" + x)
        cv2.drawContours(new, y, -1, (0, 255, 0), 3)
        img = cv2.imencode(".jpg", new)
        report[x] = [True, "data:image/jpeg;base64," + str(base64.b64encode(img[1]), "utf-8"), False]
        passes = passes + 1
print("\n" + Fore.GREEN + "Passes\t" + str(passes))
print(Fore.RED + "Fails\t" + str(total - passes))
print(Fore.BLUE + "Total\t" + str(total))
print(Fore.YELLOW + "Writing coverage report...")
doc, tag, text = Doc().tagtext()
with tag("html"):
    with tag("head"):
        with tag("title"):
            text("CVCov Report")
        doc.stag("link", rel="stylesheet", href="https://fonts.googleapis.com/css?family=Inconsolata|Montserrat")
    with tag("body"):
        with tag("table", style="width: 100%"):
            with tag("tr", style="font-family: \"Montserrat\""):
                with tag("th"):
                    with tag("center"):
                        with tag("h1"):
                            text("Name of Image")
                with tag("th"):
                    with tag("center"):
                        with tag("h1"):
                            text("Status")
                with tag("th"):
                    with tag("center"):
                        with tag("h1"):
                            text("Picture")
                with tag("th"):
                    with tag("center"):
                        with tag("h1"):
                            text("Complete?")
            for key, value in report.items():
                with tag("tr", style="font-family: \"Inconsolata\""):
                    with tag("td"):
                        with tag("center"):
                            with tag("h2", style="font-weight: 300"):
                                text(key)
                    with tag("td"):
                        with tag("center"):
                            if value[0] == True:
                                with tag("h1", style="color: #4CAF50; font-weight: 300"):
                                    text("✔")
                            else:
                                with tag("h1", style="color: #F44336; font-weight: 300"):
                                    text("✘")
                    with tag("td"):
                        with tag("center"):
                            doc.stag("img", src=str(value[1]))
                    with tag("td"):
                        with tag("center"):
                            if value[2] == True:
                                with tag("h2", style="color: #FF9800; font-weight: 300"):
                                    text("⊬ Does Not Prove")
                            else:
                                with tag("h2", style="color: #4CAF50; font-weight: 300"):
                                    text("⊢ Complete")
with open("report.html", "w") as file:
    file.write(doc.getvalue())