#!/usr/bin/env python3
"""Build one mutant copy of the head scripts (no self-test run), for probing.
Usage: make_mutant.py <head-root> <dest-root> <mutation-id-prefix>"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mutate import MUTATIONS  # noqa: E402

root, dest, prefix = sys.argv[1:4]
ident, name, old, new = next(m for m in MUTATIONS if m[0].startswith(prefix))
shutil.rmtree(dest, ignore_errors=True)
shutil.copytree(root, dest)
path = os.path.join(dest, "scripts", name)
text = open(path, encoding="utf-8").read()
assert text.count(old) == 1, ident
open(path, "w", encoding="utf-8").write(text.replace(old, new))
print("built", ident, "at", dest)
