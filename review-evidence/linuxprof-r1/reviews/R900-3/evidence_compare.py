#!/usr/bin/env python3
"""Compare immutable public evidence with independently repeated checks."""
import hashlib
import json
from pathlib import Path
import re
packet = Path(__file__).resolve().parent
pub = packet / 'scratch/published'
r3 = pub / 'author-r3/receipts'

def budget_payload(name):
    text = (r3 / name).read_bytes()
    text = text.split(b'\n', 1)[1]
    return re.sub(rb'rc=\d+ seconds=\d+\n?$', b'', text)

for stem, own in [('shape_costs_check', 'shape-check'), ('shape_costs_selftest', 'shape-selftest'),
                  ('load_grade_check', 'load-check'), ('flip_grade_check_1x1', 'flip-1x1'),
                  ('flip_grade_check', 'flip-all'), ('run_selftest', None)]:
    a, b = [budget_payload('budget_' + stem + '_' + rev + '.txt') for rev in ('base', 'head')]
    assert a == b, stem
    print(stem, 'published base/head stdout IDENTICAL', len(a.splitlines()), 'lines', hashlib.sha256(a).hexdigest())
    if own:
        current = (packet / (own + '.log')).read_bytes()
        assert current == b, stem
        print(' independently repeated head stdout IDENTICAL, rc', (packet / (own + '.rc')).read_text().strip())
    else:
        assert b'Traceback' not in b
        print(' timeout at 580 seconds at both revisions; NO completed self-test verdict')

base = json.loads((r3 / 'identity-854bd723.json').read_text())
head = json.loads((r3 / 'identity-58f7673b.json').read_text())
prior = json.loads((pub / 'author-r2/receipts/identity-66b4def3.json').read_text())
assert base == head == prior and len(base) == 245
print('FPGA manifests: 245/245 entries IDENTICAL at source base, prior head and exact head')
print('Full-tree published receipt:', (r3 / 'identity_fulltree.txt').read_text().strip())
pre = (r3 / 'fpga_preproc_base_vs_head.txt').read_text()
assert pre.count('SAME if=') == 12 and pre.count('ctrl_loop.o identical') == 6
assert 'MBX_N_IF=2u' in pre and 'compared 12 points; 6 ctrl_loop.o pairs byte-identical; differ=0' in pre
print('Published compile receipt: 12 preprocessor points SAME, 6 object pairs byte-identical; force-included interface count recorded')
board = (r3 / 'board_host_build.txt').read_text()
assert 'afc350641dc2d93cee39bb4c62258b6d55f00ccb' in board
assert 'objects: 35 identical, 0 differ' in board and 'binary: byte-identical' in board
print('Board build receipt: 35 objects and binary identical; public board revision afc350641dc2d93cee39bb4c62258b6d55f00ccb')
for line in board.splitlines():
    if 'sha256' in line or line.startswith(('fw/ctrl_loop.o:', 'control program binary:')):
        print(line)
print('Evidence class: author source receipts; no manager source-bank or candidate execution inferred')
print('RESULT: PASS')
