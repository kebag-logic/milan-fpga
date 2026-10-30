#!/usr/bin/env python3
"""Concurrent split-boot preparation, serialized native make -j16, foreground completion.

Usage: run_boots.py CHECKOUT LITEX_PYTHON CPU_PACKAGE COMPILER_BIN VERILATOR_BIN
The CPU package must be a disposable copy. No source or shared installation is edited.
Start run_campaigns.py first or concurrently: native compilation waits for its four rc receipts.
"""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
python, cpu_package, compiler_bin, verilator_bin = sys.argv[2:]
env = dict(os.environ, PYTHONPATH=cpu_package, PYTHONDONTWRITEBYTECODE='1',
           PYTHONHASHSEED='0', COURSIER_MODE='offline', SBT_OPTS='-Dsbt.offline=true',
           LITEX_ENV_CC_TRIPLE='riscv32-buildroot-linux-gnu')
env['PATH'] = ':'.join([verilator_bin, compiler_bin, str(Path(python).parent), env['PATH']])
code = '''import fcntl, importlib.util, sys, time
from pathlib import Path
packet, root = map(Path, sys.argv[1:3])
spec = importlib.util.spec_from_file_location('boot_run',root/'tb/verilator/ctrl_split_boot/run.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
original = m.run
def run(argv, *args, **kw):
    if argv[0] != 'make':
        return original(argv, *args, **kw)
    with (packet/'scratch/native-make.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        while not all((packet/f'firmware-shard{n}.rc').exists() for n in range(4)):
            time.sleep(1)
        return original(argv, *args, **kw)
m.run = run
sys.argv = ['run.py', *sys.argv[3:]]
raise SystemExit(m.main())
'''
def point(name, args):
    out = packet/'scratch'/name
    cmd = [python, '-B', '-c', code, str(packet), str(root), '--build-dir', str(out), *args]
    with (packet/f'{name}.log').open('w') as log:
        log.write('CPU 50000000 Hz; bus 100000000 Hz; exact head ac105b158bb740a65e0154305377fd4a7d0f6f87\n')
        log.flush()
        rc = subprocess.run(cmd, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    (packet/f'{name}.rc').write_text(str(rc)+'\n')
    print(name, rc, flush=True)
    if not args or '--shape' in args:
        cmd += ['--regrade']
        with (packet/f'{name}-regrade.log').open('w') as log:
            log.write('CPU 50000000 Hz; bus 100000000 Hz\n'); log.flush()
            regrade = subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
        (packet/f'{name}-regrade.rc').write_text(str(regrade)+'\n')
        return rc or regrade
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    fs = [pool.submit(point, 'boot-1x1', []),
          pool.submit(point, 'boot-8x8', ['--shape','endstation_ax7101_8x8']),
          pool.submit(point, 'boot-plants', ['--self-test'])]
    results = [f.result() for f in fs]
sys.exit(any(results))
