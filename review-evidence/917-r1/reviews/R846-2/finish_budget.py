"""Finish uncompleted independent mutation cases from budget.log.
Usage: python3 -B finish_budget.py CHECKOUT PACKET
The baseline and every remaining mutation use the repository's checks.
"""
import os
import sys
from pathlib import Path

root, packet = (Path(x).resolve() for x in sys.argv[1:3])
os.environ['TMPDIR'] = str(packet / 'scratch/budget')
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import selftest as st
import grade

earlier = (packet / 'budget.log').read_text()
assert not any(line.startswith(('FAIL:', 'MUTANT ESCAPED:')) for line in earlier.splitlines())
caught = [name for name in st.selftest_mutants.MUTANTS if 'MUTANT caught: ' + name + ':' in earlier]
remaining = [name for name in st.selftest_mutants.MUTANTS if name not in caught]
print(f'Interrupted run: {len(caught)} independent mutations caught; {len(remaining)} remaining', flush=True)
bad = [(n, detail) for n, ok, detail in st.checks() if not ok]
assert not bad, bad
print('Fresh baseline: PASS', flush=True)
for name in remaining:
    with st.mutated(name):
        try:
            failed = [(n, detail) for n, ok, detail in st.checks() if not ok]
        except (grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as error:
            failed = [(f'refused: {error}', '')]
    assert failed, name
    print(f'MUTANT caught: {name}: {failed[0][0]}', flush=True)
print(f'Combined: {len(caught) + len(remaining)}/{len(st.selftest_mutants.MUTANTS)} independent mutations caught', flush=True)
