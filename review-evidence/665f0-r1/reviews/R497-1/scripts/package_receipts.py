#!/usr/bin/env python3
"""Keep local-path originals private and checksum all publishable packet files."""
import hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parents[1]
private=p/'scratch/raw-receipts';private.mkdir(exist_ok=True)
home=str(pathlib.Path.home());redactions=[]
for f in sorted((p/'receipts').iterdir()):
    if not f.is_file() or f.name=='path-redactions.json':continue
    data=f.read_bytes()
    if home.encode() not in data:continue
    (private/f.name).write_bytes(data)
    public=data.replace(home.encode(),b'${REVIEW_HOME}')
    f.write_bytes(public)
    redactions.append({'path':str(f.relative_to(p)),'replacement':'machine-local home prefix -> ${REVIEW_HOME}',
      'count':data.count(home.encode()),'original_sha256':hashlib.sha256(data).hexdigest(),
      'published_sha256':hashlib.sha256(public).hexdigest()})
(p/'receipts/path-redactions.json').write_text(json.dumps(redactions,indent=2)+'\n')
files=[p/'REPORT.md',*sorted((p/'scripts').glob('*')),*sorted((p/'receipts').glob('*'))]
files=[f for f in files if f.is_file()]
report=(p/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R497] NEGATIVE - exact head 0bfef4987eede4b022b17c7b2f56d079ff84893b'
assert report.splitlines()[-1]=='R497-1 FINISHED'
assert 'SKELETON' not in report and '[R497] INCOMPLETE' not in report
manifest=''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(p))+'\n' for f in files)
(p/'MANIFEST.sha256').write_text(manifest)
print('Publishable files:',len(files),'(all listed; scratch excluded)')
print('Home-path-redacted receipts:',len(redactions))
