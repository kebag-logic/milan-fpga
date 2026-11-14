#!/usr/bin/env python3
"""nvm_plant.py TREE OUT: the AECP campaign (aecp_mutants.campaign) of TREE with its table replaced by one defect, the
names runs' count check dropped in aecp_nvm_changed, which Nvm.EveryChangeQueuesOnlyItsOwnedRecords must catch with
its absent-records diagnostic. The campaign's own table-drift control is skipped (the table is cut). Exit 1 when the
defect escaped or was refused."""
import sys
from pathlib import Path

tree_root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree_root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(tree_root / 'sw/firmware/gtest'))
import aecp_mutants  # noqa: E402

aecp_mutants.DEFECTS = (aecp_mutants.defect(
    'nvm-name-run-count-dropped', 'aecp_nvm.c',
    'if (r->type == type && at < r->count) mark(n, NVM_G_NAME, r->ordinal + at);',
    'if (r->type == type) mark(n, NVM_G_NAME, r->ordinal + at);',
    ('Nvm.EveryChangeQueuesOnlyItsOwnedRecords', 'reserved and absent records never enter the queue')),)
aecp_mutants.controls = lambda: None
failed = aecp_mutants.campaign(out, 4)
print(f"nvm plant: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
