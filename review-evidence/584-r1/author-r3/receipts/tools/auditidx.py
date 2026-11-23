#!/usr/bin/env python3
"""auditidx.py REPO COMMIT INDEX RECEIPTS: check every row of a receipts index against the blobs of an immutable
commit. INDEX is a path inside COMMIT's tree, or a local file; RECEIPTS is the tree path the index's rows are
relative to. Prints `<matching>/<rows>` and each row that does not match its blob's size and sha256."""
import hashlib
import re
import subprocess
import sys
from pathlib import Path


def blob(repo: str, commit: str, path: str) -> bytes | None:
    """The bytes of PATH at COMMIT, or None when it is not there."""
    out = subprocess.run(['/usr/bin/git', '-C', repo, 'show', f'{commit}:{path}'], capture_output=True, check=False)
    return out.stdout if out.returncode == 0 else None


def main() -> int:
    """Audit one index; 0 when every row matches."""
    repo, commit, index, receipts = sys.argv[1:5]
    text = Path(index).read_text() if Path(index).is_file() else (blob(repo, commit, index) or b'').decode()
    rows = re.findall(r"^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|", text, re.M)
    bad = []
    for rel, size, sha in rows:
        data = blob(repo, commit, f'{receipts}/{rel}')
        if data is None or len(data) != int(size) or hashlib.sha256(data).hexdigest() != sha:
            got = 'absent' if data is None else f'{len(data)} B {hashlib.sha256(data).hexdigest()}'
            bad.append(f'{rel}: indexed {size} B {sha}, published {got}')
    print(f'{len(rows) - len(bad)}/{len(rows)}')
    for line in bad:
        print(f'  {line}')
    return 1 if bad or not rows else 0


if __name__ == '__main__':
    sys.exit(main())
