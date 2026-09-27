"""Run one foreground command and retain bounded evidence."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
WORK = Path('$VALIDATION_STORAGE/580-a366')
ROOT = Path('$LANES/580-pp-pin-16be6768')
name, *command = sys.argv[1:]
log = WORK / (name + '.log')
start = time.monotonic()
print('RUN', name, command, flush=True)
with log.open('wb') as stream:
    result = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT,
                            timeout=14400, env=dict(os.environ, PYTHONUNBUFFERED='1', PYTHONHASHSEED='0'))
data = log.read_bytes()
record = dict(name=name, command=command, cwd=str(ROOT), rc=result.returncode,
              seconds=round(time.monotonic()-start, 3), log=str(log),
              bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
if len(data) <= 200000:
    shutil.copyfile(log, OUT / log.name)
    record['retained_log'] = log.name
else:
    (OUT / (name + '.tail.txt')).write_bytes(data[-24000:])
with (OUT / 'gate-results.jsonl').open('a') as stream:
    stream.write(json.dumps(record) + '\n')
print(json.dumps(record), flush=True)
print(data[-5000:].decode(errors='replace'), flush=True)
raise SystemExit(result.returncode)
