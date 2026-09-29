#!/usr/bin/env python3
"""Check that the per-cycle and per-step tables in the live PR body equal the pages' tables.

usage: pr_body_tables.py <repo-at-head> <pr-body.md>
"""
import sys
from pathlib import Path


def blocks(text):
    out, cur = [], []
    for line in text.splitlines():
        if line.startswith("|"):
            cur.append(line)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return {b[0]: b for b in out}


repo, body = Path(sys.argv[1]), Path(sys.argv[2]).read_text()
pages = {}
for p in ("docs/findings/599_394_E1_LINK_CYCLES.md", "docs/findings/387_SOFTWARE_GM_STEP.md"):
    pages.update(blocks((repo / p).read_text()))
fails = 0
for head, b in blocks(body).items():
    if head.startswith(("| Cycle |", "| Run | Edge |")):
        same = pages.get(head) == b
        fails += not same
        print(("IDENTICAL" if same else "DIFFERS  ") + f" ({len(b)} lines) {head[:60]}")
    else:
        print(f"PR-only   ({len(b)} lines) {head[:60]}")
sys.exit(1 if fails else 0)
