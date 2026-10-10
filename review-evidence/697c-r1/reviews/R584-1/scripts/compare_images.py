#!/usr/bin/env python3
"""Pair head/dev lines of images.sh output (argv[1]); optionally compare against a published table (argv[2])."""
import re, sys
rows = {}
for line in open(sys.argv[1]):
    m = re.match(r"(head|dev) (ctrl_image|ctrl_srp_image) (\S+) rc=(\d+) ([0-9a-f]{64})?", line)
    if m:
        rows.setdefault((m[2], m[3]), {})[m[1]] = m[5]
pub = {}
if len(sys.argv) > 2:
    for line in open(sys.argv[2]):
        m = re.match(r"\| (ctrl_image\.py|ctrl_srp_image\.py) (\S+) \| `([0-9a-f]{64})` \| `([0-9a-f]{64})`", line)
        if m:
            pub[(m[1][:-3], m[2])] = (m[3], m[4])
same = 0
for k in sorted(rows):
    h, d = rows[k].get("head"), rows[k].get("dev")
    ok = h is not None and h == d
    same += ok
    p = pub.get(k)
    pm = "" if not pub else (" published-match" if p and p == (d, h) else " PUBLISHED-MISMATCH")
    print(f"{k[0]} {k[1]}: dev {d} head {h} {'IDENTICAL' if ok else 'DIFFERENT'}{pm}")
print(f"{same} of {len(rows)} identical")
sys.exit(0 if same == len(rows) == 25 else 1)
