#!/usr/bin/env python3
"""window_counterfactual.py - check the README's claim about a time-window attribution of LeaveAll frames.

Usage: python3 -I window_counterfactual.py CLONE CAPTURE.json

The README (tb/verilator/milan_dp/README.md, 'A Join timer's frame is what lwSRP did') says a time window
that gives a frame to the Join timer when the latest Join or periodic expiry within 100 ms before it is a
Join expiry would, over the LeaveAll frames the grade now counts, refuse six LeaveAll frames of `wire`,
each after a Join expiry that found nothing to send. This applies that window to every non-queued LeaveAll
frame, grades its gap from the frame before against JOIN_BOUNDS_MS, and lists those it would refuse with
the bench's after_join and idle_us for the frame.
"""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    clone = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(clone / "tb/verilator/milan_dp"))
    import srptx_grade as g  # noqa: E402
    cap = g.load(Path(sys.argv[2]))
    lo, hi = g.JOIN_BOUNDS_MS
    total = 0
    for proto in ("MSRP", "MVRP"):
        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        exp = [t for t in cap.doc["timers"] if t["proto"] == proto and t["event"] == "expire"
               and t["kind"] in ("join", "periodic")]
        for k in range(1, len(frames)):
            f = frames[k]
            if not f.leave_all_types() or cap.held(frames[k - 1].ms, f.ms):
                continue
            before = [t for t in exp if t["us"] <= f.us and f.us - t["us"] < g.ATTRIBUTE_MS * 1000]
            if not before or max(before, key=lambda t: t["us"])["kind"] != "join":
                continue
            gap = (f.us - frames[k - 1].us) / 1000
            if not lo <= gap <= hi:
                total += 1
                print(f"{proto} LeaveAll frame at ms {f.ms}: {gap:.3f} ms after the one before; "
                      f"after_join={f.after_join} idle_us={f.idle_us}")
    print(f"window would refuse {total} LeaveAll frame(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
