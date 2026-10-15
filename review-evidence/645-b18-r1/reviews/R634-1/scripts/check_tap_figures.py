#!/usr/bin/env python3
"""Check the B18 page's tap-derived cells against the graded per-cycle summaries, and the B17 columns
of the comparison table against B17's own published page section and summaries.

usage: python3 -I check_tap_figures.py <page.md> <b18_author_dir> <b17_author_r2_dir>
"""
import json, re, sys, decimal
from pathlib import Path

D = decimal.Decimal


def rnd(x, q):
    return str(D(repr(x)).quantize(D(q), rounding=decimal.ROUND_HALF_EVEN))


page = open(sys.argv[1]).read()
b18 = Path(sys.argv[2])
b17 = Path(sys.argv[3])
cj = json.load(open(b18 / "summary/cycles.json"))
sec = page[page.index("## Dev 9ef71772, 2026-10-15: lane B18"):]
b17sec = page[page.index("## Dev 5603c353, 2026-10-15: lane B17"):page.index("## Dev 9ef71772")]
fails = 0
rows = {}
for l in sec.splitlines():
    m = re.match(r"\| (c\d\d) \| (\d\d:\d\d:\d\d\.\d{3}) \| 80, (\S+) to (\S+) \|", l)
    if m:
        rows.setdefault(m.group(1), {})["binds"] = [c.strip() for c in l.strip("|").split("|")]
    m = re.match(r"\| (c\d\d) \| (\d\d:\d\d:\d\d\.\d{3}) \| [\d.]+ \| [\d.]+ to", l)
    if m:
        rows.setdefault(m.group(1), {})["cmp"] = [c.strip() for c in l.strip("|").split("|")]
gaps = []
for c in cj["cycles"]:
    r = rows[c["cycle"]]["binds"]
    fb = c["first_burst"]
    exp = {
        "first_pdu": f"{c['first_pdu_ms']:.3f}",
        "first_burst": f"{rnd(fb['s'], '0.01')}, {rnd(fb['peak_us'], '0.1')} us",
        "bursts": f"{c['bursts_to_last_poll']}, {rnd(c['peak_to_last_poll_us'], '0.1')} us",
        "dppm": (("+" if c["delta_ppm"] > 0 else "") + f"{c['delta_ppm']:.4f}"),
    }
    got = {"first_pdu": r[6], "first_burst": r[7], "bursts": r[8], "dppm": r[10]}
    for k in exp:
        ok = exp[k] == got[k]
        fails += not ok
        if not ok:
            print("MISMATCH", c["cycle"], k, "page", got[k], "summary", exp[k])
    # bursts and arming window
    gap_ms = fb["s"] * 1000 - c["arm_fires_ms_design"]
    gaps.append(gap_ms)
    pre = c["over_10us_before_arm"]
    same = c["first_over_10us"]["s"] == fb["s"]
    print(c["cycle"], "grade", c["grade"], "first_burst_s", fb["s"], "peak", fb["peak_us"], "pdus", fb["pdus"],
          "fire_ms", round(c["arm_fires_ms_design"], 3), "burst_after_fire_ms", round(gap_ms, 3),
          "over10_before_arm", pre, "first_over10_is_first_burst", same,
          "to_capture", c["bursts_to_capture"], round(c["peak_to_capture_us"], 3),
          "p999", c["lateness_p999_us"], "peer_ppm", c["peer_rate_ppm"], "seq_gaps", c["pdus_seq_gaps"],
          "slip_grades", c["slip_grades"])
print("burst after design firing, ms: min", round(min(gaps), 3), "max", round(max(gaps), 3))
# B17 columns of the comparison table against B17's own section
b17rows = {}
for l in b17sec.splitlines():
    m = re.match(r"\| (c\d\d) \| (\d\d:\d\d:\d\d\.\d{3}) \| Undefined", l)
    if m:
        cells = [x.strip() for x in l.strip("|").split("|")]
        b17rows[m.group(1)] = cells
for cyc, r in sorted(rows.items()):
    cm = r["cmp"]
    b = b17rows[cyc]
    slip17 = b[5].split(", 0 skips")[0]
    ok = (cm[1] == b[1]) and (cm[3] == slip17)
    print("CMP", cyc, "b17 bind", cm[1], b[1], "| slip", cm[3], "vs", slip17, "|", "OK" if ok else "MISMATCH")
    fails += not ok
    b18c = next(c for c in cj["cycles"] if c["cycle"] == cyc)
    ok2 = cm[5] == f"{b18c['first_pdu_ms']:.3f}" and cm[6] == "None" and cm[7] == rows[cyc]["binds"][7]
    fails += not ok2
    if not ok2:
        print("MISMATCH b18 columns", cyc, cm[5:])
# B17 first-PDU and first burst against B17's packet summaries (round 2 summaries hold cNN.json)
for cyc in sorted(rows):
    cm = rows[cyc]["cmp"]
    p = b17 / "summary" / f"{cyc}.json"
    if p.exists():
        s = json.load(open(p))
        txt = json.dumps(s)
        print("B17SUM", cyc, "page first PDU", cm[2], "in summary", cm[2] in txt, "| page burst", cm[4])
print("FAILS", fails)
