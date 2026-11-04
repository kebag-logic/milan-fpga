#!/usr/bin/env python3
"""Recompute every `scripts` digest of ci/image/command-table.json against a tree's own bytes.
Prints the stale and missing entries so two trees can be compared (the checker's digest arm only).
Usage: python3 -I table_digests.py TREE"""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1]); t = json.loads((root / 'ci/image/command-table.json').read_text())
stale, missing, ok = [], [], 0
for path, row in sorted(t['scripts'].items()):
    if not isinstance(row, dict) or 'sha256' not in row: continue
    f = root / path
    if not f.is_file(): missing.append(path); continue
    if hashlib.sha256(f.read_bytes()).hexdigest() != row['sha256']: stale.append(path)
    else: ok += 1
print(f"entries ok={ok} stale={len(stale)} missing={len(missing)}")
for p in stale: print("STALE", p)
for p in missing: print("MISSING", p)
