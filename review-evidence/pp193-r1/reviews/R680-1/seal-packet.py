#!/usr/bin/env python3
"""Validate the review packet and write a relative-path sha256sum manifest."""
import ast
import hashlib
from pathlib import Path
import re

p=Path(__file__).resolve().parent
report=(p/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R680] NEGATIVE - exact head 6ddfcda4c3170b8f463c8623833f7541ca8c1faf'
assert report.splitlines()[-1]=='R680-1 FINISHED'
assert 'SKELETON' not in report
for script in p.glob('*.py'):
    ast.parse(script.read_text(),filename=str(script))
for target in re.findall(r'\]\(([^)]+)\)',report):
    if not target.startswith(('https://','http://')):
        assert (p/target).is_file(),target
assert 'Clean tracked/index/untracked state: PASS' in (p/'source-integrity.txt').read_text()
(p/'packet-check.txt').write_text(
    'Report first/last line: PASS\nNo skeleton remains: PASS\n'
    'Portable scripts parse: PASS\nReport receipt links exist: PASS\n'
    'Source integrity receipt: PASS\nScratch excluded from publication: PASS\n')
files=sorted(f for f in p.rglob('*') if f.is_file()
             and 'scratch' not in f.relative_to(p).parts
             and f.name!='MANIFEST.sha256')
manifest=''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(p).as_posix()+'\n'
                 for f in files)
(p/'MANIFEST.sha256').write_text(manifest)
for line in manifest.splitlines():
    digest,rel=line.split('  ',1)
    assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==digest
print(f'Packet sealed: {len(files)} files; scratch excluded; all hashes verified.')
