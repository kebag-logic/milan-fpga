#!/usr/bin/env python3
"""Focused ledger and boot native-grader controls; no full banks."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
root = Path.cwd()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
commands = {
    'ledger-controls': [sys.executable, '-B', '-c', '''
import sys
from pathlib import Path
sys.path.insert(0, 'sw/litex')
import test_ctrl_memory as t
p = Path(sys.argv[1]); p.mkdir(parents=True, exist_ok=True)
problems = []
t.ledger_arms(problems, p)
t.ledger_plant_arms(problems, p, {'checks'})
for problem in problems: print('FAIL:', problem)
print('ledger controls failures:', len(problems))
sys.exit(bool(problems))
''', str(scratch / 'ledger-controls')],
    'native-controls': [sys.executable, '-B', 'tb/verilator/ctrl_split_boot/run.py',
                        '--build-dir', str(scratch / 'native-controls'), '--native-controls'],
}
def run(item):
    name, cmd = item
    with (packet / f'{name}.log').open('w') as sink:
        r = subprocess.run(cmd, env=env, stdout=sink, stderr=subprocess.STDOUT)
    (packet / f'{name}.rc').write_text(str(r.returncode) + '\n')
    return name, r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, commands.items()))
print(results)
sys.exit(any(rc for _, rc in results))
