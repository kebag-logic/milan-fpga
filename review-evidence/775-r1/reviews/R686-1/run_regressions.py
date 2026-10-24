#!/usr/bin/env python3
"""Build and run focused reset/hazard and discontinuity regressions.
Usage: python3 run_regressions.py CHECKOUT PACKET
Run run_probes.py first to create the bounded compiler wrapper.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import subprocess
import sys

root, packet = map(lambda x:Path(x).resolve(), sys.argv[1:])
scratch = packet/'scratch'
jobs = [
    ('lockstep', 'avtp_rxmon', 'lockstep-build', 'LS_MDIR='+str(scratch/'lockstep'), [('lockstep1','Vavtp_rxmon_lockstep'),('lockstep8','Vavtp_rxmon_lockstep')]),
    ('discontinuity', 'crf_rx', 'discontinuity-build', 'DISC_MDIR='+str(scratch/'discontinuity'), [('discontinuity','Vdiscontinuity')]),
]
def run(job):
    label, suite, target, option, binaries = job
    cmd=['make','-j16','-C',str(root/'tb/verilator'/suite),target,option,'VERILATOR='+str(scratch/'bounded_simulator.py')]
    with (packet/'probes'/f'{label}.build.log').open('w') as log:
        log.write(repr(cmd)+'\n');log.flush()
        built=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,env=dict(os.environ,TMPDIR=str(scratch)))
    (packet/'probes'/f'{label}.build.rc').write_text(str(built.returncode)+'\n')
    if built.returncode:return False
    passed=True
    for directory, name in binaries:
        with (packet/'probes'/f'{directory}.run.log').open('w') as log:
            result=subprocess.run([str(scratch/directory/name)],stdout=log,stderr=subprocess.STDOUT)
        (packet/'probes'/f'{directory}.run.rc').write_text(str(result.returncode)+'\n')
        passed=passed and result.returncode==0
    print(label, 'PASS' if passed else 'FAIL',flush=True)
    return passed
with ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,jobs))
raise SystemExit(0 if all(results) else 1)
