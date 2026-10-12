#!/usr/bin/env python3
"""R624-9: dump the pinned parser's nodes, as the figures check reads them, for small documents.

usage: <parser python> dump_nodes.py <check_b16_figures.py> <repo> <scratch dir> <doc.md>...
Loads the check as a module (its main does not run) and prints tree() and extents() for each document.
"""
import importlib.util
import sys
from pathlib import Path

CHECK, REPO, SCRATCH = sys.argv[1:4]
DOCS = sys.argv[4:]
SCRATCH = Path(SCRATCH)
SCRATCH.mkdir(parents=True, exist_ok=True)
sys.argv = [CHECK, str(SCRATCH / "page.md"), str(SCRATCH), str(SCRATCH / "r.tsv"), str(SCRATCH / "c.tsv"), "--repo", REPO]
spec = importlib.util.spec_from_file_location("check_b16_figures", CHECK)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

for doc in DOCS:
    p = Path(doc)
    nodes = C.tree(p)
    ext, last = C.extents(nodes, C.lines_of(p))
    print("==", doc)
    for (kind, sl, sc, el, ec, lit, url, d), x, la in zip(nodes, ext, last):
        print(f"{'  ' * d}{kind} rep=({sl},{sc})-({el},{ec}) ext={x} last={la} lit={lit[:50]!r} url={url[:40]!r}")
