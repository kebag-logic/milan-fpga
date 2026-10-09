"""Run the documented workflow commands in bounded foreground partitions."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--root', type=Path, required=True)
p.add_argument('--scratch', type=Path, required=True)
p.add_argument('--part', type=int, required=True)
p.add_argument('--parts', type=int, default=3)
a = p.parse_args()
assert 0 <= a.part < a.parts
commands = json.loads((Path(__file__).parent / 'docs-commands.json').read_text())
a.scratch.mkdir(parents=True, exist_ok=True)
receipts = []
for i in range(a.part, len(commands), a.parts):
    command = [arg.replace('$DOC_PYTHON', sys.executable).replace('$F5_SCRATCH', str(a.scratch.resolve())) for arg in commands[i]]
    start = time.monotonic()
    with (a.scratch / f'docs-{i:02}.log').open('w') as log:
        result = subprocess.run(command, cwd=a.root, stdout=log, stderr=subprocess.STDOUT, timeout=500)
    receipts.append(dict(index=i, command=command, rc=result.returncode, seconds=time.monotonic()-start))
    print(i, result.returncode, flush=True)
    assert result.returncode == 0, command
(a.scratch / f'docs-receipts{a.part}.json').write_text(json.dumps(receipts, indent=2) + '\n')
