#!/usr/bin/env python3
"""Repeat this review's focused runs; no full source or consumer bank is invoked.
Usage: python3 reproduce.py SOURCE PACKET SIMULATOR
The simulator must identify as 5.050. Documentation prerequisites must be on PATH.
All subprocesses run in the foreground; independent commands are joined here.
"""
import concurrent.futures,os,shutil,subprocess,sys
from pathlib import Path
src,packet,sim=map(lambda x:Path(x).resolve(),sys.argv[1:4])
assert subprocess.check_output([str(sim),'--version'],text=True).startswith('Verilator 5.050 ')
assert subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD'],text=True).strip()=='96d3b78384f34a630d6056ebd8fa5e30f6836650'
work=packet/'scratch/reproduction';work.mkdir(parents=True,exist_ok=False)
tree=work/'golden';subprocess.run(['git','clone','--quiet','--shared',str(src),str(tree)],check=True)
logs=packet/'receipts/reproduction';logs.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env.update(REVIEW_VERILATOR=str(sim),REVIEW_BUILD_JOBS='2',TMPDIR=str(work),MAKEFLAGS='-j16')
env['PATH']=str(sim.parent)+os.pathsep+env['PATH']
wrapper=str(packet/'scripts/simulator.py')
fields='unbind_talker_echo retry_status_cleared retry_probe_status_cleared lock_status_13 lock_gate_bypassed disconnect_invalid_success disconnect_changes_gate disconnect_not_accepted settled_vlan_truncated settlement_vlan_truncated stored_vlan_truncated gsi_vlan_external parent_vlan_shifted probe_guard_current_controller probe_retry_current_controller field_reset_blocked'.split()
tasks=[('fields',tree,['python3','tb/pp_top/acmp_mutants.py','--output',str(logs/'fields'),'--verilator',wrapper,'--jobs','4','--only',*fields]),
       ('notification',tree/'tb/aecp_notify',['make','-j16','VERILATOR='+wrapper]),
       ('lint',tree,['bash','scripts/lint_hdl.sh']),
       ('docs',tree,['make','-j16','check'])]
def run(task):
 name,cwd,argv=task
 return subprocess.run(['python3',str(packet/'scripts/run_logged.py'),str(logs/(name+'.log')),str(cwd),*argv],env=env).returncode
with concurrent.futures.ThreadPoolExecutor(4) as pool:rcs=list(pool.map(run,tasks))
probe=work/'probe'
for d in ['hdl','tb/common','tb/acmp_listener']:
 shutil.copytree(src/d,probe/d,ignore=shutil.ignore_patterns('obj*','*.hex','__pycache__'))
subprocess.run(['git','apply',str(packet/'scripts/reviewer-lifetimes.patch')],cwd=probe,check=True)
rcs.append(run(('reviewer-lifetimes',probe/'tb/acmp_listener',['make','-j16','VERILATOR='+wrapper])))
rcs.append(run(('matrix',tree,['python3','scripts/gen_matrix.py','--check'])))
subprocess.run(['python3',str(packet/'scripts/verify_tree.py'),str(src),str(logs/'exact-tree.json')],check=True)
raise SystemExit(1 if any(rcs) else 0)
