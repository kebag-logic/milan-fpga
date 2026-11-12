#!/usr/bin/env python3
"""Plant reviewer defects into load_grade.py of a scratch tree (argv[1], a git archive of the head) one at a time and
run --selftest and --check; a defect the self-test still passes on (exit 0) escaped."""
import subprocess, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
path = tree / 'tb/verilator/ctrl_service_budget/load_grade.py'
pristine = path.read_text()
PLANTS = [
    ('none', None, None),
    ('the pin column dropped', "COLUMNS = (('at the pin', STATED_US), ('with tsn-c-stack#32', STATED_US_DONOR))",
     "COLUMNS = (('with tsn-c-stack#32', STATED_US_DONOR),)"),
    ('the column not named', "out.append(f'{point}: the load {total:.3f} {name} is over its ceiling {top:.2f}')",
     "out.append(f'{point}: the load {total:.3f} is over its ceiling {top:.2f}')"),
    ('a planted pin column ignored', 'terms = load(root, point, planted[name] or column)',
     'terms = load(root, point, column if name == COLUMNS[0][0] else (planted[name] or column))'),
    ('the pin column graded at the donor ceiling only', 'if total > top:',
     "if total > top and name != 'at the pin':"),
]
for name, old, new in PLANTS:
    text = pristine
    if old:
        assert pristine.count(old) == 1, name
        text = pristine.replace(old, new)
    path.write_text(text)
    st = subprocess.run([sys.executable, '-B', str(path), '--selftest'], capture_output=True, text=True)
    ck = subprocess.run([sys.executable, '-B', str(path), '--check'], capture_output=True, text=True)
    last = (st.stdout.strip().splitlines() or [''])[-1]
    esc = [ln for ln in st.stdout.splitlines() if 'ESCAPED' in ln or 'escaped' in ln.lower()]
    print(f'{name}: selftest rc {st.returncode} ({last}); check rc {ck.returncode}; {esc[:3]}')
path.write_text(pristine)
