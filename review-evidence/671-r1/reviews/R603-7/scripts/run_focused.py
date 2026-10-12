#!/usr/bin/env python3
"""Foreground focused checks, at most two concurrent processes."""
import concurrent.futures,os,pathlib,subprocess,sys,time
R=pathlib.Path(sys.argv[1]).resolve();P=pathlib.Path(__file__).resolve().parents[1]
env=dict(os.environ,TMPDIR=str(P/'scratch'),PYTHONDONTWRITEBYTECODE='1',PYTHONUNBUFFERED='1')
checks=[('capture',[sys.executable,'scripts/check_nvm_capture.py'],0)]
checks += [('capture-'+name,[sys.executable,'scripts/check_nvm_capture.py','--mutation',name],1) for name in ['bytes','records','clock','ignore-off-timing','receipt-opt-out']]
checks += [('capture-provenance',[sys.executable,str(P/'scripts/audit_capture.py'),str(R)],0),('docs',[sys.executable,'scripts/docs_check.py'],0),('diff',['git','diff','--check','c6bd08c6..HEAD'],0)]
def run(item):
 name,cmd,want=item;start=time.monotonic()
 with (P/'receipts'/f'{name}.log').open('w') as f:
  result=subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=180)
  f.write(f'\nRETURN CODE: {result.returncode}; EXPECTED: {want}; ELAPSED: {time.monotonic()-start:.2f} s\n')
 (P/'receipts'/f'{name}.rc').write_text(str(result.returncode)+'\n')
 return dict(name=name,rc=result.returncode,expected=want,ok=result.returncode==want)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,checks))
(P/'receipts/focused-summary.json').write_text(__import__('json').dumps(rows,indent=2)+'\n')
for row in rows:print(row)
raise SystemExit(not all(row['ok'] for row in rows))
