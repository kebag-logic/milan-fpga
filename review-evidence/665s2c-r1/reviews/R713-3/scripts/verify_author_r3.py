#!/usr/bin/env python3
"""Check the round-3 author receipts of review-evidence/665s2c-r1 against its MANIFEST.json.

Usage: python3 -I verify_author_r3.py <extracted review-evidence/665s2c-r1 directory>
Prints one line per mismatch and a total; exit 1 on any mismatch or missing file.
Also compares the round-3 1x1 table.md with round 2's regrade of the same arm.
"""
import hashlib
import json
import sys
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    root = Path(sys.argv[1])
    entries = [e for e in json.loads((root / 'MANIFEST.json').read_text()) if e['file'].startswith('author-r3/')]
    bad = 0
    for e in entries:
        p = root / e['file']
        if not p.is_file():
            print('MISSING', e['file']); bad += 1
        elif sha(p) != e['published_sha256']:
            print('MISMATCH', e['file']); bad += 1
    on_disk = sum(1 for p in (root / 'author-r3').rglob('*') if p.is_file())
    print(f'author-r3: {len(entries)} manifest entries, {on_disk} files on disk, {bad} mismatched or missing')
    r3 = root / 'author-r3/receipts/run-1x1-64x1/table.md'
    r2 = root / 'author/receipts/regrade/arms/P1-64x1/table.md'
    if r2.is_file():
        print(f'table.md round 3 {sha(r3)}\ntable.md round 2 {sha(r2)}\nidentical: {sha(r3) == sha(r2)}')
    return 1 if bad or on_disk != len(entries) else 0


if __name__ == '__main__':
    sys.exit(main())
