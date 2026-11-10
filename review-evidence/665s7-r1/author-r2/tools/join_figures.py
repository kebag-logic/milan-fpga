"""join_figures.py GRADER_DIR CAPTURE...: each capture's Join-timer intervals (the grade's join_intervals) against
JOIN_BOUNDS_MS, per application: N, min, max, and how many fall outside."""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import srptx_grade as g
lo, hi = g.JOIN_BOUNDS_MS
print(f"bound: {lo} to {hi} ms (JOIN_RANGE_MS {g.JOIN_RANGE_MS}, SVC_MS {g.SVC_MS})")
for path in sys.argv[2:]:
    cap = g.load(Path(path))
    for proto in g.APPLICATIONS:
        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        gaps = [gap / 1000 for _, gap in g.join_intervals(cap, frames, g.causes(cap, proto, frames))]
        out = [x for x in gaps if not lo <= x <= hi]
        print(f"{cap.scenario:8s} {proto}: N {len(gaps)}, min {min(gaps):.3f} ms, max {max(gaps):.3f} ms, "
              f"outside {len(out)}" if gaps else f"{cap.scenario:8s} {proto}: N 0")
