#!/usr/bin/env python3
"""Compare D3 15.1 selected-option cells with the manager ruling, byte for byte,
and compare the FASTCONNECT section 16 checkbox state sequence at two commits.

Usage: check_register_and_checklist.py <clone> <issue70_comments.json> <old> <new>
"""
import json, re, subprocess, sys
clone, cj, old, new = sys.argv[1:5]
def show(rev, path):
    return subprocess.run(["git", "-C", clone, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
ruling = next(c["body"] for c in json.load(open(cj)) if c["id"] == 5862405632)
rul = {}
for line in ruling.splitlines():
    m = re.match(r"\| (DR\w+) \| (.*) \|$", line)
    if m:
        rul[m.group(1)] = m.group(2)
rc = 0
for rev in (old, new):
    d3 = show(rev, "docs/design/SAVED_STATE_MATERIALIZATION.md")
    reg = d3.split("### 15.1 Manager decision register", 1)[1].split("DR3b's source evidence", 1)[0]
    rows = {}
    for line in reg.splitlines():
        m = re.match(r"\| (DR\w+): .*?\*\*RULED\*\* \| (.*?) \| (.*?) \| (.*?) \|$", line)
        if m:
            rows[m.group(1)] = m.group(3)
    same = [k for k in rul if rows.get(k) == rul[k]]
    print(f"{rev[:8]}: register rows RULED {len(rows)}, selected-option byte-equal to ruling {len(same)}/{len(rul)}")
    if len(same) != len(rul) or len(rows) != 10:
        rc = 1
seqs = []
for rev in (old, new):
    fc = show(rev, "docs/design/SAVED_STATE_FASTCONNECT.md")
    sec = fc.split("## 16. Acceptance for the implementation", 1)[1]
    seq = "".join("x" if m.group(1) == "x" else "-" for m in re.finditer(r"^- \[( |x)\]", sec, re.M))
    seqs.append(seq)
    print(f"{rev[:8]}: section 16 checkboxes {len(seq)} checked {seq.count('x')} sequence {seq}")
print("checkbox sequence identical:", seqs[0] == seqs[1])
if seqs[0] != seqs[1]:
    rc = 1
sys.exit(rc)
