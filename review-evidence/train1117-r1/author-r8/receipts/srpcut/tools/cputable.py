"""cputable.py NEW_OUT OLD_OUT NEW OLD POINT...: the full re-measure's CPU table (CPU-TABLE-<new>.md) from analyse6.sh's
outputs: each point's survey comparison (compare-ordinary.txt), every stated cost against its measurement with the
previous head's figure for the same statement beside it, the long notice (compare-long.txt) and the AECP records by
class (record_classes.py). Scratch only (#665's ruling of 2026-11-20, item 3)."""
import re
import sys
from pathlib import Path

new_out, old_out, new, old = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
NAMES = {'1x1': '1x1/1if', '8x8-1if': '8x8/1if'}
ROW = re.compile(r'^(\S+)\s+([\d,]+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(.*)$')


def rows(path: Path) -> list[tuple]:
    out = []
    for line in path.read_text().splitlines()[2:]:
        m = ROW.match(line)
        if m and m.groups() not in out:
            out.append(m.groups())
    return out


lines = [f'# The full CPU budget re-measure at `{new}` (the SRP cut): every stated cost against its measurement', '',
         'Every arm the harness holds, every group, the formal measurement\'s options; 64 parts a point. A cost\'s '
         'measured figure is the most CPU cycles over every instance and leg; "rule" is that figure plus 5 %, rounded up '
         f'to 5 us. "`{old}`" is the previous head\'s measured figure for the same statement.', '']
for point in sys.argv[5:]:
    name = NAMES[point]
    cur = rows(new_out / f'survey-{point}/compare-ordinary.txt')
    prev = {(r[0], r[6].split(';')[0]): r[1] for r in rows(old_out / f'survey-{point}/compare-ordinary.txt')}
    over = [r for r in cur if r[5].startswith('OVER')]
    lines += [f'## {name}', '', f'{len(over)} of {len(cur)} statements exceeded.', '',
              f'| Cost | Measured, cycles | `{old}` | Rule, us | Stated, us | Verdict | Statement; where |',
              '|---|---:|---:|---:|---:|---|---|']
    for cost, cyc, us, rule, stated, verdict, where in cur:
        was = prev.get((cost, where.split(';')[0]), '-')
        v = f'**{verdict}**' if verdict.startswith('OVER') else verdict
        lines.append(f'| {cost} | {cyc} | {was} | {rule} | {stated} | {v} | {where} |')
    lines += ['', '**The long notice** (`compare-long.txt`):', '']
    lines += [f'- {l}' for l in (new_out / f'survey-{point}/compare-long.txt').read_text().splitlines()[1:]]
    rc = new_out / f'record-classes-{point}.txt'
    if rc.is_file():
        keep = [l for l in rc.read_text().splitlines() if l.startswith(('1x1/1if ', '8x8/1if ', 'REPORTED', 'REFUSED',
                                                                         'RESULT'))]
        lines += ['', '**The AECP records by class** (`record_classes.py`):', ''] + [f'- {l}' for l in keep]
    lines.append('')
print('\n'.join(lines))
