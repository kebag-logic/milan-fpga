#!/usr/bin/env python3
"""Quoted Markdown pages published in the PR #515 R237/R238 reports.

Usage: prior_quoted_pages.py <pr515_comments.json> <repo> <out-pages.json>
Extracts every double- or single-quoted literal that spells a line break as
a backslash-n escape and carries `#` (a heading), decodes it as a Python
string literal, and reports whether the fixture holds that exact page
(trailing newline normalised). Writes the uncovered pages as probe input.
"""
import ast, json, re, sys
from pathlib import Path
comments = json.load(open(sys.argv[1])); repo = Path(sys.argv[2])
fixture = {s["page"].rstrip("\n") + "\n" for s in json.loads((repo / "scripts/gen_toc_shapes.json").read_text())["shapes"]}
seen, rows = set(), []
for c in comments:
    b = c["body"]
    if not (b.startswith("[R237") or b.startswith("[R238")):
        continue
    who = b.split("\n")[0].split(" - ")[0] + " " + b.split("exact head ")[1][:8]
    for m in re.finditer(r'''("(?:[^"\\\n]|\\.)*\\n(?:[^"\\\n]|\\.)*")|('(?:[^'\\\n]|\\.)*\\n(?:[^'\\\n]|\\.)*')''', b):
        lit = m.group(0)
        try:
            page = ast.literal_eval(lit)
        except Exception:
            continue
        if "#" not in page or page in seen:
            continue
        seen.add(page)
        rows.append({"report": who, "comment": c["id"], "page": page,
                     "in_fixture": page.rstrip("\n") + "\n" in fixture})
cov = sum(r["in_fixture"] for r in rows)
print(f"quoted pages: {len(rows)}, in fixture: {cov}, not in fixture: {len(rows) - cov}")
by = {}
for r in rows:
    by.setdefault(r["report"], [0, 0]); by[r["report"]][0] += 1; by[r["report"]][1] += r["in_fixture"]
for k, (n, f) in by.items():
    print(f"  {k}: {n} quoted pages, {f} in fixture")
Path(sys.argv[3]).write_text(json.dumps([{"name": f"prior {r['report']} #{i}", "page": r["page"]}
                                         for i, r in enumerate(rows) if not r["in_fixture"]], indent=1))
json.dump(rows, open(sys.argv[3].replace(".json", "-all.json"), "w"), indent=1)
