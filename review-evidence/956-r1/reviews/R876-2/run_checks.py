#!/usr/bin/env python3
"""Focused mutation and static checks; foreground supervisor, each child logged."""
import concurrent.futures, os, subprocess, sys
from pathlib import Path
P=Path(__file__).resolve().parent
R=Path(sys.argv[1]).resolve(); py=sys.executable
os.environ['PYTHONDONTWRITEBYTECODE']='1'
base=R/'tb/verilator/ctrl_service_budget'
tasks=[('plants-srp',[py,'-B',str(P/'plants.py'),str(R),'srp',str(P/'scratch/plants-srp'),'2','talker-unchanged-held,talker-resume-drops-what-came-due,talker-resume-drops-what-came-due-at-a-phase,talker-registration-kept-across-a-reset,build-resumed-drops-what-came-due,build-paused-keeps-its-due,build-paused-not-aged,build-paused-unreported,build-refused-second-slice-not-due,talker-hold-off-adds-its-terms']),
('plants-aecp',[py,'-B',str(P/'plants.py'),str(R),'aecp',str(P/'scratch/plants-aecp'),'registration-notice-kept-across-a-reset']),
('load',[py,'-B',str(base/'load_grade.py'),'--check']),
('flip-1x1',[py,'-B',str(base/'flip_grade.py'),'--check','--point','1x1/1if']),
('flip-8x8',[py,'-B',str(base/'flip_grade.py'),'--check','--point','8x8/1if']),
('shape',[py,'-B',str(base/'shape_costs.py'),'--check']),
('docs',[py,'-B',str(R/'scripts/docs_check.py')])]
def run(t):
    name,cmd=t
    with (P/(name+'.log')).open('w') as f:
        try: rc=subprocess.run(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT,timeout=540).returncode
        except subprocess.TimeoutExpired: rc=124
    (P/(name+'.rc')).write_text(str(rc)+'\n')
    print(name,rc,flush=True)
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    codes=list(pool.map(run,tasks))
sys.exit(any(codes))
