#!/usr/bin/env python3
"""Beat-comb geometry from the published grades: source frames as grade_b6.py
defines them, member spacing, distance to capture-path events, missing teeth,
and where the A2 read-time exceptions sit relative to its longest stall.
Usage: beat_geometry.py <author/summary dir>"""
import csv, json, os, sys
import numpy as np
S = sys.argv[1]
def load(c):
    ev = list(csv.DictReader(open(os.path.join(S, c, "events.csv"))))
    g = json.load(open(os.path.join(S, c, "grade.json")))
    lost = {x["cluster"]: x["lost_frames"] for x in g["skip_clusters"] if x["capture_path"]}
    for e in ev:
        for k in ("capture_frame", "frame", "frames", "step"):
            e[k] = int(e[k])
    # source frames exactly as grade_b6.py builds them (a capture cluster corrected to its
    # true loss at its first event)
    cum = 0; seen = set()
    for e in ev:
        e["source"] = e["capture_frame"] + cum
        cum += e["step"]
        if e["cause"] == "capture path" and e["cluster"] != "" and int(e["cluster"]) not in seen:
            ci = int(e["cluster"]); seen.add(ci)
            cum += lost[ci] - sum(x["step"] for x in ev if x["cluster"] == e["cluster"] and x["cause"] == "capture path")
    return ev, g
for c in ("a0", "a1", "a2", "bint"):
    ev, g = load(c)
    b = np.array([e["source"] for e in ev if e["cause"] == "DUT beat"], dtype=float)
    cp = [e for e in ev if e["cause"] == "capture path"]
    n = np.round((b - b[0]) / g["beat_comb"]["period_frames"])
    P, b0 = np.polyfit(n, b, 1)
    resid = b - (b0 + n * P)
    sp = np.diff(b)
    per_tooth = len(np.unique(n)) == len(n)
    cps = np.array([e["source"] for e in cp], dtype=float)
    cpc = np.array([e["capture_frame"] for e in cp], dtype=float)
    bc = np.array([e["capture_frame"] for e in ev if e["cause"] == "DUT beat"], dtype=float)
    dsrc = np.min(np.abs(b[:, None] - cps[None, :]), axis=1) if len(cps) else None
    dcap = np.min(np.abs(bc[:, None] - cpc[None, :]), axis=1) if len(cpc) else None
    allt = np.arange(int(n.min()), int(n.max()) + 1)
    missing = sorted(set(allt) - set(n.astype(int)))
    print(f"== {c}: members {len(b)}, period fit {P:.2f}, one per tooth {per_tooth}, residual max {np.abs(resid).max():.3f}")
    print(f"   source spacing min {sp.min():.0f} max {sp.max():.0f}; min distance to a capture-path event: source {dsrc.min():.0f}, capture {dcap.min():.0f}")
    big = [x for x in g["skip_clusters"] if x["capture_path"] and x["lost_frames"] > 48000]
    spans = []
    for x in big:
        mem = [e for e in ev if e["cluster"] == str(x["cluster"]) and e["cause"] == "capture path"]
        s0 = mem[0]["source"]; spans.append((x["cluster"], s0, s0 + x["lost_frames"], x["lost_frames"]))
    print(f"   clusters over one loop (cluster, source start, source end, lost): {spans}")
    mt = [(int(t), b0 + t * P) for t in missing]
    inside = [any(s - 50 <= pos <= e + 50 for _, s, e, _ in spans) for _, pos in mt]
    print(f"   missing interior teeth {len(missing)}: inside a >1-loop loss {sum(inside)}; positions {[round(p) for _, p in mt]}")
    print(f"   teeth before first / after last member are window-edge teeth; teeth_in_window {g['beat_comb']['teeth_in_window']:.1f}")
    if c == "a2":
        st = [x for x in g["skip_clusters"] if x["recent_read_gap_ms"] and x["recent_read_gap_ms"] > 13000]
        for x in st:
            print(f"   long-stall cluster {x['cluster']} first capture frame {x['first_frame']} gap {x['recent_read_gap_ms']} steps {x['steps']}")
        for e in ev:
            if e["cause"] == "DUT beat" and e["read_jump_ms"] and abs(float(e["read_jump_ms"])) > 1.01:
                d = [(e["capture_frame"] - x["first_frame"]) / 48000 for x in st]
                print(f"   exception beat repeat at capture frame {e['capture_frame']} rise {e['read_jump_ms']} ms; seconds from the 13.3 s stall cluster's first event: {[round(v,3) for v in d]}")
        cl46 = [x for x in g["skip_clusters"] if x["cluster"] == 46][0]
        print(f"   cluster 46: steps {cl46['steps']} net {cl46['net_step']} net mod 48 {cl46['net_step'] % 48} lost {cl46['lost_frames']} loops {cl46['whole_loops_added']} rise {cl46['read_rise_ms']}")
        cl55 = [x for x in g["skip_clusters"] if x["cluster"] == 55][0]
        print(f"   cluster 55: steps {cl55['steps']} lost {cl55['lost_frames']} loops {cl55['whole_loops_added']} rise {cl55['read_rise_ms']}")
