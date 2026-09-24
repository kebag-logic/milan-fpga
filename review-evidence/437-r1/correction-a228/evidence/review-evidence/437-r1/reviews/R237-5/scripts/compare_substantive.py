#!/usr/bin/env python3
"""Like compare_inventory.py, but a block-label difference counts only on a
line that is not blank (spaces/tabs only), since the head documents one
convention change: the blank line ending a raw HTML block is no longer
labelled with it. Usage: compare_substantive.py <inv_base> <inv_head> <shapes>
"""
import json
import sys

base = json.load(open(sys.argv[1]))
head = json.load(open(sys.argv[2]))
shapes = json.load(open(sys.argv[3]))["shapes"]
recorded = {s["page"]: s for s in shapes}
base_pages = {a[1] for arms in base["arms"].values() for a in arms}
rows = []
for page, hb in head["answers"].items():
    bb = base["answers"][page]
    lines = page.split("\n")
    lab = [i for i, (x, y) in enumerate(zip(bb["blocks"], hb["blocks"]))
           if x != y and lines[i].strip(" \t") != ""]
    blank_only = [i for i, (x, y) in enumerate(zip(bb["blocks"], hb["blocks"]))
                  if x != y and lines[i].strip(" \t") == ""]
    heads = bb["headings"] != hb["headings"]
    if lab or heads:
        rows.append((page, lab, heads))
print(f"substantive differences: {len(rows)} pages; "
      f"base-arm pages among them: {sum(p in base_pages for p, _, _ in rows)}")
miss = [r for r in rows if r[0] not in recorded]
print(f"without a recorded GitHub rendering: {len(miss)}")
for page, lab, heads in rows:
    tag = "recorded:" + recorded[page]["set"] if page in recorded else "NOT RECORDED"
    src = "base-arm" if page in base_pages else "head-only"
    print(f"- [{tag}; {src}] lines{lab} heads_differ={heads} {page!r}"[:300])
    if page not in recorded:
        print(f"    base {base['answers'][page]['blocks']} {base['answers'][page]['headings']}"[:300])
        print(f"    head {head['answers'][page]['blocks']} {head['answers'][page]['headings']}"[:300])
