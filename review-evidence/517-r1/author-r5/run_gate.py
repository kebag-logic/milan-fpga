import json
import os
from pathlib import Path
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
ROOT = Path('$LANES/517-bounded-simulation-pool')
ENV = {key: os.environ[key] for key in ('HOME', 'USER', 'LOGNAME', 'LANG', 'SHELL', 'TERM') if key in os.environ}
ENV['PATH'] = '$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin'
ENV['PATH'] = '$VALIDATION_STORAGE/517-manager-r4/pinned-tool-bin:' + ENV['PATH']
ENV['PYTHONDONTWRITEBYTECODE'] = '1'
ENV['VERILATOR_JOBS'] = '8'
ENV['TMPDIR'] = '/tmp/517-a324-runtime'
for key in ('MILAN_COUNTER_FRAME_OUT', 'MAKEFLAGS', 'OBJCACHE'):
    ENV.pop(key, None)
Path(ENV['TMPDIR']).mkdir(exist_ok=True)

def run(name, argv, cwd=ROOT, env=None):
    start = time.time()
    with (OUT / (name + '.log')).open('wb') as log:
        proc = subprocess.run(argv, cwd=cwd, env=env or ENV, stdout=log,
                              stderr=subprocess.STDOUT, timeout=14400)
    row = dict(name=name, argv=argv, cwd=str(cwd), start=start,
               seconds=round(time.time()-start, 3), exit=proc.returncode)
    (OUT / (name + '.json')).write_text(json.dumps(row, indent=2)+'\n')
    with (OUT / 'gates.jsonl').open('a') as log:
        log.write(json.dumps(row)+'\n')
    print(json.dumps(row), flush=True)
    return proc.returncode

if __name__ == '__main__':
    sys.exit(run(sys.argv[1], sys.argv[2:]))
