#!/usr/bin/env python3
"""Check each lane's stated route against its dated and current gate records."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location('original', Path(__file__).with_name('record_vs_lane_routes.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
plan = (root/'docs/design/MARK_II_AREA_PLAN.md').read_text()
records = {}
for ref in ('e8454e27', 'HEAD'):
    records[ref] = json.loads(subprocess.check_output(
        ['git','show',ref+':syn/ooc/pp_resource_baseline.json'], cwd=root))['endpoints']['route-1x1']
pat = re.compile(r'^\| (Base route at dev `\w+`|M[256] route at `\w+`) \| ([\d,]+) \| ([\d,]+) \| '
                 r'([\d,]+) \| (\d+) / (\d+) \| ([+-][\d.]+) / ([+-][\d.]+) \|$', re.M)
rows = [(r.group(1),dict(zip(m.FIG,map(m.num,r.groups()[1:])))) for r in pat.finditer(plan)]
assert len(rows)==6
for name, figures in rows:
    if name.startswith('Base'):
        assert all(figures[k] == records['e8454e27']['record']['figures'][k] for k in m.FIG)
        print('PASS historical base matches e8454e27 record:',name)
    else:
        for ref, endpoint in records.items():
            result = m.verdict(figures,endpoint['record']['figures'],endpoint['tolerance'],endpoint['floor'])
            print(name,'against',ref,result)
            assert result == 'PASS'
for lane in ('M2','M5','M6'):
    section=plan.split(f'### {lane} intermediate measurement',1)[1].split('\n### ',1)[0].split('\n## ',1)[0]
    assert '#645/#647' in section and "against #696's record" in section
    assert f'{lane} does not re-record the gate under D7.' in section
    assert 'The base route equals the `route-1x1` record' not in section
    print('PASS comparison wording and no-re-record scope:',lane)
print('PASS lane figures unchanged; historical record 50267, current record 50013')
