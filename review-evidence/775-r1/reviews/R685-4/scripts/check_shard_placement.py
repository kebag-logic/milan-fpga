#!/usr/bin/env python3
"""Check that every --ci-pieces case is placed on exactly one of the shards.

usage: check_shard_placement.py SHARD_LISTS_LOG SUITE_INVENTORY_LOG
SHARD_LISTS_LOG holds '## shard i/N' headers, case names and 'rc=0' lines, one
block per `run_all_suites.sh --ci-pieces --shard i/N --list`; the inventory is
`run_all_suites.sh --list`. A piece 'suite__k' maps back to 'suite'.
"""
import collections, re, sys
c = collections.Counter(); shards = 0
for l in open(sys.argv[1]):
    l = l.strip()
    if not l: continue
    if l.startswith('## '): shards += 1; continue
    if l.startswith('rc='):
        assert l == 'rc=0', l; continue
    c[l] += 1
inv = [l.strip() for l in open(sys.argv[2]) if l.strip()]
base = set(re.sub(r'__\d+$', '', p) for p in c)
multi = [k for k, v in c.items() if v != 1]
print("shards", shards, "cases", len(c), "total placements", sum(c.values()))
print("multiply placed:", multi)
print("inventory", len(inv), "pieces' suites", len(base))
print("inventory not placed:", sorted(set(inv) - base))
print("placed not in inventory:", sorted(base - set(inv)))
sys.exit(1 if multi or set(inv) != base else 0)
