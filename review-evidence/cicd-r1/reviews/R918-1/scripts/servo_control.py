#!/usr/bin/env python3
"""Pair the existing policy-slew planted defect across base and head."""
import concurrent.futures,pathlib,subprocess,os,json,importlib.util
P=pathlib.Path(__file__).resolve().parents[1];S=P/'scratch';R=P/'receipts'
def one(label):
 T=S/label;d=T/'tb/verilator/mmcm_servo';W=S/('servo-control-'+label);W.mkdir(exist_ok=True)
 spec=importlib.util.spec_from_file_location('slew_'+label,d/'slew_mutants.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 name,anchor,replacement,failure=m.MUTANTS[0];src=m.RTL.read_text();assert src.count(anchor)==1
 rtl=W/'mutant.sv';rtl.write_text(src.replace(anchor,replacement))
 env=dict(os.environ,OBJCACHE='',MAKEFLAGS='--no-print-directory')
 def call(kind,args,rc):
  with (R/(label+'.servo-control.'+kind+'.log')).open('w') as out:
   result=subprocess.run(args,cwd=d,env=env,stdout=out,stderr=subprocess.STDOUT)
  assert result.returncode==rc,(label,kind,result.returncode)
 call('clean',[str(d/'obj_phc/Vphc_step'),'+slew_control'],0)
 call('build',['make','-j16','phc_step_build','SERVO_RTL='+str(rtl),'PHC_MDIR='+str(W/'obj'),'VERILATOR='+str(S/'simulator')],0)
 call('mutant',[str(W/'obj/Vphc_step'),'+slew_control'],1)
 output=(R/(label+'.servo-control.mutant.log')).read_text();assert '[FAIL] '+failure in output and 'RESULT: FAIL' in output
 return {'variant':label,'mutant':name,'rc':1,'named_check':failure,'caught':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(one,['base','head']))
for kind in ('clean','mutant'):assert (R/('base.servo-control.'+kind+'.log')).read_bytes()==(R/('head.servo-control.'+kind+'.log')).read_bytes()
(R/'servo-control.json').write_text(json.dumps({'results':results,'outputs_byte_identical':True},indent=2)+'\n')
print(json.dumps(results))
