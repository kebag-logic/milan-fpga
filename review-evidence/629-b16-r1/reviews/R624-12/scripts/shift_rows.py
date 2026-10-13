#!/usr/bin/env python3
"""R624-12 probe: copy a check, moving every page-row locator in its ROWS block by N lines.

usage: shift_rows.py <check.py> <N> <out check.py> <out summary.json>

Only lines between '# ROWS-BEGIN' and '# ROWS-END' whose first tab field is a bare line number are
changed; README.md:<n> rows, comments and every byte outside the block are copied unchanged.
"""
import json
import sys

src, n, out, summ = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
text = open(src, encoding="utf-8").read()
a = text.index("# ROWS-BEGIN\n") + len("# ROWS-BEGIN\n")
b = text.index("# ROWS-END")
moved = readme = other = 0
lines = []
for x in text[a:b].split("\n"):
    f = x.split("\t", 1)
    if len(f) == 2 and f[0].isdigit():
        x = f"{int(f[0]) + n}\t{f[1]}"
        moved += 1
    elif x.startswith("README.md:"):
        readme += 1
    elif x:
        other += 1
    lines.append(x)
open(out, "w", encoding="utf-8").write(text[:a] + "\n".join(lines) + text[b:])
json.dump({"shift": n, "page_rows_moved": moved, "readme_rows": readme, "other_lines": other},
          open(summ, "w"), indent=1)
print(json.dumps({"shift": n, "page_rows_moved": moved, "readme_rows": readme, "other_lines": other}))
