import json
import os
from pathlib import Path
import shutil
import subprocess
import time

work = Path(__file__).parent
repo = Path(os.environ['REPO'])
env = os.environ.copy()
env.update(STAGE_ROOT=str(work), PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0',
           MAKEFLAGS='-j16', TMPDIR=str(work / 'tmp'))
evidence = Path(os.environ['EVIDENCE'])
vendor = os.environ['VIVADO_EXE']


def run(name, argv, cwd=repo, override=None):
    print('START', name, flush=True)
    options = env.copy()
    if override:
        options.update(override)
    with (work / (name + '.log')).open('w') as log:
        rc = subprocess.run(argv, cwd=cwd, env=options, stdout=log,
                            stderr=subprocess.STDOUT).returncode
    (work / (name + '.rc')).write_text(str(rc) + '\n')
    print('DONE', name, rc, flush=True)
    return rc


def require(name, argv, cwd=repo, override=None):
    rc = run(name, argv, cwd, override)
    if rc:
        raise SystemExit(rc)


def await_gate(name):
    path = work / (name + '.rc')
    while not path.exists():
        time.sleep(5)
    rc = int(path.read_text())
    if rc:
        raise RuntimeError(f'{name} failed with {rc}; measurement not started')


try:
    if os.environ.get('RESUME_PREPARED') == '1':
        print('Resume prepared export after documentation-only dev merge', flush=True)
        require('source-inputs-resume', ['python3', '-B', str(work / 'source_inventory.py'), '--verify'])
        (work / 'source-inputs-after.json').rename(work / 'source-inputs-resume.json')
    else:
        await_gate('builder')
        while (repo / 'sw/builder/out').is_symlink():
            time.sleep(1)
        require('export', ['python3', '-B', str(work / 'prepare.py')])
        require('source-inputs-before', ['python3', '-B', str(work / 'source_inventory.py')])
    print('Waiting for all other heavy builds to finish', flush=True)
    for name in ['physical-build', 'datapath', 'render', 'media-clock', 'pp-shadow',
                 'portability', 'render-pullin', 'render-boundary-builds',
                 'source-selftest', 'wire-truth-selftest', 'capture-coherence', 'source/all']:
        await_gate(name)
    require('routes', ['python3', '-B', str(work / 'run_routes.py')])
    for directive in ['ExtraPostPlacementOpt', 'AltSpreadLogic_high', 'ExtraTimingOpt']:
        rc = run('grade-' + directive,
                 [os.environ['LITEX_PYTHON'], '-B', str(work / 'collect_timing.py'),
                  '--work', str(work), '--evidence', str(evidence), '--directive', directive])
        if rc not in (0, 1) or not (evidence / 'timing-current' / directive / 'timing-summary.json').exists():
            raise RuntimeError('Timing collection failed: ' + directive)
    require('vendor-parser', ['flock', '$VIVADO_LOCK', 'python3', '-B',
                             'scripts/xvlog_gate.py', '--check'])
    area = work / 'area-ooc'
    for tag in ['settle_base', 'settle_head', 'cmc_base', 'cmc_head']:
        require('ooc-' + tag, ['flock', '$VIVADO_LOCK', vendor, '-mode', 'batch',
                              '-source', 'ooc.tcl', '-nojournal', '-log', tag + '.vendor.log'],
                area, {'ONLY': tag})
    area = work / 'area-route'
    gate = work / 'route/ax7101/gateware'
    base = work.parent / 'route/ax7101/gateware'
    for name in ['baseline_hierarchy.rpt', 'baseline_cells.tsv']:
        shutil.copy2(gate / name, area / name)
    for label, script in [('area-ownership', 'ownership.tcl'), ('area-shared', 'shared-logic.tcl')]:
        require(label, ['flock', '$VIVADO_LOCK', vendor, '-mode', 'batch',
                        '-source', str(area / script), '-nojournal', '-log', label + '.vendor.log',
                        '-tclargs', str(gate / 'alinx_ax7101_route.dcp'),
                        str(base / 'alinx_ax7101_route.dcp')], area)
    require('area-proof', ['python3', '-B', str(area / 'prove_shared.py'), str(area), str(area)], area)
    require('area-compare', ['python3', '-B', str(area / 'compare.py'), str(repo), str(base), str(area)], area)
    ownership = json.loads((area / 'candidate_area_comparison.json').read_text())['ownership']
    lut, ff = ownership['final_own_LUT_upper_bound'], ownership['own_FF_delta']
    rc = int(lut > 120 or ff > 120)
    (work / 'area-limit.rc').write_text(str(rc) + '\n')
    (work / 'area-limit.log').write_text(f'Conservative own routed logic: {lut} LUT / {ff} FF; limit 120/120; rc={rc}\n')
    if rc:
        raise RuntimeError('Own routed area exceeds limit')
    require('source-inputs-after', ['python3', '-B', str(work / 'source_inventory.py'), '--verify'])
except BaseException as error:
    print(type(error).__name__, str(error), flush=True)
    (work / 'all-measurements.rc').write_text('1\n')
    raise
(work / 'all-measurements.rc').write_text('0\n')
print('ALL MEASUREMENTS DONE', flush=True)
