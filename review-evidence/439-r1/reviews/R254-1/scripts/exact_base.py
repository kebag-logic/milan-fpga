import json, pathlib, subprocess, sys
root=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);base='483a133ed08867ea0d300d2b4a027b5b48a4282f';d=out/'disposable/exact-base';d.mkdir(exist_ok=True)
files=['scripts/ci_events.py','docs/testing/CI_WORKFLOWS.md',*[str(p.relative_to(root)) for p in (root/'.github/workflows').iterdir() if p.is_file()]]
for rel in files:
 p=d/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(subprocess.check_output(['rtk','proxy','git','-C',str(root),'show',base+':'+rel]))
results=[]
for mode in ['--check','--selftest']:
 argv=['rtk','proxy','python3','-B',str(d/'scripts/ci_events.py'),mode,'--root',str(d)]
 r=subprocess.run(argv,capture_output=True,timeout=120);label='exact-base'+mode
 (out/'receipts'/(label+'.stdout')).write_bytes(r.stdout);(out/'receipts'/(label+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0
 assert r.stdout==(out/'receipts/cli'/('base'+mode+'.stdout')).read_bytes()
 results.append({'argv':argv,'exit':r.returncode,'label':label,'identical_to_base_checker_receipt':True})
(out/'receipts/exact-base-results.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS: exact base files; check/selftest outputs equal original comparison receipts')
