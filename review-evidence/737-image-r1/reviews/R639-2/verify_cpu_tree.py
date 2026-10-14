#!/usr/bin/env python3
"""Compare recursive public source members with the image's CPU layer."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile

root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
cache=out/'scratch/image/context'
pins=json.loads((root/'ci/image/sources.lock.json').read_text())
lock=json.loads((root/'ci/image/image.lock.json').read_text())
rows={r['tool']:r for r in pins['sources']}
places={'VexiiRiscv':''}
while True:
 before=len(places)
 for name,row in rows.items():
  if row.get('parent') in places:
   places[name]='/'.join(filter(None,[places[row['parent']],row['path']]))
 if len(places)==before:break
expected={}
original=None
for name,prefix in places.items():
 row=rows[name];path=cache/row['filename']
 with path.open('rb') as f: assert hashlib.file_digest(f,'sha256').hexdigest()==row['sha256']
 with tarfile.open(path) as tar:
  for m in tar:
   rel=m.name.partition('/')[2]
   if not rel or m.isdir():continue
   key='/'.join(filter(None,[prefix,rel]))
   if m.isfile():
    data=tar.extractfile(m).read()
    expected[key]=['file',hashlib.sha256(data).hexdigest(),bool(m.mode&0o111)]
    if name=='VexiiRiscv' and rel=='src/main/scala/vexiiriscv/soc/litex/Soc.scala':original=data
   elif m.issym():expected[key]=['link',m.linkname,False]
   else:raise ValueError('unsupported member type')
patch=root/'sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch'
text=patch.read_bytes()
target=next(line[6:].decode() for line in text.splitlines() if line.startswith(b'--- a/'))
work=out/'scratch/cpu-patch'; dest=work/target
dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(original)
proc=subprocess.run(['patch','-p1','--batch','--fuzz=0'],input=text,cwd=work,capture_output=True)
assert proc.returncode==0,proc.stderr.decode()
expected['src/main/scala/vexiiriscv/soc/litex/Soc.scala'][1]=hashlib.sha256(dest.read_bytes()).hexdigest()
layer=next(r for r in lock['layers'] if r['tool']=='litex')
prefix='opt/python/lib/python3.12/site-packages/pythondata_cpu_vexiiriscv/verilog/ext/VexiiRiscv/'
actual={}
with tarfile.open(out/'scratch/image/image.tar') as archive:
 with archive.extractfile('blobs/'+layer['oci_digest'].replace(':','/')) as stream, tarfile.open(fileobj=stream,mode='r|*') as tar:
  for m in tar:
   if not m.name.startswith(prefix) or m.isdir():continue
   key=m.name.removeprefix(prefix)
   if m.isfile():actual[key]=['file',hashlib.sha256(tar.extractfile(m).read()).hexdigest(),bool(m.mode&0o111)]
   elif m.issym():actual[key]=['link',m.linkname,False]
   else:raise ValueError('unsupported image member type')
missing=sorted(expected.keys()-actual.keys());extra=sorted(actual.keys()-expected.keys())
changed=sorted(k for k in expected.keys()&actual.keys() if expected[k]!=actual[k])
result={'sources':{name:rows[name]['version'] for name in places},'expected_files':len(expected),'actual_files':len(actual),'missing':missing,'extra':extra,'changed':changed,'patch_sha256':hashlib.sha256(text).hexdigest(),'patched_member_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'tree_sha256':hashlib.sha256(json.dumps(actual,sort_keys=True).encode()).hexdigest()}
(out/'cpu-tree-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert not missing and not extra and not changed
