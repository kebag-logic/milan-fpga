#!/usr/bin/env python3
"""Re-hash every entry of an evidence archive's MANIFEST.json against the blobs at one commit.

usage: verify_manifest.py <git-dir> <commit> <prefix>   (prefix: e.g. review-evidence/665s8-r1)
Reads blobs with `git cat-file`, never checks anything out.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys


def blob(git: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(['git', '--git-dir', git, 'cat-file', 'blob', f'{rev}:{path}'], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def main() -> int:
    git, rev, prefix = sys.argv[1:4]
    entries = json.loads(blob(git, rev, f'{prefix}/MANIFEST.json'))
    listed = {e['file'] for e in entries}
    tree = subprocess.run(['git', '--git-dir', git, 'ls-tree', '-r', '--name-only', rev, prefix + '/'],
                          capture_output=True, text=True).stdout.split()
    present = {p[len(prefix) + 1:] for p in tree} - {'MANIFEST.json'}
    bad = missing = 0
    per_top: dict[str, int] = {}
    for e in entries:
        data = blob(git, rev, f"{prefix}/{e['file']}")
        if data is None:
            missing += 1
            print('MISSING', e['file'])
            continue
        if hashlib.sha256(data).hexdigest() != e['published_sha256']:
            bad += 1
            print('MISMATCH', e['file'])
        per_top[e['file'].split('/')[0]] = per_top.get(e['file'].split('/')[0], 0) + 1
    unlisted = sorted(present - listed)
    for p in unlisted:
        print('UNLISTED', p)
    print(f'entries {len(entries)}, mismatched {bad}, missing {missing}, unlisted {len(unlisted)}; per top: {per_top}')
    return 1 if bad or missing or unlisted else 0


if __name__ == '__main__':
    sys.exit(main())
