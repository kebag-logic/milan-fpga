# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's mutants: each replaces one rule of the grader, the run, the scenario or the
build with a plausible defect, and selftest.py requires a named check to fail under it.

A mutant whose name ends in "(earlier rule)" restores a rule this harness had
before these checks, so its check is the test that fails on that rule. Each
mutant is a function returning the patches it applies.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import re
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import build
import grade
import mrpdu_grade
import notice_window
import poll_grade
import round_grade
import run
import save_grade
import save_window
import scenario
import share
import whole_grade

Patches = Callable[[], list]


def _from_last_erase(flash: list) -> list:
    """A log's flash operations from its last erase on: the last save's."""
    last = max((n for n, (_, op, *_) in enumerate(flash) if op == grade.FLASH_ERASE), default=0)
    return flash[last:]


def _first_save(edit: Callable[[save_grade.Save], dict]) -> list:
    """save_grade.first_save with some of its findings replaced."""
    original = save_grade.first_save

    def first_save(log: grade.Log, n: int = 0) -> save_grade.Save | None:
        """The mutant first save."""
        save = original(log, n)
        return dataclasses.replace(save, **edit(save)) if save is not None else None
    return [patch.object(save_grade, 'first_save', first_save)]


def _save_time(edit: Callable[[dict], dict]) -> list:
    """save_grade.save_time with its finding edited."""
    original = save_grade.save_time
    return [patch.object(save_grade, 'save_time', lambda log, group: (lambda r: r and edit(r))(original(log, group)))]


def _work_steps_unaged(log: grade.Log) -> grade.Log:
    """Every step a work pass carried read as not aged, as grade.parse read a PASS line before its aged field."""
    work = {p.index for p in log.passes}
    log.stepped = [(i, s, c, st, aged and i not in work) for i, s, c, st, aged in log.stepped]
    return log


def _first_pass_only() -> list:
    """The composed window's passes cut to its first: the composed maximum is that pass."""
    original = grade.composed_passes
    return [patch.object(grade, 'composed_passes', lambda log, start, end: original(log, start, end)[:1])]


def _last_pass_dropped() -> list:
    """The log's last work pass dropped, so the worst pass never sees it."""
    original = grade.parse

    def parse(text: str, sys_hz: int, cpu_hz: int) -> grade.Log:
        """The mutant parse: every pass but the last."""
        log = original(text, sys_hz, cpu_hz)
        log.passes = log.passes[:-1]
        return log
    return [patch.object(grade, 'parse', parse)]


def _cut_pass_idle() -> list:
    """The run the script's end flushes counted as whole idle passes."""
    original = grade.parse

    def parse(text: str, sys_hz: int, cpu_hz: int) -> grade.Log:
        """The mutant parse: the cut pass not marked."""
        log = original(text, sys_hz, cpu_hz)
        log.cut_idle = False
        return log
    return [patch.object(grade, 'parse', parse)]


def _load_at_least(group: scenario.Group, got: dict, refused: list, held: int = 0) -> None:
    """A window refused only when it committed fewer records than its defined load."""
    want = grade.defined_load(group.name)
    if any(got[k] < want.get(k, 0) for k in got):
        raise grade.Refusal(f'{group.name}: the composed window committed {got}, its defined load is {want}')


def _load_declared(group: scenario.Group, got: dict, refused: list, held: int = 0) -> None:
    """A window checked against its stimulus's own declaration."""
    want = {name: group.load.get(name, 0) for name in got}
    if got != want:
        raise grade.Refusal(f'{group.name}: the composed window committed {got}, its load is {want}')


def _starved_omitted() -> list:
    """The service rows without the records never released."""
    original = grade.service
    return [patch.object(grade, 'service', lambda *a: [r for r in original(*a) if not r['starved']])]


def _cost_over_recipients() -> list:
    """Each fan-out's cost a recipient divided by its recipients, not the gaps between them."""
    original = grade.grade_probe

    def grade_probe(grader: grade.Grader, probe: scenario.Probe, *a: object) -> dict:
        """The mutant grade_probe: the fan-out's cost recomputed over its recipients."""
        row = original(grader, probe, *a)
        fan = row.get('fanout')
        if fan and fan['recipients']:
            fan['per_recipient_cpu_cycles'] = grader.cpu_cycles(fan['last_sys'] - fan['first_sys']) // fan['recipients']
        return row
    return [patch.object(grade, 'grade_probe', grade_probe)]


def _ahead_never_released() -> list:
    """A served record's records ahead counted as only the earlier records never released."""
    original = grade.service

    def service(grader: grade.Grader, *a: object) -> list[dict]:
        """The mutant service: each row's records ahead recounted without the later releases."""
        rows = original(grader, *a)
        for row in rows:
            records = grade.releases(grader.log, scenario.CH[row['ring']])
            n = next(k for k, (c, *_) in enumerate(records) if c == row['start_sys'])
            row['ahead'] = sum(1 for _, _, r in records[:n] if r is None)
        return rows
    return [patch.object(grade, 'service', service)]


def _maximum_of(keep: Callable[[dict], bool], bound: bool = True) -> Patches:
    """run.composed_maximum over the results keep selects, or never a lower bound."""
    original = run.composed_maximum

    def composed_maximum(results: list[dict]) -> dict | None:
        """The mutant composed maximum."""
        top = original([g for g in results if keep(g)])
        return top if bound or top is None else dict(top, lower_bound=False)
    return lambda: [patch.object(run, 'composed_maximum', composed_maximum)]


def _maximum_edited(edit: Callable[[dict], dict]) -> Patches:
    """run.composed_maximum with its record edited."""
    original = run.composed_maximum

    def composed_maximum(results: list[dict]) -> dict | None:
        """The mutant composed maximum: the record edited."""
        top = original(results)
        return None if top is None else edit(top)
    return lambda: [patch.object(run, 'composed_maximum', composed_maximum)]


def _maximum_line(pattern: str, repl: str) -> Patches:
    """run.table with the pattern replaced in its composed maximum line only."""
    original = run.table

    def table(results: list[dict], point: str) -> str:
        """The mutant table: the composed maximum line rewritten."""
        return '\n'.join(re.sub(pattern, repl, line) if line.startswith('Composed maximum') else line
                         for line in original(results, point).split('\n'))
    return lambda: [patch.object(run, 'table', table)]


def _offer_without(channel: str, groups: str, after: str = '') -> Patches:
    """Group.offer dropping a channel's records, step and declaration together, in the named
    groups (after a mark, if given): a stimulus that omits background work."""
    original = scenario.Group.offer

    def offer(self: scenario.Group, ch: str, step: str, frame: bytes) -> None:
        """The mutant offer: the channel's records in those groups never sent nor declared."""
        if ch == channel and self.name.startswith(groups) and (not after or f'mark {after}' in self.steps):
            return
        original(self, ch, step, frame)
    return lambda: [patch.object(scenario.Group, 'offer', offer)]


def _control_own_path() -> list:
    """A control probe keyed by its own name, not the path it is an instance of."""
    original = scenario.Probe.path_key

    def path_key(self: scenario.Probe) -> tuple[str, int]:
        """The mutant key: a control's name without .if<n>."""
        if self.name.startswith('control.'):
            base, _, suffix = self.name.rpartition('.if')
            return base, int(suffix)
        return original(self)
    return [patch.object(scenario.Probe, 'path_key', path_key)]


def _start_with(rule: Callable) -> Patches:
    """Grader.start with one marker kind replaced by rule(self, probe, after, before), else unchanged."""
    original = grade.Grader.start

    def start(self: grade.Grader, probe: scenario.Probe, interface: int, after: int, before: int) -> int | None:
        """The mutant start: rule's hit, or the original marker where rule leaves it unchanged."""
        hit = rule(self, probe, after, before)
        return original(self, probe, interface, after, before) if hit == 'unchanged' else hit
    return lambda: [patch.object(grade.Grader, 'start', start)]


def _tag_ignored(self: grade.Grader, probe: scenario.Probe, after: int, before: int) -> object:
    if not probe.start.startswith('rxc'):
        return 'unchanged'
    hits = [c for c, k, *_ in self.log.rxc if after <= c < before and k == int(probe.start.split(':')[1])]
    return hits[0] if hits else None


def _timer_posted(self: grade.Grader, probe: scenario.Probe, after: int, before: int) -> object:
    if not probe.start.startswith('deadline'):
        return 'unchanged'
    slot = int(probe.start.split(':')[1])
    hits = [c for c, w in self.log.records if after <= c < before and w[0] & 0xFF == grade.EV_TIMER
            and (w[1] >> 16) & 0xFF == slot]
    return hits[0] if hits else None


def _timer_late(self: grade.Grader, probe: scenario.Probe, after: int, before: int) -> object:
    if not probe.start.startswith('deadline'):
        return 'unchanged'
    slot = int(probe.start.split(':')[1])
    for c, w in self.log.records:
        if after <= c < before and w[0] & 0xFF == grade.EV_TIMER and (w[1] >> 16) & 0xFF == slot:
            return self.log.ms.get(w[2] + 1, self.log.ms.get(w[2]))
    return None


def _entry_any(self: grade.Grader, probe: scenario.Probe, after: int, before: int) -> object:
    if not probe.start.startswith('entry'):
        return 'unchanged'
    hits = [c for c, _ in self.log.entries if after <= c < before]
    return hits[0] if hits else None


def _end_with(rewrite: Callable[[str], str] | None = None, interface_free: bool = False) -> Patches:
    """Grader.end with a resp end read as any TX on the channel, or matched on every interface."""
    original = grade.Grader.end

    def end(self: grade.Grader, spec: str, probe: scenario.Probe, interface: int, start: int,
            before: int) -> int | None:
        """The mutant end: a resp end matched on any interface, or the spec rewritten."""
        if spec.startswith('resp') and interface_free:
            ch, seq = int(spec.split(':')[1]), int(spec.split(':')[2], 16)
            hits = [c for c, k, _, fr in self.log.tx if start <= c <= before and k == ch
                    and grade.response_sequence(fr) == seq]
            return hits[0] if hits else None
        return original(self, rewrite(spec) if rewrite else spec, probe, interface, start, before)
    return lambda: [patch.object(grade.Grader, 'end', end)]


def _owner_oldest(pending: list, cycle: int, refused: list) -> tuple[int, str, int]:
    """The oldest pending frame, those older than 64 cycles dropped while another waits."""
    while len(pending) > 1 and pending[0][3] < cycle - 64:
        refused.append(pending.pop(0))
    return pending.pop(0)[:3] if pending else (-1, '-', 0)


def _recipients_first_any(self: grade.Grader, spec: str, probe: scenario.Probe, start: int,
                          before: int) -> tuple[dict, list]:
    """The first unsolicited AECP frame on any interface ends every recipient."""
    ch = int(spec.split(':')[1])
    hits = [c for c, k, _, fr in self.log.tx if start <= c <= before and k == ch and len(fr) > 37
            and fr[14] == 0xFB and fr[36] & 0x80]
    return {r: hits[0] if hits else None for r in probe.recipients}, []


def _recipients_unchecked() -> list:
    original = grade.Grader.recipients
    return [patch.object(grade.Grader, 'recipients', lambda self, *a: (original(self, *a)[0], []))]


def _missing_ignored() -> list:
    original = grade.fan_out
    return [patch.object(grade, 'fanout_end', lambda found: max((c for c in found.values() if c), default=None)),
            patch.object(grade, 'fan_out', lambda *a: '' if original(*a).startswith('no ') else original(*a))]


def _verdicts(edit: Callable[[dict, float, scenario.Probe], dict]) -> Patches:
    original = grade.verdicts
    return lambda: [patch.object(grade, 'verdicts', lambda ms, probe: edit(original(ms, probe), ms, probe))]


def _run_ignores_traps(log: grade.Log, group: scenario.Group) -> None:
    if log.result != 'PASS' or log.errors:
        raise grade.Refusal(f'{group.name}: the simulation did not complete')


def _recorded_drops(groups: list, out: Path) -> tuple[list, list, list]:
    """A selected group whose log is absent is dropped, silently."""
    kept = [g for g in groups if (out / f'{g.name}.log').exists()]
    stale = [g.name for g in kept if not (out / f'{g.name}.txt').exists()
             or (out / f'{g.name}.txt').read_text() != g.script()]
    return ([g for g in kept if g.name not in stale], [out / f'{g.name}.log' for g in kept if g.name not in stale],
            [f'{name}: stale' for name in stale])


def _reused_checkout_only(build_dir: Path) -> dict:
    """Only an input under the checkout is rechecked; any other key is skipped."""
    spec = json.loads((build_dir / 'build.json').read_text())
    for key, want in spec['inputs'].items():
        path = build.ROOT / key
        if not Path(key).is_absolute() and path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() != want:
            raise RuntimeError(f'reused build is stale: {key} changed')
    if hashlib.sha256((build_dir / 'native/Vsim').read_bytes()).hexdigest() != spec['executable_sha256']:
        raise RuntimeError('reused build is stale: the native model changed')
    return spec


def _first_instance(results: list[dict]) -> list[dict]:
    """Each path reported at its first measured instance."""
    out: dict = {}
    for group in results:
        for r in group['probes']:
            if r['status'] == 'measured':
                entry = out.setdefault(tuple(r['path']), dict(path=r['path'][0], interface=r['path'][1],
                                                              row=r['row'], instances=0, misses=0,
                                                              worst=dict(r, group=group['group'])))
                entry['instances'] += 1
                entry['misses'] += not r['within_budget']
    return list(out.values())


def _counts_per_instance() -> list:
    original = run.counts
    return [patch.object(run, 'counts', lambda results: dict(original(results),
                                                              path_misses=original(results)['instance_misses']))]


def _verdict(refusals_fail: bool, misses_fail: bool) -> Patches:
    def verdict(args: object, groups: list, refusals: list, misses: list, shares: list = (), late: list = ()) -> int:
        """The mutant exit status: refusals or misses fail only where the flags say; a late save or notice fails."""
        if late or refusals_fail and (refusals or not groups):
            return 1
        if shares and not args.record_share_findings:
            return 1
        return 1 if misses_fail and misses and not args.record_budget_findings else 0
    return lambda: [patch.object(run, 'verdict', verdict)]


def _shares_seen(keep: Callable[[object, list], bool]) -> Patches:
    """run.verdict handed the passes over the share only where keep(args, misses) says."""
    original = run.verdict

    def verdict(args: object, groups: list, refusals: list, misses: list, shares: list = (), late: list = ()) -> int:
        """The mutant exit status: the passes over the share dropped unless keep holds."""
        return original(args, groups, refusals, misses, shares if keep(args, misses) else [], late)
    return lambda: [patch.object(run, 'verdict', verdict)]


def _fetch_bus_cacheless(spec: dict) -> tuple[list, int]:
    """The cacheless CPU's observers and one beat a command, whatever the CPU fetches through."""
    return list(build.ACCESSORS), 1


def _lsu_bus_cacheless(rows: list, netlist: str) -> list:
    """The cacheless LSU's observers, whatever the CPU's load/store plugin."""
    return rows


def _fetch_bus_one_beat(spec: dict, original: Callable = build.fetch_bus) -> tuple[list, int]:
    """The CPU's own fetch observers, with one beat a refill instead of its line's words."""
    return original(spec)[0], 1


def _built_as_without_cache(spec: dict) -> tuple:
    """A reused build's identity without its fetch L1 and arm."""
    return (spec['shape'], spec['interfaces'], spec['cpu_regions'], spec['mutation'], spec['variant'], 'none', False)


def _selected_without_cache(args: object, shape: str, n_if: int) -> tuple:
    """The selected build's identity without its fetch L1 and arm."""
    return shape, n_if, args.cpu_regions, args.mutation, args.variant, 'none', False


def _build_recorded(edit: Callable[[dict], dict]) -> Patches:
    """build.build with its build.json record edited, on disk and returned."""
    original = build.build

    def build_(build_dir: Path, *a: object, **k: object) -> dict:
        """The mutant build: its record edited."""
        spec = edit(original(build_dir, *a, **k))
        (build_dir / 'build.json').write_text(json.dumps(spec, indent=2) + '\n')
        return spec
    return lambda: [patch.object(build, 'build', build_)]


def _build_with(edit: Callable[[build.Core], build.Core]) -> Patches:
    """build.build handed an edited selection: it builds a CPU or arm other than the one selected."""
    original = build.build

    def build_(build_dir: Path, *a: object, core: build.Core = build.Core(), **k: object) -> dict:
        """The mutant build: the selection edited before it is built and recorded."""
        return original(build_dir, *a, core=edit(core), **k)
    return lambda: [patch.object(build, 'build', build_)]


def _refusals_kept(keep: Callable[[str], bool]) -> Patches:
    """build.cpu_clock_refusals keeping only the refusals keep(refusal) holds for."""
    original = build.cpu_clock_refusals
    return lambda: [patch.object(build, 'cpu_clock_refusals', lambda spec: [r for r in original(spec) if keep(r)])]


def _reuse_unchecked() -> Patches:
    """build.reused without the CPU clock refusal; a new build keeps it."""
    original = build.reused

    def reused(build_dir: Path) -> dict:
        """The mutant reuse: any CPU clock is taken."""
        with patch.object(build, 'cpu_clock_refusals', lambda spec: []):
            return original(build_dir)
    return lambda: [patch.object(build, 'reused', reused)]


MUTANTS: dict[str, Patches] = {
    'marker: the frame tag is ignored': _start_with(_tag_ignored),
    'marker: a timer path starts when its record is posted': _start_with(_timer_posted),
    'marker: a timer path starts one millisecond after its deadline': _start_with(_timer_late),
    'marker: an entry start takes any function entry': _start_with(_entry_any),
    'marker: any response on the channel ends the path': _end_with(lambda s: 'tx:' + s.split(':')[1]
                                                                   if s.startswith('resp') else s),
    'marker: the interface is ignored': _end_with(interface_free=True),
    'marker: the first required output ends the path': lambda: [patch.object(grade, 'combine_ends', min)],
    'marker: a receive commit goes to the oldest pending frame (earlier rule)':
        lambda: [patch.object(grade, 'owner', _owner_oldest)],
    'marker: the expected-response check is skipped': lambda: [patch.object(grade, 'expectation', lambda *a: '')],
    "notify: the first recipient's commit ends the fan-out": lambda: [patch.object(grade, 'fanout_end', lambda f:
                                                                      min(f.values()) if None not in f.values()
                                                                      else None)],
    'notify: the first unsolicited response on any interface ends it (earlier rule)':
        lambda: [patch.object(grade.Grader, 'recipients', _recipients_first_any)],
    'notify: any unsolicited response counts as the change': lambda: [patch.object(
        grade, 'causal', lambda fr, *a: len(fr) > 37 and fr[14] == 0xFB and fr[15] & 0xF == 1 and bool(fr[36] & 0x80))],
    'notify: a missing recipient is not refused': _missing_ignored,
    'notify: a recipient outside the set is not refused': _recipients_unchecked,
    'clock ratio: CPU cycles equal bus cycles': lambda: [patch.object(grade.Grader, 'cpu_cycles', lambda self, n: n)],
    'clock ratio: inverted': lambda: [patch.object(grade.Grader, 'cpu_cycles',
                                                   lambda self, n: n * self.log.sys_hz // self.log.cpu_hz)],
    'clock ratio: CPU cycles rounded down': lambda: [patch.object(
        grade.Grader, 'cpu_cycles', lambda self, n: n * self.log.cpu_hz // self.log.sys_hz)],
    'clock ratio: milliseconds from the CPU clock': lambda: [patch.object(
        grade.Grader, 'ms', lambda self, n: n * 1000.0 / self.log.cpu_hz)],
    "clock ratio: a pass's milliseconds from the bus clock": lambda: [patch.object(
        grade.Grader, 'cpu_ms', lambda self, n: n * 1000.0 / self.log.sys_hz)],
    "clock ratio: a pass's bus cycles equal its CPU cycles": lambda: [patch.object(grade.Grader, 'bus_cycles',
                                                                                   lambda self, n: n)],
    'pass bound: it starts at the input, not at the running pass': lambda: [patch.object(
        grade.Grader, 'pass_origin', lambda self, start: start)],
    "composition: the window's population is not checked": lambda: [patch.object(grade, 'check_load',
                                                                                 lambda *a: None)],
    "composition: the composed maximum is the run's worst pass": lambda: [patch.object(
        grade, 'composed_passes', lambda log, start, end: log.passes)],
    "composition: the composed maximum is the window's first pass": _first_pass_only,
    "worst pass: the run's last pass is dropped": _last_pass_dropped,
    "passes: the pass the script's end cuts counts as idle (earlier rule)": _cut_pass_idle,
    'composition: a window that committed more than its load is accepted': lambda: [patch.object(
        grade, 'check_load', _load_at_least)],
    "composition: the load is the stimulus's own declaration (earlier rule)": lambda: [patch.object(
        grade, 'check_load', _load_declared)],
    "pacing: an AECP group's frames meet an empty token bucket": lambda: [patch.object(
        scenario, 'paced', lambda g, channel: g)],
    'flash: a cached window is taken': lambda: [patch.object(
        build, 'flash_window_refusals', lambda spec: [])],
    'flash: the hybrid-XIP arm is held to the uncached window': lambda: [patch.object(
        build, 'flash_window_refusals', lambda spec, f=build.flash_window_refusals: f({**spec, 'xip': False}))],
    'opening: a backlog window opens without waiting for the drained event ring': lambda: [patch.object(
        scenario, 'OPEN_WINDOW', ('gap 1', 'mark composed'))],
    'opening: the window opens with records held': lambda: [patch.object(
        scenario, 'OPEN_WINDOW', (f'wait events 2 within {400 * scenario.MS}', 'gap 1', 'mark composed'))],
    'opening: the records released are not counted': lambda: [patch.object(
        grade.Grader, 'events_held', lambda self, start: sum(1 for c, _ in self.log.records if c < start))],
    'opening: the refusal does not name the records held': lambda: [patch.object(
        grade, 'check_load', lambda group, got, refused, held=0, f=grade.check_load: f(group, got, refused))],
    'composition: the backlog stimulus omits SRP': _offer_without('srp', 'backlog'),
    'composition: the backlog stimulus omits MAAP': _offer_without('maap', 'backlog'),
    'composition: the owed row omits the ACMP commands behind its input (earlier rule)': _offer_without(
        'acmp', 'backlog-owed', after='backlog.owed.if0'),
    'service: a record never released is omitted': _starved_omitted,
    'service: a window that left its load unreleased reports it released (earlier rule)': lambda: [patch.object(
        grade, 'unreleased', lambda *a: {})],
    'composition: the composed maximum is taken over the windows that released their load (earlier rule)':
        _maximum_of(lambda g: (g['passes'].get('composed') or {}).get('serviced', False)),
    'composition: the composed maximum is no lower bound where a window left its load unreleased': _maximum_of(
        lambda g: True, bound=False),
    "composition: the composed maximum includes the fixture's short window": lambda: [patch.object(
        grade, 'BACKLOG_ROWS', grade.COMPOSED_ROWS)],
    'composition: the composed maximum is a lower bound only where its own window left its load unreleased':
        _maximum_edited(lambda top: dict(top, lower_bound=top['group'] in top['unreleased'])),
    'composition: the composed maximum does not name the backlog rows a run did not include': _maximum_edited(
        lambda top: dict(top, not_run=[], partial=False)),
    'tables: results.json omits the composed maximum': lambda: [patch.object(
        run, 'summary', lambda *a, f=run.summary: dict(f(*a), composed_maximum=None))],
    'tables: the composed maximum line drops its lower-bound label': _maximum_line(
        r'at least |, a lower bound \(load unreleased in [^)]*\)', ''),
    'tables: the composed maximum line drops its partial label': _maximum_line(
        r'(\d+) of \d+ backlog windows, a partial figure \([^)]*\)', r'the \1 backlog windows'),
    'service: the records ahead count only those never released': _ahead_never_released,
    'notify: the cost a recipient divides by the recipients, not the gaps': _cost_over_recipients,
    "service: a record's service ends at its release, not at its pass's end": lambda: [patch.object(
        grade, 'served', lambda grader, taking, released: released)],
    'owed: the responses ahead are not checked': lambda: [patch.object(
        grade, 'owed_ahead', lambda grader, probe, *a: list(probe.owed))],
    'owed: a command never answered fits': lambda: [patch.object(
        grade, 'never_answered', lambda grader, probe, row, start: dict(row, status='measured', ms=0.0, start_sys=start,
                                                                        within_budget=True, within_ceiling=True))],
    'notify: the fan-out registers one controller an interface (earlier rule)': lambda: [patch.object(
        scenario, 'registrations', lambda: 1)],
    'deadline: T_svc pinned at the 10 ms proposal (earlier rule)': lambda: [patch.object(scenario, 'T_SVC_MS', 10.0)],
    'deadline: each family graded against its ceiling alone, not T_svc': lambda: [patch.object(
        grade, 'budget_ms', lambda probe: scenario.CEILING_MS[probe.family] + probe.wait_ms)],
    'deadline: strictly below the budget': _verdicts(lambda v, ms, probe: dict(v, within_budget=ms < v['budget_ms'])),
    'deadline: the normative wait is not added': _verdicts(lambda v, ms, probe: dict(
        v, within_budget=ms <= min(scenario.T_SVC_MS, scenario.CEILING_MS[probe.family]))),
    'deadline: the ceiling drops the normative wait': _verdicts(lambda v, ms, probe: dict(
        v, within_ceiling=ms <= scenario.CEILING_MS[probe.family])),
    'deadline: the ACMP ceiling is the transaction timeout': lambda: [patch.dict(scenario.CEILING_MS, {'acmp': 200.0})],
    'run: a CPU trap is not refused': lambda: [patch.object(grade, 'refuse_run', _run_ignores_traps)],
    'run: a budget miss never fails the run': _verdict(refusals_fail=True, misses_fail=False),
    'run: a refusal does not fail the run': _verdict(refusals_fail=False, misses_fail=True),
    'run: the as-built control is caught by an instruction access fault only (earlier rule)': lambda: [patch.object(
        run, 'AS_BUILT_CAUSES', (1,))],
    'run: the as-built control is caught by any trap': lambda: [patch.object(
        run, 'as_built_faults', lambda refusals: [r for r in refusals if 'trapped' in r])],
    "run: the as-built control matches the cause's leading digit": lambda: [patch.object(
        run, 'as_built_faults', lambda refusals: [r for r in refusals if re.search(r'TRAP \d+ 0 [15]', r)])],
    'run: the as-built control is caught whatever the boot does': lambda: [patch.object(
        run, 'as_built_faults', lambda refusals: ['planted'])],
    'regrade: a selected group without its log is dropped (earlier rule)':
        lambda: [patch.object(run, 'recorded', _recorded_drops)],
    'reuse: an input outside the checkout is not rechecked (earlier rule)':
        lambda: [patch.object(build, 'reused', _reused_checkout_only)],
    'reuse: the ROM files are not attested': lambda: [patch.object(
        build, 'run_inputs', lambda d, spec, f=build.run_inputs: [p for p in f(d, spec) if p.suffix != '.init'])],
    "tables: a path's first instance is reported, not its worst (earlier rule)":
        lambda: [patch.object(run, 'paths', _first_instance)],
    'tables: misses are counted per probe instance only (earlier rule)': _counts_per_instance,
    'tables: a control instance is its own path (earlier rule)': _control_own_path,
    "tables: a starved instance is not its path's worst": lambda: [patch.object(
        run, 'severity', lambda r: (False, r['ms']))],
    'build: the 1x1 point names the ledgered override too': lambda: [patch.dict(
        build.LEDGERED_POINTS, {('endstation_ax7101_1x1_tdm8', 1): '8x8-two-interfaces'})],
    "build: arm B anchors the fixture's own observation callbacks (earlier rule)": lambda: [patch.dict(
        build.VARIANTS, {'answering-ports': [(
            '{ (void)ctx; (void)i; (void)t; (void)n; (void)v; return false; }\nstatic bool a_avb',
            '{ (void)ctx; (void)i; (void)t; (void)n; memset(v, 0, sizeof *v); return true; }\nstatic bool a_avb')]})],
    'fetch bus: the cacheless observers on a cached CPU':
        lambda: [patch.object(build, 'fetch_bus', _fetch_bus_cacheless)],
    'fetch bus: one beat a refill': lambda: [patch.object(build, 'fetch_bus', _fetch_bus_one_beat)],
    'lsu bus: the cacheless observers on a data-cached CPU':
        lambda: [patch.object(build, 'lsu_bus', _lsu_bus_cacheless)],
    'reuse: the fetch L1 and the arm are not compared':
        lambda: [patch.object(run, 'built_as', _built_as_without_cache),
                 patch.object(run, 'selected', _selected_without_cache)],
    'reuse: a reused build is not compared with the selection': lambda: [
        patch.object(run, 'built_as', lambda spec: ()), patch.object(run, 'selected', lambda *a: ())],
    'build: an XIP build records the block-RAM arm': _build_recorded(lambda spec: dict(spec, xip=False)),
    "build: the CPU is built with the split's cache whatever the selection": _build_with(
        lambda core: dataclasses.replace(core, fetch_l1='split')),
    'xip: the reset entry moves to flash with the other code': lambda: [patch.object(
        build, 'XIP_TEXT', (build.XIP_TEXT[0], build.XIP_TEXT[1].replace('} > rom', '} > flash')))],
    'xip: the flash driver moves to flash with the other code': lambda: [patch.object(build, 'XIP_TEXT', (
        build.XIP_TEXT[0], build.XIP_TEXT[1].replace(' *-nvm_flash_litespi.o(.text .text.*)', '')))],
    'xip: the hot code and the rest stay in rom': lambda: [patch.object(
        build, 'XIP_END', (build.XIP_END[0], build.XIP_END[0]))],
    'share: the bound over eight passes': lambda: [patch.object(share, 'SHARE_PASSES', 8)],
    'share: a pass at the share is over it': lambda: [patch.object(
        share, 'share_cycles', lambda hz, f=share.share_cycles: f(hz) - 1)],
    'share: in bus cycles, not CPU time': lambda: [patch.object(
        share, 'share_cycles', lambda hz, f=share.share_cycles: f(100_000_000))],
    'share: the passes are not held to it': lambda: [patch.object(
        grade, 'pass_share', lambda log, f=grade.pass_share: dict(f(log), over=0, over_passes=[]))],
    'share: a pass over it is no finding': lambda: [patch.object(run, 'share_misses', lambda results: [])],
    'share: the planted store step is judged as a budget control': lambda: [patch.object(build, 'SHARE_CONTROLS', ())],
    'share: a pass with no mailbox write is not held to it': lambda: [patch.object(
        grade, 'pass_share', lambda log, f=grade.pass_share: f(dataclasses.replace(log, idle=[])))],
    "load: any window may hold the flood's last change": lambda: [patch.object(
        save_window, 'aged_age', lambda name: 2)],
    "load: an aged window may hold no more than its row's": lambda: [patch.object(
        save_window, 'aged_age', lambda name: None)],
    'stated: no pass is held to its cost': lambda: [patch.object(
        whole_grade, 'held', lambda log, n, f=whole_grade.held: dict(f(log, n), over=[]))],
    'stated: a pass over its cost is no finding': lambda: [patch.object(run, 'stated_misses', lambda results: [])],
    "stated: one point's costs at both": lambda: [patch.object(
        whole_grade, 'stated_us', lambda interfaces, f=whole_grade.stated_us: f(2))],
    "stated: a build of one is held to a build of two's cost": lambda: [patch.object(
        whole_grade, 'COSTS', dict(whole_grade.COSTS, **{'build-one': whole_grade.COSTS['build']}))],
    'stated: a pass whose round did something is held too': lambda: [patch.object(
        whole_grade, 'round_idle', lambda modules: True)],
    'stated: a round that found nothing leaves no work alone': lambda: [patch.object(
        whole_grade, 'ROUND_IDLE_CYCLES', 0)],
    "stated: an aged step's silent pass is not held": lambda: [patch.object(
        whole_grade, 'held', lambda log, n, f=whole_grade.held: f(dataclasses.replace(
            log, stepped=[s for s in log.stepped if s[1] in {p.start_sys for p in log.passes}]), n))],
    'stated: an aged step is not held': lambda: [patch.object(
        whole_grade, 'held', lambda log, n, f=whole_grade.held: f(dataclasses.replace(log, stepped=[]), n))],
    'stated: in bus cycles, not CPU time': lambda: [patch.object(
        whole_grade, 'held', lambda log, n, f=whole_grade.held: f(dataclasses.replace(log, cpu_hz=2 * log.cpu_hz), n))],
    "save: a save's window carries no defined load": lambda: [patch.object(save_window, 'row', lambda name: name)],
    'save: a window outside its flash phase is graded': lambda: [patch.object(grade, 'save_phase', lambda *a: None)],
    'save: the phase read off the last save, not the first': lambda: [patch.object(
        grade, 'save_phase', lambda log, name, start, f=grade.save_phase: f(dataclasses.replace(
            log, flash_ops=_from_last_erase(log.flash_ops)), name, start))],
    "save: the program phase ends at the window's last page, not the save's": lambda: [patch.object(
        grade, 'save_phase', lambda log, name, start, f=grade.save_phase: f(dataclasses.replace(
            log, flash_ops=[op for op in log.flash_ops if op[0] < start]), name, start))],
    "save: a verify window is graded after its read-backs read back the container": lambda: _first_save(
        lambda save: dict(verified=[])),
    "save: the bound counts one tick a step, not the age limit's": lambda: [patch.object(
        save_window, 'step_age', lambda: 0)],
    "save: the bound leaves out the verify's read-backs": lambda: [patch.object(
        save_window, 'steps', lambda image, records, f=save_window.steps: f(image, records)
        - -(-image // save_window.READ))],
    "save: durable at the verify's first read-back, not the one that completes it": lambda: _first_save(
        lambda save: dict(durable=save.verified[0][0] if save.verified else None)),
    'save: a save never durable in the run is within its bound': lambda: _save_time(
        lambda r: dict(r, within=r['within'] or r['ms'] is None)),
    'save: a save over its stated worst case is no finding': lambda: [patch.object(
        run, 'save_misses', lambda results: [])],
    "save: the age limit's plant is judged as a budget control": lambda: [patch.object(build, 'SAVE_CONTROLS', ())],
    'save: a held group that commits fewer records than it offered is graded': lambda: [patch.object(
        save_grade, 'held_load', lambda log, group: None)],
    'save: a channel left out of the held load': lambda: [patch.object(
        save_window, 'arrivals', lambda p, run_ms, f=save_window.arrivals: [
            a for a in f(p, run_ms) if a[1] != 'srp'])],
    'save: the held load a burst once, then nothing': lambda: [patch.object(
        save_window, 'arrivals', lambda p, run_ms, f=save_window.arrivals: [
            a for a in f(p, run_ms) if a[0] < 1])],
    "save: the in-flight change's bound leaves out the save in flight": lambda: [patch.object(
        save_window, 'bound_ms', lambda image, records, age=None, flight=None, f=save_window.bound_ms: f(
            image, records, age))],
    "save: the in-flight change waits for every step of the save in flight": lambda: [patch.object(
        save_window, 'bound_ms', lambda image, records, age=None, flight=None, f=save_window.bound_ms: f(
            image, records, age, flight) + (60 if flight else 0))],
    "save: the in-flight change's wait not its first-dirty window where that is longer": lambda: [patch.object(
        save_window, 'bound_ms', lambda image, records, age=None, flight=None, f=save_window.bound_ms: f(
            image, records, age) if flight is None else 30 * (save_window.steps(image, flight) - 2
                                                             + save_window.steps(image, records)) + 10)],
    'save: the second change timed to the save in flight': lambda: [patch.object(
        save_grade, 'first_save', lambda log, n=0, f=save_grade.first_save: f(log, 0))],
    'save: a second change not marked while the save is in flight is graded': lambda: [patch.object(
        save_grade, 'in_flight', lambda log, marks, change: True)],
    'save: the second change the same name as the first': lambda: [patch.object(
        save_window, 'set_name', lambda p, value=b'save', f=save_window.set_name: f(p))],
    "save: the second change marked before the save in flight's capture": lambda: [patch.object(
        save_window, 'SECOND_MS', 500)],
    'aged: the opening age counts TICK records, not their centiseconds': lambda: [patch.object(
        save_grade, 'opening_age', lambda log, last, start: sum(
            1 for c, w in log.records if last < c <= start and w[0] & 0xFF == save_grade.EV_TICK))],
    "aged: the age counted from the window's lead, not from its last step": lambda: [patch.object(
        save_grade, 'opening_age', lambda log, last, start, f=save_grade.opening_age: f(log, 0, start))],
    'aged: a pass that took nothing before the window does not end the age': lambda: [patch.object(
        save_grade, 'empty_passes', lambda log, index, start: [])],
    "aged: a window opened at another age than its name declares is graded": lambda: [patch.object(
        save_grade, 'aged_refusal', lambda name, age, got, empty, inside, *rest, f=save_grade.aged_refusal: f(
            name, age, age, empty, inside))],
    "aged: an aged step's work pass is read as not aged": lambda: [patch.object(
        grade, 'parse', lambda *a, f=grade.parse, **k: _work_steps_unaged(f(*a, **k)))],
    'aged: a window at the limit that drains before its aged step is refused': lambda: [patch.object(
        save_grade, 'aged_refusal', lambda name, age, got, empty, inside, *rest, f=save_grade.aged_refusal: f(
            name, age, got, empty, [a for a in inside if a['among']], *rest))],
    'aged: a window at the age limit with no aged step in it is graded': lambda: [patch.object(
        save_grade, 'aged_refusal', lambda name, age, got, empty, inside, *rest, f=save_grade.aged_refusal: f(
            name, age, got, empty, inside or [dict(kind=k) for k in save_grade.AGED_KIND.values()], *rest))],
    'aged: a window that closed before its centisecond is refused': lambda: [patch.object(
        save_grade, 'aged_refusal', lambda name, age, got, empty, inside, ticked=True, f=save_grade.aged_refusal: f(
            name, age, got, empty, inside, True))],
    'aged: a step a pass that took nothing ran is not counted': lambda: [patch.object(
        save_grade, 'plain_steps', lambda log, start, end: [])],
    "aged: the program phase's aged step need not be a page's issue": lambda: [patch.dict(
        save_grade.AGED_KIND, program='read-back')],
    "aged: the heavier aged step's plant is judged as a budget control": lambda: [patch.object(
        build, 'AGED_CONTROLS', ())],
    "notice: a retried notice later than its bound is a budget finding only": lambda: [patch.object(
        run, 'notice_misses', lambda results, interfaces: [])],
    'notice: a retried notice is held to its ceiling, not its bound': lambda: [patch.object(
        run, 'notice_misses', lambda results, interfaces: [n['group'] for n in run.notices(results)
                                                       if not n['within_ceiling']])],
    "notice: the age-less plant is judged as a budget control": lambda: [patch.object(build, 'NOTICE_CONTROLS', ())],
    "notice: the port answers before the load": lambda: [patch.object(
        notice_window, 'ANSWER_MS', notice_window.LOAD_MS - 1)],
    "transmit: the aged build's plant is judged as a budget control": lambda: [patch.object(
        build, 'SRP_CONTROLS', ())],
    "transmit: any row over its bound catches the aged build's plant": lambda: [
        patch.object(run, 'mrpdu_groups', lambda misses: {m.partition(':')[0].partition('.')[0] for m in misses})],
    "transmit: a timer's row ends at the first build, with no frame": lambda: [patch.object(
        mrpdu_grade, 'commits', lambda grader, entry: [])],
    "transmit: a timer's row starts at its entry, not at the deadline": lambda: [patch.object(
        mrpdu_grade, 'ticks', lambda log: [c for c, _ in log.entries])],
    "notice: a queued notice's bound is the first's": lambda: [patch.object(
        notice_window, 'queued_ms', lambda interfaces: scenario.T_SVC_MS)],
    "notice: the first of a queue is held to the queue's bound": lambda: [patch.object(
        notice_window, 'queued_first_ms', notice_window.queued_ms)],
    'notice: the first of a queue is held to T_svc at both points (earlier rule)': lambda: [patch.object(
        notice_window, 'queued_first_ms', lambda interfaces: scenario.T_SVC_MS)],
    'round: no round is held to its cost': lambda: [patch.object(
        round_grade, 'held', lambda log, n, f=round_grade.held: dict(f(log, n), over=[]))],
    'round: a refused attempt is free': lambda: [patch.object(
        round_grade, 'stated_us', lambda interfaces, f=round_grade.stated_us: dict(f(interfaces), attempt=0))],
    "round: one point's costs at both": lambda: [patch.object(
        round_grade, 'stated_us', lambda interfaces, f=round_grade.stated_us: f(2))],
    'round: the notices it built are not counted': lambda: [patch.object(round_grade, 'BUILT', 'aecp:none')],
    'round: calls outside it are counted': lambda: [patch.object(
        round_grade, 'inside', lambda cycles, start, end: len(cycles))],
    'round: in bus cycles, not CPU time': lambda: [patch.object(
        round_grade, 'held', lambda log, n, f=round_grade.held: f(dataclasses.replace(log, cpu_hz=2 * log.cpu_hz), n))],
    'polls: no base is held to its cost': lambda: [patch.object(
        poll_grade, 'held', lambda log, n, f=poll_grade.held: (lambda r: dict(r, over=[
            o for o in r['over'] if o['kind'] != 'base']))(f(log, n)))],
    'polls: no item is held to its cost': lambda: [patch.object(
        poll_grade, 'held', lambda log, n, f=poll_grade.held: (lambda r: dict(r, over=[
            o for o in r['over'] if o['kind'] == 'base']))(f(log, n)))],
    'polls: the items are not taken from the base': lambda: [patch.object(
        poll_grade, 'instances', lambda log, traced, commits, start, end: [])],
    'polls: an ACMP or AECP call that sent nothing is an item': lambda: [patch.dict(
        poll_grade.ITEMS, acmp=('acmp_mbx:on_poll', None), aecp=('aecp:transmit', None))],
    'polls: an item after the polls is theirs': lambda: [patch.object(
        poll_grade, 'sections', lambda traced, f=poll_grade.sections: [(s, e + 10_000, ss) for s, e, ss in f(traced)])],
    'polls: an item nested in another is counted twice': lambda: [patch.object(
        poll_grade, 'outermost', lambda found: [(kind, e - s) for s, e, kind in found])],
    "polls: one point's costs at both": lambda: [patch.object(
        poll_grade, 'stated_us', lambda interfaces, f=poll_grade.stated_us: f(2))],
    'polls: in bus cycles, not CPU time': lambda: [patch.object(
        poll_grade, 'held', lambda log, n, f=poll_grade.held: f(dataclasses.replace(log, cpu_hz=2 * log.cpu_hz), n))],
    'aged: one delay an aged window': lambda: [patch.object(save_window, 'AGED_DELAYS', (5.0,))],
    "aged: the delays across the tick's first 8.75 ms only": lambda: [patch.object(
        save_window, 'AGED_DELAYS', tuple(1.25 * n for n in range(8)))],
    'aged: windows at the age limit only': lambda: [patch.object(
        save_window, 'aged_windows', lambda p, ages=None, f=save_window.aged_windows: f(p, (save_window.step_age(),)))],
    "aged: the program phase's window one step short of a page's issue": lambda: [patch.object(
        save_window, 'AGED_LEAD', 1)],
    'steps: a pass that carries a step and writes nothing to the mailbox is left out': lambda: [patch.object(
        save_grade, 'step_figures', lambda grader, f=save_grade.step_figures: f(grade.Grader(dataclasses.replace(
            grader.log, step_passes=[]))))],
    'steps: a work pass that carries a step is left out': lambda: [patch.object(
        save_grade, 'step_figures', lambda grader, f=save_grade.step_figures: f(grade.Grader(dataclasses.replace(
            grader.log, passes=[]))))],
    "save: the held AECP channel bursts with its change, the SET_NAME's token not yet back": lambda: [patch.object(
        save_window, 'held_start', lambda: 0)],
    'save: the starved save without its grandmaster flood': lambda: [patch.object(
        save_window, 'loaded', lambda p, name, flood, image, f=save_window.loaded: f(p, name, False, image))],
    'save: four tick phases a flash phase': lambda: [patch.object(save_window, 'TICK_PHASES', 4)],
    "save: the program phase spread across one tick, not its step's two": lambda: [patch.dict(
        save_window.PHASES, program=('program 1', 30, 10))],
    'save: the blank check staged after the first page program': lambda: [patch.dict(
        save_window.PHASES, blank=('program 1', 30, 10))],
    'save: the verify staged while the pages are programmed': lambda: [patch.dict(
        save_window.PHASES, verify=('program 1', 10, 10))],
    'share: the rows option records the passes too': _shares_seen(lambda args, misses: not args.record_budget_findings),
    'share: a pass over it fails the run only beside a row miss': _shares_seen(lambda args, misses: bool(misses)),
    'clock: the CPU is built on the Milan clock': _build_with(
        lambda core: dataclasses.replace(core, cpu_cd='milan')),
    "clock: build.json records the point's Milan clock as the CPU's": _build_recorded(
        lambda spec: dict(spec, cpu_hz=spec['milan_hz'])),
    'clock: no CPU clock refusal': lambda: [patch.object(build, 'cpu_clock_refusals', lambda spec: [])],
    "clock: the CPU's domain is not checked": _refusals_kept(lambda refusal: 'domain' not in refusal),
    "clock: the CPU's clock is not checked against the bus clock": _refusals_kept(lambda refusal: 'domain' in refusal),
    'clock: a reused build is not checked': _reuse_unchecked(),
}
