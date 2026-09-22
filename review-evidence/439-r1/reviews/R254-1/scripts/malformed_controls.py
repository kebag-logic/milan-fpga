import json, pathlib, subprocess, sys, yaml
root=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);receipts=[]
# Public R220 optional generator-diagnostic finding, independently retained.
for name in ['blank-carrier','nameless-carrier']:
 d=out/'disposable'/name;d.mkdir(exist_ok=True)
 for rel in ['docs/testing/CI_WORKFLOWS.md',*[str(p.relative_to(root)) for p in (root/'.github/workflows').iterdir() if p.is_file()]]:
  dest=d/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((root/rel).read_bytes())
 p=d/'.github/workflows/docs.yml';w=yaml.safe_load(p.read_text());step=next(s for s in w['jobs']['docs-check']['steps'] if 'check_py_idiom.py' in s.get('run',''))
 if name=='blank-carrier': step['run']=' \t\n'
 else: del step['name']
 p.write_text(yaml.safe_dump(w,sort_keys=False))
 for mode in ['--check','--selftest']:
  argv=['rtk','proxy','python3','-B',str(root/'scripts/ci_events.py'),mode,'--root',str(d)]
  r=subprocess.run(argv,capture_output=True,timeout=120)
  label=name+mode
  (out/'receipts'/(label+'.stdout')).write_bytes(r.stdout);(out/'receipts'/(label+'.stderr')).write_bytes(r.stderr)
  assert r.returncode==1,(name,mode,r.returncode)
  if mode=='--selftest':assert ('IndexError' if name=='blank-carrier' else 'KeyError') in r.stderr.decode()
  receipts.append({'label':label,'argv':argv,'exit':r.returncode,'classification':'retained optional diagnostic limitation; fail closed, not passing source gate'})
(out/'receipts/malformed-results.json').write_text(json.dumps(receipts,indent=2)+'\n')
print('Retained optional R220 malformed-pristine diagnostic limitation: check 1; selftest 1 with traceback for both cases')
