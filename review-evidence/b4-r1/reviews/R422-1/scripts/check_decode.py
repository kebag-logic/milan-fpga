#!/usr/bin/env python3
"""Cross-check the packet's decode and attribution records against the page.

usage: check_decode.py <decode.json> <attribution-summary.json>
"""
import json
import sys

d = json.load(open(sys.argv[1]))
A = json.load(open(sys.argv[2]))
a = A["summary"]
F = d["frames"]
chk = {}
chk["bytes_eq_frames_x32"] = d["bytes"] == F * 32 == 730595328
chk["frames"] = F
chk["nominal_seconds"] = d["nominal_seconds"]
chk["sha256_is_page_raw"] = d["sha256"] == "dd201b3a926317a9f488b8290123fa235da7733dae06301f2cd21688da2d36cb"
chk["torn"] = d["torn_frames"]
chk["silent"] = d["silent_frames"]
chk["per_channel_ok"] = all(
    pc["tags"] == {str(pc["soc_channel"] + 1): F} and pc["zero_words"] == 0 and pc["non_pattern_words"] == 0
    for pc in d["per_channel"])
st = d["ordinal_steps"]
chk["ordinal_steps"] = st
chk["steps_sum_eq_frames_minus_1"] = sum(st.values()) == F - 1
chk["backward"] = st.get("backward", 0)
chk["clusters"] = d["clusters"]
cd = d["cluster_detail"]
chk["cluster_repeats_total"] = sum(c["repeats"] for c in cd)
chk["cluster_skips_total"] = sum(c["skips"] for c in cd)
chk["cluster_other_total"] = sum(len(c["other"]) for c in cd)
chk["jump_sizes"] = d["jump_sizes"]
chk["attribution"] = {k: a.get(k) for k in ("clusters", "beat", "sender", "unexplained", "beat_repeats", "beat_skips", "late_pdus_logged")}
chk["attribution_partition_ok"] = a["beat"] + a["sender"] + a["unexplained"] == a["clusters"] == d["clusters"]
gaps = d["cluster_start_gaps_frames"]
chk["cluster_gaps_22000_26000"] = sum(1 for g in gaps if 22000 <= g <= 26000)
h = A["unexplained_spacing_frames_hist_2000"]
chk["unexplained_spacing_22000_26000"] = h.get("22000", 0) + h.get("24000", 0)
chk["unexplained_5_5_8to12"] = sum(c for j, c in A["unexplained_other_jumps_top"] if j[:2] == [5, 5] and len(j) == 3 and 8 <= j[2] <= 12)
print(json.dumps(chk, indent=1))
