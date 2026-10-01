#!/usr/bin/env python3
"""Independent recount of every case figure on the page from the published
summary/<case>/{grade.json,events.csv,blocks.csv}, and an audit of the attribution.

usage: recheck_cases.py <evidence author dir>
"""
import csv, json, sys, collections, os
root = sys.argv[1]
FS = 48000
for case in ("a0", "a1", "a2", "bint", "bcrf"):
    d = os.path.join(root, "summary", case)
    g = json.load(open(os.path.join(d, "grade.json")))
    ev = list(csv.DictReader(open(os.path.join(d, "events.csv"))))
    bl = list(csv.DictReader(open(os.path.join(d, "blocks.csv"))))
    print(f"===== {case} ({g['case']})")
    c = collections.Counter((e["cause"], e["kind"]) for e in ev)
    print(" causes:", dict(c))
    lst = [e for e in ev if e["cause"] == "listener"]
    print(" listener drops", sum(1 for e in lst if e["kind"] == "skip"), "frames", sum(int(e["frames"]) for e in lst if e["kind"] == "skip"),
          "repeats", sum(1 for e in lst if e["kind"] == "repeat"), "inserts", sum(1 for e in lst if e["kind"] == "insert"),
          "listener sizes", collections.Counter((e["kind"], e["frames"]) for e in lst))
    beat = [e for e in ev if e["cause"] == "DUT beat"]
    print(" beat repeats", len(beat), "all 1-frame repeats:", all(e["kind"] == "repeat" and e["frames"] == "1" for e in beat))
    cap = [e for e in ev if e["cause"] == "capture path"]
    cl = [x for x in g["skip_clusters"] if x["capture_path"]]
    noncap_cl = [x for x in g["skip_clusters"] if not x["capture_path"]]
    print(" capture events", len(cap), "clusters", len(cl), "lost", sum(x["lost_frames"] for x in cl),
          "| grade attribution lost", g["attribution"].get("capture path", {}).get("lost_frames"))
    print(" multi-frame clusters NOT capture path:", [(x["first_frame"], x["steps"], x["read_rise_ms"], x["recent_read_gap_ms"]) for x in noncap_cl])
    bases = collections.Counter(x["basis"] for x in cl)
    print(" capture-cluster bases:", dict(bases))
    # non-discriminating rise test: |lost| <= ~1 ms so a zero rise would also pass
    weak = [x for x in cl if x["basis"] == "read-time rise" and abs(x["read_rise_ms"]) <= 1.0 + 0.02 * x["lost_ms"] and x["lost_ms"] <= 1.0 + 0.02 * x["lost_ms"] + 0]
    small = [x for x in cl if x["lost_frames"] <= 49]
    print(" clusters lost <= 49 frames (rise test cannot exclude a zero rise):", [(x["first_frame"], x["steps"], x["read_rise_ms"], x["recent_read_gap_ms"], x["basis"]) for x in small])
    # rise residual for rise-basis clusters
    res = [(x["read_rise_ms"] - x["lost_ms"]) for x in cl if x["basis"] == "read-time rise"]
    if res:
        print(" rise-basis residual ms: n", len(res), "min %.3f max %.3f" % (min(res), max(res)),
              "| rises below 1.5 ms:", sorted(round(x["read_rise_ms"], 3) for x in cl if x["basis"] == "read-time rise" and x["read_rise_ms"] < 1.5))
    gapb = [(x["first_frame"], x["steps"], x["read_rise_ms"], x["recent_read_gap_ms"], x["basis"], x["whole_loops_added"]) for x in cl if x["basis"] != "read-time rise"]
    print(" non-rise-basis capture clusters:", gapb)
    loops = [(x["first_frame"], x["net_step"], x["whole_loops_added"], x["lost_frames"], x["read_rise_ms"]) for x in cl if x["whole_loops_added"]]
    print(" clusters with whole loops added:", loops)
    neg = [(x["first_frame"], x["steps"], x["read_rise_ms"]) for x in cl if any(s < 0 for s in x["steps"])]
    print(" capture clusters with a step back:", neg)
    sz = [int(e["frames"]) for e in cap if e["kind"] == "skip"]
    print(" capture skips:", len(sz), "48n+12:", sum(1 for s in sz if s % 48 == 12), "others:", sorted(s for s in sz if s % 48 != 12))
    # one-frame events' read jumps
    one = [float(e["read_jump_ms"]) for e in ev if e["cause"] != "capture path" and e["read_jump_ms"] not in ("", None)]
    if one:
        one_s = sorted(one, key=abs)
        print(" one-frame events read_jump: n", len(one), "median %.3f" % one_s[len(one_s)//2], "max|.| %.3f" % max(abs(v) for v in one),
              "over 1.05 ms:", [round(v, 3) for v in one if abs(v) > 1.05])
    t = g["tone"]
    print(" tone: blocks", t["blocks"], "clean", t["clean_blocks"], "invalid", t["invalid"], "torn", t["torn"], "events_across_invalid", t["events_across_invalid"],
          "maxdev", round(t["ch0_clean_max_dev_from_floor_db"], 6), round(t["ch1_clean_max_dev_from_floor_db"], 6))
    nb = collections.Counter()
    for b in bl:
        k = ("L" if int(b["listener"]) else "") + ("B" if int(b["dut_beat"]) else "") + ("C" if int(b["capture_path"]) else "") + ("I" if int(b["invalid"]) else "")
        nb[k or "clean"] += 1
    print(" blocks by content:", dict(nb))
    clean_ppm = max(max(abs(float(b["ppm_997"])), abs(float(b["ppm_9973"]))) for b in bl if int(b["events"]) == 0 and int(b["invalid"]) == 0)
    print(" clean-block max |ppm| either tone: %.2g" % clean_ppm)
    bf = g.get("beat_comb")
    if bf:
        print(" beat comb:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in bf.items()})
        # one member per tooth?
        bfr = sorted(int(e["frame"]) for e in beat)
    r = g["frame_rate_ratio"]
    m = r.get("mcasp_capture", {})
    print(" counted ppm %.3f steps %d frames %d | timed %.2f +- %.2f halves %.2f / %.2f | ext reads %d" % (
        r["counted"]["ppm"], r["counted"]["steps_non_capture"], r["counted"]["observed_frames"],
        m.get("ratio_ppm", float('nan')), m.get("ratio_ppm_halfwidth95", float('nan')),
        m.get("ratio_ppm_first_half", float('nan')), m.get("ratio_ppm_second_half", float('nan')), r["external_capture"]["reads"]))
    print(" mcasp board rate %.3f" % m.get("rate_board", float('nan')), "playback:", {k: r.get("mcasp_playback", {}).get(k) for k in ("ratio_ppm", "ratio_ppm_halfwidth95", "error")})
    cr = g["capture_reads"]
    print(" capture reads", cr["records"], "stalls>15ms", cr["stalls"], "max gap ms", cr["read_gap_ms_max"])
    print(" window s", g["window"]["seconds"], "effective offsets", {k: round(v, 3) for k, v in g["effective_offset_ppm"].items()})
