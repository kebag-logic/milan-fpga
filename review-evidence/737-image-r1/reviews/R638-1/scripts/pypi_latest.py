"""Compare locked Python package versions with the current PyPI latest release."""
import json, sys, urllib.request
d = json.load(open(sys.argv[1]))
for row in d["sources"]:
    if row.get("kind") != "python":
        continue
    with urllib.request.urlopen(f"https://pypi.org/pypi/{row['tool']}/json", timeout=60) as r:
        info = json.load(r)
    latest = info["info"]["version"]
    uploaded = max((f["upload_time"] for f in info["releases"].get(latest, [])), default="?")
    print(f"{row['tool']:24} locked={row['version']:14} latest={latest:14} latest_uploaded={uploaded} {'SAME' if latest == row['version'] else 'DIFF'}")
