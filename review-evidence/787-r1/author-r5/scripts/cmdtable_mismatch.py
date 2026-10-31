import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
t = json.loads((root / "ci/image/command-table.json").read_text())
bad = []
for name, entry in sorted(t["scripts"].items()):
    p = root / name
    h = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "missing"
    if h != entry.get("sha256"):
        bad.append(name)
print(len(bad), "mismatches")
for b in bad: print(" ", b)
