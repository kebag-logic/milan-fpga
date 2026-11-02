#!/usr/bin/env python3
"""Plant one reviewer mutant into a disposable copy of the tree.

Usage: plant.py <copy root> <name>
  step-beside-input   ctrl_loop.c: THE STEP called in every pass, input or not
  both-builds         srp_mbx.c: the one-build-a-pass deferral removed
  room-is-deadline    nvm_store.c: the step admitted while any time is left before the deadline
"""
import sys
from pathlib import Path

PLANTS = {
    'step-beside-input': ('sw/firmware/ctrl/loop/ctrl_loop.c', 'if (l->step != NULL && work == 0u) {',
                          'if (l->step != NULL) {'),
    'both-builds': ('sw/firmware/ctrl/srp/srp_mbx.c', 'if (!i->msrp && (built || !builds_first(m,n))) {',
                    'if (false && !i->msrp && (built || !builds_first(m,n))) {'),
    'room-is-deadline': ('sw/firmware/ctrl_nvm/nvm_store.c',
                         'if ((int32_t)(deadline - nvm_store_clock(ctx)) < (int32_t)NVM_STEP_US) {',
                         'if ((int32_t)(deadline - nvm_store_clock(ctx)) < 0) {'),
}
root, name = Path(sys.argv[1]), sys.argv[2]
path, old, new = PLANTS[name]
p = root / path
s = p.read_text()
assert s.count(old) == 1, f'{name}: anchor not unique in {path}'
p.write_text(s.replace(old, new))
print(f'planted {name} in {p}')
