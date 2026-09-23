#!/usr/bin/env python3
"""Count console commands by verb in every transcript carrying '### <ts> cmd=' headers.

Usage: console_command_census.py ARCHIVE_ROOT
Also counts echoed command lines after each header, so a command sent outside
the header wrapper would show as a mismatch.
"""
import collections, os, re, sys

root = sys.argv[1]
hdr = re.compile(r"^### \S+ cmd='([^']*)'")
tot = collections.Counter()
files = []
for dp, dn, fn in os.walk(root):
    dn.sort()
    for f in sorted(fn):
        p = os.path.join(dp, f)
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if "### " not in t or " cmd='" not in t:
            continue
        c = collections.Counter()
        for ln in t.splitlines():
            m = hdr.match(ln)
            if m:
                c[m.group(1).split()[0] if m.group(1).split() else "(empty)"] += 1
        if c:
            files.append(os.path.relpath(p, root))
            tot.update(c)
            print(f"FILE {os.path.relpath(p, root)} {dict(c)} total={sum(c.values())}")
print(f"TRANSCRIPTS {len(files)} VERBS {dict(sorted(tot.items()))} TOTAL {sum(tot.values())}")
