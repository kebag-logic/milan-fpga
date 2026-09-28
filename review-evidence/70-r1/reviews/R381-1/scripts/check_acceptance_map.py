#!/usr/bin/env python3
"""FASTCONNECT section 16 checklist vs D3 section 17 reconciliation rows.

Run from repository root: check_acceptance_map.py <base-rev>
Reports per-group checkbox counts at base and head, checked-state
sequence at base and head, and D3 section 17 row counts per group.
"""
import re, subprocess, sys
base = sys.argv[1]
def show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True).stdout
FC = "docs/design/SAVED_STATE_FASTCONNECT.md"
D3 = "docs/design/SAVED_STATE_MATERIALIZATION.md"
def boxes(text):
    sec = text.split("## 16. Acceptance for the implementation", 1)[1]
    grp = None; out = []
    for l in sec.splitlines():
        m = re.match(r"^\*\*(.+)\*\*\s*$", l)
        if m: grp = m.group(1); continue
        m = re.match(r"^- \[( |x)\] (.*)", l)
        if m: out.append((grp, m.group(1) == "x", m.group(2)[:60]))
    return out
b, h = boxes(show(base, FC)), boxes(open(FC, encoding="utf-8").read())
def counts(bx):
    c = {}
    for g, _, _ in bx: c[g] = c.get(g, 0) + 1
    return c
print("base groups", counts(b), "total", len(b))
print("head groups", counts(h), "total", len(h))
print("base checked", [x for _, x, _ in b])
print("head checked", [x for _, x, _ in h])
same_state = [x for _, x, _ in b] == [x for _, x, _ in h]
d3 = open(D3, encoding="utf-8").read().split("## 17. Acceptance reconciliation", 1)[1].split("## 18.", 1)[0]
rows = [l for l in d3.splitlines() if re.match(r"^\| (Namespace|Container|Status|Saved set|Trigger|Area) \d", l)]
rc = {}
for l in rows:
    g = re.match(r"^\| (Namespace|Container|Status|Saved set|Trigger|Area)", l).group(1); rc[g] = rc.get(g, 0) + 1
print("d3 s17 rows", rc, "total", len(rows))
ok = same_state and len(rows) == len(h) and list(rc.values()) == list(counts(h).values())
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
