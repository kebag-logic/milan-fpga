"""#817: compare two routed `report_exceptions` files as sets of exceptions, ignoring Vivado's position numbers.

Each exception is one table entry, its wrapped continuation lines joined back, its leading position dropped.
Prints the exceptions only in the first, only in the second, and the counts.
usage: python3 exceptions_diff.py <dev exceptions.rpt> <head exceptions.rpt>
"""
import re
import sys
from collections import Counter
from pathlib import Path


def entries(path: Path) -> Counter:
    """Exceptions keyed by their columns with the wrapped text rejoined and the position removed."""
    lines = path.read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("Position"))
    header = lines[start]
    cuts = [m.start() for m in re.finditer(r"(?<=\s)\S", " " + header)]
    cuts = [c - 1 for c in cuts]
    rows, current = [], None
    for line in lines[start + 2:]:
        if not line.strip():
            continue
        if line[:cuts[1]].strip():
            current = [line[a:b].strip() for a, b in zip(cuts, cuts[1:] + [None])]
            rows.append(current)
        elif current is not None:
            for k, (a, b) in enumerate(zip(cuts, cuts[1:] + [None])):
                current[k] += line[a:b].strip()
    return Counter(" | ".join(row[1:]) for row in rows)


dev, head = entries(Path(sys.argv[1])), entries(Path(sys.argv[2]))
print(f"dev exceptions: {sum(dev.values())}   head exceptions: {sum(head.values())}")
for label, diff in (("only at dev", dev - head), ("only at head", head - dev)):
    print(f"{label}: {sum(diff.values())}")
    for key, count in sorted(diff.items()):
        print(f"  {count} x {key}")
