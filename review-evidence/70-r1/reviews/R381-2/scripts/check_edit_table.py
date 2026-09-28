#!/usr/bin/env python3
"""Check D3 section 15.2 rows against the pinned processor tree.

Usage: check_edit_table.py <parent-clone>
Reads docs/design/SAVED_STATE_MATERIALIZATION.md at HEAD of the clone and the
protocol-processor submodule checkout (must be at the pin named in the page).
For every row: path exists at the pin, every cited line number is within the
file, and prints the cited lines' first 100 chars for manual comparison.
"""
import re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
pin = "16be6768f710e79450aace277abacd6c2c3336e5"
pp = root / "protocol-processor"
head = subprocess.run(["git", "-C", str(pp), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print("processor HEAD", head, "pin match" if head == pin else "PIN MISMATCH")
text = subprocess.run(["git", "-C", str(root), "show", "HEAD:docs/design/SAVED_STATE_MATERIALIZATION.md"], capture_output=True, text=True).stdout
sec = text.split("### 15.2 Processor F07.9 edit table", 1)[1].split("## 16. Traceability", 1)[0]
rows = [l for l in sec.splitlines() if l.startswith("| [")]
print("rows", len(rows))
files = set()
bad = 0
for r in rows:
    cells = [c.strip() for c in r.strip("|").split("|")]
    m = re.search(r"/blob/([0-9a-f]{40})/([^)]+)\)", cells[0])
    sha, path = m.group(1), m.group(2)
    files.add(path)
    ok = sha == pin
    f = pp / path
    exists = subprocess.run(["git", "-C", str(pp), "cat-file", "-e", f"{pin}:{path}"]).returncode == 0
    n = len(subprocess.run(["git", "-C", str(pp), "show", f"{pin}:{path}"], capture_output=True, text=True).stdout.splitlines()) if exists else 0
    lines = []
    for a, b in re.findall(r"lines? (\d+)(?:-(\d+))?", cells[1]):
        lines.append((int(a), int(b) if b else int(a)))
    for a in re.findall(r"line (\d+)", cells[1]):
        pass
    inrange = all(b <= n for a, b in lines)
    status = "OK" if (ok and exists and inrange) else "BAD"
    if status == "BAD":
        bad += 1
    print(f"[{status}] {path} (pin link {'ok' if ok else sha}, exists {exists}, {n} lines) section: {cells[1][:110]}")
print("distinct files", len(files))
print("bad rows", bad)
sys.exit(1 if bad else 0)
