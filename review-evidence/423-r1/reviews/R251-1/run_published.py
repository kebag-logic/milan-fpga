#!/usr/bin/env python3
"""Run the downloaded public example unchanged, in a new temporary directory."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

OUT = Path(__file__).resolve().parent
SOURCE = Path('$VALIDATION_STORAGE/reviews/r251-423-locale-retry')
work = Path(tempfile.mkdtemp(prefix='r251-locale-'))
(OUT / 'work-directory.txt').write_text(str(work) + '\n')
receipts = OUT / 'receipts' / 'reproduced'
receipts.mkdir(exist_ok=True)
env = dict(os.environ, LC_ALL='C.UTF-8', PYTHONUTF8='0',
           PYTHONCOERCECLOCALE='0', PYTHONDONTWRITEBYTECODE='1',
           GIT_TERMINAL_PROMPT='0', OMP_NUM_THREADS='1',
           OPENBLAS_NUM_THREADS='1', MAKEFLAGS='-j1')
command = ['rtk', 'proxy', 'bash', '-x',
           str(OUT / 'receipts' / 'locale_transport_probe.sh'),
           str(SOURCE), str(work), str(receipts)]
with (receipts / 'stdout.bin').open('wb') as stdout, \
     (receipts / 'stderr-xtrace.bin').open('wb') as stderr:
    result = subprocess.run(command, env=env, stdout=stdout, stderr=stderr)
(receipts / 'execution.json').write_text(json.dumps({
    'argv': command, 'cwd': os.getcwd(), 'returncode': result.returncode,
    'environment_overrides': {key: env[key] for key in (
        'LC_ALL', 'PYTHONUTF8', 'PYTHONCOERCECLOCALE', 'PYTHONDONTWRITEBYTECODE',
        'GIT_TERMINAL_PROMPT', 'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MAKEFLAGS')},
    'work': str(work), 'jobs': 1,
    'note': 'Probe exit 0 means execution completed; individual checker exits are in stdout.'
}, indent=2) + '\n')
print((receipts / 'stdout.bin').read_bytes().decode('utf-8', 'backslashreplace'))
print('probe exit:', result.returncode, 'temporary work:', work)
raise SystemExit(result.returncode)
