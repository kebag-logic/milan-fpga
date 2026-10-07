# SPDX-License-Identifier: Apache-2.0
"""Check publication boundaries and list every selected receipt by SHA-256."""
import argparse, ast, hashlib, json, re
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--packet',type=Path,required=True)
a=p.parse_args()
packet=a.packet.resolve()
report=(packet/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R541] NEGATIVE - exact head 0a45695db537badb8d7e9cbf578925fe5b89d647'
assert report.splitlines()[-1]=='R541-4 FINISHED'
assert 'SKELETON' not in report
for f in (packet/'scripts').glob('*.py'):
    ast.parse(f.read_text(),filename=f.name)
for link in re.findall(r'\]\(([^)]+)\)',report):
    if '://' not in link and link!='MANIFEST.sha256':
        assert (packet/link.split('#')[0]).is_file(),link
files=[packet/'REPORT.md']+[f for root in ['scripts','receipts'] for f in (packet/root).rglob('*') if f.is_file()]
for f in files:
    assert 'scratch' not in f.relative_to(packet).parts
    assert not f.is_symlink()
    assert not re.search(r'/(?:home|data)/[A-Za-z0-9_]',f.read_text()),f.name
manifest=''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(packet))+'\n' for f in sorted(files))
(packet/'MANIFEST.sha256').write_text(manifest)
print('Manifest entries:',len(files))
print('Report boundary lines, script syntax, relative links, and publication boundaries pass.')
