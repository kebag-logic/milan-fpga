#!/usr/bin/env python3
"""Extract checksum-verified reference packages into disposable storage only."""
import concurrent.futures,hashlib,io,json,pathlib,subprocess,sys,tarfile,zipfile
from compression import zstd
root=pathlib.Path(sys.argv[1]); out=pathlib.Path(__file__).resolve().parent; scratch=out/'scratch/reference';scratch.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(root/'ci/image'));import build
pins=json.loads((root/'ci/image/sources.lock.json').read_text())
selected=[r for r in pins['packages'] if r['tool'] in ('make','python3.12','python3.12-minimal','libpython3.12-minimal','libpython3.12-stdlib')]
bash=json.loads((out/'reference-bash.json').read_text())
selected.append({'tool':'bash','version':bash['Version'],'filename':pathlib.Path(bash['Filename']).name,'size':int(bash['Size']),'sha256':bash['SHA256'],'url':'https://archive.ubuntu.com/ubuntu/'+bash['Filename']})
def download(row):
 path=scratch/row['filename']; build.verified_download(row,path);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: list(pool.map(download,selected))
for row in selected:
 with (scratch/row['filename']).open('rb') as stream:
  assert stream.read(8)==b'!<arch>\n'
  while header:=stream.read(60):
   size=int(header[48:58]); data=stream.read(size)
   if header[:16].strip().startswith(b'data.tar'):
    if b'.zst' in header[:16]: data=zstd.decompress(data)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
     for member in archive:
      if member.issym() and member.linkname.startswith('/'): continue
      archive.extract(member,scratch/'root',filter='data')
   if size%2: stream.read(1)
row=next(r for r in pins['sources'] if r['tool'].lower()=='pyyaml');path=scratch/row['filename'];build.verified_download(row,path)
with zipfile.ZipFile(path) as archive: archive.extractall(scratch/'python')
(out/'reference-packages.json').write_text(json.dumps([*selected,row],indent=2)+'\n')
for cmd in ([str(scratch/'root/usr/bin/make'),'--version'],[str(scratch/'root/usr/bin/python3.12'),'--version']):
 r=subprocess.run(cmd,capture_output=True,text=True);print(r.returncode,r.stdout,r.stderr)
