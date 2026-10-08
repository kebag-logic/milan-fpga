#!/usr/bin/env python3
import argparse,concurrent.futures,json,os,subprocess,sys,time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('spec',type=Path);ap.add_argument('--workers',type=int,default=4);ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--source',type=Path,default=Path.cwd());a=ap.parse_args();p=a.packet.resolve();r=a.source.resolve()
spec=json.loads(a.spec.read_text());env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(p/'scratch'))
def run(task):
 name=task['name'];argv=[x.replace('@SOURCE@',str(r)).replace('@PACKET@',str(p)).replace('@DEPENDENCIES@',os.environ.get('REVIEW_DEPENDENCIES','')).replace('@DOCS_PYTHON@',os.environ.get('REVIEW_DOCS_PYTHON','python3')) for x in task['argv']]
 assert all(argv), 'Set REVIEW_DEPENDENCIES for the image runtime sources'
 start=time.monotonic()
 with (p/'receipts'/f'{name}.log').open('w') as log:
  result=subprocess.run(argv,cwd=r,env=env,stdout=log,stderr=subprocess.STDOUT)
 (p/'receipts'/f'{name}.rc').write_text(str(result.returncode)+'\n')
 row={'name':name,'argv':argv,'rc':result.returncode,'seconds':round(time.monotonic()-start,3)}
 print(json.dumps(row),flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool: rows=list(pool.map(run,spec))
(p/'receipts'/(a.spec.stem+'-execution.json')).write_text(json.dumps(rows,indent=2)+'\n')
