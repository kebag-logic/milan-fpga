"""s2_compare.py <base results dir> <head results dir> <point>: S2's path table at both pins, row by row (recorded, not graded)."""
import re, sys
from pathlib import Path
def rows(d):
    out, order = {}, []
    for line in (Path(d) / "table.md").read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 8 and cells[0] not in ("Path", "---") and not cells[0].startswith("-"):
            key = (cells[0], cells[1])
            if key not in out:
                out[key] = (cells[3], cells[4], cells[6], cells[7]); order.append(key)
    return out, order
b, ob = rows(sys.argv[1]); h, oh = rows(sys.argv[2])
print(f"### {sys.argv[3]}: S2's paths at 70936b77 and at 715589c (recorded, not graded)\n")
print("| Path | Interface | ms (bound) at 70936b77 | Verdict | ms (bound) at 715589c | Verdict | Instances, misses (old -> new) |")
print("|---|---:|---:|---|---:|---|---|")
for k in ob + [k for k in oh if k not in b]:
    x, y = b.get(k, ("-", "-", "-", "-")), h.get(k, ("-", "-", "-", "-"))
    mark = "" if x[1] == y[1] else " **changed**"
    print(f"| {k[0]} | {k[1]} | {x[0]} | {x[1]} | {y[0]} | {y[1]}{mark} | {x[2]}, {x[3]} -> {y[2]}, {y[3]} |")
