"""Copy a public extract without the srp-bound case, retaining all other bytes.

Usage: python3 prepare_missing_bound.py EXTRACT NEW_SCRATCH_DIRECTORY
"""
import json
import os
import sys
from pathlib import Path

src, dst = map(Path, sys.argv[1:])
dst.mkdir(parents=True, exist_ok=False)
for file in src.rglob('*'):
    rel = file.relative_to(src)
    if 'srp-bound' in rel.parts:
        continue
    target = dst / rel
    if file.is_dir():
        target.mkdir(exist_ok=True)
    elif rel.as_posix() != 'census.json':
        os.link(file, target)
census = json.loads((src / 'census.json').read_text())
census['cases'] = [r for r in census['cases'] if r['case'].split('/')[-1] != 'srp-bound']
(dst / 'census.json').write_text(json.dumps(census))
print('Missing-bound control cases:', len(census['cases']))
