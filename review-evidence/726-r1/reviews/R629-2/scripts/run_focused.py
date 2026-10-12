#!/usr/bin/env python3
"""Run independent review checks concurrently; retain logs and return codes."""
import argparse, concurrent.futures, json, os, pathlib, shutil, subprocess, time
p=argparse.ArgumentParser()
p.add_argument('repo',type=pathlib.Path)
p.add_argument('packet',type=pathlib.Path)
p.add_argument('--phase',choices=['counter','light'],required=True)
a=p.parse_args(); repo=a.repo.resolve(); packet=a.packet.resolve()
scratch=packet/'scratch'; receipts=packet/'receipts'; scratch.mkdir(exist_ok=True); receipts.mkdir(exist_ok=True)
env=dict(os.environ); env['TMPDIR']=str(scratch); env['PYTHONDONTWRITEBYTECODE']='1'
env['VERILATOR']=os.environ.get('VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
jobs=[]
if a.phase=='counter':
    for shape in (1,8):
        jobs.append((f'frames-only-{shape}', ['python3','tb/verilator/milan_dp/stream_counters.py','--shape',str(shape),'--output-condition','frames-only'],repo))
    for variant in ('tx-nodirty','tx-interval','rx-interval','tx-reset','aaf-reset','crf-reset','rx-saturation','late','rate'):
        jobs.append((variant,['python3','tb/verilator/milan_dp/stream_counters.py','--variant',variant],repo))
    for shape in (1,8):
        jobs.append((f'before-{shape}',['python3','tb/verilator/milan_dp/stream_counters.py','--shape',str(shape),'--variant','before'],repo))
else:
    jobs=[('bdd',['python3','-m','behave','--no-capture','-f','plain'],repo/'tests'),('grader',['python3','tb/tools/torture_campaign.py','--self-test'],repo)]
def run(job):
    name,cmd,cwd=job; work=scratch/name
    if a.phase=='counter': cmd=cmd+['--work',str(work)]
    start=time.time()
    with (receipts/(name+'.driver.log')).open('w') as out:
        r=subprocess.run(cmd,cwd=cwd,env=env,stdout=out,stderr=subprocess.STDOUT)
    (receipts/(name+'.rc')).write_text(str(r.returncode)+'\n')
    (receipts/(name+'.command.json')).write_text(json.dumps({'command':cmd,'cwd':str(cwd),'elapsed_s':round(time.time()-start,3)},indent=2)+'\n')
    for f in ('run.log','escape.log','build.log'):
        if (work/f).exists(): shutil.copyfile(work/f,receipts/(name+'.'+f))
    print(name, 'rc='+str(r.returncode), 'seconds='+str(round(time.time()-start)),flush=True)
    return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(run,jobs))
raise SystemExit(int(any(results)))
