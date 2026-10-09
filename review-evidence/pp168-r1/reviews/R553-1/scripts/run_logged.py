#!/usr/bin/env python3
"""Foreground execution with a durable log, exit code and command receipt."""
import json,subprocess,sys,time
from pathlib import Path
log=Path(sys.argv[1]); cwd=sys.argv[2]; argv=sys.argv[3:]
start=time.time()
with log.open('w') as f:
    rc=subprocess.run(argv,cwd=cwd,stdout=f,stderr=subprocess.STDOUT).returncode
log.with_suffix('.rc').write_text(str(rc)+'\n')
log.with_suffix('.command.json').write_text(json.dumps(dict(cwd=cwd,argv=argv,rc=rc,elapsed_seconds=round(time.time()-start,3)),indent=2)+'\n')
print(log.name, 'rc',rc, 'seconds',round(time.time()-start,1),flush=True)
sys.exit(rc)
