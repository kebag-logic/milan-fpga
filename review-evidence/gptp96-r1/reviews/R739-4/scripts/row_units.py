"""List the unit each protocol-constants row gets from its Meaning cell.
Usage: python3 -I row_units.py <INTEGRATION.md> <regex>"""
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
unit_re = re.compile(sys.argv[2])
on = False
for line in text.splitlines():
    if line.startswith("## "):
        on = line.strip() == "## Protocol constants"
        continue
    m = re.match(r"^\|\s*`([A-Za-z_][A-Za-z0-9_]*)`\s*\|", line.strip())
    if on and m:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        u = unit_re.search(cells[2]) if len(cells) > 2 else None
        print(f"{m.group(1):20s} {cells[1]:>10s}  unit={u.group(1) if u else '-':4s} meaning={cells[2]!r}")
