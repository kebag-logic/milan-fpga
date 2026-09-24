#!/usr/bin/env python3
"""Console command census and tcpdump drop logs over a pinned 117-r1 tree.

Usage: console_tcpdump_census.py <117-r1-root>
Counts every console command record (`### <utc> cmd='...'`) per transcript,
the command verbs, every RST_EPOCH (0x90000720) value read, and the
"packets dropped by kernel" line of every tcpdump log.
"""
import collections
import os
import re
import sys

root = sys.argv[1]
files, cmds = [], collections.Counter()
for d, _, fs in sorted(os.walk(root)):
    for f in sorted(fs):
        p = os.path.join(d, f)
        if f.endswith(".py"):
            continue
        try:
            txt = open(p, errors="replace").read()
        except OSError:
            continue
        n = re.findall(r"^### \S+Z cmd='([^']*)'", txt, re.M)
        if n:
            files.append((os.path.relpath(p, root), len(n), txt))
            for c in n:
                cmds[c.split()[0]] += 1
print("transcripts with console command records:", len(files))
for p, n, _ in files:
    print(f"  {p} {n}")
print("total commands:", sum(n for _, n, _ in files))
print("command verbs:", dict(cmds))
vals = collections.Counter()
for _, _, txt in files:
    for m in re.finditer(r"mem_read 0x90000720 4\nMemory dump:\n0x90000720  (\S\S) (\S\S) (\S\S) (\S\S)", txt):
        vals["".join(reversed(m.groups()))] += 1
print("RST_EPOCH values read:", dict(vals))
logs = []
for d, _, fs in sorted(os.walk(root)):
    for f in sorted(fs):
        if f.startswith("tcpdump") and f.endswith(".log"):
            t = open(os.path.join(d, f)).read()
            m = re.search(r"(\d+) packets? dropped by kernel", t)
            logs.append((os.path.relpath(os.path.join(d, f), root), m.group(1) if m else "NO-DROP-LINE"))
print("tcpdump logs:", len(logs))
for p, v in logs:
    print(f"  {p} dropped={v}")
