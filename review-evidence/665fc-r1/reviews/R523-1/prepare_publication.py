#!/usr/bin/env python3
"""Prepare public receipts with path-only redaction of local compiler support paths."""
from pathlib import Path
import re,json,hashlib
p=Path(__file__).resolve().parent
raw=p/'scratch/raw-receipts';raw.mkdir(parents=True,exist_ok=True)
records=[]
pattern=re.compile(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff/usr/share/verilator')
for name in ('mbx-suite.log','boundary-probe.log'):
 f=p/name
 original=(raw/name).read_bytes() if (raw/name).exists() else f.read_bytes()
 (raw/name).write_bytes(original)
 rendered,n=pattern.subn('<SIMULATOR_SUPPORT>',original.decode())
 f.write_text(rendered)
 records.append({'file':name,'original_sha256':hashlib.sha256(original).hexdigest(),
                 'published_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),
                 'path_substitutions':n,'replacement':'<SIMULATOR_SUPPORT>'})
(p/'redaction-receipt.json').write_text(json.dumps(records,indent=2)+'\n')
files=sorted([*p.glob('*.log'),*p.glob('*.rc'),*p.glob('*.command.json'),*p.glob('*.py'),
              p/'boundary_probe.cpp',p/'simulator-identity.json',p/'hosted-checks.json',
              p/'prior-findings.json',p/'pr-body-punctuation.json',p/'redaction-receipt.json'])
for f in files:
 text=f.read_text(errors='replace')
 if f.name != 'prepare_publication.py': assert '/home/' not in text,f.name
 assert ('milan-fpga-' + 'management') not in text,f.name
assert len(files)==len(set(files))
(p/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name+'\n' for f in files))
print('Prepared',len(files),'public files; two logs have path-only redactions')
