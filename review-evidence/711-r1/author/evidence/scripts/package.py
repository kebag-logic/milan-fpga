"""Copy small evidence files into the output directory with host prefixes replaced; list large ones by size and SHA-256.

Usage: python3 package.py OUTPUT_DIR
"""
import hashlib
import sys
from pathlib import Path

S = Path('$SCRATCH')
OUT = Path(sys.argv[1])
SUBS = ((str(S), '$SCRATCH'), ('$LITEX_ENV', '$LITEX_ENV'), ('$XILINX', '$XILINX'),
        ('$HOME', '$HOME'), ('$TOOLS', '$TOOLS'), ('$SDK', '$SDK'),
        ('$LANE', '$LANE'), ('$TMPROOT', '$TMPROOT'))
COPY = {
    'evidence/scripts': sorted((S / 'scripts').glob('*')),
    'evidence/firmware': [S / f'fw/{s}/summary.txt' for s in ('cand', 'base')],
    'evidence/docs': [S / f'docs/{s}/summary.tsv' for s in ('cand', 'base')],
    'evidence/static': [S / 'static/summary.tsv', S / 'static/02.log'],
    'evidence/decoded': [S / 'dump/compare.md', S / 'dump/compare.json', S / 'dump/control-drop-one-event.txt',
                         S / 'dump/control-swap-event.txt'],
    'evidence/walker': [S / f'quick/walk-{n}.log' for n in ('e1', 'e2', 'e3', 'e4')] + [S / 'quick/walk-summary.txt'],
    'evidence/capture': [S / 'capture/compare.json', S / 'capture/base/campaign.rc', S / 'capture/cand/campaign.rc']
                        + [S / f'capture/{s}/capture-{a}/capture.log' for s in ('base', 'cand')
                           for a in ('1x1-50-on', '1x1-50-off', '8x8-50-on', '8x8-50-off', '8x8-100-on', '8x8-100-off',
                                     'skip-copy', 'no-traffic', 'byte-only')],
    'evidence/export': [S / f'res/compare-{p}.json' for p in ('base-cand', 'base-bas2', 'bas2-cand')],
    'evidence/yosys': [S / 'yosys/summary.txt'],
    'evidence/sweep': [S / 'sweep/summary.txt', S / 'sweep/run.log'],
    'evidence/vendor': sorted((S / 'vendor').glob('*.rc')) + sorted((S / 'vendor').glob('check-*.log'))
                       + sorted((S / 'vendor').glob('record-*.log')) + [S / 'vendor/driver.log']
                       + sorted((S / 'vendor').glob('*-images.log')) + sorted((S / 'vendor').glob('xvlog-*.log'))
                       + sorted((S / 'vendor').glob('compare-routes*.txt')),
    'evidence/firmware-size': sorted((S / 'srpimage').glob('*.log')),
    'evidence/route': [S / f'res/{s}/ax7101/gateware/{r}' for s in ('base', 'cand')
                       for r in ('baseline_utilization.rpt', 'baseline_timing.rpt', 'baseline_pp_utilization.rpt',
                                 'baseline_pp_boundary_timing.rpt', 'baseline_scope_timing.tsv', 'baseline_cells.tsv',
                                 'baseline_images.json', 'alinx_ax7101_route_status.rpt')],
}
LARGE = [S / 'fw/cand/ctrl-firmware.log', S / 'fw/base/ctrl-firmware.log', S / 'fw/cand/coverage-check.log',
         S / 'fw/base/coverage-check.log', S / 'dump/base/arms.log', S / 'dump/cand/arms.log', S / 'yosys/run.log',
         S / 'memwatch.log'] + sorted((S / 'capture').glob('*/*.log')) + sorted((S / 'dump').glob('*/frames/*.txt')) \
        + [S / f'res/{s}/{sh}/gateware/alinx_ax7101_rom.init' for s in ('base', 'cand') for sh in ('ax7101', 'ax8x8')]
LARGE += [S / f'res/{s}/ax7101/gateware/{n}' for s in ('base', 'cand') for n in ('baseline.log', 'baseline_hierarchy.rpt')]
rows = []
for folder, files in COPY.items():
    for f in files:
        if not f.is_file():
            continue
        data = f.read_bytes()
        target = OUT / folder / (f.parent.name + '--' + f.name if folder in ('evidence/capture', 'evidence/firmware', 'evidence/docs') else f.name)
        if folder == 'evidence/route':
            target = OUT / folder / (f.parts[-4] + '--' + f.name)
        if len(data) > 200_000:
            LARGE.append(f)
            continue
        try:
            text = data.decode()
            for old, new in SUBS:
                text = text.replace(old, new)
            data = text.encode()
        except UnicodeDecodeError:
            pass
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
for f in LARGE:
    if f.is_file():
        data = f.read_bytes()
        name = str(f)
        for old, new in SUBS:
            name = name.replace(old, new)
        rows.append(f'{len(data)}\t{hashlib.sha256(data).hexdigest()}\t{name}')
(OUT / 'ARTIFACTS.tsv').write_text('bytes\tsha256\tscratch path\n' + '\n'.join(rows) + '\n')
big = [p for p in OUT.rglob('*') if p.is_file() and p.stat().st_size > 200_000]
print('copied', sum(1 for p in OUT.rglob('*') if p.is_file()), 'files; over 200 KB:', big)
