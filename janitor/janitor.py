import json

report = {
    "status": "working"
}

with open("report.json", "w") as f:
    json.dump(report, f)

with open("report.md", "w") as f:
    f.write("# Cost Janitor Report")