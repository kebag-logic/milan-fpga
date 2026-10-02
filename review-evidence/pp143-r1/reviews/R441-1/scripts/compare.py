#!/usr/bin/env python3
"""Compare a --jobs 1 run with a --jobs 8 run of one driver.

usage: compare.py STDOUT_A STDOUT_B OUTDIR_A OUTDIR_B
Checks: the two summaries (stdout) identical line for line; the same set of
receipt files; in every receipt the same FAIL lines (in order) and the same
tally lines; results.json / coverage.txt byte-identical where present.
Prints one line per check and a final MATCH or DIFFER.
"""
import re
import sys
from pathlib import Path

TALLY = re.compile(r"(\d+ checks?[:,].*(PASS|FAIL|failures).*|return code: .*)")


def facts(path: Path) -> tuple[list[str], list[str]]:
    lines = path.read_text(errors="replace").splitlines()
    fails = [l for l in lines if l.startswith("FAIL")]
    tallies = [m.group(0) for l in lines if (m := TALLY.search(l))]
    return fails, tallies


def main() -> int:
    sa, sb, da, db = map(Path, sys.argv[1:5])
    ok = True
    a, b = sa.read_text().splitlines(), sb.read_text().splitlines()
    same = a == b
    ok &= same
    print(f"summary: {len(a)} vs {len(b)} lines, {'identical' if same else 'DIFFERENT'}")
    if not same:
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print(f"  first difference at line {i + 1}:\n  - {x}\n  + {y}")
                break
    fa = sorted(p.relative_to(da).as_posix() for p in da.rglob("*") if p.is_file())
    fb = sorted(p.relative_to(db).as_posix() for p in db.rglob("*") if p.is_file())
    ok &= fa == fb
    print(f"receipts: {len(fa)} vs {len(fb)} files, {'same names' if fa == fb else 'DIFFERENT names'}")
    nfail = 0
    for name in sorted(set(fa) & set(fb)):
        pa, pb = da / name, db / name
        if name.endswith(("results.json", "coverage.txt")):
            eq = pa.read_bytes() == pb.read_bytes()
            print(f"  {name}: {'byte-identical' if eq else 'DIFFERENT'}")
            ok &= eq
            continue
        xa, xb = facts(pa), facts(pb)
        nfail += len(xa[0])
        if xa != xb:
            ok = False
            print(f"  {name}: FAIL/tally lines DIFFERENT")
    print(f"FAIL lines compared: {nfail}")
    print("MATCH" if ok else "DIFFER")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
