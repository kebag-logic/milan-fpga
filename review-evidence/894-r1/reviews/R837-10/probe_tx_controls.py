"""Probe: the two THE TRANSMIT statement controls (rows_tiers.channel_controls and flip_grade.channel_controls) at the
head, and with rows_tiers.tx_statements mutated in memory to skip one interface count. Usage:
    python3 -I probe_tx_controls.py <checkout>/tb/verilator/ctrl_service_budget
No file is written; the mutation is an in-process patch of the module attribute."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import rows_tiers  # noqa: E402
import flip_grade  # noqa: E402

ROOT = flip_grade.ROOT
ORIG = rows_tiers.tx_statements
TAG = "THE TRANSMIT's stated figure under its row"


def skipping(skip):
    def m(root, points=rows_tiers.POINTS, texts=None):
        return ORIG(root, tuple(p for p in points if p != skip), texts)
    return m


def run(label, patch):
    rows_tiers.tx_statements = patch or ORIG
    try:
        a = [e for e in rows_tiers.channel_controls(ROOT) if 'TRANSMIT' in e]
        b = [e for e in flip_grade.channel_controls(ROOT) if 'TRANSMIT' in e]
        direct = rows_tiers.tx_statements(ROOT)
    finally:
        rows_tiers.tx_statements = ORIG
    print(f'{label}: tx_statements(head)={direct} rows_tiers escaped={a} flip_grade escaped={b}')
    return a, b, direct


ok = True
a, b, d = run('head', None)
ok &= a == [] and b == [] and d == []
for skip in ('8x8/2if', '1x1/1if'):
    a, b, d = run(f'mutant skip {skip}', skipping(skip))
    ok &= TAG in ' '.join(a) and TAG in ' '.join(b)
print('PROBE', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
