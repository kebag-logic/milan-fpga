"""collect_route.py <run-dir> <dest-dir> <prefix>: the gate-relevant receipts of one Vivado measurement directory, host
paths masked, each named <prefix>-<report>. A file over 200 KB is recorded by SHA-256 and size in <dest>/large.sha256."""
import glob
import hashlib
import sys
from pathlib import Path

run, dest, prefix = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
dest.mkdir(parents=True, exist_ok=True)
MASK = (('$VALIDATION_STORAGE/scratch/843-a737b', '<scratch>'), ('$VALIDATION_STORAGE/scratch', '<scratch-root>'),
        ('$VALIDATION_TOOLS', '<tools>'), ('$LANES', '<lanes>'), ('$HOME', '<home>'),
        ('/tmp/milan-vivado', '<vivado-lock>'))


def put(name, text):
    """Write one receipt, masked; record a large one by digest."""
    for a, b in MASK:
        text = text.replace(a, b)
    data = text.encode()
    if len(data) > 200 * 1024:
        with open(dest / 'large.sha256', 'a') as h:
            h.write(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {prefix}-{name}\n')
        return
    (dest / f'{prefix}-{name}').write_text(text)


def design_table(text):
    """The Design Timing Summary's header, rule and figures."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if 'WNS(ns)' in line and 'TNS(ns)' in line:
            return '\n'.join(lines[i:i + 3]) + '\n'
    return 'no design timing summary found\n'


for pattern in ('*_route_status.rpt', '*_utilization_place.rpt', '*_iob_pack.rpt', '*_drc.rpt', 'baseline_utilization.rpt',
                'baseline_hierarchy.rpt', 'baseline_images.json', 'baseline_parameters.json', 'baseline_chparam.txt',
                'baseline.log.rc'):
    for found in sorted(run.glob(pattern)):
        put(found.name.replace('alinx_ax7101_', ''), found.read_text(errors='replace'))
summary = []
for path in sorted(run.glob('*_timing*.rpt')):
    summary.append(f'== {path.name}\n{design_table(path.read_text(errors="replace"))}')
put('timing-design-tables.txt', '\n'.join(summary))
log = run / 'baseline.log'
if log.exists():
    text = log.read_text(errors='replace')
    put('baseline.log.tail', ''.join(text.splitlines(True)[-40:]))
    data = text.encode()
    with open(dest / 'large.sha256', 'a') as h:
        h.write(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {prefix}-baseline.log\n')
print(f'collected {prefix} from {run.name}')
