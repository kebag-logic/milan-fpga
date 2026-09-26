#!/usr/bin/env python3
"""Print Vivado hierarchical-utilization rows below one instance.

usage: hier_rows.py <baseline_hierarchy.rpt> <instance-name> [max-depth]
Prints instance, module, total LUT, logic LUT, LUTRAM, SRL, FF, RAMB36,
RAMB18, DSP for the named instance and its descendants, sorted by the
report's own order, with the depth relative to that instance.
"""
import sys
from pathlib import Path


def rows(text: str) -> list[tuple[int, list[str]]]:
    """Return (indent, cells) for every data row of the hierarchy table."""
    out = []
    for line in text.splitlines():
        if not line.startswith("| ") or "Instance" in line:
            continue
        cells = line.split("|")[1:-1]
        if len(cells) < 10:
            continue
        name = cells[0]
        indent = len(name) - len(name.lstrip(" "))
        out.append((indent, [c.strip() for c in cells]))
    return out


def main() -> None:
    """Select the subtree and print it."""
    path, inst = Path(sys.argv[1]), sys.argv[2]
    depth = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    table = rows(path.read_text())
    start = next(i for i, (_, c) in enumerate(table) if c[0] == inst)
    base = table[start][0]
    print(f"{'instance':34} {'module':36} " + " ".join(
        f"{h:>7}" for h in ("LUT", "logic", "LUTRAM", "SRL", "FF", "RAMB36", "RAMB18", "DSP")))
    for indent, cells in table[start:]:
        if indent <= base and cells is not table[start][1]:
            break
        level = (indent - base) // 2
        if level > depth:
            continue
        print(f"{'  ' * level + cells[0]:34} {cells[1][-36:]:36} " + " ".join(
            f"{c:>7}" for c in cells[2:10]))


if __name__ == "__main__":
    main()
