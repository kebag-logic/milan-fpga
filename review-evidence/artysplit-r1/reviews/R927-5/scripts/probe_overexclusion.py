"""Disposable probe: plant an over-exclusion defect in egress_mii's held-egress marking (every record held) and
report which of the grade's own controls catch it. Usage: python3 -I -B probe_overexclusion.py <clone>"""
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(clone / 'tb/verilator/ctrl_service_budget'))
import egress_mii as m  # noqa: E402


def all_held(recs, windows, ends):
    """The defect: every record is left to the held-egress ledger, so the row grades nothing."""
    for r in recs:
        r.held = True


def first_held_only(recs, windows, ends):
    """A subtler defect: every record committed after the first is excluded."""
    for i, r in enumerate(sorted(recs, key=lambda x: x.commit)):
        r.held = i > 0


p = m.params(m.arty_spec())
for name, fn in (('all-held', all_held), ('all-but-first-held', first_held_only)):
    res = m.controls(p, {'mark': fn})
    caught = [c for c, ok in res if not ok]
    print(f'{"CAUGHT" if caught else "MISSED"} {name}' + (f': {"; ".join(caught)}' if caught else ''))
    # what the row would read on a synthetic unheld case under the defect
    quiet = (p.sr_period_ps * 8 + 20 * 10**6) // p.sys_ps
    log = m.testbench_log(p, [(quiet, 2, 1514), (quiet + 1, 2, 1514)])
    saved = m.mark_held
    m.mark_held = fn
    try:
        row = m.grade_case(log, p)
    finally:
        m.mark_held = saved
    ok, lines = m.verdict({'synthetic': row}, p)
    print(f'  synthetic two-frame case under {name}: wait_ps={row.get("wait_ps")} held={row.get("held")} verdict={"PASS" if ok else "FAIL"}')
print('shipping grade on the same synthetic case:', m.grade_case(m.testbench_log(p, [((p.sr_period_ps * 8 + 20 * 10**6) // p.sys_ps, 2, 1514), ((p.sr_period_ps * 8 + 20 * 10**6) // p.sys_ps + 1, 2, 1514)]), p).get('wait_ps'))
