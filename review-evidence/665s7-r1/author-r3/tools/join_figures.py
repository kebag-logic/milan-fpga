"""join_figures.py MILAN_DP CAPTURE...: per capture and application, at this head's grade: the Join timer intervals
join_intervals() grades (N, min, max in ms, and how many lie outside JOIN_BOUNDS_MS), and the requested transmit
opportunities' egress after lwSRP's last idle poll (N, max in ms, how many past JOIN_FOLLOW_MS)."""
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import srptx_grade as g  # noqa: E402

lo, hi = g.JOIN_BOUNDS_MS
for path in sys.argv[2:]:
    cap = g.load(Path(path))
    for proto in g.APPLICATIONS:
        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        gaps = [gap / 1000 for _, gap in g.join_intervals(cap, frames)]
        req = [(f.us - f.idle_us) / 1000 for f in frames if f.idle_us is not None and not cap.held(f.idle_us / 1000, f.ms)]
        print(f"{Path(path).name} {proto}: Join intervals N {len(gaps)}, {min(gaps):.3f} to {max(gaps):.3f} ms, "
              f"{sum(not lo <= x <= hi for x in gaps)} outside {lo} to {hi}; requested N {len(req)}, egress after the "
              f"last idle poll at most {max(req):.4f} ms, {sum(x > g.JOIN_FOLLOW_MS for x in req)} past {g.JOIN_FOLLOW_MS}")
