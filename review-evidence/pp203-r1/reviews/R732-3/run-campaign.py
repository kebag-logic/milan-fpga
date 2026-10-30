from pathlib import Path
import subprocess,os,sys
p=Path(__file__).resolve().parent
s=Path(sys.argv[1]).resolve()
env=dict(os.environ,TMPDIR=str(p/'scratch'),MAKEFLAGS='-j16')
cmd=['python3','-B','tb/pp_top/aecp_dispatch_mutants.py','--only','rbt-request-at-acceptance,rbt-last-frame-unwatched,rbt-last-byte-offered','--jobs','2','--verilator',str(p/'scratch/simulator-j4.py'),'--output',str(p/'focused-mutants')]
with (p/'focused-mutants.log').open('w') as f: rc=subprocess.run(cmd,cwd=s,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
(p/'focused-mutants.rc').write_text(str(rc)+'\n')
sys.exit(rc)
