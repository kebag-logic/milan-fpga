"""PR #609's five native groups (service 8x8, service 1x1, service mutations,
capture arms, capture controls) at this lane's head.

This is PR #609's `run_native.py` (its merge-dev packet) with these changes and
nothing else: the lane root, the scratch directory (fresh), the expected head
and processor pin, the evidence directory, no `taskset` (the session's own
CPU set, 64-95, is inherited), and a limit of SIMS concurrent simulations
beside the serialized builds, because this session runs under a 12 GiB memory
cap. Arguments, environment and STOP conditions are PR #609's: an 8x8 capture
over 24.5 ms, or an MDIO charge over 50 ms, stops the run. Every raw log,
receipt and spec is retained under `native-<head8>/`, gzip-compressed (and
split) above 200 KB, bound by raw and stored SHA-256.

Usage, from the lane root: python3 run_native.py <expected head>
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import gzip
import hashlib
import json
import subprocess
import sys
import threading
import time

ROOT = Path('$LANES/70-lane2-pin')
OUT = Path(__file__).parent
RTK = '$WORKSPACE_HOME/.local/bin/rtk'
PYTHON = '$WORKSPACE_HOME/litex-milan/venv/bin/python'
EXPECTED_HEAD = sys.argv[1]
PIN = 'b2db3a970cedbbff2f8ba813acb96122c442bc58'
SCRATCH = Path('$VALIDATION_STORAGE/a448-native-' + EXPECTED_HEAD[:8])
EVIDENCE = OUT / ('native-' + EXPECTED_HEAD[:8])
SIMS = 6
COMMON = [RTK, 'proxy', 'timeout', '28800', 'unshare', '-Urn', 'env',
          'PYTHONHASHSEED=0', 'PYTHONDONTWRITEBYTECODE=1', 'PYTHONUNBUFFERED=1',
          'COURSIER_MODE=offline', 'SBT_OPTS=-Dsbt.offline=true',
          'LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux',
          'PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin',
          PYTHON, '-B']


def git(*args, cwd=ROOT):
    return subprocess.check_output([RTK, 'proxy', 'git', *args], cwd=cwd, text=True).strip()


assert Path.cwd() == ROOT
HEAD = git('rev-parse', 'HEAD')
assert HEAD == EXPECTED_HEAD, HEAD
assert not git('status', '--porcelain')
assert Path(git('rev-parse', '--show-toplevel', cwd=ROOT / 'protocol-processor')) == ROOT / 'protocol-processor'
assert git('rev-parse', 'HEAD', cwd=ROOT / 'protocol-processor') == PIN
assert git('ls-tree', 'HEAD', 'protocol-processor').split()[2] == PIN
SCRATCH.mkdir(parents=True, exist_ok=False)
EVIDENCE.mkdir(exist_ok=False)
build_lock = threading.Lock()
sim_slots = threading.Semaphore(SIMS)
record_lock = threading.Lock()
baseline_ready = threading.Event()
records = []
artifacts = []
stop = threading.Event()


def retain(source, name):
    raw = source.read_bytes()
    body = gzip.compress(raw, mtime=0) if len(raw) > 200000 else raw
    name += '.gz' if len(raw) > 200000 else ''
    parts = [body[i:i+190000] for i in range(0, len(body), 190000)] if len(body) > 200000 else [body]
    stored = []
    for index, part in enumerate(parts):
        path = EVIDENCE / (name + (f'.part{index:02d}' if len(parts) > 1 else ''))
        path.write_bytes(part)
        stored.append(dict(path=str(path.relative_to(OUT)), size=len(part), sha256=hashlib.sha256(part).hexdigest()))
    with record_lock:
        artifacts.append(dict(name=name, raw_size=len(raw), raw_sha256=hashlib.sha256(raw).hexdigest(), stored=stored))
        (EVIDENCE/'native-artifacts.json').write_text(json.dumps(artifacts, indent=2)+'\n')


def command(name, args):
    if stop.is_set():
        raise RuntimeError('STOP: another native arm failed')
    log = SCRATCH / (name + '.log')
    argv = COMMON + args
    print('START', name, time.strftime('%H:%M:%S'), flush=True)
    started = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(argv, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, timeout=29000)
    retain(log, name + '.log')
    with record_lock:
        records.append(dict(name=name, head=HEAD, command=argv, rc=result.returncode,
                            seconds=round(time.monotonic()-started, 3)))
        (EVIDENCE/'native-commands.json').write_text(json.dumps(records, indent=2)+'\n')
    print('END', name, result.returncode, time.strftime('%H:%M:%S'), flush=True)
    if result.returncode:
        stop.set()
        raise RuntimeError(name + ' failed: ' + log.read_text()[-5000:])


def simulate(name, args):
    with sim_slots:
        command(name, args)


def capture(name, args, baseline=None):
    directory = Path(args[args.index('--build-dir')+1])
    with build_lock:
        command('build-' + name, args + ['--build-only'])
    native = [str(OUT/'run_capture_native.py'), str(directory)]
    if baseline is not None:
        while not baseline_ready.wait(30):
            if stop.is_set():
                raise RuntimeError('STOP: byte-only baseline failed')
        native.append(str(baseline))
    simulate(name, native)
    path = directory/'measurement.json'
    if path.exists():
        data = json.loads(path.read_text())
        if data['shape'] == 'endstation_ax7101_8x8' and data['maximum_ms'] > 24.5:
            stop.set()
            raise RuntimeError('STOP: 8x8 capture exceeds 24.5 ms')
        retain(path, name+'.json')
    retain(directory/'capture.log', name+'-raw.log')
    retain(directory/'sources.json', name+'-sources.json')
    if name == 'capture-8x8-50-on':
        baseline_ready.set()


def service(name, args):
    directory = Path(args[args.index('--build-dir')+1])
    mutation = args[args.index('--mutation')+1] if '--mutation' in args else 'none'
    with build_lock:
        command('build-' + name, args + ['--build-only'])
    simulate(name, args + ['--reuse-build'])
    receipts = sorted(directory.glob('service-*.json'))
    logs = sorted(directory.glob('service-*.log'))
    assert len(logs) == 1 and len(receipts) == (0 if mutation == 'no-publish' else 1), (logs, receipts)
    for path in receipts:
        data = json.loads(path.read_text())
        if mutation == 'none':
            phy = data['phy']
            charge = (phy['max_poll_sys_cycles']+9*phy['max_transaction_sys_cycles'])/100000
            if charge > 50:
                stop.set()
                raise RuntimeError('STOP: MDIO charge exceeds smallest device wait')
        retain(path, name+'-receipt.json')
    retain(logs[0], name+'-raw.log')
    retain(directory/'service_spec.json', name+'-spec.json')
    if mutation != 'no-publish':
        command('regrade-'+name, args + ['--reuse-build', '--regrade'])


cases = []
for short, shape in [('8x8', 'endstation_ax7101_8x8'), ('1x1', 'endstation_ax7101_1x1_tdm8')]:
    for plan in ('queued-input', 'queued-builtins', 'device-wait', 'uart-paced', 'all', 'queued-short'):
        name = 'service-'+short+'-'+plan
        args = ['tb/verilator/fw_service_budget/run.py', '--shape', shape, '--build-dir', str(SCRATCH/name),
                '--populated', '--plan', plan, '--enforce-service']
        if plan == 'device-wait':
            args += ['--device-wait-us', '3000000', '--program-wait-us', '5000']
        cases.append((service, name, args))
for mutation, plan in [('remove-dispatch', 'queued-builtins'), ('remove-dispatch', 'queued-short'),
                       ('late-sample', 'all'), ('no-publish', 'all')]:
    name = 'service-'+mutation+'-'+plan
    cases.append((service, name, ['tb/verilator/fw_service_budget/run.py', '--shape', 'endstation_ax7101_1x1_tdm8',
                                  '--build-dir', str(SCRATCH/name), '--populated', '--plan', plan,
                                  '--enforce-service', '--mutation', mutation]))
for short, shape, mhz in [('8x8', 'endstation_ax7101_8x8', 100), ('8x8', 'endstation_ax7101_8x8', 50),
                           ('1x1', 'endstation_ax7101_1x1_tdm8', 50)]:
    for traffic in ('on', 'off'):
        name = f'capture-{short}-{mhz}-{traffic}'
        cases.append((capture, name, ['tb/verilator/nvm_capture_cpu/run.py', '--shape', shape,
                                      '--cpu-hz', str(mhz*1000000), '--captures', '16', '--traffic', traffic,
                                      '--build-dir', str(SCRATCH/name)]))
for mutation in ('byte-only', 'skip-copy', 'no-traffic'):
    name = 'capture-'+mutation
    args = ['tb/verilator/nvm_capture_cpu/run.py', '--shape',
            'endstation_ax7101_8x8' if mutation == 'byte-only' else 'endstation_ax7101_1x1_tdm8',
            '--captures', '2', '--mutation', mutation, '--build-dir', str(SCRATCH/name)]
    baseline = None
    if mutation == 'byte-only':
        baseline = SCRATCH/'capture-8x8-50-on/measurement.json'
        args += ['--baseline-measurement', str(baseline)]
    cases.append((capture, name, args) if baseline is None else
                 (lambda n, a, b=baseline: capture(n, a, b), name, args))
failures = []
with ThreadPoolExecutor(max_workers=len(cases)) as pool:
    futures = {pool.submit(function, name, args): name for function, name, args in cases}
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as exc:  # report every arm, then fail
            failures.append(futures[future])
            print('FAILED', futures[future], str(exc)[-2000:], flush=True)
assert git('rev-parse', 'HEAD') == HEAD and not git('status', '--porcelain')
if failures:
    raise SystemExit('NATIVE FAILURES: ' + ', '.join(sorted(failures)))
print(f'ALL NATIVE MEASUREMENTS COMPLETE: {len(cases)} arms at {HEAD}', flush=True)
