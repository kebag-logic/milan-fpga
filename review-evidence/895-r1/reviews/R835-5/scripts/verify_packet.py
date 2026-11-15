#!/usr/bin/env python3
"""verify_packet.py RECEIPTS_DIR TREE

Reviewer check of a published author packet and of its class figures:
1. every row of RECEIPTS_DIR/INDEX.md (file, bytes, sha256, per section) against the file's bytes, and every file
   under RECEIPTS_DIR listed;
2. the class maxima the packet states, recomputed by TREE's own record_classes.rule, and TREE's stated class costs
   (record_classes.statements) at 1x1/1if and 8x8/2if.
Read-only. Exit 1 on any mismatch."""
import hashlib
import os
import re
import sys
from pathlib import Path

rec, tree = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
bad = ok = 0
seen = set()
section = '.'
for line in (rec / 'INDEX.md').read_text().splitlines():
    m = re.match(r'## (.+)', line)
    if m:
        section = m.group(1).strip()
        continue
    m = re.match(r'\| (\S+) \| (\d+) \| `([0-9a-f]{64})` \|', line)
    if m:
        p = os.path.normpath(os.path.join(section, m.group(1)))
        seen.add(p)
        f = rec / p
        b = f.read_bytes() if f.is_file() else None
        if b is not None and len(b) == int(m.group(2)) and hashlib.sha256(b).hexdigest() == m.group(3):
            ok += 1
        else:
            bad += 1
            print('MISMATCH', p)
present = {str(p.relative_to(rec)) for p in rec.rglob('*') if p.is_file()} - {'INDEX.md'}
unlisted = sorted(present - seen)
print(f'INDEX rows verified {ok}, mismatched {bad}, unlisted files {len(unlisted)} {unlisted}')

sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import record_classes as rc  # noqa: E402

stated = {p: rc.statements(p, tree) for p in ('1x1/1if', '8x8/2if')}
print('stated', stated)
claims = [  # point, class, cycles, rule us claimed
    ('1x1/1if', 'paced', 28288, 300), ('1x1/1if', 'other', 21187, 225), ('1x1/1if', 'long', 86698, 915),
    ('8x8/2if', 'paced', 55365, 585), ('8x8/2if', 'other', 18904, 200), ('8x8/2if', 'long', 126152, 1325),
    ('1x1/1if', 'other', 20363, 215), ('8x8/2if', 'other', 17511, 185), ('8x8/2if', 'other', 17300, 185),
]
for point, kind, cycles, us in claims:
    got = rc.rule(cycles, 100_000_000)
    within = got <= stated[point][kind]
    good = got == us and within
    bad += not good
    print(f'{point} {kind} {cycles:,} cycles -> {got} us (claimed {us}), stated {stated[point][kind]}: '
          f'{"ok" if good else "MISMATCH"}')
print('RESULT', 'PASS' if bad == 0 else 'FAIL')
sys.exit(1 if bad else 0)
