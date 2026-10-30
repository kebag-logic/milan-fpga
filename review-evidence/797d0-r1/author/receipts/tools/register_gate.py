"""Register the inventory gate's commands and script digest in ci/image/command-table.json."""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
path = root / "ci/image/command-table.json"
table = json.loads(path.read_text())
python = table["commands"]["python3"]["patterns"]
for form in (["scripts/docs_inventory.py", "--check"], ["scripts/docs_inventory.py", "--selftest"]):
    if form not in python:
        python.append(form)
python.sort()
git = table["commands"]["git"]["patterns"]
form = ["-C", "<runtime>", "ls-files", "-z"]
if form not in git:
    git.insert(git.index(["-C", "<runtime>", "ls-files", "-z", "*.md"]), form)
script = root / "scripts/docs_inventory.py"
table["scripts"]["scripts/docs_inventory.py"] = {
    "class": "reviewed non-installing",
    "reason": "Validation and source inspection: invokes existing tools or local fixtures; installs nothing.",
    "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
}
original = path.read_text()
assert original == json.dumps(json.loads(original), sort_keys=True, indent=2) + "\n", "table is not in canonical form"
path.write_text(json.dumps(table, sort_keys=True, indent=2) + "\n")
print("registered; script sha256", table["scripts"]["scripts/docs_inventory.py"]["sha256"])
