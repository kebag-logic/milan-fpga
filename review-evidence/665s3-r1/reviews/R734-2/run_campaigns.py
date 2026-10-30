#!/usr/bin/env python3
"""Run four firmware self-test shards concurrently; retain commands, output and status."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
def run(n):
    name = f'firmware-shard{n}'
    cmd = [sys.executable, '-B', str(root/'sw/firmware/ctrl/test/test_ctrl_firmware.py'),
           '--require-rv32', '--self-test', '--shard', f'{n}/4', '--jobs', '2',
           '--build-dir', str(packet/'scratch'/name)]
    (packet/f'{name}.command').write_text(repr(cmd)+'\n')
    with (packet/f'{name}.log').open('w') as log:
        rc = subprocess.run(cmd, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    (packet/f'{name}.rc').write_text(str(rc)+'\n')
    print(name, rc, flush=True)
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, range(4)))
sys.exit(any(results))
