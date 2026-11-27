#!/usr/bin/env python3
"""Create and verify the publication manifest, excluding disposable scratch trees."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
report=(root/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R960] NEGATIVE - exact head 73007b4807977517045e8aa485c61ebb8f5ee843'
assert report.splitlines()[-1]=='R960-1 FINISHED'
assert 'SKELETON' not in report
integrity=json.loads((root/'receipts/integrity.json').read_text())
assert integrity['head']=='73007b4807977517045e8aa485c61ebb8f5ee843'
assert integrity['tree']=='eeb3e733b50398a056f5b52325168959c280f45f'
assert not integrity['bad'] and not integrity['index_diff'] and not integrity['status'] and not integrity['gitlinks']
paths=sorted(p for p in root.rglob('*') if p.is_file() and 'scratch' not in p.relative_to(root).parts and p.name!='MANIFEST.sha256')
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix() for p in paths]
(root/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
for line in (root/'MANIFEST.sha256').read_text().splitlines():
    digest,path=line.split('  ',1)
    assert 'scratch' not in Path(path).parts
    assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest,path
print(json.dumps({'published_files':len(paths),'manifest_verified':True,'report_complete':True,'tracked_integrity_verified':True}))
