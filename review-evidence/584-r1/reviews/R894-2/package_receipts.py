#!/usr/bin/env python3
"""Extract unmodified runtime stdout, save public indexes, and hash publishable files."""
import hashlib, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]).resolve()
for raw,dest in [('ship8-build.raw','ship8-clean.log'),('freshness.raw','freshness.log')]:
    b=(out/'scratch'/raw).read_bytes()
    marker=b'./obj_ship8/Vmilan_dp_ship8\n'
    assert marker in b
    b=b.split(marker,1)[1]
    b=b.split(b'make: Leaving directory',1)[0]
    (out/dest).write_bytes(b)
commit='e3127c9139ae456ef671b098eab55bed6d41d0f4'
for name in ['author-r1/receipts/INDEX.md','author-r2/receipts/INDEX.md','author-r2/receipts/f5/round1-INDEX-corrected.md','MANIFEST.json']:
    b=subprocess.check_output(['git','show',commit+':review-evidence/584-r1/'+name],cwd=repo)
    p=out/'public-receipts'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
files=sorted(p for p in out.rglob('*') if p.is_file() and p.relative_to(out).parts[0]!='scratch' and p.name not in ('MANIFEST.sha256','REPORT.md') and '__pycache__' not in p.parts)
(out/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(out))+'\n' for p in files))
print('Publishable files:',len(files),'+ REPORT.md')
