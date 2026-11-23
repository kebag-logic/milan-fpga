#!/usr/bin/env python3
"""Foreground supervisor: focused arms and three campaigns, at most 16 compiler jobs.
Usage: python3 -I run_focused.py CHECKOUT PACKET
"""
import concurrent.futures
from pathlib import Path
import shutil
import subprocess
import sys

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
scripts, scratch, receipts = (packet / p for p in ('scripts', 'scratch', 'receipts'))
tasks = [('arms-run', [sys.executable, '-I', str(scripts / 'run_arms.py'), str(root), str(packet), '2', '2',
                        '--base-src', str(scratch / 'f863')])]
for shape, interfaces in [('1x1', 1), ('1x1', 2), ('endstation_ax7101_8x8', 1)]:
    name = f'early-{shape}-if{interfaces}'
    tasks.append((name, [sys.executable, '-I', str(scripts / 'early_campaign.py'), str(root),
                         str(scratch / name), str(interfaces), shape, '4']))

def run(task):
    name, cmd = task
    with (receipts / (name + '.log')).open('w') as log:
        rc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, cwd=root).returncode
    (receipts / (name + '.rc')).write_text(f'{rc}\n')
    if name.startswith('early-'):
        for log in (scratch / name).glob('*.log'):
            dst = receipts / 'campaigns' / name / log.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(log, dst)
    print(f'{name}: rc={rc}', flush=True)
    return rc

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, tasks))
sys.exit(int(any(results)))
