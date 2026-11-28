#!/usr/bin/env python3
"""Focused model/edge/floor probes; mutations are in-process only."""
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import flip_grade as flip
import load_grade as load

assert flip.FLIP == flip.RULED_FLIP == {'8x8/2if': .70, '8x8/1if': .79}
assert flip.EDGE_1IF == (.790, .791)
assert not flip.over(.790, .79) and flip.over(.791, .79)
result = {'ceilings': flip.FLIP.copy(), 'edges': {'0.790_over': flip.over(.790, .79),
    '0.791_over': flip.over(.791, .79)}, 'points': {}}
for point, expected in [('8x8/1if', .7821365), ('1x1/1if', .5325402076023392)]:
    terms = load.load(ROOT, point, load.STATED_US)
    total = sum(terms.values())
    assert abs(total - expected) < 1e-12
    assert terms['deliveries'] == load.DELIVERY_US[point] * 3 * load.record_values(point, ROOT) / 270000
    old = load.DELIVERY_US[point]
    load.DELIVERY_US[point] = old - 5
    floors = load.delivery_findings(ROOT)
    load.DELIVERY_US[point] = old
    assert any(point in f and 'under' in f for f in floors)
    result['points'][point] = {'load_at_pin': total, 'rounded_5dp': f'{total:.5f}',
        'without_deliveries': total - terms['deliveries'], 'terms': terms, 'lower_floor_refused': floors}
assert not flip.findings(ROOT, ceiling={'8x8/1if': .79})
result['former_077_refusal'] = flip.findings(ROOT, ceiling={'8x8/1if': .77})
assert result['former_077_refusal']
result['normal_failed_adapters'] = [x for x in flip.flip_checks() + load.ceiling_checks() if not x[1]]
assert not result['normal_failed_adapters']
flip.FLIP['8x8/1if'] = .77
result['lowered_ceiling_escapes'] = flip.controls(ROOT)
assert flip.CEILINGS_CONTROL in result['lowered_ceiling_escapes']
assert flip.EDGE_CONTROL in result['lowered_ceiling_escapes']
flip.FLIP['8x8/1if'] = .79
(OUT / 'model-probe.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: 0.78214 / 0.53254; 0.790 accepted / 0.791 refused; floors and malformed ceiling refused')
