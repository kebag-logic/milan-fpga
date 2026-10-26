#!/usr/bin/env python3
"""Reviewer-owned source mutants of the budget grader at the round-2 head, each run against
the harness's own self-test (run.py --self-test must exit non-zero to count as caught).

Usage: review_mutants2.py SANDBOX_ROOT
SANDBOX_ROOT holds tb/verilator/ctrl_service_budget.orig (a copy of the head's harness) with
every other path symlinked to the checkout. R* are round 1's twelve mutants, re-anchored to the
refactored code with the same defect; N* are new plants in the clock ratio, the pass bound and
the composition. Each is one exact-text edit; an anchor that is not unique is reported, not run.
"""
import shutil
import subprocess
import sys
from pathlib import Path

G, R = 'grade.py', 'run.py'
MUTANTS = [
    ('R1', G, 'return -(-sys_cycles * self.log.cpu_hz // self.log.sys_hz)',
     'return sys_cycles * self.log.cpu_hz // self.log.sys_hz', 'clock ratio: CPU cycles rounded down'),
    ('R2', G, 'ms=round(grader.cpu_ms(top.cycles), 5)', 'ms=round(grader.ms(top.cycles), 5)',
     'clock ratio: composed-maximum ms from the bus clock'),
    ('R3', G, 'ms=round(grader.cpu_ms(worst.cycles), 5)', 'ms=round(grader.ms(worst.cycles), 5)',
     'clock ratio: worst-pass ms from the bus clock'),
    ('R4', G, '        return self.pass_end(taking) - self.pass_origin(start)',
     '        return taking.start_sys + taking.cycles - self.pass_origin(start)',
     'clock ratio: the pass bound treats CPU cycles as bus cycles'),
    ('R5', G, '                    hits.append(self.log.ms[deadline])',
     '                    hits.append(self.log.ms.get(deadline + 1, self.log.ms[deadline]))',
     'marker: a timer path starts one millisecond after its deadline'),
    ('R6', G, '    ceiling = scenario.CEILING_MS[probe.family] + probe.wait_ms',
     '    ceiling = scenario.CEILING_MS[probe.family]', 'deadline: the ceiling verdict drops the normative wait'),
    ('R7', G, '    check = wrong or expectation(grader, probe, i, start, next_mark)', '    check = wrong',
     'marker: the expected-response check is skipped'),
    ('R8', G, '    frame = pending.pop()\n', '    frame = pending.pop(0)\n',
     'marker: a receive commit is given to the oldest pending frame (round 1 planted the newest; the rule inverted)'),
    ('R9', G, '        return self.pass_end(taking) - self.pass_origin(start)',
     '        return self.pass_end(taking) - start', 'pass bound: starts at the input, not at the running pass'),
    ('R10', R, '    return 1 if misses and not args.record_budget_findings else 0', '    return 0',
     'deadline: a T_svc miss never fails the run'),
    ('R11', R, '    if refusals or not groups:\n        return 1\n', '    if not groups:\n        return 1\n',
     'a refused (unmeasured) probe does not fail the run'),
    ('R12', G, '    if log.traps:\n', '    if False:\n', 'a CPU trap or bus error is not refused'),
    # New plants: pass bound
    ('N1', G, '                return start - self.bus_cycles(p.idle_before)', '                return start',
     'pass bound: an idle pass running at the input is not charged'),
    ('N2', G, '        return self.pass_end(taking) - self.pass_origin(start)',
     '        return taking.start_sys - self.pass_origin(start)',
     'pass bound: ends at the taking pass\'s start, not its end'),
    ('N3', G, '                return start - self.bus_cycles(p.idle_before)',
     '                return start - p.idle_before', 'pass bound: the idle charge is in CPU cycles on the bus clock'),
    # New plants: clock ratio
    ('N4', G, '        return cpu_cycles * self.log.sys_hz // self.log.cpu_hz',
     '        return cpu_cycles * self.log.cpu_hz // self.log.sys_hz', 'clock ratio: bus cycles from CPU cycles inverted'),
    ('N5', G, '        return cpu_cycles * 1000.0 / self.log.cpu_hz', '        return cpu_cycles * 1000.0 / self.log.sys_hz',
     'clock ratio: cpu_ms on the bus clock (every pass figure)'),
    # New plants: composition
    ('N6', G, '    top = max(inside, key=lambda p: p.cycles)', '    top = inside[0]',
     'composition: the composed maximum is the window\'s first pass, not its longest'),
    ('N7', G, '    return [p for p in log.passes if start <= p.start_sys <= end]',
     '    return [p for p in log.passes if start <= p.start_sys <= end][:-1]',
     'composition: the window\'s last pass is dropped'),
    ('N8', G, '    if got != want:\n', '    if any(got[k] < want[k] for k in want):\n',
     'composition: a window that committed MORE than its load is accepted'),
    ('N9', G, "        if start <= c <= end and name in out:", "        if start <= c <= end and name in out and name != 'GM':",
     'composition: GM events are not counted in the population'),
    ('N10', G, '    worst = max(log.passes, key=lambda p: p.cycles, default=None)',
     '    worst = max(log.passes[:-1], key=lambda p: p.cycles, default=None)', 'worst pass: the last work pass is dropped'),
    ('N11', G, '    for c, ch, *_ in log.rxc:\n        if start <= c <= end:',
     '    for c, ch, *_ in log.rxc:\n        if start <= c < end:', 'composition: a commit at the window\'s end is not counted'),
    # Notification fan-out
    ('N12', G, "    return None if not cycles or None in cycles else max(cycles)",
     "    return None if not cycles else max((c for c in cycles if c is not None), default=None)",
     'notify: a missing recipient is skipped by the end rule (fan_out() still refuses)'),
    ('N13', G, '                if key not in found:\n                    unexpected.append(key)',
     '                if key not in found:\n                    pass',
     'notify: a recipient outside the set is not reported'),
]


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    orig = root / 'tb/verilator/ctrl_service_budget.orig'
    work = root / 'tb/verilator/ctrl_service_budget'
    escaped = 0
    for ident, name, old, new, what in MUTANTS:
        shutil.rmtree(work, ignore_errors=True)
        shutil.copytree(orig, work)
        path = work / name
        text = path.read_text()
        if text.count(old) != 1:
            print(f'{ident} ANCHOR-NOT-UNIQUE ({text.count(old)}) {what}')
            escaped += 1
            continue
        path.write_text(text.replace(old, new))
        result = subprocess.run([sys.executable, '-B', str(work / 'run.py'), '--self-test'],
                                capture_output=True, text=True)
        failed = [line for line in result.stdout.splitlines() if line.startswith(('FAIL', 'MUTANT ESCAPED'))]
        verdict = 'CAUGHT' if result.returncode else 'ESCAPED'
        escaped += verdict == 'ESCAPED'
        print(f'{ident} {verdict} rc={result.returncode} {what}' + (f' :: {failed[0][:160]}' if failed else ''))
    shutil.rmtree(work, ignore_errors=True)
    print(f'review mutants: {len(MUTANTS)} run, {escaped} escaped the self-test')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
