"""One native service arm at the lane head, with PR #609's arguments and environment.

It builds and measures `service-1x1-all` (tb/verilator/fw_service_budget/run.py,
populated, plan `all`, service enforced) in a fresh scratch directory, then
regrades it. The CPU set is the whole host and the command runs niced; build
and run logs stay in the scratch directory, and the receipt records rc,
seconds, sizes and SHA-256.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import time

ROOT = Path('$LANES/70-lane2-pin')
OUT = Path(__file__).parent
SCRATCH = Path('$VALIDATION_STORAGE/70-a448/native')
PYTHON = '$WORKSPACE_HOME/litex-milan/venv/bin/python'
COMMON = ['nice', '-n', '5', 'timeout', '28800', 'unshare', '-Urn', 'env',
          'PYTHONHASHSEED=0', 'PYTHONDONTWRITEBYTECODE=1', 'PYTHONUNBUFFERED=1',
          'COURSIER_MODE=offline', 'SBT_OPTS=-Dsbt.offline=true',
          'LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux',
          'PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin',
          PYTHON, '-B']
NAME = 'service-1x1-all'
BUILD = SCRATCH / NAME
ARGS = ['tb/verilator/fw_service_budget/run.py', '--shape', 'endstation_ax7101_1x1_tdm8',
        '--build-dir', str(BUILD), '--populated', '--plan', 'all', '--enforce-service']
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
assert not subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'],
                                   cwd=ROOT, text=True).strip()
records = []
for step, extra in (('build', ['--build-only']), ('run', ['--reuse-build'])):
    log = SCRATCH / f'{NAME}-{step}.log'
    start = time.monotonic()
    with log.open('w') as stream:
        rc = subprocess.run(COMMON + ARGS + extra, cwd=ROOT, stdout=stream,
                            stderr=subprocess.STDOUT).returncode
    raw = log.read_bytes()
    records.append(dict(step=step, head=head, command=COMMON + ARGS + extra, rc=rc,
                        seconds=round(time.monotonic() - start, 1), log=str(log),
                        log_bytes=len(raw), log_sha256=hashlib.sha256(raw).hexdigest()))
    (OUT / 'service-probe.json').write_text(json.dumps(records, indent=2) + '\n')
    print(step, rc, flush=True)
    if rc and step == 'build':
        break
