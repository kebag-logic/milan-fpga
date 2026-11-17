"""Reviewer probe: falsification cases for the LeaveAll / run-out owner binding (mrpdu_grade.leave_alls, resolve).

Usage: python3 -I -B probe_owner.py <checkout>/tb/verilator/ctrl_service_budget
Builds synthetic held-group logs through the self-test's own log builder (selftest_leaveall.harness) and prints
each case's LeaveAll outcomes, failing run-outs and stated findings, with an expectation and OK/UNEXPECTED.
"""
import sys

sys.path.insert(0, sys.argv[1])
import selftest  # noqa: E402
import selftest_leaveall as sl  # noqa: E402
import run  # noqa: E402

graded = sl.harness(selftest.synthetic, selftest.SYS_HZ, selftest.CPU_HZ, selftest.tx_record)
MSRP, MVRP, LA, JOIN, PT = sl.MSRP, sl.MVRP, sl.LA, sl.JOIN, 'on_pt_timer'
bad = 0


def show(name, held, expect, ok):
    global bad
    misses = run.stated_misses([dict(group=name, passes=dict(joins=held))])
    print(f"{'OK' if ok else 'UNEXPECTED'} {name}: leave_all={sl.by(held)} runs="
          f"{ {k: v for k, v in held['runs'].items() if v} } expect: {expect}")
    for m in misses:
        print(f"    STATED {m}")
    bad += not ok


# A. The traces' shape: two expiries 400 ms apart, each owner's LeaveAll at once; then the owners swapped.
sends = ((1_000, MSRP, False, 0), (1_010, MVRP, False, 0), (1_051, MSRP, True, 0), (1_451, MVRP, True, 0))
_, a = graded(sends, ((1_050, LA, 'if0 MSRP'), (1_450, LA, 'if0 MVRP')), ordinary=(1_500,))
show('A-true-owners', a, "sent 2", sl.by(a) == {'sent': 2} and not a['leave_all']['failing'])
_, a2 = graded(sends, ((1_050, LA, 'if0 MVRP'), (1_450, LA, 'if0 MSRP')), ordinary=(1_500,))
show('A-swapped-owners', a2, "both fail (owner's LeaveAll 400 ms away)",
     len(a2['leave_all']['failing']) == 2)
# B. Interface 1's MSRP expiry, interface 0's MSRP LeaveAll at once, interface 1 silent afterwards.
_, b = graded(((1_000, MSRP, False, 1), (1_000, MSRP, False, 0), (1_051, MSRP, True, 0)),
              ((1_050, LA, 'if1 MSRP'),), ordinary=(1_400,))
show('B-other-interface-answers', b, "absent for if1 MSRP", sl.by(b) == {'absent': 1})
# C. An owner recorded that never sent anything and stays silent: absent, named.
_, c = graded(((1_000, MSRP, False, 0), (1_051, MSRP, True, 0)), ((1_050, LA, 'if0 MVRP'),), ordinary=(1_400,))
show('C-silent-owner', c, "absent for if0 MVRP", sl.by(c) == {'absent': 1})
# D. Two expiries of one owner before its opportunity, one LeaveAll: informative (both answered by it).
_, d = graded(((1_000, MSRP, False, 0), (1_181, MSRP, True, 0)),
              ((1_050, LA, 'if0 MSRP'), (1_060, LA, 'if0 MSRP'), (1_180, JOIN, 'if0 MSRP')))
show('D-double-expiry-one-LeaveAll', d, "informative: sent 2", True)
# E. A periodic run-out owned by MVRP whose build sends nothing, MSRP's join timer still running: not held by MSRP's.
_, e = graded(((1_000, MSRP, False, 0), (1_250, MSRP, False, 0)), ((1_300, PT, 'if0 MVRP'),), (), (1_460,))
show('E-empty-build-other-participant-running', e, "late (MVRP's own opportunity is its run-out)",
     [f['outcome'] for f in e['failing']] == ['late'])
# F. Same, owned by MSRP whose own join timer runs to 1,430 ms: held, empty.
_, f = graded(((1_000, MSRP, False, 0), (1_250, MSRP, False, 0)), ((1_300, PT, 'if0 MSRP'),), (), (1_460,))
show('F-empty-build-own-running', f, "empty, no failure", not f['failing'] and f['runs']['empty'] == 1)
# G. Join run-out with an owner text the testbench never prints for a bound owner ('unresolved' + arg): unowned.
_, g = graded(((1_000, MSRP, False, 0), (1_191, MSRP, False, 0)), ((1_190, JOIN, 'unresolved 10008ca0'),))
show('G-join-unresolved', g, "unowned, named", [x['outcome'] for x in g['failing']] == ['unowned'])
# H. A LeaveAll expiry with an owner and a later expiry with none: the owned one stays sent, the other unowned.
_, h = graded(((1_000, MSRP, False, 0), (1_051, MSRP, True, 0), (1_451, MVRP, True, 0)),
              ((1_050, LA, 'if0 MSRP'), (1_450, LA, None)), ordinary=(1_500,))
show('H-mixed-owned-unowned', h, "sent 1, unowned 1", sl.by(h) == {'sent': 1, 'unowned': 1})
print(f"probe: {bad} unexpected")
sys.exit(1 if bad else 0)
