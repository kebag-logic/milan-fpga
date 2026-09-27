#!/usr/bin/env python3
"""Run one command in the foreground and keep a receipt: argv, cwd, rc, output.

Usage: rr.py <name> <cwd> -- <argv...>
Writes receipts/<name>.log next to this script and exits with the command's rc.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    name, cwd, sep, *argv = sys.argv[1:]
    assert sep == '--' and argv, __doc__
    out = HERE / 'receipts' / f'{name}.log'
    out.parent.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    start = time.monotonic()
    proc = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)
    took = time.monotonic() - start
    cwd_label = Path(cwd).resolve().name
    header = (f'# argv: {argv!r}\n# cwd: <{cwd_label}>\n# rc: {proc.returncode}\n'
              f'# seconds: {took:.1f}\n')
    out.write_bytes(header.encode() + proc.stdout)
    print(f'{name}: rc={proc.returncode} ({took:.1f}s)')
    return proc.returncode


if __name__ == '__main__':
    sys.exit(main())
