#!/usr/bin/env python3
"""Compare an independent capture re-run's CAPTURE rows with the receipt's rows.
Usage: compare_capture_rows.py <repo> <capture.log> <shape> <cpu_hz> <traffic>"""
import json, re, sys
from pathlib import Path
repo, log, shape, cpu, traffic = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5]
rc = json.loads((repo / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
arm = [m for m in rc['measurements'] if (m['shape'], m['cpu_hz'], m['traffic']) == (shape, cpu, traffic)][0]
rows = {r['index']: r for r in arm['rows']}
got = {}
for line in log.read_text(errors='replace').splitlines():
    if line.startswith('CAPTURE index='):
        kv = dict(t.split('=') for t in line.split()[1:])
        got[int(kv['index'])] = {k: int(v) for k, v in kv.items()}
same = 0
for i, g in sorted(got.items()):
    r = rows[i]
    keys = ['ok', 'sys_cycles', 'raw', 'records', 'mismatches', 'open'] + (['requests', 'responses', 'reads'] if traffic == 'off' else [])
    eq = all(g[k] == r[k] for k in keys)
    same += eq
    print(f"index {i}: rerun sys_cycles={g['sys_cycles']} receipt={r['sys_cycles']} {'EQUAL' if eq else 'DIFFERENT'}"
          + ('' if traffic == 'off' else f" (traffic counters rerun {g['requests']}/{g['responses']}/{g['reads']}, receipt {r['requests']}/{r['responses']}/{r['reads']})"))
print(f"{same} of {len(got)} re-run captures equal the receipt's rows (receipt has {len(rows)})")
sys.exit(0 if got and same == len(got) else 1)
