#!/usr/bin/env python3
"""Run selected AECP campaign rows (named) plus extra reviewer plants against a tree, each in the campaign's own
isolated copy. usage: run_rows.py TREE OUT SHARD_INDEX SHARD_COUNT [--extra] [NAME...]"""
import sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(tree / 'sw/firmware/gtest'))
import aecp_mutants as am  # noqa: E402
import aecp_map_mutants as mm  # noqa: E402
out, idx, cnt = Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rest = sys.argv[5:]
extra = '--extra' in rest
names = [a for a in rest if a != '--extra']
EXTRA = (
    # reviewer plant R1: the BARRED pass over another output port's map cut to the own map's reach
    ('rev-foreign-pass-cut-to-reach', 'aecp_maps.c',
     'size_t k = match != 0u ? 0u : e->from;', 'size_t k = match == FOUND ? 0u : e->from;',
     (mm.OWNER, ''),),
    ('rev-foreign-pass-end-at-reach', 'aecp_maps.c',
     'size_t end = match != 0u ? count : e->to;', 'size_t end = match == FOUND ? count : e->to;',
     (mm.OWNER, ''),),
    # reviewer plant R2: the reach's end held one row past its last (a semantics-neutral control: must NOT be caught)
    ('rev-neutral-reach-to-count', 'aecp_maps.c',
     '\t\te->to = to;', '\t\te->to = count;', (mm.EDIT, ''),),
    # reviewer plant R3: a REMOVE that starts at row 0 (neutral control)
    ('rev-neutral-reach-from-zero', 'aecp_maps.c',
     '\t\te->from = from;', '\t\te->from = 0u;', (mm.EDIT, ''),),
)
sel = [d for d in am.DEFECTS if not names or d.name in names]
if extra:
    sel += [am.Defect(n, 'aecp/' + f, o, w, tuple(cs)) for n, f, o, w, *cs in EXTRA]
print('selected', len(sel), [d.name for d in sel][:40], flush=True)
am.controls()  # the full table's drift check at this tree, before narrowing
print('full-table controls: pass', flush=True)
am.DEFECTS = tuple(sel)
am.controls = lambda: None
sys.exit(int(am.campaign(out, jobs=2, shard=(idx, cnt), stack=(tree / 'third_party/tsn-c-stack').resolve())))
