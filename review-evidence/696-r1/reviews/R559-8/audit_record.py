#!/usr/bin/env python3
"""Check record-only changes and all current inventory table cells."""
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
path = 'syn/ooc/pp_resource_baseline.json'
before = json.loads(subprocess.check_output(['git', '-C', str(root), 'show', '09c7231e:' + path]))
after = json.loads((root / path).read_text())
changes = []
def walk(a, b, keys):
    if isinstance(a, dict) and isinstance(b, dict):
        assert a.keys() == b.keys(), keys
        for key in a:
            walk(a[key], b[key], keys + [key])
    elif a != b:
        assert 'record' in keys or keys[-1] == 'measured', keys
        changes.append('.'.join(keys))
walk(before, after, [])
plan = (root / 'docs/design/MARK_II_AREA_PLAN.md').read_text()
section = plan.split('### Current processor inventory', 1)[1].split('\n## ', 1)[0]
rows = re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|', section, re.M)
assert len(rows) == 22
for scope, *figures in rows:
    for endpoint, figure in zip(('route-1x1', 'ooc-1x1', 'ooc-8x8'), figures):
        recorded = after['endpoints'][endpoint]['record']['scopes'][scope]['LUT']
        assert int(figure.replace(',', '')) == recorded, (scope, endpoint, figure, recorded)
print(json.dumps({'policy_unchanged': True, 'changed_record_or_measurement_metadata': changes,
                  'inventory_rows': len(rows), 'inventory_cells_checked': 66,
                  'inventory_differences': 0}, indent=2))
