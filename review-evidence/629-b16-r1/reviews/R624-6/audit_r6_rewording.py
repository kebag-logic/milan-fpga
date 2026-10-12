#!/usr/bin/env python3
"""R624-6: round 6 reworded the covered text "within its lines". Check, line by line between the page at
36190193 and at e91a62ee, that no line moved before the new subsection, and that every line keeps its
digit runs, its link targets and its verdict words (PASS/FAIL/NOT RUN/MISMATCH/SAMPLE-EXACT/PRESENT/ABSENT/
Met/met/LOCKED) in order. Lines that differ only otherwise are listed with both texts for reading.

usage: audit_r6_rewording.py <old page> <new page> <old README> <new README> <out.json>"""
import json, re, sys
old, new = (open(p, encoding="utf-8").read().split("\n") for p in sys.argv[1:3])
ro, rn = (open(p, encoding="utf-8").read().split("\n") for p in sys.argv[3:5])
NUM = re.compile(r"\d+")
LINK = re.compile(r"\]\(([^)]+)\)")
VERD = re.compile(r"\b(PASS|FAIL|NOT RUN|MISMATCH|SAMPLE-EXACT|PRESENT|ABSENT|STOP|Met|met|NOT met|LOCKED|ACQUIRE|IDLE|Graded|Done|Not needed)\b")
new_sub = next(i for i, l in enumerate(new) if l.startswith("### B16, round 6: the closed list"))
res = dict(changed=[], digit_changes=[], link_changes=[], verdict_changes=[], lines_old=len(old), new_subsection_line=new_sub + 1)
for i in range(min(new_sub, len(old))):
    a, b = old[i], new[i]
    if a == b:
        continue
    d = dict(line=i + 1, old=a, new=b)
    res["changed"].append(d)
    if NUM.findall(a) != NUM.findall(b):
        res["digit_changes"].append(d)
    if LINK.findall(a) != LINK.findall(b):
        res["link_changes"].append(d)
    if VERD.findall(a) != VERD.findall(b):
        res["verdict_changes"].append(d)
json.dump(res, open(sys.argv[5], "w"), indent=1, ensure_ascii=False)
print("changed lines before round 6's subsection:", len(res["changed"]))
print("lines whose digit runs changed:", len(res["digit_changes"]))
for d in res["digit_changes"]:
    print("  L%d\n   - %s\n   + %s" % (d["line"], d["old"][:300], d["new"][:300]))
print("lines whose link targets changed:", len(res["link_changes"]))
for d in res["link_changes"]:
    print("  L%d\n   - %s\n   + %s" % (d["line"], d["old"][:300], d["new"][:300]))
print("lines whose verdict words changed:", len(res["verdict_changes"]))
for d in res["verdict_changes"]:
    print("  L%d\n   - %s\n   + %s" % (d["line"], d["old"][:300], d["new"][:300]))
