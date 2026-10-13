"""Scratch: compare two recorded configuration sets by (side argv head, unit, label)."""
import json, sys, collections
def load(p):
    recs = json.load(open(p))["records"]
    out = {}
    for r in recs:
        side = " ".join(r["argv"][:2])
        import re
        label = re.sub(r"(-D[A-Za-z_]\w*)=1(?=\s|$)", r"\1", r["label"])
        key = (side, r["unit"], label)
        out[key] = (tuple(r["deps"]), tuple(r["tested"]), r["error"], r["stopped"])
    return recs, out
ra, a = load(sys.argv[1]); rb, b = load(sys.argv[2])
print("configurations", len(ra), len(rb), "distinct keys", len(a), len(b))
only_a = sorted(set(a) - set(b)); only_b = sorted(set(b) - set(a))
print("only in first:", len(only_a)); [print("  ", k) for k in only_a[:20]]
print("only in second:", len(only_b)); [print("  ", k) for k in only_b[:20]]
diff = [k for k in set(a) & set(b) if a[k] != b[k]]
print("differ (deps/tested/error):", len(diff))
for k in diff[:10]:
    print("  ", k)
    da, db = a[k], b[k]
    print("     deps -", sorted(set(da[0]) - set(db[0]))[:5], "+", sorted(set(db[0]) - set(da[0]))[:5])
    print("     tested -", sorted(set(da[1]) - set(db[1]))[:8], "+", sorted(set(db[1]) - set(da[1]))[:8])
