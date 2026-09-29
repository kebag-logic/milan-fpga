#!/usr/bin/env python3
"""Check an evidence archive's MANIFEST.json against its files, and diff two archives.

usage: check_manifest.py <new-root> [<old-root>]
Each root is an extracted `review-evidence/b1-r1` directory. For <new-root>:
every manifest row's published_sha256 must equal the file's SHA-256, and every
file except MANIFEST.json must have exactly one row. With <old-root>, it lists
the files whose bytes changed, were added or were removed between the two, and
for each changed file prints its old and new manifest rows.
Prints only paths and hashes. Exit 1 on any closure mismatch, 0 otherwise.
"""
import hashlib
import json
import sys
from pathlib import Path


def load(root):
    root = Path(root)
    files = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(root.rglob("*")) if p.is_file()}
    files.pop("MANIFEST.json", None)  # the root manifest itself; nested MANIFEST files stay
    rows = json.loads((root / "MANIFEST.json").read_text())
    return files, rows


new_files, new_rows = load(sys.argv[1])
bad = 0
by_file = {}
for r in new_rows:
    by_file.setdefault(r["file"], []).append(r)
for f, rs in sorted(by_file.items()):
    if len(rs) != 1:
        print(f"DUPLICATE ROW {f} x{len(rs)}"); bad += 1
    if f not in new_files:
        print(f"ROW WITHOUT FILE {f}"); bad += 1
    elif rs[0]["published_sha256"] != new_files[f]:
        print(f"HASH MISMATCH {f} row {rs[0]['published_sha256'][:12]} file {new_files[f][:12]}"); bad += 1
for f in sorted(set(new_files) - set(by_file)):
    print(f"FILE WITHOUT ROW {f}"); bad += 1
print(f"closure: {len(new_files)} files, {len(new_rows)} rows, {bad} mismatches")

if len(sys.argv) > 2:
    old_files, old_rows = load(sys.argv[2])
    old_by = {r["file"]: r for r in old_rows}
    changed = sorted(f for f in set(new_files) & set(old_files) if new_files[f] != old_files[f])
    added = sorted(set(new_files) - set(old_files))
    removed = sorted(set(old_files) - set(new_files))
    print(f"vs old: {len(changed)} changed, {len(added)} added, {len(removed)} removed")
    for f in changed:
        o, n = old_by.get(f, {}), by_file[f][0]
        print(f"  CHANGED {f}")
        print(f"    old file {old_files[f]}  old row published {o.get('published_sha256')} original {o.get('original_sha256')} path_redacted {o.get('path_redacted')}")
        print(f"    new file {new_files[f]}  new row published {n.get('published_sha256')} original {n.get('original_sha256')} path_redacted {n.get('path_redacted')}")
        extra = {k: v for k, v in n.items() if k not in ("file", "original_sha256", "published_sha256", "path_redacted")}
        if extra:
            print(f"    new row extra fields {json.dumps(extra, sort_keys=True)}")
    for f in added:
        print(f"  ADDED {f}")
    for f in removed:
        print(f"  REMOVED {f}")
    rowdiff = sorted(f for f in set(by_file) & set(old_by)
                     if by_file[f][0] != old_by[f] and f not in changed)
    print(f"rows changed without a byte change: {len(rowdiff)}" + (" " + ", ".join(rowdiff) if rowdiff else ""))
sys.exit(1 if bad else 0)
