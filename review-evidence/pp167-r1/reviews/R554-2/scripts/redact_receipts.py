#!/usr/bin/env python3
"""Replace the host's container tool-root prefix with <TOOLROOT> in receipt text files.
usage: redact_receipts.py DIR"""
import os, re, sys
pat = re.compile(r"/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff")
n = 0
for root, _, files in os.walk(sys.argv[1]):
    for f in files:
        p = os.path.join(root, f)
        try:
            s = open(p, encoding="utf-8").read()
        except UnicodeDecodeError:
            continue
        t = pat.sub("<TOOLROOT>", s)
        if t != s:
            open(p, "w", encoding="utf-8").write(t); n += 1
print("redacted files:", n)
