#!/usr/bin/env python3
"""Every arm of tdm8_render_mutants.py whose source is a file: each edit's
pattern occurs exactly once in that file at the tree's head (a FIXTURE
otherwise). usage: render_anchor_check.py <tree-root>"""
import sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tb/verilator/milan_dp_render"))
import tdm8_render_mutants as m
bad = 0
for arm in m.MUTATIONS:
    name, source, edits = arm[0], arm[1], arm[2]
    path = m.SOURCES[source][0]
    if path.is_dir() or not path.is_file():
        print(f"skip (directory source) {name}")
        continue
    text = path.read_text()
    counts = [text.count(old) for old, _ in edits]
    ok = all(c == 1 for c in counts)
    bad += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {source:8s} {counts} {name}")
print(f"{len(m.MUTATIONS)} arms; {bad} with an anchor not found exactly once")
sys.exit(1 if bad else 0)
