#!/usr/bin/env python3
"""Per-arm comparison of one campaign's receipts at base and head.
usage: compare_camp.py <base work dir> <head work dir>
For every log present on both sides, the set of failing-check lines (FAIL...
and the JSON verdict lines, normalised) is compared; prints a summary and the
differing lines, and the logs present on one side only."""
import re
import sys
from pathlib import Path

SUBS = [
    (re.compile(r"<submodule>|<lane>"), "<root>"),
    (re.compile(r"/tmp/[A-Za-z0-9_.-]+"), "<tmp>"),
    (re.compile(r"<scratch>/rec2/(base|head)-camps"), "<out>"),
    (re.compile(r"\b[0-9]+(\.[0-9]+)? ?(s|ms)\b"), "<t>"),
    (re.compile(r"all\.v:[0-9]+"), "all.v:N"),
]


def fails(p: Path) -> set[str]:
    out = set()
    for line in p.read_text(errors="replace").splitlines():
        s = line.strip()
        if s.startswith("FAIL") or '"verdict"' in s or "KILLED" in s or "SURVIVED" in s:
            for pat, rep in SUBS:
                s = pat.sub(rep, s)
            out.add(s)
    return out


def main() -> int:
    base, head = Path(sys.argv[1]), Path(sys.argv[2])
    bl = {p.relative_to(base): p for p in base.rglob("*.log")}
    hl = {p.relative_to(head): p for p in head.rglob("*.log")}
    same = differ = 0
    for k in sorted(set(bl) & set(hl)):
        a, b = fails(bl[k]), fails(hl[k])
        if a == b:
            same += 1
        else:
            differ += 1
            print(f"DIFF {k}")
            for x in sorted(a - b):
                print(f"   base only: {x[:220]}")
            for x in sorted(b - a):
                print(f"   head only: {x[:220]}")
    for k in sorted(set(bl) - set(hl)):
        print(f"BASE ONLY {k}: {len(fails(bl[k]))} FAIL lines")
    for k in sorted(set(hl) - set(bl)):
        print(f"HEAD ONLY {k}: {len(fails(hl[k]))} FAIL lines")
    print(f"common logs: {same} identical FAIL sets, {differ} differ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
