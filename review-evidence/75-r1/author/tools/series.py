"""Run a bounded series, releasing the bench lock between cycles."""
import json,subprocess,sys
from pathlib import Path
p=Path(__file__).resolve().parent.parent
direction,*endpoints=sys.argv[1:]
streak=0
for i in range(1,101):
 name=f'{direction}-{i:03d}'
 if (p/name/'result.json').exists():
  result=json.loads((p/name/'result.json').read_text())
  assert (p/name/'analysis.json').exists(),'unfinished prior cycle'
 else:
  args=['rtk','proxy','timeout','60s','flock','-w','5','/tmp/milan-bench.lock','timeout','52s','python3',str(p/'tools/action.py'),name,'cycle',direction,*endpoints]
  r=subprocess.run(args,timeout=63,capture_output=True,text=True)
  (p/name/'action.log').write_text(r.stdout+r.stderr)
  subprocess.run(['rtk','proxy','timeout','8s','python3',str(p/'tools/ledger.py')],timeout=10,check=True,capture_output=True)
  if r.returncode:raise SystemExit(r.returncode)
  subprocess.run(['rtk','proxy','timeout','12s','python3',str(p/'tools/analyze.py'),name],timeout=14,check=True,capture_output=True)
  result=json.loads((p/name/'result.json').read_text())
 streak=streak+1 if result['status']=='FAIL' else 0
 print('CYCLE',name,'latency',result.get('latency_s'),'consecutive overruns',streak,flush=True)
 if streak>=10:
  print('EARLY STOP',direction,'ten consecutive overruns',flush=True);break
