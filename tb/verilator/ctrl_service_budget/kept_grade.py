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
tier-2 slices of SRP's records over the slice, and the bound group's walk, polls base and work passes over THE SHARE
that its registrations make are each named OWED #977, never a pass, while all of these hold, each a finding otherwise:

  the logs        both groups' logs are present and each finished: the simulation completed, with no trap or bus
                  error (grade.refuse_run, as run.py refuses a group's log);
  the records     every probe kept_window makes at the point's interface count is marked in its group's log, none
                  other is, and each has its record;
  kept <= bound   every srp-kept probe's dearest record costs no more than the dearest srp-bound record of its own
                  interface on the same image (the same MRPDU, its inputs unbound and bound), that record present;
  the share       no work pass of srp-kept is over THE SHARE (share.py, 2 ms), nor the longest of any idle run of
                  either group (an idle pass makes no registration, so none is owed); both are read from the logs
                  graded here (grade.pass_share), never from a result file beside them;
  the builds      every pass of either group given whole to THE TRANSMIT's build, and every build of one MRPDU, is
                  within its stated cost (whole_grade.held; CTRL_LOOP_BUILD_PASS_US, CTRL_LOOP_BUILD_ONE_PASS_US);
  the pair        both groups are graded together, on one image.

run.py applies the same disposition to its STATED and SHARE lines (Disposition): with every condition held, the
owed ones are printed OWED and fail nothing; otherwise each stays a failure and each finding is one more.

usage: python3 -I kept_grade.py <build-dir> [--results DIR] | --selftest
Exit 0 = every condition held; 1 = a finding, or a group's log missing.
--selftest grades synthetic logs at 1x1/1if, through held, Disposition and the standalone entry point: each
condition's breach is a finding of its own, by name, the unit's overrun alone is owed, and a record is its own
probe's, never an earlier mark's.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import tempfile
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
#: The owner's disposition of the registration cost (#969, ruling of 2026-11-22, option 1).
DISPOSITION = '#977 (https://github.com/kebag-logic/milan-fpga/issues/977)'
#: run.py's STATED lines the registrations make, each group's (run.stated_misses' words), owed while held.
OWED_KINDS = {kept_window.NAME: ("an SRP record's apply of ", "a tier-2 slice of SRP's records of "),
              kept_window.BOUND: ("an SRP record's apply of ", "a tier-2 slice of SRP's records of ",
                                  "a walk item of ", "a pass's polls base of ")}


def probes(interfaces: int) -> dict[str, list[str]]:
    """Each group's probe names at that many interfaces, as kept_window makes them."""
    point = scenario.Point('', '', interfaces, 0, 0, interfaces, interfaces)
    return {g.name: [p.name for p in g.probes] for g in kept_window.groups(point)}


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


def dearest(log: grade.Log, names: list[str]) -> dict[str, int | None]:
    """Each named probe marked in the log, its dearest record's CPU cycles, None for none."""
    found = records(log)
    marked = {probe for _, probe in log.marks}
    return {probe: max((cycles for mark, _, cycles in found if mark == probe), default=None)
            for probe in names if probe in marked}


def over_share(log: grade.Log) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """The log's work passes over THE SHARE, (bus cycle, CPU cycles) each, and its idle runs whose longest pass is over
    it, (run, CPU cycles) each: grade.pass_share of the log itself, its work passes by their start, its idle runs by
    their index (an idle pass is printed only as its run's longest)."""
    over = grade.pass_share(log)['over_passes']
    return ([(o['start_sys'], o['cycles']) for o in over if 'start_sys' in o],
            [(o['idle_run'], o['cycles']) for o in over if 'idle_run' in o])


def held(kept: grade.Log, bound: grade.Log, shape: shape_costs.Shape, interfaces: int) -> tuple[list[str], list[str],
                                                                                              list[str]]:
    """The report's lines, the owed lines and the findings of both groups' logs on one image of that many
    interfaces."""
    unit = shape_costs.at(shape, scenario.ROOT)[UNIT]
    lines, owed, findings = [], [], []
    want, recs = probes(interfaces), {}
    for name, log, prefix in ((kept_window.NAME, kept, 'srp.kept_'), (kept_window.BOUND, bound, 'srp.bound_')):
        try:
            grade.refuse_run(log, scenario.Group(name))
        except grade.Refusal as error:
            findings.append(f'{name}: its log measures nothing: {error}')
        marked = [probe for _, probe in sorted(log.marks)]
        findings += [f'{probe}: never marked in the {name} log' for probe in want[name] if probe not in marked]
        findings += [f'{probe}: marked in the {name} log, not a probe of {name} at {interfaces} interface(s)'
                     for probe in marked if probe.startswith(prefix) and probe not in want[name]]
        recs[name] = dearest(log, want[name])
        for probe, cycles in recs[name].items():
            if cycles is None:
                findings.append(f'{probe}: no SRP record follows its mark')
                continue
            us = record_classes.rule(cycles, kept.cpu_hz)
            lines.append(f'RECORD {probe}: the dearest {cycles:,} CPU cycles, {us} us by the rule, against {UNIT} '
                         f'{unit} us')
            if us > unit:
                owed.append(f'{probe}: a record of {cycles:,} CPU cycles, {us} us by the rule, over {UNIT} {unit} us, '
                            f'owed to {DISPOSITION}')
    mates = {probe.rpartition('.')[2]: probe for probe in want[kept_window.BOUND]}
    for probe, cycles in recs[kept_window.NAME].items():
        mate = mates.get(probe.rpartition('.')[2])
        if cycles is None:
            continue
        if recs[kept_window.BOUND].get(mate) is None:
            findings.append(f'{probe}: no {mate or "srp-bound"} record of its interface on the same image, so kept <= '
                            f'bound is unchecked')
            continue
        lines.append(f'KEPT <= BOUND {probe}: {cycles:,} against {recs[kept_window.BOUND][mate]:,} CPU cycles')
        if cycles > recs[kept_window.BOUND][mate]:
            findings.append(f'{probe}: kept <= bound broken, {cycles:,} CPU cycles against the bound record\'s '
                            f'{recs[kept_window.BOUND][mate]:,}')
    (k_work, k_idle), (b_work, b_idle) = over_share(kept), over_share(bound)
    lines += [f'SHARE {name}: {len(work)} work pass(es) and {len(idle)} idle run(s) over THE SHARE, of '
              f'{len(log.passes)} work pass(es) and {len(log.idle)} idle run(s) in its log'
              for name, log, work, idle in ((kept_window.NAME, kept, k_work, k_idle),
                                            (kept_window.BOUND, bound, b_work, b_idle))]
    findings += [f'{kept_window.NAME}: a work pass of {cycles:,} CPU cycles at bus cycle {at} over THE SHARE'
                 for at, cycles in k_work]
    owed += [f'{kept_window.BOUND}: a work pass of {cycles:,} CPU cycles at bus cycle {at} over THE SHARE, the '
             f'bound path\'s registrations, owed to {DISPOSITION}' for at, cycles in b_work]
    findings += [f'{name}: idle run {run}\'s longest pass, {cycles:,} CPU cycles, over THE SHARE (an idle pass makes '
                 f'no registration, so it is not owed)' for name, idle in ((kept_window.NAME, k_idle),
                                                                       (kept_window.BOUND, b_idle))
                 for run, cycles in idle]
    for name, log in ((kept_window.NAME, kept), (kept_window.BOUND, bound)):
        builds = whole_grade.held(log, shape)
        for kind in ('build', 'build-one'):
            lines.append(f'BUILD {name} {kind}: the heaviest pass {builds["heaviest"][kind]:,} CPU cycles, against '
                         f'its stated {builds["limits"][kind]:,} ({whole_grade.COSTS[kind]})')
        findings += [f'{name}: a {o["kind"]} pass at bus cycle {o["start_sys"]}: {o["cycles"]:,} CPU cycles over its '
                     f'stated cost' for o in builds['over'] if o['kind'] != 'step']
    return lines, owed, findings


def point_shape(spec: dict) -> shape_costs.Shape:
    """The image's shape: what its builder states for the configuration and interfaces it was built at, or, for a
    self-test's spec, which names no configuration, the shipping shape's streams (as run.graded's)."""
    return shape_costs.of_config(scenario.ROOT / 'configs' / f'{spec["shape"]}.yaml', spec['interfaces'],
                                 scenario.ROOT) if 'shape' in spec else shape_costs.shape(spec['interfaces'])


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
        _, self.owed, self.findings = held(*logs, point_shape(spec), spec['interfaces'])

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


def grade_dir(build_dir: Path, results: Path | None = None) -> tuple[list[str], list[str], list[str]]:
    """The standalone grade of a build's srp-kept and srp-bound logs: the report's lines, the owed lines and the
    findings. Every figure is read from the logs themselves; a result file beside them is never read."""
    spec = json.loads((build_dir / 'build.json').read_text())
    results = results or build_dir / 'results'
    missing = [name for name in OWED_KINDS if not (results / f'{name}.log').is_file()]
    if missing:
        return [], [], [f'{name}: no {name}.log in the results: run.py --groups {",".join(OWED_KINDS)} first'
                         for name in missing]
    logs = []
    for name in OWED_KINDS:
        try:
            logs.append(grade.parse((results / f'{name}.log').read_text(errors='replace'), spec['sys_hz'],
                                    spec['cpu_hz']))
        except grade.Refusal as error:
            return [], [], [f'{name}: its log does not parse: {error}']
    shape = point_shape(spec)
    lines, owed, findings = held(*logs, shape, spec['interfaces'])
    return [f'POINT {spec.get("shape", "-")}, {spec["interfaces"]} interface(s): shape {tuple(shape)}', *lines], \
        owed, findings


def selftest() -> list[tuple[str, bool, str]]:
    """Each condition's outcome on synthetic logs at 1x1/1if and 100 MHz, the unit's edge from the rule, through held,
    Disposition and the standalone entry point."""
    shape, hz = shape_costs.of_point('1x1/1if'), 100_000_000
    unit = shape_costs.at(shape, scenario.ROOT)[UNIT]
    edge = next(c for c in range(unit * 100, 0, -1) if record_classes.rule(c, hz) <= unit)
    share = grade.pass_share(grade.parse('', hz, hz))['cycles']
    build_one = whole_grade.held(grade.parse('', hz, hz), shape)['limits']['build-one']
    kept_names = ('srp.kept_advertise.if0', 'srp.kept_recount.if0', 'srp.kept_failed.if0')
    clean = ([edge, edge, 1_000], [('srp.bound_advertise.if0', edge)])

    def text(probes: list[tuple[str, int | None]], extra: tuple[str, ...] = (), result: str = 'PASS') -> str:
        """A log of the probes' marks, each followed by a record of those cycles, or none, then the extra lines."""
        lines = []
        for k, (probe, c) in enumerate(probes):
            at = 1_000_000 * (k + 1)
            lines.append(f'MARK {at} {probe}')
            if c is not None:
                lines.append(f'SPAN {at + 100} {at + 100} {c} 00002000 {RECORD}')
        return '\n'.join([*lines, *extra, 'SUMMARY passes=1', f'RESULT: {result}']) + '\n'

    def texts(kept: list[int | None], bound: list[tuple[str, int | None]], kept_extra: tuple[str, ...] = (),
              bound_extra: tuple[str, ...] = (), kept_result: str = 'PASS') -> dict[str, str]:
        """srp-kept's three probes, those cycles each, and srp-bound's probes, each log with its extra lines."""
        return {kept_window.NAME: text(list(zip(kept_names, kept)), kept_extra, kept_result),
                kept_window.BOUND: text(bound, bound_extra)}

    def graded(*args, **kwargs) -> tuple[list[str], list[str]]:
        """The owed lines and the findings of held on those logs; an exception is a finding of its own."""
        logs = texts(*args, **kwargs)
        try:
            return held(*(grade.parse(logs[name], hz, hz) for name in OWED_KINDS), shape, 1)[1:]
        except Exception as error:  # noqa: BLE001 - the self-test reports it as the check's failure
            return [], [f'held raised {type(error).__name__}: {error}']

    over_share_pass = (f'PASS 0 9000000 9000000 {share + 1}',)
    idle_over = (f'IDLE 4 1000 {share + 1}',)
    build_over = (f'PASS 1 9500000 9500000 {build_one + 1}', 'ENTRY 9500010 build_mrpdu')
    within = graded(*clean)
    owed = graded([2 * edge, edge, 1_000], [('srp.bound_advertise.if0', 3 * edge)])
    over = graded([2 * edge, edge, 1_000], [('srp.bound_advertise.if0', 2 * edge - 1)])
    missing = graded([1_000, None, 1], [('srp.bound_advertise.if0', edge)])
    shared = graded(*clean, kept_extra=over_share_pass, bound_extra=over_share_pass)
    idle = [graded(*clean, kept_extra=idle_over), graded(*clean, bound_extra=idle_over)]
    built = [graded(*clean, kept_extra=build_over), graded(*clean, bound_extra=build_over)]
    unfinished = graded(*clean, kept_result='FAIL')
    unmarked = graded([1_000, 1_000], [('srp.bound_advertise.if0', edge)])
    unmated = graded(clean[0], [('srp.bound_advertise.if1', edge)])

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        (out / 'build.json').write_text(json.dumps(dict(sys_hz=hz, cpu_hz=hz, interfaces=1)))
        (out / 'results').mkdir()

        def standalone(logs: dict[str, str | None], beside: str | None = None) -> tuple[int, str]:
            """main's exit and output on those logs (None: no log), each with that text as its result file."""
            for name, body in logs.items():
                for suffix in ('.log', '.json'):
                    (out / 'results' / f'{name}{suffix}').unlink(missing_ok=True)
                if body is not None:
                    (out / 'results' / f'{name}.log').write_text(body)
                if beside is not None:
                    (out / 'results' / f'{name}.json').write_text(beside)
            printed = io.StringIO()
            try:
                with contextlib.redirect_stdout(printed):
                    rc = main([str(out)])
            except Exception as error:  # noqa: BLE001 - the self-test reports it as the check's failure
                return 2, f'main raised {type(error).__name__}: {error}'
            return rc, printed.getvalue()

        stale = json.dumps(dict(group=kept_window.NAME, passes=dict(share=dict(over_passes=[]))))
        alone_clean = standalone(texts(*clean))
        alone_over = [standalone(texts(*clean, kept_extra=over_share_pass), beside) for beside in (stale, '{}')]
        alone_idle = standalone(texts(*clean, kept_extra=idle_over))
        alone_absent = standalone({**texts(*clean), kept_window.BOUND: None})
        alone_failed = standalone(texts(*clean, kept_result='FAIL'), stale)
        alone_garbled = standalone({**texts(*clean), kept_window.NAME: 'NOT-A-LINE 1\nRESULT: PASS\n'})
        for name, body in texts(*clean).items():
            (out / f'{name}.log').write_text(body)
        pair = Disposition([dict(group=name) for name in OWED_KINDS], out, dict(sys_hz=hz, cpu_hz=hz, interfaces=1))
        stated = [f"{kept_window.NAME}: an SRP record's apply of 40,000 CPU cycles, over its stated 28,500",
                  f'{kept_window.BOUND}: a walk item of 15,000 CPU cycles, over its stated 12,000']
        pair_left = pair.stated(list(stated))
        alone = Disposition([dict(group=kept_window.NAME)], out, dict(sys_hz=hz, cpu_hz=hz, interfaces=1))
        alone_left = alone.stated(list(stated))
        (out / f'{kept_window.NAME}.log').write_text(texts(*clean, kept_extra=over_share_pass)[kept_window.NAME])
        broken = Disposition([dict(group=name) for name in OWED_KINDS], out, dict(sys_hz=hz, cpu_hz=hz, interfaces=1))
        broken_left = broken.stated(list(stated))

    def only(found: list[str], *words: str) -> bool:
        """One finding, carrying every word."""
        return len(found) == 1 and all(w in found[0] for w in words)

    return [(f'records at the unit by the rule ({edge:,} cycles, {unit} us), kept <= bound: nothing owed or found',
             within == ([], []), str(within)),
            ('records past the unit with kept <= bound are owed to #977, by name and link, and found nothing',
             len(owed[0]) == 2 and all('#977' in o and '/issues/977' in o for o in owed[0]) and owed[1] == [],
             str(owed)),
            ('a kept record one cycle dearer than the bound one breaks kept <= bound, its own probe\'s',
             only(over[1], 'kept_advertise', 'kept <= bound broken'), str(over)),
            ('a probe with no record is a finding, the next probe\'s record not taken for it',
             only(missing[1], 'kept_recount', 'no SRP record'), str(missing)),
            ('a work pass of srp-kept over THE SHARE is a finding; srp-bound\'s is owed to #977',
             only(shared[1], kept_window.NAME, 'work pass', 'THE SHARE') and
             any(kept_window.BOUND in o and 'THE SHARE' in o and '#977' in o for o in shared[0]), str(shared)),
            ('an idle run over THE SHARE in either group is a finding, never owed, read without a work pass\'s start',
             all(only(f, name, 'idle run', 'THE SHARE') and not any('idle' in o for o in o_)
                 for (o_, f), name in zip(idle, OWED_KINDS)), str(idle)),
            ('a build of one MRPDU one cycle over its stated cost is a finding in either group',
             all(only(f, name, 'build-one pass', 'over its stated cost') for (_, f), name in zip(built, OWED_KINDS)),
             str(built)),
            ('an unfinished srp-kept log measures nothing: a finding',
             only(unfinished[1], kept_window.NAME, 'measures nothing'), str(unfinished)),
            ('a probe the point makes that is never marked is a finding',
             only(unmarked[1], 'srp.kept_failed.if0', 'never marked'), str(unmarked)),
            ('a kept probe with no bound record of its own interface is a finding, never a skipped comparison',
             len(unmated[1]) == 5 and sum('kept <= bound is unchecked' in f for f in unmated[1]) == 3 and
             any('srp.bound_advertise.if0: never marked' in f for f in unmated[1]) and
             any('srp.bound_advertise.if1' in f and 'not a probe' in f for f in unmated[1]), str(unmated)),
            ('both groups graded together: their #977 lines are owed by name and link, and nothing stays',
             pair.findings == [] and pair_left == [] and len(pair.owed) == 2 and
             all('/issues/977' in o for o in pair.owed), str((pair.findings, pair_left, pair.owed))),
            ('one group graded alone is a finding: nothing is owed and every line stays a failure',
             only(alone.findings, 'graded together', 'alone') and alone.owed == [] and
             alone_left[:2] == stated and len(alone_left) == 3, str((alone.findings, alone_left))),
            ('both groups graded together with a condition broken in a log: the finding stays, nothing is owed',
             only(broken.findings, kept_window.NAME, 'work pass', 'THE SHARE') and broken.owed == [] and
             broken_left[:2] == stated and len(broken_left) == 3 and
             broken.shares([f'{kept_window.BOUND}: a pass over THE SHARE']) != [],
             str((broken.findings, broken_left))),
            ('standalone: both logs complete and within: PASS',
             alone_clean[0] == 0 and 'kept_grade: PASS' in alone_clean[1], alone_clean[1]),
            ('standalone: THE SHARE is read from the log, so a kept work pass over it fails beside a stale or empty '
             'result file', all(rc == 1 and 'FINDING srp-kept: a work pass' in o for rc, o in alone_over),
             str(alone_over)),
            ('standalone: an idle run over THE SHARE fails by name, never a crash',
             alone_idle[0] == 1 and 'FINDING srp-kept: idle run' in alone_idle[1], alone_idle[1]),
            ('standalone: a group with no log fails by name',
             alone_absent[0] == 1 and f'FINDING {kept_window.BOUND}: no {kept_window.BOUND}.log' in alone_absent[1],
             alone_absent[1]),
            ('standalone: an unfinished log fails by name beside a within-share result file',
             alone_failed[0] == 1 and 'FINDING srp-kept: its log measures nothing' in alone_failed[1],
             alone_failed[1]),
            ('standalone: a log that does not parse fails by name',
             alone_garbled[0] == 1 and 'FINDING srp-kept: its log does not parse' in alone_garbled[1],
             alone_garbled[1])]


def main(argv: list[str]) -> int:
    """Grade a build's srp-kept and srp-bound logs, or run the self-test."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('build_dir', type=Path, nargs='?')
    parser.add_argument('--results', type=Path, help="the groups' logs (default: <build-dir>/results)")
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args(argv)
    if args.selftest:
        checks = selftest()
        for what, ok, detail in checks:
            print(f'[{"ok" if ok else "FAIL"}] {what}' + ('' if ok else f': {detail}'))
        print(f'kept_grade selftest: {"PASS" if all(ok for _, ok, _ in checks) else "FAIL"} ({len(checks)} checks)')
        return 0 if all(ok for _, ok, _ in checks) else 1
    if args.build_dir is None:
        parser.error('a build directory, or --selftest')
    lines, owed, findings = grade_dir(args.build_dir, args.results)
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
