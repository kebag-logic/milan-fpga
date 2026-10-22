#!/usr/bin/env python3
"""Re-record pin-derived budgets and ROM ledger in a disposable exact-head clone."""
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
assert repo.is_relative_to(packet / 'scratch'), 'use only a disposable clone'
commands = [
    ['bash', 'syn/yosys/ooc.sh', '--record-rom-digests'],
    ['python3', 'scripts/check_port_contracts.py', '--write-budget'],
    ['python3', 'scripts/measure_naming.py', '--write-budget'],
    ['git', 'diff', '--exit-code', '--', 'syn/yosys/rom_digests.tsv', 'scripts/port_docs.budget', 'scripts/naming.budget'],
]
with (packet / 'regenerated-records.log').open('w') as log:
    for command in commands:
        print('COMMAND', ' '.join(command), file=log, flush=True)
        p = subprocess.run(command, cwd=repo, stdout=log, stderr=subprocess.STDOUT, timeout=180)
        print('RC', p.returncode, file=log, flush=True)
        if p.returncode:
            (packet / 'regenerated-records.rc').write_text(str(p.returncode) + '\n')
            sys.exit(p.returncode)
    print('PASS: all three generated records are byte-identical', file=log)
(packet / 'regenerated-records.rc').write_text('0\n')
print('PASS generated ROM, port-contract and naming records')
