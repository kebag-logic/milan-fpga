"""Run the round 27 checks of the CPU budget harness self-test (answer_checks for #882, ceiling_checks for the load
gate and the flip check) once, then each round 27 mutant (names starting answers:/run:/scenario:/flip:/load:) against
only those checks. Usage: python3 -I selftest_r27_subset.py <repo>"""
import sys
from pathlib import Path
here = Path(sys.argv[1]).resolve() / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(here))
import selftest as st
import selftest_mutants
def subset():
    return [*st.ceiling_checks(), *st.answer_checks(st)]
fails = 0
base = subset()
for n, ok, d in base:
    print(('PASS' if ok else 'FAIL') + ': ' + n + ('' if ok else ': ' + d[:200]))
    fails += not ok
names = [n for n in selftest_mutants.MUTANTS if n.split(':')[0] in ('answers', 'run', 'scenario', 'flip', 'load')]
for name in names:
    with st.mutated(name):
        try:
            failed = [(n, d) for n, ok, d in subset() if not ok]
        except Exception as e:  # a refusal counts as caught, as selftest.main counts it
            failed = [(f'refused: {e}', '')]
    print(('MUTANT caught: ' if failed else 'MUTANT ESCAPED: ') + name + (f': {failed[0][0]}' if failed else ''))
    fails += not failed
print(f'subset: {len(base)} checks, {len(names)} mutants, {fails} failures')
sys.exit(1 if fails else 0)
