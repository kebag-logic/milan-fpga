#!/usr/bin/env python3
"""Run the SRP adapter arms of a milan-fpga checkout without modifying it.

Usage: python3 -I run_arms.py CHECKOUT PACKET JOBS_PER_ARM WORKERS [--base-src DIR]

Arms (each 1x1 and 8x8 entity, one and two interfaces):
  head-full    the head's srp_mbx.cpp, every test;
  head-probes  scripts/probes.cpp (the two prior rounds' probes and this round's), every probe;
  base-probes  the same probes against DIR's sw/firmware/ctrl (the previously reviewed head's adapter), with the
               head's test fixtures;
and the platform sink arms (test_plat_sinks.cpp at 8x8/1if and 1x1/1if) at the head.
Each arm writes receipts/arms/<name>.log and .rc; a summary goes to receipts/arms/SUMMARY.txt.
"""
import concurrent.futures
import sys
import traceback
from pathlib import Path

args = sys.argv[1:]
probes_only = '--probes-only' in args
if probes_only:
    args.remove('--probes-only')
base_src = None
if '--base-src' in args:
    k = args.index('--base-src')
    base_src = Path(args[k + 1]).resolve()
    del args[k:k + 2]
root, packet = Path(args[0]).resolve(), Path(args[1]).resolve()
jobs, workers = int(args[2]), int(args[3])
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(root / 'sw/firmware/gtest'))
import ctrl_build as cb  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
import srp_arms  # noqa: E402

assert cb.CTRL.resolve().is_relative_to(root), (cb.CTRL, root)
out = packet / 'receipts' / 'arms'
out.mkdir(parents=True, exist_ok=True)
scratch = packet / 'scratch' / 'arms'
probes = packet / 'scripts' / 'probes.cpp'
lwsrp = root / 'third_party/lwSRP'
CFG = {'1x1': srp_arms.DEFAULT_ENTITY, '8x8': srp_arms.ENTITY_8X8}


def gtest_lines(log):
    return [ln for ln in log.splitlines() if '[  FAILED  ]' in ln or '[  PASSED  ]' in ln or '[  SKIPPED ]' in ln]


def run(spec):
    kind, shape, n_if = spec
    name = f'{kind}-{shape}-if{n_if}'
    src = base_src / 'sw/firmware/ctrl' if kind.startswith('base') else cb.CTRL
    work = scratch / name
    work.mkdir(parents=True, exist_ok=True)
    tree = cb.Tree(src, work, work / 'reuse', fw_gtest.Build(jobs=jobs))
    selected = '*Probe*:SrpEarlyTalker.Review*'
    if n_if == 1:
        selected += '-RvProbe.OtherInterfaceResetKeepsThisCount'
    test = ('srp_mbx.cpp', '*') if kind == 'head-full' else (str(probes), selected)
    try:
        result = srp_arms.arm_srp(tree, lwsrp, n_if, test=test, config=CFG[shape])
        rc, log = result.rc, result.log
    except Exception:
        rc, log = 2, traceback.format_exc()
    (out / f'{name}.log').write_text(log)
    (out / f'{name}.rc').write_text(f'{rc}\n')
    return name, rc, gtest_lines(log)


def sinks():
    work = scratch / 'head-platsinks'
    work.mkdir(parents=True, exist_ok=True)
    tree = cb.Tree(cb.CTRL, work, work / 'reuse', fw_gtest.Build(jobs=jobs))
    res = []
    try:
        for (config, _), o in zip(plat_arms.SINK_SHAPES, plat_arms.sink_arms(tree)):
            name = f'head-platsinks-{config.stem}'
            (out / f'{name}.log').write_text(o.log)
            (out / f'{name}.rc').write_text(f'{o.rc}\n')
            res.append((name, o.rc, gtest_lines(o.log)))
    except Exception:
        (out / 'head-platsinks.log').write_text(traceback.format_exc())
        res.append(('head-platsinks', 2, []))
    return res


specs = [(k, s, i) for k in (('head-probes',) if probes_only else ('head-probes', 'head-full')) + (('base-probes',) if base_src else ())
         for s in ('1x1', '8x8') for i in (1, 2)]
with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
    futs = [pool.submit(run, s) for s in specs]
    sink_fut = None if probes_only else pool.submit(sinks)
    results = [f.result() for f in futs] + (sink_fut.result() if sink_fut else [])
lines = []
for name, rc, gl in results:
    lines.append(f'ARM {name} rc={rc}')
    lines += [f'    {ln}' for ln in gl]
(out / ('PROBES-SUMMARY.txt' if probes_only else 'SUMMARY.txt')).write_text('\n'.join(lines) + '\n')
print('\n'.join(lines))
sys.exit(int(any(rc != (1 if name.startswith('base-probes') else 0) for name, rc, _ in results)))
