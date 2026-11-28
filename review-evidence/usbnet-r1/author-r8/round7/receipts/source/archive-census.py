"""Archive the complete native evidence without changing a trace byte."""
import concurrent.futures,gzip,hashlib,json,shutil
from pathlib import Path
root=Path('$VALIDATION_STORAGE/usbnet-a855/round7/census')
out=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts/census')
manifest=json.loads((root/'manifest.json').read_text())
completed=json.loads((root/'completed.json').read_text())
expected={(v,g) for v,gs in manifest['groups'].items() for g in gs}
assert {(r['variant'],r['group']) for r in completed}==expected
out.mkdir(exist_ok=True)
def one(row):
 source=root/row['variant']/'results'/row['group']
 target=out/row['variant']/'results'/row['group']
 target.parent.mkdir(parents=True,exist_ok=True)
 raw=hashlib.sha256();length=0
 dest=target.with_suffix(target.suffix+'.log.gz')
 original=source.with_suffix(source.suffix+'.log')
 with original.open('rb') as src,dest.open('wb') as f,gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0,compresslevel=1) as zipped:
  while chunk:=src.read(1048576):raw.update(chunk);length+=len(chunk);zipped.write(chunk)
 assert raw.hexdigest()==row['trace_sha256']
 for suffix in ('.json','.txt','.status'):
  src=source.with_suffix(source.suffix+suffix)
  shutil.copyfile(src,target.with_suffix(target.suffix+suffix))
 return dict(case=row['variant']+'/'+row['group'],path=str(dest.relative_to(out)),raw_bytes=length,raw_sha256=raw.hexdigest(),gzip_sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(one,completed))
for variant in manifest['groups']:
 directory=root/variant;target=out/variant
 for name in ('build.json','budget_config.hpp','usbnet-extension.json','usbnet_census_main.cpp','usbnet_egress_queue.hpp'):
  shutil.copyfile(directory/name,target/name)
 spec=json.loads((directory/'build.json').read_text())
 for name in ('ctrl_app.elf','ctrl_app.map'):
  shutil.copyfile(Path(spec['elf']).with_name(name),target/name)
 for source in (directory/'results').glob('*journal*'):
  if source.is_file():shutil.copyfile(source,target/'results'/source.name)
for source in root.iterdir():
 if source.is_file():shutil.copyfile(source,out/source.name)
(out/'ARCHIVE.json').write_text(json.dumps(dict(cases=rows,manifest=manifest),indent=2)+'\n')
print('ARCHIVED',len(rows),'complete traces',sum(r['raw_bytes'] for r in rows),'bytes')
