"""Scan the added lines of a diff's non-markdown files for workflow labels in source text: issue-comment IDs,
lane labels (S<n>), review rounds, agent/reviewer IDs (A<n>/R<n>), bench lane labels (B<n>), the word lane.
usage: git diff -U0 BASE..HEAD -- . ':!*.md' > d.diff; python3 -I residue_scan.py d.diff"""
import re, sys
pat = re.compile(r'issuecomment|\bS\d+[a-z]?\b|\bround \d+|\b[AR]\d{2,4}[a-z]?\b|\bB\d{1,3}\b|lane', re.I)
f, ln, hits = None, 0, 0
for line in open(sys.argv[1], encoding='utf-8', errors='replace'):
    if line.startswith('+++ '): f = line[6:].strip(); continue
    m = re.match(r'@@ -\S+ \+(\d+)', line)
    if m: ln = int(m.group(1)); continue
    if line.startswith('+'):
        if pat.search(line): hits += 1; print(f"{f}:{ln}: {line[1:].rstrip()[:200]}")
        ln += 1
print(f"{hits} hit(s)")
