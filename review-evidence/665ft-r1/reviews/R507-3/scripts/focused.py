#!/usr/bin/env python3
"""Reproduce the round-three focused review; all subprocesses are awaited.

Usage: python3 focused.py REPOSITORY PACKET {tally,codec,adp}
Disposable products stay in PACKET/scratch; raw receipts stay in receipts.
"""
import concurrent.futures
import gzip
import json
import os
from pathlib import Path
import resource
import subprocess
import sys

ROOT, PACKET = (Path(x).resolve() for x in sys.argv[1:3])
MODE = sys.argv[3]
WORK = PACKET / 'scratch' / MODE
OUT = PACKET / 'receipts' / MODE
WORK.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(WORK)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
sys.path.insert(0, str(ROOT / 'sw/firmware/gtest'))
import fw_gtest


def save(name, result):
    (OUT / (name + '.log')).write_text(result.stdout + result.stderr)
    (OUT / (name + '.rc')).write_text(str(result.returncode) + '\n')


def tally():
    import tally_selftest as ts
    b = fw_gtest.Build(jobs=2)
    print('toolchain:', fw_gtest.toolchain(), flush=True)
    exe = ts.build(WORK / 'control', b)
    cases = OUT / 'control'
    cases.mkdir(exist_ok=True)
    for case in ts.CASES:
        wrong = ts.grade_case(case, exe, cases)
        assert not wrong, (case.gtest_filter, wrong)
    print(f'control: {len(ts.CASES)} of {len(ts.CASES)} cases passed', flush=True)
    for defect in ts.DEFECTS:
        work = WORK / defect.name
        out = OUT / defect.name
        work.mkdir(exist_ok=True)
        out.mkdir(exist_ok=True)
        exe = ts.build(work, b, ts.plant(defect, work))
        results = {c.gtest_filter: ts.grade_case(c, exe, out, quiet=True)
                   for c in ts.CASES if not c.env}
        (out / 'grades.json').write_text(json.dumps(results, indent=2) + '\n')
        assert all(results[f] for f in defect.cases), (defect.name, results)
        print('CAUGHT', defect.name, {f: results[f] for f in defect.cases}, flush=True)
    print(f'listener defects: {len(ts.DEFECTS)} of {len(ts.DEFECTS)} caught', flush=True)


def codec():
    sys.path.insert(0, str(ROOT / 'sw/firmware/ctrl_nvm/test'))
    import test_ctrl_nvm as gate
    import nvm_bench as nb
    import nvm_mutants as nm
    binary = nb.Binary('codec', (*nb.RIG, 'test_nvm_boot.cpp', 'test_nvm_codec.cpp'))
    print('toolchain:', fw_gtest.toolchain(), flush=True)
    shapes = {}
    for cfg in sorted((ROOT / 'configs').glob('endstation_*.yaml')):
        shape = gate.prepare(cfg, WORK / cfg.stem / 'input')
        shapes[cfg.stem] = shape
        exe = nb.build_suite(shape.inputs, WORK / cfg.stem / 'build', fw_gtest.Build(jobs=8), binary)
        res = fw_gtest.run([str(exe)], env={**os.environ, 'NVM_FIXTURE': str(shape.fixture)}, timeout=120)
        save(cfg.stem, res)
        ok, why = fw_gtest.grade(res.returncode, res.stdout + res.stderr)
        print(cfg.stem, why, flush=True)
        assert ok
    names = {'header_guard_early', 'header_guard_late', 'payload_guard_early', 'payload_guard_late'}
    mutants = [m for m in nm.MUTANTS if m.name in names]
    assert len(mutants) == 4
    shape = shapes['endstation_ax7101_1x1_tdm8']

    def probe(m):
        work = WORK / m.name
        tree = work / 'tree'
        nm.plant(m, tree)
        exe = nb.build_suite(shape.inputs, work / 'build', fw_gtest.Build(jobs=2), binary, tree)
        res = fw_gtest.run([str(exe), '--gtest_filter=NvmCodec.codec_loaded_prefix'],
                          env={**os.environ, 'NVM_FIXTURE': str(shape.fixture)}, timeout=120)
        save(m.name, res)
        log = res.stdout + res.stderr
        assert res.returncode == 1
        assert 'NvmCodec.codec_loaded_prefix' in fw_gtest.failed_tests(log)
        assert not fw_gtest.grade(res.returncode, log)[0]
        print('CAUGHT', m.name, next(x.strip() for x in log.splitlines() if '[FAIL]' in x), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(probe, mutants))
    print('codec: five shape controls green; four boundary defects caught', flush=True)


def adp():
    source = PACKET / 'scripts/adp_probe.c'
    target = ROOT / 'sw/firmware/ctrl/adp/adp.c'
    # These are exactly the line/arc claims in the five README rows.
    lines = target.read_text().splitlines()
    statements = [
        'if (a->state == ADP_STATE_DOWN) {',
        'if (a->state != ADP_STATE_DOWN) {',
        'if (a->state == ADP_STATE_DELAY && kind == ADP_TIMER_DELAY) {',
        '} else if (a->state == ADP_STATE_WAITING && kind == ADP_TIMER_ADVERTISE) {',
        'if (a->enabled && a->state == ADP_STATE_DELAY) {',
    ]
    # Row 1 also occurs in shutdown: select only the public link-change function.
    start = lines.index('void adp_link_change(struct adp *a, bool up)')
    row_lines = [next(i + 1 for i in range(start, len(lines)) if lines[i].strip() == s)
                 for s in statements]
    wanted = {1: [(0, 2)], 2: [(1, 2)], 3: [(2, 4), (3, 2)],
              4: [(3, 4)], 5: [(4, 4)], 6: [(4, 2)]}
    summary = {}
    for case in range(1, 7):
        work = WORK / str(case)
        work.mkdir(exist_ok=True)
        argv = ['gcc', '-std=c11', '-O0', '--coverage', '-Wall', '-Wextra', '-Werror',
                '-I' + str(target.parent), '-I' + str(ROOT / 'sw/firmware/ctrl/wire')]
        subprocess.run([*argv, '-c', str(target), '-o', str(work / 'adp.o')], check=True)
        subprocess.run([*argv, str(source), str(work / 'adp.o'), '-o', str(work / 'probe')], check=True)
        res = subprocess.run([str(work / 'probe'), str(case)], capture_output=True, text=True, check=False)
        save(str(case), res)
        assert res.returncode == 0
        subprocess.run(['gcov', '-b', '-j', str(work / 'adp.gcno')], cwd=work, check=True,
                       stdout=subprocess.DEVNULL)
        raw_bytes = (work / 'adp.gcov.json.gz').read_bytes()
        (OUT / f'{case}.gcov.json.gz').write_bytes(raw_bytes)
        raw = json.loads(gzip.decompress(raw_bytes))
        measured = next(f for f in raw['files'] if Path(f['file']) == target)
        data = {x['line_number']: x for x in measured['lines']}
        summary[case] = {str(i + 1): {'line': line, 'count': data[line]['count'],
                                     'arcs': [b['count'] for b in data[line]['branches']]}
                         for i, line in enumerate(row_lines)}
        for row, arc in wanted[case]:
            assert summary[case][str(row + 1)]['arcs'][arc - 1] > 0, (case, row, arc)
        print(res.stdout.strip(), summary[case], flush=True)
    (OUT / 'arcs.json').write_text(json.dumps(summary, indent=2) + '\n')
    print('ADP: all five rows and all seven excluded arcs reached by rule-breaking ports', flush=True)


{'tally': tally, 'codec': codec, 'adp': adp}[MODE]()
