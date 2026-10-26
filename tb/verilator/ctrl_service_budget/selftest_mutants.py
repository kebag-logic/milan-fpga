# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's mutants: each replaces one rule of the grader, the run, the scenario or the
build with a plausible defect, and selftest.py requires a named check to fail under it.

A mutant whose name ends in "(earlier rule)" restores a rule this harness had
before these checks, so its check is the test that fails on that rule. Each
mutant is a function returning the patches it applies.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import build
import grade
import run
import scenario

Patches = Callable[[], list]


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


def _load_at_least(group: scenario.Group, got: dict, refused: list) -> None:
    """A window refused only when it committed fewer records than its defined load."""
    want = grade.defined_load(group.name)
    if any(got[k] < want.get(k, 0) for k in got):
        raise grade.Refusal(f'{group.name}: the composed window committed {got}, its defined load is {want}')


def _load_declared(group: scenario.Group, got: dict, refused: list) -> None:
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
                entry['misses'] += not r['within_t_svc']
    return list(out.values())


def _counts_per_instance() -> list:
    original = run.counts
    return [patch.object(run, 'counts', lambda results: dict(original(results),
                                                              path_misses=original(results)['instance_misses']))]


def _verdict(refusals_fail: bool, misses_fail: bool) -> Patches:
    def verdict(args: object, groups: list, refusals: list, misses: list) -> int:
        """The mutant exit status: refusals or misses fail only where the flags say."""
        if refusals_fail and (refusals or not groups):
            return 1
        return 1 if misses_fail and misses and not args.record_budget_findings else 0
    return lambda: [patch.object(run, 'verdict', verdict)]


def _fetch_bus_cacheless(spec: dict) -> tuple[list, int]:
    """The cacheless CPU's observers and one beat a command, whatever the CPU fetches through."""
    return list(build.ACCESSORS), 1


def _fetch_bus_one_beat(spec: dict, original: Callable = build.fetch_bus) -> tuple[list, int]:
    """The CPU's own fetch observers, with one beat a refill instead of its line's words."""
    return original(spec)[0], 1


def _built_as_without_cache(spec: dict) -> tuple:
    """A reused build's identity without its fetch L1 and arm."""
    return (spec['shape'], spec['interfaces'], spec['cpu_regions'], spec['mutation'], spec['variant'], 'none', False)


def _selected_without_cache(args: object, shape: str, n_if: int) -> tuple:
    """The selected build's identity without its fetch L1 and arm."""
    return shape, n_if, args.cpu_regions, args.mutation, args.variant, 'none', False


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
                                                                        within_t_svc=True, within_ceiling=True))],
    'notify: the fan-out registers one controller an interface (earlier rule)': lambda: [patch.object(
        scenario, 'registrations', lambda: 1)],
    'deadline: T_svc 20 ms': lambda: [patch.object(scenario, 'T_SVC_MS', 20.0)],
    'deadline: strictly below the budget': _verdicts(lambda v, ms, probe: dict(v, within_t_svc=ms < v['t_svc_ms'])),
    'deadline: the normative wait is not added': _verdicts(lambda v, ms, probe: dict(
        v, within_t_svc=ms <= scenario.T_SVC_MS)),
    'deadline: the ceiling drops the normative wait': _verdicts(lambda v, ms, probe: dict(
        v, within_ceiling=ms <= scenario.CEILING_MS[probe.family])),
    'deadline: the ACMP ceiling is the transaction timeout': lambda: [patch.dict(scenario.CEILING_MS, {'acmp': 200.0})],
    'run: a CPU trap is not refused': lambda: [patch.object(grade, 'refuse_run', _run_ignores_traps)],
    'run: a T_svc miss never fails the run': _verdict(refusals_fail=True, misses_fail=False),
    'run: a refusal does not fail the run': _verdict(refusals_fail=False, misses_fail=True),
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
    'fetch bus: the cacheless observers on a cached CPU':
        lambda: [patch.object(build, 'fetch_bus', _fetch_bus_cacheless)],
    'fetch bus: one beat a refill': lambda: [patch.object(build, 'fetch_bus', _fetch_bus_one_beat)],
    'reuse: the fetch L1 and the arm are not compared':
        lambda: [patch.object(run, 'built_as', _built_as_without_cache),
                 patch.object(run, 'selected', _selected_without_cache)],
    'xip: the reset entry moves to flash with the other code': lambda: [patch.object(
        build, 'XIP_TEXT', (build.XIP_TEXT[0], build.XIP_TEXT[1].replace('} > rom', '} > flash')))],
    "xip: F1's flash driver moves to flash with the other code": lambda: [patch.object(
        build, 'XIP_TEXT', (build.XIP_TEXT[0], build.XIP_TEXT[1].replace(' *-nvm_flash_litespi.o(.text .text.*)', '')))],
}
