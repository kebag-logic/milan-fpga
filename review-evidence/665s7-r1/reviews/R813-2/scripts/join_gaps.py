"""join_gaps.py MILAN_DP CAPTURE...: for each capture, every consecutive MSRP/MVRP egress gap (frames the grade
keeps), classified by the grade's own cause attribution, and the Join-timer intervals the grade bounds.

Prints, per application: the Join-timer intervals (N, min, max, outside JOIN_BOUNDS_MS), and every gap NOT graded
as a Join-timer interval that lies outside JOIN_BOUNDS_MS, with its cause, so a reader can see what the two-sided
check leaves out and why. Read-only: it imports the grade from MILAN_DP and writes nothing."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import srptx_grade as g  # noqa: E402

lo, hi = g.JOIN_BOUNDS_MS
print(f"grade bounds: JOIN_BOUNDS_MS {g.JOIN_BOUNDS_MS}, SVC_MS {g.SVC_MS}, JOIN_RANGE_MS {g.JOIN_RANGE_MS}")
for path in sys.argv[2:]:
    cap = g.load(Path(path))
    for proto in g.APPLICATIONS:
        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        cause = g.causes(cap, proto, frames)
        joins = g.join_intervals(cap, frames, cause)
        gaps = [gap / 1000 for _, gap in joins]
        out = [x for x in gaps if not lo <= x <= hi]
        print(f"{cap.scenario:8} {proto}: frames {len(frames)}, Join-timer intervals N {len(gaps)}, "
              f"min {min(gaps):.3f}, max {max(gaps):.3f}, outside {len(out)}")
        kinds = Counter()
        for k in range(1, len(frames)):
            gap = (frames[k].us - frames[k - 1].us) / 1000
            c = cause[k][0] if cause[k] else None
            held = cap.held(frames[k - 1].ms, frames[k].ms)
            if (c == "join" and not held) or lo <= gap <= hi:
                continue
            kinds[(c, held)] += 1
            if kinds[(c, held)] <= 3:
                print(f"    not a graded Join interval: ms {frames[k].ms}, gap {gap:.3f} ms, cause {c}, held {held}")
        print(f"    ungraded gaps outside the bound by (cause, held): {dict(kinds)}")
