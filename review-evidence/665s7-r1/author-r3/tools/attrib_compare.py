"""attrib_compare.py OLD_GRADE_DIR TREE CAPTURE...: each graded MRPDU's cause under the time-window attribution
the grade had at 2131eff4 (its causes(), OLD_GRADE_DIR/srptx_grade.py, its decoder import from TREE) beside what
the bench recorded lwSRP did at the poll that sent it (after_join, idle_us); prints every frame where the two
differ, and counts. Frames sent at a periodic tick are named so from the old cause."""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[2]) / "sw/firmware/ctrl/test"))
sys.path.insert(0, sys.argv[1])
import srptx_grade as g  # noqa: E402

for path in sys.argv[3:]:
    cap = g.load(Path(path))
    accepted = [e for e in cap.doc["lib"] if e["rc"] == 0]
    rec = {}
    for f, a in zip(cap.mrpdus, accepted):
        if f.frame[14:14 + len(a["hex"]) // 2].hex() == a["hex"]:
            rec[id(f)] = a
    print(f"== {Path(path).name}")
    for proto in g.APPLICATIONS:
        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        cause = g.causes(cap, proto, frames)
        n = Counter()
        for k, (f, c) in enumerate(zip(frames, cause)):
            a = rec.get(id(f), {})
            old = c[0] if c else None
            la = bool(f.leave_all_types())
            new = "leaveall" if la else "join" if a.get("after_join") else "not join"
            idle = a.get("idle_us", -1)
            n[(old, new)] += 1
            if (old == "join") != (new == "join") and not la:
                gap = (f.us - frames[k - 1].us) / 1000 if k else None
                print(f"  {proto} ms {f.us / 1000:.3f}: old {old} ({(c[1]['us'] / 1000) if c else '-'}), new {new}, "
                      f"after_join {a.get('after_join')}, "
                      f"idle {idle / 1000 if idle >= 0 else None}, gap {gap}")
        print(f"  {proto} (old, new) counts: {dict(sorted(n.items(), key=str))}")
        req = [(f.us / 1000, (f.us - rec[id(f)]["idle_us"]) / 1000) for f in frames
               if id(f) in rec and rec[id(f)]["idle_us"] >= 0]
        print(f"  {proto} frames with idle_us: {len(req)}; egress - idle max "
              f"{max((r[1] for r in req), default=None)}; top 5 {sorted(req, key=lambda r: -r[1])[:5]}")
