"""Probe rows_tiers.tx_statements at the head and with each interface leg planted one under its row.
Usage: python3 -I -B tx_probe.py <repo-root>"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import rows_tiers  # noqa: E402
loop = 'sw/firmware/ctrl/loop/ctrl_loop.h'
text = (root / loop).read_text()
fig = '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 99u)'
print('figure present once:', text.count(fig) == 1)
print('head, both points:', rows_tiers.tx_statements(root))
for p in rows_tiers.POINTS:
    print('head', p, rows_tiers.tx_statements(root, (p,)))
for leg, p in (('33u : 99u', '1x1/1if'), ('34u : 98u', '8x8/2if'), ('34u : 99u', None)):
    t = {loop: text.replace(fig, fig.replace('34u : 99u', leg))}
    print('planted', leg, {q: rows_tiers.tx_statements(root, (q,), t) for q in rows_tiers.POINTS})
