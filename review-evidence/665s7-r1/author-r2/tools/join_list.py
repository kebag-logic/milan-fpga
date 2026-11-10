"""join_list.py GRADER_DIR CAPTURE: every Join-timer-driven frame per application, its gap and events."""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import srptx_grade as g
cap = g.load(Path(sys.argv[2]))
for proto in g.APPLICATIONS:
    frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
    exp = [t for t in cap.doc["timers"] if t["proto"] == proto and t["event"] == "expire" and t["kind"] in ("join", "periodic", "leaveall")]
    rows = []
    for k, f in enumerate(frames):
        before = [t for t in exp if t["kind"] in ("join", "periodic") and t["us"] <= f.us and f.us - t["us"] < g.ATTRIBUTE_MS * 1000]
        if f.leave_all_types() or not before or max(before, key=lambda t: t["us"])["kind"] != "join" or k == 0:
            continue
        p = frames[k - 1]
        rows.append((k, f.ms, round((f.us - p.us) / 1000, 3), sorted({e for _, _, e in p.values()}), sorted({e for _, _, e in f.values()}),
                     sorted(p.leave_all_types())))
    print(proto, len(rows))
    for r in rows[:40]:
        print("  ", r)
