"""Per half and application: LeaveAll frames, omitted declared values at them, full ones, the least spare room."""
import sys
from pathlib import Path
sys.path.insert(0, ".")
import twin_decode as td, twin_mrp as tm
for name in ("fabric", "split"):
    cap = td.load(Path(sys.argv[1]) / f"{name}.json")
    for app in tm.APPLICATIONS:
        frames = cap.frames.get(app, [])
        la = [s for s in frames if tm.frame_events(app, s)[1]]
        spare = [tm.MRPDU_ROOM - tm.mrpdu_octets(app, s) for s in la]
        obs = tm.observations(cap, app)
        omitted = sum(1 for seen in obs.values() for x in seen if x.leave_all and x.sent is None)
        full = sum(1 for seen in obs.values() for x in seen if x.full)
        g = tm.grade(cap, app)
        print(f"{cap.placement} {app}: frames={len(frames)} leaveall_frames={len(la)} omissions_at_leaveall={omitted} "
              f"full={full} least_spare_octets={min(spare) if spare else None} largest_mrpdu={max((tm.mrpdu_octets(app,s) for s in frames), default=0)} findings={len(g.findings)}")
