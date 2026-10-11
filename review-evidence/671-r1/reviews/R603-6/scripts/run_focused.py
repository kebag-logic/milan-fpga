#!/usr/bin/env python3
"""Run focused source checks concurrently, retaining logs and exit statuses."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('root', type=Path)
p.add_argument('packet', type=Path)
a = p.parse_args()
root, packet = a.root.resolve(), a.packet.resolve()
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1')
commands = {
    'writer': [sys.executable, 'sw/firmware/nvm_hosttest/test_nvm_firmware.py', '--self-test', '--jobs', '4'],
    'capture': [sys.executable, 'scripts/check_nvm_capture.py'],
}
def run(item):
    name, cmd = item
    start = time.monotonic()
    with (packet / 'receipts' / (name + '.log')).open('w') as log:
        print('COMMAND:', ' '.join(cmd), file=log, flush=True)
        r = subprocess.run(cmd, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=1200)
        print('EXIT:', r.returncode, 'ELAPSED_SECONDS:', round(time.monotonic()-start, 2), file=log)
    (packet / 'receipts' / (name + '.rc')).write_text(str(r.returncode)+'\n')
    print(name, r.returncode, flush=True)
    return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    statuses = list(pool.map(run, commands.items()))
sys.exit(any(statuses))
