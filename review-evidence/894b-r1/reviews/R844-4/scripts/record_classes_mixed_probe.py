"""In-process probe of record_classes.py's completeness rule on a pass that mixes points (argument: the harness dir).

The pass: 8x8/1if complete (synthetic_8x8) plus 1x1/1if's answering-ports leg alone, its arm A leg dropped and its
accepted SET_CONFIGURATION removed. The completeness map is built as main() builds it: a point enters it only where
the pass runs arm A there. No file is written.
"""
import copy
import sys
from pathlib import Path

HERE = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(HERE))
import record_classes as rc  # noqa: E402

legs1, groups1, stated1 = rc.synthetic()
legs8, groups8, at8 = rc.synthetic_8x8()
own = {'1x1/1if': stated1, '8x8/1if': at8('8x8/1if')}
ports1 = copy.deepcopy([leg for leg in legs1 if leg.variant == 'answering-ports'])
fan = ports1[0].groups.get('aecp-fanout', [])
ports1[0].groups['aecp-fanout'] = [r for r in fan if r.command != rc.SET_CONFIGURATION]
legs = legs8 + ports1
arm = {leg.point: groups8['8x8/1if'] for leg in legs if leg.point in rc.COMPLETE and leg.variant == 'none'}
found, _ = rc.findings(legs, arm, lambda point: own[point])
print('completeness map built as main() builds it:', sorted(arm))
print('mixed pass, 1x1/1if arm A absent and its SET_CONFIGURATION removed: findings', len(found))
for f in found:
    print('  ', f)
both = dict(arm, **{'1x1/1if': groups1})
found2, _ = rc.findings(legs, both, lambda point: own[point])
print('the same pass held complete at 1x1/1if too: findings', len(found2))
for f in found2[:4]:
    print('  ', f)
only1 = [leg for leg in ports1]
found3, _ = rc.findings(only1, {}, lambda point: own[point])
print('1x1/1if answering-ports alone (no arm A anywhere): findings', len(found3), found3[:1])
