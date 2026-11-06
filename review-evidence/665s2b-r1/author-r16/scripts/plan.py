#!/usr/bin/env python3
"""A leg's LONG and REST group lists (#665): its groups by round 15's durations, the longest n LONG.
usage: plan.py LEG all|LIST n POINT -> prints LONG then REST, one comma list a line"""
import json, sys
sys.path.insert(0, '$VALIDATION_STORAGE/665s2b-a683u/C/tb/verilator/ctrl_service_budget')
import scenario, run  # noqa: E402
leg, wanted, n, point = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
dur = json.load(open('$VALIDATION_STORAGE/665s2b-a683u/r15-durations.json'))
ref = {'N-A8': 'N-A8', 'N-B8': 'N-B8', 'D-A8': 'D-A8', 'D-B8': 'D-B8p', 'N-A1': 'N-A1', 'N-B1': 'N-B1p',
       'D-A1': 'D-A1p', 'D-B1': 'D-B1p', 'AH-A8': 'AH-A8'}[leg]
if wanted == 'all':
    spec = json.load(open(f'$VALIDATION_STORAGE/665s2b-a683r/builds/{ref}/build.json'))
    names = [g.name for g in scenario.all_groups(scenario.point(point, spec), spec)]
else:
    names = wanted.split(',')
d = dur.get(ref, {})
order = sorted(names, key=lambda g: -d.get(g, 0))
print(','.join(order[:n]))
print(','.join(order[n:]))
