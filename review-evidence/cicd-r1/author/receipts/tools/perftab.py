#!/usr/bin/env python3
"""perftab.py DIR...: one row per perf-stat CSV (DIR/perf) with time, IPC and miss rates."""
import sys
from pathlib import Path


def read(path):
    v = {}
    for line in Path(path).read_text().splitlines():
        f = line.split(',')
        if len(f) > 3 and f[0] and f[0][0].isdigit():
            v[f[2].replace(':u', '')] = float(f[0])
    return v


def row(name, v, t):
    cyc, ins = v.get('cycles', 0), v.get('instructions', 0)
    l1 = v.get('L1-dcache-load-misses', 0) / max(v.get('L1-dcache-loads', 1), 1) * 100
    cm = v.get('cache-misses', 0) / max(v.get('cache-references', 1), 1) * 100
    br = v.get('branch-misses', 0) / max(v.get('branches', 1), 1) * 100
    return (f"| {name} | {t} | {v.get('task-clock', 0)/1000:.0f} | {ins/1e12:.2f} | {cyc/1e12:.2f} | "
            f"{ins/max(cyc,1):.2f} | {v.get('L1-dcache-load-misses',0)/1e9:.2f} ({l1:.3f} %) | "
            f"{v.get('cache-misses',0)/1e6:.0f} ({cm:.2f} %) | {v.get('L1-icache-load-misses',0)/1e6:.0f} | "
            f"{v.get('branch-misses',0)/1e9:.2f} ({br:.2f} %) |")


print('| run | wall s | CPU s | instr T | cycles T | IPC | L1d misses G (rate) | cache-misses M (rate) '
      '| L1i misses M | branch misses G (rate) |')
print('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for d in sys.argv[1:]:
    p = Path(d)
    perf = p / 'perf' if (p / 'perf').exists() else p
    t = '?'
    tf = p / 'time' if p.is_dir() else Path(str(p).replace('.perf', '.time'))
    if tf.exists():
        w = tf.read_text().split()
        t = next((w[i - 1] for i, x in enumerate(w) if x == 'wall'), '?')
    print(row(str(d).replace('/data-2/milan/tmp/cicd-a839/', ''), read(perf), t))
