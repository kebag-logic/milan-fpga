#!/usr/bin/env python3
"""Plant one defect in a copy of align_b16.py and report which published controls catch it.

usage: mutate_align.py <src align_b16.py> <dst dir> <mutant id: M1 low-byte key and compare | M2 slips ignored>
"""
import shutil, sys, os
src, dst, mid = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(dst, exist_ok=True)
for f in os.listdir(os.path.dirname(src)):
    if f.endswith(".py"):
        shutil.copy(os.path.join(os.path.dirname(src), f), dst)
p = os.path.join(dst, "align_b16.py")
t = open(p).read()
if mid == "M1":
    # lane B15's weakness: key and per-frame equality on each sample's low byte only
    t = t.replace("k = k * np.uint64(31) + (a[:, c] + (1 << 23)).astype(np.uint64) * P[c % len(P)]",
                  "k = k * np.uint64(31) + (a[:, c] & 0xff).astype(np.uint64) * P[c % len(P)]")
    t = t.replace("np.array_equal(s[p:p + len(win)], m_win)", "np.array_equal(s[p:p + len(win)] & 0xff, m_win & 0xff)")
    old = "if ks[j] == km[i] and np.array_equal(s[j], m[i]):"
    new = "if ks[j] == km[i] and np.array_equal(s[j] & 0xff, m[i] & 0xff):"
elif mid == "M2":
    old = 'verdict="SAMPLE-EXACT" if diffs == 0 and not slips else "DIFFERENT")'
    new = 'verdict="SAMPLE-EXACT" if diffs == 0 else "DIFFERENT")'
assert t.count(old) == 1, "anchor not unique"
open(p, "w").write(t.replace(old, new))
print("planted", mid)
