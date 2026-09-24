#!/usr/bin/env python3
"""Reviewer probe (R238-5): every tracked page's answers under one walk.

Usage: python probe_tracked_answers.py <scripts-dir> <pages-root> <out.json>

Imports `gen_toc` from <scripts-dir> (a head or a prior head) and, for every
tracked *.md page under <pages-root> (`git ls-files`), records blocks(),
line_kinds(), headings() with anchors, refusals() and plan(). Two outputs
compared with `cmp` show whether the correction changed any tracked answer
(acceptance 4 at this round).
"""
import json
import subprocess
import sys
from pathlib import Path

scripts, pages_root, out = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(scripts.resolve()))
import gen_toc  # noqa: E402

tracked = subprocess.run(["git", "-C", str(pages_root), "ls-files", "*.md"],
                         capture_output=True, text=True,
                         check=True).stdout.split()
answers = {}
for rel in tracked:
    text = (pages_root / rel).read_text(encoding="utf-8")
    answers[rel] = {"blocks": gen_toc.blocks(text),
                    "line_kinds": gen_toc.line_kinds(text),
                    "headings": gen_toc.headings(text),
                    "refusals": gen_toc.refusals(text),
                    "plan": gen_toc.plan(text)}
Path(out).write_text(json.dumps(answers, sort_keys=True, indent=0))
print(f"{len(answers)} tracked pages recorded")
