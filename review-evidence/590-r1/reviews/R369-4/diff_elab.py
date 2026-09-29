#!/usr/bin/env python3
"""Compare two probe_elab.py output trees after normalizing local paths and timestamps.

Usage: diff_elab.py <base-dir> <base-root> <cand-dir> <cand-root>
Prints one line per file (IDENTICAL / DIFFERS / ONLY-IN) and exits 1 on any
difference. Normalization: each tree's checkout root and build dir become
fixed tokens, and LiteX's generation date lines are dropped.
"""
import hashlib
import re
import sys
from pathlib import Path

DATE = re.compile(rb'(on \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|\(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\)'
                  rb'|Date\s*: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')


def normalized(path: Path, build: Path, root: Path) -> bytes:
    data = path.read_bytes()
    data = data.replace(str(build).encode(), b'<BUILD>').replace(str(root).encode(), b'<ROOT>')
    return DATE.sub(b'<DATE>', data)


def listing(build: Path) -> dict:
    return {p.relative_to(build): p for p in build.rglob('*')
            if p.is_file() and 'measurement_firmware' not in p.parts and p.name != 'litex.log'}


def main() -> None:
    base, base_root, cand, cand_root = (Path(a).resolve() for a in sys.argv[1:5])
    left, right = listing(base), listing(cand)
    differ = 0
    for rel in sorted(set(left) | set(right)):
        if rel not in left or rel not in right:
            print(f'ONLY-IN-{"cand" if rel in right else "base"} {rel}')
            differ += 1
            continue
        a = normalized(left[rel], base, base_root)
        b = normalized(right[rel], cand, cand_root)
        same = a == b
        differ += not same
        print(f'{"IDENTICAL" if same else "DIFFERS  "} {hashlib.sha256(b).hexdigest()[:16]} {rel}')
    print(f'files={len(set(left) | set(right))} differing={differ}')
    sys.exit(1 if differ else 0)


if __name__ == '__main__':
    main()
