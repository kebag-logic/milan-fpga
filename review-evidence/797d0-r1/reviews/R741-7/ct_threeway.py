#!/usr/bin/env python3
"""Three-way check of ci/image/command-table.json across a merge.

Usage: python3 -I ct_threeway.py <repo> <base> <ours> <theirs> <result>
Flattens each table to (json-path -> leaf) plus list-of-rows membership and
verifies that every change from base on either side is present in result and
that result carries nothing neither side introduced.  Exit 0 = keeps both.
"""
import json, subprocess, sys

def load(repo, rev):
    out = subprocess.run(["git", "-C", repo, "show", f"{rev}:ci/image/command-table.json"],
                         check=True, capture_output=True).stdout
    return json.loads(out)

def flat(obj, pre=()):
    """Dict keys are paths; lists of rows become sets of canonical rows."""
    res = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            res.update(flat(v, pre + (k,)))
    elif isinstance(obj, list):
        res[pre] = frozenset(json.dumps(x, sort_keys=True) for x in obj)
        res[pre + ("#len",)] = len(obj)
    else:
        res[pre] = json.dumps(obj)
    return res

def main():
    repo, b, o, t, r = sys.argv[1:6]
    B, O, T, R = (flat(load(repo, x)) for x in (b, o, t, r))
    bad = 0
    keys = set(B) | set(O) | set(T) | set(R)
    changes = {"ours": 0, "theirs": 0}
    for k in sorted(keys, key=str):
        if k and k[-1] == "#len":
            continue
        bv, ov, tv, rv = B.get(k), O.get(k), T.get(k), R.get(k)
        if isinstance(bv or ov or tv or rv, frozenset):
            bs, os_, ts, rs = (x or frozenset() for x in (bv, ov, tv, rv))
            want = (bs | (os_ - bs) | (ts - bs)) - (bs - os_) - (bs - ts)
            if os_ != bs: changes["ours"] += len(os_ ^ bs)
            if ts != bs: changes["theirs"] += len(ts ^ bs)
            if rs != want:
                bad += 1
                print("ROWSET MISMATCH", k, "missing", sorted(want - rs)[:3], "extra", sorted(rs - want)[:3])
        else:
            if ov != bv: changes["ours"] += 1
            if tv != bv: changes["theirs"] += 1
            if ov != bv and tv != bv and ov != tv:
                print("CONFLICT", k, ov, tv, rv); bad += 1; continue
            want = ov if ov != bv else tv
            if rv != want:
                bad += 1
                print("LEAF MISMATCH", k, "want", want, "got", rv)
    print(f"changes from base: ours={changes['ours']} theirs={changes['theirs']}; mismatches={bad}")
    sys.exit(1 if bad else 0)

main()
