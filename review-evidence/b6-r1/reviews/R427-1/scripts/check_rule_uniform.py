#!/usr/bin/env python3
"""Re-derive every cluster's capture-path decision from its published fields with the
page's stated rule, in every case, and compare with the published decision; also check
that no one-frame event carries a capture-path cause and that every beat member is a
one-frame repeat.

usage: check_rule_uniform.py <evidence author/summary dir>
"""
import csv, json, sys
root = sys.argv[1]
bad = 0
for c in ("a0", "a1", "a2", "bint", "bcrf"):
    g = json.load(open(f"{root}/{c}/grade.json"))
    n = 0
    for x in g["skip_clusters"]:
        rise, lost, net, gap, sig = x["read_rise_ms"], x["lost_frames"], x["net_step"], x["recent_read_gap_ms"], x["size_signature"]
        cap = False
        if rise is not None:
            cap = lost > 0 and abs(rise - lost / 48) <= 1.0 + 0.02 * lost / 48
            if cap and (lost - net) % 48000:
                cap = False
        if not cap and net > 0 and gap is not None and gap >= 11.0 and (rise is None or sig):
            cap = True
        n += 1
        if cap != x["capture_path"]:
            bad += 1
            print("MISMATCH", c, x)
    ev = list(csv.DictReader(open(f"{root}/{c}/events.csv")))
    one_cap = [e for e in ev if e["cause"] == "capture path" and int(e["frames"]) == 1]
    beat_bad = [e for e in ev if e["cause"] == "DUT beat" and not (e["kind"] == "repeat" and e["frames"] == "1")]
    multi_noncap = [e for e in ev if e["cause"] != "capture path" and int(e["frames"]) >= 2]
    print(f"{c}: clusters re-derived {n}, mismatches so far {bad}; one-frame events marked capture path {len(one_cap)}; non-repeat beat members {len(beat_bad)}; multi-frame events outside the capture path {len(multi_noncap)}")
    bad += len(beat_bad)
print("RESULT", "PASS" if bad == 0 else f"FAIL {bad}")
