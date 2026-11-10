#!/usr/bin/env python3
"""Reviewer probe for #867 round 2 (portable): run from tb/verilator/milan_dp of a clone at the reviewed head.

usage: python3 -B probe_join.py CAPTURE_DIR OUT_DIR

1. every Join-timer interval the grade's join_intervals returns, per scenario and participant, against JOIN_BOUNDS_MS;
2. the two new plants and their controls with the new Join-interval check removed (bounds unbounded);
3. the whole plant set with the grade's SVC_MS re-derived at 19, 21 and 20 ms (1 ms drift either side);
4. the interval after the moved frame in the join-late-within-t-svc control (the README's 179.99 ms claim);
5. each new plant's full findings at the head, to show which words refuse it.
"""
import contextlib
import copy
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
import srptx_grade as g  # noqa: E402
import srptx_plants as p  # noqa: E402

cap_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
docs = {s: json.loads((cap_dir / f"{s}.json").read_text()) for s in ("wire", "hold", "licence")}

print("== 1. Join-timer intervals, bound", g.JOIN_BOUNDS_MS, "SVC_MS", g.SVC_MS)
for s in docs:
    cap = g.load(cap_dir / f"{s}.json")
    for proto in g.APPLICATIONS:
        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        iv = [gap / 1000 for _, gap in g.join_intervals(cap, frames, g.causes(cap, proto, frames))]
        lo, hi = g.JOIN_BOUNDS_MS
        print(f"{s:8} {proto}: N {len(iv)}, min {min(iv):.3f}, max {max(iv):.3f}, outside {sum(not lo <= v <= hi for v in iv)}")


def findings(name, scen="wire"):
    doc = copy.deepcopy(docs[scen])
    p.plant(name, doc)
    f = out / f"{scen}-{name}.json"
    f.write_text(json.dumps(doc) + "\n")
    return g.grade(g.load(f))[0]


print("\n== 5. new plants and controls at the head, full findings")
for name in ("join-early-past-t-svc", "join-interval-late", "join-late-past-t-svc",
             "join-early-within-t-svc", "join-interval-late-within", "join-late-within-t-svc"):
    fs = findings(name)
    print(f"{name}: {len(fs)} finding(s)")
    for x in fs:
        print("   ", x[:200])

print("\n== 2. new Join-interval check removed (JOIN_BOUNDS_MS unbounded)")
saved = g.JOIN_BOUNDS_MS
g.JOIN_BOUNDS_MS = (-1e12, 1e12)
for name in ("join-early-past-t-svc", "join-interval-late"):
    fs = findings(name)
    print(f"{name}: {len(fs)} finding(s) {fs[:2]}")
abl = out / "ablated"
abl.mkdir(exist_ok=True)
for s in docs:
    (abl / f"{s}.json").write_text((cap_dir / f"{s}.json").read_text())
sys.argv = ["srptx_plants.py", str(abl)]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = p.main()
lines = buf.getvalue().splitlines()
print(f"-- full plant set ablated: rc {rc}; {lines[-1]}")
for line in lines:
    if line.startswith("FAIL"):
        print("   ", line[:160])
g.JOIN_BOUNDS_MS = saved

print("\n== 3. SVC_MS drift")
base = dict(SVC_MS=g.SVC_MS, RATE_WINDOW_MS=g.RATE_WINDOW_MS, JOIN_FOLLOW_MS=g.JOIN_FOLLOW_MS,
            JOIN_BOUNDS_MS=g.JOIN_BOUNDS_MS, LEAVE_ALL_BOUNDS_MS=g.LEAVE_ALL_BOUNDS_MS)
for svc in (19, 21, 20):
    g.SVC_MS = svc
    g.RATE_WINDOW_MS = 3 * g.JOIN_MS // 2 - svc
    g.JOIN_FOLLOW_MS = g.JOIN_MS + svc
    g.JOIN_BOUNDS_MS = (g.JOIN_RANGE_MS[0] - svc, g.JOIN_RANGE_MS[1] + svc)
    g.LEAVE_ALL_BOUNDS_MS = (g.LEAVE_ALL_MS - g.JOIN_MS - svc, 3 * g.LEAVE_ALL_MS // 2 + g.JOIN_MS + svc)
    sys.argv = ["srptx_plants.py", str(out / f"drift{svc}")]
    (out / f"drift{svc}").mkdir(exist_ok=True)
    for s in docs:
        (out / f"drift{svc}" / f"{s}.json").write_text((cap_dir / f"{s}.json").read_text())
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = p.main()
    lines = buf.getvalue().splitlines()
    print(f"-- SVC_MS {svc}: rc {rc}; {lines[-1]}")
    for line in lines:
        if line.startswith("FAIL"):
            print("   ", line[:160])
for k, v in base.items():
    setattr(g, k, v)

print("\n== 4. join-late-within-t-svc: the MSRP interval after the moved frame")
doc = copy.deepcopy(docs["wire"])
p.plant("join-late-within-t-svc", doc)
ms = [m for m in p.frames(doc, "MSRP")][:4]
print("first MSRP frames, us:", [round(m["us"], 3) for m in ms])
print("gaps ms:", [round((b["us"] - a["us"]) / 1000, 3) for a, b in zip(ms, ms[1:])])
