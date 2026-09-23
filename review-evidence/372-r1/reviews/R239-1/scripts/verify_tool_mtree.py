#!/usr/bin/env python3
"""Verify every regular file listed in a pacman package mtree against its sha256digest.
Usage: verify_tool_mtree.py <package-root>  (root containing var/lib/pacman/local/<pkg>/mtree)"""
import gzip, hashlib, sys, pathlib
root = pathlib.Path(sys.argv[1])
pkg = sys.argv[2] if len(sys.argv) > 2 else "verilator-5.050-1"
mtree = root / "var/lib/pacman/local" / pkg / "mtree"
ok = bad = missing = 0
for raw in gzip.open(mtree, "rt"):
    line = raw.strip()
    if not line or line.startswith("#") or line.startswith("/set"):
        continue
    parts = line.split()
    path = parts[0]
    if path.startswith("./."):
        continue
    attrs = dict(p.split("=", 1) for p in parts[1:] if "=" in p)
    if attrs.get("type", "file") != "file" or "sha256digest" not in attrs:
        continue
    f = root / path[2:]
    if not f.is_file():
        missing += 1
        print("MISSING", path)
        continue
    digest = hashlib.sha256(f.read_bytes()).hexdigest()
    if digest == attrs["sha256digest"]:
        ok += 1
    else:
        bad += 1
        print("MISMATCH", path)
print(f"mtree {mtree}: match={ok} mismatch={bad} missing={missing}")
sys.exit(1 if bad else 0)
