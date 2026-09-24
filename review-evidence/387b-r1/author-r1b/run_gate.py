from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

out = Path(__file__).parent
label, *command = sys.argv[1:]
assert command
log = out / (label + '.log')
receipt = out / (label + '.json')
assert not log.exists() and not receipt.exists()
env = os.environ.copy()
env['PATH'] = '$VALIDATION_STORAGE/387b-manager-r1/pinned-tool-bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin'
env['VERILATOR_ROOT'] = '$WORKSPACE_HOME/.local/share/containers/storage/overlay/9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/share/verilator'
started = time.time()
with log.open('wb') as stream:
    result = subprocess.run(['rtk', 'proxy', *command], stdout=stream,
                            stderr=subprocess.STDOUT, env=env, timeout=10800)
record = dict(command=command, cwd=os.getcwd(), exit_code=result.returncode,
              elapsed_seconds=round(time.time()-started, 3),
              environment={k: env[k] for k in ('PATH', 'VERILATOR_ROOT')},
              log_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
receipt.write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record), flush=True)
print(log.read_text(errors='replace')[-6000:])
sys.exit(result.returncode)
