#!/usr/bin/env python3
"""Build and run an exhaustive compiled-state probe, with a zero-seed control.
Usage: run_seed_probe.py REPO PACKET SIMULATOR
"""
import concurrent.futures
from pathlib import Path
import subprocess
import sys

repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
simulator = sys.argv[3]
source = (repo/'hdl/ieee1722/maap/KL_maap.sv').read_text()
anchor = "(mac_seed_w == 16'h0) ? 16'hACE1 : mac_seed_w"
assert source.count(anchor)==1
def run(name):
    work=packet/'scratch'/('seed-'+name)
    work.mkdir(parents=True,exist_ok=True)
    rtl=work/'KL_maap.sv'
    rtl.write_text(source if name=='clean' else source.replace(anchor,'mac_seed_w'))
    cmd=[simulator,'--cc','--exe','--build','-j','8','--public-flat-rw',
         '--top-module','KL_maap','-GCLK_FREQ_HZ_P=10000','-Wno-fatal',
         '-CFLAGS','-std=c++17 -O2','--Mdir',str(work/'obj'),str(rtl),
         str(packet/'scripts/seed_probe.cpp'),'-o','seed_probe']
    with (packet/'receipts'/f'seed-{name}.build.log').open('w') as log:
        build=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=180)
    (packet/'receipts'/f'seed-{name}.build.rc').write_text(str(build.returncode)+'\n')
    assert build.returncode==0
    result=subprocess.run([str(work/'obj/seed_probe')],capture_output=True,text=True,timeout=60)
    (packet/'receipts'/f'seed-{name}.run.log').write_text(result.stdout+result.stderr)
    (packet/'receipts'/f'seed-{name}.run.rc').write_text(str(result.returncode)+'\n')
    print(name,result.returncode,result.stdout,flush=True)
    assert result.returncode==(0 if name=='clean' else 1)
    if name!='clean': assert 'FAIL reset seed: 44257' in result.stdout
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    list(pool.map(run,['clean','zero-mutant']))
