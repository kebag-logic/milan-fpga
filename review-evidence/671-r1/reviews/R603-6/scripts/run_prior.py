#!/usr/bin/env python3
"""Run the two byte-identical public round-five probes concurrently."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
import time
root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
env = dict(os.environ, TMPDIR=str(packet/'scratch'), PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1')
commands = {
    'prior-r603': [sys.executable, '-B', str(packet/'scripts/prior_probe_comparison.py'), str(root), '--jobs', '4'],
    'prior-r602': [sys.executable, '-I', '-B', str(packet/'scripts/prior_probe_r602_5.py'), str(root),
                   str(packet/'scratch/prior-r602'), '--jobs', '4', '--mutants', 'no_tail,digest_short',
                   '--sets', 'none', '--standing'],
}
def run(item):
    label, cmd = item
    begin = time.monotonic()
    with (packet/'receipts'/f'{label}.log').open('w') as log:
        r = subprocess.run(cmd, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=1200)
        print('EXIT',r.returncode,'ELAPSED_SECONDS',round(time.monotonic()-begin,2),file=log)
    (packet/'receipts'/f'{label}.rc').write_text(str(r.returncode)+'\n')
    print(label,r.returncode,flush=True)
    return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    codes = list(pool.map(run,commands.items()))
sys.exit(any(codes))
