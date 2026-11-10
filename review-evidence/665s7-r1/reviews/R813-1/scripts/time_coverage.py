#!/usr/bin/env python3
"""How many [TIME] JoinTime-follow checks srptx_grade.py evaluates in each capture, and how many it skips
because a frame of the application was received in the window or a hold touched it (reviewer probe; reads
srptx_grade's own functions, mirrors grade_time's selection loop without changing it).

  python3 -I time_coverage.py MILAN_DP_DIR CAPTURE_DIR
"""
import sys
from pathlib import Path

DP, CAPS = (Path(a).resolve() for a in sys.argv[1:3])
sys.path.insert(0, str(DP))
import srptx_grade as g  # noqa: E402

for s in ("wire", "hold", "licence"):
    cap = g.load(CAPS / f"{s}.json")
    for proto in g.APPLICATIONS:
        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        received = cap.received(proto)
        hist = {}
        for f in frames:
            for kind, value, event in f.values():
                hist.setdefault((kind, value), []).append((f, event))
        ev = skip_rx = skip_hold = 0
        worst = 0.0
        for (kind, value), msgs in hist.items():
            for k, (f, event) in enumerate(msgs):
                first = event in g.DECLARING and (k == 0 or msgs[k - 1][1] in ("Lv", "Mt"))
                if event != "New" and not first:
                    continue
                later = msgs[k + 1][0] if k + 1 < len(msgs) else None
                until = later.us / 1000 if later else cap.doc["run_ms"]
                if any(f.ms <= r <= until for r, _ in received):
                    skip_rx += 1
                elif cap.held(f.ms, until):
                    skip_hold += 1
                else:
                    ev += 1
                    worst = max(worst, until - f.us / 1000)
        print(f"{s} {proto}: {ev} evaluated (worst {worst:.3f} ms against {g.JOIN_FOLLOW_MS}), "
              f"{skip_rx} skipped for a received frame, {skip_hold} for a hold; {len(received)} received")
