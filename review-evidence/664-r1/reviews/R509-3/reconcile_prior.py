#!/usr/bin/env python3
"""Check preservation of the previously corrected requirement passages."""
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
approved = '8fb296e3e02985aee27ef04cb08278836b734a14'
head = '4dab80ae4564ef8d6e1030564dcea4ba19235ee6'

def read(rev, path):
    return subprocess.check_output(['git', '-C', str(root), 'show', f'{rev}:{path}'], env=dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')).decode()

path = 'docs/reference/FR_NFR.md'
before, after = read(approved, path), read(head, path)
for prefix in ['| MAAP PROBE and conflict DEFEND |', '| MAAP ANNOUNCE and reallocation |',
               '| Listener ADP AVAILABLE, DEPARTING and discovery aging |', '| H-DISC |']:
    old = next(line for line in before.splitlines() if line.startswith(prefix))
    new = next(line for line in after.splitlines() if line.startswith(prefix))
    assert old == new
    print(f'PASS preserved prior correction: {prefix}')
start, end = 'H-DISC follows discovery events through their connection actions.', 'Each hook MUST run at every supported'
assert before.split(start)[1].split(end)[0] == after.split(start)[1].split(end)[0]
print('PASS preserved complete H-DISC adverse-transition and timing block')
path = 'docs/design/MAILBOX_SPLIT.md'
before, after = read(approved, path), read(head, path)
start, end = "The listener's discovery machine", '### Service latency'
assert before.split(start)[1].split(end)[0] == after.split(start)[1].split(end)[0]
print('PASS preserved F3 listener-discovery interface/timing boundary')
path = 'sw/firmware/ctrl_nvm/README.md'
before, after = read(approved, path), read(head, path)
assert before == after
assert "F0's switch is not merged" in after
print('RETAINED R509-2-R1 wording residue: store README unchanged and still says switch is not merged')
print('PASS prior MINOR corrections preserved at this head; PR publication wording assessed separately')
