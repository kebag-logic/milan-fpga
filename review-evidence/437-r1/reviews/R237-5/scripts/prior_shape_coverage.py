#!/usr/bin/env python3
"""Which Markdown pages spelled literally in the prior PR #515 review
reports are in the committed shape fixture (by exact bytes)?
Usage: prior_shape_coverage.py <shapes.json> <report.md>...
A candidate is a single- or double-quoted Python-style literal carrying an
escaped line feed and a '#' (a page with a heading); it is decoded with
ast.literal_eval. Undecodable candidates are listed, not dropped."""
import ast, json, re, sys
pages = {s["page"] for s in json.load(open(sys.argv[1]))["shapes"]}
lit = re.compile(r"""(?<![A-Za-z0-9_])("(?:[^"\\\n]|\\.)*\\n(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*\\n(?:[^'\\\n]|\\.)*')""")
total = found = 0
for path in sys.argv[2:]:
    text = open(path, encoding="utf-8").read()
    miss, bad, seen = [], [], set()
    for m in lit.finditer(text):
        raw = m.group(1)
        if "#" not in raw:
            continue
        try:
            page = ast.literal_eval(raw)
        except Exception:
            bad.append(raw[:80]); continue
        if not isinstance(page, str) or page in seen:
            continue
        seen.add(page); total += 1
        if page in pages:
            found += 1
        else:
            miss.append(page)
    print(f"{path.split('/')[-1]}: {len(seen)} literal page(s), {len(seen) - len(miss)} in fixture, {len(miss)} not, {len(bad)} undecodable")
    for p in miss:
        print(f"    NOT IN FIXTURE: {p!r}"[:220])
print(f"total {total}, in fixture {found}")
