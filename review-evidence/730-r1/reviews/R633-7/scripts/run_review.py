#!/usr/bin/env python3
"""Foreground review driver; at most 15 simultaneous candidate processes, all namespaced."""
import concurrent.futures,json,pathlib,subprocess,time
P=pathlib.Path(__file__).resolve().parent.parent
S=P/'scripts'; T=P/'scratch/pristine'; R=P/'receipts'
def run(name,args,limit=580):
 start=time.monotonic()
 with (R/(name+'.log')).open('wb') as log:
  try: rc=subprocess.run([str(x) for x in args],stdout=log,stderr=subprocess.STDOUT,timeout=limit).returncode
  except subprocess.TimeoutExpired: rc=124
 (R/(name+'.rc')).write_text(str(rc)+'\n')
 result={'name':name,'rc':rc,'elapsed_s':round(time.monotonic()-start,3),'command':[str(x) for x in args]}
 print(json.dumps(result),flush=True)
 return result
def focused():
 results=[]
 for name in ['probe_cpu_ranges_r1','probe_cpu_ranges_compat','probe_lifecycle','probe_monitor','probe_shutdown','probe_r3','probe_cleanup_entry','probe_boundary_precedence','probe_r6_interrupt_diag','offline_dryrun']:
  results.append(run(name,[S/'sandbox.sh',T,'python3','-I',S/(name+'.py'),T]))
 for name,args in [('ci-events-check',['python3','scripts/ci_events.py','--check']),('ci-events-selftest',['python3','scripts/ci_events.py','--selftest']),('slot-proof',['bash','scripts/act_slot_proof.sh','--selftest'])]:
  results.append(run(name,[S/'sandbox.sh',T,*args]))
 return results
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 futures=[pool.submit(run,'runner-selftest',[S/'sandbox.sh',T,'python3','-I','scripts/act_ci.py','--selftest'])]
 for driver,jobs in [('mutants_r2',5),('mutants_r3',5),('mutants_r632_6',3)]:
  futures.append(pool.submit(run,driver,['python3','-I',S/(driver+'.py'),P,T,'--jobs',str(jobs)]))
 futures.append(pool.submit(focused))
 results=[f.result() for f in futures]
(R/'execution.json').write_text(json.dumps(results,indent=2)+'\n')
