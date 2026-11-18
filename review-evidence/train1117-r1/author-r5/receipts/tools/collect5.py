#!/usr/bin/env python3
"""collect5.py OUT: round 5's receipts into OUT/receipts, each file at most 200 KB; a larger one becomes
<name>.stub.txt with its size, sha256 and last 60 lines. Run sanitize.py and index.py on OUT afterwards."""
import hashlib
import shutil
import sys
from pathlib import Path

S = Path('<scratch>')
out = Path(sys.argv[1]) / 'receipts'
LIMIT = 200 * 1024
M = S / 'r4meas'
SOURCES = [
    # step 10 on the frozen head: the merge's resolutions
    ('step10/conflicts', S / 's10f', '*.res.py'),
    # the hot list: the three-window traces' summaries, the filter and its inputs, each relearn
    ('hot/tools', S / 'r5hot', '*.py'), ('hot/tools', S / 'r5hot', '*.sh'),
    *[(f'hot/{h}', S / f'r5hot/{h}', p) for h in ('082d0037', '26f30fea', '08c28218')
      for p in ('order.txt', 'order-filtered.txt', 'filter.txt', 'dropped.txt', 'order.summary', 'trace-build.log',
                '*.pcs')],
    ('hot/logs', S / 'logs', 'r5-relearn*.log*'), ('hot/logs', S / 'logs', 'r5-maps*.log*'),
    # attempt 2's cuts, their tools and the traces
    ('cuts/tools', S / 'cut2', '*.py'), ('cuts/tools', S / 'cut2', '*.sh'),
    ('cuts/trace', S / 'cut', '*.perfunc.txt'), ('cuts/trace', S / 'cut', 'b81-base.pcs'),
    ('cuts/trace', S / 'cut', 'tip-81-srp.pcs'), ('cuts/trace', S / 'cut', '*.sh'), ('cuts/trace', S / 'cut', '*.py'),
    # the re-grade before measuring and the what-ifs on B's figures
    ('regrade', S / 'r5re', '*'), ('regrade', S / 'r5out', '*'),
    # gates
    ('gates/p10-082d0037', S / 'logs', 'r5-p10-*.log*'), ('gates/p10-082d0037/q', S / 'q/r5-p10', '*'),
    ('gates/step9-0bc158a7', S / 'logs', 'r5-s9c-*.log*'), ('gates/step9-0bc158a7/q', S / 'q/r5-s9c', '*'),
    ('gates/step9-7b3c1c94', S / 'logs', 'r5-s9d-*.log*'),
    ('gates/step9-112ab9b1', S / 'logs', 'r5-s9e-*.log*'), ('gates/step9-112ab9b1', S / 'logs', 'r5-cov*.log*'),
    ('gates/p10-bf2c1184', S / 'logs', 'r5-tip-*.log*'), ('gates/p10-bf2c1184/q', S / 'q/r5-tip', '*'),
    ('gates/p10-0cfe1ddc', S / 'logs', 'r5-tip2-*.log*'), ('gates/p10-0cfe1ddc/q', S / 'q/r5-tip2', '*'),
    ('cuts/trace/logs', S / 'logs', 'r5-trace-*.log*'),
    ('gates/p10-tip/q-ledger-edit', S / 'q/r5-led', '*'),
    # the ROM ledger
    ('ledger/B-41d2bc2b-before-restatement', S / 'r5bled', 'plat-ledger.log'),
    ('ledger/B-41d2bc2b-before-restatement', S / 'r5bled', 'ctrl_memory.log'),
    ('ledger/B-41d2bc2b-before-restatement', S / 'r5bled', 'fixture-summary.txt'),
    ('ledger/tip-bf2c1184', S / 'r5tipled', 'plat-ledger.log'), ('ledger/tip-bf2c1184', S / 'r5tipled', 'ctrl_memory.log'),
    ('ledger/logs', S / 'logs', 'r5-b-ledger.log*'), ('ledger/logs', S / 'logs', 'r5-tip-ledger.log*'),
    # the measurement: each head's leg logs and the survey
    *[(f'measure/{r}/legs-{p}', M / f'{r}/{p}', g) for r in ('41d2bc2b', '68c97849', 'b5802de9', 'oldlist', 'nofilter',
                                                            'unit375', 'nu375')
      for p in ('1x1', '8x8-1if', '8x8') for g in ('*.log', '*.rc')],
    *[(f'measure/{r}/legs-{p}/{k}', M / f'{r}/{p}/{k}', 'parts.json') for r in ('41d2bc2b', 'unit375')
      for p in ('1x1', '8x8-1if', '8x8') for k in ('none', 'aep', 'ap', 'vd')],
    ('measure/41d2bc2b', M / 'out/41d2bc2b', '*'),
    *[(f'measure/41d2bc2b/survey-{p}', M / f'out/41d2bc2b/survey-{p}', g) for p in ('1x1', '8x8-1if', '8x8')
      for g in ('*.txt', '*.json', '*.out')],
    *[(f'measure/{r}', M / f'out/{r}', '*') for r in ('unit375', 'nu375', 'nofilter')],
    *[(f'measure/{r}/survey-{p}', M / f'out/{r}/survey-{p}', g) for r in ('unit375', 'nu375', 'nofilter')
      for p in ('1x1', '8x8-1if') for g in ('*.txt', '*.json', '*.out')],
    ('gates/candidate-0b054867', S / 'logs', 'r5-cand-*.log*'), ('gates/candidate-0b054867/q', S / 'q/r5-cand', '*'),
    ('gates/candidate-0b054867/q-prose', S / 'q/r5-prose', '*'),
    ('images', S / 'r5img/3cdc613b', 'hashes.txt'),
    ('fit/tools', S / 'r5fit/tools', '*'), ('fit', S / 'r5fit', '*.log'), ('fit', S / 'r5fit', '*.rc'),
    *[(f'fit/{w}', S / f'r5fit/{w}', g) for w in ('route', 'route8') for g in ('slot-*.log', 'FIT_DONE', '*.sha256')],
    *[(f'fit/{w}/{d}', S / f'r5fit/{w}/{d}', g) for w in ('route', 'route8')
      for d in ('split/gateware', 'split-ExtraTimingOpt', 'split-AltSpreadLogic_high')
      for g in ('route.rc', 'route.start', 'route.end', '*signoff*_timing.rpt', '*utilization_place.rpt')],
    *[(f'measure/unit380/legs-8x8-1if', M / 'unit380/8x8-1if', g) for g in ('*.log', '*.rc')],
    ('measure/unit380', M / 'out/unit380', '*'),
    ('measure/unit380/survey-8x8-1if', M / 'out/unit380/survey-8x8-1if', '*.txt'),
    ('fit-B-bf2c1184', S / 'r5fitB', '*.log'),
    *[(f'fit-B-bf2c1184/route8/{d}', S / f'r5fitB/route8/{d}', g)
      for d in ('split/gateware', 'split-ExtraTimingOpt', 'split-AltSpreadLogic_high')
      for g in ('route.rc', 'route.start', 'route.end', '*signoff*_timing.rpt', '*utilization_place.rpt')],
    # step 11 (RULING-1118c)
    ('step11/gates', S / 'logs', 'r5-p11-*.log*'), ('step11/gates/q-candidate-4374cc27', S / 'q/r5-4374cc27', '*'),
    ('step11/gates/q-c8ff391a', S / 'q/r5-c8ff391a', '*'), ('step11/images', S / 'r5img/3e908539', 'hashes.txt'),
    ('step11/confirmation', S / 'r5conf', '*.log'),
    *[(f'step11/confirmation/{d}', S / f'r5conf/{d}', g) for d in ('8x8-1if-vd', '8x8-1if-ap', '1x1-ap', '8x8-ap')
      for g in ('*.txt', '*.json', '*.log', 'table.md')],
    ('step11/fit/tools', S / 'r5fitP11/tools', '*'), ('step11/fit', S / 'r5fitP11', '*.log'),
    *[(f'step11/fit/{w}/{d}', S / f'r5fitP11/{w}/{d}', g) for w in ('route', 'route8')
      for d in ('split/gateware', 'split-ExtraTimingOpt', 'split-AltSpreadLogic_high')
      for g in ('route.rc', 'route.start', 'route.end', '*utilization_place.rpt', '*utilization_hierarchical_synth.rpt')],
    ('step11/release', S / 'r5rel', '*.sh'), ('step11/release', S / 'r5rel', '*.log'),
    ('step11/release', S / 'r5rel/work', '*.log'), ('step11/release', S / 'r5rel/work', '*.json'),
    ('step11/release/candidate-synth', S / 'r5relC', '*.sh'), ('step11/release/candidate-synth', S / 'r5relC', '*.log'),
    ('step11/fifo', S / 'r5fifo', '*.sh'), ('step11/fifo', S / 'r5fifo', '*.ys'), ('step11/fifo', S / 'r5fifo', '*.out'),
    ('step11/fifo', S / 'r5fifo', 'bmc-*.log'), ('step11/fifo', S / 'r5fifo', 'syn-*.log'),
    ('step11/fifo/ooc', S / 'r5fifo/ooc', '*.tcl'), ('step11/fifo/ooc', S / 'r5fifo/ooc', '*.rpt'),
    ('step11/fifo/ooc', S / 'r5fifo/ooc', '*.sh'),
    *[(f'step11/release/{d}', S / f'r5rel/work/{d}', g) for d in ('ax7101/gateware', 'ax7101-AltSpreadLogic_high', 'ax7101-ExtraTimingOpt')
      for g in ('route.rc', '*utilization_place.rpt', '*utilization_hierarchical_synth.rpt')],
    ('step11/release/candidate-synth', S / 'r5relC/work/ax7101/gateware', '*utilization_hierarchical_synth.rpt'),
    ('step11/release/candidate-route', S / 'r5relC', 'routeC.*'),
    ('step11/release/candidate-route', S / 'r5relC/work/ax7101-ExtraPostPlacementOpt', '*utilization_place.rpt'),
    # RULING-1118d: the preflight fix's checks and images, and the release image's delta by hierarchy
    ('step11/gates/q-05dc1791', S / 'q/r5-05dc1791', '*'), ('step11/images', S / 'r5img/05dc1791', 'hashes-05dc1791.txt'),
    ('step11/images', S / 'logs', 'r5-img05dc.log*'),
    ('step11/release', S / 'r5hier', 'hier-diff.txt'), ('step11/release', S / 'r5hier', 'record-dryrun.txt'),
    *[('step11/release/hier', S / 'r5hier', g) for g in ('*.tcl', '*.sh', '*.py', '*.rpt', 'prims-*.txt', 'lutram-*.txt',
                                                        'ffs-*.txt', '*slot.log', '*slot.log.rc', '*.log')],
    # RULING-1118e item 3: u_fcdc's storage-to-read-register crossing in the existing routed checkpoints
    ('step11/cdc', S / 'r5cdc', 'fcdc-*.txt'),
    *[('step11/cdc/reports', S / 'r5cdc', g) for g in ('cdc-summary-*.rpt', 'cdc-clocks-*.rpt', 'cdc-full-*.rpt',
                                                      'methodology-full-*.rpt', 'cdc*.log', 'slot-*.log', 'slot-*.log.rc')],
    *[('step11/cdc/tools', S / 'r5cdc', g) for g in ('cdc.tcl', 'cdc.sh', 'cdc_summary.py')],
    ('step11/cdc/first-attempt', S / 'r5cdc/try1', '*'),
    # RULING-1118f: the record-only re-baseline at 73272666 and its checks
    *[('step11/release', S / 'r5hier', g) for g in ('record-write.txt', 'gate-after.txt', 'check-baseline.txt',
                                                   'gate-selftest.txt', 'pp_*_selftest.txt')],
    ('step11/gates/q-73272666', S / 'q/r5-73272666', '*'), ('step11/images', S / 'r5img/73272666', 'hashes-73272666.txt'),
    ('step11/images', S / 'logs', 'r5-img7327.log*'),
    # tools
    ('tools', S / 'tools', 'collect5.py'), ('tools', S / 'tools', 'legs.py'), ('tools', S / 'bin', '*.sh'),
    ('tools', S / 'bin', '*.py'), ('tools', S / 'r4meas', '*.sh'), ('tools', S / 'r4meas', '*.py'),
    ('tools/survey', S / 'tools/survey', '*'), ('tools/checks', S / 'checks', 'r5-*.tsv'),
]


def put(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    if len(data) <= LIMIT:
        shutil.copyfile(src, dst)
        return
    tail = data.decode(errors='replace').splitlines()[-60:]
    dst.with_name(dst.name + '.stub.txt').write_text(
        f'{src.name}: {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}; over 200 KB, kept in scratch. '
        f'Its last {len(tail)} lines:\n' + '\n'.join(tail) + '\n')


n = 0
for where, root, pattern in SOURCES:
    if not root.is_dir():
        continue
    for f in sorted(root.glob(pattern)):
        if f.is_file() and not f.is_symlink():
            if f.name == 'sanitize.py':
                # its table names the host paths it replaces, so it is recorded, not copied
                data = f.read_bytes()
                (out / where).mkdir(parents=True, exist_ok=True)
                (out / where / 'sanitize.py.stub.txt').write_text(
                    f'sanitize.py: {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}; it replaces host '
                    'paths and account names in every text receipt and refuses if any survives, so its own table '
                    'stays in scratch.\n')
            else:
                put(f, out / where / f.name)
            n += 1
print(f'{n} files collected into {out}')
