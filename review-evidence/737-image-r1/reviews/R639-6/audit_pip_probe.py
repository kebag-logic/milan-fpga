#!/usr/bin/env python3
"""Plant a real, harmless offline pip install only into disposable review storage."""
import hashlib,io,json,os,pathlib,sys,tarfile,tempfile,zipfile
from compression import zstd
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(root/'ci/image'));import build,exec_audit
pins=json.loads((root/'ci/image/sources.lock.json').read_text())
row=next(r for r in pins['packages'] if r['tool']=='python3-pip-whl')
ref=out/'scratch/reference';archive=ref/row['filename'];build.verified_download(row,archive)
stream=io.BytesIO(archive.read_bytes()); assert stream.read(8)==b'!<arch>\n'
while header:=stream.read(60):
 size=int(header[48:58]);data=stream.read(size)
 if header[:16].strip().startswith(b'data.tar'):
  if b'.zst' in header[:16]:data=zstd.decompress(data)
  with tarfile.open(fileobj=io.BytesIO(data)) as tar:
   member=next(m for m in tar if m.name.endswith('.whl'))
   with zipfile.ZipFile(io.BytesIO(tar.extractfile(member).read())) as wheel: wheel.extractall(ref/'python')
 if size%2:stream.read(1)
with tempfile.TemporaryDirectory(dir=out/'scratch',prefix='pip-probe-') as tmp:
 base=pathlib.Path(tmp);wheel=base/'review_probe-0.0.1-py3-none-any.whl'
 files={'review_probe.py':'VALUE = 1\n','review_probe-0.0.1.dist-info/METADATA':'Metadata-Version: 2.1\nName: review-probe\nVersion: 0.0.1\n',
 'review_probe-0.0.1.dist-info/WHEEL':'Wheel-Version: 1.0\nGenerator: review\nRoot-Is-Purelib: true\nTag: py3-none-any\n'}
 files['review_probe-0.0.1.dist-info/RECORD']=''.join(name+',,\n' for name in files)+'review_probe-0.0.1.dist-info/RECORD,,\n'
 with zipfile.ZipFile(wheel,'w') as z:
  for name,text in files.items():z.writestr(name,text)
 env={'PATH':'/usr/bin:/bin','HOME':str(base),'PYTHONHOME':str(ref/'root/usr'),'PYTHONPATH':str(ref/'python'),'PYTHONDONTWRITEBYTECODE':'1','PIP_NO_INDEX':'1'}
 argv=[str(ref/'root/usr/bin/python3.12'),'-m','pip','--isolated','install','--disable-pip-version-check','--no-index','--no-deps','--no-compile','--target',str(base/'installed'),str(wheel)]
 result=exec_audit.audit_step('offline harmless installer',argv,base,env,exec_audit.allowlist())
 result['installed']=(base/'installed/review_probe.py').read_text()=='VALUE = 1\n'
 result['pip_pin']={k:row[k] for k in ('version','sha256','url')}
 text=json.dumps(result,indent=2).replace(str(out),'$PACKET')+'\n';(out/'audit-pip-probe.json').write_text(text);print(text)
