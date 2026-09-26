import subprocess,os,json,time
from pathlib import Path
root=Path('$VALIDATION_STORAGE/565-a344')
env=os.environ.copy()
env['SUITE_TIMEOUT']='14400'
for shard in (1,3,4):
    name='sweep-'+str(shard)
    argv=['scripts/run_all_suites.sh',str(root/name),'--shard',str(shard)+'/5']
    start=time.monotonic()
    with (root/(name+'.log')).open('w') as log:
        r=subprocess.run(argv,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=43200)
    result=dict(argv=argv,rc=r.returncode,seconds=time.monotonic()-start)
    (root/(name+'-result.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(result,flush=True)
    print((root/(name+'.log')).read_text()[-4000:],flush=True)
    if r.returncode:
        raise SystemExit(r.returncode)
