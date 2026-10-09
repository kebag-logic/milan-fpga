#!/usr/bin/env python3
"""Run independent commands concurrently, retaining each log and exit status."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
spec=pathlib.Path(sys.argv[1]).resolve()
root=spec.parent.parent
env=os.environ.copy()
env['PACKET']=str(root)
def expand(value):
    if isinstance(value, str):
        import re
        return re.sub(r'\$([A-Z][A-Z0-9_]*)', lambda m: env[m[1]], value)
    if isinstance(value, list): return [expand(x) for x in value]
    if isinstance(value, dict): return {k:expand(v) for k,v in value.items()}
    return value
jobs=expand(json.loads(spec.read_text()))
env.update(TMPDIR=str(root/'scratch/tmp'), PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1')
(root/'scratch/tmp').mkdir(exist_ok=True,parents=True)
def run(j):
    started=time.time()
    log=root/'receipts'/(j['name']+'.log')
    with log.open('w') as f:
        f.write('COMMAND '+json.dumps(j['argv'])+'\n');f.flush()
        try:
            result=subprocess.run(j['argv'],cwd=j['cwd'],env={**env,**j.get('env',{})},stdout=f,stderr=subprocess.STDOUT,timeout=j.get('timeout',540))
            rc=result.returncode
        except subprocess.TimeoutExpired:
            rc=124;f.write('TIMEOUT\n')
    (root/'receipts'/(j['name']+'.rc')).write_text(str(rc)+'\n')
    (root/'receipts'/(j['name']+'.time')).write_text(f'{time.time()-started:.3f} seconds\n')
    print(j['name'], 'rc='+str(rc), flush=True)
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs)) as pool:
    r=list(pool.map(run,jobs))
sys.exit(int(any(r)))
