import hashlib,json,shutil,subprocess,time
from pathlib import Path
w=Path(__file__).resolve().parent;repo=w/'candidate';out=w/'recorded';out.mkdir(exist_ok=True)
while not (w/'resource-bank.rc').exists(): time.sleep(10)
assert (w/'resource-bank.rc').read_text().strip()=='0'
policy=w/'measurement-policy.json';shutil.copy2(repo/'syn/ooc/pp_resource_baseline.json',policy)
records={}
for name,folder,endpoint in [('candidate-route',w/'shipping-candidate/ax7101/gateware','route-1x1'),('candidate-ooc-1x1',w/'shipping-candidate/ax7101-ooc','ooc-1x1'),('candidate-ooc-8x8',w/'shipping-candidate/ax8x8-ooc','ooc-8x8')]:
 args=['python3','syn/ooc/pp_resource_gate.py','record',str(folder),'--endpoint',endpoint,'--write','--baseline',str(policy)]
 with (out/(name+'.log')).open('w') as f:r=subprocess.run(args,cwd=repo,stdout=f,stderr=subprocess.STDOUT)
 (out/(name+'.rc')).write_text(str(r.returncode)+'\n')
 if r.returncode:raise SystemExit(r.returncode)
 records[name]=json.loads((out/(name+'.log')).read_text())
 (out/(name+'.command.json')).write_text(json.dumps({'argv':args,'rc':r.returncode},indent=2)+'\n')
(w/'measurement-records.json').write_text(json.dumps(records,indent=2)+'\n')
changes=[];checked=0
for shape in json.loads((w/'source-inputs.json').read_text()):
 for entry in shape['files']:
  checked+=1;p=Path(entry['path']);actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
  if actual!=entry['sha256']:changes.append(str(p))
(out/'input-recheck.json').write_text(json.dumps(dict(checked=checked,changes=changes),indent=2)+'\n')
assert not changes,changes
print('Three records written; input identities preserved',checked)
