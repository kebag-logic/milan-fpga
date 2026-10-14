import json, sys
d = json.load(open(sys.argv[1]))
print(" ".join(p["tool"] + "=" + p["version"] for p in d["packages"]))
