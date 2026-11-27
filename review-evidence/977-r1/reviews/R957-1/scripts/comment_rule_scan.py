#!/usr/bin/env python3
"""Reviewer scan: comment-rule tokens (review rounds, issue-comment IDs, lane names, role labels) added by a
range in tracked non-Markdown source files, as new instances (count at head minus count at base, per file and token).

usage: comment_rule_scan.py <repo> <base> <head>
"""
import re
import subprocess
import sys
from collections import Counter

repo, base, head = sys.argv[1:4]
PATTERNS = {
    "review-round": re.compile(r"\bround[s]? \d+\b|\bround \d+'s\b|\bits round \d+\b|\bround-\d+\b"),
    "issue-comment-id": re.compile(r"issuecomment-\d+|\bcomment \d{8,}\b|\brulings? \d{8,}\b"),
    "lane-name": re.compile(r"\blane [A-Z]\d+[a-z]?\b|\bto S\d+\b|\bS1\d\b"),
    "role-label": re.compile(r"\[[AR]\d+(?:-[a-z])?\]|\bthe manager\b"),
    "bench-lane": re.compile(r"\bB\d{1,3}\b"),
}


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True).stdout


def count(rev: str, path: str) -> Counter:
    try:
        text = git("show", f"{rev}:{path}")
    except subprocess.CalledProcessError:
        return Counter()
    found = Counter()
    for name, rx in PATTERNS.items():
        for m in rx.finditer(text):
            found[(name, m.group(0))] += 1
    return found


changed = [p for p in git("diff", "--name-only", f"{base}..{head}").split()
           if not p.endswith((".md", ".png", ".svg", ".drawio", ".json")) and not p.startswith(("docs/", "third_party/"))]
total = 0
for path in changed:
    before, after = count(base, path), count(head, path)
    new = {k: after[k] - before[k] for k in after if after[k] > before[k]}
    for (name, token), n in sorted(new.items()):
        total += n
        lines = [i + 1 for i, ln in enumerate(git("show", f"{head}:{path}").splitlines()) if token in ln]
        print(f"{path}\t{name}\t{token!r}\t+{n}\tlines {lines[:12]}")
print(f"TOTAL new instances: {total}")
