"""Run one foreground gate, retaining a bounded receipt and full scratch log."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path('$LANES/602-phc-step-mr')
OUT = Path(__file__).resolve().parent
WORK = Path('$VALIDATION_STORAGE/602-a388-work')

name, seconds, *command = sys.argv[1:]
log = WORK / (name + '.log')
head = subprocess.check_output(['rtk', 'proxy', 'git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
start = time.monotonic()
env = dict(os.environ, VERILATOR_JOBS='8', PYTHONUNBUFFERED='1')
env['PATH'] = '$VALIDATION_STORAGE/602-a383-work/venv/bin' + os.pathsep + env['PATH']
with log.open('wb') as stream:
    result = subprocess.run(['rtk', 'proxy', 'timeout', '--signal=TERM', '--kill-after=60', seconds, *command],
                            cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT, check=False)
data = log.read_bytes()
receipt = dict(name=name, head=head, cwd=str(ROOT), command=command, timeout=seconds,
               rc=result.returncode, seconds=round(time.monotonic()-start, 2),
               log=str(log), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
(OUT/(name+'.json')).write_text(json.dumps(receipt, indent=2)+'\n')
if len(data) <= 190000:
    (OUT/(name+'.log')).write_bytes(data)
else:
    (OUT/(name+'.tail.log')).write_bytes(data[-20000:])
print(json.dumps(receipt, indent=2))
print(data[-3000:].decode(errors='replace'))
sys.exit(result.returncode)
