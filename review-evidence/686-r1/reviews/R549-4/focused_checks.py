#!/usr/bin/env python3
"""Reproduce focused exact-source checks; all build outputs stay in scratch."""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess

def main():
    p = argparse.ArgumentParser()
    p.add_argument('repo', type=Path)
    p.add_argument('compiler', type=Path)
    p.add_argument('--jobs', type=int, default=16)
    a = p.parse_args()
    assert 1 <= a.jobs <= 16
    repo, compiler = a.repo.resolve(), a.compiler.resolve()
    out = Path(__file__).resolve().parent
    work = out / 'scratch' / 'focused'
    work.mkdir(parents=True, exist_ok=True)
    identity = subprocess.check_output([str(compiler), '--version'], text=True)
    assert identity.startswith('Verilator 5.050 '), identity
    (out / 'compiler-identity.txt').write_text(identity + 'sha256 ' + hashlib.sha256(compiler.read_bytes()).hexdigest() + '\n')
    for rel in ['tb/verilator/maap/Makefile', 'tb/verilator/maap/sim_main.cpp',
                'tb/verilator/maap/mutants.py', 'tb/common/verilator_harness.hpp',
                'hdl/ieee1722/maap/KL_maap.sv']:
        dst = work / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repo / rel, dst)
    spec = importlib.util.spec_from_file_location('cases', work / 'tb/verilator/maap/mutants.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source = (repo / 'hdl/ieee1722/maap/KL_maap.sv').read_text()
    names = {'cdl_28', 'zero_seed_freezes_the_probe_draw',
             'announce_judged_on_conflict_fields', 'three_probes',
             'defend_rewrites_the_frame_on_the_wire'}
    cases = [('clean', source, None)]
    for name, _, anchor, replacement, failure in module.MUTANTS:
        if name in names:
            assert source.count(anchor) == 1
            cases.append((name, source.replace(anchor, replacement), failure))
    assert len(cases) == 6
    concurrency = min(4, a.jobs)
    compiler_jobs = max(1, a.jobs // concurrency)
    def run(case):
        name, content, expected = case
        case_dir = work / name
        case_dir.mkdir(exist_ok=True)
        rtl = case_dir / 'KL_maap.sv'
        rtl.write_text(content)
        cmd = ['make', '-j16', '-C', str(work / 'tb/verilator/maap'), 'build',
               'MAAP_RTL=' + str(rtl), 'MDIR=' + str(case_dir / 'obj'),
               'VERILATOR=' + str(compiler), 'VERILATOR_JOBS=' + str(compiler_jobs)]
        with (case_dir / 'build.log').open('w') as log:
            built = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=300)
        (out / (name + '.build.rc')).write_text(str(built.returncode) + '\n')
        if built.returncode:
            return {'case': name, 'build_rc': built.returncode, 'passed': False}
        r = subprocess.run([str(case_dir / 'obj/VKL_maap_sim')], text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        (out / (name + '.run.log')).write_text(r.stdout)
        (out / (name + '.run.rc')).write_text(str(r.returncode) + '\n')
        good = (r.returncode == 0 and '130 checks, 0 failures' in r.stdout) if expected is None else (
            r.returncode == 1 and '[FAIL] ' + expected in r.stdout)
        return {'case': name, 'build_rc': 0, 'run_rc': r.returncode,
                'expected_rejection': expected, 'passed': good}
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
        results = list(pool.map(run, cases))
    (out / 'focused-results.json').write_text(json.dumps(results, indent=2) + '\n')
    for r in results:
        print(json.dumps(r), flush=True)
    return 0 if all(r['passed'] for r in results) else 1

if __name__ == '__main__':
    raise SystemExit(main())
