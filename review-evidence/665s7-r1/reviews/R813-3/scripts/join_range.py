#!/usr/bin/env python3
"""join_range.py - the Join-timer intervals and requested-opportunity latencies the head grade measures.

Usage: python3 -I join_range.py CLONE CAPTURE.json [...]

Imports CLONE's tb/verilator/milan_dp/srptx_grade.py and, for each capture, prints the min and max of
join_intervals() per protocol (ms), and the max of (frame us - idle_us) over frames with idle_us set (ms),
the two figures the README's 'What it finds at this head' states for every scenario and off-grid control.
"""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    clone = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(clone / "tb/verilator/milan_dp"))
    import srptx_grade as g  # noqa: E402
    lo, hi, req = float("inf"), float("-inf"), 0.0
    for path in sys.argv[2:]:
        cap = g.load(Path(path))
        for proto in ("MSRP", "MVRP"):
            frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
            gaps = [gap / 1000 for _, gap in g.join_intervals(cap, frames)]
            reqs = [(f.us - f.idle_us) / 1000 for f in frames if f.idle_us is not None
                    and not cap.held(f.idle_us / 1000, f.ms)]
            if gaps:
                lo, hi = min(lo, min(gaps)), max(hi, max(gaps))
            if reqs:
                req = max(req, max(reqs))
            print(f"{Path(path).name} {proto}: {len(gaps)} Join intervals "
                  f"{min(gaps, default=0):.3f}..{max(gaps, default=0):.3f} ms; {len(reqs)} requested, "
                  f"max {max(reqs, default=0):.3f} ms")
    print(f"all: Join intervals {lo:.3f}..{hi:.3f} ms; requested max {req:.3f} ms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
