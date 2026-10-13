#!/usr/bin/env python3
"""Copy a reviewed tree to a disposable directory and apply one mutation.

Usage: python3 -I apply_mutation.py <readonly-tree> <dest-dir> <mutations.json> <id>
Each mutation is [id, path, old, new]; `old` must occur exactly once.
"""
import json
import pathlib
import shutil
import stat
import sys

tree, dest, muts, ident = sys.argv[1:5]
dest_path = pathlib.Path(dest)
if dest_path.exists():
    for p in dest_path.rglob("*"):
        if not p.is_symlink():
            p.chmod(p.stat().st_mode | stat.S_IWUSR)
    shutil.rmtree(dest_path)
shutil.copytree(tree, dest_path, symlinks=True)
for p in dest_path.rglob("*"):
    if not p.is_symlink():
        p.chmod(p.stat().st_mode | stat.S_IWUSR)
for i, path, old, new in json.load(open(muts)):
    if i == ident:
        target = dest_path / path
        text = target.read_text()
        assert text.count(old) == 1, f"{ident}: anchor count {text.count(old)}"
        target.write_text(text.replace(old, new, 1))
        print(f"{ident}: applied to {path}")
