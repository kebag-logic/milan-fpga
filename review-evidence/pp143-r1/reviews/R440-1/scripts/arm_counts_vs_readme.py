#!/usr/bin/env python3
"""Compare 'ARM: rc=R failures=N named=M KILLED' summary lines with a README table whose
last column starts with the failing-check count 'N:' (adp, aecp, dispatch tables).
usage: arm_counts_vs_readme.py README SECTION_START SUMMARY"""
import re
import sys
readme, start, summary = open(sys.argv[1]).read(), sys.argv[2], open(sys.argv[3]).read()
section = readme[readme.index(start):]
table = {}
for line in section.splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("| `") else None
    if cells:
        m = re.match(r"(\d+)\b", cells[-1])
        if m:
            table.setdefault(cells[0].strip("`"), int(m.group(1)))
run = {a: int(n) for a, n in re.findall(r"^([\w.-]+): rc=\d+ failures=(\d+) named=\d+ KILLED$",
                                        summary, re.M)}
common = sorted(set(run) & set(table))
mism = {a: (table[a], run[a]) for a in common if table[a] != run[a]}
print(f"KILLED arms {len(run)}, README rows with a count {len(table)}, compared {len(common)}, "
      f"arms without a README count {sorted(set(run) - set(table))}, mismatches {mism}")
sys.exit(bool(mism))
