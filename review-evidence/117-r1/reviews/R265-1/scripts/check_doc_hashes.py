#!/usr/bin/env python3
"""Map every SHA-256 (full or 8-hex-prefix with '...') cited in the findings
page to the public evidence manifest (original_sha256 of the packet file).

Usage: check_doc_hashes.py <findings.md> <review-evidence/117-r1 dir>
Prints each cited hash, the table row label it sits on, and the matching
packet file(s) or NO-MATCH.
"""
import json, os, re, sys

doc, root = sys.argv[1], sys.argv[2]
man = json.load(open(os.path.join(root, "MANIFEST.json")))
full = re.compile(r"`([0-9a-f]{64})`")
pref = re.compile(r"`([0-9a-f]{8})\.\.\.`")
for ln, line in enumerate(open(doc), 1):
    for rx, kind in ((full, "full"), (pref, "prefix")):
        for m in rx.finditer(line):
            h = m.group(1)
            hits = sorted({e["file"] for e in man
                           if e["original_sha256"].startswith(h)
                           or e["published_sha256"].startswith(h)})
            label = line.strip()[:90]
            print(f"L{ln} {kind} {h[:16]} -> {', '.join(hits) if hits else 'NO-MATCH'} | {label}")
