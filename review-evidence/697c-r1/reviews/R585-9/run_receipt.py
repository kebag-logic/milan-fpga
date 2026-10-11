#!/usr/bin/env python3
"""Run one foreground command and keep its combined output and exit status."""
import argparse
import os
import subprocess
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('packet', type=Path)
ap.add_argument('name')
ap.add_argument('command', nargs=argparse.REMAINDER)
args = ap.parse_args()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', MAKEFLAGS='-j16', TMPDIR=str(args.packet / 'scratch'))
result = subprocess.run(args.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, check=False)
(args.packet / (args.name + '.log')).write_bytes(result.stdout)
(args.packet / (args.name + '.rc')).write_text(str(result.returncode) + '\n')
print(args.name, 'rc', result.returncode)
print(result.stdout.decode(errors='replace')[-3000:])
