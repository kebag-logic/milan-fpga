"""Run the capture receipt's recipe (six arms, three controls) from one checkout.

Usage: python3 capture_campaign.py SIDE CHECKOUT
SIDE names the output directory under $SCRATCH/capture. The
recipe, environment, launcher and arguments are identical for every side; only
the checkout and the build directory differ (the #621 ruling's comparison model).
Every run records its own exit status; a non-zero exit does not stop the others.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import shlex
import subprocess
import sys

side, clone = sys.argv[1], Path(sys.argv[2]).resolve()
root = Path('$SCRATCH')
scratch = root / 'capture' / side
scratch.mkdir(parents=True, exist_ok=True)
python = '$LITEX_ENV/venv/bin/python3'
env = dict(os.environ,
           PATH=':'.join([str(root / 'bin5052'), '$LITEX_ENV/venv/bin', os.environ['PATH'],
                          '$SDK/bin']),
           PRODUCT_PYTHON=python, PYTHON=python, SCRATCH=str(scratch), TMPDIR=str(root / 'tmp'),
           PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0', LITEX_ENV_CC_TRIPLE='riscv32-linux',
           COURSIER_MODE='offline', SBT_OPTS='-Dsbt.offline=true', VERILATOR_JOBS='2', MAKEFLAGS='-j4')
SMALL, LARGE = 'endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8'


def arm(label, shape, cpu, traffic):
    return (label, ['--shape', shape, '--cpu-hz', str(cpu), '--captures', '16', '--traffic', traffic,
                    '--build-dir', str(scratch / ('capture-' + label))])


def control(label, shape, mutation, *extra):
    return (label, ['--shape', shape, '--captures', '2', '--mutation', mutation,
                    '--build-dir', str(scratch / ('capture-' + label)), *extra])


WORKERS = [
    [arm('8x8-50-on', LARGE, 50000000, 'on'),
     control('byte-only', LARGE, 'byte-only', '--baseline-measurement',
             str(scratch / 'capture-8x8-50-on/measurement.json'))],
    [arm('8x8-50-off', LARGE, 50000000, 'off'), control('skip-copy', SMALL, 'skip-copy'),
     control('no-traffic', SMALL, 'no-traffic')],
    [arm('8x8-100-on', LARGE, 100000000, 'on'), arm('1x1-50-on', SMALL, 50000000, 'on')],
    [arm('8x8-100-off', LARGE, 100000000, 'off'), arm('1x1-50-off', SMALL, 50000000, 'off')],
]


def worker(jobs):
    rcs = []
    for label, args in jobs:
        argv = ['unshare', '-Urn', python, '-B', 'tb/verilator/nvm_capture_cpu/run.py', *args]
        with (scratch / (label + '.log')).open('w') as log:
            log.write('CWD ' + str(clone) + '\n' + shlex.join(argv) + '\n')
            log.flush()
            rc = subprocess.run(argv, cwd=clone, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
        (scratch / (label + '.rc')).write_text(str(rc) + '\n')
        print(label + ': rc ' + str(rc), flush=True)
        rcs.append(rc)
    return rcs


with ThreadPoolExecutor(max_workers=4) as pool:
    results = [rc for rcs in pool.map(worker, WORKERS) for rc in rcs]
(scratch / 'campaign.rc').write_text(' '.join(map(str, results)) + '\n')
print('campaign rcs:', results, flush=True)
