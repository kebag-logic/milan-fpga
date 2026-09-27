"""Run one foreground gate, retain its exit status and bounded evidence."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

output = Path(__file__).resolve().parent
scratch = Path('/tmp/573-a355/logs')
scratch.mkdir(parents=True, exist_ok=True)
label, *command = sys.argv[1:]
log = scratch / (label + '.log')
started = time.time()
with log.open('wb') as stream:
    result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                            timeout=10800, check=False)
data = log.read_bytes()
saved = output / (label + '.log')
if len(data) <= 190000:
    saved.write_bytes(data)
else:
    saved.write_bytes(data[:40000] + b'\n[Excerpt: complete log retained in scratch.]\n' + data[-140000:])
row = dict(gate=label, command=command, cwd=os.getcwd(), returncode=result.returncode,
           seconds=round(time.time()-started, 2), log_bytes=len(data),
           log_sha256=hashlib.sha256(data).hexdigest(), evidence=saved.name)
with (output / 'gate-results.jsonl').open('a') as stream:
    stream.write(json.dumps(row) + '\n')
print(json.dumps(row), flush=True)
if result.returncode:
    print(data[-5000:].decode(errors='replace'), flush=True)
sys.exit(result.returncode)
