#!/usr/bin/env python3
"""Console command census and capture drop logs across both packets.

usage: console_census.py <archive-dir>   (review-evidence/117-r1)
"""
import collections
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
tot, per, cmds = 0, [], collections.Counter()
for f in sorted(root.glob("bench-a20[02]/**/console*.txt")):
    n = 0
    for line in f.read_text(errors="replace").splitlines():
        m = re.match(r"^### \S+ cmd='([^']*)'", line)
        if m:
            n += 1
            cmds[m.group(1).split()[0]] += 1
    if n:
        per.append((str(f.relative_to(root)), n))
        tot += n
for f, n in per:
    print(n, f)
print(f"transcripts with commands: {len(per)}; commands: {tot}; by verb: {dict(cmds)}")
logs = sorted(root.glob("bench-a20[02]/**/tcpdump*.log"))
nz = [str(f.relative_to(root)) for f in logs
      if re.search(r"(\d+) packets dropped by kernel", f.read_text()).group(1) != "0"]
print(f"tcpdump logs: {len(logs)}; with non-zero drops: {nz}")
