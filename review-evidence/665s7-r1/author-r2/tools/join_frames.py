"""join_frames.py GRADER_DIR CAPTURE PROTO [N]: the first N frames of PROTO with their timer cause and each value's event."""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import srptx_grade as g
cap = g.load(Path(sys.argv[2]))
proto, n = sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 12
frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
exp = [t for t in cap.doc["timers"] if t["proto"] == proto and t["event"] == "expire" and t["kind"] in ("join", "periodic", "leaveall")]
prev = None
for f in frames[:n]:
    before = [t for t in exp if t["us"] <= f.us and f.us - t["us"] < g.ATTRIBUTE_MS * 1000]
    c = max(before, key=lambda t: t["us"])["kind"] if before else None
    if f.leave_all_types():
        c = "leaveall"
    gap = (f.us - prev.us) / 1000 if prev else None
    print(f"ms {f.ms:6d} us {f.us:12.2f} gap {gap if gap is None else round(gap, 3)} cause {c} LA {sorted(f.leave_all_types())}",
          sorted({e for _, _, e in f.values()}))
    prev = f
