#!/usr/bin/env python3
"""Scan added lines of a unified diff for comment-rule residue patterns.
usage: residue_scan.py <diff>   prints path:newline: text for each hit."""
import re, sys
pat = re.compile(r'issue ?comment|issuecomment|\b\d{10}\b|\[[ABR]\d+[a-z]?\]|\b[ABR]\d{2,4}[a-z]?\b|\bround [0-9]\b|\bB\d{1,3}\b|\blane [A-Z]\d|\bS\d{1,2}[ab]?\b', re.I)
path = None; ln = 0
for line in open(sys.argv[1], encoding='utf-8', errors='replace'):
    if line.startswith('+++ '):
        path = line[6:].strip(); continue
    m = re.match(r'@@ -\d+(?:,\d+)? \+(\d+)', line)
    if m: ln = int(m.group(1)); continue
    if line.startswith('+'):
        if pat.search(line): print(f"{path}:{ln}: {line[1:].rstrip()[:200]}")
        ln += 1
    elif line.startswith(' '): ln += 1
