"""The same mixed-point pass as record_classes_mixed_probe.py, graded by the record_classes.py of the bare merge of
#902's 234bc149 (647d5c4a), before the lane's change to its completeness rule (argument: an extracted copy of that
commit's harness dir). That version's main() passes [] where the pass runs no arm A leg at 1x1/1if.
"""
import copy
import sys
from pathlib import Path

HERE = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(HERE))
import record_classes as rc  # noqa: E402

legs1, groups1, stated1 = rc.synthetic()
hz = 100_000_000
arm8 = rc.Leg('8x8/1if', 'none', hz, hz, {'aecp': [rc.Record(0, 24_000, 0x10, 0)]})
ports1 = copy.deepcopy([leg for leg in legs1 if leg.variant == 'answering-ports'])
fan = ports1[0].groups.get('aecp-fanout', [])
ports1[0].groups['aecp-fanout'] = [r for r in fan if r.command != rc.SET_CONFIGURATION]
found, _ = rc.findings([arm8] + ports1, [], lambda point: stated1)
print("647d5c4a's rule, the same 1x1/1if legs beside an 8x8/1if arm A leg: findings", len(found))
for f in found:
    print('  ', f)
