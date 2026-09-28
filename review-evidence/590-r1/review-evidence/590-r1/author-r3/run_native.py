"""Serialize builds and await foreground native measurements with bound evidence."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import gzip
import hashlib
import json
import subprocess
import threading
import time

ROOT = Path('$LANES/590-592-599-firmware')
OUT = Path(__file__).parent
SCRATCH = Path('$VALIDATION_STORAGE/590-a411')
EVIDENCE = OUT / 'native-evidence'
PYTHON = '$WORKSPACE_HOME/litex-milan/venv/bin/python'
COMMON = ['rtk', 'proxy', 'timeout', '28800', 'unshare', '-Urn', 'env',
          'PYTHONHASHSEED=0', 'PYTHONDONTWRITEBYTECODE=1', 'PYTHONUNBUFFERED=1',
          'COURSIER_MODE=offline', 'SBT_OPTS=-Dsbt.offline=true',
          'LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux',
          'PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin',
          PYTHON, '-B']
HEAD = subprocess.check_output(['rtk', 'proxy', 'git', 'rev-parse', 'HEAD'], text=True).strip()
build_lock = threading.Lock()
record_lock = threading.Lock()
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
        (OUT/'native-artifacts.json').write_text(json.dumps(artifacts, indent=2)+'\n')


def command(name, args):
    if stop.is_set():
        raise RuntimeError('STOP: another native arm failed')
    log = SCRATCH / (name + '.log')
    argv = COMMON + args
    print('START', name, flush=True)
    started = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(argv, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, timeout=29000)
    retain(log, name + '.log')
    with record_lock:
        records.append(dict(name=name, head=HEAD, command=argv, rc=result.returncode,
                            seconds=round(time.monotonic()-started, 3)))
        (OUT/'native-commands.json').write_text(json.dumps(records, indent=2)+'\n')
    print('END', name, result.returncode, flush=True)
    if result.returncode:
        stop.set()
        raise RuntimeError(name + ' failed: ' + log.read_text()[-5000:])


def case(name, args, capture):
    directory = Path(args[args.index('--build-dir')+1])
    with build_lock:
        command('build-' + name, args + ['--build-only'])
    if capture:
        native = [str(OUT/'run_capture_native.py'), str(directory)]
        command(name, native)
        path = directory/'measurement.json'
        if path.exists():
            data = json.loads(path.read_text())
            if data['shape'] == 'endstation_ax7101_8x8' and data['maximum_ms'] > 24.5:
                stop.set()
                raise RuntimeError('STOP: 8x8 capture exceeds 24.5 ms')
            retain(path, name+'.json')
        retain(directory/'capture.log', name+'-raw.log')
        retain(directory/'sources.json', name+'-sources.json')
    else:
        command(name, args + ['--reuse-build'])
        for path in sorted(directory.glob('service-*.json')):
            data = json.loads(path.read_text())
            if args[args.index('--mutation')+1] == 'none' if '--mutation' in args else True:
                phy = data['phy']
                charge = (phy['max_poll_sys_cycles']+9*phy['max_transaction_sys_cycles'])/100000
                if charge > 50:
                    stop.set()
                    raise RuntimeError('STOP: MDIO charge exceeds smallest device wait')
            retain(path, name+'-receipt.json')
            retain(path.with_suffix('.log'), name+'-raw.log')
        retain(directory/'service_spec.json', name+'-spec.json')
        if '--mutation' not in args or args[args.index('--mutation')+1] != 'no-publish':
            command('regrade-'+name, args + ['--regrade'])


cases = []
for short, shape, mhz in [('8x8', 'endstation_ax7101_8x8', 50),
                           ('1x1', 'endstation_ax7101_1x1_tdm8', 50),
                           ('8x8', 'endstation_ax7101_8x8', 100)]:
    for traffic in ('on', 'off'):
        name = f'capture-{short}-{mhz}-{traffic}'
        cases.append((name, ['tb/verilator/nvm_capture_cpu/run.py', '--shape', shape,
                             '--cpu-hz', str(mhz*1000000), '--captures', '16', '--traffic', traffic,
                             '--build-dir', str(SCRATCH/name)], True))
for short, shape in [('1x1', 'endstation_ax7101_1x1_tdm8'), ('8x8', 'endstation_ax7101_8x8')]:
    for plan in ('all', 'uart-paced', 'queued-input', 'queued-short', 'queued-builtins', 'device-wait'):
        name = 'service-'+short+'-'+plan
        args = ['tb/verilator/fw_service_budget/run.py', '--shape', shape, '--build-dir', str(SCRATCH/name),
                '--populated', '--plan', plan, '--enforce-service']
        if plan == 'device-wait':
            args += ['--device-wait-us', '3000000', '--program-wait-us', '5000']
        cases.append((name, args, False))
for mutation, plan in [('remove-dispatch', 'queued-builtins'), ('late-sample', 'all'),
                       ('remove-dispatch', 'queued-short'), ('no-publish', 'all')]:
    name = 'service-'+mutation+'-'+plan
    cases.append((name, ['tb/verilator/fw_service_budget/run.py', '--shape', 'endstation_ax7101_1x1_tdm8',
                         '--build-dir', str(SCRATCH/name), '--populated', '--plan', plan,
                         '--enforce-service', '--mutation', mutation], False))
with ThreadPoolExecutor(max_workers=8) as pool:
    futures = [pool.submit(case, *entry) for entry in cases]
    for future in as_completed(futures):
        future.result()
for mutation in ('byte-only', 'skip-copy', 'no-traffic'):
    name = 'capture-'+mutation
    directory = SCRATCH/name
    args = ['tb/verilator/nvm_capture_cpu/run.py', '--shape',
            'endstation_ax7101_8x8' if mutation == 'byte-only' else 'endstation_ax7101_1x1_tdm8',
            '--captures', '2', '--mutation', mutation, '--build-dir', str(directory)]
    if mutation == 'byte-only':
        args += ['--baseline-measurement', str(SCRATCH/'capture-8x8-50-on/measurement.json')]
    command(name, args)
    for filename in ('capture.log', 'measurement.json', 'sources.json'):
        path = directory/filename
        if path.exists():
            retain(path, name+'-'+filename)
print('ALL NATIVE MEASUREMENTS COMPLETE', flush=True)
