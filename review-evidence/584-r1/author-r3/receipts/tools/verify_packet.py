#!/usr/bin/env python3
"""Verify every local receipt against INDEX.md, including complete file coverage.

The detached corrected historical indexes have their own immutable Git corpus;
use auditidx.py for those. This check verifies their bytes like every other file.
"""
import argparse
import hashlib
import re
import sys
import tempfile
from pathlib import Path

ROW = re.compile(r'^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|', re.M)


def audit(root):
    rows = ROW.findall((root / 'INDEX.md').read_text())
    errors = []
    listed = set()
    for name, size, sha in rows:
        p = root / name
        if name in listed:
            errors.append('DUPLICATE_ROW ' + name)
        listed.add(name)
        if not p.is_file():
            errors.append('MISSING_FILE ' + name)
            continue
        raw = p.read_bytes()
        if len(raw) != int(size):
            errors.append('SIZE_MISMATCH ' + name)
        if hashlib.sha256(raw).hexdigest() != sha:
            errors.append('HASH_MISMATCH ' + name)
    present = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p != root / 'INDEX.md'}
    errors += ['UNINDEXED_FILE ' + name for name in sorted(present - listed)]
    if not rows:
        errors.append('EMPTY_INDEX')
    return len(rows), errors


def selftest():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        original = b'pass\n'
        (root / 'result.txt').write_bytes(original)
        (root / 'INDEX.md').write_text(f'| `result.txt` | {len(original)} | `{hashlib.sha256(original).hexdigest()}` |\n')
        assert audit(root) == (1, [])
        (root / 'result.txt').write_bytes(b'fail\n')
        assert 'HASH_MISMATCH result.txt' in audit(root)[1]
        (root / 'result.txt').write_bytes(b'failure\n')
        assert 'SIZE_MISMATCH result.txt' in audit(root)[1]
        (root / 'result.txt').write_bytes(original)
        (root / 'unlisted.txt').write_bytes(original)
        assert 'UNINDEXED_FILE unlisted.txt' in audit(root)[1]
    print('Index selftest: PASS; same-size hash, changed-size and omitted-file plants caught by name')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipts', type=Path, nargs='?')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return 0
    if args.receipts is None:
        parser.error('receipts directory is required')
    count, errors = audit(args.receipts)
    for error in errors:
        print(error)
    print(f'Index check: {count} rows; {len(errors)} failures')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
