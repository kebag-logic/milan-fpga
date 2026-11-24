"""Reviewer mutants of kept_grade's round-3 slice disposition (in-memory monkeypatches, no file is changed).

usage: python3 -I -B mutants_r911_2.py <repo-root>
  drop-fail-closed   owes() drops `cycles not in slices['build']`: an equal-length build of one and whole pass
                     would owe the whole pass's slice line. Does the self-test catch it?
  idle-filtered      transmit_slices classes a build slice 'build-one' only where whole_grade.held would (round idle,
                     not an aged step), else 'build': the stricter reading. Does the self-test stay green?
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


def owes_no_fail_closed(self, line):
    if self.findings:
        return False
    if line.startswith(f'{k.kept_window.BOUND}: {k.TRANSMIT_SLICE}'):
        return k.kept_window.BOUND in self.ran and k.stated_cycles(line) in self.slices['build-one']
    return any(line.startswith(f'{n}: {kind}') for n, kinds in k.OWED_KINDS.items() for kind in kinds
               if n in self.ran)


def idle_filtered(log, shape):
    srp = scenario.CH['srp']
    frames = sorted(c for c, ch, _ in log.commits if ch == srp)
    aged = {start for _, start, _, _, was in log.stepped if was}
    idle = {p.start_sys for p in log.passes if whole_grade.round_idle(p.modules) and p.start_sys not in aged}
    out = {'build': set(), 'build-one': set()}
    for o in slice_grade.held(log, shape)['over']:
        if o['kind'] == 'build':
            end = o['start_sys'] + o['cycles'] * log.sys_hz // log.cpu_hz
            one = o['start_sys'] in idle and whole_grade.within(frames, o['start_sys'], end) <= 1
            out['build-one' if one else 'build'].add(o['cycles'])
    return out


base = [w for w, ok, _ in k.selftest() if not ok]
print(f'unpatched: {len(base)} fail')
run('drop-fail-closed', k.Disposition, 'owes', owes_no_fail_closed)
run('idle-filtered', k, 'transmit_slices', idle_filtered)
