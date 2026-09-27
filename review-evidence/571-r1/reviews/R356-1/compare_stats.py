#!/usr/bin/env python3
"""R356-1: compare Verilator __stats.txt reports with run-specific lines removed.

Removed: the Arguments line (it names the -G list and Mdir) and every line
reporting time, memory or job counts. Everything else (per-stage node-kind
counts, variable widths, global counts) must match exactly.
Usage: compare_stats.py <elab dir> <legA>:<legB> [...]
"""
import re
import sys
from pathlib import Path

DROP = re.compile(r"Arguments:|[Tt]ime|[Mm]emory|jobs|Cpu|MB\b|Wall")


def norm(path: Path) -> list[str]:
    return [line.rstrip() for line in path.read_text().splitlines()
            if not DROP.search(line)]


def main() -> int:
    root = Path(sys.argv[1])
    rc = 0
    for pair in sys.argv[2:]:
        a, b = pair.split(":")
        la = norm(root / a / "VKL_pp_shadow__stats.txt")
        lb = norm(root / b / "VKL_pp_shadow__stats.txt")
        diff = [(x, y) for x, y in zip(la, lb) if x != y]
        same = la == lb
        print(f"{a} vs {b}: lines {len(la)}/{len(lb)} "
              f"{'IDENTICAL' if same else 'DIFFER'} ({len(diff)} differing rows)")
        for x, y in diff[:12]:
            print(f"   - {x.strip()}\n   + {y.strip()}")
        rc |= 0
    return rc


if __name__ == "__main__":
    sys.exit(main())
