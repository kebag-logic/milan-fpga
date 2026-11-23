#!/usr/bin/env python3
"""Print bounded sections of public evidence from its immutable Git object."""
import gzip
import subprocess

ref = 'eea845dba7b561499de5cf537a5b665d72e278b1'
prefix = 'review-evidence/948-r1/author-r3/receipts/'
selected = {
    'gates/gates-64117b77.txt': None,
    'rtl/avtp_rxmon-suite-64117b77.log.gz': ['FANOUT N=8:', 'DEPKT:', 'pending DEPKT tallies are three bits', 'half-full DEPKT tally waits', '24 checks:'],
    'twin/twin-gate-64117b77.log.gz': ['caught (shared):', 'caught (one-index):', 'END rc='],
    'rtl/dt5-plant/result.txt': None,
    'fit/SUMMARY.txt': None,
}
for path, needles in selected.items():
    data = subprocess.check_output(['git', 'show', f'{ref}:{prefix}{path}'])
    if path.endswith('.gz'):
        data = gzip.decompress(data)
    print(f'ARTIFACT {prefix}{path} AT {ref}')
    for line in data.decode().splitlines():
        if needles is None or any(n in line for n in needles):
            print(line)
