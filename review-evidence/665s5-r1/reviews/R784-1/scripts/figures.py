"""Recompute the README's headline figures from the author's published results.json receipts.
Usage: python3 -I figures.py <receipts/runs dir>"""
import json, sys
from pathlib import Path
runs = Path(sys.argv[1])
R = {d: json.load(open(runs / d / 'results.json')) for d in ('1x1-idle', '1x1-ans', '8x8-idle', '8x8-ans')}
for d, r in R.items():
    rows = r['rows']
    print(f'== {d}: clock={r["clock"]!r} cpu_hz={r["cpu_hz"]} sys_hz={r["sys_hz"]} T_svc={r["t_svc_ms"]} paths={len(rows)} '
          f'refusals={len(r["refusals"])} superseded={len(r["superseded"])} findings={len(r["findings"])} '
          f'LATE={sum(f.startswith("LATE") for f in r["findings"])} NARROW={sum(f.startswith("NARROW") for f in r["findings"])} '
          f'ORDER={sum(f.startswith("ORDER") for f in r["findings"])}')
    for h, s in r['summary'].items():
        w = s['worst']
        fmt = lambda x: None if x is None else ('never' if x['unbounded'] else round(x['ms'], 2), x['probe'], x['within'])
        print(f'  {h:11s} paths={s["paths"]:3d} misses={s["misses"]:2d} alone={fmt(w.get("alone"))} loaded={fmt(w.get("loaded"))} '
              f'applied={s["applied"]} undecided={s["undecided"]} ord={len(s["ordering_findings"])}')
    aecp_last = [x for x in rows if x['hook'] == 'H-AECP' and x['loaded'] and x['probe'].endswith(('.last.if0', '.last.if1'))]
    print('  AECP loaded .last range', min(x['ms'] for x in aecp_last), max(x['ms'] for x in aecp_last))
    owed = [x for x in rows if x['hook'] == 'H-ACMP' and 'owed' in x['probe']]
    print('  ACMP owed rows', [(x['probe'], x['ms'], x['unbounded']) for x in owed])
    srp_starved = [x for x in rows if x['hook'] == 'H-SRP' and x['unbounded']]
    print('  SRP never served', [(x['probe'], x['group'], x['ms']) for x in srp_starved])
    cnt = [x for x in rows if x['hook'] == 'H-COUNTERS']
    print('  COUNTERS', [(x['probe'], x['ms'], x['cpu_cycles'], x['wait_ms']) for x in cnt])
