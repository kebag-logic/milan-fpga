"""Re-record the three resource endpoints from the finished merged-head measurement.

Runs only when the Vivado job ended rc 0 and all three gate checks exited 0.
Every figure comes from `pp_resource_gate.py record --write`; only the human `measured`
note is set afterwards, serialized exactly as record --write does.
"""
import json,os,subprocess,sys,time
from pathlib import Path
w=Path(__file__).resolve().parent
main=Path('<lane>')
shipping=w/'shipping'
out=w/'record';out.mkdir(exist_ok=True)
assert (w/'vivado-bank.rc').read_text().strip()=='0'
measurement=json.loads((w/'vivado-results.json').read_text())
head=subprocess.check_output(['git','-C',str(main),'rev-parse','HEAD'],text=True).strip()
assert measurement['head']==head
assert [r['inputs_sha256'] for r in measurement['before']]==[r['inputs_sha256'] for r in measurement['after']]
rcs={r['name']:r['rc'] for r in measurement['rows']}
for name in ['route','route-queries','rtl-8x8','ax7101-ooc','ax8x8-ooc','check-route-1x1','check-ooc-1x1','check-ooc-8x8']:
 assert rcs[name]==0,(name,rcs.get(name))
for args in [['diff','--quiet'],['diff','--cached','--quiet']]:subprocess.run(['git','-C',str(main),*args],check=True)
baseline=main/'syn/ooc/pp_resource_baseline.json'
original=baseline.read_text();before=json.loads(original)
(out/'resource-baseline-before.json').write_text(original)
rows=[]
env=dict(os.environ,TMPDIR=str(w/'tmp'),PYTHONDONTWRITEBYTECODE='1')
def run(name,args):
 start=time.time()
 with (out/(name+'.log')).open('w') as f:rc=subprocess.run(args,cwd=main,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (out/(name+'.rc')).write_text(str(rc)+'\n')
 rows.append(dict(name=name,argv=list(map(str,args)),rc=rc,seconds=round(time.time()-start,1),head=head))
 (out/'record-results.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(name,rc,flush=True)
 if rc:raise SystemExit(rc)
endpoints=[('route-1x1',shipping/'ax7101/gateware'),('ooc-1x1',shipping/'ax7101-ooc'),('ooc-8x8',shipping/'ax8x8-ooc')]
for endpoint,directory in endpoints:run('record-'+endpoint,['python3','syn/ooc/pp_resource_gate.py','record',str(directory),'--endpoint',endpoint,'--write'])
after=json.loads(baseline.read_text())
note=sys.argv[1]
keep=lambda entry:{k:v for k,v in entry.items() if k not in ('record','measured')}
for name in before['endpoints']:
 assert keep(before['endpoints'][name])==keep(after['endpoints'][name]),name
 after['endpoints'][name]['measured']=note
assert {k:v for k,v in before.items() if k!='endpoints'}=={k:v for k,v in after.items() if k!='endpoints'}
baseline.write_text(json.dumps(after,indent=1)+'\n')
for endpoint,directory in endpoints:run('after-'+endpoint,['python3','syn/ooc/pp_resource_gate.py','check',str(directory),'--endpoint',endpoint])
run('check-baseline',['python3','syn/ooc/pp_resource_gate.py','check-baseline'])
(out/'resource-baseline-after.json').write_text(baseline.read_text())
print('All three records written by record --write; policies unchanged.',flush=True)
