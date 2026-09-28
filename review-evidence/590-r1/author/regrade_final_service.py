"""Regrade retained native evidence after verifying compiled-source and log bindings."""
from pathlib import Path
import hashlib
import json
import shlex
import subprocess
import time

root = Path.cwd()
out = Path(__file__).parent
assert root == Path('$LANES/590-592-599-firmware')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
inventory = json.loads((out/'final3-command-inventory.json').read_text())
results = []
for row in inventory:
    name = row['name']
    if not ((name.startswith(('service-1x1-', 'service-8x8-'))) or name == 'remove-dispatch'):
        continue
    assert row['rc'] == 0
    command = shlex.split(row['command'])
    command = command[:command.index('>')] + ['--regrade']
    log = Path('/tmp/a385-final-regrade-' + name + '.log')
    start = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
    results.append(dict(name='bound-' + name, head=head, command=command, rc=result.returncode,
                        seconds=round(time.monotonic()-start,3), path=str(log), size=log.stat().st_size,
                        sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
    (out/'final-target-gates.json').write_text(json.dumps(results, indent=2)+'\n')
    print(name, result.returncode, flush=True)
    assert result.returncode == 0
assert len(results) == 11
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip() == head
