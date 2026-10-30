#!/usr/bin/env python3
"""Exercise saved-result boundary cases through the real point and regrade paths."""
import importlib.util
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
path = root/'tb/verilator/ctrl_split_boot/run.py'
spec = importlib.util.spec_from_file_location('boot_edges', path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
shape = 'endstation_ax7101_1x1_tdm8'
cases = {
    'positive': (0, m.PASSED, False),
    'nonzero-valid-tally': (7, m.PASSED, True),
    'failed-tally-exit-zero': (0, m.FAILED, True),
    'no-tally': (0, '', True),
    'zero-checks': (0, '== ctrl_split_boot: checks: 0   failures: 0 ==\nRESULT: PASS\n', True),
    'truncated-tally': (0, '== ctrl_split_boot: checks: 1   failures:', True),
    'failure-marker': (0, '  [FAIL] boundary failure\n'+m.PASSED, True),
}
for name, (status, ending, fail) in cases.items():
    out = packet/'scratch/native-edges'/name
    out.mkdir(parents=True, exist_ok=True)
    model = m.stand_in(out, shape, 1, m.Control(status, ending, True, '', ''))
    normal, _ = m.point(out, shape, 1, False, model=model)
    regrade, _ = m.point(out, shape, 1, True)
    assert bool(normal) == fail and bool(regrade) == fail, (name,normal,regrade)
    assert normal == regrade, (name,normal,regrade)
    assert not normal or all(x.startswith('NATIVE:') for x in normal)
    print(name, 'normal/regrade', m.verdict(normal), normal, flush=True)
out = packet/'scratch/native-edges/positive'
(out/m.STATUS).write_text('invalid status\n')
findings, _ = m.point(out, shape, 1, True)
assert m.verdict(findings) == 'NATIVE'
print('invalid saved status rejected', findings)
print('PASS: 8 native boundary probes')
