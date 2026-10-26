#!/usr/bin/env python3
"""R703-1's twelve source mutants (scripts/review_mutants.py), applied to this round's harness.

Usage: review_mutants_r2.py SANDBOX_ROOT
SANDBOX_ROOT holds tb/verilator/ctrl_service_budget.orig (a copy of the head's harness) and
symlinks sw/ and configs/ to the checkout. Each mutant is the same defect as R703-1's, as one
exact-text edit of this round's source (the anchors moved with the code); the self-test
(run.py --self-test) must exit non-zero to count as caught. R8's defect is inverted: the
commit-to-frame rule is now "the newest pending frame" (KL_mbx_rx takes no byte of the next
frame before a verdict), so the defect planted is the oldest pending frame.
"""
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    ('R1', 'grade.py', 'return -(-sys_cycles * self.log.cpu_hz // self.log.sys_hz)',
     'return sys_cycles * self.log.cpu_hz // self.log.sys_hz', 'clock ratio: CPU cycles rounded down'),
    ('R2', 'grade.py', 'return dict(cycles=top.cycles, ms=round(grader.cpu_ms(top.cycles), 5),',
     'return dict(cycles=top.cycles, ms=round(top.cycles * 1000.0 / grader.log.sys_hz, 5),',
     'clock ratio: composed-maximum ms from the bus clock'),
    ('R3', 'grade.py', 'worst=dict(cycles=worst.cycles, ms=round(grader.cpu_ms(worst.cycles), 5),',
     'worst=dict(cycles=worst.cycles, ms=round(worst.cycles * 1000.0 / sys_hz, 5),',
     'clock ratio: worst-pass ms from the bus clock'),
    ('R4', 'grade.py', '        return self.pass_end(taking) - self.pass_origin(start)',
     '        return taking.start_sys + taking.cycles - self.pass_origin(start)',
     'clock ratio: the pass bound treats CPU cycles as bus cycles'),
    ('R5', 'grade.py', '                    hits.append(self.log.ms[deadline])',
     '                    hits.append(self.log.ms.get(deadline + 1, self.log.ms[deadline]))',
     'marker: a timer path starts one millisecond after its deadline'),
    ('R6', 'grade.py', '    ceiling = scenario.CEILING_MS[probe.family] + probe.wait_ms',
     '    ceiling = scenario.CEILING_MS[probe.family]', 'deadline: the ceiling verdict drops the normative wait'),
    ('R7', 'grade.py', '    check = wrong or expectation(grader, probe, i, start, next_mark)',
     '    check = wrong', 'marker: the expected-response check is skipped'),
    ('R8', 'grade.py', '    frame = pending.pop()\n', '    frame = pending.pop(0)\n',
     'marker: a receive commit is given to the oldest pending frame (R8 inverted)'),
    ('R9', 'grade.py', '            if p.start_sys <= start < self.pass_end(p):\n                return p.start_sys\n',
     '            if p.start_sys <= start < self.pass_end(p):\n                return start\n',
     'pass bound: starts at the input, not at the running pass'),
    ('R10', 'run.py', '    return 1 if misses and not args.record_budget_findings else 0',
     '    return 0', 'deadline: a T_svc miss never fails the run'),
    ('R11', 'run.py', '    if refusals or not groups:\n        return 1\n', '    if refusals or not groups:\n        return 0\n',
     'a refused (unmeasured) probe does not fail the run'),
    ('R12', 'grade.py', "    if log.traps:\n", "    if False:\n", 'a CPU trap or bus error is not refused'),
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
    return 1 if escaped else 0


if __name__ == '__main__':
    raise SystemExit(main())
