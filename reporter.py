import json
from yattag import Doc
doc, tag, text = Doc().tagtext()
with open("cvcov.json") as data:
	d = json.load(data)
	with tag("html"):
		with tag("head"):
			with tag("title"):
				text("CVCov Report")
		with tag("body"):
			with tag("table", style="width: 100%"):
				with tag("tr"):
					with tag("th"):
						with tag("center"):
							text("Name of Image")
					with tag("th"):
						with tag("center"):
							text("Status")
					with tag("th"):
						with tag("center"):
							text("Picture")
				for key, value in d.items():
					with tag("tr"):
						with tag("td"):
							with tag("center"):
								with tag("h4"):
									text(key)
						with tag("td"):
							with tag("center"):
								if value[0] == True:
									with tag("h1", style="color: green"):
										text("✔")
								else:
									with tag("h1", style="color: red"):
										text("✘")
						with tag("td"):
							with tag("center"):
								doc.stag("img", src=str(value[1]))
with open("report.html", "w") as file:
	file.write(doc.getvalue())
