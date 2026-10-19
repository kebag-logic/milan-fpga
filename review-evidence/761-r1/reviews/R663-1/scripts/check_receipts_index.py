#!/usr/bin/env python3
"""Check a receipts INDEX.md (| `path` | bytes | sha256 |) against the files present.

Usage: check_receipts_index.py <receipts_dir>
Prints every mismatch; exit 0 only when the index and the tree agree exactly
(every file listed once with its size and SHA-256, no listed file missing,
INDEX.md itself excluded).
"""
import hashlib
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([\d,]+)\s*\|\s*`([0-9a-f]{64})`\s*\|")


def main() -> int:
    root = Path(sys.argv[1])
    index = root / "INDEX.md"
    listed = {}
    dup = []
    for line in index.read_text().splitlines():
        m = ROW.match(line)
        if m:
            path, size, sha = m.group(1), int(m.group(2).replace(",", "")), m.group(3)
            if path in listed:
                dup.append(path)
            listed[path] = (size, sha)
    present = {p.relative_to(root).as_posix(): p for p in root.rglob("*")
               if p.is_file() and p != index}
    bad = 0
    for path in sorted(set(listed) - set(present)):
        print(f"LISTED-NOT-PRESENT {path}"); bad += 1
    for path in sorted(set(present) - set(listed)):
        print(f"PRESENT-NOT-LISTED {path}"); bad += 1
    for path in dup:
        print(f"DUPLICATE {path}"); bad += 1
    for path in sorted(set(listed) & set(present)):
        data = present[path].read_bytes()
        size, sha = listed[path]
        if len(data) != size or hashlib.sha256(data).hexdigest() != sha:
            print(f"MISMATCH {path} index={size}/{sha[:12]} file={len(data)}/"
                  f"{hashlib.sha256(data).hexdigest()[:12]}"); bad += 1
    print(f"listed={len(listed)} present={len(present)} problems={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
