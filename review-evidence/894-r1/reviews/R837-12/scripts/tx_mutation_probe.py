"""Mutation probe: make rows_tiers.tx_statements blind to 8x8/2if (and, separately, to 1x1/1if) in-process, and
require both self-test controls of THE TRANSMIT's stated figure to report the escape. No file is written.
Usage: python3 -I -B tx_mutation_probe.py <repo-root>"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import rows_tiers, flip_grade  # noqa: E402,E401
real = rows_tiers.tx_statements
name = "THE TRANSMIT's stated figure under its row"
print('head: rows_tiers', [e for e in rows_tiers.channel_controls(root) if 'TRANSMIT' in e],
      'flip_grade', [e for e in flip_grade.channel_controls(root) if 'TRANSMIT' in e])
ok = True
for blind in ('8x8/2if', '1x1/1if'):
    def mutant(r, points=rows_tiers.POINTS, texts=None, blind=blind):
        return [f for f in real(r, points, texts) if not f.startswith(blind)]
    rows_tiers.tx_statements = mutant
    a = [e for e in rows_tiers.channel_controls(root) if 'TRANSMIT' in e]
    b = [e for e in flip_grade.channel_controls(root) if 'TRANSMIT' in e]
    rows_tiers.tx_statements = real
    caught = name in a and any('TRANSMIT' in e for e in b)
    ok &= caught
    print(f'blind to {blind}: rows_tiers escaped {a}; flip_grade escaped {b}; caught by both: {caught}')
print('RESULT:', 'PASS' if ok else 'FAIL')
