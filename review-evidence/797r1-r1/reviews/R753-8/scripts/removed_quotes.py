import json, subprocess, sys, pathlib
a = json.loads(subprocess.check_output(["git","show",f"{sys.argv[1]}~1:scripts/docs_inventory.json"]))
b = {e["id"] for e in json.loads(subprocess.check_output(["git","show",f"{sys.argv[1]}:scripts/docs_inventory.json"]))["findings"]}
files = subprocess.check_output(["git","ls-files","*.md"]).decode().split()
texts = {f: pathlib.Path(f).read_text(errors="replace") for f in files}
print("keys of an entry:", sorted(a["findings"][0].keys()))
for e in a["findings"]:
    if e["id"] in b and e["id"] not in ("D0-040","D0-057"): continue
    q = e["quote"]; hits = [f for f,t in texts.items() if q in t]
    print(e["id"], e["page"], "copies=", e.get("copies"), "quote-hits=", hits)
