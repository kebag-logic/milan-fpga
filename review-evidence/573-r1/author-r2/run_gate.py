"""Run one foreground gate with bounded logs and its true return code."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
SCRATCH = Path('/tmp/573-a352')
name, *command = sys.argv[1:]
log = SCRATCH / f'{name}.log'
start = time.monotonic()
with log.open('wb') as stream:
    result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                            timeout=10800)
blob = log.read_bytes()
# Public receipts omit identifying home paths while retaining raw hashes.
text = blob.decode(errors='replace').replace(str(Path.home()), '$USER_HOME')
parts = [text[i:i + 150000] for i in range(0, len(text), 150000)] or ['']
logs = []
for i, part in enumerate(parts):
    dest = OUT / (f'{name}.log' if len(parts) == 1 else f'{name}.{i+1}.log')
    dest.write_text(part)
    logs.append(dest.name)
receipt = dict(gate=name, command=command, returncode=result.returncode,
               seconds=round(time.monotonic()-start, 2), bytes=len(blob),
               raw_sha256=hashlib.sha256(blob).hexdigest(), logs=logs)
(OUT / f'{name}.result.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt), flush=True)
print('\n'.join(text.splitlines()[-8:]), flush=True)
sys.exit(result.returncode)
