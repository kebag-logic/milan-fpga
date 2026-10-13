#!/usr/bin/env python3
"""Round 10: missing source starts and digit loss, duplication or substitution in parser output.
Usage: python -B r10_reader_controls.py CHECK REPO SCRATCH OUT.json
These mutations change parser results in memory, never source files or requirements.
"""
import importlib.util
import json
import sys
from pathlib import Path

check, repo, scratch, output = sys.argv[1:]
scratch = Path(scratch)
scratch.mkdir(parents=True, exist_ok=True)
page, index = scratch / "page.md", scratch / "README.md"
index.write_text("")
sys.argv = [check, str(page), str(scratch), str(scratch / "rows.tsv"), str(scratch / "coverage.tsv"), "--repo", repo]
spec = importlib.util.spec_from_file_location("figures", check)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
original = C.tree
results = []
cases = [("paragraph", "value 7 ppm\n"), ("heading", "## value 7 ppm\n"),
         ("table_cell", "| name | value |\n|---|---|\n| x | 7 ppm |\n"),
         ("block_quote", "> value 7 ppm\n"), ("list", "- value 7 ppm\n"),
         ("item", "- value 7 ppm\n"), ("emph", "value *7* ppm\n"),
         ("strong", "value **7** ppm\n"), ("link", "value [7](#target) ppm\n"),
         ("text", "value 7 ppm\n"), ("code", "value `7` ppm\n"),
         ("document", "value 7 ppm\n")]
for kind, source in cases:
    page.write_text(source)
    nodes = original(page)
    at = next(i for i, n in enumerate(nodes) if n[0] == kind and (kind != "table_cell" or n[1] == 3))
    changed = list(nodes)
    n = nodes[at]
    changed[at] = (n[0], 0, 0, *n[3:])
    C.tree = lambda p, ns=changed: ns if p == page else original(p)
    scope = {(page.name, i): (line, 0) for i, line in enumerate(C.lines_of(page), 1)}
    read, refused = C.blocks(scope)
    met = any(why == C.NOPOS for where, block, why in refused)
    results.append(dict(case="missing start: " + kind, met=met,
                        refused=[dict(line=w[1], kind=b.split()[0], reason=y) for w,b,y in refused]))
for name, replacement in [("lost digit", ""), ("duplicated digit", "77"), ("substituted digit", "8")]:
    page.write_text("value 7 ppm\n")
    nodes = original(page)
    changed = [(*n[:5], n[5].replace("7", replacement), *n[6:]) if n[0] == "text" else n for n in nodes]
    C.tree = lambda p, ns=changed: ns if p == page else original(p)
    read, refused = C.blocks({(page.name, 1): ("value 7 ppm", 0)})
    met = any(why == C.SUM and w[1] == 1 for w, b, why in refused)
    results.append(dict(case=name, met=met, refused=[dict(line=w[1], reason=y) for w,b,y in refused]))
C.tree = original
out = dict(note="Offline parser-output mutations; source unchanged; no bench action", cases=results,
           all_met=all(r["met"] for r in results))
Path(output).write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({"cases": len(results), "met": sum(r["met"] for r in results)}))
raise SystemExit(0 if out["all_met"] else 1)
