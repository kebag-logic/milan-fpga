#!/usr/bin/env python3
"""Read the head's timing derivations and solve each allowed pace."""
import math
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root/'tb/verilator/ctrl_service_budget'))
import join_grade
import paced_rows
import rows_tiers
import queued_bound
from unittest.mock import patch

i = rows_tiers.point_inputs(root, '1x1/1if')
print('TX bound:', rows_tiers.TX_BUDGET_MS)
print('R4L bound:', paced_rows.PACED_BOUNDS)
print('Join commit bounds:', join_grade.LEAST_MS, join_grade.MOST_MS)
print('Largest legal record:', rows_tiers.LONG_RECORD_US['1x1/1if'], 'us')
print('P txL R4L')
for p in range(1, 14):
    j = i._replace(pace_ms=p)
    print(p, rows_tiers.solve('txL', j, rows_tiers.BUILT)[0], rows_tiers.solve('R4L', j, rows_tiers.BUILT)[0])
print('Chosen pace:', paced_rows.choice(root), 'stated:', i.pace_ms)
print('Queued bound findings:', queued_bound.statements(root))
print('Gate count findings:', paced_rows.count_findings())
with patch.object(paced_rows, 'edits', lambda w, p: 1 + math.floor(w/p)):
    print('Old-count mutant findings:', paced_rows.count_findings())
cycles = 92766
print('Record padding: ceil(max_cycles / 100 * 1.05 / 5) * 5 =', math.ceil(cycles/100*1.05/5)*5, 'us')
