#!/usr/bin/env python3
"""Run focused probes in disposable storage. Args: checkout packet compiler-wrapper."""
import concurrent.futures as cf
import os
from pathlib import Path
import shutil
import subprocess
import sys

repo, packet, compiler = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
bench = packet / 'scratch/tb/verilator/mbx'
bench.mkdir(parents=True, exist_ok=True)
for p in (repo / 'tb/verilator/mbx').iterdir():
    if p.is_file(): shutil.copy2(p, bench / p.name)
shutil.copytree(repo / 'tb/common', packet / 'scratch/tb/common', dirs_exist_ok=True)
(bench / 'suite_probe.hpp').write_text((bench / 'suite.hpp').read_text().replace(' private:', ' public:'))
shutil.copy2(packet / 'probe.cpp', bench / 'probe.cpp')
base = subprocess.check_output(['make','-s','print-vflags',f'ROOT={repo}',f'VERILATOR={compiler}',
                                'VBUILD_JOBS=3'], cwd=bench, text=True).splitlines()
rtl = [str(repo / 'hdl/milan/mailbox' / p) for p in
       ['KL_mbx_pkg.sv','KL_mbx_ring.sv','KL_mbx_rx.sv','KL_mbx_tx.sv','KL_mbx_evt.sv','KL_mbx.sv',
        'KL_mbx_wb.sv','KL_mbx_axil.sv']] + ['tb_mbx_top.sv']
def run(host):
    out = bench / ('obj_probe'+str(host))
    cmd = base + [f'-GHOST_P={host}', '--Mdir', str(out), *rtl, 'probe.cpp','-o','probe']
    with (packet / f'probe-{host}.log').open('w') as log:
        log.write('Exact source 3926c271aaf77420fb9093694be0ab9d511b898d\n'); log.flush()
        rc = subprocess.run(cmd,cwd=bench,stdout=log,stderr=subprocess.STDOUT).returncode
        if rc == 0: rc = subprocess.run([str(out/'probe'),str(host)],stdout=log,stderr=subprocess.STDOUT).returncode
    (packet/f'probe-{host}.rc').write_text(str(rc)+'\n')
    return rc
with cf.ThreadPoolExecutor(max_workers=2) as pool:
    codes=list(pool.map(run,[0,1]))
fw=repo/'sw/firmware/ctrl'
inc=[f'-I{fw/p}' for p in ['mbx','host','test']]+[f'-I{bench}',f'-I{repo}/third_party/tsn-c-stack/include']
with (packet/'probe-model.log').open('w') as log:
    cmd=['cc','-std=c11','-O2',*inc,'-c',str(fw/'host/mbx_model.c'),'-o',str(bench/'probe-model.o')]
    rc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT).returncode
    if rc==0: rc=subprocess.run(['c++','-std=c++17','-O2','-DREVIEW_MODEL',*inc,str(bench/'probe.cpp'),
                                  str(bench/'probe-model.o'),'-o',str(bench/'probe-model')],stdout=log,stderr=subprocess.STDOUT).returncode
    if rc==0: rc=subprocess.run([str(bench/'probe-model')],stdout=log,stderr=subprocess.STDOUT).returncode
    codes.append(rc)
    (packet/'probe-model.rc').write_text(str(rc)+'\n')
print('Probe return codes:',codes)
sys.exit(any(codes))
