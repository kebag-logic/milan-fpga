#!/usr/bin/env python3
"""Scrub installation paths, verify retained simulation bytes, hash the packet."""
import hashlib
import json
from pathlib import Path
import re
import shutil

root = Path(__file__).resolve().parents[1]
receipts = root / 'receipts'
for path in receipts.glob('*.log'):
    text = path.read_text()
    text = re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff/usr/share/verilator',
                  '<simulator-runtime>', text)
    path.write_text(text)
for name in ['epoch-base-run', 'epoch-head-run', 'epoch-dev-run']:
    assert (root / 'scratch' / (name + '.raw.log')).read_bytes() == (
        receipts / (name + '.log')).read_bytes(), name
shutil.rmtree(root / 'scripts/__pycache__', ignore_errors=True)
report = (root / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R515] NEGATIVE - exact head 41bc9dac031526c1fd637ff1e801d3c6dc1260b4'
assert report.splitlines()[-1] == 'R515-1 FINISHED'
assert 'SKELETON' not in report
files = sorted([x for x in receipts.iterdir() if x.is_file()] +
               [x for x in (root / 'scripts').iterdir() if x.is_file()] +
               [root / 'REPORT.md'])
for path in files:
    data = path.read_bytes()
    assert re.search(rb'/home/[A-Za-z0-9_.-]+/', data) is None, path.name
    assert (b'milan-fpga' + b'-management') not in data, path.name
manifest = ''.join(hashlib.sha256(x.read_bytes()).hexdigest() + '  ' +
                   str(x.relative_to(root)) + '\n' for x in files)
(root / 'MANIFEST.sha256').write_text(manifest)
print(json.dumps({'manifest_files': len(files),
                  'publishable_bytes': sum(x.stat().st_size for x in files),
                  'render_stdout_bytes_unmodified': True,
                  'report_first_line': report.splitlines()[0],
                  'report_last_line': report.splitlines()[-1]}, indent=2))
