#!/usr/bin/env python3
"""Scan files and a commit range for private bench names, by label only.

usage: b5_token_scan.py <redaction_map.json> <extra_patterns.json> <repo> <base> <head> <path>...

The redaction map (private, not published) holds literal values and regular
expressions, each with a public label. Every file under the given paths, every
line the range base..head adds, and the range's commit messages are searched for
each of them, case-insensitively, plus MAC addresses and home directories, and the
labelled patterns of a second private list (capture channel numbers, clock-topology
words, agent tool and model names), kept out of this file for the same reason. A hit
prints the label, the place and the line number, never the matched text, so this
output can be published.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

MAP, EXTRA, REPO, BASE, HEAD = sys.argv[1:6]
PATHS = [Path(p) for p in sys.argv[6:]]
m = json.load(open(MAP))
pats = [(lab, re.compile(re.escape(v), re.I)) for v, lab in m["literal"]]
pats += [(lab, re.compile(v, re.I)) for v, lab in m["regex"]]
GENERIC = [
    ('generic MAC address', '\\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\\b'),
    ('home directory', '/hom[e]/|/User[s]/|~[/]'),   # bracketed so this line does not match itself
]
GENERIC += [tuple(x) for x in json.load(open(EXTRA))]
pats += [(lab, re.compile(rx, re.I)) for lab, rx in GENERIC]


def scan(name, lines, hits):
    for n, line in enumerate(lines, 1):
        for lab, rx in pats:
            if rx.search(line):
                hits.append(f"{lab}: {name}:{n}")


hits, scanned = [], []
for root in PATHS:
    for f in sorted([root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]):
        scanned.append(str(f))
        scan(f.name if root.is_file() else str(f.relative_to(root.parent)),
             f.read_bytes().decode("latin-1").split("\n"), hits)
diff = subprocess.run(["git", "-C", REPO, "diff", "-U0", f"{BASE}..{HEAD}"], capture_output=True, check=True).stdout.decode()
added = [l[1:] for l in diff.split("\n") if l.startswith("+") and not l.startswith("+++")]
scan(f"diff {BASE[:8]}..{HEAD[:8]} (added lines)", added, hits)
msgs = subprocess.run(["git", "-C", REPO, "log", "--format=%B", f"{BASE}..{HEAD}"], capture_output=True,
                      check=True).stdout.decode().split("\n")
scan(f"commit messages {BASE[:8]}..{HEAD[:8]}", msgs, hits)
print(f"patterns: {len(m['literal'])} literal and {len(m['regex'])} regular-expression entries from the private "
      f"redaction map; {len(GENERIC)} labelled patterns: {sorted(set(lab for lab, _ in GENERIC))}")
print(f"scanned: {len(scanned)} files, {len(added)} added diff lines, {len(msgs)} commit-message lines")
print(f"hits: {len(hits)}")
for h in hits:
    print("  " + h)
