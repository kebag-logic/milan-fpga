#!/usr/bin/env python3
"""Measure what the lane-routing mutants do to the real work lists.

Usage: lane_routing_probe.py CLONE HEAD_SCRIPT WORK. Writes each mutated script into CLONE/scripts, runs
--findings-dir, and compares every (finding, page, line) to the lane file it landed in. Restores the script after.
"""
import pathlib
import re
import shutil
import subprocess
import sys

clone, head, work = (pathlib.Path(a).resolve() for a in sys.argv[1:4])
OLD = "grouped.setdefault(lanes[finding.page], [])"
VARIANTS = {"head": OLD, "W11 one lane": 'grouped.setdefault("one lane", [])',
            "W12 copy under its origin's lane": "grouped.setdefault(lanes[finding.origin or finding.page], [])"}
target = clone / "scripts/docs_inventory.py"
source = head.read_text(encoding="utf-8")
table = {}
for name, new in VARIANTS.items():
    target.write_text(source.replace(OLD, new), encoding="utf-8")
    out = work / re.sub(r"\W+", "_", name)
    shutil.rmtree(out, ignore_errors=True)
    check = subprocess.run([sys.executable, "-I", str(target), "--check"], capture_output=True, text=True, cwd=clone)
    subprocess.run([sys.executable, "-I", str(target), "--findings-dir", str(out)], capture_output=True, text=True, cwd=clone)
    entries = {}
    for lane in sorted(out.glob("*.md")):
        for ident, path in re.findall(r"^## (D0-\d+): (.+):(?:\d+|\?)$", lane.read_text(encoding="utf-8"), re.M):
            entries[(ident, path)] = lane.stem
    table[name] = entries
    print(f"{name}: --check rc {check.returncode}, files {sorted(p.stem for p in out.glob('*.md'))}, entries {len(entries)}")
target.write_text(source, encoding="utf-8")
base = table["head"]
for name in list(VARIANTS)[1:]:
    moved = {key: (base[key], lane) for key, lane in table[name].items() if base.get(key) != lane}
    print(f"{name}: {len(moved)} of {len(base)} entries sit in another lane's file than at head")
    for key, (was, now) in sorted(moved.items())[:12]:
        print("   ", key[0], key[1], was, "->", now)
