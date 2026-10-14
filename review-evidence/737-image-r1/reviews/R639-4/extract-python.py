#!/usr/bin/env python3
"""Extract only pinned public interpreter files and Python dependencies."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
sys.path.insert(0, str(root / 'ci/image'))
import privacy

pins = json.loads((root / 'ci/image/sources.lock.json').read_text())
cache = packet / 'scratch/image/context'
target = packet / 'scratch/reference'
count = 0
for row in pins['packages']:
    if row['tool'] not in ('python3.12-minimal', 'libpython3.12-minimal', 'libpython3.12-stdlib',
                           'libexpat1', 'libffi8', 'libssl3t64'):
        continue
    path = cache / 'debs' / row['filename']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    for name, stream in privacy.deb_members(path):
        rel = Path(name.removeprefix('./'))
        assert not rel.is_absolute() and '..' not in rel.parts
        if not str(rel).startswith(('usr/bin/', 'usr/lib/')):
            continue
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(stream.read())
        dest.chmod(0o755 if str(rel).startswith('usr/bin/') else 0o644)
        count += 1
for row in pins['sources']:
    if row.get('kind') != 'python' or not row['filename'].endswith('.whl'):
        continue
    path = cache / row['filename']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
    with zipfile.ZipFile(path) as archive:
        for member in archive.infolist():
            rel = Path(member.filename)
            assert not rel.is_absolute() and '..' not in rel.parts
            if member.is_dir():
                continue
            dest = target / 'site' / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(archive.read(member))
            count += 1
print('Extracted', count, 'authenticated regular files; no links or devices')
