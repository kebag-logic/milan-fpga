#!/usr/bin/env python3
"""Run a foreground command and retain its exact argv, output and status."""
import json
import os
from pathlib import Path
import subprocess
import sys

packet = Path(__file__).resolve().parents[1]
name, *argv = sys.argv[1:]
out = packet / 'receipts'
out.mkdir(exist_ok=True)
(out / (name + '.command.json')).write_text(json.dumps({'cwd': os.getcwd(), 'argv': argv}, indent=2) + '\n')
with (out / (name + '.log')).open('wb') as log:
    result = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT, check=False)
(out / (name + '.rc')).write_text(str(result.returncode) + '\n')
print(name, 'rc', result.returncode, flush=True)
sys.exit(result.returncode)
