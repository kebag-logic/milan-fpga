#!/usr/bin/env python3
import gzip
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys

selector = Path(sys.argv[1]).resolve()
text = selector.read_text()
args = shlex.split(text.splitlines()[1])
assert args[:2] == ['exec', 'env']
root = Path(args[2].removeprefix('VERILATOR_ROOT='))
layer = root.parents[2]
expected = json.loads((Path(__file__).resolve().parents[1] /
                       'public-manager/pinned-tool-identity.json').read_text())
binary = layer / 'usr/bin/verilator_bin'
assert hashlib.sha256(binary.read_bytes()).hexdigest() == expected['binary_sha256']
mtree = layer / 'var/lib/pacman/local/verilator-5.050-1/mtree'
rows, missing = [], []
defaults = {}
for line in gzip.decompress(mtree.read_bytes()).decode().splitlines():
    parts = line.split()
    if parts and parts[0] == '/set':
        defaults.update(p.split('=', 1) for p in parts[1:] if '=' in p)
        continue
    if not parts or not parts[0].startswith('./usr/'):
        continue
    attributes = dict(defaults)
    attributes.update(p.split('=', 1) for p in parts[1:] if '=' in p)
    if attributes.get('type') != 'file':
        continue
    file = layer / parts[0]
    if not file.exists():
        assert parts[0] in expected['missing_manual_pages'], parts[0]
        missing.append(parts[0])
        continue
    actual = hashlib.sha256(file.read_bytes()).hexdigest()
    assert actual == attributes['sha256digest'], parts[0]
    rows.append(dict(path=parts[0], sha256=actual))
assert {r['path'] for r in rows} == set(expected['matched_files']), len(rows)
version = subprocess.check_output(['rtk', 'proxy', str(selector), '--version'], text=True).strip()
assert version == expected['version'], version
print(json.dumps(dict(version=version, selector=str(selector),
                     selector_sha256=hashlib.sha256(selector.read_bytes()).hexdigest(),
                     layer=str(layer), binary_sha256=expected['binary_sha256'],
                     matched=rows, missing_manual_pages=missing), indent=2))
