#!/usr/bin/env python3
"""Compare the raw re-decode of item 3 (ta_lv_recheck.py output) with item3/cycles.tsv.

Per cycle: the bridge's Listener Lv after the DISCONNECT_RX_RESPONSE from the raw
re-decode against cycles.tsv lv_after_disconnect_s, and the presence of a DUT
Talker Advertise Lv in the capture against cycles.tsv dut_ta_lv_in_hold.
Exits 1 if any cycle is missing from either side, differs by 0.5 us or more,
or disagrees on the Talker Advertise Lv.

usage: ta_lv_vs_cycles.py <ta_lv_all.txt> <packet-author-dir>
"""
import csv
import re
import sys

TA, A = sys.argv[1], sys.argv[2]

dec = {}
cur = None
for line in open(TA):
    m = re.search(r"cycle-(\d{3})/tap\.pcap$", line.rstrip())
    if m and not line.startswith(" "):
        cur = dec.setdefault(int(m.group(1)), {"ta": None})
        continue
    m = re.search(r"bridge Listener Lv after the response\s+([0-9.]+) s", line)
    if m:
        cur["bridge"] = float(m.group(1))
    m = re.search(r"DUT Talker Advertise Lv after bridge Lv\s+([0-9.]+) s", line)
    if m:
        cur["ta"] = float(m.group(1))
    m = re.search(r"DUT Talker Advertise Lv after the response\s+([0-9.]+) s", line)
    if m:
        cur["ta_resp"] = float(m.group(1))

tsv = {}
for row in csv.DictReader(open(f"{A}/item3/cycles.tsv"), delimiter="\t"):
    tsv[int(row["cycle"].split("-")[1])] = row

bad = 0
worst = 0.0
print("cycle  decoder_bridge_lv_s  cycles_tsv_lv_s  diff_us  decoder_ta_lv  cycles_tsv_ta_lv")
for c in sorted(set(dec) | set(tsv)):
    if c not in dec or c not in tsv or "bridge" not in dec[c]:
        print(f"{c:03d}    MISSING decoder={c in dec} tsv={c in tsv}")
        bad += 1
        continue
    d, t = dec[c], tsv[c]
    ref = float(t["lv_after_disconnect_s"])
    diff = (d["bridge"] - ref) * 1e6
    worst = max(worst, abs(diff))
    ta = d["ta"] is not None
    ta_ref = t["dut_ta_lv_in_hold"] == "1"
    ok = abs(diff) < 0.5 and ta == ta_ref
    bad += not ok
    print(f"{c:03d}    {d['bridge']:.6f}             {ref:.9f}      {diff:+.3f}   {'yes' if ta else 'no ':3s}            "
          f"{t['dut_ta_lv_in_hold']}{'' if ok else '   MISMATCH'}")
print(f"cycles compared {len(dec)} decoder, {len(tsv)} cycles.tsv")
print(f"largest |diff| {worst:.3f} us; cycles within 0.5 us: {sum(1 for c in dec if c in tsv and abs((dec[c]['bridge'] - float(tsv[c]['lv_after_disconnect_s'])) * 1e6) < 0.5)}")
for c in sorted(c for c in dec if dec[c]["ta"] is not None):
    print(f"DUT Talker Advertise Lv in cycle {c:03d}: {dec[c]['ta']:.4f} s after the bridge's Lv, "
          f"{dec[c]['ta_resp']:.4f} s after the response")
print(f"mismatches {bad}")
sys.exit(1 if bad else 0)
