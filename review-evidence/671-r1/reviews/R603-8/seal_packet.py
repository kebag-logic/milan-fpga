#!/usr/bin/env python3
"""Hash publishable packet files, excluding scratch and redundant public bodies."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parent
exclude = {'MANIFEST.sha256', 'pr.json', 'prior-public-findings.json',
           'issue-scope-comments.json', 'pr-evidence-comments.json'}
report = (root/'REPORT.md').read_text()
assert report.splitlines()[0] == '[R603] POSITIVE - exact head d5cd863561ba1ee7bc6342fb1b00f57dd786bd97'
assert report.splitlines()[-1] == 'R603-8 FINISHED'
assert 'SKELETON' not in report
files = sorted(p for p in root.rglob('*') if p.is_file()
               and 'scratch' not in p.relative_to(root).parts
               and p.name not in exclude)
for path in files:
    if path.suffix == '.py':
        compile(path.read_text(), str(path.relative_to(root)), 'exec')
manifest = ''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '
                   +str(p.relative_to(root))+'\n' for p in files)
(root/'MANIFEST.sha256').write_text(manifest)
print('Sealed',len(files),'publishable files; scratch excluded; report framing verified.')
