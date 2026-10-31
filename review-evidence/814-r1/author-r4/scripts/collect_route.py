"""collect_route.py <run-dir> <dest-dir> <prefix>: the receipts of one routed Vivado run, host paths redacted, each
named <prefix>-<report>. Copies the route status, placed utilization (flat and hierarchical), IOB packing, DRC, the
timing summary's design table, each signoff corner's design table, the top-20 sys path report and the path table's
summary; a report over 200 KB is recorded by SHA-256 and size in <dest>/large.sha256 instead."""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

run, dest, prefix = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
dest.mkdir(parents=True, exist_ok=True)
REDACT = (('$VALIDATION_STORAGE/scratch/814-a703d', '<scratch>'), ('$VALIDATION_STORAGE/scratch', '<scratch-root>'),
          ('$VALIDATION_TOOLS', '<tools>'), ('$LANES', '<lanes>'), ('$WORKSPACE_HOME', '<home>'))


def put(name, text):
    """Write one receipt, redacted; record a large one by digest."""
    for a, b in REDACT:
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


for pattern, name in (('*_route_status.rpt', 'route_status.rpt'), ('*_utilization_place.rpt', 'utilization_place.rpt'),
                      ('*_utilization_hierarchical_place.rpt', 'utilization_hierarchical_place.rpt'),
                      ('*_iob_pack.rpt', 'iob_pack.rpt'), ('*_drc.rpt', 'drc.rpt'), ('sys_top20.rpt', 'sys_top20.rpt'),
                      ('*_signoff_grade.txt', 'signoff_grade.txt')):
    found = sorted(run.glob(pattern))
    if found:
        put(name, found[0].read_text(errors='replace'))
summary = []
for path in sorted(run.glob('*_timing.rpt')):
    if path.name.endswith(('_synth.rpt',)):
        continue
    summary.append(f'== {path.name}\n{design_table(path.read_text(errors="replace"))}')
put('timing-design-tables.txt', '\n'.join(summary))
for extra in ('stage_cells.tsv', 'all_top30.rpt'):
    if (run / extra).exists():
        put(extra, (run / extra).read_text(errors='replace'))
allp = run / 'all_paths.tsv'
if allp.exists():
    out = subprocess.run([sys.executable, '-B', str(Path(__file__).with_name('summarize_all.py')), prefix, str(allp)],
                         capture_output=True, text=True, check=True).stdout
    put('all-top30.md', out)
    data = allp.read_bytes()
    with open(dest / 'large.sha256', 'a') as h:
        h.write(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {prefix}-all_paths.tsv (worst path per endpoint, every group)\n')
paths = run / 'sys_paths.tsv'
if paths.exists():
    out = subprocess.run([sys.executable, '-B', str(Path(__file__).with_name('summarize_paths.py')), prefix, str(paths)],
                         capture_output=True, text=True, check=True).stdout
    put('top20.md', out)
    data = paths.read_bytes()
    with open(dest / 'large.sha256', 'a') as h:
        h.write(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {prefix}-sys_paths.tsv (worst path per sys endpoint)\n')
print(f'collected {prefix} from {run.name}')
