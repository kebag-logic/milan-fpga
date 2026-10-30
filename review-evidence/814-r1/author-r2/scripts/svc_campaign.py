"""#814 round 2: the service-budget harness's product-CPU runs (tb/verilator/fw_service_budget/README.md), plan
`all` with `--populated --enforce-service`, both shapes, from one checkout: the real firmware's commits, wipe and
AEM reads through the shipping flash controller (and, at the head, its PHY stage), with the capture's environment.
Usage: python3 svc_campaign.py SIDE CHECKOUT
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import shlex
import subprocess
import sys

side, clone = sys.argv[1], Path(sys.argv[2]).resolve()
root = Path('$VALIDATION_STORAGE/scratch/814-a703b')
scratch = root / 'service' / side
scratch.mkdir(parents=True, exist_ok=True)
python = '$WORKSPACE_HOME/litex-milan/venv/bin/python3'
sdk = '$VALIDATION_STORAGE/scratch/803-a693/sdk/br-milan-rv32/host'
env = dict(os.environ,
           PATH=':'.join([str(root / 'bin5052'), '$WORKSPACE_HOME/litex-milan/venv/bin', os.environ['PATH'], sdk + '/bin']),
           PRODUCT_PYTHON=python, PYTHON=python, TMPDIR=str(root / 'tmp'),
           PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0', LITEX_ENV_CC_TRIPLE='riscv32-linux',
           COURSIER_MODE='offline', SBT_OPTS='-Dsbt.offline=true', VERILATOR_JOBS='2', MAKEFLAGS='-j4')


def worker(shape):
    label = shape.split('_')[2]
    build = scratch / ('service-' + label)
    steps = [('build', ['--shape', shape, '--build-dir', str(build), '--build-only']),
             ('all', ['--shape', shape, '--build-dir', str(build), '--reuse-build', '--populated', '--enforce-service'])]
    rcs = []
    for step, args in steps:
        argv = ['unshare', '-Urn', python, '-B', 'tb/verilator/fw_service_budget/run.py', *args]
        name = f'{label}-{step}'
        with (scratch / (name + '.log')).open('w') as log:
            log.write('CWD ' + str(clone) + '\n' + shlex.join(argv) + '\n')
            log.flush()
            rc = subprocess.run(argv, cwd=clone, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
        (scratch / (name + '.rc')).write_text(str(rc) + '\n')
        print(name + ': rc ' + str(rc), flush=True)
        rcs.append(rc)
        if rc:
            break
    return rcs


with ThreadPoolExecutor(max_workers=2) as pool:
    results = [rc for rcs in pool.map(worker, ['endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8']) for rc in rcs]
(scratch / 'campaign.rc').write_text(' '.join(map(str, results)) + '\n')
print('service rcs:', results, flush=True)
