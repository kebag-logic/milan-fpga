# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The records that register Talkers, the kept Talkers' (#969) and the bound ones the base makes, owed to #977
(kept_window.py's srp-kept and srp-bound groups).

Each SRP record is a span of srp_mbx.c's record handler (receive, a SPAN line), and each probe's records are those
from its mark to the next mark. A record that registers more than one or two Talkers is past ctrl_loop.h's
CTRL_LOOP_SRP_UNIT_US (by the stated rule: its cycles at the CPU clock, plus 5 %, rounded up to 5 us;
record_classes.rule) on the bound path the base has, a bridge re-declaring the bound Talkers after any LeaveAll, and
the kept Talkers make the same registrations before the bindings. That cost is #977's, owed and never restated here
(the owner's ruling on #969, 2026-11-22: DISPOSITION). So each record of either group over the unit, each of their
tier-2 slices of SRP's records over the slice, and the bound group's walk, polls base and passes over THE SHARE that
its registrations make are each named OWED #977, never a pass, while all of these hold, each a finding otherwise:

  kept <= bound   every srp-kept probe's dearest record costs no more than the dearest srp-bound record of its
                  interface on the same image (the same MRPDU, its inputs unbound and bound);
  the share       no work pass of srp-kept is over THE SHARE (share.py, 2 ms);
  the builds      every pass of either group given whole to THE TRANSMIT's build, and every build of one MRPDU, is
                  within its stated cost (whole_grade.held; CTRL_LOOP_BUILD_PASS_US, CTRL_LOOP_BUILD_ONE_PASS_US);
  the records     every probe of both groups has its record, and both groups are graded together.

run.py applies the same disposition to its STATED and SHARE lines (Disposition): with every condition held, the
owed ones are printed OWED and fail nothing; otherwise each stays a failure and each finding is one more.

usage: python3 -I kept_grade.py <build-dir> [--results DIR] | --selftest
Exit 0 = every condition held; 1 = a finding, or a group's log missing.
--selftest grades synthetic logs at 1x1/1if: each condition's breach is a finding of its own, the unit's overrun
alone is owed, and a record is its own probe's, never an earlier mark's.
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
#: The owner's disposition of the registration cost (#969's STOP of round 2, ruled 2026-11-22, option 1).
DISPOSITION = '#977 (https://github.com/kebag-logic/milan-fpga/issues/977)'
#: run.py's STATED lines the registrations make, each group's (run.stated_misses' words), owed while held.
OWED_KINDS = {kept_window.NAME: ("an SRP record's apply of ", "a tier-2 slice of SRP's records of "),
              kept_window.BOUND: ("an SRP record's apply of ", "a tier-2 slice of SRP's records of ",
                                  "a walk item of ", "a pass's polls base of ")}


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


def dearest(log: grade.Log, prefix: str) -> dict[str, int | None]:
    """Each probe of the log whose name starts with prefix, its dearest record's CPU cycles, None for none."""
    found = records(log)
    out: dict[str, int | None] = {}
    for _, probe in sorted(log.marks):
        if probe.startswith(prefix):
            mine = [cycles for mark, _, cycles in found if mark == probe]
            out[probe] = max(mine) if mine else None
    return out


def held(kept: grade.Log, bound: grade.Log, shape: shape_costs.Shape,
         kept_shares: list[tuple[int, int]], bound_shares: list[tuple[int, int]]) -> tuple[list[str], list[str],
                                                                                            list[str]]:
    """The report's lines, the owed lines and the findings of both groups' logs on one image, with each group's
    work passes over THE SHARE (bus cycle, CPU cycles)."""
    unit = shape_costs.at(shape, scenario.ROOT)[UNIT]
    lines, owed, findings = [], [], []
    k_rec, b_rec = dearest(kept, 'srp.kept_'), dearest(bound, 'srp.bound_')
    for name, recs in ((kept_window.NAME, k_rec), (kept_window.BOUND, b_rec)):
        if not recs:
            findings.append(f'{name}: none of its probes ran')
        for probe, cycles in recs.items():
            if cycles is None:
                findings.append(f'{probe}: no SRP record follows its mark')
                continue
            us = record_classes.rule(cycles, kept.cpu_hz)
            lines.append(f'RECORD {probe}: the dearest {cycles:,} CPU cycles, {us} us by the rule, against {UNIT} '
                         f'{unit} us')
            if us > unit:
                owed.append(f'{probe}: a record of {cycles:,} CPU cycles, {us} us by the rule, over {UNIT} {unit} us, '
                            f'owed to {DISPOSITION}')
    for probe, cycles in k_rec.items():
        mate = b_rec.get(f'srp.bound_advertise.{probe.rpartition(".")[2]}')
        if cycles is None or mate is None:
            continue
        lines.append(f'KEPT <= BOUND {probe}: {cycles:,} against {mate:,} CPU cycles')
        if cycles > mate:
            findings.append(f'{probe}: kept <= bound broken, {cycles:,} CPU cycles against the bound record\'s '
                            f'{mate:,}')
    findings += [f'{kept_window.NAME}: a work pass of {cycles:,} CPU cycles at bus cycle {at} over THE SHARE'
                 for at, cycles in kept_shares]
    owed += [f'{kept_window.BOUND}: a work pass of {cycles:,} CPU cycles at bus cycle {at} over THE SHARE, the '
             f'bound path\'s registrations, owed to {DISPOSITION}' for at, cycles in bound_shares]
    for name, log in ((kept_window.NAME, kept), (kept_window.BOUND, bound)):
        builds = whole_grade.held(log, shape)
        for kind in ('build', 'build-one'):
            lines.append(f'BUILD {name} {kind}: the heaviest pass {builds["heaviest"][kind]:,} CPU cycles, against '
                         f'its stated {builds["limits"][kind]:,} ({whole_grade.COSTS[kind]})')
        findings += [f'{name}: a {o["kind"]} pass at bus cycle {o["start_sys"]}: {o["cycles"]:,} CPU cycles over its '
                     f'stated cost' for o in builds['over'] if o['kind'] != 'step']
    return lines, owed, findings


def over_share(result: dict | None) -> list[tuple[int, int]]:
    """A graded group's work passes over THE SHARE (grade.pass_share), (bus cycle, CPU cycles) each."""
    share = (result or {}).get('passes', {}).get('share') or {}
    return [(o['start_sys'], o['cycles']) for o in share.get('over_passes', [])]


class Disposition:
    """run.py's: the STATED and SHARE lines #977 owes, each printed OWED and failing nothing while kept_grade's
    conditions hold on this run's logs of both groups; otherwise every one stays a failure, with each finding."""

    def __init__(self, results: list[dict], out: Path, spec: dict) -> None:
        by = {g['group']: g for g in results}
        self.ran = [name for name in OWED_KINDS if name in by]
        self.owed, self.findings = [], []
        if not self.ran:
            return
        if len(self.ran) < len(OWED_KINDS):
            self.findings = [f'{" and ".join(OWED_KINDS)} are graded together on one image, this run graded '
                             f'{self.ran[0]} alone']
            return
        logs = [grade.parse((out / f'{name}.log').read_text(errors='replace'), spec['sys_hz'], spec['cpu_hz'])
                for name in OWED_KINDS]
        shape = shape_costs.of_config(scenario.ROOT / 'configs' / f'{spec["shape"]}.yaml', spec['interfaces'],
                                      scenario.ROOT) if 'shape' in spec else shape_costs.shape(spec['interfaces'])
        _, self.owed, self.findings = held(*logs, shape, *(over_share(by[name]) for name in OWED_KINDS))

    def owes(self, line: str) -> bool:
        """Whether a STATED line is one the registrations make in a group this disposition holds."""
        return not self.findings and any(line.startswith(f'{name}: {kind}') for name, kinds in OWED_KINDS.items()
                                         for kind in kinds if name in self.ran)

    def stated(self, lines: list[str]) -> list[str]:
        """The STATED lines that still fail: those not owed, and each finding."""
        self.owed += [f'{line}, owed to {DISPOSITION}' for line in lines if self.owes(line)]
        return [line for line in lines if not self.owes(line)] + [f'{DISPOSITION}: {f}' for f in self.findings]

    def shares(self, lines: list[str]) -> list[str]:
        """The SHARE lines that still fail: srp-bound's is owed while the disposition holds (its passes are OWED)."""
        return [line for line in lines if self.findings or not line.startswith(f'{kept_window.BOUND}:')]


def selftest() -> list[tuple[str, bool, str]]:
    """Each condition's outcome on synthetic logs at 1x1/1if and 100 MHz, the unit's edge from the rule."""
    shape, hz = shape_costs.of_point('1x1/1if'), 100_000_000
    unit = shape_costs.at(shape, scenario.ROOT)[UNIT]
    edge = next(c for c in range(unit * 100, 0, -1) if record_classes.rule(c, hz) <= unit)

    def log(probes: list[tuple[str, int | None]]) -> grade.Log:
        """A log of the probes' marks, each followed by a record of those cycles, or none."""
        lines = []
        for k, (probe, c) in enumerate(probes):
            at = 1_000_000 * (k + 1)
            lines.append(f'MARK {at} {probe}')
            if c is not None:
                lines.append(f'SPAN {at + 100} {at + 100} {c} 00002000 {RECORD}')
        return grade.parse('\n'.join([*lines, 'SUMMARY passes=1', 'RESULT: PASS']) + '\n', hz, hz)

    def graded(kept: list[int | None], bound: int | None, shares: tuple = ((), ())) -> tuple[list[str], list[str]]:
        """The owed lines and the findings of srp-kept's three probes and srp-bound's one."""
        names = ('srp.kept_advertise.if0', 'srp.kept_recount.if0', 'srp.kept_failed.if0')
        return held(log(list(zip(names, kept))), log([('srp.bound_advertise.if0', bound)]), shape, *shares)[1:]
    within = graded([edge, edge, 1_000], edge)
    owed = graded([2 * edge, edge, 1_000], 3 * edge)
    over = graded([2 * edge, edge, 1_000], 2 * edge - 1)
    missing = graded([1_000, None, 1], edge)
    shared = graded([1_000, 1_000, 1_000], edge, ([(5_000, 250_000)], [(6_000, 260_000)]))
    return [(f'records at the unit by the rule ({edge:,} cycles, {unit} us), kept <= bound: nothing owed or found',
             within == ([], []), str(within)),
            ('records past the unit with kept <= bound are owed to #977, by name and link, and found nothing',
             len(owed[0]) == 2 and all('#977' in o and '/issues/977' in o for o in owed[0]) and owed[1] == [],
             str(owed)),
            ('a kept record one cycle dearer than the bound one breaks kept <= bound, its own probe\'s',
             len(over[1]) == 1 and 'kept_advertise' in over[1][0] and 'kept <= bound' in over[1][0], str(over)),
            ('a probe with no record is a finding, the next probe\'s record not taken for it',
             len(missing[1]) == 1 and 'kept_recount' in missing[1][0] and 'no SRP record' in missing[1][0],
             str(missing)),
            ('a work pass of srp-kept over THE SHARE is a finding; srp-bound\'s is owed to #977',
             len(shared[1]) == 1 and 'srp-kept' in shared[1][0] and 'THE SHARE' in shared[1][0] and
             any('srp-bound' in o and '#977' in o for o in shared[0]), str(shared))]


def main(argv: list[str]) -> int:
    """Grade a build's srp-kept and srp-bound logs, or run the self-test."""
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
    missing = [name for name in OWED_KINDS if not (results / f'{name}.log').is_file()]
    if missing:
        print(f'kept_grade: no {", ".join(missing)} log in the results: run.py --groups {",".join(OWED_KINDS)} first')
        return 1
    logs = [grade.parse((results / f'{name}.log').read_text(errors='replace'), spec['sys_hz'], spec['cpu_hz'])
            for name in OWED_KINDS]
    graded = [json.loads(p.read_text()) if (p := results / f'{name}.json').is_file() else None for name in OWED_KINDS]
    shape = shape_costs.of_config(scenario.ROOT / 'configs' / f'{spec["shape"]}.yaml', spec['interfaces'],
                                  scenario.ROOT)
    lines, owed, findings = held(*logs, shape, *(over_share(g) for g in graded))
    # the share is read from run.py's grading of each group (its <group>.json): with none, it is unchecked
    findings += [f'{name}: no {name}.json beside its log, so THE SHARE is unchecked: run.py grades it'
                 for name, g in zip(OWED_KINDS, graded) if g is None]
    print(f'POINT {spec["shape"]}, {spec["interfaces"]} interface(s): shape {tuple(shape)}')
    print('\n'.join(lines))
    for line in owed:
        print(f'OWED {line}')
    for finding in findings:
        print(f'FINDING {finding}')
    print(f'kept_grade: {"PASS" if not findings else "FAIL"} ({len(findings)} finding(s), {len(owed)} owed to '
          f'{DISPOSITION})')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
