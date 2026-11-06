#!/usr/bin/env python3
"""Run the hook harness's self-test and print, per mutant, why its named check failed and which checks failed."""
import sys, json
from contextlib import ExitStack
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_hooks'))
import hooks_selftest as s
base = s.run_checks()
print('BASE', sum(v is None for v in base.values()), 'of', len(base))
out = []
for name, make, named in s.MUTANTS:
    with ExitStack() as st:
        st.enter_context(make())
        got = s.run_checks()
    failed = {k: v for k, v in got.items() if v}
    why = got[named]
    kind = 'NONE' if why is None else ('RAISED' if why.split(':')[0].endswith(('Error', 'Exception', 'Iteration', 'Interrupt')) or why.startswith('StopIteration') else 'RULE')
    out.append(dict(mutant=name, check=named, kind=kind, why=why, others=sorted(k for k in failed if k != named)))
    print(f'{kind:6} {name} -> [{named}] {str(why)[:170]} | also: {len(failed)-(why is not None)}')
print('TOTAL', len(out), {k: sum(o['kind'] == k for o in out) for k in ('RULE', 'RAISED', 'NONE')})
json.dump(out, open(sys.argv[2], 'w'), indent=1)
