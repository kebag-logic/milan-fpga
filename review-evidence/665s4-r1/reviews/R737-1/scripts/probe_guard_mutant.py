#!/usr/bin/env python3
"""Reviewer probe: does the target `guard` case catch a guard off by one at the journal's end?

Usage: probe_guard_mutant.py CLONE POINT BUILD_DIR OUT_DIR [MAKE_JOBS]

Plants, in a scratch copy of the saved-state store's tree (the harness's own
build.Plant machinery; the checkout is never edited), a guard that accepts a
program starting exactly at the journal's end:
    addr - OFFSET <= SIZE - len   becomes   addr - OFFSET <= SIZE - len + 1u
builds the guard-probe arm on it with the checkout's run.built, boots the
`guard` case's own script on blank flash with the checkout's run.boot, and
grades it with the checkout's target_grade.grade_case, exactly as run.py grades
the `guard` case (the commit case is not needed: the guard boots blank flash).
The probe holds when the case FAILS with a finding naming the device or the
escape. Exit 0 = caught; 1 = escaped.
"""
import json
import sys
from pathlib import Path

clone, point = Path(sys.argv[1]).resolve(), sys.argv[2]
build_dir, out = Path(sys.argv[3]).resolve(), Path(sys.argv[4]).resolve()
sys.path.insert(0, str(clone / 'tb/verilator/nvm_split_target'))
import run  # noqa: E402
import target_cases as cases  # noqa: E402
import target_grade as tg  # noqa: E402

if len(sys.argv) > 5:
    run.build.JOBS = int(sys.argv[5])
ANCHOR = '\t       addr - MILAN_FLASH_JOURNAL_OFFSET <= MILAN_FLASH_JOURNAL_SIZE - len;\n'
cases.PLANTS['guard-end-plus-one'] = cases.build.Plant(
    'guard-end-plus-one', 'ctrl_nvm/plat/nvm_flash_litespi.c', ANCHOR,
    '\t       addr - MILAN_FLASH_JOURNAL_OFFSET <= MILAN_FLASH_JOURNAL_SIZE - len + 1u;\n')
case = cases.Case('guard', 'guard-probe', 'guard-end-plus-one', 'blank')
out.mkdir(parents=True, exist_ok=True)
spec = run.built(build_dir, cases.build_key(case), point, reuse=True)
target = cases.scenario.point(point, spec)
slot = json.loads((Path(spec['flash_map']) / 'flash_port.json').read_text())['journal']['size'] // 2
log, left = run.boot(spec, out, case, cases.script(case, target, 0, 0), b'\xff' * 2 * slot)
ctx = tg.Context(spec['cpu_hz'], 0, 0, b'\xff' * 2 * slot, left, {}, [])
result = tg.grade_case(case, tg.observe(log, spec['sys_hz'], spec['cpu_hz']), ctx, None)
print('PROBE guard result:', json.dumps(result))
caught = not result['passed'] and any(
    'escaped' in f or 'device saw' in f or 'testbench' in f for f in result['findings'])
print('PROBE', 'CAUGHT' if caught else 'ESCAPED')
sys.exit(0 if caught else 1)
