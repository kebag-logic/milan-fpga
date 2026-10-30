#!/usr/bin/env python3
"""Reviewer scan (R732-1): added lines of a unified diff that show a lane label,
an issue-comment ID, a review round or a reviewer/bench label (owner comment
rule, 2026-10-15). Usage: git diff BASE..HEAD -- hdl sw tb scripts syn tests > d.diff
then python3 -I comment_rule_scan.py d.diff. Case-sensitive on purpose."""
import re
import sys

PAT = re.compile(r"\[(A|R)\d+[a-z]?(-[a-z])?\]|\bA\d{2,4}[a-d]?\b|\bR\d{3}\b|issuecomment"
                 r"|\bround (\d+|one|two|three|four)\b|\blane\b|\bB\d{1,2}\b|pre-run|reviewer")
path, line_no, hits = None, 0, 0
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    if line.startswith("+++ "):
        path = line[6:].strip()
        continue
    if line.startswith("@@"):
        line_no = int(re.search(r"\+(\d+)", line).group(1)) - 1
        continue
    if line.startswith("+"):
        line_no += 1
        if PAT.search(line):
            hits += 1
            print(f"{path}:{line_no}: {line[1:].rstrip()[:200]}")
    elif not line.startswith("-"):
        line_no += 1
print("hits:", hits)
