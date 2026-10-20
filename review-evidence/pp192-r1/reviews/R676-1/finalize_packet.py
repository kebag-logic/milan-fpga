#!/usr/bin/env python3
"""Mask local build-path prefixes and inventory the publishable packet."""
import hashlib, json, pathlib, re, subprocess, sys
p=pathlib.Path(__file__).resolve().parent
root=pathlib.Path(sys.argv[1]).resolve()
with (p/'checkout-verification.json').open('w') as log:
    subprocess.run([sys.executable,str(p/'verify_checkout.py'),str(root)],stdout=log,check=True)
records=[]
for f in sorted(p.rglob('*.log')):
    rel=f.relative_to(p)
    if rel.parts[0] in ('scratch','public'): continue
    data=f.read_bytes(); s=data.decode()
    s=s.replace(str(p/'scratch'),'<scratch>').replace(str(root),'<review-checkout>').replace(str(p),'<packet>')
    s=re.sub(r'/home/[^/]+/\.local/share/containers/storage/overlay/[^/]+/diff/usr/share/verilator','<frontend-root>',s)
    s=s.replace('$VALIDATION_TOOLS/pinned-verilator-5.050','<pinned-frontend-dir>')
    published=s.encode()
    original=p/'scratch/raw-receipts'/rel
    if not original.exists():
        original.parent.mkdir(parents=True,exist_ok=True); original.write_bytes(data)
    records.append({'path':str(rel),'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'published_sha256':hashlib.sha256(published).hexdigest(),'change':'local build-path prefixes only'})
    f.write_bytes(published)
(p/'receipt-redactions.json').write_text(json.dumps(records,indent=2)+'\n')
files=[f for f in p.rglob('*') if f.is_file() and f.relative_to(p).parts[0]!='scratch' and f.name!='MANIFEST.sha256']
(p/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(p))+'\n' for f in sorted(files)))
print('Manifest files:',len(files))
