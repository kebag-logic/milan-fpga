#!/usr/bin/env python3
"""Seal and independently check the publishable review packet."""
import hashlib,json,pathlib,re
p=pathlib.Path(__file__).resolve().parents[1]
head='59354ffe75697e17a16fd117d9ba853e104394bc'
report=(p/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R633] POSITIVE - exact head '+head
assert report.splitlines()[-1]=='R633-4 FINISHED'
assert 'SKELETON' not in report
assert report.count('| CLEAN |')==5
accepted=['ci-scope','ci-events','runner-workflow','prior-round1','prior-round2','prior-external','documentation','mutation-R01','mutation-R02-final','mutation-R03','mutation-before','linked-images-accepted','image-controls-final']
for name in accepted:
    meta=json.loads((p/'receipts'/(name+'.json')).read_text())
    assert meta['returncode']==0 and meta['source_head']==head,name
    assert (p/'receipts'/(name+'.rc')).read_text().strip()=='0',name
assert json.loads((p/'receipts/integrity-before.json').read_text())==json.loads((p/'receipts/integrity-final.json').read_text())
for pair in json.loads((p/'receipts/image-comparison.json').read_text())['pairs']:
    assert pair['equal'] and pair['sha256_head']==pair['sha256_base']
expected=json.loads((p/'receipts/public-provenance.json').read_text())['files']
for path in (p/'scripts/prior').iterdir():
    match=[x for x in expected if x['path'].endswith('/'+path.name)]
    assert len(match)==1 and hashlib.sha256(path.read_bytes()).hexdigest()==match[0]['sha256'],path
files=[p/'REPORT.md',p/'REPRODUCE.md',p/'source.diff']
for folder in ['scripts','receipts','public']:
    files.extend(x for x in (p/folder).rglob('*') if x.is_file())
assert all(not x.is_symlink() for x in files)
for f in files:
    data=f.read_bytes()
    assert bytes([47,104,111,109,101,47,97,108,101,120,47]) not in data,f
    assert str(p/'scratch').encode() not in data,f
rows=[hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(p).as_posix() for f in sorted(set(files))]
(p/'MANIFEST.sha256').write_text('\n'.join(rows)+'\n')
for row in rows:
    digest,rel=row.split('  ',1)
    assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==digest,rel
print('PASS packet:',len(rows),'files;',len(accepted),'accepted executions; all five lenses CLEAN; five image pairs identical')
