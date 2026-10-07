#!/usr/bin/env python3
"""Normalize local roots in receipts, preserve provenance and bind publication."""
import hashlib
import json
import re
import sys
from pathlib import Path
packet=Path(__file__).resolve().parents[1]
repo=Path(sys.argv[1]).resolve()
replacements=[(str(packet),'${PACKET}'),(str(repo),'${REPO}'),
              (str(Path.home()/'standards'),'${STANDARDS_DIR}'),(str(repo.parents[1]/'tools'),'${TOOLS}')]
records=[]
provenance=packet/'receipts/receipt-provenance.json'
prior={r['path']:r for r in json.loads(provenance.read_text())} if provenance.exists() else {}
for f in sorted((packet/'receipts').rglob('*')):
    if not f.is_file() or f==provenance:
        continue
    before=f.read_bytes()
    text=before.decode()
    for old,new in replacements:
        text=text.replace(old,new)
    text=re.sub(r'/home/[^/]+/\.local/share/containers/storage/overlay/[^/]+/diff/usr/share/verilator', '${HDL_ROOT}', text)
    after=text.encode()
    f.write_bytes(after)
    old=prior.get(str(f.relative_to(packet)), {})
    records.append({'path':str(f.relative_to(packet)),'original_sha256':old.get('original_sha256',hashlib.sha256(before).hexdigest()),
                    'published_sha256':hashlib.sha256(after).hexdigest(),'original_size':old.get('original_size',len(before)),
                    'published_size':len(after),'normalized':old.get('normalized',False) or before!=after})
provenance.write_text(json.dumps(records,indent=2)+'\n')
files=[packet/'REPORT.md',packet/'REPRODUCE.md',packet/'independent-pass.txt']
files+=sorted(f for folder in ('scripts','receipts') for f in (packet/folder).rglob('*')
              if f.is_file() and '__pycache__' not in f.parts)
lines=[hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(packet)) for f in files]
(packet/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
assert (packet/'REPORT.md').read_text().startswith('[R533] NEGATIVE - exact head cce554f64f6bdab1f6d26e5c4d7b46d54d228c52\n')
assert (packet/'REPORT.md').read_text().splitlines()[-1]=='R533-6 FINISHED'
assert 'SKELETON' not in (packet/'REPORT.md').read_text()
for f in files:
    data=f.read_text()
    assert str(Path.home())+'/' not in data,f
    assert str(repo.parents[1])+'/' not in data,f
    assert '\u2014' not in data or f.is_relative_to(packet/'receipts'),f
print('Publishable files:',len(files))
print('All manifest paths are relative; scratch excluded.')
