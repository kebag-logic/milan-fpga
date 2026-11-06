#!/usr/bin/env python3
"""Run the plant rule on the published unplanted findings, as written and with counters-late's path moved to a row that
already misses, the round 1 defect at path level. Usage: vacuity_probe.py <clone-root> <author-r2 receipts dir>"""
import dataclasses, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
H = Path(sys.argv[1]) / 'tb/verilator/ctrl_service_hooks'
sys.path.insert(0, str(H))
import hooks_selftest as s
found = json.load(open(Path(sys.argv[2]) / 'runs/1x1-ans/results.json'))['findings']
plant = s.hooks.plants()['counters-late'][1]
print('as written, probe', plant.probe, '-> unplanted findings that catch it:', len(s.run.plant_findings(plant, found)))
moved = dataclasses.replace(plant, probe='counters.all.if0')
print('moved to counters.all.if0 -> unplanted findings that catch it:', len(s.run.plant_findings(moved, found)), s.run.plant_findings(moved, found)[:1])
real = s.hooks.plants
s.hooks.plants = lambda: {k: (h, moved if k == 'counters-late' else p) for k, (h, p) in real().items()}
got = s.run_checks()
print('self-test checks failing with the path moved:', {k: v[:90] for k, v in got.items() if v})
