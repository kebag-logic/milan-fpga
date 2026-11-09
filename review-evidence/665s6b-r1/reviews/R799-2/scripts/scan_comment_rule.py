#!/usr/bin/env python3
"""Comment-rule scan: list the lines a range adds outside Markdown files that carry an issue-comment ID, a
ruling ID or a plan-lane label.

usage: scan_comment_rule.py REPO BASE HEAD [--broad]

The default pattern is the round-1 scan's (calibrated to reproduce its 43 lines at e69d243a against
6584b7bf). --broad adds bare lane labels (S<n>), review-round and reviewer IDs (R<n>, A<n>, B<n>) and the
words "plan's", "lane" and "round". Output: one "path:line: text" per hit, then a count.
"""
import re
import subprocess
import sys

REPO, BASE, HEAD = sys.argv[1:4]
BROAD = "--broad" in sys.argv[4:]
NARROW = re.compile(r"issuecomment|ruling \d|\bS\d+[a-z]\b|\bS1[0-9]\b")
WIDE = re.compile(r"\bS\d+[a-z]?\b|\b[ABR]\d+(-\d+)?\b|plan's|\blane\b|\bround\b", re.I)

diff = subprocess.run(["git", "-C", REPO, "diff", "-U0", "--no-color", f"{BASE}..{HEAD}", "--", ".",
                       ":(exclude)*.md"], capture_output=True, text=True, check=True).stdout
path, line, hits = None, 0, []
for raw in diff.splitlines():
    if raw.startswith("+++ "):
        path = raw[6:] if raw.startswith("+++ b/") else None
    elif raw.startswith("@@"):
        line = int(re.match(r"@@ -\S+ \+(\d+)", raw).group(1))
    elif raw.startswith("+") and path:
        text = raw[1:]
        if NARROW.search(text) or (BROAD and WIDE.search(text)):
            hits.append(f"{path}:{line}: {text.strip()}")
        line += 1
for h in hits:
    print(h)
print(f"{len(hits)} line(s)")
