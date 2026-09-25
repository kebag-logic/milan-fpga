"""Run one foreground command, preserving its raw output and exit status."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
REPO = Path('$LANES/443-render-csr')


def main():
    name, *command = sys.argv[1:]
    env = dict(os.environ)
    env['PATH'] = (OUT / 'python-env.txt').read_text().strip() + '/bin:' + env['PATH']
    env['VERILATOR_JOBS'] = '8'
    start = time.monotonic()
    print(f'RUN {name}: {command}', flush=True)
    with (OUT / f'{name}.log').open('w') as log:
        result = subprocess.run(['rtk', 'proxy', *command], cwd=REPO, env=env,
                                stdout=log, stderr=subprocess.STDOUT, timeout=14400)
    diff = subprocess.run(['rtk', 'proxy', 'git', 'diff', 'HEAD'], cwd=REPO,
                          capture_output=True, check=True, timeout=180).stdout
    head = subprocess.run(['rtk', 'proxy', 'git', 'rev-parse', 'HEAD'], cwd=REPO,
                          capture_output=True, text=True, check=True, timeout=180).stdout.strip()
    record = dict(name=name, command=command, rc=result.returncode,
                  seconds=round(time.monotonic()-start, 2), head=head,
                  diff_sha256=hashlib.sha256(diff).hexdigest())
    with (OUT / 'gates.jsonl').open('a') as ledger:
        ledger.write(json.dumps(record) + '\n')
    print(json.dumps(record), flush=True)
    print('\n'.join((OUT / f'{name}.log').read_text(errors='replace').splitlines()[-10:]))
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
