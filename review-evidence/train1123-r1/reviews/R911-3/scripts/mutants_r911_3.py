"""Reviewer mutants of kept_grade's slice classification at the fixed head (in-memory monkeypatches, no file changed).

usage: python3 -I -B mutants_r911_3.py <repo-root>
Each mutant replaces kept_grade.transmit_slices (or Disposition.owes) and runs kept_grade.selftest(); a mutant the
self-test should catch must make at least one check fail.
  frame-count-only   the prior head's rule: a build slice is 'build-one' wherever it holds at most one SRP frame
  no-round-filter    'build-one' where at most one SRP frame and not an aged step, round work ignored
  no-aged-filter     'build-one' where at most one SRP frame and the round idle, aged steps ignored
  any-over-kind      'build-one' wherever whole_grade.held puts the pass in 'over', whatever its kind
  all-build-one      every build slice over the limit is 'build-one'
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).resolve() / 'tb/verilator/ctrl_service_budget'))
import kept_grade as k  # noqa: E402
import scenario  # noqa: E402
import slice_grade  # noqa: E402
import whole_grade  # noqa: E402


def run(name, target, attr, value):
    saved = getattr(target, attr)
    setattr(target, attr, value)
    try:
        checks = k.selftest()
    finally:
        setattr(target, attr, saved)
    failed = [what for what, ok, _ in checks if not ok]
    print(f'{name}: {len(failed)} of {len(checks)} checks fail')
    for what in failed:
        print(f'    - {what}')
    return len(failed)


def classed(keep):
    def transmit(log, shape):
        srp = scenario.CH['srp']
        frames = sorted(c for c, ch, _ in log.commits if ch == srp)
        aged = {start for _, start, _, _, was in log.stepped if was}
        idle = {p.start_sys for p in log.passes if whole_grade.round_idle(p.modules)}
        out = {'build': set(), 'build-one': set()}
        for o in slice_grade.held(log, shape)['over']:
            if o['kind'] == 'build':
                end = o['start_sys'] + o['cycles'] * log.sys_hz // log.cpu_hz
                one = keep(o, whole_grade.within(frames, o['start_sys'], end), o['start_sys'] in idle,
                           o['start_sys'] in aged, log, shape)
                out['build-one' if one else 'build'].add(o['cycles'])
        return out
    return transmit


def any_over(o, n, idle, aged, log, shape):
    return o['start_sys'] in {x['start_sys'] for x in whole_grade.held(log, shape)['over']}


MUTANTS = [
    ('frame-count-only', classed(lambda o, n, idle, aged, log, shape: n <= 1)),
    ('no-round-filter', classed(lambda o, n, idle, aged, log, shape: n <= 1 and not aged)),
    ('no-aged-filter', classed(lambda o, n, idle, aged, log, shape: n <= 1 and idle)),
    ('any-over-kind', classed(any_over)),
    ('all-build-one', classed(lambda o, n, idle, aged, log, shape: True)),
]

base = [w for w, ok, _ in k.selftest() if not ok]
print(f'unpatched: {len(base)} fail')
survived = [name for name, fn in MUTANTS if run(name, k, 'transmit_slices', fn) == 0]
print(f'survivors: {survived or "none"}')
