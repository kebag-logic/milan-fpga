#!/usr/bin/env python3
"""Independent boundary probes of the paired budget grader, using synthetic logs.
Usage: python3 -I probe_kept_grade.py CHECKOUT PACKET
Each synthetic input and raw CLI result is retained under receipts/grader-probes.
"""
import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys

root, packet = (Path(p).resolve() for p in sys.argv[1:])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import grade
import kept_grade as kg
import mrpdu_grade
import shape_costs
import whole_grade

out = packet / 'receipts' / 'grader-probes'
out.mkdir(parents=True, exist_ok=True)
work = packet / 'scratch' / 'grader-probes'
work.mkdir(parents=True, exist_ok=True)
shape = shape_costs.of_point('1x1/1if')
hz = 100_000_000
spec = dict(shape='endstation_ax7101_1x1_tdm8', interfaces=1, sys_hz=hz, cpu_hz=hz)
(work / 'build.json').write_text(json.dumps(spec))

def lines(kind, cycles, work_cycles=10000):
    probes = ['srp.bound_advertise.if0'] if kind == 'srp-bound' else [
        'srp.kept_advertise.if0', 'srp.kept_recount.if0', 'srp.kept_failed.if0']
    result = []
    for k, probe in enumerate(probes):
        start = (k + 1) * 1_000_000
        result += [f'MARK {start} {probe}', f'SPAN {start+100} {start+100} {cycles} 00002000 srp_mbx:receive']
    return '\n'.join(result + [f'PASS 0 5000000 5000000 {work_cycles}', 'SUMMARY passes=1', 'RESULT: PASS']) + '\n'

clean = {name: lines(name, 20000 if name == 'srp-kept' else 25000) for name in kg.OWED_KINDS}
parsed = {name: grade.parse(text, hz, hz) for name, text in clean.items()}
results = {name: dict(group=name, passes=dict(share=grade.pass_share(log))) for name, log in parsed.items()}
checks = []
def check(name, ok, detail):
    checks.append((name, ok, detail))
    print(f'{"PASS" if ok else "FAIL"} {name}: {detail}', flush=True)

for name, ok, detail in kg.selftest():
    check('repository selftest: ' + name, ok, detail)

build_log = copy.deepcopy(parsed['srp-kept'])
cost = whole_grade.held(build_log, shape)['limits']['build-one']
build_log.passes = [grade.Pass(0, 5000000, 5000000, cost+1, {}, [], {})]
build_log.entries = [(5000001, mrpdu_grade.BUILD)]
found = kg.held(build_log, parsed['srp-bound'], shape, [], [])[2]
check('build-one one cycle over cost', bool(found) and 'build-one' in found[0], found)

for name in kg.OWED_KINDS:
    (work / f'{name}.log').write_text(clean[name])
single = kg.Disposition([results['srp-kept']], work, spec)
check('only one group graded', bool(single.findings), single.findings)
pair = kg.Disposition(list(results.values()), work, spec)
stated = ['srp-kept: an SRP record\'s apply of 40000 CPU cycles, over its stated 28500',
          'srp-bound: a walk item of 15000 CPU cycles, over its stated 12000']
check('named and linked OWED disposition', pair.stated(stated) == [] and len(pair.owed) == 2 and
      all('#977' in x and '/issues/977' in x for x in pair.owed), pair.owed)

idle_log = copy.deepcopy(parsed['srp-kept'])
idle_log.idle = [(4000000, 4000000, 250000)]
idle_result = dict(passes=dict(share=grade.pass_share(idle_log)))
try:
    work_over = kg.over_share(idle_result)
    check('valid idle-only over-share row', work_over == [], work_over)
except KeyError as error:
    check('valid idle-only over-share row', False, f'KeyError: {error}; idle rows use idle_run, not start_sys')

# An actual over-share work pass in the log. A complete grade detects it; the empty/incomplete grade probes test
# whether the standalone gate distinguishes "no evidence of grading" from "graded and no over-share pass".
over = dict(clean, **{'srp-kept': lines('srp-kept', 20000, 250000)})
for label in ('complete-clean', 'complete-over-share', 'missing-json', 'empty-json', 'missing-share'):
    inputs = clean if label == 'complete-clean' else over
    case = out / label
    case.mkdir(exist_ok=True)
    for name, text in inputs.items():
        (case / f'{name}.log').write_text(text)
        data = dict(group=name, passes=dict(share=grade.pass_share(grade.parse(text, hz, hz))))
        if name == 'srp-kept' and label == 'empty-json':
            data = {}
        elif name == 'srp-kept' and label == 'missing-share':
            data = dict(group=name, passes={})
        dest = case / f'{name}.json'
        if name == 'srp-kept' and label == 'missing-json':
            dest.unlink(missing_ok=True)
        else:
            dest.write_text(json.dumps(data, indent=2) + '\n')
    proc = subprocess.run([sys.executable, '-I', str(root / 'tb/verilator/ctrl_service_budget/kept_grade.py'),
                           str(work), '--results', str(case)], capture_output=True, text=True)
    (case / 'stdout.txt').write_text(proc.stdout)
    (case / 'stderr.txt').write_text(proc.stderr)
    (case / 'rc.txt').write_text(f'{proc.returncode}\n')
    expected = 0 if label == 'complete-clean' else 1
    check(label, proc.returncode == expected, f'expected rc={expected}, observed rc={proc.returncode}')

(out / 'SUMMARY.txt').write_text('\n'.join(f'{"PASS" if ok else "FAIL"} {name}: {detail}'
                                          for name, ok, detail in checks) + '\n')
sys.exit(int(any(not ok for _, ok, _ in checks)))
