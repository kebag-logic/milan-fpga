#!/usr/bin/env python3
"""Run the exact-head ACMP walk and isolated old-answer controls.
Usage: python3 probe_acmp.py CHECKOUT PACKET
Builds stay in PACKET/scratch. No tracked source is edited.
"""
import concurrent.futures, pathlib, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import ctrl_build as b, ctrl_reuse as reuse, ctrl_arms as arms, fw_gtest
work=packet/'scratch/acmp'; work.mkdir(parents=True,exist_ok=True)
reuse.cut_reuse(work/'reference')
# Extract only the published test model from the old accepted processor object.
old=subprocess.check_output(['git','-C',str(root/'protocol-processor'),'show','2ad2f845:tb/acmp_listener/sim_main.cpp'],text=True).splitlines()
new=(work/'reference/pp_acmp_reuse.inc').read_text()
oldtext='\n'.join(reuse.cut(old,*reuse.REUSE[1][2][0]))+'\n'
variants={'current':new,'old_all':oldtext}
# Record the exact old-model substitution used by the negative control.
import difflib
hunks=list(difflib.unified_diff(new.splitlines(),oldtext.splitlines()))
(packet/'acmp-model-control.diff').write_text('\n'.join(hunks)+'\n')

def run(item):
 name,model=item; out=work/name; (out/'reuse').mkdir(parents=True,exist_ok=True)
 for f in (work/'reference').iterdir(): (out/'reuse'/f.name).write_bytes(f.read_bytes())
 (out/'reuse/pp_acmp_reuse.inc').write_text(model)
 tree=b.Tree(b.CTRL,out/'build',out/'reuse',fw_gtest.Build(jobs=4))
 result=arms.arm_acmpwalk(tree)
 (packet/(name+'.log')).write_text(result.log)
 (packet/(name+'.rc')).write_text(str(result.rc)+'\n')
 print(name,'rc',result.rc,flush=True)
 if name=='current': assert result.rc==0 and 'checks: 127   failures: 0' in result.log
 else:
  assert result.rc==1
  for label in ['LD1','LD2','LD3']: assert label in result.log
 return name,result.rc
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: list(pool.map(run,variants.items()))
print('PASS current accepted; old processor model rejected with LD1, LD2 and LD3 diagnostics')
