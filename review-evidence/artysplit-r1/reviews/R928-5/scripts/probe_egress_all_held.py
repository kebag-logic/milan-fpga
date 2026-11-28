#!/usr/bin/env python3
"""Confirm or refute the prior public finding that the egress grade's controls miss an over-exclusion defect:
mark_held replaced by one that leaves every record to the ledger.

usage: python3 -B probe_egress_all_held.py SOURCE
"""
import sys
from pathlib import Path


def main(source: Path) -> int:
    sys.path.insert(0, str(source / 'tb/verilator/ctrl_service_budget'))
    import egress_mii as em
    p = em.params(em.arty_spec())

    def all_held(recs, windows, ends):
        for r in recs:
            r.held = True

    failed = [name for name, ok in em.controls(p, dict(mark=all_held)) if not ok]
    print('all-held plant:', f'CAUGHT by {failed}' if failed else 'MISSED (every control still holds)')
    quiet = (p.sr_period_ps * 8 + 20 * 10**6) // p.sys_ps
    log = em.testbench_log(p, [(quiet, 2, 550), (quiet + 1, 2, 550)])
    shipped = em.grade_case(log, p)
    saved = em.mark_held
    em.mark_held = all_held
    try:
        planted = em.grade_case(log, p)
        ok, _ = em.verdict({'unheld': planted}, p)
    finally:
        em.mark_held = saved
    print(f'two unheld 550-byte frames: shipped wait_ps={shipped["wait_ps"]} held={shipped["held"]}; '
          f'planted wait_ps={planted["wait_ps"]} held={planted["held"]} verdict={"PASS" if ok else "FAIL"}')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
