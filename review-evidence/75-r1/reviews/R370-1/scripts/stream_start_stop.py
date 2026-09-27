"""Count talker STREAM_START / STREAM_STOP increments across each 100-cycle series.

usage: stream_start_stop.py <packet author dir>
Uses only the public setup/restore snapshots (which bracket every numbered
cycle) and the five public per-cycle snapshots. Counter indices follow the
STREAM_OUTPUT layout: 0 = STREAM_START, 1 = STREAM_STOP.
"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
def counters(path, role, what):
    for line in open(path):
        r = json.loads(line)
        if r.get('role') == role and r.get('what') == what:
            return r['response']['counters']
    raise SystemExit(f'missing {role} {what} in {path}')
series = {'talker': ('dut', 'counter-6-1', 'DUT Stream Output 1 (DUT talker)'),
          'listener': ('peer', 'counter-6-2', 'reference Stream Output 2 (talker feeding the DUT)')}
for d, (role, what, label) in series.items():
    s_after = counters(root / f'{d}-setup/snapshot-after.jsonl', role, what)
    r_before = counters(root / f'{d}-restore/snapshot-before.jsonl', role, what)
    r_after = counters(root / f'{d}-restore/snapshot-after.jsonl', role, what)
    starts = r_before['0'] - s_after['0']; stops = r_before['1'] - s_after['1']
    print(f'{d} series, {label}:')
    print(f'  after initial bind START={s_after["0"]} STOP={s_after["1"]}; before restore START={r_before["0"]} STOP={r_before["1"]}; after restore STOP={r_after["1"]}')
    print(f'  increments spanning numbered cycles 1..100: START +{starts}, STOP +{stops} (100 expected for 100 stop/restart cycles)')
    for n in range(1, 6):
        b = counters(root / f'{d}-{n:03d}/snapshot-before.jsonl', role, what)
        a = counters(root / f'{d}-{n:03d}/snapshot-after.jsonl', role, what)
        print(f'  public cycle {n}: START +{a["0"] - b["0"]} STOP +{a["1"] - b["1"]}')
