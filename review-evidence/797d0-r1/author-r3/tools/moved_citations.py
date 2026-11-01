#!/usr/bin/env python3
"""For every line citation in the findings' source and correction cells: is its text the same as at the round 2 head?

Usage: python3 -I moved_citations.py LANE. A citation is compared at the round 2 data file's number and the head's.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
OLD = "3e6d92c1"
PINS = {"protocol-processor": ("f65c8ff7", "a9e84b66"), "gptp-processor": ("f97c1803", "135afd04")}
PAT = re.compile(r"`([\w./+-]+\.\w+)`(?:,)? ?(?:\(?)lines? (\d+)")


def show(rev, path):
    """The file's lines at the round 2 head (rev old) or the lane head."""
    for sub, (old, new) in PINS.items():
        if path.startswith(sub + "/"):
            out = subprocess.run(["git", "-C", str(root / sub), "show", f"{old if rev == 'old' else new}:{path[len(sub) + 1:]}"],
                                 capture_output=True, text=True, errors="replace")
            return out.stdout.split("\n") if out.returncode == 0 else None
    out = subprocess.run(["git", "-C", str(root), "show", f"{OLD if rev == 'old' else 'HEAD'}:{path}"],
                         capture_output=True, text=True, errors="replace")
    return out.stdout.split("\n") if out.returncode == 0 else None


old_data = json.loads(subprocess.run(["git", "-C", str(root), "show", f"{OLD}:scripts/docs_inventory.json"],
                                     capture_output=True, text=True).stdout)
new_data = json.loads((root / "scripts/docs_inventory.json").read_text(encoding="utf-8"))
new_ids = {f["id"]: f for f in new_data["findings"]}
same = moved = 0
for finding in old_data["findings"]:
    now = new_ids.get(finding["id"])
    if now is None:
        print(f"{finding['id']}: REMOVED")
        continue
    for field in ("source", "correction"):
        for was, is_now in zip(PAT.finditer(finding[field]), PAT.finditer(now[field])):
            path, a, b = was.group(1), int(was.group(2)), int(is_now.group(2))
            old_lines, new_lines = show("old", path), show("new", path)
            if old_lines is None or new_lines is None or was.group(1) != is_now.group(1):
                print(f"{finding['id']} {field}: {path}: REWORDED, read by hand")
                continue
            equal = old_lines[a - 1] == new_lines[b - 1]
            same += equal and a == b
            moved += equal and a != b
            if not equal:
                print(f"{finding['id']} {field}: {path}:{a} -> :{b} TEXT DIFFERS: {old_lines[a - 1].strip()[:60]!r} / {new_lines[b - 1].strip()[:60]!r}")
            elif a != b:
                print(f"{finding['id']} {field}: {path}:{a} -> :{b}, same text")
print(f"same line {same}, moved with the same text {moved}")
