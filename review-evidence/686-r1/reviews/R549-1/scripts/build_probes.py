#!/usr/bin/env python3
"""Two foreground builds; no checkout mutations or detached processes."""
import argparse
import concurrent.futures
import pathlib
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True, type=pathlib.Path)
p.add_argument('--verilator', required=True)
a = p.parse_args()
repo = a.repo.resolve()
packet = pathlib.Path(__file__).resolve().parents[1]

def run_case(name, source):
    work = packet / 'scratch' / name
    work.mkdir(parents=True, exist_ok=True)
    flags = ['--cc', '--exe', '--build', '-j', '4', '--top-module', 'KL_maap',
             '-GCLK_FREQ_HZ_P=10000', '-Wno-fatal', '--Mdir', str(work / 'obj'),
             '-CFLAGS', '-std=c++17 -O2 -Wall -Wextra', '-o', str(work / 'run')]
    if name == 'unit':
        flags.append('--coverage')
    argv = [a.verilator, *flags, str(repo/'hdl/ieee1722/maap/KL_maap.sv'), str(source)]
    with (packet/'receipts'/f'{name}-build.log').open('w') as log:
        built = subprocess.run(argv, cwd=work, stdout=log, stderr=subprocess.STDOUT)
    (packet/'receipts'/f'{name}-build.rc').write_text(str(built.returncode)+'\n')
    if built.returncode:
        return name, built.returncode
    with (packet/'receipts'/f'{name}.log').open('w') as log:
        ran = subprocess.run([str(work/'run')], cwd=work, stdout=log, stderr=subprocess.STDOUT)
    (packet/'receipts'/f'{name}.rc').write_text(str(ran.returncode)+'\n')
    return name, ran.returncode

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(run_case, 'unit', repo/'tb/verilator/maap/sim_main.cpp'),
               pool.submit(run_case, 'probe', packet/'scripts/probe.cpp')]
    for future in futures:
        name, rc = future.result()
        print(f'{name}: rc={rc}')
        path = packet/'receipts'/f'{name}.log'
        print(path.read_text()[-3000:] if path.exists() else 'build failed')
