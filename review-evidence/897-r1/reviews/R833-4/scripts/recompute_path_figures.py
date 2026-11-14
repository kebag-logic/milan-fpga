#!/usr/bin/env python3
"""Recompute section 13's GET_AS_PATH per-word and round figures from the
published harness/scratch receipts. usage: recompute_path_figures.py <scratch dir>
SPAN lines: SPAN <end> <start> <cycles> <call-site pc> <symbol>."""
import os, re, sys

d = sys.argv[1]
def spans(name):
    out = []
    for line in open(os.path.join(d, name), encoding="utf-8"):
        f = line.split()
        if f and f[0] == "SPAN":
            out.append((int(f[3]), f[4]))
    return out

bad = 0
def check(label, got, want):
    global bad
    ok = got == want
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {label}: {got} (doc {want})")

sa = spans("sA1-aecp-mbx_win_read.txt") + spans("sA1-datapath-events-mbx_win_read.txt")
check("arm A unanswered word, least cycles", min(c for c, _ in sa), 378)
check("arm A unanswered word, most cycles", max(c for c, _ in sa), 796)
allmax = 0
for grp, n_count in (("notice-every-0", 22), ("notice-burst-0", 23)):
    s = spans(f"pN1-{grp}-mbx_win_read.txt")
    sites = sorted({pc for _, pc in s})
    count = [c for c, pc in s if pc == sites[0]]
    entry = [c for c, pc in s if pc == sites[1]]
    check(f"{grp} count reads", len(count), n_count)
    check(f"{grp} entry reads", len(entry), 8)
    check(f"{grp} entry cycles", sum(entry), 3032)
    check(f"{grp} entry most", max(entry), 386)
    check(f"{grp} count most", max(count), 877)
    allmax = max(allmax, max(count), max(entry))
check("most a word took, any receipt", max(allmax, max(c for c, _ in sa)), 877)
pr = open(os.path.join(d, "path_round.txt"), encoding="utf-8").read()
rounds = [int(x) for x in re.findall(r"round (\d+) CPU cycles", pr)]
check("rounds (every-0, burst-0)", rounds, [46397, 47490])
adm = [int(x) for x in re.findall(r"admitted at (\d+)", pr)]
check("admitted at (cold 85 + 2 x 255 us, 100 cycles/us)", adm, [(85 + 2 * 255) * 100] * 2)
check("margins positive", all(a > r for a, r in zip(adm, rounds)), True)
refused = re.findall(r"(\d+) refused attempts", pr)
check("answered rounds, refused attempts", refused, ["0", "0"])
summ = open(os.path.join(d, "summary-pN1.txt"), encoding="utf-8").read()
check("pN1 notices all within", all(l.rstrip().endswith("within") for l in summ.splitlines() if l.startswith("NOTICE")), True)
check("pN1 budget misses / passes over share", bool(re.search(r"0 budget misses .* 0 of \d+ work passes over", summ)), True)
sumA = open(os.path.join(d, "summary-sA1.txt"), encoding="utf-8").read()
check("sA1 budget misses / passes over share", bool(re.search(r"0 budget misses .* 0 of \d+ work passes over", sumA)), True)
# GET_AS_PATH record estimate: arm A record + 8 words at 877 + 16 data words at 60 (+64 B copy)
est = 11655 + 8 * 877 + 16 * 60
print(f"INFO record estimate before the 64 B copy: {est} cycles (doc: about 19,950, 200 us; stated 235 us = 23,500)")
check("estimate under stated record.aecp", est < 23500, True)
print(f"bad={bad}")
sys.exit(1 if bad else 0)
