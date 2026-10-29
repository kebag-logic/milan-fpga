#!/usr/bin/env python3
"""Reviewer probe: do the target boot cases catch a store that skips a restore walk?

Usage: probe_restore_mutants.py CLONE POINT RUN_DIR BUILD_DIR OUT_DIR [MAKE_JOBS]

RUN_DIR is a finished `run.py --point POINT` results directory (its commit's
journal, commit.journal.out, is booted). Each plant is a scratch copy of the
saved-state store's tree (build.Plant; the checkout is never edited):
  skip-bind-walk  nvm.st.bind_terminal = nvm_walk_bind();  ->  = ((void)nvm_walk_bind, NVM_T_COMPLETE);
  skip-d3-walk    nvm.st.terminal = nvm_walk_d3();         ->  = ((void)nvm_walk_d3, NVM_T_COMPLETE);
Each is built on the fixture arm with the checkout's run.built, booted on the
`valid` case's script and journal with run.boot, and graded with the
checkout's grade_case against the container's apply order, as run.py grades
`valid`. A plant is caught when the case FAILS; both must be caught, and the
findings must name the missing apply entries or the answered values.
Exit 0 = both caught; 1 = one escaped.
"""
import json
import struct
import sys
from pathlib import Path

clone, point = Path(sys.argv[1]).resolve(), sys.argv[2]
run_dir, build_dir, out = (Path(a).resolve() for a in sys.argv[3:6])
sys.path.insert(0, str(clone / 'tb/verilator/nvm_split_target'))
import run  # noqa: E402
import target_cases as cases  # noqa: E402
import target_grade as tg  # noqa: E402

if len(sys.argv) > 6:
    run.build.JOBS = int(sys.argv[6])
PLANTS = {
    'skip-bind-walk': ('\t\tnvm.st.bind_terminal = nvm_walk_bind();\n', '\t\tnvm.st.bind_terminal = ((void)nvm_walk_bind, NVM_T_COMPLETE);\n'),
    'skip-d3-walk': ('\t\tnvm.st.terminal = nvm_walk_d3();\n', '\t\tnvm.st.terminal = ((void)nvm_walk_d3, NVM_T_COMPLETE);\n'),
}
saved = (run_dir / 'commit.journal.out').read_bytes()
shape = run.POINTS[point][0]
out.mkdir(parents=True, exist_ok=True)
bench, records, length = cases.shape_bench(shape, out / 'shape')
pages = -(-length // cases.PAGE)
applied = bench.decode(saved[:struct.unpack_from('<I', saved, 16)[0]])[1]
applies = tg.expected_applies(applied, bench.expect, bench.donor.base)
caught_all = True
for name, (anchor, replacement) in PLANTS.items():
    cases.PLANTS[name] = cases.build.Plant(name, 'ctrl_nvm/nvm_store.c', anchor, replacement)
    case = cases.Case('valid', 'fixture', name, 'saved')
    spec = run.built(build_dir, cases.build_key(case), point, reuse=True)
    target = cases.scenario.point(point, spec)
    sub = out / name
    sub.mkdir(exist_ok=True)
    log, left = run.boot(spec, sub, case, cases.script(case, target, records, pages), saved)
    ctx = tg.Context(spec['cpu_hz'], records, pages, saved, left, applied, applies)
    result = tg.grade_case(case, tg.observe(log, spec['sys_hz'], spec['cpu_hz']), ctx, bench)
    caught = not result['passed']
    caught_all &= caught
    print(f'PROBE {name}:', 'CAUGHT' if caught else 'ESCAPED', json.dumps(result['findings'])[:600])
sys.exit(0 if caught_all else 1)
