#!/usr/bin/env python3
"""Focused source review reproduction. Run from the exact-head repository.

Requires installed C/C++ compilers and the repository's test dependencies.
Set CPLUS_INCLUDE_PATH and LIBRARY_PATH for a non-system test library.
All disposable sources and builds stay under packet/scratch.
"""
import concurrent.futures
import contextlib
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path.cwd()
PACKET = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'sw/firmware/ctrl/test'))
import ctrl_build
import srp_arms
import srp_mutants
import srp_link_mutants


def task(spec):
    kind, shape = spec
    label = kind + '-' + shape
    work = PACKET / 'scratch' / label
    work.mkdir(parents=True, exist_ok=True)
    receipts = PACKET / 'receipts'
    receipts.mkdir(exist_ok=True)
    interfaces = 2 if shape.endswith('2if') else 1
    entity = 'endstation_ax7101_8x8' if shape.startswith('8x8') else 'endstation_ax7101_1x1_tdm8'
    config = ROOT / 'configs' / (entity + '.yaml')
    build = ctrl_build.fw_gtest.Build(jobs=3)
    rc = 0
    with (receipts / (label + '.log')).open('w') as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        print('head', subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(), flush=True)
        print('task', label, flush=True)
        try:
            if kind == 'plants':
                srp_mutants.DEFECTS = srp_link_mutants.defects(srp_mutants.Defect)
                rc = int(srp_mutants.campaign(work, ROOT / 'third_party/lwSRP', jobs=3, interfaces=interfaces, entity=entity))
                for p in work.glob('link-pass-*.log'):
                    shutil.copyfile(p, receipts / (label + '-' + p.name))
            else:
                src = ctrl_build.CTRL
                if kind == 'base':
                    src = work / 'ctrl'
                    shutil.copytree(ctrl_build.CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
                    for name in ('srp/srp_mbx.c', 'srp/srp_mbx.h'):
                        (src / name).write_bytes(subprocess.check_output(['git', 'show', 'dd163e41:sw/firmware/ctrl/' + name]))
                tree = ctrl_build.Tree(src, work / 'build', work / 'reuse', build)
                suites = ['srp_link_pass.cpp']
                if kind == 'head':
                    suites += ['srp_mbx.cpp', 'srp_app.cpp']
                for suite in suites:
                    result = srp_arms.arm_srp(tree, ROOT / 'third_party/lwSRP', interfaces, test=suite, config=config)
                    print(result.arm, 'rc', result.rc)
                    print(result.log, flush=True)
                    if kind == 'base':
                        good = result.rc != 0 and 'a first UP resets nothing' in result.log and 'a later UP resets the interface once' in result.log
                        print('expected baseline defect reproduced:', good)
                        rc |= int(not good)
                    else:
                        rc |= result.rc
        except Exception:
            import traceback
            traceback.print_exc()
            rc = 2
        print('task exit:', rc, flush=True)
    (receipts / (label + '.rc')).write_text(str(rc) + '\n')
    return label, rc


if __name__ == '__main__':
    specs = [(kind, shape) for kind in ('head', 'base', 'plants') for shape in ('1x1-1if', '8x8-1if')]
    specs += [('head', '8x8-2if'), ('plants', '1x1-2if')]
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(task, specs))
    for label, rc in results:
        print(label, rc)
    sys.exit(any(rc for _, rc in results))
