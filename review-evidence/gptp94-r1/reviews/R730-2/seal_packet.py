#!/usr/bin/env python3
"""Seal publishable artifacts; disposable trees are never included."""
import hashlib, pathlib
root=pathlib.Path(__file__).resolve().parent
report=(root/'REPORT.md').read_text()
assert report.startswith('[R730] POSITIVE - exact head 409c3075a6c5525d283de5a93584ad87a4528137\n')
assert report.rstrip().endswith('R730-2 FINISHED') and 'SKELETON' not in report
rows=[]
for p in sorted(root.rglob('*')):
    rel=p.relative_to(root)
    if not p.is_file() or rel.parts[0]=='scratch' or p.name=='MANIFEST.sha256':continue
    rows.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(rel))
(root/'MANIFEST.sha256').write_text('\n'.join(rows)+'\n')
print('Sealed',len(rows),'publishable files; scratch excluded')
