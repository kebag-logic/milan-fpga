#!/usr/bin/env python3
"""Focused, foreground review checks. Run from the pinned source checkout.

python3 /path/to/packet/run_review.py
All temporary material stays in packet/scratch. Four independent workers,
each limited to four compilation jobs, finish before this command returns.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

PACKET = Path(__file__).resolve().parent
ROOT = Path.cwd().resolve()
SCRATCH = PACKET / 'scratch'
HEAD = '6c94e9f5f496ac25f8c4e31f9e3685c725de29f3'


def worker(which):
    sys.path[:0] = [str(ROOT / 'sw/firmware/ctrl/test'),
                   str(ROOT / 'sw/firmware/ctrl_nvm/test'),
                   str(ROOT / 'sw/firmware/gtest')]
    import fw_gtest
    print('toolchain:', fw_gtest.toolchain(), flush=True)
    if which == 'ctrl':
        import ctrl_arms
        import test_ctrl_firmware
        # The installed bare-metal compiler has the required ilp32 headers.
        # The separately installed Linux SDK lacks that multilib header set.
        ctrl_arms.RV32_CANDIDATES = ('riscv64-elf-gcc',)
        return test_ctrl_firmware.main(['--require-rv32', '--jobs', '4',
                                       '--build-dir', str(SCRATCH / 'ctrl')])
    if which == 'nvm':
        return subprocess.call([sys.executable, 'sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py',
                                '--require-rv32', '--jobs', '4'])
    if which == 'coverage':
        for flag in ('--selftest', '--check'):
            rc = subprocess.call([sys.executable, 'sw/firmware/gtest/fw_coverage.py', flag, '--jobs', '4'])
            if rc:
                return rc
        return 0
    if which == 'probes':
        import ctrl_arms
        import ctrl_mutants
        from ctrl_build import Tree
        import nvm_bench
        import nvm_mutants
        import test_ctrl_nvm
        failures = []
        build = fw_gtest.Build(jobs=4)
        out = SCRATCH / 'probes'
        for m in ctrl_mutants.MUTANTS[:3]:
            tree = Tree(ctrl_mutants.plant(m, out), out / m.name / 'build', out / 'reuse', build)
            outcomes = {}
            for arm, test, needle in m.kills():
                if arm not in outcomes:
                    outcomes[arm] = getattr(ctrl_arms, 'arm_' + arm)(tree)
                    (PACKET / f'{m.name}-{arm}.log').write_text(outcomes[arm].log)
                caught = ctrl_mutants.caught(test, needle, outcomes[arm])
                print(f'{m.name}: {arm}: {test}: caught={caught}', flush=True)
                if not caught:
                    failures.append(f'{m.name}:{arm}:{test}')
        shape = test_ctrl_nvm.prepare(ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml', out / 'shape')
        binary = next(b for b in nvm_bench.UNITS if b.name == 'prefix')
        exe = nvm_bench.build_suite(shape.inputs, out / 'prefix-control', build, binary)
        passed, log = nvm_bench.run_suite(exe, shape.fixture)
        (PACKET / 'prefix-control.log').write_text(log)
        print(f'prefix control passed={passed}', flush=True)
        if not passed:
            failures.append('prefix-control')
        for m in nvm_mutants.MUTANTS:
            if not m.name.startswith('erased_payload_'):
                continue
            tree = out / m.name / 'tree'
            nvm_mutants.plant(m, tree)
            exe = nvm_bench.build_suite(shape.inputs, out / m.name / 'build', build, binary, tree)
            passed, log = nvm_bench.run_suite(exe, shape.fixture, m.kills)
            (PACKET / f'{m.name}.log').write_text(log)
            survivors = nvm_mutants.survivors(m, log)
            print(f'{m.name}: passed={passed} survivors={survivors}', flush=True)
            if passed or survivors:
                failures.append(m.name)
            if m.name in ('erased_payload_end_bound', 'erased_payload_guard_late'):
                if 'heap-buffer-overflow' not in log:
                    failures.append(m.name + ':missing-ASan-diagnostic')
        print('focused probe failures:', failures, flush=True)
        return int(bool(failures))
    raise ValueError(which)


def run_task(name):
    start = time.monotonic()
    argv = [sys.executable, str(Path(__file__).resolve()), '--worker', name]
    with (PACKET / f'{name}.log').open('w') as log:
        result = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT, timeout=590, check=False)
    (PACKET / f'{name}.rc').write_text(str(result.returncode) + '\n')
    row = {'check': name, 'rc': result.returncode, 'seconds': round(time.monotonic() - start, 2)}
    print(json.dumps(row), flush=True)
    return row


if __name__ == '__main__':
    SCRATCH.mkdir(exist_ok=True)
    (SCRATCH / 'tmp').mkdir(exist_ok=True)
    os.environ.update(TMPDIR=str(SCRATCH / 'tmp'), PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1',
                      GIT_NO_REPLACE_OBJECTS='1', LC_ALL='C')
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == HEAD
    if len(sys.argv) > 1:
        sys.exit(worker(sys.argv[2]))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(run_task, ('ctrl', 'nvm', 'coverage', 'probes')))
    (PACKET / 'checks.json').write_text(json.dumps(rows, indent=2) + '\n')
    sys.exit(int(any(row['rc'] for row in rows)))
