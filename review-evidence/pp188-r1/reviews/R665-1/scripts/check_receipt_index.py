#!/usr/bin/env python3
"""Check a receipt INDEX.md table against the files present beside it.

Usage: check_receipt_index.py DIR [MANIFEST.json]

DIR holds receipts/INDEX.md; its table rows are
| `path` | bytes | sha256 first 16 | first line |, with paths relative to DIR.
Every row must match a file (bytes, sha256 prefix, first line), and every
file under DIR except receipts/INDEX.md itself must have a row. An optional
publication MANIFEST.json (a list of {file, original_sha256, published_sha256,
path_redacted}) is checked against the files, and a path-redacted file's index
row is matched against its original_sha256.
Reads only; never executes anything from DIR.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\| `([^`]+)` \| (\d+) \| ([0-9a-f]{16}) \| (.*) \|$")


def first_line(data: bytes) -> str:
    """The index's rendering: first non-blank line, leading "#" and blanks dropped."""
    for raw in data.decode("utf-8", "replace").splitlines():
        if raw.strip():
            return raw.lstrip("# ").rstrip()
    return ""


def main() -> int:
    root = Path(sys.argv[1])
    index = root / "receipts" / "INDEX.md"
    text = index.read_text()
    m = re.search(r"^(\d+) files\.$", text, re.M)
    claimed = int(m.group(1)) if m else None
    rows = {}
    for line in text.splitlines():
        r = ROW.match(line)
        if r:
            rows[r.group(1)] = (int(r.group(2)), r.group(3), r.group(4))
    files = sorted(str(p.relative_to(root)) for p in root.rglob("*")
                   if p.is_file() and p != index)
    bad = 0
    # publication manifest: [{file, original_sha256, published_sha256, path_redacted}]
    man = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    pub = {}
    if man is not None:
        prefix = str(root.relative_to(man.parent))
        for e in json.loads(man.read_text()):
            rel = e["file"][len(prefix) + 1:] if e["file"].startswith(prefix + "/") else None
            pub[rel if rel is not None else "../" + e["file"]] = e
        mbad = 0
        present = {str(p.relative_to(man.parent)) for p in man.parent.rglob("*")
                   if p.is_file() and p != man}
        for e in json.loads(man.read_text()):
            pth = man.parent / e["file"]
            if not pth.is_file():
                print(f"MANIFEST MISSING {e['file']}")
                mbad += 1
            elif hashlib.sha256(pth.read_bytes()).hexdigest() != e["published_sha256"]:
                print(f"MANIFEST PUBLISHED-SHA MISMATCH {e['file']}")
                mbad += 1
            elif not e["path_redacted"] and e["original_sha256"] != e["published_sha256"]:
                print(f"MANIFEST unredacted file with differing shas {e['file']}")
                mbad += 1
        listed = {e["file"] for e in json.loads(man.read_text())}
        for f in sorted(present - listed):
            print(f"MANIFEST UNLISTED {f}")
            mbad += 1
        redacted = sum(1 for e in json.loads(man.read_text()) if e["path_redacted"])
        print(f"manifest entries {len(listed)}, files present {len(present)}, "
              f"path-redacted {redacted}, problems {mbad}")
        bad += mbad
    redacted_ok = 0
    for f in files:
        if f not in rows:
            print(f"UNINDEXED {f}")
            bad += 1
            continue
        data = (root / f).read_bytes()
        size, sha, fl = rows[f]
        e = pub.get(f)
        if e is not None and e["path_redacted"]:
            # the index describes the original bytes; the manifest ties them
            if e["original_sha256"][:16] != sha:
                print(f"MISMATCH {f}: index sha {sha} != manifest original {e['original_sha256'][:16]}")
                bad += 1
            else:
                redacted_ok += 1
            continue
        got = (len(data), hashlib.sha256(data).hexdigest()[:16])
        fl_file = first_line(data)
        fl_ok = fl_file.replace("|", "\\|").startswith(fl.rstrip()[:60]) or \
            fl_file.startswith(fl.rstrip()[:60]) or fl.rstrip() == ""
        if got != (size, sha) or not fl_ok:
            print(f"MISMATCH {f}: index {size} {sha} | file {got[0]} {got[1]} first-line-ok={fl_ok}")
            bad += 1
    for f in rows:
        if f not in files:
            print(f"MISSING {f}")
            bad += 1
    print(f"index rows {len(rows)}, claimed {claimed}, files present {len(files)}, "
          f"path-redacted rows matched via manifest {redacted_ok}")
    if claimed != len(files):
        print("COUNT MISMATCH")
        bad += 1
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'} ({bad} problems)")
    return int(bad != 0)


if __name__ == "__main__":
    raise SystemExit(main())
