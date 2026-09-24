#!/usr/bin/env python3
"""Compare milan_dp leg run logs between two trees, line by line.

For each leg present in both directories, report whether the run logs are
byte-identical (after dropping the first `$ <command>` line, which carries the
tree path), and otherwise print a unified diff limited to --max lines. Used to
show (a) candidate vs reviewed source head: the composition changes no check
line of the source's legs, and (b) candidate vs dev tip: the only differences
are the lines the source adds.

Usage: compare_legs.py <dirA> <dirB> [--max N]
"""
import difflib
import sys
from pathlib import Path


def body(p: Path) -> list[str]:
    lines = p.read_text().splitlines()
    return lines[1:] if lines and lines[0].startswith("$ ") else lines


def main() -> int:
    a, b = Path(sys.argv[1]), Path(sys.argv[2])
    mx = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 80
    legs = sorted({p.name for p in a.glob("*.run.log")} & {p.name for p in b.glob("*.run.log")})
    ident = 0
    for leg in legs:
        la, lb = body(a / leg), body(b / leg)
        if la == lb:
            print("IDENTICAL %s (%d lines)" % (leg, len(la)))
            ident += 1
            continue
        d = list(difflib.unified_diff(la, lb, a.name + "/" + leg, b.name + "/" + leg, n=0, lineterm=""))
        adds = sum(1 for l in d if l.startswith("+") and not l.startswith("+++"))
        dels = sum(1 for l in d if l.startswith("-") and not l.startswith("---"))
        print("DIFFERS   %s (-%d +%d)" % (leg, dels, adds))
        for l in d[:mx]:
            print("    " + l[:200])
        if len(d) > mx:
            print("    ... %d more diff lines" % (len(d) - mx))
    print("%d of %d legs identical" % (ident, len(legs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
