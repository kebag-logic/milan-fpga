import json
import subprocess
import sys
import time
from pathlib import Path

out = Path(__file__).resolve().parent
name, *cmd = sys.argv[1:]
start = time.monotonic()
with (out / (name + '.log')).open('w') as log:
    log.write('$ ' + ' '.join(cmd) + '\n')
    log.flush()
    result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=14400)
record = dict(name=name, command=cmd, rc=result.returncode, seconds=round(time.monotonic()-start, 2))
with (out / 'gates.jsonl').open('a') as log:
    log.write(json.dumps(record) + '\n')
print(json.dumps(record), flush=True)
print('\n'.join((out / (name + '.log')).read_text(errors='replace').splitlines()[-10:]))
sys.exit(result.returncode)
