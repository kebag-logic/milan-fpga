"""Run one foreground gate and retain bounded receipts."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
SCRATCH = Path('/tmp/580-a368')
SCRATCH.mkdir(exist_ok=True)
name, *command = sys.argv[1:]
log = SCRATCH / (name + '.log')
started = time.time()
print('START', name, flush=True)
with log.open('wb') as stream:
    result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                            timeout=14400, check=False)
data = log.read_bytes()
receipt = dict(name=name, command=command, cwd=os.getcwd(), rc=result.returncode,
               elapsed_seconds=round(time.time()-started, 3), log=str(log),
               bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
(OUT / (name + '.json')).write_text(json.dumps(receipt, indent=2) + '\n')
if len(data) <= 200000:
    shutil.copyfile(log, OUT / log.name)
print(json.dumps(receipt), flush=True)
print('\n'.join(data.decode(errors='replace').splitlines()[-16:]), flush=True)
sys.exit(result.returncode)
