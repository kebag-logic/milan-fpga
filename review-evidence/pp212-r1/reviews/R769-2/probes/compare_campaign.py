#!/usr/bin/env python3
"""compare_campaign.py <own.log> <author camp-srp.log>: per-label verdict and
failure-count comparison of an --only run against the author's full run."""
import re, sys
def read(p):
    d = {}
    for l in open(p):
        m = re.match(r'^([a-z0-9-]+): rc=(\d+) failures=(\d+) (\w+) tags=(\S*)', l)
        if m:
            d.setdefault(m.group(1), []).append((int(m.group(3)), m.group(4), m.group(5)))
    return d
own, auth = read(sys.argv[1]), read(sys.argv[2])
same = 0
for k in sorted(own):
    eq = own[k] == auth.get(k)
    same += eq
    print(f"{k}\town={own[k]}\tauthor={auth.get(k)}\t{'SAME' if eq else 'DIFF'}")
print(f"labels {len(own)}, entries {sum(map(len, own.values()))}, same as author {same}")
