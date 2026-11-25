#!/usr/bin/env python3
"""Recheck checkout integrity and hash only publishable packet files."""
import hashlib
import json
from pathlib import Path
import re
import runpy
import sys

out = Path(__file__).resolve().parent
source = Path(sys.argv[1]).resolve()
sys.argv = [str(out/'run_probes.py'), str(source), str(out)]
namespace = runpy.run_path(str(out/'run_probes.py'))
namespace['integrity']('integrity-after.json')
integrity = json.loads((out/'integrity-after.json').read_text())
assert len(integrity['tracked_blobs']) == 100
report = (out/'REPORT.md').read_text()
assert report.startswith('[R930] POSITIVE - exact head ec727b64663b4eef2fc8da1ea5e0eae6541597d1\n')
assert report.rstrip().endswith('R930-2 FINISHED')
assert 'SKELETON' not in report
files = sorted(p for p in out.iterdir() if p.is_file() and p.name != 'MANIFEST.sha256')
for p in files:
    text = p.read_text()
    assert not re.search(r'/(?:home|srv|data|mnt|media|Users)/', text), p.name
    if p.suffix == '.py':
        compile(text, p.name, 'exec')
lines = [hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name for p in files]
(out/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
print(json.dumps({'publishable_files': len(files), 'tracked_blobs': len(integrity['tracked_blobs']),
                  'head': integrity['head'], 'tree': integrity['tree'], 'index_matches': integrity['index_matches'],
                  'source_gitlinks': integrity['gitlinks'], 'status': integrity['status'],
                  'manifest': 'PASS', 'host_path_scan': 'PASS'}))
