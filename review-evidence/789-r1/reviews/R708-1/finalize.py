#!/usr/bin/env python3
"""Normalize local scratch paths and enumerate only publication files."""
import hashlib
import json
from pathlib import Path

out = Path(__file__).resolve().parent
raw_dir = out/'scratch/raw-receipts'
raw_dir.mkdir(exist_ok=True)
records = []
for name in ['ci_capture_cases_selftest.log','markdown-setup.log']:
    path = out/name
    original_path = raw_dir/name
    if not original_path.exists():
        original_path.write_bytes(path.read_bytes())
    original = original_path.read_bytes()
    public = original.replace(str(out/'scratch').encode(),b'<scratch>')
    path.write_bytes(public)
    records.append({'file':name,'replacement':'local scratch prefix -> <scratch>',
                    'original_sha256':hashlib.sha256(original).hexdigest(),
                    'published_sha256':hashlib.sha256(public).hexdigest()})
(out/'REDACTIONS.json').write_text(json.dumps(records,indent=2)+'\n')
lines = []
for path in sorted(out.rglob('*')):
    relative = path.relative_to(out)
    if not path.is_file() or relative.parts[0] == 'scratch' or path.name == 'MANIFEST.sha256':
        continue
    lines.append(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+relative.as_posix())
(out/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
print('Publishable files:',len(lines))
report = (out/'REPORT.md').read_text()
assert report.splitlines()[0] == '[R708] POSITIVE - exact head fddf3671ebc96a953755fa1b9a3ecec5f071a350'
assert report.splitlines()[-1] == 'R708-1 FINISHED'
assert 'SKELETON' not in report
assert all('/scratch/' not in line for line in lines)
print('Report, ledger and publication manifest: PASS')
