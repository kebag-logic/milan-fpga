#!/usr/bin/env python3
"""Verify selected publication hashes and their binding to the exact reviewed source."""
import hashlib,json,pathlib,subprocess
p=pathlib.Path(__file__).resolve().parents[1]
a=p/'public/author-r4'
outer={e['file']:e for e in json.loads((p/'public/MANIFEST.json').read_text())}
checked=[]
for f in sorted(a.iterdir()):
    key='author-r4/'+f.name
    if key in outer:
        entry=outer[key];actual=hashlib.sha256(f.read_bytes()).hexdigest()
        assert actual==entry['published_sha256'],key
        checked.append({'file':key,'sha256':actual,'path_redacted':entry.get('path_redacted')})
head=json.loads((a/'r4-head.json').read_text())
assert head['head']==subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for path,m in head['files'].items():
    data=pathlib.Path(path).read_bytes()
    assert len(data)==m['bytes'] and hashlib.sha256(data).hexdigest()==m['sha256'],path
images=json.loads((a/'r4-image-hashes.json').read_text())
assert len(images)==5
for i in images:assert i['bytes_before']==i['bytes_after'] and i['sha256_before']==i['sha256_after']
changed=subprocess.check_output(['git','diff','--name-only','a0f39ad4..HEAD'],text=True).splitlines()
assert not any(x.startswith(('sw/','configs/','hdl/','syn/','third_party/','protocol-processor','gptp-processor')) for x in changed)
result={'evidence_revision':'beeb9d6cbdd2d6abc75f2cb3cc21d9e6f33efa9c','head':head['head'],'published_manifest_entries_verified':checked,'source_files_verified':list(head['files']),'changed_paths':changed,'author_image_pairs':images,'limits':['Original author checksums precede documented publication path redaction. Published bytes were checked against the outer publication manifest.','Author execution receipts are independently matched to source; no manager source bank asserted.']}
(p/'receipts/public-evidence-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS',len(checked),'published manifest entries;',len(head['files']),'source files;',len(images),'image pairs')
