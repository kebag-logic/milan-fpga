#!/usr/bin/env python3
"""Check a two-parent merge keeps both sides: every file only one side changed
equals that side; every line either side added against the base is present in
the merge (as a multiset per file).  usage: merge_keeps_both.py <repo> <merge>"""
import collections, subprocess, sys
repo, m = sys.argv[1], sys.argv[2]
g = lambda *a: subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout
p1, p2 = g("rev-parse", m + "^1", m + "^2").split()
base = g("merge-base", p1, p2).strip()
ch = lambda a, b: set(g("diff", "--name-only", a, b).split())
s1, s2 = ch(base, p1), ch(base, p2)
def blob(c, f):
    r = subprocess.run(["git", "-C", repo, "rev-parse", f"{c}:{f}"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None
bad = 0
for side, mine, other, tip in (("ours", s1, s2, p1), ("theirs", s2, s1, p2)):
    for f in sorted(mine - other):
        ok = blob(m, f) == blob(tip, f); bad += not ok
        print(("SAME " if ok else "DIFF ") + side, f)
for f in sorted(s1 & s2):
    for side, tip in (("ours", p1), ("theirs", p2)):
        added = [l[1:] for l in g("diff", "-U0", base, tip, "--", f).splitlines()
                 if l.startswith("+") and not l.startswith("+++")]
        need = collections.Counter(added); got = collections.Counter(g("show", f"{m}:{f}").splitlines())
        lost = [l for l in need if got[l] < need[l]]
        bad += bool(lost)
        print(f"BOTH {side} {f}: {len(added)} added lines, {len(lost)} missing")
        for l in lost[:5]: print("   MISSING:", l[:160])
print(f"merge {m} base {base} p1 {p1} p2 {p2}: {'KEEPS BOTH' if not bad else 'DROPS'}")
sys.exit(1 if bad else 0)
