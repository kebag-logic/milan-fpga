#!/usr/bin/env python3
"""Round-2 checks of lane B6's attribution against its five absorption paths (read-only).

usage: attribution_checks.py <lane_packet_dir> <raw_dir>

Inputs, never written:
  <lane_packet_dir>/summary/<case>/grade.json and events.csv  (published in the evidence archive)
  <raw_dir>/<case>/grade-full.json  (full grade; the page lists its SHA-256)
  <raw_dir>/<case>/cap-ts.bin       (capture read times; the page lists its SHA-256)

The grader's constants are restated here, not imported: clusters of |step| >= 2 within
30 reads of 480 frames, the rise test 1 ms + 2 %, the read gap 11 ms in the 60 reads before
the cluster through 2 reads after it, beat membership within 50 frames of the comb line.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

FS = 48000
LOOP = 48000
GAP_MS = 11.0
LOOKBACK_READS = 60
BEAT_RES = 50
CASES = ["a0", "a1", "a2", "bint", "bcrf"]

pk, raw = Path(sys.argv[1]), Path(sys.argv[2])


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def tol_ms(lost_ms):
    return 1.0 + 0.02 * lost_ms


out = []
p = out.append
p("Lane B6 round-2 attribution checks; inputs and their SHA-256:")
for c in CASES:
    for f in (pk / "summary" / c / "grade.json", pk / "summary" / c / "events.csv",
              raw / c / "grade-full.json", raw / c / "cap-ts.bin"):
        p(f"  {c}/{f.parent.name if f.parent.name != c else ''}{'/' if f.parent.name != c else ''}{f.name} {sha(f)}")
p("")

for c in CASES:
    g = json.load(open(pk / "summary" / c / "grade.json"))
    full = json.load(open(raw / c / "grade-full.json"))
    ev = full["events_list"]
    cl = g["skip_clusters"]
    cap = [k for k in cl if k["capture_path"]]
    p(f"=== {c}: {len(cl)} clusters, {len(cap)} capture path; events {len(ev)}")

    # path 1: a one-frame listener drop merged into a capture-path skip shows as 48 n + 13
    # (a repeat as 48 n + 11); losses over a loop and stale-replay clusters carry no size test
    sizes = {}
    off = []
    for k in cap:
        replay = any(s < 0 for s in k["steps"])
        loops = k["whole_loops_added"] > 0
        for s in k["steps"]:
            if s <= 0:
                continue
            r = s % 48
            sizes[r] = sizes.get(r, 0) + 1
            if r != 12:
                why = ("loss over a loop" if loops else "stale-replay cluster" if replay else
                       "cluster total 48n+12" if k["net_step"] % 48 == 12 else "one frame off" if r in (11, 13)
                       else "other")
                off.append((k["cluster"], s, r, why, k["basis"], k["net_step"], k["lost_frames"], k["read_rise_ms"]))
    p(f"  path 1  capture-path skips by size mod 48: {dict(sorted(sizes.items()))}")
    for o in off:
        p(f"          off 48n+12: cluster {o[0]} skip {o[1]} (48n+{o[2]}): {o[3]}; basis {o[4]}; "
          f"net {o[5]}, lost {o[6]}, rise {o[7]} ms")
    for k in cap:
        if k["whole_loops_added"] > 0 or any(s < 0 for s in k["steps"]):
            res = None if k["read_rise_ms"] is None else round(k["read_rise_ms"] - k["lost_ms"], 4)
            p(f"          no size test: cluster {k['cluster']} steps {k['steps']} loops {k['whole_loops_added']} "
              f"lost {k['lost_frames']} ({k['lost_ms']} ms) rise {k['read_rise_ms']} ms, rise less loss {res} ms, "
              f"tolerance {round(tol_ms(k['lost_ms']), 3)} ms")

    # path 2: a listener repeat within 50 frames of a beat tooth joins the comb
    one = [e for e in ev if e["frames"] == 1]
    mem = [e for e in ev if e.get("beat_member")]
    bc = g.get("beat_comb")
    p(f"  path 2  one-frame events {len(one)} (repeats {sum(e['kind'] == 'repeat' for e in one)}, "
      f"skips {sum(e['kind'] == 'skip' for e in one)}, inserts {sum(e['kind'] == 'insert' for e in one)}); "
      f"beat members {len(mem)}")
    if bc and mem:
        P = bc["period_frames"]
        sf = np.array(sorted(e["source_frame"] for e in mem), dtype=np.float64)
        sp = np.diff(sf)
        teeth = np.round((sf - sf[0]) / P).astype(int)
        u, n = np.unique(teeth, return_counts=True)
        exp = int(round(bc["teeth_in_window"]))
        p(f"          member spacing min {int(sp.min())} frames, max {int(sp.max())}; teeth with two or more "
          f"members {int((n > 1).sum())}; teeth spanned {int(teeth[-1]) + 1}, occupied {len(u)}, "
          f"comb residual max {bc['residual_max']:.3f} frames")
        # a listener repeat could stand in for a beat only at a tooth whose beat was hidden in lost
        # audio, so within 50 frames of a capture-path loss; distance of each member to the nearest
        # capture-path event, in capture frames
        cf_cap = np.array(sorted(e["capture_frame"] for e in ev if e["cause"] == "capture path"), dtype=np.int64)
        if len(cf_cap):
            d = [int(np.abs(cf_cap - e["capture_frame"]).min()) for e in mem]
            p(f"          member nearest capture-path event: min {min(d)} capture frames")
        miss = sorted(set(range(int(teeth[-1]) + 1)) - set(u.tolist()))
        p(f"          missing teeth inside the span: {len(miss)}")
        # where each missing tooth falls: the source frames an event's step jumps over
        # (sf, sf + step + whole loops], the loops counted at a cluster's first event
        if miss:
            Pf, b0 = np.polyfit(teeth.astype(np.float64), sf, 1)
            for t in miss:
                T = b0 + t * Pf
                where = []
                for e in ev:
                    extra = 0
                    if e.get("cluster_lost_frames"):
                        extra = e["cluster_lost_frames"] - sum(
                            x["step"] for x in ev if x.get("cluster") == e.get("cluster") and x["cause"] == "capture path")
                    jump = e["step"] + extra
                    if jump > 0 and e["source_frame"] - BEAT_RES < T <= e["source_frame"] + jump + BEAT_RES:
                        where.append((e["capture_frame"], e["cause"], e.get("cluster"), int(jump)))
                p(f"          missing tooth {t} at source frame {T:.0f}: inside {where}")

    # path 3: a spoiled (measured, non-matching) rise accepted on a read gap and the 48 n + 12 size
    sp3 = [k for k in cap if k["basis"] == "read gap and 48 n + 12 size"]
    p(f"  path 3  clusters on the read gap and size rule with a measured rise: {len(sp3)} "
      f"{[(k['cluster'], k['steps'], k['read_rise_ms'], k['recent_read_gap_ms']) for k in sp3]}")

    # path 4: the rise tolerance; a zero rise matches any loss of 48 frames or less, and a rise at
    # the read-time floor's step (up to 1.0 ms on a one-frame event) matches up to about 98 frames
    small = sorted(cap, key=lambda k: k["lost_frames"])
    p(f"  path 4  smallest capture-path loss {small[0]['lost_frames'] if small else None} frames; "
      f"clusters with loss <= 48 frames: {sum(k['lost_frames'] <= 48 for k in cap)}; "
      f"<= 98 frames: {[(k['cluster'], k['steps'], k['read_rise_ms'], k['recent_read_gap_ms'], k['basis']) for k in cap if k['lost_frames'] <= 98]}")

    # path 5: the gap-only branch (no measurable rise): no size test in the rule
    g5 = [k for k in cap if k["basis"] == "read gap"]
    p(f"  path 5  gap-only clusters {len(g5)}; every skip 48n+12: "
      f"{all(s % 48 == 12 for k in g5 for s in k['steps'] if s > 0)}; "
      f"{[(k['cluster'], k['steps'], k['recent_read_gap_ms']) for k in g5]}")
    ts = np.fromfile(raw / c / "cap-ts.bin", dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("raw", "<i8")]))
    TF, TRAW = ts["f"], ts["raw"]
    gaps = np.diff(TRAW) / 1e6
    # every read inside the window, as the position of a hypothetical one-event cluster
    lo = int(np.searchsorted(TF, g["window"]["start_frame"], side="left"))
    hi = int(np.searchsorted(TF, g["window"]["end_frame"], side="left"))
    big = gaps >= GAP_MS
    cs = np.concatenate([[0], np.cumsum(big)])
    hit = 0
    tot = 0
    for j in range(max(lo, 1), min(hi, len(gaps))):
        a, b = max(0, j - 1 - LOOKBACK_READS), min(len(gaps), j + 3)
        tot += 1
        hit += (cs[b] - cs[a]) > 0
    p(f"          a read position in the window meets the read-gap test: {hit} of {tot} = "
      f"{100.0 * hit / max(tot, 1):.1f} %")

    # read-time rise across one-frame events (item 3)
    with open(pk / "summary" / c / "events.csv") as f:
        rows = list(csv.DictReader(f))
    for cause in ("listener", "DUT beat"):
        r1 = [r for r in rows if r["frames"] == "1" and r["cause"] == cause]
        m = [float(r["read_jump_ms"]) for r in r1 if r["read_jump_ms"] not in ("", "None")]
        over = [(r["capture_frame"], r["kind"], r["read_jump_ms"]) for r in r1
                if r["read_jump_ms"] not in ("", "None") and abs(float(r["read_jump_ms"])) > 1.05]
        if r1:
            p(f"  item 3  {cause}: one-frame events {len(r1)}, measurable rise {len(m)}, median "
              f"{np.median(m) if m else None:.3f} ms, max |rise| {max(abs(x) for x in m) if m else None:.4f} ms, "
              f"over 1.05 ms {over}")
        else:
            p(f"  item 3  {cause}: one-frame events 0")
    longest = max(cap, key=lambda k: k["lost_frames"]) if cap else None
    if longest:
        p(f"  longest capture-path loss: cluster {longest['cluster']} at capture frame {longest['first_frame']}, "
          f"lost {longest['lost_frames']} frames, gap {longest['recent_read_gap_ms']} ms")
    p("")

print("\n".join(out))
