#!/usr/bin/env python3
"""Focused in-memory probes. Usage: python3 -B probe_model.py SOURCE_ROOT."""
import contextlib
import io
import json
import sys
from pathlib import Path
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import load_grade as load
import flip_grade as flip
import load_deliveries

def failed(rows):
    return [list(row) for row in rows if not row[1]]

out = {'head_controls': flip.controls(root),
       'head_flip_failures': failed(flip.flip_checks()),
       'head_ceiling_failures': failed(load.ceiling_checks()),
       'delivery_controls': load_deliveries.controls(root)}
assert all(not v for v in out.values()), out
with patch.dict(flip.FLIP, {'8x8/2if': 0.71}):
    out['ceiling_071'] = {'controls': flip.controls(root),
                          'flip_checks': failed(flip.flip_checks()),
                          'ceiling_checks': failed(load.ceiling_checks())}
assert all(out['ceiling_071'].values())
with patch.object(flip, 'controls', return_value=['independent unknown failure']):
    out['unknown_flip'] = failed(flip.flip_checks())
    out['unknown_flip_through_load'] = failed(load.ceiling_checks())
with patch.object(load, 'controls', return_value=['independent unknown failure']):
    out['unknown_load'] = failed(load.ceiling_checks())
assert all(out[k] for k in ('unknown_flip', 'unknown_flip_through_load', 'unknown_load'))
out['loads'] = {}
for point in ('1x1/1if', '8x8/1if'):
    terms = load.load(root, point, load.STATED_US)
    out['loads'][point] = {'total': sum(terms.values()), 'deliveries': terms['deliveries'],
                         'V': load.record_values(point, root), 'statement_us': load.DELIVERY_US[point],
                         'floor_us': load.rule_us(load.DELIVERY_MEASURED[point])}
out['proposed_ceiling_findings'] = flip.findings(root, ceiling={'8x8/1if': 0.79})
out['approved_ceiling_findings'] = flip.findings(root, ceiling={'8x8/1if': 0.77})
assert not out['proposed_ceiling_findings'] and out['approved_ceiling_findings']
out['edge_0790_pass'] = not flip.over(0.790, 0.79)
out['edge_0791_fail'] = flip.over(0.791, 0.79)
assert out['edge_0790_pass'] and out['edge_0791_fail']
with patch.dict(load.DELIVERY_US, {'8x8/1if': 155}):
    out['delivery_155'] = load.delivery_findings(root)
    buf = io.StringIO()
    with patch.object(sys, 'argv', ['load_grade.py', '--check']), contextlib.redirect_stdout(buf):
        out['delivery_155_cli_rc'] = load.main()
    out['delivery_155_cli_output'] = buf.getvalue()
assert out['delivery_155'] and out['delivery_155_cli_rc'] == 1
with patch.dict(load.DELIVERY_US, {'1x1/1if': 195}):
    out['delivery_195'] = load.delivery_findings(root)
assert out['delivery_195']
print(json.dumps(out, indent=2))
