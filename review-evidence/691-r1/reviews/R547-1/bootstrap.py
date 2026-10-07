#!/usr/bin/env python3
"""Fetch pinned dependency sources into a disposable review environment."""
import concurrent.futures
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import urllib.request

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
deps = scratch / 'deps'
deps.mkdir(exist_ok=True)
pins = re.findall(r'^git\+https://github.com/([^@]+)\.git@([0-9a-f]+)$',
                  (repo / 'sw/litex/litex_pins.txt').read_text(), re.M)

def fetch(pin):
    name, sha = pin
    target = deps / name.split('/')[-1]
    data = urllib.request.urlopen(f'https://codeload.github.com/{name}/tar.gz/{sha}', timeout=120).read()
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
        top = archive.getnames()[0].split('/')[0]
        archive.extractall(deps, filter='data')
    (deps / top).rename(target)
    return {'repository': name, 'commit': sha, 'archive_sha256': hashlib.sha256(data).hexdigest()}

with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
    receipts = list(pool.map(fetch, pins))
(packet / 'dependencies.json').write_text(json.dumps(receipts, indent=2) + '\n')
venv = scratch / 'venv'
subprocess.run([sys.executable, '-m', 'venv', str(venv)], check=True)
python = venv / 'bin/python'
env = dict(os.environ, TMPDIR=str(scratch), PIP_DISABLE_PIP_VERSION_CHECK='1',
           PYTHONDONTWRITEBYTECODE='1', PIP_CACHE_DIR=str(scratch / 'pip-cache'))
with (scratch / 'pip.log').open('w') as log:
    subprocess.run([str(python), '-m', 'pip', 'install', 'pyyaml', *[str(deps / n.split('/')[-1]) for n, _ in pins]],
                   env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
print('PASS: seven pinned archives fetched and isolated environment installed')
