import subprocess,sys,os,json,time
from pathlib import Path
root=Path('$VALIDATION_STORAGE/565-a344')
shape,clock,traffic=sys.argv[1:]
name='capture-'+shape+'-'+clock+'-'+traffic
build=root/name
env=os.environ.copy();env.update(json.loads((root/'environment.json').read_text()))
argv=['unshare','-Urn','$WORKSPACE_HOME/litex-milan/venv/bin/python3','-B','tb/verilator/nvm_capture_cpu/run.py','--shape','endstation_ax7101_'+shape,'--cpu-hz',str(int(clock)*1000000),'--captures','16','--traffic',traffic,'--build-dir',str(build)]
start=time.monotonic()
with (root/(name+'.log')).open('w') as log:
    r=subprocess.run(argv,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=14400)
result=dict(argv=argv,rc=r.returncode,seconds=time.monotonic()-start)
(root/(name+'-result.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
if r.returncode:
    print((root/(name+'.log')).read_text()[-5000:])
else:
    m=json.loads((build/'measurement.json').read_text());m.pop('rows');print(json.dumps(m))
raise SystemExit(r.returncode)
