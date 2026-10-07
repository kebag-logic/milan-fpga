#!/usr/bin/env python3
"""Reproduce documented limitations only in disposable source copies."""
import concurrent.futures
import os
from pathlib import Path
import shutil
import subprocess
import sys

packet = Path(sys.argv[1]).resolve()
host = packet / 'scratch/host'
probe = packet / 'scratch/wrong-disable'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
sdk = packet / 'scratch/sdk'
for key, value in [('CMAKE_PREFIX_PATH', sdk), ('CPATH', sdk / 'include'),
                   ('LIBRARY_PATH', sdk / 'lib'), ('LD_LIBRARY_PATH', sdk / 'lib')]:
    env[key] = str(value) + (os.pathsep + env[key] if env.get(key) else '')

def run(name, command, cwd):
    r = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=540)
    (packet / 'receipts' / (name + '.log')).write_text((r.stdout+r.stderr).replace(str(packet),'$PACKET'))
    (packet / 'receipts' / (name + '.rc')).write_text(str(r.returncode)+'\n')
    print(name, r.returncode, flush=True)
    assert r.returncode == 0

def binding_probe():
    shutil.copytree(host, probe, ignore=shutil.ignore_patterns('build','__pycache__'), dirs_exist_ok=True)
    f = probe / 'tests/features/switch_bindings.c'
    original = f.read_bytes()
    assert original.count(b'return shlan_port_disable(sw, port_id);') == 1
    f.write_bytes(original.replace(b'return shlan_port_disable(sw, port_id);',b'return shlan_port_enable(sw, port_id);'))
    try:
        run('wrong-disable-configure',['cmake','-S','.','-B','build','-DCMAKE_BUILD_TYPE=Debug'],probe)
        run('wrong-disable-build',['cmake','--build','build','--parallel','2'],probe)
        run('wrong-disable-scenarios',['behave'],probe)
    finally:
        f.write_bytes(original)
    assert f.read_bytes()==original
    (packet / 'receipts/wrong-disable-restored.txt').write_text('Disposable binding source restored byte-for-byte. Reviewed checkout was never mutated.\n')

def receive_probe():
    run('receive-probe-compile',['cc','-std=c11','-Isrc/include',str(packet/'scripts/receive_probe.c'),
        '-Lbuild','-Wl,-rpath,'+str(host/'build'),'-lshlan','-o','build/receive-probe'],host)
    run('receive-probe',['./build/receive-probe'],host)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures=[pool.submit(binding_probe),pool.submit(receive_probe)]
    for future in futures:
        future.result()
