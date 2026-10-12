#!/usr/bin/env python3
"""Attribute each row's maximum notification gap in an instrumented
stream_counters run.log (EV/ELIG/WATCH_OFF/SERVICE lines) to the measured
window or to the post-window tail. Usage: gap_attribution.py <run.log> <cycles_per_ms>"""
import sys
from collections import defaultdict

log, cyc_ms = sys.argv[1], float(sys.argv[2])
ev = defaultdict(list)
service = {}
watch_off = None
for line in open(log):
    p = line.strip().split(",")
    if p[0] == "EV":
        ev[(int(p[1]), int(p[2]), int(p[3]))].append(int(p[4]))
    elif p[0] == "WATCH_OFF":
        watch_off = int(p[1])
    elif p[0] == "SERVICE":
        service[int(p[1])] = int(p[2])
n_streams = max(s for (_, s, _) in ev) if ev else 0
print(f"watch_off_cycle={watch_off}")
print("type,index,recipient,max_gap_ms,max_gap_ends_after_watch_off,max_in_window_gap_ms,service_ms,bound_ms,full_ok,in_window_ok")
for (ty, s, r), ts in sorted(ev.items()):
    ts = sorted(ts)
    gaps = [(b - a, b) for a, b in zip(ts, ts[1:])]
    if not gaps:
        continue
    g, end = max(gaps)
    inwin = [x for x, e in gaps if watch_off is None or e <= watch_off]
    slot = (0 if ty == 5 else n_streams + 1) + s
    sv = service.get(slot, 0)
    bound = 1000 * cyc_ms + sv
    print(f"{ty},{s},{r},{g/cyc_ms:.3f},{int(watch_off is not None and end > watch_off)},"
          f"{(max(inwin)/cyc_ms if inwin else 0):.3f},{sv/cyc_ms:.3f},{bound/cyc_ms:.3f},"
          f"{int(g <= bound)},{int((max(inwin) if inwin else 0) <= bound)}")
