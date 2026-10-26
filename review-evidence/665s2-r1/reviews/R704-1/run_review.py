#!/usr/bin/env python3
"""Focused independent reproduction; all children joined in the foreground.

Use the product Python environment. Set REVIEW_ROOT, REVIEW_PACKET,
LITEX_ENV_CC_TRIPLE and MILAN_RV32_CC; place the pinned simulator on PATH.
The CPU package must be an isolated copy on PYTHONPATH.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(os.environ['REVIEW_ROOT'])
PACKET = Path(os.environ['REVIEW_PACKET'])
SCRATCH = PACKET / 'scratch'
HARNESS = ROOT / 'tb/verilator/ctrl_service_budget'


def run(name, argv, cwd=ROOT):
    start = time.monotonic()
    print('START', name, flush=True)
    with (SCRATCH / (name + '.raw.log')).open('w') as out:
        result = subprocess.run(argv, cwd=cwd, stdout=out, stderr=subprocess.STDOUT)
    receipt = {'name': name, 'returncode': result.returncode,
               'elapsed_seconds': round(time.monotonic() - start, 3)}
    (PACKET / (name + '.rc.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    print('END', receipt, flush=True)
    return result.returncode


def build_one(name, point, regions='cover', mutation='none', variant='none'):
    sys.path.insert(0, str(HARNESS))
    import build
    # Independently planted defect: slow every ACMP receive before dispatch.
    if mutation == 'review-slow-acmp':
        source = (ROOT / 'sw/firmware/ctrl/acmp/acmp_mbx.c').read_text()
        anchor = '\tacmp_rx('
        lines = [line for line in source.splitlines(True) if line.startswith(anchor)]
        assert len(lines) == 1, lines
        build.MUTATIONS[mutation] = ('acmp/acmp_mbx.c', lines[0],
            '\tfor (volatile uint32_t review_delay = 0; review_delay < 24000u; ++review_delay) { }\n' + lines[0])
    shapes = {'1x1': ('endstation_ax7101_1x1_tdm8', 1), '8x8': ('endstation_ax7101_8x8', 2)}
    build.build(SCRATCH / name, *shapes[point], cpu_regions=regions, mutation=mutation, variant=variant)


def campaign(name, point, groups, extra=()):
    return run(name + '-run', [sys.executable, '-B', str(HARNESS / 'run.py'),
        '--point', point, '--build-dir', str(SCRATCH / name), '--reuse-build',
        '--jobs', '8', '--groups', groups, '--record-budget-findings', *extra])


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'build-one':
        build_one(*sys.argv[2:])
    elif mode == 'build':
        for name, point in [('A1', '1x1'), ('A8', '8x8')]:
            if run(name + '-build', [sys.executable, '-B', __file__, 'build-one', name, point]):
                raise SystemExit(1)
    elif mode == 'measure':
        groups = 'acmp-cmd,acmp-disc,acmp-noresp,acmp-notk,adp-link,adp-gm,adp-discover,adp-advertise,aecp,maap,srp,backlog,backlog-adp,control'
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda x: campaign(*x, groups), [('A1', '1x1'), ('A8', '8x8')]))
        raise SystemExit(bool(any(results)))
    elif mode == 'gates':
        gates = [('selftest', [str(HARNESS / 'run.py'), '--self-test'])]
        for name, args in [('docs_check', []), ('check_doc_paths', []), ('check_doc_style', []),
                           ('check_archive', []), ('check_em_dash', ['--base', 'e76a755a']),
                           ('gen_toc', ['--check'])]:
            gates.append((name, [str(ROOT / 'scripts' / (name + '.py')), *args]))
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            futures = [pool.submit(run, name, [sys.executable, '-B', *argv]) for name, argv in gates]
            futures.append(pool.submit(run, 'behave', [sys.executable, '-B', '-m', 'behave'], ROOT / 'tests'))
            results = [f.result() for f in futures]
        raise SystemExit(bool(any(results)))
