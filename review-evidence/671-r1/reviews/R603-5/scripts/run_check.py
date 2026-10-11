#!/usr/bin/env python3
"""Run one scoped review check in the foreground and retain its receipt."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('root', type=Path)
p.add_argument('check', choices=['writer', 'cosim', 'capture', 'docs'])
p.add_argument('--simulator', type=Path)
a = p.parse_args()
packet = Path(__file__).resolve().parents[1]
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1')
if a.simulator:
    env['PATH'] = str(a.simulator.parent) + os.pathsep + env['PATH']
commands = {
    'writer': [[sys.executable, '-B', 'sw/firmware/nvm_hosttest/test_nvm_firmware.py', '--self-test', '--jobs', '8']],
    'cosim': [[sys.executable, '-B', str(packet / 'scripts/cosim_scoped.py'), str(a.root), str(scratch / 'cosim')]],
    'capture': [[sys.executable, '-B', 'scripts/check_nvm_capture.py']],
    'docs': [[sys.executable, '-B', 'scripts/docs_check.py']],
}[a.check]
log = packet / 'receipts' / (a.check + '.log')
start = time.monotonic()
rc = 0
with log.open('w') as out:
    for command in commands:
        print('COMMAND:', ' '.join(command), file=out, flush=True)
        result = subprocess.run(command, cwd=a.root, env=env, stdout=out, stderr=subprocess.STDOUT)
        rc = result.returncode
        if rc:
            break
    print(f'RETURN_CODE={rc}\nELAPSED_SECONDS={time.monotonic()-start:.3f}', file=out)
(packet / 'receipts' / (a.check + '.rc')).write_text(str(rc) + '\n')
print(f'{a.check}: rc={rc}, seconds={time.monotonic()-start:.3f}, receipt={log.name}')
sys.exit(rc)
