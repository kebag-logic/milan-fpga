#!/usr/bin/env python3
"""Line diff of the live PR body against the archived round-4b body.

Strips one trailing newline added by the API fetch, prints a unified diff,
and classifies every change: only pure insertions are allowed.

usage: body_delta.py ARCHIVED_R4B.md LIVE.md
"""
import difflib
import sys

a = open(sys.argv[1], encoding="utf-8").read()
b = open(sys.argv[2], encoding="utf-8").read()
if b.endswith("\n") and not a.endswith("\n"):
    b = b[:-1]
al, bl = a.split("\n"), b.split("\n")
print(f"archived: {len(a)} chars, {len(al)} lines; live: {len(b)} chars, {len(bl)} lines; delta {len(b)-len(a)} chars")
sm = difflib.SequenceMatcher(None, al, bl, autojunk=False)
other = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    print(f"\n[{tag}] archived lines {i1+1}-{i2} -> live lines {j1+1}-{j2}")
    for x in al[i1:i2]:
        print("  - " + x)
    for x in bl[j1:j2]:
        print("  + " + x)
    if tag != "insert":
        other += 1
print(f"\nnon-insert changes: {other}")
# reconstruct: deleting the inserted live lines must give the archived body byte for byte
keep = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        keep.extend(bl[j1:j2])
    elif tag in ("replace", "delete"):
        keep.extend(["<<CHANGED>>"])
print("live minus inserted lines == archived:", "\n".join(keep) == a)
