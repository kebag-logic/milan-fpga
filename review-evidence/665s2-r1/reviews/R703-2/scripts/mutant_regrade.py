#!/usr/bin/env python3
"""Regrade real head logs under the reviewer's self-test-escaping grader mutants.

Usage: mutant_regrade.py SANDBOX_ROOT BUILD_DIR GROUP[,GROUP...]
For each mutant that escaped the harness self-test (review_mutants.py), apply it to a
fresh copy of the head's harness in the sandbox, grade the named groups' logs from
BUILD_DIR/results with the copy, and report which published figures change.
Each mutant runs in a fresh interpreter so no module state leaks between them.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from review_mutants import MUTANTS  # noqa: E402

KEYS = ('status', 'start_sys', 'end_sys', 'ms', 'within_t_svc', 'within_ceiling', 'bound_ms')
CHILD = r'''
import json, sys
from pathlib import Path
here = Path(sys.argv[1]); build = Path(sys.argv[2]); groups = sys.argv[3].split(',')
sys.path.insert(0, str(here))
import grade, scenario
spec = json.loads((build / 'build.json').read_text())
p = scenario.point('1x1' if spec['interfaces'] == 1 else '8x8', spec)
out = {}
for g in scenario.all_groups(p, spec):
    if g.name not in groups:
        continue
    try:
        r = grade.grade((build / 'results' / f'{g.name}.log').read_text(), g, spec['sys_hz'], spec['cpu_hz'])
    except grade.Refusal as e:
        out[g.name] = {'refused': str(e)[:200]}
        continue
    out[g.name] = dict(probes={x['probe']: {k: x.get(k) for k in %r} for x in r['probes']},
                       worst=r['passes']['worst'] and r['passes']['worst']['ms'],
                       composed=r['passes']['composed'] and r['passes']['composed']['ms'])
print(json.dumps(out))
''' % (KEYS,)


def graded(work: Path, build: Path, groups: str) -> dict:
    res = subprocess.run([sys.executable, '-B', '-c', CHILD, str(work), str(build), groups],
                         capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def main() -> int:
    root, build, groups = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
    orig = root / 'tb/verilator/ctrl_service_budget.orig'
    work = root / 'tb/verilator/ctrl_service_budget'
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(orig, work)
    base = graded(work, build, groups)
    for ident, name, old, new, what in MUTANTS:
        if name != 'grade.py':
            continue
        shutil.rmtree(work, ignore_errors=True)
        shutil.copytree(orig, work)
        path = work / name
        path.write_text(path.read_text().replace(old, new))
        got = graded(work, build, groups)
        changes = []
        for g in base:
            if 'refused' in base[g] or 'refused' in got.get(g, {}):
                if base[g] != got.get(g):
                    changes.append(f'{g}: refusal changed')
                continue
            for field in ('worst', 'composed'):
                if base[g][field] != got[g][field]:
                    changes.append(f'{g} {field} {base[g][field]} -> {got[g][field]}')
            for probe, row in base[g]['probes'].items():
                new_row = got[g]['probes'].get(probe)
                for k in KEYS:
                    if new_row is None or row.get(k) != new_row.get(k):
                        changes.append(f'{probe} {k} {row.get(k)} -> {None if new_row is None else new_row.get(k)}')
        print(f'{ident} {what}: {len(changes)} published values change' + ''.join(f'\n    {c}' for c in changes[:6]))
    shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
