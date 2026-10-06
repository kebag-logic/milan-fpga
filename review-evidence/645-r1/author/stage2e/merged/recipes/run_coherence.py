import json, os, subprocess
from pathlib import Path
m=Path(__file__).parent
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0',MAKEFLAGS='-j16',VERILATOR_JOBS='2',TMPDIR=str(m/'tmp'))
argv=['taskset','-c','32,33','make','-j16','VERILATOR_JOBS=2']
cwd=m/'broad/tb/verilator/capture_coherence'
(m/'capture-coherence-command.json').write_text(json.dumps({'argv':argv,'cwd':str(cwd)},indent=2)+'\n')
with (m/'capture-coherence.log').open('w') as log: rc=subprocess.run(argv,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
(m/'capture-coherence.rc').write_text(str(rc)+'\n')
raise SystemExit(rc)
