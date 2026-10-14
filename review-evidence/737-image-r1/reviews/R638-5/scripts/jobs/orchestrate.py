import subprocess, sys, time, os, shutil, json
S='$REVIEWS/737-image-r638-5-packet/scratch'
IMG='fpga-validation@sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c'
jobs=[('lint',5),('docs-check',4),('changes',1),('bdd',1),('wire',1),('nogit',1),('yosys',5),
      ('pubcensus',6),('fwunit',4),('mut1',3),('mut2',3),('mut3',3),('boundary',3),('fwver',4)]
BUDGET=12
CPUS={n:f'{4*(i%4)}-{4*(i%4)+3}' for i,(n,_) in enumerate(jobs)}
os.makedirs(f'{S}/runs/out',exist_ok=True)
running={}; queue=list(jobs); used=0; t0=time.time(); log=open(f'{S}/runs/orchestrate.log','a')
def start(name,mem):
    tree=f'{S}/runs/{name}/tree'
    if os.path.exists(f'{S}/runs/{name}'): shutil.rmtree(f'{S}/runs/{name}')
    subprocess.run(['cp','-a',f'{S}/base',tree.rsplit('/',1)[0]+'/tree'],check=True) if False else None
    os.makedirs(f'{S}/runs/{name}'); subprocess.run(['cp','-a',f'{S}/base',tree],check=True)
    if name=='nogit': shutil.rmtree(f'{tree}/.git')
    cmd=['sudo','-n','-u','alex','-g','docker','docker','run','--rm','--name',f'r638-5-{name}','--network','none','--cpuset-cpus',CPUS[name],
         '--user','1000:1000','--memory',f'{mem}g','--memory-swap',f'{mem}g',
         '-e','HOME=/tmp/home','-e','RUNNER_TEMP=/tmp/rt','-e','GITHUB_WORKSPACE=/work','-e',f'JOB={name}',
         '-e','CI=true','-e','GITHUB_ACTIONS=true','-e','GITHUB_SHA=4391f353690972f4844cb641b1e77fa94f38cdf4',
         '-e','GITHUB_EVENT_NAME=pull_request','-e','GITHUB_REPOSITORY=kebag-logic/milan-fpga',
         '-e','GITHUB_OUTPUT=/tmp/rt/github_output','-e','GITHUB_ENV=/tmp/rt/github_env','-e','GITHUB_PATH=/tmp/rt/github_path',
         '--mount',f'type=bind,src={tree},dst=/work','--mount',f'type=bind,src={S}/jobs,dst=/jobs,readonly',
         '--mount',f'type=bind,src={S}/runs/out,dst=/out','-w','/work',IMG,'bash',f'/jobs/{name}.sh']
    f=open(f'{S}/runs/{name}/container.log','w')
    p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT)
    print(f'{time.time()-t0:7.0f}s START {name} mem={mem}g',file=log,flush=True)
    return p
while queue or running:
    for name,mem in list(queue):
        if used+mem<=BUDGET:
            running[name]=(start(name,mem),mem,time.time()); used+=mem; queue.remove((name,mem))
    for name,(p,mem,ts) in list(running.items()):
        if p.poll() is not None:
            print(f'{time.time()-t0:7.0f}s END {name} rc={p.returncode} dur={time.time()-ts:.0f}s',file=log,flush=True)
            used-=mem; del running[name]
    time.sleep(5)
print(f'{time.time()-t0:7.0f}s ALL DONE',file=log,flush=True)
