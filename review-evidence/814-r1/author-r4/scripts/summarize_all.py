"""summarize_all.py <label> <all_paths.tsv> [<n>]: the top n (default 30) setup paths over every path group of one
routed checkpoint (paths.tcl's all_paths.tsv, worst path per endpoint), and the families: summarize_paths.py's
F1-F4 rules for sys paths, else the clock pair and the generalized start and end registers, each with its worst
slack, its endpoint count and its distance from the checkpoint's worst path; then every family within 0.3 ns."""
import sys
from collections import OrderedDict
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).resolve().parent))
import summarize_paths as sp  # noqa: E402
args = sys.argv[1:]

label, tsv = args[0], args[1]
n = int(args[2]) if len(args) > 2 else 30
CLK = {'milansoc_crg_clkout0': 'sys', 'milansoc_crg_clkout1': 'milan', 'milansoc_crg_clkout4': 'idelay/ps 200 MHz'}
rows = []
for line in open(tsv).read().splitlines()[1:]:
    slack, levels, data, route, start, end, group, sclk, eclk = line.split('\t')
    rows.append((float(slack), int(levels), float(data), float(route), start, end, group, sclk, eclk))
rows.sort(key=lambda r: r[0])


def family(r):
    sclk, eclk = CLK.get(r[7], r[7] or '-'), CLK.get(r[8], r[8] or '-')
    if sclk == eclk == 'sys':
        name = sp.family(r)
        if re.match(r'F[1-4] ', name):
            return name
    return f'[{sclk} -> {eclk}] {sp.family_name(sp.cell(r[4]))} -> {sp.family_name(sp.cell(r[5]))}'


worst = rows[0][0]
print(f'# {label}: {len(rows)} endpoints over every path group, worst slack {worst:+.3f} ns')
print('| # | Slack ns | Levels | Data ns | Routing | Clocks | Start | End | Family |')
print('|---:|---:|---:|---:|---:|---|---|---|---|')
for i, r in enumerate(rows[:n], 1):
    clocks = f'{CLK.get(r[7], r[7])} -> {CLK.get(r[8], r[8])}'
    print(f'| {i} | {r[0]:+.3f} | {r[1]} | {r[2]:.3f} | {100 * r[3] / r[2]:.0f} % | {clocks} | `{sp.cell(r[4])}` | '
          f'`{sp.cell(r[5])}` | {family(r)} |')
fams = OrderedDict()
for r in rows:
    fams.setdefault(family(r), []).append(r)
print()
print('| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |')
print('|---|---:|---:|---:|---:|---:|')
for name, members in list(fams.items())[:25]:
    t = members[0]
    print(f'| {name} | {t[0]:+.3f} | {t[0] - worst:.3f} | {len(members)} | {t[1]} | {100 * t[3] / t[2]:.0f} % |')
print()
near = [(name, m[0][0]) for name, m in fams.items() if m[0][0] - worst <= 0.3]
print(f'Families within 0.3 ns of the worst path ({worst:+.3f} ns): ' +
      '; '.join(f'{name} {s:+.3f}' for name, s in near))
for name in ('F1 bridge -> SPI-flash PHY', 'F2 SDRAM arbitration -> crossing FIFO read register',
             'F3 ZQCS timer -> bank machines', 'F4 CPU DMA write bridge (inside the CPU netlist)'):
    m = fams.get(name)
    print(f'{name}: ' + (f'worst {m[0][0]:+.3f} ns, {m[0][0] - worst:.3f} ns from the worst path, {len(m)} endpoints'
                         if m else 'no endpoint among the listed paths'))
