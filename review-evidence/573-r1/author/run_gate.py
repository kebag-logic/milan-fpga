"""Run one foreground gate with a generous deadline and bounded evidence."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path('$LANES/573-builder-refusals')
OUT = Path(__file__).resolve().parent
name, *command = sys.argv[1:]
started = time.monotonic()
with tempfile.NamedTemporaryFile(prefix='shipping-gate-', suffix='.log', delete=False) as log:
    path = Path(log.name)
    result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=7200)
data = path.read_bytes()
record = dict(gate=name, command=command, returncode=result.returncode,
              seconds=round(time.monotonic()-started, 2), bytes=len(data),
              sha256=hashlib.sha256(data).hexdigest())
if len(data) <= 200000:
    (OUT / (name + '.log')).write_bytes(data)
    record['log'] = name + '.log'
    path.unlink()
else:
    record['large_log'] = str(path)
    (OUT / (name + '.tail.log')).write_bytes(data[-40000:])
(OUT / (name + '.result.json')).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
print(data.decode(errors='replace')[-5000:])
sys.exit(result.returncode)
