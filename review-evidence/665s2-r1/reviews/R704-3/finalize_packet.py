#!/usr/bin/env python3
"""Normalize local metadata paths, verify preserved probe bytes, and hash the publishable packet."""
import hashlib,json,os,subprocess
from pathlib import Path
p=Path(os.environ['REVIEW_PACKET']);root=Path(os.environ['REVIEW_ROOT'])
identity=subprocess.check_output(['python3','-B',str(p/'verify_identity.py')],text=True)
(p/'identity-final.json').write_text(identity)
assert json.loads(identity)==json.loads((p/'identity-initial.json').read_text())
for f in (p/'prior').glob('*.py'):
 assert f.read_bytes()==(p/'scratch/public/reviews/R704-2'/f.name).read_bytes(),f.name
checks=(p/'selftest.log').read_text().splitlines()
assert sum(x.startswith('PASS:') for x in checks)==81
assert sum(x.startswith('MUTANT caught:') for x in checks)==52
assert (p/'native-audit.rc').read_text().strip()=='0'
assert len(json.loads((p/'native-audit.json').read_text())['groups'])==12
receipt=[]
substitutions=[(str(root),'<checkout>'),(str(p),'<packet>')]
for env,key in [('PRODUCT_ENV_ROOT','<product-environment>'),('COMPILER_ROOT','<compiler-root>'),('SIMULATOR_ROOT','<simulator-root>')]:
 if os.environ.get(env):substitutions.append((os.environ[env],key))
for f in sorted(p.rglob('*')):
 rel=f.relative_to(p)
 if not f.is_file() or rel.parts[0]=='scratch' or f.name in ('MANIFEST.sha256','REPORT.md','receipt-index.json'):continue
 before=f.read_bytes();after=before
 for old,new in substitutions:after=after.replace(old.encode(),new.encode())
 if rel.parts[0]=='prior' or (rel.parts[0] in ('measurements','native-probes') and f.suffix=='.log'):
  assert before==after,('raw receipt needs redaction',str(rel))
 if before!=after:f.write_bytes(after)
 receipt.append(dict(file=str(rel),original_sha256=hashlib.sha256(before).hexdigest(),published_sha256=hashlib.sha256(after).hexdigest(),path_normalized=before!=after))
(p/'receipt-index.json').write_text(json.dumps(receipt,indent=2)+'\n')
files=[f for f in sorted(p.rglob('*')) if f.is_file() and f.relative_to(p).parts[0]!='scratch' and f.name!='MANIFEST.sha256']
(p/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(p))+'\n' for f in files))
report=(p/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R704] POSITIVE - exact head f887663852d118e810ef690c3dd5cf9fe2292588'
assert report.splitlines()[-1]=='R704-3 FINISHED' and 'SKELETON' not in report
print('PASS: final identity, preserved prior scripts and raw traces, 81 checks/52 controls, 12 exact native groups;',len(files),'manifest entries')
