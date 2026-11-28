"""Run the unchanged injected replay once per completed, hash-bound trace."""
import dataclasses,hashlib,json,sys,time
from pathlib import Path
root=Path.cwd();scratch=Path('$VALIDATION_STORAGE/usbnet-a855/round7')
packet=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
sys.path.insert(0,str(root/'tb/verilator/usbnet'))
import egress_grade as g
params=g.usb.base.params(g.usb.base.arty_spec())
def sha(data):return hashlib.sha256(data).hexdigest()
def inputs():
 files=[root/'tb/verilator/usbnet'/x for x in ('egress_usb.py','egress_grade.py')]
 files += [root/'tb/verilator/ctrl_service_budget'/x for x in ('egress_mii.py','grade.py')]
 return dict(sources={str(f.relative_to(root)):sha(f.read_bytes()) for f in files},params=dataclasses.asdict(params))
frozen=inputs()
manifest=json.loads((scratch/'census/manifest.json').read_text())
expected=sorted((v,n) for v,ns in manifest['groups'].items() for n in ns)
output=packet/'egress-cases';output.mkdir(exist_ok=True)
mode=sys.argv[1]
if mode!='verify':
 worker=int(mode);wanted=set(expected[worker::2]);done=set()
 while done!=wanted:
  for name in ('census','census-supplemental'):
   directory=scratch/name;f=directory/'completed.json'
   try:rows=json.loads(f.read_text())
   except (OSError,json.JSONDecodeError):continue
   for row in rows:
    key=(row['variant'],row['group'])
    if key not in wanted or key in done:continue
    assert inputs()==frozen,'grader inputs changed'
    trace=directory/key[0]/'results'/(key[1]+'.log')
    raw=trace.read_bytes();assert sha(raw)==row['trace_sha256']
    result=g.grade(raw.decode(),params)
    record=dict(case=list(key),trace_sha256=sha(raw),inputs=frozen,result=result)
    dest=output/key[0]/(key[1]+'.json');dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(record,indent=2)+'\n')
    print('/'.join(key),json.dumps(result),flush=True);done.add(key)
  if done!=wanted:time.sleep(1)
 print('COMPLETE',worker,len(done),flush=True)
else:
 completed=json.loads((scratch/'census/completed.json').read_text())
 records={(r['variant'],r['group']):r for r in completed}
 assert sorted(records)==expected
 present=sorted((p.parent.name,p.stem) for p in output.glob('*/*.json'))
 assert present==expected,(len(present),len(expected))
 results={}
 for key in expected:
  cached=json.loads((output/key[0]/(key[1]+'.json')).read_text())
  assert json.dumps(cached['inputs'],sort_keys=True)==json.dumps(frozen,sort_keys=True)
  assert cached['case']==list(key)
  trace=scratch/'census'/key[0]/'results'/(key[1]+'.log')
  assert cached['trace_sha256']==records[key]['trace_sha256']==sha(trace.read_bytes())
  name='/'.join(key);results[name]=cached['result'];print(name,json.dumps(cached['result']),flush=True)
 ok,lines=g.verdict(results,params)
 print('\n'.join(lines),flush=True)
 print(f"RESULT: {'PASS' if ok else 'FAIL'} cases={len(results)}",flush=True)
 raise SystemExit(not ok)
