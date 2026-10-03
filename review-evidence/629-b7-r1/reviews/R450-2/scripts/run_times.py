#!/usr/bin/env python3
"""Print run start, window start/end, DUT clock set and end in CEST from each runs/<case>/events.jsonl.
Event payloads are not printed (they carry the peer's descriptor indices).
usage: run_times.py <packet author dir>"""
import json, sys, datetime as dt
root = sys.argv[1]
tz = dt.timezone(dt.timedelta(hours=2))
f = lambda t: dt.datetime.fromtimestamp(t, tz).strftime('%H:%M:%S.%f')[:-3]
for r in ['smoke-baaf', 'a0', 'a1', 'a2', 'b0', 'bcrf', 'baaf', 'probe']:
    for l in open(f'{root}/runs/{r}/events.jsonl'):
        x = json.loads(l)
        k = x.get('kind')
        if k in ('start', 'end', 'window-start', 'window-end', 'servo-lock', 'll-unbind', 'll-rebind') or (k == 'set-clock' and x.get('who') == 'dut'):
            print(f'{r:10s} {f(x["t"])} {k}' + (f' src={x.get("src")} tag={x.get("tag")}' if k == 'set-clock' else ''))
