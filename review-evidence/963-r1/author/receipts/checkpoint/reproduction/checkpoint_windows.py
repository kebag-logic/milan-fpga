#!/usr/bin/env python3
"""Complete all save windows by process snapshots, retaining the original model and graders.
Each arm calibrates every previously completed window against its complete ordinary-run log.
Any mismatch aborts before accepting newly checkpointed measurements.
"""
import hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
T=Path('<scratch>'); part=int(sys.argv[1]); n_parts=int(sys.argv[2])
J=[(t,p,a) for t in ('base','h4') for p in ('1x1','8x8-1if') for a in ('none','answering-ports')]
for idx,(tree,point,arm) in enumerate(J):
 if idx%n_parts!=part: continue
 build=T/'meas/full'/tree/point/arm; out=T/'checkpoint'/tree/point/arm; out.mkdir(parents=True,exist_ok=True)
 helper=T/'bin/checkpoint_prepare.py'
 subprocess.run([sys.executable,str(helper),tree,point,arm],check=True)
 env=dict(os.environ,CHECKPOINT_MANIFEST=str(out/'manifest'),CHECKPOINT_LOG=str(out/'root.log'))
 scripts=sorted(out.glob('*.txt')); assert len(scripts)==72
 argv=[str(build/'native/Vsim_checkpoint'),str(scripts[0]),'-']
 print('START',tree,point,arm,time.strftime('%H:%M:%S'),flush=True)
 with (out/'root.log').open('w') as f:
  rc=subprocess.run(argv,cwd=build/'gateware',env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (out/'native.rc').write_text(str(rc)+'\n'); assert rc==0,(tree,point,arm,rc)
 calibration=[]
 for script in scripts:
  g=script.stem; old=build/'g'/g; raw=(out/(g+'.log')).read_bytes()
  assert b'RESULT: PASS' in raw[-1000:],g
  if (old/'results.json').is_file():
   reference=(old/(g+'.log')).read_bytes(); same=raw==reference
   calibration.append(dict(group=g,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),reference_sha256=hashlib.sha256(reference).hexdigest(),same=same))
 (out/'calibration.json').write_text(json.dumps(calibration,indent=1)+'\n')
 assert len(calibration)==9 and all(r['same'] for r in calibration),calibration
 print('CALIBRATION',tree,point,arm,'9/9 entire logs identical',flush=True)
 for script in scripts:
  g=script.stem; dest=build/'g'/g; dest.mkdir(exist_ok=True)
  if (dest/'results.json').is_file(): continue
  shutil.copy2(script,dest/script.name); shutil.move(str(out/(g+'.log')),str(dest/(g+'.log')))
  argv=[sys.executable,'-B',str(T/'clones'/tree/'tb/verilator/ctrl_service_budget/run.py'),'--point',point,'--build-dir',str(build),'--reuse-build','--regrade','--out',str(dest),'--groups',g,'--record-budget-findings','--record-share-findings','--fetch-l1','split']
  if arm!='none': argv+=['--variant',arm]
  with (dest/'regrade.log').open('w') as f: rc=subprocess.run(argv,stdout=f,stderr=subprocess.STDOUT).returncode
  (dest/'rc').write_text(str(rc)+'\n'); (dest/'rc.from').write_text('checkpoint calibrated on 9 ordinary full logs, original grader\n')
  assert rc==0,(tree,point,arm,g,rc)
 print('DONE',tree,point,arm,'72 windows graded',time.strftime('%H:%M:%S'),flush=True)
 for p in out.iterdir():
  if p.name=='root.log' or '.prefix-' in p.name or (p.suffix=='.log' and p.name.startswith('backlog-')): p.unlink()
