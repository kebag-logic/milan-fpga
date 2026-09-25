from pathlib import Path
import json

OUT = Path(__file__).resolve().parent
TOPS = {'milan_csr', 'KL_pp_shadow', 'milan_datapath'}
COLUMNS = ['LUT', 'LUTRAM', 'LUT_TOT', 'FF', 'RAMB36', 'RAMB18', 'DSP', 'CARRY4']

def read_rows(name):
    rows = {}
    for line in (OUT / name).read_text().splitlines():
        words = line.split()
        if words and words[0] in TOPS:
            rows[words[0]] = dict(zip(COLUMNS, map(int, words[1:]), strict=True))
    return rows

base = read_rows('ooc-base.log')
head = read_rows('ooc-head-main.log') | read_rows('ooc-head-csr.log')
assert set(base) == set(head) == TOPS
result = {top: dict(base=base[top], head=head[top], delta={key: head[top][key]-base[top][key] for key in COLUMNS}) for top in sorted(TOPS)}
(OUT / 'area.json').write_text(json.dumps(result, indent=2)+'\n')
lines = ['| Module | ' + ' | '.join(COLUMNS) + ' |', '|---|' + '---:|' * len(COLUMNS)]
for top in sorted(TOPS):
    lines.append('| ' + top + ' | ' + ' | '.join(str(result[top]['delta'][key]) for key in COLUMNS) + ' |')
(OUT / 'area-delta.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
