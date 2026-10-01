#!/usr/bin/env python3
"""Re-derive, from the archived grades alone, the round-2 attribution statements
on the B6 findings page that the published summaries can decide.

Usage: attribution_recheck.py <summary-dir>   (review-evidence/b6-r1/author/summary)

Inputs per case: grade.json (skip_clusters, beat_comb, attribution, window,
dut_reads) and events.csv. The raw read times (cap-ts.bin) and grade-full.json
are not published, so the gap-test share of read positions (path 5) and the
beat-member distance to the nearest *read-time* event are out of reach here;
what is in reach is printed with the page's claim beside it.
"""
import csv, json, os, sys

root = sys.argv[1]
CASES = ["a0", "a1", "a2", "bint", "bcrf"]
LOOP = 48000


def load(c):
    g = json.load(open(os.path.join(root, c, "grade.json")))
    ev = list(csv.DictReader(open(os.path.join(root, c, "events.csv"))))
    return g, ev


def mod48(n):
    return n % 48


out = []
def say(*a):
    print(*a)

for c in CASES:
    g, ev = load(c)
    cl = g["skip_clusters"]
    say(f"\n=== {c}")
    caps = [e for e in ev if e["cause"] == "capture path"]
    lis = [e for e in ev if e["cause"] == "listener"]
    beat = [e for e in ev if e["cause"] == "DUT beat"]
    other = sorted({e["cause"] for e in ev} - {"capture path", "listener", "DUT beat"})
    say(f"events: capture {len(caps)}, listener {len(lis)}, beat {len(beat)}, other causes {other}")
    cpc = [k for k in cl if k["capture_path"]]
    say(f"clusters: {len(cl)} total, capture-path {len(cpc)}; non-capture {[k['cluster'] for k in cl if not k['capture_path']]}")
    bases = {}
    for k in cpc:
        bases.setdefault(k["basis"], []).append(k["cluster"])
    say("capture-path cluster basis:", {b: len(v) for b, v in bases.items()})

    # Path 1: every capture-path skip size modulo 48.
    skips = [(k["cluster"], s, k["basis"]) for k in cpc for s in k["steps"]]
    off = [(cid, s, mod48(s) if s > 0 else None, b) for cid, s, b in skips if not (s > 0 and mod48(s) == 12)]
    say(f"path1: capture-path steps {len(skips)}; not a positive 48n+12 skip: {off}")
    p13 = [(cid, s) for cid, s, b in skips if s > 0 and mod48(s) == 13]
    p11 = [(cid, s) for cid, s, b in skips if s > 0 and mod48(s) == 11]
    say(f"path1: 48n+13 skips {p13}; 48n+11 skips {p11}")
    # The page's 255 of 265 statement counts skips in clusters with a matching rise.
    rise = [k for k in cpc if k["basis"] == "read-time rise"]
    rs = [s for k in rise for s in k["steps"] if s > 0]
    say(f"rise-basis clusters {len(rise)}: positive skips {len(rs)}, of them 48n+12 {sum(1 for s in rs if mod48(s) == 12)}")

    # Path 3: clusters where a rise was measured but did not match (gap+size branch),
    # path 5: rise unmeasurable (gap-only), by the grade's own basis and read_rise_ms.
    for k in cpc:
        if k["basis"] != "read-time rise":
            say(f"  non-rise cluster {k['cluster']}: basis={k['basis']!r} rise={k['read_rise_ms']} gap={k['recent_read_gap_ms']} "
                f"size_sig={k['size_signature']} steps={k['steps'][:8]}{'...' if len(k['steps'])>8 else ''}")

    # Path 4: capture-path clusters whose total loss is under 98 frames.
    small = [k for k in cpc if abs(k["lost_frames"]) < 98]
    say(f"path4: smallest capture-path loss {min(abs(k['lost_frames']) for k in cpc) if cpc else None}; clusters under 98 frames: "
        + str([(k['cluster'], k['events'], k['steps'], k['read_rise_ms'], k['recent_read_gap_ms']) for k in small]))

    # Path 2: beat members one per tooth.
    bc = g["beat_comb"]
    bf = sorted(int(e["frame"]) for e in beat)
    if bc is None:
        say(f"path2: no beat comb; beat events {len(beat)}")
    else:
      say(f"path2: comb members {bc['members']}, teeth in window {bc['teeth_in_window']:.1f}, residual_max {bc['residual_max']:.3f}")
    if c in ("a1",):
        # Source-frame position (the page's definition): the captured frame plus every
        # earlier step, with a cluster's whole loops added at its event. events.csv
        # 'frame' is the window-relative capture ordinal; 'capture_frame' is the file
        # ordinal, which the clusters' first_frame uses.
        allev = sorted(ev, key=lambda e: int(e["frame"]))
        cum = 0
        src = {}
        loops = {k["first_frame"]: k["whole_loops_added"] for k in cpc}
        for e in allev:
            src[id(e)] = int(e["frame"]) + cum
            cum += int(e["step"]) + (LOOP * loops.pop(int(e["capture_frame"]), 0) if e["cause"] == "capture path" else 0)
        bsrc = sorted(src[id(e)] for e in beat)
        gaps = [b - a for a, b in zip(bsrc, bsrc[1:])]
        P = bc["period_frames"]
        say(f"path2 a1: min source-frame spacing {min(gaps)}, max {max(gaps)}; spacings not ~1 period: "
            f"{[(i, gg, round(gg / P, 3)) for i, gg in enumerate(gaps) if abs(gg / P - round(gg / P)) > 0.01 or round(gg / P) != 1][:10]}")
        miss = [(i, round(gg / P)) for i, gg in enumerate(gaps) if round(gg / P) > 1]
        say(f"path2 a1: gaps spanning >1 tooth (index, teeth): {miss}; total missing teeth {sum(t - 1 for _, t in miss)}")
        # Capture-frame distance from each beat member to the nearest capture-path event.
        cf = sorted(int(e["frame"]) for e in caps)
        d = [min(abs(b - x) for x in cf) for b in bf]
        say(f"path2 a1: min capture-ordinal distance beat member -> capture-path event: {min(d)}")
        # Where the missing teeth fall: the capture-path clusters straddling those gaps.
        for i, t in miss:
            bcf = sorted(int(e["capture_frame"]) for e in beat)
            lo, hi = bcf[i], bcf[i + 1]
            inside = [(k["cluster"], k["lost_frames"], k["whole_loops_added"], k["read_rise_ms"]) for k in cpc
                      if lo <= k["first_frame"] <= hi]
            say(f"  gap {i}: capture {lo}..{hi}, {t - 1} missing teeth; capture-path clusters between the two members (capture ordinals): {inside}")
    one = [e for e in ev if abs(int(e["step"])) == 1 or e["kind"] in ("insert",)]
    say(f"one-frame events of any cause: {len(one)}")

    # Read-time rise measurability for one-frame events (events.csv read_jump_ms).
    for name, grp in (("listener", lis), ("beat", beat)):
        m = [float(e["read_jump_ms"]) for e in grp if e["read_jump_ms"] not in ("", "None")]
        if grp:
            mx = max(m, key=abs) if m else None
            big = sorted([x for x in m if abs(x) > 1.05], key=abs)
            med = sorted(m)[len(m) // 2] if m else None
            say(f"rise {name}: measurable {len(m)} of {len(grp)}; median {med}; max |.| {mx}; over 1.05 ms {big}")

    # Window start against the last bind/set.
    w = g["window"]
    say(f"window: {w}")
    dr = g.get("dut_reads", [])
    say("dut_reads tags:", [(r["tag"], round(r["t"], 3), r["words"].get("0x8f8")) for r in dr][:12])
