"""Re-record the three resource endpoints from the finished shipping measurement.

Every figure comes from `pp_resource_gate.py record --write`; only the human
`measured` notes are set afterwards, serialized exactly as record --write does.
"""
import json,os,subprocess,sys,time
from pathlib import Path
w=Path(__file__).resolve().parent
main=Path('$LANES/696-maap-annexb')
shipping=Path('$VALIDATION_STORAGE/696-a570/resume-differential/shipping')
assert (w/'shipping-bank.rc').read_text().strip()=='0'
measurement=json.loads((w/'shipping-results.json').read_text())
head=subprocess.check_output(['git','-C',str(main),'rev-parse','HEAD'],text=True).strip()
assert measurement['head']==head and measurement['before']==measurement['after']
for args in [['diff','--quiet'],['diff','--cached','--quiet']]:subprocess.run(['git','-C',str(main),*args],check=True)
baseline=main/'syn/ooc/pp_resource_baseline.json'
original=baseline.read_text();before=json.loads(original)
(w/'resource-baseline-before.json').write_text(original)
rows=[]
env=dict(os.environ,TMPDIR=str(w),PYTHONDONTWRITEBYTECODE='1')
def run(name,args):
 start=time.time()
 with (w/(name+'.log')).open('w') as f:rc=subprocess.run(args,cwd=main,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (w/(name+'.rc')).write_text(str(rc)+'\n')
 rows.append(dict(name=name,argv=list(map(str,args)),rc=rc,seconds=round(time.time()-start,1),head=head))
 (w/'resource-record-results.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(name,rc,flush=True)
 if rc:raise SystemExit(rc)
endpoints=[('route-1x1',shipping/'ax7101/gateware'),('ooc-1x1',shipping/'ax7101-ooc'),('ooc-8x8',shipping/'ax8x8-ooc')]
for endpoint,directory in endpoints:run('resource-record-'+endpoint,['python3','syn/ooc/pp_resource_gate.py','record',str(directory),'--endpoint',endpoint,'--write'])
after=json.loads(baseline.read_text())
note=sys.argv[1]
for name in before['endpoints']:
 keep=lambda entry:{k:v for k,v in entry.items() if k not in ('record','measured')}
 assert keep(before['endpoints'][name])==keep(after['endpoints'][name]),name
 after['endpoints'][name]['measured']=note
assert {k:v for k,v in before.items() if k!='endpoints'}=={k:v for k,v in after.items() if k!='endpoints'}
baseline.write_text(json.dumps(after,indent=1)+'\n')
for endpoint,directory in endpoints:run('resource-after-'+endpoint,['python3','syn/ooc/pp_resource_gate.py','check',str(directory),'--endpoint',endpoint])
run('resource-check-baseline',['python3','syn/ooc/pp_resource_gate.py','check-baseline'])
(w/'resource-baseline-after.json').write_text(baseline.read_text())
print('All three records written by record --write; policies unchanged.',flush=True)
