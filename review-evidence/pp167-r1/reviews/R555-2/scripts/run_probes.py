#!/usr/bin/env python3
import concurrent.futures,json,os,pathlib,subprocess,sys,time
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve(); scratch=packet/'scratch'; receipts=packet/'receipts'; pub=packet/'scripts/public-probes'
old=scratch/'reviewed'
if not old.exists():
    subprocess.run(['git','clone','--shared','--quiet','--no-checkout',str(root),str(old)],check=True)
    subprocess.run(['git','-C',str(old),'checkout','--quiet','--detach','f3fef22448ce4f9bed8fd249a21a5d472148bd3d'],check=True)
env=os.environ.copy(); env['VERILATOR']=str(packet/'scripts/limited_verilator.py'); env['TMPDIR']=str(scratch)
def run(item):
    name,script,src=item; work=scratch/name; argv=['bash',str(pub/script),str(src),str(work)]; start=time.time()
    with (receipts/(name+'.log')).open('w') as log: rc=subprocess.run(argv,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    (receipts/(name+'.rc')).write_text(str(rc)+'\n')
    builds=list(work.rglob('build.log'))
    for i,b in enumerate(builds): (receipts/(name+f'-build-{i}.log')).write_bytes(b.read_bytes())
    rec={'name':name,'rc':rc,'argv':argv,'seconds':round(time.time()-start,3)}
    (receipts/(name+'.json')).write_text(json.dumps(rec,indent=2)+'\n'); print(name,rc,flush=True); return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(run,[('p1-head','p1_build.sh',root),('p1-reviewed','p1_build.sh',old),('p2-head','p2_build.sh',root)]))
assert all(r['rc']==0 for r in results)
p1h=(receipts/'p1-head.log').read_text(); p1b=(receipts/'p1-reviewed.log').read_text(); p2=(receipts/'p2-head.log').read_text()
assert 'fail_at=1 setup=1 met=1 cancels={1,1} owner1_cancel_offset=1 registry_count=1 dereg_cycles_to_commanding_controller=0' in p1h
assert 'fail_at=1 setup=1 met=1 cancels={1,1} owner1_cancel_offset=1 registry_count=0 dereg_cycles_to_commanding_controller=1' in p1b
assert 'cancel_at_E=0 fail_for_owner1=1 fail_offset_from_E=1' in p2
assert 'cancel_at_E=1 fail_for_owner1=0 fail_offset_from_E=-1' in p2
print('P1 offset-1 closure and P2 base timing assertions PASS')
(receipts/'probe-assertions.json').write_text(json.dumps({'results':results,'assertions':'PASS'},indent=2)+'\n')
