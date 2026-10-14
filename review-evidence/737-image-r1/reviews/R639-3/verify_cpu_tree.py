#!/usr/bin/env python3
"""Compare installed recursive CPU files with authenticated sources and real patch application."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

root=Path(sys.argv[1]).resolve(); work=Path(sys.argv[2]).resolve()
packet=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'ci/image'))
import image_archive
pins=json.loads((root/'ci/image/sources.lock.json').read_text())
_,manifest,_=image_archive.metadata(work/'image.tar',pins['platform'])
prefix='pythondata_cpu_vexiiriscv/verilog/ext/VexiiRiscv'
with tempfile.TemporaryDirectory(dir=packet/'scratch',prefix='cpu-proof-') as temporary:
 stage=Path(temporary)
 located={'VexiiRiscv':stage/prefix}
 pending=[r for r in pins['sources'] if r['tool']=='VexiiRiscv' or r.get('parent')]
 # Only the recursive CPU family, excluding other tool families.
 selected=[]
 while True:
  ready=[r for r in pending if r['tool']=='VexiiRiscv' or r.get('parent') in located]
  if not ready:break
  for row in ready:
   target=located.get(row['tool']) or located[row['parent']]/row['path']
   located[row['tool']]=target; target.mkdir(parents=True,exist_ok=True)
   archive=work/'context'/row['filename']
   assert hashlib.sha256(archive.read_bytes()).hexdigest()==row['sha256']
   with tarfile.open(archive) as entries:
    for member in entries:
     name=member.name.partition('/')[2]
     if not name:continue
     member.name=name
     entries.extract(member,target,filter='data')
   pending.remove(row); selected.append({'tool':row['tool'],'pin':row['version'],'source_sha256':row['sha256']})
 patch=root/'sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch'
 subprocess.run(['git','apply',str(patch)],cwd=stage,check=True,capture_output=True)
 wanted={}
 for path in sorted((stage/prefix).rglob('*')):
  name=path.relative_to(stage/prefix).as_posix()
  if path.is_symlink(): wanted[name]=['symlink',str(path.readlink())]
  elif path.is_file(): wanted[name]=['file',hashlib.sha256(path.read_bytes()).hexdigest(),bool(path.stat().st_mode&0o111)]
 found={}; installed='opt/python/lib/python3.12/site-packages/'+prefix+'/'
 with tarfile.open(work/'image.tar') as outer:
  for layer in manifest['layers']:
   with image_archive.blob(outer,layer['digest']) as stream,tarfile.open(fileobj=stream,mode='r|*') as entries:
    for member in entries:
     name=member.name.removeprefix('./')
     if not name.startswith(installed):continue
     name=name[len(installed):]
     if member.issym():found[name]=['symlink',member.linkname]
     elif member.isfile():found[name]=['file',hashlib.file_digest(entries.extractfile(member),'sha256').hexdigest(),bool(member.mode&0o111)]
 errors={'missing':sorted(wanted.keys()-found.keys()),'extra':sorted(found.keys()-wanted.keys()),
         'changed':sorted(k for k in wanted.keys()&found.keys() if wanted[k]!=found[k])}
 assert not any(errors.values()),{k:len(v) for k,v in errors.items()}
 result={'sources':selected,'patch_sha256':hashlib.sha256(patch.read_bytes()).hexdigest(),
         'files_and_links':len(found),'differences':errors,'claim':'Exact file/link/execute-bit equality; no CPU build or hardware claim.'}
 (packet/'cpu-tree-verification.json').write_text(json.dumps(result,indent=2)+'\n')
 print(f'PASS: {len(found)} CPU files and links match six public source archives plus committed patch.')
