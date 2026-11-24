# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The records that register Talkers, the kept Talkers' (#969) and the bound ones the base makes (kept_window.py's
srp-kept and srp-bound groups), each held to the drain's charge since #977.

Each SRP record is a span of srp_mbx.c's record handler (receive, a SPAN line), and each probe's records are those
from its mark to the next mark. A record that registers more than one or two Talkers is past ctrl_loop.h's
CTRL_LOOP_SRP_UNIT_US (by the stated rule: its cycles at the CPU clock, plus 5 %, rounded up to 5 us;
record_classes.rule) on the bound path the base has, a bridge re-declaring the bound Talkers after any LeaveAll, and
the kept Talkers make the same registrations before the bindings. That cost was #977's, owed here by the owner's
ruling on #969 (2026-11-22: DISPOSITION, amended 2026-11-23: AMENDED). #977 charges it: the drain charges each record
CTRL_LOOP_SRP_UNIT_US plus CTRL_LOOP_SRP_REG_US for each Talker value its frame carries (poll_grade.record_limits), so
each record of either group is held to that charge, and nothing is owed: every condition below is a finding when it
fails, srp-bound's passes over THE SHARE and its builds of one over their stated cost as srp-kept's are:

  the logs        both groups' logs are present and each finished: the simulation completed, with no trap or bus
                  error (grade.refuse_run, as run.py refuses a group's log);
  the records     every probe kept_window makes at the point's interface count is marked in its group's log, none
                  other is, and each has its record, its dearest within its charge;
  kept <= bound   every srp-kept probe's dearest record costs no more than the dearest srp-bound record of its own
                  interface on the same image (the same MRPDU, its inputs unbound and bound), that record present,
                  held within the measurement rule's 5 % (record_classes.rule): kept <= bound x 1.05 (#969's
                  2026-11-23 amendment), printed with both figures and the margin;
  the share       no work pass of either group is over THE SHARE (share.py, 2 ms), nor the longest of any idle run of
                  either; both are read from the logs graded here (grade.pass_share), never from a result file beside
                  them;
  the builds      every pass of either group given whole to THE TRANSMIT's build, and every build of one MRPDU, is
                  within its stated cost (whole_grade.held; CTRL_LOOP_BUILD_PASS_US, CTRL_LOOP_BUILD_ONE_PASS_US);
  the pair        both groups are graded together, on one image.

run.py applies the same grade to its STATED and SHARE lines (Disposition): none is owed, each stays a failure, and
each finding is one more.

usage: python3 -I kept_grade.py <build-dir> [--results DIR] | --selftest
Exit 0 = every condition held; 1 = a finding, or a group's log missing.
--selftest grades synthetic logs at 1x1/1if, through held, Disposition and the standalone entry point: each
condition's breach is a finding of its own, by name, a record over its charge and the bound path's build of one and
passes over THE SHARE among them, a record whose tagged frame carries Talker values charged them (held at that charge,
one cycle more a finding), nothing is owed, kept 4 % over bound holds and 6 % over breaks, bound + 5 % exactly
holds and one cycle more breaks, a pass given whole to THE TRANSMIT's build over the slice stays a failure, as does a
bound build of one over it, one whose round did work or that is an aged step's (whole_grade.held classes neither a
build of one), and a build of one as long as a pass given whole, and a record is its own probe's, never an earlier
mark's.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import tempfile
from bisect import bisect_left
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import grade  # noqa: E402
import kept_window  # noqa: E402
import poll_grade  # noqa: E402
import record_classes  # noqa: E402
import scenario  # noqa: E402
import shape_costs  # noqa: E402
import slice_grade  # noqa: E402
import whole_grade  # noqa: E402

RECORD = 'srp_mbx:receive'
UNIT = 'CTRL_LOOP_SRP_UNIT_US'
#: The owner's disposition of the registration cost (#969, ruling of 2026-11-22, option 1).
DISPOSITION = '#977 (https://github.com/kebag-logic/milan-fpga/issues/977)'
#: The amendment (#969, ruling of 2026-11-23): kept <= bound within the rule, and srp-bound's build of one owed to #977.
AMENDED = "#969's ruling of 2026-11-23"
#: kept <= bound is held within the measurement rule's 5 % (record_classes.rule), per AMENDED.
KEPT_MARGIN_PERCENT = 5
#: run.py's STATED line of a tier-2 slice of THE TRANSMIT's build (run.stated_misses' words). AMENDED owes srp-bound's
#: only where its pass is a build of one (Disposition.owes), never a pass given whole to the build, never srp-kept's.
TRANSMIT_SLICE = "a tier-2 slice of THE TRANSMIT's build of "
#: run.py's STATED lines owed, each group's (run.stated_misses' words): none since #977 charges the registrations, the
#: groups graded together on one image.
OWED_KINDS: dict[str, tuple[str, ...]] = {kept_window.NAME: (), kept_window.BOUND: ()}
#: The pass kinds of whole_grade.held owed: none since #977 (srp-bound's build of one was, by AMENDED).
BOUND_OWED_BUILDS: tuple[str, ...] = ()


def kept_within(kept: int, bound: int) -> bool:
    """Whether a kept record is within the bound record by the rule: kept <= bound x (1 + KEPT_MARGIN_PERCENT %)."""
    return kept * 100 <= bound * (100 + KEPT_MARGIN_PERCENT)


def kept_line(probe: str, kept: int, bound: int) -> str:
    """The KEPT <= BOUND line: both figures, the difference and the margin left to the rule's allowance."""
    allowed = bound * (100 + KEPT_MARGIN_PERCENT) // 100
    return (f'KEPT <= BOUND {probe}: {kept:,} against {bound:,} CPU cycles, {kept - bound:+,} '
            f'({(kept - bound) * 100 / bound:+.2f} %), {"within" if kept_within(kept, bound) else "past"} the rule\'s '
            f'+{KEPT_MARGIN_PERCENT} % ({allowed:,}), margin {allowed - kept:+,}')


def probes(interfaces: int) -> dict[str, list[str]]:
    """Each group's probe names at that many interfaces, as kept_window makes them."""
    point = scenario.Point('', '', interfaces, 0, 0, interfaces, interfaces)
    return {g.name: [p.name for p in g.probes] for g in kept_window.groups(point)}


def records(log: grade.Log) -> list[tuple[str, int, int, int]]:
    """Each SRP record of the log: the mark it follows, its bus cycle, its CPU cycles and the CPU cycle it started."""
    marks = sorted(log.marks)
    starts = [cycle for cycle, _ in marks]
    out = []
    for kind, *rest in log.traced:
        if kind == 'SPAN' and len(rest) >= 5 and rest[4] == RECORD:
            sys_start, cpu_start, cycles = int(rest[0]), int(rest[1]), int(rest[2])
            k = bisect_left(starts, sys_start + 1) - 1
            out.append((marks[k][1] if k >= 0 else '', sys_start, cycles, cpu_start))
    return out


def dearest(log: grade.Log, names: list[str], charge: Callable[[int], int] | None = None
            ) -> dict[str, tuple[int, int] | None]:
    """Each named probe marked in the log, its dearest record's CPU cycles and that record's charge (charge, from the
    CPU cycle it started; 0 without one), None for none."""
    found = records(log)
    marked = {probe for _, probe in log.marks}
    out: dict[str, tuple[int, int] | None] = {}
    for probe in names:
        if probe in marked:
            mine = [(cycles, start) for mark, _, cycles, start in found if mark == probe]
            cycles, start = max(mine, default=(None, 0))
            out[probe] = None if cycles is None else (cycles, charge(start) if charge else 0)
    return out


def charges(log: grade.Log, shape: shape_costs.Shape, name: str) -> Callable[[int], int]:
    """The drain's charge of the group's SRP record that starts at a CPU cycle, in CPU cycles: CTRL_LOOP_SRP_UNIT_US
    plus CTRL_LOOP_SRP_REG_US for each Talker value its own tagged frame carries (poll_grade.record_limits), from the
    group's steps at the shape (#977). A record here is its handler's own span, starting on the handler's cycle, so its
    charge is the last handler's to start at or before it (charged takes the last strictly before)."""
    unit = shape_costs.at(shape, scenario.ROOT)[UNIT] * log.cpu_hz // 1_000_000
    point = scenario.Point('', '', shape.interfaces, 0, 0, shape.sources, shape.sinks)
    steps = next(g.steps for g in kept_window.groups(point) if g.name == name)
    limits = poll_grade.record_limits(log, poll_grade.spans(log), shape, unit, list(steps))
    return lambda start: poll_grade.charged(limits, start + 1, unit)


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
        found = dearest(log, want[name], charges(log, shape, name))
        recs[name] = {probe: None if r is None else r[0] for probe, r in found.items()}
        for probe, record in found.items():
            if record is None:
                findings.append(f'{probe}: no SRP record follows its mark')
                continue
            cycles, charge = record
            us = record_classes.rule(cycles, kept.cpu_hz)
            lines.append(f'RECORD {probe}: the dearest {cycles:,} CPU cycles, {us} us by the rule, against its '
                         f'charge {charge:,} ({UNIT} {unit} us and its Talker values)')
            if cycles > charge:
                findings.append(f'{probe}: a record of {cycles:,} CPU cycles over its charge {charge:,}')
    mates = {probe.rpartition('.')[2]: probe for probe in want[kept_window.BOUND]}
    for probe, cycles in recs[kept_window.NAME].items():
        mate = mates.get(probe.rpartition('.')[2])
        if cycles is None:
            continue
        if recs[kept_window.BOUND].get(mate) is None:
            findings.append(f'{probe}: no {mate or "srp-bound"} record of its interface on the same image, so kept <= '
                            f'bound is unchecked')
            continue
        bound_cycles = recs[kept_window.BOUND][mate]
        lines.append(kept_line(probe, cycles, bound_cycles))
        if not kept_within(cycles, bound_cycles):
            findings.append(f'{probe}: kept <= bound broken, {cycles:,} CPU cycles against the bound record\'s '
                            f'{bound_cycles:,} past the rule\'s +{KEPT_MARGIN_PERCENT} % '
                            f'({bound_cycles * (100 + KEPT_MARGIN_PERCENT) // 100:,})')
    (k_work, k_idle), (b_work, b_idle) = over_share(kept), over_share(bound)
    lines += [f'SHARE {name}: {len(work)} work pass(es) and {len(idle)} idle run(s) over THE SHARE, of '
              f'{len(log.passes)} work pass(es) and {len(log.idle)} idle run(s) in its log'
              for name, log, work, idle in ((kept_window.NAME, kept, k_work, k_idle),
                                            (kept_window.BOUND, bound, b_work, b_idle))]
    findings += [f'{name}: a work pass of {cycles:,} CPU cycles at bus cycle {at} over THE SHARE'
                 for name, work in ((kept_window.NAME, k_work), (kept_window.BOUND, b_work)) for at, cycles in work]
    findings += [f'{name}: idle run {run}\'s longest pass, {cycles:,} CPU cycles, over THE SHARE'
                 for name, idle in ((kept_window.NAME, k_idle), (kept_window.BOUND, b_idle)) for run, cycles in idle]
    for name, log in ((kept_window.NAME, kept), (kept_window.BOUND, bound)):
        builds = whole_grade.held(log, shape)
        for kind in ('build', 'build-one'):
            lines.append(f'BUILD {name} {kind}: the heaviest pass {builds["heaviest"][kind]:,} CPU cycles, against '
                         f'its stated {builds["limits"][kind]:,} ({whole_grade.COSTS[kind]})')
        over = [o for o in builds['over'] if o['kind'] != 'step']
        owes = [o for o in over if name == kept_window.BOUND and o['kind'] in BOUND_OWED_BUILDS]
        owed += [f'{name}: a {o["kind"]} pass at bus cycle {o["start_sys"]}: {o["cycles"]:,} CPU cycles over its '
                 f'stated {builds["limits"][o["kind"]]:,} ({whole_grade.COSTS[o["kind"]]}, not restated), the bound '
                 f'path\'s registrations, owed to {DISPOSITION}' for o in owes]
        findings += [f'{name}: a {o["kind"]} pass at bus cycle {o["start_sys"]}: {o["cycles"]:,} CPU cycles over its '
                     f'stated cost' for o in over if o not in owes]
    return lines, owed, findings


def transmit_slices(log: grade.Log, shape: shape_costs.Shape) -> dict[str, set[int]]:
    """The CPU cycles of each tier-2 slice of THE TRANSMIT's build over the stated slice (slice_grade.held): 'build-one'
    where whole_grade.held itself classes the slice's pass, by its start, a build of one over its stated cost (the pass
    held owes, BOUND_OWED_BUILDS), and 'build' for every other: a pass given whole to the build (both MRPDUs), one whose
    round did work, an aged step's. Every shape's slice is at least its build of one's stated cost (THE SHAPES), so a
    build of one over the slice is over that cost too; one that were not would stay a failure."""
    ones = {o['start_sys'] for o in whole_grade.held(log, shape)['over'] if o['kind'] in BOUND_OWED_BUILDS}
    out: dict[str, set[int]] = {'build': set(), 'build-one': set()}
    for o in slice_grade.held(log, shape)['over']:
        if o['kind'] == 'build':
            out['build-one' if o['start_sys'] in ones else 'build'].add(o['cycles'])
    return out


def stated_cycles(line: str) -> int | None:
    """The CPU cycles a STATED line names first, None for none."""
    head = line.split(' CPU cycles', 1)
    figure = head[0].rpartition(' ')[2].replace(',', '') if len(head) == 2 else ''
    return int(figure) if figure.isdigit() else None


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
        self.slices: dict[str, set[int]] = {'build': set(), 'build-one': set()}
        if not self.ran:
            return
        if len(self.ran) < len(OWED_KINDS):
            self.findings = [f'{" and ".join(OWED_KINDS)} are graded together on one image, this run graded '
                             f'{self.ran[0]} alone']
            return
        logs = {name: grade.parse((out / f'{name}.log').read_text(errors='replace'), spec['sys_hz'], spec['cpu_hz'])
                for name in OWED_KINDS}
        _, self.owed, self.findings = held(*logs.values(), point_shape(spec), spec['interfaces'])
        self.slices = transmit_slices(logs[kept_window.BOUND], point_shape(spec))

    def owes(self, line: str) -> bool:
        """Whether a STATED line is one the registrations make in a group this disposition holds: none since #977
        charges them (OWED_KINDS empty). srp-bound's slice of THE TRANSMIT's build was owed only where its log's slice
        of those cycles is a build of one (AMENDED)."""
        if self.findings or not any(OWED_KINDS.values()):
            return False
        if line.startswith(f'{kept_window.BOUND}: {TRANSMIT_SLICE}'):
            cycles = stated_cycles(line)
            return (kept_window.BOUND in self.ran and cycles in self.slices['build-one'] and
                    cycles not in self.slices['build'])
        return any(line.startswith(f'{name}: {kind}') for name, kinds in OWED_KINDS.items() for kind in kinds
                   if name in self.ran)

    def stated(self, lines: list[str]) -> list[str]:
        """The STATED lines that still fail: those not owed (every one since #977), and each finding."""
        self.owed += [f'{line}, owed to {DISPOSITION}' for line in lines if self.owes(line)]
        return [line for line in lines if not self.owes(line)] + [f'kept_grade: {f}' for f in self.findings]

    def shares(self, lines: list[str]) -> list[str]:
        """The SHARE lines that still fail: every one since #977 (srp-bound's was owed while the disposition held)."""
        return list(lines)


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


class Synthetic:
    """The self-test's synthetic logs at 1x1/1if and 100 MHz: the unit's edge from the rule, THE SHARE and the stated
    build of one MRPDU, and the extra lines that break each condition."""

    KEPT = ('srp.kept_advertise.if0', 'srp.kept_recount.if0', 'srp.kept_failed.if0')

    def __init__(self) -> None:
        self.shape, self.hz = shape_costs.of_point('1x1/1if'), 100_000_000
        self.unit = shape_costs.at(self.shape, scenario.ROOT)[UNIT]
        self.edge = next(c for c in range(self.unit * 100, 0, -1) if record_classes.rule(c, self.hz) <= self.unit)
        share = grade.pass_share(grade.parse('', self.hz, self.hz))['cycles']
        limits = whole_grade.held(grade.parse('', self.hz, self.hz), self.shape)['limits']
        self.clean = ([self.edge, self.edge, 1_000], [('srp.bound_advertise.if0', self.edge)])
        self.over_share = (f'PASS 0 9000000 9000000 {share + 1}',)
        self.idle_over = (f'IDLE 4 1000 {share + 1}',)
        self.build_over = (f'PASS 1 9500000 9500000 {limits["build-one"] + 1}', 'ENTRY 9500010 build_mrpdu')
        srp = scenario.CH['srp']   # a build pass with two SRP head writes is given whole to THE TRANSMIT's build;
        self.whole_over = (f'PASS 1 9500000 9500000 {limits["build"] + 1}', 'ENTRY 9500010 build_mrpdu',
                           f'TXC 9500020 {srp} 0', f'TXC 9500030 {srp} 0')   # each at the head, so no record to read
        self.slice = slice_grade.held(grade.parse('', self.hz, self.hz), self.shape)['limit']
        self.limits = limits
        #: the drain's charge of srp.bound_advertise's record (and srp.kept_advertise's), its tagged frame's Talker
        #: values, one a sink, each CTRL_LOOP_SRP_REG_US past the unit
        self.values = poll_grade.talker_values(kept_window.declared(0, self.shape.sinks), self.shape.sinks)
        self.charge = (self.unit + self.values * poll_grade.registration_us(self.shape)) * self.hz // 1_000_000
        #: a build of one MRPDU one cycle over the slice (and so over its stated cost, below the slice), and a pass
        #: given whole to THE TRANSMIT's build over the slice and within CTRL_LOOP_BUILD_PASS_US (above the slice)
        self.one_cycles, self.whole_cycles = self.slice + 1, (self.slice + limits['build']) // 2
        self.slice_one = (f'PASS 1 9500000 9500000 {self.one_cycles}', 'ENTRY 9500010 build_mrpdu',
                          f'TXC 9500020 {srp} 0')
        self.slice_whole = (f'PASS 2 9700000 9700000 {self.whole_cycles}', 'ENTRY 9700010 build_mrpdu',
                            f'TXC 9700020 {srp} 0', f'TXC 9700030 {srp} 0')
        #: the same build of one, its round one cycle past idle (whole_grade.ROUND_IDLE_CYCLES of AECP modules), and an
        #: aged step's: whole_grade.held classes neither a build of one, so neither is the pass AMENDED owes
        self.slice_busy = (f'PASS 1 9500000 9500000 {self.one_cycles} mods=aecp:{whole_grade.ROUND_IDLE_CYCLES + 1}',
                           *self.slice_one[1:])
        self.slice_aged = (f'PASS 1 9500000 9500000 {self.one_cycles} step=1 aged=1', *self.slice_one[1:])
        #: a build of one as long as the pass given whole: the slice line's figure names either, so it is ambiguous
        self.slice_equal = (f'PASS 1 9500000 9500000 {self.whole_cycles}', *self.slice_one[1:], *self.slice_whole)
        self.spec = dict(sys_hz=self.hz, cpu_hz=self.hz, interfaces=1)
        #: whether each record's frame is committed to SRP carrying its probe's name (text)
        self.tagged = False

    @staticmethod
    def text(probes: list[tuple[str, int | None]], extra: tuple[str, ...] = (), result: str = 'PASS',
             tagged: bool = False) -> str:
        """A log of the probes' marks, each followed by a record of those cycles, or none, then the extra lines;
        tagged, each record's frame is committed to SRP carrying its probe's name first, so the record is charged that
        frame's Talker values."""
        lines = []
        for k, (probe, c) in enumerate(probes):
            at = 1_000_000 * (k + 1)
            lines.append(f'MARK {at} {probe}')
            if c is not None and tagged:
                lines += [f'RXS {at + 1} 0 60 {probe}', f'RXE {at + 50}', f'RXC {at + 60} {scenario.CH["srp"]}']
            if c is not None:
                lines.append(f'SPAN {at + 100} {at + 100} {c} 00002000 {RECORD}')
        return '\n'.join([*lines, *extra, 'SUMMARY passes=1', f'RESULT: {result}']) + '\n'

    def texts(self, kept: list[int | None], bound: list[tuple[str, int | None]], kept_extra: tuple[str, ...] = (),
              bound_extra: tuple[str, ...] = (), kept_result: str = 'PASS') -> dict[str, str]:
        """srp-kept's three probes, those cycles each, and srp-bound's probes, each log with its extra lines, their
        frames tagged where self.tagged is set."""
        return {kept_window.NAME: self.text(list(zip(self.KEPT, kept)), kept_extra, kept_result, self.tagged),
                kept_window.BOUND: self.text(bound, bound_extra, tagged=self.tagged)}

    def graded(self, *args, **kwargs) -> tuple[list[str], list[str]]:
        """The owed lines and the findings of held on those logs; an exception is a finding of its own."""
        logs = self.texts(*args, **kwargs)
        try:
            return held(*(grade.parse(logs[name], self.hz, self.hz) for name in OWED_KINDS), self.shape, 1)[1:]
        except Exception as error:  # noqa: BLE001 - the self-test reports it as the check's failure
            return [], [f'held raised {type(error).__name__}: {error}']


def only(found: list[str], *words: str) -> bool:
    """One finding, carrying every word."""
    return len(found) == 1 and all(w in found[0] for w in words)


def compared(graded: tuple[list[str], list[str]]) -> tuple[list[str], list[str]]:
    """The owed lines and the findings but the records' charges, for the checks of kept <= bound, whose records are
    past the synthetic logs' charge, the unit (their frames are not tagged)."""
    return graded[0], [f for f in graded[1] if 'over its charge' not in f]


def selftest_held(s: Synthetic) -> list[tuple[str, bool, str]]:
    """Each condition's outcome through held."""
    within = s.graded(*s.clean)
    owed = s.graded([2 * s.edge, s.edge, 1_000], [('srp.bound_advertise.if0', 3 * s.edge)])
    bound = 3 * s.edge
    allowed = bound * (100 + KEPT_MARGIN_PERCENT) // 100
    rule = {name: compared(s.graded([kept, s.edge, 1_000], [('srp.bound_advertise.if0', bound)]))
            for name, kept in (('4 %', bound * 104 // 100), ('6 %', bound * 106 // 100), ('at', allowed),
                               ('past', allowed + 1))}
    integral = {name: compared(s.graded([kept, s.edge, 1_000], [('srp.bound_advertise.if0', 100_000)]))
                for name, kept in (('equal', 105_000), ('over', 105_001))}
    missing = s.graded([1_000, None, 1], [('srp.bound_advertise.if0', s.edge)])
    shared = s.graded(*s.clean, kept_extra=s.over_share, bound_extra=s.over_share)
    bound_shared = s.graded(*s.clean, bound_extra=s.over_share)
    idle = [s.graded(*s.clean, kept_extra=s.idle_over), s.graded(*s.clean, bound_extra=s.idle_over)]
    built = [s.graded(*s.clean, kept_extra=s.build_over), s.graded(*s.clean, bound_extra=s.build_over)]
    whole = [s.graded(*s.clean, kept_extra=s.whole_over), s.graded(*s.clean, bound_extra=s.whole_over)]
    unfinished = s.graded(*s.clean, kept_result='FAIL')
    unmarked = s.graded([1_000, 1_000], [('srp.bound_advertise.if0', s.edge)])
    unmated = s.graded(s.clean[0], [('srp.bound_advertise.if1', s.edge)])
    s.tagged = True
    charged = {name: s.graded([s.charge, s.edge, 1_000], [('srp.bound_advertise.if0', s.charge + extra)])
               for name, extra in (('at', 0), ('past', 1))}
    s.tagged = False
    return [(f'records at the unit by the rule ({s.edge:,} cycles, {s.unit} us), kept <= bound: nothing owed or found',
             within == ([], []), str(within)),
            (f'records whose tagged frames carry Talker values are charged them: at the unit and CTRL_LOOP_SRP_REG_US '
             f'for each of {s.values} ({s.charge:,} cycles, past the unit) they hold, one cycle more is its own '
             f'probe\'s finding', s.values == s.shape.sinks > 0 and charged['at'] == ([], []) and
             charged['past'][0] == [] and only(charged['past'][1], 'srp.bound_advertise.if0', 'over its charge',
                                                f'{s.charge:,}'), str(charged)),
            ('records past their charge with kept <= bound are findings, each its own probe\'s, and nothing is owed',
             owed[0] == [] and len(owed[1]) == 2 and all('over its charge' in f for f in owed[1]) and
             any(f.startswith('srp.kept_advertise') for f in owed[1]) and
             any(f.startswith('srp.bound_advertise') for f in owed[1]), str(owed)),
            ('a kept record 4 % dearer than the bound one holds kept <= bound within the rule\'s 5 %: no finding',
             rule['4 %'][1] == [], str(rule['4 %'])),
            ('a kept record 6 % dearer than the bound one breaks kept <= bound, its own probe\'s, never owed',
             only(rule['6 %'][1], 'kept_advertise', 'kept <= bound broken', f'+{KEPT_MARGIN_PERCENT} %') and
             not any('kept <= bound' in o for o in rule['6 %'][0]), str(rule['6 %'])),
            (f'a kept record at bound + 5 % ({allowed:,} against {bound:,}) holds, one cycle more breaks',
             rule['at'][1] == [] and only(rule['past'][1], 'kept_advertise', 'kept <= bound broken'), str(rule)),
            ('kept exactly bound + 5 % (105,000 against 100,000) holds, 105,001 breaks: the rule is inclusive',
             kept_within(105_000, 100_000) and not kept_within(105_001, 100_000) and integral['equal'][1] == [] and
             only(integral['over'][1], 'kept_advertise', 'kept <= bound broken'), str(integral)),
            ('a probe with no record is a finding, the next probe\'s record not taken for it',
             only(missing[1], 'kept_recount', 'no SRP record'), str(missing)),
            ('a work pass of either group over THE SHARE is a finding of its own, nothing owed',
             shared[0] == [] and len(shared[1]) == 2 and
             all(any(f.startswith(name) and 'work pass' in f and 'THE SHARE' in f for f in shared[1])
                 for name in OWED_KINDS), str(shared)),
            ('a work pass of srp-bound alone over THE SHARE is a finding, nothing owed',
             bound_shared[0] == [] and only(bound_shared[1], kept_window.BOUND, 'work pass', 'THE SHARE'),
             str(bound_shared)),
            ('an idle run over THE SHARE in either group is a finding, never owed, read without a work pass\'s start',
             all(only(f, name, 'idle run', 'THE SHARE') and not any('idle' in o for o in o_)
                 for (o_, f), name in zip(idle, OWED_KINDS)), str(idle)),
            ('a build of one MRPDU one cycle over its stated cost is a finding in srp-kept, never owed',
             only(built[0][1], kept_window.NAME, 'build-one pass', 'over its stated cost') and
             not any('build-one' in o for o in built[0][0]), str(built[0])),
            ('srp-bound\'s build of one MRPDU one cycle over its stated cost is a finding, nothing owed',
             built[1][0] == [] and only(built[1][1], kept_window.BOUND, 'build-one pass', 'over its stated cost'),
             str(built[1])),
            ('a pass given whole to THE TRANSMIT\'s build one cycle over its stated cost is a finding in either group',
             all(only(f, name, 'build pass', 'over its stated cost') and o_ == [] for (o_, f), name in
                 zip(whole, OWED_KINDS)), str(whole)),
            ('an unfinished srp-kept log measures nothing: a finding',
             only(unfinished[1], kept_window.NAME, 'measures nothing'), str(unfinished)),
            ('a probe the point makes that is never marked is a finding',
             only(unmarked[1], 'srp.kept_failed.if0', 'never marked'), str(unmarked)),
            ('a kept probe with no bound record of its own interface is a finding, never a skipped comparison',
             len(unmated[1]) == 5 and sum('kept <= bound is unchecked' in f for f in unmated[1]) == 3 and
             any('srp.bound_advertise.if0: never marked' in f for f in unmated[1]) and
             any('srp.bound_advertise.if1' in f and 'not a probe' in f for f in unmated[1]), str(unmated))]


def standalone(out: Path, logs: dict[str, str | None], beside: str | None = None) -> tuple[int, str]:
    """main's exit and output on a build directory's logs (None: no log), each with that text as its result file
    (None: none); an exception is exit 2."""
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


def disposed(s: Synthetic, out: Path, **extra: tuple[str, ...]) -> tuple[Disposition, list[str], list[str]]:
    """Disposition of both groups' logs with those extra lines, written to out, run.py's STATED lines of them, and those
    that still fail."""
    import run   # its STATED lines, as it prints them (run.stated_misses)
    for name, body in s.texts(*s.clean, **extra).items():
        (out / f'{name}.log').write_text(body)
    logs = {name: grade.parse((out / f'{name}.log').read_text(), s.hz, s.hz) for name in OWED_KINDS}
    lines = run.stated_misses([dict(group=name, passes=dict(slices=slice_grade.held(log, s.shape),
                                                            stated=whole_grade.held(log, s.shape)))
                               for name, log in logs.items()])
    d = Disposition([dict(group=name) for name in OWED_KINDS], out, s.spec)
    return d, lines, d.stated(list(lines))


def unowed(d: tuple[Disposition, list[str], list[str]], cycles: str, count: int) -> bool:
    """Nothing found, and exactly count STATED lines still failing, each THE TRANSMIT slice line of those cycles, none
    of them owed."""
    return (d[0].findings == [] and len(d[2]) == count and all(line.startswith(cycles) for line in d[2]) and
            not any(TRANSMIT_SLICE in o for o in d[0].owed))


def selftest_transmit(s: Synthetic, out: Path) -> list[tuple[str, bool, str]]:
    """Each tier-2 slice of THE TRANSMIT's build over the slice through Disposition, on files in out: none owed since
    #977 charges the registrations; srp-bound's build of one, as whole_grade.held classes it, a finding of its own."""
    one = disposed(s, out, bound_extra=s.slice_one)
    whole = disposed(s, out, bound_extra=s.slice_whole)
    both = disposed(s, out, bound_extra=(*s.slice_one, *s.slice_whole))
    kept_whole = disposed(s, out, kept_extra=s.slice_whole)
    busy = disposed(s, out, bound_extra=s.slice_busy)
    aged = disposed(s, out, bound_extra=s.slice_aged)
    equal = disposed(s, out, bound_extra=s.slice_equal)
    whole_slice = f"{kept_window.BOUND}: {TRANSMIT_SLICE}{s.whole_cycles:,} CPU cycles"
    one_slice = f"{kept_window.BOUND}: {TRANSMIT_SLICE}{s.one_cycles:,} CPU cycles"
    built = f'kept_grade: {kept_window.BOUND}: a build-one pass at bus cycle 9500000: '
    return [(f'srp-bound\'s build of one over the slice ({s.one_cycles:,} against {s.slice:,}): run.py\'s build-one '
             f'and THE TRANSMIT slice lines both fail, and it is a finding, nothing owed',
             one[2][:-1] == one[1] and one[2][-1].startswith(f'{built}{s.one_cycles:,} CPU cycles') and
             len(one[1]) == 2 and any(TRANSMIT_SLICE in line for line in one[1]) and one[0].owed == [], str(one[1:])),
            (f'a srp-bound pass given whole to THE TRANSMIT\'s build, over the slice and within '
             f'CTRL_LOOP_BUILD_PASS_US ({s.whole_cycles:,} against {s.slice:,} and {s.limits["build"]:,}): its slice '
             f'line FAILS, never owed', s.slice < s.whole_cycles <= s.limits['build'] and whole[0].findings == [] and
             len(whole[1]) == 1 and len(whole[2]) == 1 and whole[2][0].startswith(whole_slice) and
             not any(TRANSMIT_SLICE in o for o in whole[0].owed), str(whole[1:])),
            ('srp-bound\'s build of one and its pass given whole, in one log: both fail, nothing owed',
             both[2][:-1] == both[1] and both[2][-1].startswith(f'{built}{s.one_cycles:,} CPU cycles') and
             any(line.startswith(whole_slice) for line in both[2]) and both[0].owed == [], str(both[1:])),
            ('srp-kept\'s pass given whole to THE TRANSMIT\'s build over the slice fails, never owed',
             kept_whole[0].findings == [] and len(kept_whole[2]) == 1 and
             kept_whole[2][0].startswith(f'{kept_window.NAME}: {TRANSMIT_SLICE}'), str(kept_whole[1:])),
            (f'srp-bound\'s build of one over the slice whose AECP round did work '
             f'({whole_grade.ROUND_IDLE_CYCLES + 1:,} cycles, past whole_grade.ROUND_IDLE_CYCLES): no build-one pass, '
             f'its slice line FAILS, never owed',
             unowed(busy, one_slice, 1) and busy[1] == busy[2], str(busy[1:])),
            ('srp-bound\'s build of one over the slice that is an aged step\'s: no build-one pass, its slice line '
             'FAILS, never owed', unowed(aged, one_slice, 1) and aged[1] == aged[2], str(aged[1:])),
            (f'srp-bound\'s build of one and its pass given whole, of equal length ({s.whole_cycles:,}): the build-one '
             f'pass is a finding, both slice lines FAIL, nothing owed',
             equal[0].owed == [] and only(equal[0].findings, kept_window.BOUND, 'build-one pass') and
             equal[2][:-1] == equal[1] and equal[2][-1].startswith(f'{built}{s.whole_cycles:,} CPU cycles') and
             sum(line.startswith(whole_slice) for line in equal[2]) == 2,
             str((equal[1:], equal[0].owed)))]


def selftest_files(s: Synthetic) -> list[tuple[str, bool, str]]:
    """Each condition's outcome through Disposition (run.py's) and the standalone entry point, on files."""
    stated = [f"{kept_window.NAME}: an SRP record's apply of 40,000 CPU cycles, over its stated 28,500",
              f'{kept_window.BOUND}: a walk item of 15,000 CPU cycles, over its stated 12,000',
              f'{kept_window.BOUND}: a build-one pass of {s.one_cycles:,} CPU cycles, over its stated '
              f'{s.limits["build-one"]:,}',
              f"{kept_window.BOUND}: {TRANSMIT_SLICE}{s.one_cycles:,} CPU cycles, over the stated slice {s.slice:,}"]
    kept_build = [f'{kept_window.NAME}: a build-one pass of 81,655 CPU cycles, over its stated 73,500',
                  f"{kept_window.NAME}: a tier-2 slice of THE TRANSMIT's build of 81,655 CPU cycles, over the stated "
                  f'slice 73,500']
    stale = json.dumps(dict(group=kept_window.NAME, passes=dict(share=dict(over_passes=[]))))
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        (out / 'build.json').write_text(json.dumps(s.spec))
        (out / 'results').mkdir()
        alone_clean = standalone(out, s.texts(*s.clean))
        alone_over = [standalone(out, s.texts(*s.clean, kept_extra=s.over_share), beside) for beside in (stale, '{}')]
        alone_idle = standalone(out, s.texts(*s.clean, kept_extra=s.idle_over))
        alone_absent = standalone(out, {**s.texts(*s.clean), kept_window.BOUND: None})
        alone_failed = standalone(out, s.texts(*s.clean, kept_result='FAIL'), stale)
        alone_garbled = standalone(out, {**s.texts(*s.clean), kept_window.NAME: 'NOT-A-LINE 1\nRESULT: PASS\n'})
        transmit = selftest_transmit(s, out)
        built = f'kept_grade: {kept_window.BOUND}: a build-one pass at bus cycle 9500000: {s.one_cycles:,} CPU cycles'
        for name, body in s.texts(*s.clean, bound_extra=s.slice_one).items():
            (out / f'{name}.log').write_text(body)
        pair = Disposition([dict(group=name) for name in OWED_KINDS], out, s.spec)
        pair_left = pair.stated([*stated, *kept_build])
        alone = Disposition([dict(group=kept_window.NAME)], out, s.spec)
        alone_left = alone.stated(list(stated))
        for name, body in s.texts(*s.clean, kept_extra=s.over_share).items():
            (out / f'{name}.log').write_text(body)
        broken = Disposition([dict(group=name) for name in OWED_KINDS], out, s.spec)
        broken_left = broken.stated(list(stated))
    return [('both groups graded together: nothing is owed, each line of either group stays a failure, and '
             'srp-bound\'s build of one over its stated cost is a finding of its own',
             only(pair.findings, kept_window.BOUND, 'build-one pass') and pair.owed == [] and
             pair_left[:-1] == [*stated, *kept_build] and pair_left[-1].startswith(built),
             str((pair.findings, pair_left, pair.owed))),
            *transmit,
            ('one group graded alone is a finding: nothing is owed and every line stays a failure',
             only(alone.findings, 'graded together', 'alone') and alone.owed == [] and
             alone_left[:-1] == stated and len(alone_left) == len(stated) + 1, str((alone.findings, alone_left))),
            ('both groups graded together with a condition broken in a log: the finding stays, nothing is owed',
             only(broken.findings, kept_window.NAME, 'work pass', 'THE SHARE') and broken.owed == [] and
             broken_left[:-1] == stated and len(broken_left) == len(stated) + 1 and
             broken.shares([f'{kept_window.BOUND}: a pass over THE SHARE']) != [] and
             pair.shares([f'{kept_window.BOUND}: a pass over THE SHARE']) != [],
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


def selftest() -> list[tuple[str, bool, str]]:
    """Each condition's outcome on synthetic logs at 1x1/1if and 100 MHz, through held, Disposition and the standalone
    entry point."""
    s = Synthetic()
    return selftest_held(s) + selftest_files(s)


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
    print(f'kept_grade: {"PASS" if not findings else "FAIL"} ({len(findings)} finding(s), {len(owed)} owed: the '
          f'registrations are charged since {DISPOSITION})')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
