#!/usr/bin/env python3
"""apply.py CLONE ORDER [TRACE...]: the learned order (order.py) into a scratch clone's hot list, both copies:
sw/firmware/ctrl/plat/ctrl_split_hot.txt (its header kept, a note of the traces added, the entries replaced) and the
block of sw/firmware/ctrl/plat/ctrl_split.ld between _ctrl_hot_start and _ctrl_hot_end (one `*-<stem>.o(.text.<f>)`
a line, as ctrl_hot.entry spells it). Prints how the order differs from the one it replaces. Scratch only."""
import hashlib
import sys
from pathlib import Path

clone, order = Path(sys.argv[1]), Path(sys.argv[2])
traces = [Path(t) for t in sys.argv[3:]]
plat = clone / 'sw/firmware/ctrl/plat'
sys.path.insert(0, str(clone / 'sw/firmware/ctrl/test'))
import ctrl_hot  # noqa: E402

new = [tuple(line.split()) for line in order.read_text().splitlines() if line.strip()]
hot = plat / 'ctrl_split_hot.txt'
text = hot.read_text()
old = ctrl_hot.recorded(text)
header = [line for line in text.splitlines() if line.startswith('#')]
note = ['#', '# Relearned for decision 3 (#665, ruling of 2026-11-17) by the procedure above on the step-9 tip of the',
        '# flip train (scratch, not committed); the traces\' sha256:',
        *[f'#   {t.stem:<12} {hashlib.sha256(t.read_bytes()).hexdigest()}' for t in traces]]
hot.write_text('\n'.join(header + note) + '\n' + ''.join(f'{s} {f}\n' for s, f in new))
ld = plat / 'ctrl_split.ld'
script = ld.read_text()
a = script.index(ctrl_hot.START) + len(ctrl_hot.START)
b = script.index(ctrl_hot.END)
indent = '\t\t'
script = script[:a] + '\n' + ''.join(f'{indent}{ctrl_hot.entry(e)}\n' for e in new) + indent + script[b:]
ld.write_text(script)
gone = [e for e in old if e not in new]
added = [e for e in new if e not in old]
kept = [e for e in new if e in old]
moved = sum(1 for k, e in enumerate(kept) if [x for x in old if x in kept].index(e) != k)
print(f'old {len(old)} entries, new {len(new)}: {len(added)} added, {len(gone)} gone, {moved} of {len(kept)} kept '
      f'in another place')
print('added:', ' '.join(f'{s}:{f}' for s, f in added))
print('gone:', ' '.join(f'{s}:{f}' for s, f in gone))
