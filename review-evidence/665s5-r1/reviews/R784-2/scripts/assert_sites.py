#!/usr/bin/env python3
"""For each mutant: the source line of the assertion that failed its named check. Then each expect() no mutant fires."""
import sys, re, inspect, traceback
from contextlib import ExitStack
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_hooks'))
import hooks_selftest as s
src = Path(s.__file__).read_text().splitlines()
def site(check):
    try:
        check(); return None
    except BaseException as e:
        fr = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == s.__file__ and f.name != 'expect']
        return (type(e).__name__, fr[-1].lineno if fr else 0)
fired = {}
for name, make, named in s.MUTANTS:
    with ExitStack() as st:
        st.enter_context(make())
        got = site(s.CHECKS[named])
    fired.setdefault(got[1] if got else None, []).append(name)
    print(f'{got} [{named}] {name}\n    L{got[1] if got else 0}: {src[got[1]-1].strip()[:120] if got else ""}')
print('\n== expect() lines in checks that no mutant fires ==')
for cname, fn in s.CHECKS.items():
    lines, start = inspect.getsourcelines(fn)
    for n, text in enumerate(lines, start):
        if re.match(r'\s+expect\(', text) and n not in fired:
            print(f'L{n} [{cname}] {text.strip()[:125]}')
