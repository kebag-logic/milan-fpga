import os,subprocess,time,json
from pathlib import Path
s=Path('$SCRATCH');d=s/'yosys';d.mkdir(exist_ok=True);(d/'tmp').mkdir(exist_ok=True)
cmd=['syn/yosys/run.sh','--results',str(d/'results')]
t=time.time()
with (d/'run.log').open('w') as log:
 r=subprocess.run(cmd,cwd='$CHECKOUT',env=dict(os.environ,TMPDIR=str(d/'tmp')),stdout=log,stderr=subprocess.STDOUT,timeout=14400)
(d/'run.json').write_text(json.dumps({'command':cmd,'exit':r.returncode,'seconds':time.time()-t},indent=2))
print('YOSYS',r.returncode,flush=True);raise SystemExit(r.returncode)
