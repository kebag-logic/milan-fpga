from pathlib import Path
import json
import os
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
name, cwd, *command = sys.argv[1:]
env = dict(os.environ)
env['PATH'] = '/tmp/551-a260-sv2v:$VALIDATION_TOOLS/verilator-v5.050/bin:' + env['PATH']
start = time.monotonic()
with (out / (name + '.log')).open('w') as log:
    result = subprocess.run(command, cwd=cwd, env=env, stdout=log,
                            stderr=subprocess.STDOUT, timeout=7200, check=False)
record = {'name': name, 'cwd': cwd, 'command': command,
          'rc': result.returncode, 'seconds': round(time.monotonic()-start, 2)}
with (out / 'gates.jsonl').open('a') as ledger:
    ledger.write(json.dumps(record) + '\n')
print(json.dumps(record))
print('\n'.join((out / (name + '.log')).read_text(errors='replace').splitlines()[-12:]))
sys.exit(result.returncode)
