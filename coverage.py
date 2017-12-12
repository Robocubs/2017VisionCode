import cv2, os, base64
from Pipeline import GripPipeline
from yattag import Doc
from progress.spinner import MoonSpinner
gp1 = GripPipeline(True)
gp2 = GripPipeline(False)
returns = {}
report = {}
spinner = MoonSpinner("Generating coverage report... ")
for i in os.listdir("test_images"):
    cap = cv2.imread("test_images/" + i)
    spinner.next()
    if i.startswith("red_"):
        spinner.next()
        gp2.process(cap)
        spinner.next()
        returns[i] = gp2.filter_contours_output
    else:
        spinner.next()
        gp1.process(cap)
        spinner.next()
        returns[i] = gp1.filter_contours_output
for x, y in returns.items():
    if y == []:
        spinner.next()
        report[x] = [False, "data:image/jpeg;base64," + str(base64.b64encode(cv2.imencode(".jpg", cv2.imread("test_images/" + x))[1]), "utf-8")]
        spinner.next()
    else:
        spinner.next()
        new = cv2.imread("test_images/" + x)
        spinner.next()
        cv2.drawContours(new, y, -1, (0, 255, 0), 3)
        spinner.next()
        img = cv2.imencode(".jpg", new)
        spinner.next()
        report[x] = [True, "data:image/jpeg;base64," + str(base64.b64encode(img[1]), "utf-8")]
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
            for key, value in report.items():
                spinner.next()
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
with open("report.html", "w") as file:
    file.write(doc.getvalue())
print("\nDone. Coverage report written as report.html.")
