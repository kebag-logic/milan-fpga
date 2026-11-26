#!/usr/bin/env python3
"""Compare two plat_ledger.py build directories point by point.

For every point, each function symbol (nm -S, types t/T) whose name is unique in both
images is compared by address and size; the report lists the resized ones, the ones only
in one image, and how many moved, split by whether the symbol lies below or above the
lowest address of a resized or new function (code before the change cannot move).
Usage: python3 -I image_diff.py <nm> <base build dir> <head build dir>
"""
import subprocess
import sys
from collections import Counter
from pathlib import Path


def syms(nm, elf):
    out = subprocess.run([nm, "-S", "--defined-only", str(elf)], check=True, capture_output=True, text=True).stdout
    rows = [ln.split() for ln in out.splitlines()]
    rows = [(r[3], int(r[0], 16), int(r[1], 16)) for r in rows if len(r) == 4 and r[2] in "tT"]
    count = Counter(n for n, _, _ in rows)
    return {n: (a, s) for n, a, s in rows if count[n] == 1}


def main():
    nm, base, head = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    for pt in ("1x1-if1", "1x1-if2", "8x8-if1", "8x8-if2"):
        b = syms(nm, base / pt / "ctrl_app.elf")
        h = syms(nm, head / pt / "ctrl_app.elf")
        common = sorted(set(b) & set(h), key=lambda n: b[n][0])
        resized = [n for n in common if b[n][1] != h[n][1]]
        new = sorted(set(h) - set(b))
        gone = sorted(set(b) - set(h))
        first = min([b[n][0] for n in resized] + [h[n][0] for n in new] or [0])
        moved = [n for n in common if b[n][0] != h[n][0]]
        below = [n for n in moved if b[n][0] < first]
        print(f"POINT {pt}: {len(common)} unique functions in both; {len(common) - len(moved)} at their base address; "
              f"{len(moved)} moved ({len(below)} of them below the first changed function at 0x{first:x})")
        print("  resized: " + (", ".join(f"{n} {b[n][1]}->{h[n][1]} B @0x{b[n][0]:x}" for n in resized) or "none"))
        print("  only in head: " + (", ".join(f"{n} {h[n][1]} B @0x{h[n][0]:x}" for n in new) or "none"))
        print("  only in base: " + (", ".join(gone) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
