#!/usr/bin/env python3
"""Foreground scoped review checks; all disposable files stay below scratch."""
import concurrent.futures, json, os, pathlib, subprocess, sys, tarfile
root=pathlib.Path(sys.argv[1]).resolve()
p=pathlib.Path(__file__).resolve().parent
scratch=p/'scratch'; scratch.mkdir(exist_ok=True)
env=os.environ.copy(); env['TMPDIR']=str(scratch); env['PYTHONDONTWRITEBYTECODE']='1'; env['MAKEFLAGS']='-j16'
frontend=str(p/'bounded_frontend.py')
def run(name,cmd,cwd):
    with (p/(name+'.log')).open('w') as f:
        f.write('COMMAND '+json.dumps(cmd)+'\n'); f.flush()
        rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
    (p/(name+'.rc')).write_text(str(rc)+'\n')
    return {'name':name,'rc':rc}
tree=scratch/'focused-source'; tree.mkdir(exist_ok=True)
archive=scratch/'head.tar'
with archive.open('wb') as f: subprocess.run(['git','archive','HEAD'],cwd=root,stdout=f,check=True)
with tarfile.open(archive) as f: f.extractall(tree,filter='data')
def main_suite():
    results=[run('focused-build',['make','-j16','gsi-build','VERILATOR='+frontend],tree/'tb/pp_top')]
    if results[-1]['rc']==0:
        for name,arg in [('focused-gi','--gsi-internal-only'),('focused-acmp','--acmp-only')]:
            results.append(run(name,['./obj_dir/Vpp_top_sim',arg],tree/'tb/pp_top'))
    return results
def mutants():
    return run('focused-mutants',['python3','-B','tb/pp_top/gsi_mutants.py','--jobs','2','--verilator',frontend,'--output',str(p/'mutants'),'--only','command-started-change-dropped','started-trigger-removed','coincidence-hold-removed'],root)
def srp():
    return run('focused-srp',['make','-j16','VERILATOR='+frontend],tree/'tb/srp_stream_fsms')
def docs():
    return run('focused-docs',['make','-j16','aecpcmd','modmatrix','params','matrix','links','ids','reqtags'],root)
with concurrent.futures.ThreadPoolExecutor(4) as pool:
    fs=[pool.submit(f) for f in (main_suite,mutants,srp,docs)]
    results=[f.result() for f in fs]
(p/'focused-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
