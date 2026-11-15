"""Disposable in-process mutation probe: the THE TRANSMIT statement controls of rows_tiers.py and flip_grade.py
must escape when tx_statements stops checking 8x8/2if, and hold at the unplanted head.
Usage: python3 -B tx_leg_probe.py <clean-clone-root>"""
import sys
from pathlib import Path
from unittest import mock
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import rows_tiers, flip_grade  # noqa: E402
orig = rows_tiers.tx_statements
def one_point(r, points=rows_tiers.POINTS, texts=None):
    return orig(r, tuple(p for p in points if p != '8x8/2if'), texts)
name_rt = "THE TRANSMIT's stated figure under its row"
print('POINTS', rows_tiers.POINTS)
head_rt = rows_tiers.channel_controls(root)
print('rows_tiers head escaped:', head_rt)
with mock.patch.object(rows_tiers, 'tx_statements', one_point):
    mut_rt = rows_tiers.channel_controls(root)
print('rows_tiers 8x8-skipped escaped:', mut_rt, 'CAUGHT' if name_rt in mut_rt else 'MISSED')
head_fg = flip_grade.channel_controls(root)
print('flip_grade head escaped:', head_fg)
with mock.patch.object(rows_tiers, 'tx_statements', one_point):
    mut_fg = flip_grade.channel_controls(root)
print('flip_grade 8x8-skipped escaped:', mut_fg, 'CAUGHT' if flip_grade.CHANNEL_CONTROLS[1] in mut_fg else 'MISSED')
