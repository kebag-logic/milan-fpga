#!/usr/bin/env python3
"""Focused source-head review checks; no repository files are changed."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--packet', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--worker', type=int, choices=(1, 2))
    args = ap.parse_args()
    repo, packet = args.repo.resolve(), args.packet.resolve()
    scratch = packet / 'scratch'
    scratch.mkdir(exist_ok=True)
    os.environ['TMPDIR'] = str(scratch)
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    if args.worker is None:
        def worker(n):
            with (packet / f'focused-if{n}.log').open('w') as log:
                p = subprocess.run([sys.executable, '-B', __file__, '--repo', str(repo), '--packet', str(packet),
                                    '--worker', str(n)], stdout=log, stderr=subprocess.STDOUT)
            (packet / f'focused-if{n}.rc').write_text(str(p.returncode) + '\n')
            return n, p.returncode
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(worker, (1, 2)))
        print(results)
        return int(any(rc for _, rc in results))
    sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
    import ctrl_build
    import fw_gtest
    import srp_arms
    import srp_mutants
    import srp_kind_mutants
    n = args.worker
    out = scratch / f'focused-if{n}'
    tree = ctrl_build.Tree(ctrl_build.CTRL, out / 'build', out / 'reuse', fw_gtest.Build(jobs=8))
    failed = False
    for shape, suite, selected in [
        ('1x1_tdm8', 'srp_mbx.cpp', '*'),
        ('1x1_tdm8', 'test_acmp_mbx.cpp', 'SrpFeedback.*'),
        ('8x8', 'srp_mbx.cpp', 'SrpTalkerKinds.*'),
        ('8x8', 'test_acmp_mbx.cpp', 'SrpFeedback.*'),
    ]:
        result = srp_arms.arm_srp(tree, repo / 'third_party/lwSRP', n, test=(suite, selected),
                                 config=repo / f'configs/endstation_ax7101_{shape}.yaml')
        print(f'=== {shape} if{n} {suite} {selected}: rc {result.rc} ===', flush=True)
        print(result.log, flush=True)
        failed |= bool(result.rc)
    srp_mutants.DEFECTS = srp_kind_mutants.defects(srp_mutants.Defect) + tuple(
        d for d in srp_mutants.DEFECTS if d.name == 'failed-listener-ready')
    mutants = out / 'mutants'
    failed |= srp_mutants.campaign(mutants, repo / 'third_party/lwSRP', jobs=8, interfaces=n)
    receipts = packet / f'mutations-if{n}'
    receipts.mkdir(exist_ok=True)
    for log in mutants.glob('*.log'):
        (receipts / log.name).write_bytes(log.read_bytes())
    return int(failed)

if __name__ == '__main__':
    raise SystemExit(main())
