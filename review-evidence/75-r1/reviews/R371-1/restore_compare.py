#!/usr/bin/env python3
"""Independent restore comparison of the published census files.

Usage: restore_compare.py <census-start.jsonl> <census-end.jsonl>
Checks, without the author's slicing, that the key sets match, that every
stream state was unbound at start and at end, and reports every byte that
differs between start and end settings/descriptors, including the bytes the
author's comparator excludes (clock bytes after 6, descriptor bytes 0..3).
Exits 1 on any state or unexcluded setting difference.
"""
import json
import sys


def load(path):
    return {(r["role"], r["what"]): r for r in map(json.loads, open(path, encoding="utf-8"))}


a, b = load(sys.argv[1]), load(sys.argv[2])
bad = 0
print(f"keys start {len(a)} end {len(b)}; only-start {sorted(set(a) - set(b))}; only-end {sorted(set(b) - set(a))}")
if set(a) != set(b):
    bad += 1
states = sorted(k for k in a if k[1].startswith("state-"))
print(f"stream states: {len(states)}")
for k in states:
    s, e = a[k]["response"], b[k]["response"]
    ok = s.get("status") == 0 and e.get("status") == 0 and s.get("conn_count") == 0 and e.get("conn_count") == 0
    same = {f: (s.get(f), e.get(f)) for f in ("stream_id", "talker", "talker_uid", "dmac", "flags", "vlan") if s.get(f) != e.get(f)}
    if not ok or same:
        print(f"  STATE {k}: start conn {s.get('conn_count')} end conn {e.get('conn_count')} diffs {same}")
        bad += 1
print(f"  all {len(states)} states unbound at start and at end, identical fields: {bad == 0}")
for k in sorted(a):
    if k[1] in ("clock", "config", "sample-rate") or k[1].startswith("desc-"):
        s, e = a[k]["response"], b[k]["response"]
        x, y = bytes.fromhex(s.get("payload", "")), bytes.fromhex(e.get("payload", ""))
        if s.get("status") != "SUCCESS" or e.get("status") != "SUCCESS" or len(x) != len(y):
            print(f"  SETTING {k}: status {s.get('status')}/{e.get('status')} len {len(x)}/{len(y)}"); bad += 1
            continue
        diff = [i for i in range(len(x)) if x[i] != y[i]]
        if diff:
            excluded = [i for i in diff if (k[1] == "clock" and i >= 6) or (k[1].startswith("desc-") and i < 4)]
            other = [i for i in diff if i not in excluded]
            print(f"  {k}: differing byte offsets {diff} (author-excluded {excluded}; other {other})")
            if other:
                bad += 1
print("RESULT", "PASS" if bad == 0 else f"{bad} problem(s)")
sys.exit(1 if bad else 0)
