#!/usr/bin/env python3
"""Run one foreground command, retaining raw output and exit status."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--name', required=True)
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
command = a.command[1:] if a.command[:1] == ['--'] else a.command
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1', GIT_NO_REPLACE_OBJECTS='1')
started = time.time()
with (packet / (a.name + '.log')).open('wb') as output:
    result = subprocess.run(command, cwd=a.repo, env=env, stdout=output, stderr=subprocess.STDOUT)
(packet / (a.name + '.rc')).write_text(str(result.returncode) + '\n')
display = [s.replace(str(packet), '<packet>').replace(str(a.repo), '<candidate>') for s in command]
(packet / (a.name + '.json')).write_text(json.dumps({'command': display, 'rc': result.returncode, 'seconds': round(time.time()-started, 3)}, indent=2) + '\n')
print(a.name, 'rc=' + str(result.returncode), flush=True)
print((packet / (a.name + '.log')).read_text(errors='replace')[-5000:])
raise SystemExit(result.returncode)
