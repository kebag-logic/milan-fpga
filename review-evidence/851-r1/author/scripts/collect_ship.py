"""collect_ship.py <route-dir> <gateware> <dest>: the receipts of one build-dev.sh shipping route, masked; a file over
200 KB is recorded by SHA-256 and size in <dest>/RAW-RECORDS.txt instead of copied."""
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mask import mask

run, gw, dest = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
dest.mkdir(parents=True, exist_ok=True)
raw = dest / 'RAW-RECORDS.txt'


def put(name, data):
    text = mask(data.decode(errors='replace'))
    b = text.encode()
    if len(b) > 200 * 1024:
        with raw.open('a') as h:
            h.write(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {name} (raw bytes, not copied)\n')
        return
    (dest / name).write_text(text)


for f in ('build.log', 'build.rc', 'queue.log', 'head-' + run.name.split('-')[1] + '.json'):
    p = run / f
    if p.exists():
        put(f, p.read_bytes())
for p in sorted((run / 'out').glob('*.status')):
    put('status-' + p.name, p.read_bytes())
for p in sorted((run / 'out').glob('0[0-5]*.log')):
    put(p.name, p.read_bytes())
for pat in ('*_route_status.rpt', '*_utilization_place.rpt', '*_iob_pack.rpt', '*_signoff_grade.txt'):
    for p in sorted(gw.glob(pat)):
        put(p.name.replace('alinx_ax7101_', ''), p.read_bytes())
for p in sorted(gw.glob('*_signoff_*_timing.rpt')):
    if not re.search(r'_signoff_(Slow|Fast)_[0-9]+C_timing', p.name):
        continue
    lines = p.read_text(errors='replace').splitlines()
    i = next(n for n, l in enumerate(lines) if 'Design Timing Summary' in l)
    corner = re.search(r'_signoff_(.+)_timing', p.name).group(1)
    put(f'timing-summary-{corner}.txt', ('\n'.join(lines[i:i + 8]) + '\n').encode())
t = (gw / 'alinx_ax7101_timing.rpt').read_text(errors='replace').splitlines()
i = next(n for n, l in enumerate(t) if l.startswith('Max Delay Paths'))
put('worst-setup-path.txt', ('\n'.join(t[i:i + 24]) + '\n').encode())
for p in (gw / 'vivado.log', gw / 'alinx_ax7101.v', gw / 'alinx_ax7101_timing.rpt', gw / 'alinx_ax7101.bit'):
    if p.exists():
        data = p.read_bytes()
        with raw.open('a') as h:
            h.write(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {p.name} (not copied)\n')
print('collected', dest)
