#!/usr/bin/env python3
"""Undo each conflict resolution's merged term in a copy of sw/mailbox; the generator's check and self-test must refuse."""
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
PROBES = [
    ('crosscheck list loses the source registers', 'sw/mailbox/gen_mailbox.py',
     '+ contract.pub_source_registers ', ''),
    ('crosscheck list loses the face registers', 'sw/mailbox/gen_mailbox.py',
     '+ contract.face_registers + contract.face_source_registers + contract.face_sink_registers', ''),
    ('register decode regex loses PUB_SRC_REG', 'sw/mailbox/gen_mailbox.py', 'PUB_REG|PUB_SRC_REG|PUB_SINK_REG', 'PUB_REG|PUB_SINK_REG'),
    ('register decode regex loses FACE_REG', 'sw/mailbox/gen_mailbox.py', 'PUB_SINK_REG|FACE_REG"', 'PUB_SINK_REG"'),
    ('skeleton check loses the source whole-word rule', 'sw/mailbox/mailbox_skeleton.py',
     'if any(f.lsb != 0 or f.width != 32 for r in contract.pub_source_registers for f in r.fields):', 'if False:'),
    ('skeleton check loses the face check', 'sw/mailbox/mailbox_skeleton.py', '    face.check(contract)\n', ''),
    ('version minor back to 3', 'sw/mailbox/mailbox.yaml', '  minor: 4\n', '  minor: 3\n'),
]
cmd = [sys.executable, '-B', 'sw/mailbox/gen_mailbox.py', '--check', '--crosscheck', '--selftest']
def run():
    r = subprocess.run(cmd, cwd=root, capture_output=True, text=True, errors='replace')
    bad = [l for l in (r.stdout + r.stderr).splitlines() if l.startswith('[BAD]') or 'finding' in l.lower() or 'error' in l.lower() or 'arm(s) failed' in l]
    return r.returncode, bad
rc, bad = run()
print(f'control rc={rc}: {bad[:3]}')
for name, path, old, new in PROBES:
    p = root / path
    was = p.read_text()
    if old not in was:
        print(f'{name}: PROBE TEXT ABSENT'); continue
    p.write_text(was.replace(old, new, 1))
    rc, bad = run()
    p.write_text(was)
    print(f'{name}: rc={rc} {"CAUGHT" if rc else "SURVIVED"}: {[b[:130] for b in bad[:2]]}')
rc, bad = run()
print(f'restored control rc={rc}')
