"""summarize_paths.py <label> <sys_paths.tsv> [<n>]: the top n (default 20) sys setup paths of one routed checkpoint
(paths.tcl's worst path per endpoint), each with its levels, data delay and routing share, and the path families:
start and end register names with bit indices and bank-machine numbers generalized, each with its worst slack, its
endpoint count and its distance from the checkpoint's worst path."""
import re
import sys
from collections import OrderedDict

label, tsv = sys.argv[1:3]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 20
rows = []
for line in open(tsv).read().splitlines()[1:]:
    slack, levels, data, route, start, end = line.split('\t')
    rows.append((float(slack), int(levels), float(data), float(route), start, end))
rows.sort(key=lambda r: r[0])


def cell(pin):
    """The register a pin belongs to, without the hierarchy the optimizer folded it under."""
    return pin.rsplit('/', 1)[0].rsplit('/', 1)[-1]


def family_name(name):
    """Bit indices, replica suffixes and numbered instances generalized."""
    name = re.sub(r'\[\d+\]', '[*]', name)
    name = re.sub(r'_replica(_\d+)?', '', name)
    name = re.sub(r'(bankmachine|storage_|cdc|impl)\d+', r'\1N', name)
    return re.sub(r'_\d+(_|$)', r'_N\1', name)


def family(row):
    """Which family a path belongs to: the #814 families by their registers, else start -> end. F1 is any
    path into the SPI-flash core or PHY from outside the PHY (from the bridge, or a stage register in front)."""
    start, end = cell(row[4]), cell(row[5])
    if 'spiflash' in end and not re.match(r'(milansoc_)?spiflash_phy', start):
        return 'F1 bridge -> SPI-flash PHY'
    if re.match(r'(milansoc_(read|write)_|milansoc_sdram_)', start) and re.match(r'storage_\d+_dat1_reg', end):
        return 'F2 SDRAM arbitration -> crossing FIFO read register'
    if 'zqcs_timer' in start:
        return 'F3 ZQCS timer -> bank machines'
    if 'downW_header' in start:
        return 'F4 CPU DMA write bridge (inside the CPU netlist)'
    return f'{family_name(start)} -> {family_name(end)}'


worst = rows[0][0]
print(f'# {label}: {len(rows)} sys endpoints, worst slack {worst:+.3f} ns')
print(f'| # | Slack ns | Levels | Data ns | Routing | Start | End | Family |')
print('|---:|---:|---:|---:|---:|---|---|---|')
for i, row in enumerate(rows[:n], 1):
    print(f'| {i} | {row[0]:+.3f} | {row[1]} | {row[2]:.3f} | {100 * row[3] / row[2]:.0f} % | `{cell(row[4])}` | '
          f'`{cell(row[5])}` | {family(row)} |')
families = OrderedDict()
for row in rows:
    families.setdefault(family(row), []).append(row)
print()
print('| Family | Worst slack ns | From the worst path ns | Endpoints | Levels at its worst | Routing at its worst |')
print('|---|---:|---:|---:|---:|---:|')
for name, members in list(families.items())[:12]:
    top = members[0]
    print(f'| {name} | {top[0]:+.3f} | {top[0] - worst:.3f} | {len(members)} | {top[1]} | {100 * top[3] / top[2]:.0f} % |')
for name in ('F1 bridge -> SPI-flash PHY', 'F2 SDRAM arbitration -> crossing FIFO read register',
             'F3 ZQCS timer -> bank machines', 'F4 CPU DMA write bridge (inside the CPU netlist)'):
    members = families.get(name)
    where = (f'worst {members[0][0]:+.3f} ns, {members[0][0] - worst:.3f} ns from the worst path, '
             f'{len(members)} endpoints' if members else 'no endpoint among the listed paths')
    print(f'{name}: {where}')
