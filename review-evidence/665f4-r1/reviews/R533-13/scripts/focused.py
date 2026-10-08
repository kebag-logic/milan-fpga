#!/usr/bin/env python3
"""Portable foreground focused review; all disposable outputs stay in scratch."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

HEAD = '154722e14781c7373f3229420b6e007f9bcf9835'
NAMES = ('feedback-leave-clears-advertise-only',
         'feedback-failed-indication-as-advertise',
         'feedback-change-clears-both-kinds')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--packet', type=Path, required=True)
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--worker', choices=['plain','asan','plants','coverage','prior-probes'])
    ap.add_argument('--interfaces', type=int, default=1)
    a = ap.parse_args()
    a.source = a.source.resolve(); a.packet = a.packet.resolve()
    assert 1 <= a.jobs <= 4
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.source,text=True).strip() == HEAD
    scratch = a.packet / 'scratch'; scratch.mkdir(exist_ok=True)
    receipts = a.packet / 'receipts'; receipts.mkdir(exist_ok=True)
    temp = scratch / 'tmp'; temp.mkdir(exist_ok=True)
    os.environ['TMPDIR'] = str(temp)
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    sys.dont_write_bytecode = True
    os.chdir(a.source)
    if not a.worker:
        tasks = [(mode,i) for mode in ('plain','asan','plants') for i in (1,2)] + [('coverage',1)]
        def run(task):
            mode,i = task
            label = mode if mode == 'coverage' else f'{mode}-if{i}'
            cmd = [sys.executable,'-B',str(Path(__file__).resolve()),'--source',str(a.source),
                   '--packet',str(a.packet),'--jobs',str(a.jobs),'--worker',mode,'--interfaces',str(i)]
            start = time.monotonic()
            with (receipts / (label+'.log')).open('w') as log:
                r = subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=590)
            (receipts / (label+'.rc')).write_text(str(r.returncode)+'\n')
            row = {'task':label,'rc':r.returncode,'seconds':round(time.monotonic()-start,2)}
            print(json.dumps(row),flush=True)
            return row
        # Four foreground subprocesses, four compilation jobs each: at most 16.
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            rows = list(pool.map(run,tasks))
        (receipts/'focused-results.json').write_text(json.dumps(rows,indent=2)+'\n')
        return int(any(r['rc'] for r in rows))
    if a.worker == 'coverage':
        return subprocess.run([sys.executable,'-B','sw/firmware/gtest/fw_coverage.py','--check',
                               '--jobs',str(a.jobs),'--keep',str(scratch/'coverage')]).returncode
    sys.path.insert(0,str(a.source/'sw/firmware/ctrl/test'))
    import ctrl_build
    import fw_gtest
    import srp_arms
    import srp_mutants
    out = scratch / f'{a.worker}-if{a.interfaces}'
    lw = a.source/'third_party/lwSRP'
    if a.worker == 'plants':
        srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in NAMES)
        assert len(srp_mutants.DEFECTS) == 3
        failed = srp_mutants.campaign(out,lw,jobs=a.jobs,interfaces=a.interfaces)
        for d in srp_mutants.DEFECTS:
            shutil.copyfile(out/(d.name+'.log'),receipts/f'{d.name}-if{a.interfaces}.log')
        return int(failed)
    build = fw_gtest.Build(jobs=a.jobs,address_sanitizer=a.worker=='asan')
    tree = ctrl_build.Tree(ctrl_build.CTRL,out/'build',out/'reuse',build)
    if a.worker == 'prior-probes':
        tests = out/'tests'
        shutil.copytree(ctrl_build.HERE,tests,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        probe = a.packet/'scripts/r12_failed_intrapdu.hpp'
        shutil.copyfile(probe,tests/probe.name)
        with (tests/'test_acmp_mbx.cpp').open('a') as f:
            f.write('\n#include "r12_failed_intrapdu.hpp"\n')
        srp_arms.HERE = tests
        result = srp_arms.arm_srp(tree,lw,a.interfaces,test=('test_acmp_mbx.cpp','SrpFeedback.R12*'))
        print(result.log,flush=True)
        return result.rc
    suites = ['test_acmp_mbx.cpp'] if a.worker=='plain' else [
        'srp_mbx.cpp','srp_rx_retry.cpp','srp_app.cpp','test_acmp_mbx.cpp','srp_latency.cpp','srp_walk.cpp','srp_debug.cpp']
    failed = False
    for suite in suites:
        result = srp_arms.arm_srp(tree,lw,a.interfaces,test=suite,debug=suite=='srp_debug.cpp')
        print('SUITE',suite,'IF',a.interfaces,flush=True)
        print(result.log,flush=True)
        failed |= result.rc != 0
    return int(failed)

if __name__ == '__main__':
    raise SystemExit(main())
