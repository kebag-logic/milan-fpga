#!/usr/bin/env python3
"""Print the DUT commands of B0's window-mark-1 from runs/b0/ctl.jsonl (command, descriptor type and
index, status, CEST time) and count every DUT AECP command and non-SUCCESS answer over all runs.
usage: b0_timeout_record.py <packet author dir>"""
import json, glob, sys, datetime as dt
root = sys.argv[1]
tz = dt.timezone(dt.timedelta(hours=2))
f = lambda t: dt.datetime.fromtimestamp(t, tz).strftime('%H:%M:%S.%f')[:-3]
NAMES = {0x05: 'STREAM_INPUT', 0x06: 'STREAM_OUTPUT', 0x24: 'CLOCK_DOMAIN'}  # IEEE 1722.1 Table 7.1
L = [json.loads(l) for l in open(f'{root}/runs/b0/ctl.jsonl')]
for x in L:
    ln = x.get('line', {})
    if ln.get('role') == 'dut' and ln.get('cmd') == 'GET_COUNTERS' and 1791033650 < ln.get('t_tx', 0) < 1791033670:
        _, _, dt_, idx = ln['what'].split('-')
        print(f'{f(ln["t_tx"])} tx -> {f(ln["t_rx"])} rx  GET_COUNTERS {NAMES.get(int(dt_), dt_)} {idx} ({ln["what"]})  {ln["status"]}')
tot = bad = 0
for p in sorted(glob.glob(f'{root}/runs/*/ctl.jsonl')):
    for l in open(p):
        ln = json.loads(l).get('line', {})
        if 'cmd' in ln and ln.get('role') == 'dut':
            tot += 1
            if ln.get('status') != 'SUCCESS':
                bad += 1
                print('non-SUCCESS:', p.split('/runs/')[1], ln['cmd'], ln['what'], ln['status'])
print(f'DUT AECP commands over all runs: {tot}; non-SUCCESS: {bad}')
