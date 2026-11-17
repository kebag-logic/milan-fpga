#!/usr/bin/env python3
"""(Owned: each timer callback's ENTRY line names its owner, as the testbench of c10c549e prints it.) Probe of mrpdu_grade.leave_alls's attribution of LeaveAll timer run-outs to participants.

Builds synthetic held-group logs with the self-test's own helpers (selftest.synthetic, selftest.tx_record,
selftest_leaveall.mrpdu) and the same log shape as selftest_leaveall.leave_all_checks's `graded`, then prints how
join_grade.held / mrpdu_grade.leave_alls grade them.

Case A (control, the self-test's own skip): MSRP alone skips its LeaveAll at its first transmit opportunity.
Case B (probe): the same MSRP skip, and MVRP on the same interface whose own LeaveAll timer runs out between MSRP's
skipped opportunity and MVRP's join-timer run-out, MVRP sending its LeaveAll promptly at that run-out.
Case C (probe, empty build): a periodic timer run-out whose first build (a build_mrpdu entry with no TX record)
sends nothing, 60 ms after the run-out, with
another participant's join timer run-out 30 ms after the run-out.

Usage: leaveall_attribution_probe.py <harness dir: tb/verilator/ctrl_service_budget of the tree under review>
"""
import json
import sys
from pathlib import Path

harness = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(harness))
import grade  # noqa: E402
import join_grade  # noqa: E402
import mrpdu_grade  # noqa: E402
import scenario  # noqa: E402
import selftest  # noqa: E402
import selftest_leaveall as sl  # noqa: E402

SYS_HZ, CPU_HZ = selftest.SYS_HZ, selftest.CPU_HZ
MS, RATIO, SRP = SYS_HZ // 1000, SYS_HZ // CPU_HZ, scenario.CH['srp']
MSRP, MVRP = sl.MSRP, sl.MVRP


def graded(sends, timers, ordinary=(), end_ms=1_800, empty_builds=()):
    """selftest_leaveall's `graded`, its TICKs extended to end_ms."""
    lines, word = ['MARK 1000 save.change'], 0
    for at in range(900, end_ms + 1, 10):
        lines += [f'EVW {at * MS} {n} {w:08x}' for n, w in enumerate((mrpdu_grade.TICK, 1, 0, 0))]
    for at, kind, la in sends:
        frame = sl.mrpdu(kind, la)
        lines += selftest.tx_record(SRP, 0, frame, word, at * MS)
        word += 2 + (len(frame) + 3) // 4
    lines += [f'ENTRY {at * MS - 2000} build_mrpdu' for at, _, _ in sends]
    lines += [f'ENTRY {at * MS - 2000} build_mrpdu' for at in empty_builds]
    lines += [f'PASS {at} {at * MS - 3000} {(at * MS - 3000) // RATIO} {5000 // RATIO} instr=10'
              for at in sorted([at for at, _, _ in sends] + list(ordinary) + list(empty_builds))]
    lines += [f'ENTRY {at * MS + 100} {name} {who}' for at, name, who in timers]
    log = grade.parse(selftest.synthetic(lines), SYS_HZ, CPU_HZ)
    group = scenario.Group('probe', save=dict(loaded=True, origin='save.change'))
    return log, mrpdu_grade.rows(grade.Grader(log), group), join_grade.held(log)


def show(name, log, rows, held):
    alls = mrpdu_grade.leave_alls(log)
    print(f'== {name}')
    print('leave_alls:', json.dumps(alls, default=str))
    print('held.leave_all:', json.dumps(held['leave_all'], default=str))
    print('held.runs:', json.dumps(held.get('runs'), default=str), 'held.failing:', held.get('failing'))
    print('rows:', json.dumps([(r['probe'], r.get('ms')) for r in rows]))
    return alls, held


LA, JOIN, PT = 'on_la_timer', 'on_join_timer', 'on_pt_timer'
print('JOIN_CS', mrpdu_grade.JOIN_CS, 'LATE_MS', mrpdu_grade.LATE_MS)

# A: the self-test's own skip, MSRP alone
a = show('A control: MSRP skips its LeaveAll (the self-test case)',
         *graded(((1_000, MSRP, False), (1_181, MSRP, False), (1_371, MSRP, True)),
                 ((1_050, LA, 'if0 MSRP'), (1_180, JOIN, 'if0 MSRP'), (1_370, JOIN, 'if0 MSRP'))))

# B: the same MSRP skip; MVRP's commit at 1,010 arms its join timer to the 1,190 TICK; MVRP's LeaveAll timer runs
# out at 1,185 (after MSRP's skipped opportunity at 1,180/1,181) and MVRP sends its LeaveAll at 1,191
b = show('B probe: MSRP skips its LeaveAll while MVRP\'s LeaveAll timer runs out within its join time',
         *graded(((1_000, MSRP, False), (1_010, MVRP, False), (1_181, MSRP, False), (1_191, MVRP, True),
                  (1_371, MSRP, True)),
                 ((1_050, LA, 'if0 MSRP'), (1_180, JOIN, 'if0 MSRP'), (1_185, LA, 'if0 MVRP'), (1_190, JOIN, 'if0 MVRP'), (1_370, JOIN, 'if0 MSRP'))))

# C: a periodic run-out at 1,300 whose first build (no frame) runs 60 ms later, in the pass at 1,360; another
# participant's join timer callback at 1,330 between them. MSRP's last commit at 1,000 has long run its join timer out.
c = show('C probe: an empty build 60 ms after a periodic run-out, another join run-out 30 ms after it',
         *graded(((1_000, MSRP, False),), ((1_300, PT, 'if0 MSRP'), (1_330, JOIN, 'if0 MVRP')), ordinary=(1_400,), empty_builds=(1_360,)))
c0 = show('C0 control: the same empty build with no join run-out between',
          *graded(((1_000, MSRP, False),), ((1_300, PT, 'if0 MSRP'),), ordinary=(1_400,), empty_builds=(1_360,)))


def failing(held):
    return bool(held['leave_all'].get('failing')) or bool(held.get('failing'))


verdicts = {
    'A_control_skip_fails': failing(a[1]),
    'B_skip_with_other_participant_runout_fails': failing(b[1]),
    'C0_control_empty_late_fails': failing(c0[1]),
    'C_empty_late_with_other_join_fails': failing(c[1]),
}
print('VERDICTS', json.dumps(verdicts))
