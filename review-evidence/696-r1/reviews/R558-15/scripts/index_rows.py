#!/usr/bin/env python3
"""Compare docs/findings/README.md across the dev base, the PR source head and the
composed candidate, row by row, and parse each version's table with the pinned
GFM renderer.

Usage: index_rows.py REPO DEV_SHA PR_SHA CAND_SHA OUT_JSON
Run with the interpreter that has the pinned cmarkgfm and html5lib installed.
Exit 0 only when every candidate line equals the dev line or the PR line, the
629 row equals dev, the 234 row equals PR, every other line equals both, and
each version renders one table with the same row count and three cells a row.
"""
import json
import subprocess
import sys

import cmarkgfm
import html5lib

repo, dev, pr, cand, out = sys.argv[1:]
PATH = "docs/findings/README.md"


def blob(rev):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{PATH}"],
                          capture_output=True, check=True).stdout.decode("utf-8")


def table_shape(text):
    html = cmarkgfm.github_flavored_markdown_to_html(text)
    doc = html5lib.parse(html, namespaceHTMLElements=False)
    tables = doc.findall(".//table")
    shapes = []
    for t in tables:
        rows = t.findall(".//tr")
        shapes.append([len(r.findall("td")) + len(r.findall("th")) for r in rows])
    return shapes


texts = {k: blob(v) for k, v in (("dev", dev), ("pr", pr), ("cand", cand))}
lines = {k: v.split("\n") for k, v in texts.items()}
ok = True
report = {"lines": {k: len(v) for k, v in lines.items()}, "rows": []}
if not (len(lines["dev"]) == len(lines["pr"]) == len(lines["cand"])):
    ok = False
for i, c in enumerate(lines["cand"]):
    d, p = lines["dev"][i], lines["pr"][i]
    if d == p == c:
        continue
    key = c.split("|")[1].strip()[:60] if c.startswith("|") else c[:60]
    side = "dev" if c == d else "pr" if c == p else "neither"
    report["rows"].append({"line": i + 1, "row": key, "cand_equals": side,
                           "dev_eq_pr": d == p})
    if side == "neither":
        ok = False
by_row = {r["row"].split("]")[0].lstrip("["): r["cand_equals"] for r in report["rows"]}
expect = {"629_MEDIA_CLOCK_FOLLOWING_BENCH.md": "dev", "234_PP_SHADOW_AREA_BASELINE.md": "pr"}
report["expected"] = expect
report["observed"] = by_row
if by_row != expect:
    ok = False
shapes = {k: table_shape(v) for k, v in texts.items()}
report["tables"] = {k: [{"rows": len(s), "cells_per_row": sorted(set(s))} for s in v]
                    for k, v in shapes.items()}
cand_tables = shapes["cand"]
if len(cand_tables) != 1 or set(cand_tables[0]) != {3}:
    ok = False
if [len(s) for s in shapes["cand"]] != [len(s) for s in shapes["dev"]]:
    ok = False
report["verdict"] = "PASS" if ok else "FAIL"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(report, fh, indent=1, sort_keys=True)
    fh.write("\n")
print(json.dumps({"verdict": report["verdict"], "differing": by_row,
                  "tables": report["tables"]["cand"]}))
sys.exit(0 if ok else 1)
