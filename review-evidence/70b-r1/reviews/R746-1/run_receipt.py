#!/usr/bin/env python3
"""Run one foreground check, retaining its command, output and exit status."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

packet = Path(__file__).resolve().parent
name, *command = sys.argv[1:]
env = dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
started = time.time()
with (packet / 'logs' / (name + '.log')).open('w') as log:
    result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, env=env)
receipt = {'command': command, 'cwd': os.getcwd(), 'returncode': result.returncode,
           'elapsed_seconds': round(time.time() - started, 3)}
(packet / 'logs' / (name + '.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
sys.exit(result.returncode)
