#!/usr/bin/env python3
"""Cross-check the #451 SoC-board findings page's figures against the public
packet (review-evidence/b4-r1/author at 3247bf45), offline.

usage: claims_crosscheck.py <packet author dir>
Prints one line per claim: CHECK <name> <OK|MISMATCH> <observed>.
"""
import json
import os
import sys


def main():
    a = sys.argv[1]
    j = lambda p: json.load(open(os.path.join(a, p)))
    d = j("runs/timing-long/decode.json")
    s = j("summary/summary.json")
    at = j("runs/timing-long/attribution-summary.json")
    ev = [json.loads(l) for l in open(os.path.join(a, "runs/timing-long/events.jsonl"))]
    res = []

    def chk(name, cond, obs):
        res.append(cond)
        print("CHECK", name, "OK" if cond else "MISMATCH", obs)

    chk("frames 22,831,104 = bytes/32", d["frames"] == 22831104 == d["bytes"] // 32, d["frames"])
    chk("raw sha256", d["sha256"] == "dd201b3a926317a9f488b8290123fa235da7733dae06301f2cd21688da2d36cb", d["sha256"][:16])
    chk("torn 0, silent 0", d["torn_frames"] == 0 and d["silent_frames"] == 0, (d["torn_frames"], d["silent_frames"]))
    pc = d["per_channel"]
    chk("channel c carries only tag c+1, all frames",
        all(c["tags"] == {str(i + 1): d["frames"]} for i, c in enumerate(pc)), [list(c["tags"]) for c in pc])
    chk("0 invalid, 0 zero words", all(c["non_pattern_words"] == 0 and c["zero_words"] == 0 for c in pc), "")
    st = d["ordinal_steps"]
    chk("steps sum = frames-1", sum(st.values()) == d["frames"] - 1, sum(st.values()))
    chk("steps table", st == {"+1": 22768722, "0 (repeat)": 51873, "+2 (one skipped)": 4954, "forward>2": 5554}
        and "backward" not in st, st)
    chk("clusters 1,221", d["clusters"] == 1221 == at["summary"]["clusters"], d["clusters"])
    sm = at["summary"]
    chk("189 beat / 16 sender / 1,016 unmatched", (sm["beat"], sm["sender"], sm["unexplained"]) == (189, 16, 1016), "")
    chk("beat 3,678 repeats / 3,867 skips", (sm["beat_repeats"], sm["beat_skips"]) == (3678, 3867), "")
    top = sum(n for k, n in at["unexplained_other_jumps_top"] if k[:2] == [5, 5] and len(k) == 3 and 8 <= k[2] <= 12)
    chk("816 jump 5,5,8..12", top == 816, top)
    h = at["unexplained_spacing_frames_hist_2000"]
    chk("838 spaced 22,000-26,000", h["22000"] + h["24000"] == 838, h["22000"] + h["24000"])
    st2 = s["session_2"]["run"]["slip_tdm"]
    rate = (st2["after_capture"] - st2["before"]) / st2["seconds_between_reads"]
    chk("SLIP_TDM 395 in 774.3 s, 10.63 ppm", st2["after_capture"] - st2["before"] == 395
        and round(st2["seconds_between_reads"], 1) == 774.3 and round(rate / 48000 * 1e6, 2) == 10.63,
        (round(rate, 4), round(rate / 48000 * 1e6, 2)))
    up = [e for e in ev if e.get("kind") == "upload"][0]
    chk("upload bytes/hash, no gap >=100 ms", up["bytes"] == 730595328 and up["gaps_ge_100ms"] == 0
        and up["sha256"] == d["sha256"], (up["max_gap_s"], up["gaps_ge_100ms"]))
    late = None
    for line in open(os.path.join(a, "runs/timing-long/controller-logs.txt"), encoding="latin-1"):
        if line.startswith('{"kind":"end"'):
            late = json.loads(line)
        if line.startswith('{"kind":"late-pdus"'):
            lp = json.loads(line)
    chk("8,330 PDUs >= 1 ms, max 31.8 ms", sum(late["late_hist"][5:]) == 8330 and round(late["max_late_ns"] / 1e6, 1) == 31.8,
        (sum(late["late_hist"][5:]), late["max_late_ns"]))
    chk("late-PDU list 5,000 entries, threshold 150 us", len(lp["entries"]) == 5000 and lp["threshold_ns"] == 150000, "")
    print("SUMMARY", sum(res), "of", len(res), "OK")


if __name__ == "__main__":
    main()
