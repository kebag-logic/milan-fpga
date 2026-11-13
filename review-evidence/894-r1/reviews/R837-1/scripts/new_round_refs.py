#!/usr/bin/env python3
"""Reviewer scan: lines ADDED by the lane (git diff BASE..HEAD, non-Markdown files) that name a review/lane round
("round N"), a reviewer or author ID ([R..], [A..], R123-4), a lane label (B17, S2b) or an issue-comment ID, with the
HEAD line number of each. usage: new_round_refs.py REPO BASE HEAD"""
import re
import subprocess
import sys

repo, base, head = sys.argv[1:4]
PAT = re.compile(r"issuecomment|\bround \d+|\[[AR]\d+\]|\bR\d{2,4}-\d|\bB\d{1,2}\b|\bS2b\b", re.I)
diff = subprocess.run(["git", "-C", repo, "diff", "-U0", "--no-color", f"{base}..{head}", "--", ".", ":!*.md"],
                      capture_output=True, text=True, check=True).stdout
path, line = None, 0
hits = []
for raw in diff.splitlines():
    if raw.startswith("+++ "):
        path = raw[6:] if raw.startswith("+++ b/") else None
    elif raw.startswith("@@"):
        line = int(re.search(r"\+(\d+)", raw).group(1))
    elif raw.startswith("+") and path:
        if PAT.search(raw):
            hits.append(f"{path}:{line}: {raw[1:].strip()[:200]}")
        line += 1
print("\n".join(hits))
print(f"{len(hits)} added line(s) in {len({h.split(':')[0] for h in hits})} file(s)")
