#!/usr/bin/env python3
"""statement_survey.py TREE: every cost a stated table of the CPU budget harness states at 1x1/1if and 8x8/2if, each
table's figure beside every other's for the same cost, and each documented derivation held to its source (#871 round 6,
from R821-5 F1: one item stated twice with two values). The tables: load_grade's STATED_US (the pin's column) and
STATED_US_DONOR (GRADED, the donor's), poll_grade.STATED_US, the pass costs ctrl_loop.h states (load_grade.macros) and
whole_grade.stated_us reads, rows_grade.ROW_COSTS, rows_tiers' DATAPATH_US, LONG_NOTICE_US and LONG_RECORD_US,
edit_rows' PACED and EDIT_RECORD_US. The derivations the tables document: a retained record's retry at the SRP record's
cost (poll_grade), the SRP drain's unit at the load gate's record.srp, the dearer column's (ctrl_loop.h), the longest
notice at the polls' aecp_long (rows_tiers), the paced class the dearer of its members (edit_rows).
Prints every cost with more than one value. The donor column (STATED_US_DONOR) is measured on the donor's image
(tsn-c-stack#32), every other table on the pin's, so a figure only the donor column gives differently is reported as
the two images'; any two values among the pin's tables is a conflict, as is a derivation that does not hold. Exits 1 on
a conflict."""
import re
import sys
from collections import defaultdict
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import edit_rows  # noqa: E402
import load_grade  # noqa: E402
import poll_grade  # noqa: E402
import rows_grade  # noqa: E402
import rows_tiers  # noqa: E402
import whole_grade  # noqa: E402

COLUMNS = ('load_grade.STATED_US', 'load_grade.STATED_US_DONOR')
POLL_NAME = {'base': 'base', 'aecp': 'item.aecp.notice'}
WHOLE_NAME = {'build': 'build', 'build-one': 'build_one', 'step': 'step'}
bad = 0
for point in ('1x1/1if', '8x8/2if'):
    n_if = load_grade.POINTS[point]['n_if']
    said = defaultdict(dict)
    for name, table in zip(COLUMNS, (load_grade.STATED_US, load_grade.STATED_US_DONOR)):
        for key, value in table[point].items():
            said[key][name] = value
    for key, value in poll_grade.stated_us(n_if).items():
        said[POLL_NAME.get(key, f'item.{key}')][f'poll_grade.STATED_US[{n_if}]'] = value
    h = load_grade.macros(tree, n_if)
    for key, macro in (('build', 'CTRL_LOOP_BUILD_PASS_US'), ('build_one', 'CTRL_LOOP_BUILD_ONE_PASS_US'),
                       ('step', 'CTRL_LOOP_STEP_PASS_US')):
        said[key][f'ctrl_loop.h {macro}'] = h[macro]
    for kind, value in whole_grade.stated_us(n_if).items():
        said[WHOLE_NAME.get(kind, kind)][f'whole_grade.stated_us({n_if})'] = value
    for key, value in rows_grade.ROW_COSTS[point].items():
        said[key]['rows_grade.ROW_COSTS'] = value
    for kind, value in rows_tiers.DATAPATH_US[point].items():
        said[f'event.{kind}']['rows_tiers.DATAPATH_US'] = value
    said['item.aecp_long']['rows_tiers.LONG_NOTICE_US'] = rows_tiers.LONG_NOTICE_US[point]
    said['record.aecp, the largest legal command']['rows_tiers.LONG_RECORD_US'] = rows_tiers.LONG_RECORD_US[point]
    for member, value in edit_rows.PACED[point].items():
        said[f'paced: {member}']['edit_rows.PACED'] = value
    said['the paced class']['edit_rows.EDIT_RECORD_US'] = edit_rows.EDIT_RECORD_US[point]
    print(f'== {point}: {len(said)} costs, {sum(len(v) for v in said.values())} statements')
    for key in sorted(said):
        values = said[key]
        if len(set(values.values())) > 1:
            pin = {v for k, v in values.items() if k != COLUMNS[1]}
            donor_only = len(pin) <= 1
            print(f'  TWO VALUES {key}: ' + ', '.join(f'{k} {v}' for k, v in sorted(values.items()))
                  + ("  (the donor column's own image)" if donor_only else '  CONFLICT among the pin\'s tables'))
            bad += not donor_only
    header = (tree / 'sw/firmware/ctrl/loop/ctrl_loop.h').read_text()
    unit = re.search(r'#define CTRL_LOOP_SRP_UNIT_US \(MBX_N_IF == 1u \? (\d+)u : (\d+)u\)', header)
    h['CTRL_LOOP_SRP_UNIT_US'] = int(unit[1] if n_if == 1 else unit[2])
    srp = max(t[point]['record.srp'] for t in (load_grade.STATED_US, load_grade.STATED_US_DONOR))
    checks = [
        ("a retained record's retry at the SRP record's cost (poll_grade's docstring)",
         poll_grade.stated_us(n_if)['retained'], srp),
        ("load_grade's item.retained at the SRP record's cost, the pin column",
         load_grade.STATED_US[point]['item.retained'], load_grade.STATED_US[point]['record.srp']),
        ("load_grade's item.retained at the SRP record's cost, the donor column",
         load_grade.STATED_US_DONOR[point].get('item.retained', srp), load_grade.STATED_US_DONOR[point]['record.srp']),
        ("ctrl_loop.h's CTRL_LOOP_SRP_UNIT_US at the dearer column's record.srp", h.get('CTRL_LOOP_SRP_UNIT_US'), srp),
        ("rows_tiers.LONG_NOTICE_US at the polls' aecp_long", rows_tiers.LONG_NOTICE_US[point],
         poll_grade.stated_us(n_if)['aecp_long']),
        ("edit_rows.EDIT_RECORD_US the dearest paced member", edit_rows.EDIT_RECORD_US[point],
         max(edit_rows.PACED[point].values())),
    ]
    for what, got, want in checks:
        ok = got == want
        bad += not ok
        print(f'  DERIVATION {"holds" if ok else "FAILS"}: {what}: {got} (its source {want})')
print(f'RESULT: {"FAIL" if bad else "PASS"} ({bad} conflict(s))')
sys.exit(1 if bad else 0)
