import os
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path.cwd() / 'sw/firmware/ctrl/test'))
import ctrl_mutants
import srp_mutants
import test_ctrl_firmware

interfaces, part, count = map(int, sys.argv[1:])
work = Path(os.environ['WORK']) / f'srp-if{interfaces}-{part}'
lwsrp = Path.cwd() / 'third_party/lwSRP'
tables = {}
def record(_root, _lwsrp, _jobs, interfaces=2):
    tables[interfaces] = srp_mutants.DEFECTS
    return False
with patch.object(srp_mutants, 'campaign', record), patch.object(ctrl_mutants, 'lwsrp_pin_arms', return_value=0):
    assert not test_ctrl_firmware.run_srp_mutants(SimpleNamespace(lwsrp=lwsrp,jobs=4),work)
assert len(tables[2]) == 202 and len(tables[1]) == 76
table = tables[interfaces]
batches = [table[k::count] for k in range(count)]
assert sorted(d.name for batch in batches for d in batch) == sorted(d.name for d in table)
assert len({d.name for batch in batches for d in batch}) == len(table)
srp_mutants.DEFECTS = batches[part-1]
failed = srp_mutants.campaign(work,lwsrp,4,interfaces)
if interfaces == 1:
    failed = ctrl_mutants.lwsrp_pin_arms(work / 'pins', lwsrp) != 0 or failed
print(f'SRP IF{interfaces} batch {part}/{count}: {len(srp_mutants.DEFECTS)} plants, failed={failed}',flush=True)
raise SystemExit(failed)
