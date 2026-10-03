#!/usr/bin/env python3
"""Print each run's start, window and end times (CEST) from runs/*/events.jsonl.
Usage: run_times.py <packet author dir>"""
import json, sys, pathlib, datetime as dt
tz = dt.timezone(dt.timedelta(hours=2))
root = pathlib.Path(sys.argv[1]) / "runs"
def ts(t): return dt.datetime.fromtimestamp(t, tz).strftime("%H:%M:%S.%f")[:-4]
for d in sorted(p for p in root.iterdir() if p.is_dir()):
    ev = [json.loads(l) for l in (d / "events.jsonl").read_text().splitlines() if l.strip()]
    kinds = {}
    for e in ev:
        k = e.get("kind")
        kinds.setdefault(k, []).append(e)
    print(f"== {d.name}: {len(ev)} events, first {ts(ev[0]['t'])} last {ts(ev[-1]['t'])}")
    for e in ev:
        k = e.get("kind")
        if any(s in str(k) for s in ("start", "window", "end", "lock", "grade", "mark", "done", "stop", "set", "unbind", "rebind")):
            extra = {x: e[x] for x in e if x in ("tag", "name", "label", "window_s", "dur_s", "status", "rc", "case", "s", "mark")}
            print(f"  {ts(e['t'])} {k} {json.dumps(extra)[:160]}")
