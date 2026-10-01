#!/usr/bin/env python3
"""Block-level page claims: the THD+N range of blocks off the floor, whether every positive
THD+N block holds a capture-path loss, the worst listener/beat-only blocks, and beat teeth
missing from the comb against capture-path losses.

usage: check_blocks.py <evidence author dir>
"""
import csv, json, os, sys
import numpy as np
root = sys.argv[1]
for case in ("a0", "a1", "a2", "bint", "bcrf"):
    bl = list(csv.DictReader(open(os.path.join(root, "summary", case, "blocks.csv"))))
    off = [b for b in bl if not (int(b["events"]) == 0 and int(b["invalid"]) == 0)]
    th = [float(b[k]) for b in off for k in ("thdn_db_997", "thdn_db_9973")]
    pos = [b for b in bl if max(float(b["thdn_db_997"]), float(b["thdn_db_9973"])) > 0]
    pos_nocap = [b["block"] for b in pos if int(b["capture_path"]) == 0]
    lst = [b for b in bl if int(b["listener"]) > 0]
    lst_nocap = [b for b in lst if int(b["capture_path"]) == 0]
    beat_only = [b for b in bl if int(b["dut_beat"]) > 0 and int(b["listener"]) == 0 and int(b["capture_path"]) == 0]
    def worst(g, k): return round(max(float(b[k]) for b in g), 2) if g else None
    print(f"{case}: off-floor blocks {len(off)} of {len(bl)}; THD+N range over both tones {min(th) if th else None:.2f} .. {max(th) if th else 0:.2f} dB")
    print(f"   positive-THD+N blocks {len(pos)}, without a capture-path loss: {pos_nocap}")
    print(f"   worst listener block 997/9973: {worst(lst,'thdn_db_997')} / {worst(lst,'thdn_db_9973')}; listener-only (no capture loss): {worst(lst_nocap,'thdn_db_997')} / {worst(lst_nocap,'thdn_db_9973')}")
    print(f"   worst beat-only block 997/9973: {worst(beat_only,'thdn_db_997')} / {worst(beat_only,'thdn_db_9973')}")
    ev = list(csv.DictReader(open(os.path.join(root, "summary", case, "events.csv"))))
    g = json.load(open(os.path.join(root, "summary", case, "grade.json")))
    # rebuild source frames as grade_b6.py does (steps, plus a capture cluster's whole loops at its first event)
    cl = {str(x["cluster"]): x for x in g["skip_clusters"] if x["capture_path"]}
    cum = 0; seen = set(); src = []; lost_iv = []
    for e in ev:
        sf = int(e["capture_frame"]) + cum
        src.append(sf)
        cum += int(e["step"])
        c = e["cluster"]
        if c in cl and c not in seen:
            seen.add(c)
            extra = cl[c]["lost_frames"] - cl[c]["net_step"]
            cum += extra
    # loss intervals in source frames: from the cluster's first event's source frame back by its lost frames
    for c, x in cl.items():
        i = next(j for j, e in enumerate(ev) if e["cluster"] == c)
        lost_iv.append((src[i] - 2000, src[i] + x["lost_frames"] + 2000 + (int(ev[[j for j, e in enumerate(ev) if e["cluster"] == c][-1]]["capture_frame"]) - int(ev[i]["capture_frame"]))))
    beat = np.array([s for s, e in zip(src, ev) if e["cause"] == "DUT beat"], dtype=float)
    if len(beat) > 3:
        P = g["beat_comb"]["period_frames"]
        n = np.round((beat - beat[0]) / P)
        P, b0 = np.polyfit(n, beat, 1)
        w0 = int(g["window"]["start_frame"]) - int(g["window"]["start_frame"])
        last = src[-1] + 2 * P
        teeth = np.arange(np.floor((0 - b0) / P), np.ceil((last + 0 - b0) / P) + 1)
        pos_t = b0 + teeth * P
        total_src = int(g["window"]["frames"]) + cum - sum(int(e["step"]) for e in ev) * 0
        pos_t = pos_t[(pos_t > int(g["window"]["start_frame"])) & (pos_t < int(g["window"]["end_frame"]) + sum(x["lost_frames"] for x in cl.values()) + sum(int(e["step"]) for e in ev if e["cause"] != "capture path"))]
        member = np.array([np.min(np.abs(beat - p)) <= 50 for p in pos_t])
        missing = pos_t[~member]
        inloss = [any(a <= p <= b for a, b in lost_iv) for p in missing]
        print(f"   beat teeth in span {len(pos_t)}, members {int(member.sum())}, missing {len(missing)}, missing inside a capture-path loss {sum(inloss)}; missing not in a loss at source frames {[int(p) for p, k in zip(missing, inloss) if not k]}")
        dup = len(beat) - len(set(np.round((beat - b0) / P)))
        print(f"   teeth with more than one member: {dup}")
