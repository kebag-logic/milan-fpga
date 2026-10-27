#!/usr/bin/env python3
"""R713-1-F4's verification, with failing words: each reviewer source mutant planted in turn in a
disposable copy of the head's harness, the self-test run, and its FAIL lines printed; the copy
is restored after every mutant. usage: source_mutants.py COPY_ROOT"""
import subprocess
import sys
from pathlib import Path

H = Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'
MUTANTS = [
    ('main reuse refusal removed (run.py:317)', 'run.py',
     '        if built_as(spec) != selected(args, shape, n_if):\n', '        if False:\n'),
    ('build records xip as False (build.py:520)', 'build.py',
     "    spec['xip'] = core.xip\n", "    spec['xip'] = False\n"),
    ('main builds with the default cache, ignoring --fetch-l1 (run.py:321)', 'run.py',
     'core=builder.Core(args.cpu_regions, args.fetch_l1, args.xip))',
     "core=builder.Core(args.cpu_regions, 'split', args.xip))"),
]
for label, name, old, new in MUTANTS:
    f = H / name
    original = f.read_text()
    assert original.count(old) == 1, label
    f.write_text(original.replace(old, new))
    try:
        r = subprocess.run([sys.executable, '-B', 'run.py', '--self-test'], cwd=H, capture_output=True, text=True,
                           timeout=600)
    finally:
        f.write_text(original)
    print(f"{'KILLED' if r.returncode else 'SURVIVED'} {label}: rc={r.returncode}")
    for line in r.stdout.splitlines():
        if line.startswith(('FAIL', 'MUTANT ESCAPED', 'self-test:')):
            print('   ', line[:400])
