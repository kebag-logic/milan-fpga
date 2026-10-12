#!/usr/bin/env python3
"""Run the committed refresh shell verbatim and retain its public inputs."""
import argparse
import ast
import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import textwrap

p = argparse.ArgumentParser()
p.add_argument('repo', type=Path)
p.add_argument('packet', type=Path)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
out, scratch = packet / 'receipts', packet / 'scratch'
tmp = scratch / 'refresh-tmp'
tmp.mkdir(exist_ok=True)
cache = scratch / 'refresh-cache'
env = dict(os.environ, TMPDIR=str(tmp), XDG_CACHE_HOME=str(cache), PYTHONDONTWRITEBYTECODE='1')
doc = ast.get_docstring(ast.parse((repo / 'scripts/suite_shards.py').read_text()), clean=False)
start = doc.index('    run=38217650945')
end = doc.index('\n\n', start)
shell = textwrap.dedent(doc[start:end]) + '\n'
(out / 'refresh-verbatim.sh').write_text(shell)
result = subprocess.run(['bash', '-euc', shell], cwd=repo, env=env, text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=540)
(out / 'refresh-verbatim.log').write_text(result.stdout)
(out / 'refresh-verbatim.rc').write_text(str(result.returncode) + '\n')
print('refresh rc', result.returncode, flush=True)
assert result.returncode == 0, result.stdout[-3000:]
devlogs = out / 'calibration-dev'
devlogs.mkdir(exist_ok=True)
for log in tmp.glob('*/*.log'):
    shutil.copyfile(log, devlogs / log.name)
assert len(list(devlogs.glob('*.log'))) == 5
command = ['gh', 'run', 'view', '38208503834', '-R', 'kebag-logic/milan-fpga', '--job', '114677344710', '--log']
result = subprocess.run(command, cwd=repo, env=env, capture_output=True, timeout=180)
(out / 'calibration-maap.log').write_bytes(result.stdout)
(out / 'calibration-maap.stderr').write_bytes(result.stderr)
(out / 'calibration-maap.rc').write_text(str(result.returncode) + '\n')
assert result.returncode == 0, result.stderr
result = subprocess.run(['python3', 'scripts/suite_shards.py', '--measure', str(out / 'calibration-maap.log')],
                        cwd=repo, env=env, capture_output=True, text=True, timeout=30)
(out / 'measure-maap.log').write_text(result.stdout + result.stderr)
(out / 'measure-maap.rc').write_text(str(result.returncode) + '\n')
assert result.returncode == 0, result.stderr
tree = json.loads((out / 'published-evidence-tree.json').read_text())['tree']
for entry in tree:
    if not entry['path'].startswith('review-evidence/727-r1/') or entry['type'] != 'blob':
        continue
    result = subprocess.run(['gh', 'api', 'repos/kebag-logic/milan-fpga/git/blobs/' + entry['sha']],
                            capture_output=True, text=True, check=True, timeout=60)
    blob = base64.b64decode(json.loads(result.stdout)['content'])
    dest = out / 'published' / entry['path'].removeprefix('review-evidence/727-r1/')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(blob)
print('Retained five dev logs, the maap log, and the published author evidence.', flush=True)
