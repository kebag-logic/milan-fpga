import json
import os
import subprocess
import sys
from run_gate import BANK, OUT, ROOT, run

env = os.environ.copy()
for value in json.loads(BANK.read_text())['commands'][0][1:]:
    if '=' not in value:
        break
    key, val = value.split('=', 1)
    env[key] = val
recipe = subprocess.check_output(['make', '-n', '--no-print-directory', '-C', 'tb/verilator/milan_dp', 'run'], cwd=ROOT, env=env, text=True)
commands = recipe.replace('\\\n', ' ').splitlines()
commands = [c for c in commands if c.strip() and not c.startswith('echo ')]
(OUT / 'dp-commands.json').write_text(json.dumps(commands, indent=2)+'\n')
for i, command in enumerate(commands):
    if run(f'dp-{i:02}', ['bash', '-eu', '-c', command], cwd=ROOT / 'tb/verilator/milan_dp'):
        raise SystemExit(1)
