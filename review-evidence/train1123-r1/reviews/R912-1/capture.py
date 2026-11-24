#!/usr/bin/env python3
"""Run one foreground review command and retain output and exit status."""
import os
from pathlib import Path
import subprocess
import sys

packet = Path(__file__).resolve().parent
root, label, *command = sys.argv[1:]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0',
           TMPDIR=str(packet / 'scratch' / 'tmp'))
with (packet / 'receipts' / (label + '.log')).open('w') as log:
    log.write('COMMAND ' + ' '.join(command) + '\n')
    log.flush()
    try:
        rc = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT,
                            timeout=550).returncode
    except subprocess.TimeoutExpired:
        rc = 124
        log.write('\nINCOMPLETE: review time limit of 550 seconds reached.\n')
    log.write(f'\nEXIT {rc}\n')
(packet / 'receipts' / (label + '.rc')).write_text(str(rc) + '\n')
print(f'{label}: exit {rc}')
raise SystemExit(rc)
