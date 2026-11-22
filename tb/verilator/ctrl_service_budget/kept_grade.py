# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The kept Talkers' records and builds held to their stated costs (#969; kept_window.py's srp-kept group).

Each SRP record of the group is a span of srp_mbx.c's record handler (receive, a SPAN line); each is held, by the
stated rule (its cycles at the CPU clock, plus 5 %, rounded up to 5 us; record_classes.rule), to ctrl_loop.h's
CTRL_LOOP_SRP_UNIT_US at the build's shape (shape_costs.at; THE SHAPES), the cost the slice starts a record at. Each
probe's records are those from its mark to the next mark. Each pass given whole to THE TRANSMIT's build, and each
build of one MRPDU, is held to its stated cost as whole_grade.py holds every group's (CTRL_LOOP_BUILD_PASS_US,
CTRL_LOOP_BUILD_ONE_PASS_US): the build that sends the participant's LeaveAll carries the kept attributes.

usage: python3 -I kept_grade.py <build-dir> [--results DIR] | --selftest
Exit 0 = every record and build within its stated cost; 1 = one over, or the group's log or a probe's record missing.
--selftest grades synthetic logs at 1x1/1if: records at the unit by the rule pass, one a cycle past it and a probe
with no record are each a finding, and a record is its own probe's, never an earlier mark's.
"""
from __future__ import annotations

import argparse
import json
import sys
from bisect import bisect_left
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import grade  # noqa: E402
import kept_window  # noqa: E402
import record_classes  # noqa: E402
import scenario  # noqa: E402
import shape_costs  # noqa: E402
import whole_grade  # noqa: E402

RECORD = 'srp_mbx:receive'
UNIT = 'CTRL_LOOP_SRP_UNIT_US'


def records(log: grade.Log) -> list[tuple[str, int, int]]:
    """Each SRP record of the log: the mark it follows, its bus cycle and its CPU cycles."""
    marks = sorted(log.marks)
    starts = [cycle for cycle, _ in marks]
    out = []
    for kind, *rest in log.traced:
        if kind == 'SPAN' and len(rest) >= 5 and rest[4] == RECORD:
            sys_start, cycles = int(rest[0]), int(rest[2])
            k = bisect_left(starts, sys_start + 1) - 1
            out.append((marks[k][1] if k >= 0 else '', sys_start, cycles))
    return out


def held(log: grade.Log, shape: shape_costs.Shape) -> tuple[list[str], list[str]]:
    """The report's lines and the findings: each probe's dearest record against the unit, and the builds'."""
    unit = shape_costs.at(shape, scenario.ROOT)[UNIT]
    lines, findings = [], []
    found = records(log)
    for probe in (name for _, name in sorted(log.marks) if name.startswith('srp.kept_')):
        mine = [cycles for mark, _, cycles in found if mark == probe]
        if not mine:
            findings.append(f'{probe}: no SRP record follows its mark')
            continue
        us = record_classes.rule(max(mine), log.cpu_hz)
        lines.append(f'RECORD {probe}: {len(mine)} record(s), the dearest {max(mine):,} CPU cycles, {us} us by the '
                     f'rule, against CTRL_LOOP_SRP_UNIT_US {unit} us')
        if us > unit:
            findings.append(f'{probe}: a record of {max(mine):,} cycles, {us} us by the rule, over the unit {unit} us')
    every = [cycles for _, _, cycles in found]
    if every:
        lines.append(f'RECORD the group: {len(every)} record(s), the dearest {max(every):,} CPU cycles, '
                     f'{record_classes.rule(max(every), log.cpu_hz)} us by the rule, against {unit} us')
    builds = whole_grade.held(log, shape)
    for kind in ('build', 'build-one'):
        lines.append(f'BUILD {kind}: the heaviest pass {builds["heaviest"][kind]:,} CPU cycles, against its stated '
                     f'{builds["limits"][kind]:,} ({whole_grade.COSTS[kind]})')
    findings += [f'a {o["kind"]} pass at bus cycle {o["start_sys"]}: {o["cycles"]:,} CPU cycles over its stated cost'
                 for o in builds['over'] if o['kind'] != 'step']
    return lines, findings


def selftest() -> list[tuple[str, bool, str]]:
    """Each control's outcome on a synthetic log at 1x1/1if and 100 MHz, the unit's edge from the rule."""
    shape, hz = shape_costs.of_point('1x1/1if'), 100_000_000
    unit = shape_costs.at(shape, scenario.ROOT)[UNIT]
    edge = next(c for c in range(unit * 100, 0, -1) if record_classes.rule(c, hz) <= unit)

    def graded(cycles: list[int | None]) -> list[str]:
        """The findings on a log of the three probes' marks, each followed by a record of those cycles, or none."""
        lines = []
        for k, (probe, c) in enumerate(zip(('srp.kept_advertise.if0', 'srp.kept_recount.if0',
                                            'srp.kept_failed.if0'), cycles)):
            at = 1_000_000 * (k + 1)
            lines.append(f'MARK {at} {probe}')
            if c is not None:
                lines.append(f'SPAN {at + 100} {at + 100} {c} 00002000 {RECORD}')
        text = '\n'.join([*lines, 'SUMMARY passes=1', 'RESULT: PASS']) + '\n'
        return held(grade.parse(text, hz, hz), shape)[1]
    within, over, missing = graded([edge, edge, 1_000]), graded([edge, edge + 1, 1_000]), graded([1_000, None, 1])
    return [(f'records at the unit by the rule ({edge:,} cycles, {unit} us) pass', within == [], str(within)),
            ('a record one cycle past it is a finding, its own probe\'s', len(over) == 1 and 'kept_recount' in over[0],
             str(over)),
            ('a probe with no record is a finding, the next probe\'s record not taken for it',
             len(missing) == 1 and 'kept_recount' in missing[0] and 'no SRP record' in missing[0], str(missing))]


def main(argv: list[str]) -> int:
    """Grade a build's srp-kept log, or run the self-test."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('build_dir', type=Path, nargs='?')
    parser.add_argument('--results', type=Path)
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args(argv)
    if args.selftest:
        checks = selftest()
        for what, ok, detail in checks:
            print(f'[{"ok" if ok else "FAIL"}] {what}' + ('' if ok else f': {detail}'))
        print(f'kept_grade selftest: {"PASS" if all(ok for _, ok, _ in checks) else "FAIL"}')
        return 0 if all(ok for _, ok, _ in checks) else 1
    if args.build_dir is None:
        parser.error('a build directory, or --selftest')
    spec = json.loads((args.build_dir / 'build.json').read_text())
    results = args.results or args.build_dir / 'results'
    path = results / f'{kept_window.NAME}.log'
    if not path.is_file():
        print(f'kept_grade: no {path.name} in the results: run.py --groups {kept_window.NAME} first')
        return 1
    log = grade.parse(path.read_text(errors='replace'), spec['sys_hz'], spec['cpu_hz'])
    shape = shape_costs.of_config(scenario.ROOT / 'configs' / f'{spec["shape"]}.yaml', spec['interfaces'],
                                  scenario.ROOT)
    lines, findings = held(log, shape)
    print(f'POINT {spec["shape"]}, {spec["interfaces"]} interface(s): shape {tuple(shape)}')
    print('\n'.join(lines))
    for finding in findings:
        print(f'FINDING {finding}')
    print(f'kept_grade: {"PASS" if not findings else "FAIL"} ({len(findings)} finding(s))')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
