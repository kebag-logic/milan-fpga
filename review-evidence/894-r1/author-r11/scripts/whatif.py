"""What-if rows at 1x1/1if under the built design: the tree's, then each named cost replaced in process (never in the
tree). usage: python3 -I whatif.py TREE"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import edit_rows  # noqa: E402
import rows_tiers as rt  # noqa: E402

ROWS = ('R4', 'R4L', 'ACMP', 'ADP', 'MAAP', 'first', 'R5', 'R6', 'last', 'tx', 'txL')


def show(name, i, edit=None):
    saved = dict(edit_rows.EDIT_RECORD_US)
    if edit is not None:
        edit_rows.EDIT_RECORD_US['1x1/1if'] = edit
    try:
        got = rt.rows(tree, '1x1/1if', rt.BUILT, i)
    finally:
        edit_rows.EDIT_RECORD_US.clear()
        edit_rows.EDIT_RECORD_US.update(saved)
    b = rt.bounds_at(i)
    cells = [f"{row} {got[row][0]:.2f}{'*' if got[row][0] is None or got[row][0] > b[row] else ''}" for row in ROWS]
    print(f'{name:58s} ' + ', '.join(cells))


i = rt.point_inputs(tree, '1x1/1if')
print(f"pace {i.pace_ms} ms, record.aecp {i.c['record.aecp']} us, edit {edit_rows.EDIT_RECORD_US['1x1/1if']} us, "
      f"TICK {i.c['event.TICK']} us; * over its bound")
show('the tree', i)
show('edit class 260 (arm B output REMOVE 24,360)', i, 260)
show('edit class 295 (the head 27,851)', i, 295)
for flat in (240, 295, 355):
    show(f'flat record.aecp {flat}, no split', i._replace(c={**i.c, 'record.aecp': flat}), flat)
show('non-edit 355 (arm B SET_CONFIGURATION), edit 260', i._replace(c={**i.c, 'record.aecp': 355}), 260)
