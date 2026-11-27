#!/usr/bin/env python3
"""Probe load baselines and the ceiling control adapter using in-memory mutations."""
import json
import sys
from pathlib import Path
from unittest.mock import patch

repo = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / 'tb/verilator/ctrl_service_budget'))
import load_grade as lg
import flip_grade as fg

out = {'head': '3181a3ec372b6473175cc1c842ada8133a96b127', 'loads': {}}
for point in ['1x1/1if', '8x8/1if']:
    terms = lg.load(repo, point, lg.STATED_US)
    with patch.dict(lg.DELIVERY_US, lg.DELIVERY_US_DEAREST):
        dearest = sum(lg.load(repo, point, lg.STATED_US).values())
    out['loads'][point] = {'terms': terms, 'total': sum(terms.values()), 'dearest_total': dearest,
                           'without_deliveries': sum(terms.values()) - terms['deliveries']}
out['ceiling_077'] = fg.findings(repo, ceiling={'8x8/1if': 0.77})
out['ceiling_078'] = fg.findings(repo, ceiling={'8x8/1if': 0.78})
out['control_baseline_escapes'] = fg.controls(repo)
assert not out['control_baseline_escapes']
assert out['ceiling_077'] and not out['ceiling_078']

# An unchanged 1if ceiling isolates the renamed fixed-ceiling control.
with patch.dict(fg.FLIP, {'8x8/2if': 0.71}):
    escapes = fg.controls(repo)
    checks = fg.flip_checks()
    out['mutant_2if_ceiling_071'] = {'escapes': escapes, 'failed_adapter_checks': [c for c in checks if not c[1]],
                                    'adapter_check_count': len(checks)}
    assert escapes
    assert not out['mutant_2if_ceiling_071']['failed_adapter_checks'], out

# Exercise exactly the stale-name dispatch with one returned failed control.
name = 'the flip ceilings not 0.70 at 8x8/2if and 0.78 at 8x8/1if'
with patch.object(fg, 'controls', return_value=[name]):
    out['injected_failed_control'] = {'name': name, 'failed_checks': [c for c in fg.flip_checks() if not c[1]]}
print(json.dumps(out, indent=2))
