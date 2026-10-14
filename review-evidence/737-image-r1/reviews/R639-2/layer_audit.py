#!/usr/bin/env python3
"""Independently enumerate each exported layer without extracting its paths."""
import collections
import hashlib
import json
from pathlib import Path
import sys
import tarfile

root=Path(sys.argv[1]).resolve();out=Path(__file__).resolve().parent
lock=json.loads((root/'ci/image/image.lock.json').read_text())
records=[{'tool':'base',**r} for r in lock['base_layers']]+lock['layers']
results=[]
with tarfile.open(out/'scratch/image/image.tar') as archive:
 for r in records:
  counts=collections.Counter();owners=collections.Counter();pax=collections.Counter();suspects=[]
  with archive.extractfile('blobs/'+r['oci_digest'].replace(':','/')) as stream,tarfile.open(fileobj=stream,mode='r|*') as entries:
   for m in entries:
    name=m.name.removeprefix('./')
    counts['members']+=1;counts['regular']+=int(m.isfile());counts['symlinks']+=int(m.issym())
    owners[f'{m.uid}:{m.gid}']+=1
    pax.update(m.pax_headers.keys())
    if name.startswith(('inputs/','recipe/','build/','debs/','build-context/')) or '/.git/' in name or (name.startswith('opt/tsn-gen/') and ('__pycache__' in name or name.endswith(('.pyc','.log','CMakeCache.txt')) or 'CMakeFiles' in name)):
     suspects.append(hashlib.sha256(name.encode()).hexdigest())
    if m.isfile() and name=='opt/ci-image/smoke.py':assert entries.extractfile(m).read()==(root/'ci/image/smoke.py').read_bytes()
    if m.isfile() and name=='opt/ci-image/sources.lock.json':assert entries.extractfile(m).read()==(root/'ci/image/sources.lock.json').read_bytes()
  results.append({'tool':r['tool'],'oci_digest':r['oci_digest'],'counts':dict(counts),'uid_gid_counts':dict(owners),'pax_keys':dict(pax),'forbidden_leftover_member_ids':suspects})
(out/'layer-audit.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
assert all(not r['forbidden_leftover_member_ids'] for r in results)
