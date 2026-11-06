#!/usr/bin/env python3
"""For each self-test mutant, say how its named check failed: on an expect() (its rule) or by an exception (a crash).
Usage: mutant_audit.py <harness-dir>"""
import sys, re
from contextlib import ExitStack
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import hooks_selftest as s
base = s.run_checks()
assert not any(base.values()), base
crash = rule = esc = 0
for name, make, named in s.MUTANTS:
    with ExitStack() as st:
        st.enter_context(make())
        got = s.run_checks()
    why = got[named]
    others = sorted(k for k, v in got.items() if v and k != named)
    kind = 'ESCAPED' if why is None else ('CRASH' if re.match(r'^[A-Za-z]*(Error|Exception|Iteration|Interrupt|Exit)\b.*?:', why) else 'rule')
    crash += kind == 'CRASH'; rule += kind == 'rule'; esc += kind == 'ESCAPED'
    print(f'{kind} | {name} | {named} | {(why or "")[:150]!r} | also: {len(others)}')
print(f'rule {rule} crash {crash} escaped {esc} of {len(s.MUTANTS)}')
