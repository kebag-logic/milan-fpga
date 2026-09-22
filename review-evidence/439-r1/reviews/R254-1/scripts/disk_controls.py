import copy, json, os, pathlib, subprocess, sys, time, yaml
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve()
source=(root/'scripts/ci_events.py').read_text();cases=out/'disposable/disk';cases.mkdir(exist_ok=True)
rows=json.loads((out/'receipts/inventory.json').read_text());receipts=[]
files=['docs/testing/CI_WORKFLOWS.md',*[str(p.relative_to(root)) for p in (root/'.github/workflows').iterdir() if p.is_file()]]
def case(name,row,body=None,record=None,base=False,selftest=False):
 d=cases/name;d.mkdir(exist_ok=True)
 for rel in files:
  p=d/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((root/rel).read_bytes())
 if body is not None:
  p=d/row['path'];wf=yaml.safe_load(p.read_text());wf['jobs'][row['job']]['steps'][row['step']-1]['run']=body
  p.write_text(yaml.safe_dump(wf,sort_keys=False))
 script=d/'ci_events.py'
 text=(out/'disposable/base-ci_events.py').read_text() if base else source
 if record is not None:
  patch=f"RTL_SEQUENCE_PINS[{(row['path'],row['job'])!r}][{row['step']-1}]['run'] = {tuple(record)!r}\n\n"
  text=text.replace('if __name__ == "__main__":',patch+'if __name__ == "__main__":')
 script.write_text(text)
 for mode in ['--check']+(['--selftest'] if selftest else []):
  argv=['rtk','proxy','python3','-B',str(script),mode,'--root',str(d)]
  start=time.time();r=subprocess.run(argv,capture_output=True,timeout=120,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  label=name+mode
  (out/'receipts'/(label+'.stdout')).write_bytes(r.stdout);(out/'receipts'/(label+'.stderr')).write_bytes(r.stderr)
  receipts.append({'label':label,'argv':argv,'exit':r.returncode,'seconds':round(time.time()-start,3),'stdout':label+'.stdout','stderr':label+'.stderr'})
  expect=0 if base or record is not None and body is not None else 1
  assert r.returncode==expect,(label,r.returncode,r.stdout.decode(),r.stderr.decode())
  if expect==1: assert f"job `{row['job']}` step {row['step']}" in r.stdout.decode()
sha=next(r for r in rows if r['job']=='full-ci-gate');ls=sha['canonical']
start=ls.index('if [ "$head" != "$GITHUB_SHA" ]; then');end=ls.index('fi',start)
for name,changed in [('drop-block',ls[:start]+ls[end+1:]),('exit-true',['true' if l=='exit 1' else l for l in ls])]:
 case('base-'+name,sha,'\n'.join(changed),base=True)
 case('source-'+name,sha,'\n'.join(changed))
for row in [rows[0],sha]:
 name=row['job'];maintained=[*row['canonical'],'echo R254_disk_maintenance']
 case(name+'-workflow-only',row,'\n'.join(maintained))
 case(name+'-record-only',row,record=maintained)
 case(name+'-matched',row,'\n'.join(maintained),maintained,selftest=True)
(out/'receipts/disk-results.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps(receipts,indent=2))
