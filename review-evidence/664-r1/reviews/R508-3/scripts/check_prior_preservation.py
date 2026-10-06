#!/usr/bin/env python3
"""Verify the previously corrected clauses/hooks and retained prose residue."""
from pathlib import Path
import os
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = {**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_OPTIONAL_LOCKS': '0'}
approved = '8fb296e3e02985aee27ef04cb08278836b734a14'


def source(ref, path):
    return subprocess.check_output(['git', '-C', str(root), 'show', ref + ':' + path], env=env).decode()


path = 'docs/reference/FR_NFR.md'
old, new = source(approved, path), source('HEAD', path)
for prefix in ['| MAAP PROBE and conflict DEFEND |', '| MAAP ANNOUNCE and reallocation |', '| Listener ADP AVAILABLE, DEPARTING and discovery aging |', '| H-DISC |']:
    old_row = next(line for line in old.splitlines() if line.startswith(prefix))
    new_row = next(line for line in new.splitlines() if line.startswith(prefix))
    assert new_row == old_row
    print('PASS: approved correction unchanged:', prefix)
start = 'H-DISC follows discovery events through their connection actions.'
end = 'Each hook MUST run at every supported stream/channel/rate shape.'
assert old.split(start)[1].split(end)[0] == new.split(start)[1].split(end)[0]
print('PASS: full listener discovery checks and single allowance are unchanged')
path = 'docs/design/MAILBOX_SPLIT.md'
old, new = source(approved, path), source('HEAD', path)
start = '**Listener discovery (F3):**'
if start not in old:
    # All prior design bytes are retained: only the new scope note is inserted.
    at = new.index('The following describes the implemented F0 filter.')
    end = new.index('A frame is classified by EtherType', at)
    assert new[:at] + new[end:] == old
else:
    assert old.split(start)[1] == new.split(start)[1]
print('PASS: mailbox design retains the approved listener correction')
path = 'sw/firmware/ctrl_nvm/README.md'
old, new = source(approved, path), source('HEAD', path)
assert old == new
assert "- The #665 switch and its link: F0's switch is not merged, so no image links\n  this store." in new
print('RETAINED: R509-2-R1; RESIDUE; Docs; unchanged obsolete switch publication wording')
print('EXACT FIX: - The #665 switch and its link: no image links this store yet.')
