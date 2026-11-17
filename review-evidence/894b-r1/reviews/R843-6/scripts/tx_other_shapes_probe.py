#!/usr/bin/env python3
"""Plant THE TRANSMIT's figure a millisecond under its row at the two held shapes, each in its own copy of a clean
exact-head tree, and require flip_grade.py --check at that point to refuse it by name.
usage: python3 -I tx_other_shapes_probe.py CLEAN_TREE WORK_DIR"""
import shutil
import subprocess
import sys
from pathlib import Path

base, work = Path(sys.argv[1]), Path(sys.argv[2])
L = 'sw/firmware/ctrl/loop/ctrl_loop.h'
print('# plants at the two held shapes in copies of the clean d0a2a160 tree: the 1x1/1if figure 34 -> 33, the 8x8/2if '
      'figure 105 -> 104 (both two-interface lines)')
for name, old, new, cnt, point in (('P1-1x1-33', '#define CTRL_LOOP_TX_MS 34u', '#define CTRL_LOOP_TX_MS 33u', 1, '1x1/1if'),
                                   ('P2-2if-104', '#define CTRL_LOOP_TX_MS 105u', '#define CTRL_LOOP_TX_MS 104u', 2,
                                    '8x8/2if')):
    t = work / name
    if not t.exists():
        shutil.copytree(base, t, symlinks=True)
    p = t / L
    s = p.read_text()
    assert s.count(old) == cnt, name
    p.write_text(s.replace(old, new))
    r = subprocess.run(['python3', '-B', 'tb/verilator/ctrl_service_budget/flip_grade.py', '--check', '--point', point],
                       cwd=t, capture_output=True, text=True)
    hits = [ln for ln in r.stdout.splitlines() if 'CTRL_LOOP_TX_MS' in ln and ln.startswith('OVER')]
    print(f'{name} flip --check --point {point} rc={r.returncode}: ' + (' | '.join(hits) or 'NO CTRL_LOOP_TX_MS refusal'))
