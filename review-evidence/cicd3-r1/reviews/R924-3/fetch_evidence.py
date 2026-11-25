#!/usr/bin/env python3
"""Usage: python3 fetch_evidence.py CHECKOUT PACKET. Restore public inputs under PACKET/scratch only."""
import io
import json
from pathlib import Path
import subprocess
import sys
import zipfile

root, packet = map(lambda s: Path(s).resolve(), sys.argv[1:])
revision = '22b3d7ad1e8bca3a5b783af5c8bd2446edc2cc9a'
prefix = 'review-evidence/cicd3-r1/'
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])
def api(path):
    return subprocess.check_output(['gh','api','repos/kebag-logic/milan-fpga/'+path])
# The publication commit must already be fetched into the supplied clone.
paths = git('ls-tree','-r','--name-only',revision,prefix+'author-r8').decode().splitlines()
paths.append(prefix+'MANIFEST.json')
for path in paths:
    destination = packet/'scratch'/path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(git('show',revision+':'+path))
for run in (45550366428,45528738040):
    artifacts = json.loads(api(f'actions/runs/{run}/artifacts?per_page=100'))['artifacts']
    chosen = [a for a in artifacts if a['name'] == 'suite-union-follow_ring']
    assert len(chosen) == 1 and not chosen[0]['expired']
    archive = zipfile.ZipFile(io.BytesIO(api(f'actions/artifacts/{chosen[0]["id"]}/zip')))
    assert all(not n.startswith('/') and '..' not in Path(n).parts for n in archive.namelist())
    archive.extractall(packet/f'scratch/union-{run}')
print('Public source packet and two follow_ring unions restored under scratch')
