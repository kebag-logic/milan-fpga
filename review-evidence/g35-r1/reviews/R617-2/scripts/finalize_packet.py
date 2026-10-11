#!/usr/bin/env python3
"""Select publishable files, verify report links and emit portable SHA256 list."""
import hashlib
from pathlib import Path
import re

p = Path(__file__).resolve().parents[1]
report = (p / 'REPORT.md').read_text()
assert report.splitlines()[0] == '[R617] POSITIVE - exact head a70e38804cb16435c089d024c58e8c3fb4d39ff6'
assert report.splitlines()[-1] == 'R617-2 FINISHED'
assert 'SKELETON' not in report
for lens in ('Conformance', 'RTL', 'Robustness', 'Tests', 'Docs'):
    assert f'| {lens} | CLEAN |' in report
selected = [p / 'REPORT.md']
selected.extend(f for f in (p / 'scripts').glob('*') if f.is_file())
for f in (p / 'receipts').rglob('*'):
    if not f.is_file(): continue
    if f.name.startswith(('prior-review-', 'new-comment-')): continue
    if f.name.endswith(('-build.log', '.command.json')): continue
    if f == p / 'receipts/local/parser.log': continue
    selected.append(f)
selected = sorted(set(selected), key=lambda f: str(f.relative_to(p)))
paths = {str(f.relative_to(p)) for f in selected}
for target in re.findall(r'\]\(([^)]+)\)', report):
    if target.startswith(('https://', 'http://')): continue
    assert target in paths, ('unpublished report target', target)
assert not any(x.startswith('scratch/') for x in paths)
for f in selected:
    if f.suffix in ('.log', '.txt', '.md'):
        assert '$WORKSPACE_HOME/' not in f.read_text(errors='replace'), f
(p / 'MANIFEST.sha256').write_text(''.join(
    hashlib.sha256(f.read_bytes()).hexdigest() + '  ' + str(f.relative_to(p)) + '\n'
    for f in selected))
print(f'PASS: {len(selected)} publishable files; report markers, five lenses and local links verified; scratch excluded.')
