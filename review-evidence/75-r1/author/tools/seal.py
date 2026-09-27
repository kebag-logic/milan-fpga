"""Index raw evidence and write bounded, recursive SHA-256 manifests."""
from pathlib import Path
import hashlib,json,shutil,sys
p=Path(__file__).resolve().parent.parent
rawroot=Path('/tmp/a386')
redactions=[]
# Keep original peer descriptor names only in private raw storage.
for name in ['census-start.jsonl','census-between.jsonl','census-end.jsonl']:
 f=p/name
 if not f.exists():continue
 original=rawroot/name
 if not original.exists():original.write_bytes(f.read_bytes())
 rows=[json.loads(x) for x in original.read_text().splitlines()]
 for r in rows:
  if r.get('role')=='peer' and r.get('what','').startswith('desc-') and r['response'].get('status')=='SUCCESS':
   b=bytearray.fromhex(r['response']['payload']);b[8:72]=bytes(64);r['response']['payload']=b.hex()
   r['redaction']='reference descriptor object name zeroed'
 f.write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in rows))
 redactions.append(dict(artifact=name,original=str(original),original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),retained_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),change='reference descriptor object names zeroed'))
# Capture-interface labels do not belong in shareable transcripts.
for f in p.glob('*/capture.txt'):
 original=rawroot/f.parent.name/'capture.txt'
 if not original.exists():original.write_bytes(f.read_bytes())
 text=original.read_text()
 import re
 text=re.sub(r'listening on [^,]+,','listening on <capture-interface>,',text)
 f.write_text(text)
 redactions.append(dict(artifact=str(f.relative_to(p)),original=str(original),original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),retained_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),change='capture interface role label'))
f=p/'capture-interface.txt'
if f.exists():
 original=rawroot/'capture-interface.txt'
 if not original.exists():original.write_bytes(f.read_bytes())
 f.write_text('Initial capture interface absent. Temporary driver restored the same approved tap interface, UP with carrier. Original interface metadata is indexed privately.\n')
 redactions.append(dict(artifact=f.name,original=str(original),original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),retained_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),change='interface metadata replaced by roles'))
for d in p.rglob('__pycache__'):
 shutil.rmtree(d)
(p/'redaction.json').write_text(json.dumps(redactions,indent=2)+'\n')
raws=[]
for f in sorted(rawroot.rglob('*')):
 if f.is_file():
  b=f.read_bytes();raws.append(dict(identifier=str(f.relative_to(rawroot)),path=str(f),size=len(b),sha256=hashlib.sha256(b).hexdigest()))
(p/'RAW-ARTIFACTS.json').write_text(json.dumps(raws,indent=2)+'\n')
# Each directory authenticates its immediate files and child manifests.
def manifest(d):
 for child in sorted(d.iterdir()):
  if child.is_dir():manifest(child)
 entries=[f for f in sorted(d.iterdir()) if f.is_file() and f.name!='MANIFEST.sha256']
 entries += [child/'MANIFEST.sha256' for child in sorted(d.iterdir()) if child.is_dir()]
 (d/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(d))+'\n' for f in entries))
manifest(p)
files=[f for f in p.rglob('*') if f.is_file()]
assert all(f.stat().st_size<=200000 for f in files),'oversized retained file'
for m in p.rglob('MANIFEST.sha256'):
 for line in m.read_text().splitlines():
  sha,name=line.split('  ',1);assert hashlib.sha256((m.parent/name).read_bytes()).hexdigest()==sha
print(len(raws),'raw artifacts;',sum(r['size'] for r in raws),'bytes;',len(files),'packet files; manifests PASS')
print('Largest retained file:',max((f.stat().st_size,str(f.relative_to(p))) for f in files))
