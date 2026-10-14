#!/usr/bin/env python3
"""Extract only the image's reference interpreter and pure parser dependency."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import tarfile

checkout=Path(sys.argv[1]).resolve()
archive=Path(sys.argv[2])
packet=Path(__file__).resolve().parent
destination=packet/'scratch/reference-python'
sys.path.insert(0,str(checkout/'ci/image'))
import image_archive
descriptor,manifest,config=image_archive.metadata(archive,'linux/amd64')
expected=json.loads((checkout/'ci/image/image.lock.json').read_text())
assert descriptor['digest']==expected['image_digest']
copied=[]
with tarfile.open(archive) as outer:
 for layer in manifest['layers']:
  with image_archive.blob(outer,layer['digest']) as stream:
   assert 'sha256:'+hashlib.file_digest(stream,'sha256').hexdigest()==layer['digest']
  with image_archive.blob(outer,layer['digest']) as stream,tarfile.open(fileobj=stream,mode='r|*') as inner:
   for member in inner:
    name=member.name.removeprefix('./')
    if not (name=='usr/bin/python3.12' or name.startswith('usr/lib/python3.12/') or name.startswith('opt/python/lib/python3.12/site-packages/yaml/')):continue
    if not member.isfile():continue
    parts=PurePosixPath(name)
    assert not parts.is_absolute() and '..' not in parts.parts
    target=destination/name
    target.parent.mkdir(parents=True,exist_ok=True)
    data=inner.extractfile(member).read()
    target.write_bytes(data); target.chmod(member.mode&0o777)
    copied.append({'path':name,'sha256':hashlib.sha256(data).hexdigest()})
(packet/'reference-python-extraction.json').write_text(json.dumps({'image':descriptor['digest'],'files':copied},indent=2)+'\n')
print(f'Extracted {len(copied)} regular interpreter/library files, no links or device nodes; image layers authenticated.')
