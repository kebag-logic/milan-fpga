#!/usr/bin/env python3
"""Per half and application: the LeaveAll frames each half sent, the values they leave out, how many of those the
grade reads as full (txLAF! allowed), and the least spare room of any LeaveAll frame.

Usage (from a directory holding tb/verilator/milan_dp's Python files): la_room.py <fabric.json> <split.json>
"""
import sys
from pathlib import Path

import twin_decode as td
import twin_mrp as tm

for path in sys.argv[1:]:
    cap = td.load(Path(path))
    for app in tm.APPLICATIONS:
        frames = cap.frames.get(app, [])
        la = omitted = full = 0
        least = None
        for key, seen in tm.observations(cap, app).items():
            for s in seen:
                if s.leave_all and s.sent is None and not s.got:
                    omitted += 1
                    full += s.full
        for s in frames:
            events, types = tm.frame_events(app, s)
            if types:
                la += 1
                spare = tm.MRPDU_ROOM - tm.mrpdu_octets(app, s)
                least = spare if least is None else min(least, spare)
        print(f"{path} {app}: frames={len(frames)} leaveall_frames={la} omissions={omitted} full={full} "
              f"least_spare_octets={least}")
