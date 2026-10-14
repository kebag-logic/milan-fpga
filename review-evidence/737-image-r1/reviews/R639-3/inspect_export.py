#!/usr/bin/env python3
"""Authenticate a supplied OCI export, inspect every layer, without daemon access."""
import hashlib
import json
from pathlib import Path
import sys
import tarfile
import time

root=Path(sys.argv[1]).resolve()
work=Path(sys.argv[2]).resolve()
packet=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'ci/image'))
import image_archive
import image_lock
import privacy
import build
pins=json.loads((root/'ci/image/sources.lock.json').read_text())
lock=json.loads((root/'ci/image/image.lock.json').read_text())
started=time.monotonic()
archive=work/'image.tar'
with archive.open('rb') as stream:
    export_sha=hashlib.file_digest(stream,'sha256').hexdigest()
published=json.loads((packet/'scratch/public/round3-a-artifacts.json').read_text())
assert export_sha==next(r['sha256'] for r in published['files'] if r['artifact']=='cold-a/image.tar')
upstream=privacy.provenance(pins,work/'context',privacy.Policy())
measured=image_archive.inspect(archive,pins['platform'],upstream)
image_lock.validate(lock,pins,build.recipe_digest(),build.layer_records(pins))
image_lock.verify_artifact(lock,measured)
(packet/'image-authentication.json').write_text(json.dumps(measured,indent=2,sort_keys=True)+'\n')
(packet/'image-history.json').write_text(json.dumps(measured['history'],indent=2)+'\n')
descriptor,manifest,config=image_archive.metadata(archive,pins['platform'])
counts=[]
matched={}
with tarfile.open(archive) as outer:
    for index,layer in enumerate(manifest['layers']):
        row={'index':index,'digest':layer['digest'],'members':0,'regular':0,'symlinks':0,'oracle_members':[],'leftovers':[]}
        with image_archive.blob(outer,layer['digest']) as stream, tarfile.open(fileobj=stream,mode='r|*') as entries:
            for item in entries:
                name=item.name.removeprefix('./')
                row['members']+=1; row['regular']+=item.isfile(); row['symlinks']+=item.issym()
                if name.startswith(('build/','inputs/','recipe/')) or '/.git/' in name or name.endswith('/.git'):
                    row['leftovers'].append(hashlib.sha256(name.encode()).hexdigest())
                if name.startswith('opt/tsn-gen/') and item.isfile():
                    row['oracle_members'].append(name)
                for target,source in (('opt/ci-image/smoke.py','ci/image/smoke.py'),('opt/ci-image/sources.lock.json','ci/image/sources.lock.json')):
                    if name==target and item.isfile():
                        actual=hashlib.sha256(entries.extractfile(item).read()).hexdigest()
                        assert actual==hashlib.sha256((root/source).read_bytes()).hexdigest()
                        matched[source]=actual
        counts.append(row)
assert len(matched)==2
assert not any(row['leftovers'] for row in counts)
result={'export_sha256':export_sha,'image_digest':descriptor['digest'],'config_digest':manifest['config']['digest'],
        'layers':counts,'matched_recipe_files':matched,'allowances':len(measured['upstream_allowances']),
        'history_entries':len(config['history']),'environment':config['config'].get('Env',[]),
        'seconds':round(time.monotonic()-started,3),
        'method':'Read-only archive inspection; no daemon, privilege or image execution. Every member scanned by recipe policy; independent member census and leftover checks.'}
(packet/'image-inspection.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('layers','environment')},indent=2))
