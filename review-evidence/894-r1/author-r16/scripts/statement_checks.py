#!/usr/bin/env python3
"""Every statement check the CPU budget model holds the tree's stated figures to, at both points, each printed with
what it returned (an empty list is the check passing). Run from the tree's top.
- rows_tiers: tx_statements (CTRL_LOOP_TX_BOUND_MS and CTRL_LOOP_TX_MS against the built design's tx row), unrowed
  (every served channel has a row) and findings (every row against its bound; 8x8/2if's are reported by decision);
- queued_bound.statements (AECP_QUEUED_MS against the last queued notice's rule), paced_rows.statements
  (AECP_PACE_MS against choice) and paced_rows.count_findings (the pace's window counts);
- edit_rows.findings (the paced class against its members' records) at each point;
- load_grade: srp_unit (CTRL_LOOP_SRP_UNIT_US against record.srp), findings (each load against its ceiling) and held
  (the load and ceiling at each point and column), and the stated table at each point (load_grade.stated)."""
import sys
from pathlib import Path

HERE = Path('tb/verilator/ctrl_service_budget').resolve()
sys.path.insert(0, str(HERE))
import edit_rows  # noqa: E402
import load_grade  # noqa: E402
import paced_rows  # noqa: E402
import queued_bound  # noqa: E402
import rows_tiers  # noqa: E402


def show(name, value):
    print(f'{name}: {"[] (holds)" if value == [] else value}')


def main():
    root = Path('.').resolve()
    pts = rows_tiers.POINTS
    print(f'points: {", ".join(pts)}')
    for p in pts:
        show(f'rows_tiers.tx_statements({p})', rows_tiers.tx_statements(root, (p,)))
        show(f'rows_tiers.unrowed(BUILT, {p})', rows_tiers.unrowed(root, rows_tiers.BUILT, (p,)))
        show(f'rows_tiers.findings(BUILT, {p})', rows_tiers.findings(root, rows_tiers.BUILT, (p,)))
        show(f'edit_rows.findings({p})', edit_rows.findings(rows_tiers.point_inputs(root, p, None)))
    show(f'queued_bound.statements ({queued_bound.POINT})', queued_bound.statements(root))
    show('paced_rows.statements', paced_rows.statements(root))
    show('paced_rows.count_findings', paced_rows.count_findings())
    show('load_grade.srp_unit (both points)', load_grade.srp_unit(root))
    show('load_grade.findings (every point and column)', load_grade.findings(root))
    show('load_grade.held', load_grade.held(root))
    for p in pts:
        print(f'load_grade.stated({p}): {dict(sorted(load_grade.stated(root, p).items()))}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
