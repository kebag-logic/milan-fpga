#!/usr/bin/env python3
"""Compare two tdm8render-mutants campaign logs and the published author records.

Usage: compare_render.py <head-full.log> <prior-full.log> <author-differential.json>
Prints the per-case verdict lines (top-level [PASS]/[FAIL] lines), the summary,
every indented [FAIL] assertion and 'checks:' count line, and compares:
  reviewer head vs reviewer prior; reviewer head vs author adopted; reviewer
  prior vs author prior. Exit 0 only if all case lists and summaries match.
"""
import json, re, sys
def parse(path):
    text = open(path, errors="replace").read()
    cases = [l.rstrip() for l in text.splitlines() if re.match(r"^\[(PASS|FAIL)\] ", l)]
    summ = [l.strip() for l in text.splitlines() if re.search(r"^\s*\d+ checks: \d+ PASS, \d+ FAIL", l)]
    asserts = [l.rstrip() for l in text.splitlines() if re.match(r"^\s+\[FAIL\] ", l)]
    counts = [l.strip() for l in text.splitlines() if "== tdm8_render: checks:" in l]
    return cases, summ, asserts, counts
h, p, a = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
H, P = parse(h), parse(p)
ok = True
def cmp(label, x, y):
    global ok
    same = x == y
    ok &= same
    print(f"{'MATCH' if same else 'DIFFER'} {label} ({len(x)} vs {len(y)})")
    if not same:
        for i, (u, v) in enumerate(zip(x, y)):
            if u != v: print(f"   first difference at {i}:\n     {u}\n     {v}"); break
for name, X in (("head", H), ("prior", P)):
    print(f"== reviewer {name}: {len(X[0])} cases, summary {X[1]}, {X[0].count('') } ")
    for c in X[0]:
        if c.startswith("[FAIL]"): print("   ", c[:200])
cmp("reviewer head vs prior: case verdict lines", H[0], P[0])
cmp("reviewer head vs prior: summary", H[1], P[1])
cmp("reviewer head vs prior: indented [FAIL] assertion lines", H[2], P[2])
cmp("reviewer head vs prior: per-leg checks/failures count lines", H[3], P[3])
rec = a["records"]
for mine, key in ((H, "adopted"), (P, "prior")):
    r = rec.get(key)
    if r is None:
        print(f"no author record {key}; keys {list(rec)}"); ok = False; continue
    cmp(f"reviewer vs author {key}: case verdict lines", mine[0], r["cases"])
    cmp(f"reviewer vs author {key}: summary", mine[1], [r["summary"]])
print("OVERALL", "MATCH" if ok else "DIFFER")
sys.exit(0 if ok else 1)
