#!/usr/bin/env python3
"""Run one foreground command; retain its raw output and exit status."""
import argparse
import os
from pathlib import Path
import subprocess
import time

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cwd', type=Path, required=True)
    p.add_argument('--log', type=Path, required=True)
    p.add_argument('--timeout', type=int, default=540)
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    command = a.command[1:] if a.command[:1] == ['--'] else a.command
    t = time.monotonic()
    with a.log.open('w') as out:
        out.write('command: ' + repr(command) + '\n')
        out.flush()
        try:
            result = subprocess.run(command, cwd=a.cwd, stdout=out, stderr=subprocess.STDOUT, timeout=a.timeout)
            rc = result.returncode
        except subprocess.TimeoutExpired:
            out.write('\nREVIEW TIME LIMIT\n')
            rc = 124
    a.log.with_suffix('.rc').write_text(str(rc)+'\n')
    print(a.log.name, 'rc', rc, 'elapsed', round(time.monotonic()-t,2))
    print('\n'.join(a.log.read_text(errors='replace').splitlines()[-14:]))
    raise SystemExit(rc)

if __name__ == '__main__':
    main()
