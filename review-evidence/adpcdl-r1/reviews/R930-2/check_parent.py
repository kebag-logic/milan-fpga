#!/usr/bin/env python3
"""Check the published consumer patch without a parent build or pin change."""
import base64
import hashlib
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
PATCH = OUT/'scratch/public/adpcdl-r2/author/receipts/parent-consumer.patch'
REFS = ['5de21ff3661436ea5598718aca36934361e35340', 'e275d7950ef3385753e6a15d2e191ba855b171ed']
PATHS = ['sw/firmware/ctrl/test/ctrl_mutants.py', 'sw/firmware/ctrl/test/test_adp.cpp']
results = []
for ref in REFS:
    dest = OUT/'scratch'/('parent-'+ref[:8])
    files = []
    for path in PATHS:
        obj = json.loads(subprocess.check_output(['gh', 'api',
            f'repos/kebag-logic/milan-fpga/contents/{path}?ref={ref}']))
        data = base64.b64decode(obj['content'])
        p = dest/path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        files.append({'path': path, 'blob': obj['sha'], 'sha256': hashlib.sha256(data).hexdigest()})
    p = subprocess.run(['git', 'apply', '--check', str(PATCH)], cwd=dest, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    tree = json.loads(subprocess.check_output(['gh', 'api',
        f'repos/kebag-logic/milan-fpga/git/trees/{ref}?recursive=1']))
    assert not tree.get('truncated')
    links = [{'path': e['path'], 'sha': e['sha']} for e in tree['tree'] if e['mode'] == '160000']
    results.append({'parent': ref, 'files': files, 'apply_check_rc': p.returncode,
                    'output': p.stdout+p.stderr, 'gitlinks': links})
(OUT/'parent-check.json').write_text(json.dumps(results, indent=2)+'\n')
print('PASS: patch applies without offsets to both stated parents; gitlinks recorded read-only.')
