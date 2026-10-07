#!/usr/bin/env python3
"""Run only issue #16's three named reversals using the unchanged driver."""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import sys

sys.dont_write_bytecode = True
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=Path.cwd())
parser.add_argument('--profile', choices=['OFF', 'ON'], required=True)
args = parser.parse_args()
packet = Path(__file__).resolve().parents[1]
root = args.repo.resolve()
work = packet / 'scratch' / ('reversals-' + args.profile)
driver = runpy.run_path(str(root / 'tests/check_reversals.py'))
selected = {'point-to-point-condition', 'pending-point-to-point-condition', 'shared-in-condition'}
cases = [case for case in driver['CASES'] if case[0] in selected]
assert len(cases) == 3
driver['main'].__globals__['CASES'] = cases
sys.argv = ['tests/check_reversals.py', '--work-dir', str(work), '--prefix',
            str(packet / 'scratch/unit-prefix'), '--milan', args.profile]
rc = driver['main']()
out = packet / 'receipts' / ('reversals-' + args.profile)
out.mkdir(exist_ok=True)
for path in work.iterdir():
    if path.is_file() and path.suffix in ['.log', '.json']:
        shutil.copy2(path, out / path.name)
restored = []
for name in ['CMakeLists.txt', 'src', 'tests']:
    original = root / name
    files = original.rglob('*') if original.is_dir() else [original]
    for source in files:
        if not source.is_file() or '__pycache__' in source.parts:
            continue
        relative = source.relative_to(root)
        copied = work / 'source' / relative
        assert copied.read_bytes() == source.read_bytes(), relative
        restored.append({'path': str(relative), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
(out / 'restored-bytes.json').write_text(json.dumps(restored, indent=2) + '\n')
print('Every copied source and test byte restored.')
sys.exit(rc)
