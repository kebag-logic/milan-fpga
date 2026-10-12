#!/usr/bin/env python3
"""Assert the three historical lane references; list the retained 50,267 uses."""
import json
import re
import subprocess
import sys

repo, rev = sys.argv[1:3]

def show(path):
    return subprocess.check_output(['git', '-C', repo, 'show', f'{rev}:{path}'], text=True)

plan = show('docs/design/MARK_II_AREA_PLAN.md')
record = json.loads(show('syn/ooc/pp_resource_baseline.json'))['endpoints']['route-1x1']['record']['figures']
assert record['LUT'] == 50013
failures = []
for lane in ('M2', 'M5', 'M6'):
    section = plan.split(f'### {lane} intermediate measurement\n', 1)[1].split('\n### ', 1)[0].split('\n## ', 1)[0]
    if lane in ('M2', 'M5'):
        required = [
            "The base route equals #645/#647's `route-1x1` record, the gate record at dev `e8454e27`, in every gated figure;",
            "'s 50,013-LUT re-record has since replaced it.",
            f"Against that record, the {lane} route passes with no failing endpoint; it also passes against #696's record.",
        ]
    else:
        required = ["Against #645/#647's record, the M6 route passes with no failing endpoint; it also passes against #696's record."]
    required.append(f'{lane} does not re-record the gate under D7.')
    missing = [s for s in required if s not in section]
    if missing:
        failures.append(lane)
        print('FAIL', lane, 'missing historical-record qualifier or lane-scoped no-re-record sentence')
    else:
        print('PASS', lane, 'historical comparison and current-record pass are separately stated')

bad = re.findall(r'^.*(?:base route equals the `route-1x1` record|accepted 50,267-LUT route remains the comparison record).*$'
                 , plan, re.M | re.I)
if bad:
    failures.append('unqualified record')
    print('FAIL unqualified current-record identity:', *bad, sep='\n')
for n, line in enumerate(plan.splitlines(), 1):
    if '50,267' in line or '50,013' in line:
        print(f'CONTEXT {n}: {line}')
print('NOTE: retained planning-baseline residue is reviewed in its dated section, not asserted as the live gate record.')
print('RESULT:', 'FAIL' if failures else 'PASS')
sys.exit(int(bool(failures)))
