# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A final pass's AECP records held to their stated costs by class, and the pass held to every group they depend on
(#894: the one-row map edit's record grew past record.aecp unseen, in the one group that measures it,
aecp-fanout, which the gate passes after that growth did not run).

Each AECP record is a span of the record handler (aecp_mbx.c, frame), from entry to return; its command and status
are those of the first solicited AECP response committed at or after its start and before the next record's
(grade.parse, Log.tx): a response the owed-notice queue does not take is committed by the pass's poll, after the
span, and a record that answers nothing before the next one starts is unanswered, never named by a later record's
response. Each is held, by the rule (its cycles at the CPU clock, plus 5 %, rounded up to 5 us), to its class's
stated cost at the leg's point:
  long    every record of aecp-largest-notice, the largest legal command's: rows_tiers.LONG_RECORD_US;
  paced   elsewhere, an ADD or REMOVE_AUDIO_MAPPINGS, or a SET_CONFIGURATION answered SUCCESS or IN_PROGRESS, that is
          paced, the next AECP record starting more than AECP_PACE_MS - 1 ms after it (the gate compares whole
          milliseconds, aecp_mbx.c, ready), or none following: edit_rows.EDIT_RECORD_US, which the tier model charges
          at most edits(w, P) of in a window;
  other   every other record, and one of those that is not paced, which the pace's count does not bound:
          load_grade.GRADED's record.aecp.
The legs held are the formal measurement's (#665, README: the labelled arms are never it): arm A's, every group, the
answering-every-port arm's, and in the answering-ports arm (arm B) its aecp group, the load gate's leg, and
aecp-largest-notice, which the 8x8 shape runs there, and in its aecp-fanout the paced records, over which
EDIT_RECORD_US is measured, and SET_CONFIGURATION's and SET_STREAM_INFO's, whose accepted paths no other arm reaches
(arm A's observation ports never answer), and in its aecp-reboot every REBOOT, accepted and refused, an ordinary
record, whose accepted path needs that arm's reset port (#871); the rest (arm B's other records, the 8x8-1if point)
are reported by class, not held. A pass is refused unless its arm A legs at 1x1/1if together ran every group of the
arm (run.all_groups), each stated cost measured over the arm depending on every one of them, and unless its
answering-ports leg at 1x1/1if ran aecp-fanout's accepted SET_CONFIGURATION and its SET_STREAM_INFO, and
aecp-reboot's accepted REBOOT and a refused one.

usage: python3 -I record_classes.py RESULTS_DIR...   (each a run.py --out directory; its build.json beside it or in
                                                      its parent)
       python3 -I record_classes.py --selftest"""
from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
EDITS = {0x2C: 'ADD_AUDIO_MAPPINGS', 0x2D: 'REMOVE_AUDIO_MAPPINGS'}
SET_CONFIGURATION, SET_STREAM_INFO, REBOOT = 0x06, 0x0E, 0x2A
#: The statuses of an accepted SET_CONFIGURATION, which stamps the pace (aecp_commands.c): SUCCESS, IN_PROGRESS.
ACCEPTED = (0, 9)
#: The answering-ports arm's aecp-fanout records the formal measurement holds whatever their class, and a pass must run.
HELD_COMMANDS = {SET_CONFIGURATION: 'SET_CONFIGURATION', SET_STREAM_INFO: 'SET_STREAM_INFO'}
LONG_GROUP = 'aecp-largest-notice'
#: The answering-ports arm's REBOOT group, whose REBOOT records the formal measurement holds, accepted and refused.
REBOOT_GROUP = 'aecp-reboot'
#: The answering-ports arm's groups the formal measurement holds (above).
HELD_IN_ARM_B = ('aecp', LONG_GROUP)
#: The planted defects controls() plants, in its order.
CONTROLS = ('a pass missing a group of arm A', 'an unpaced edit charged at the edit record',
            'an edit over its record', 'an ordinary record over record.aecp', 'a long record over its record',
            "a labelled arm's record held", "a pass missing arm B's SET_CONFIGURATION",
            "a pass missing arm B's SET_STREAM_INFO", 'an unpaced SET_CONFIGURATION charged as ordinary',
            'a SET_CONFIGURATION over the paced record', "a record named by a later record's response",
            "a pass missing arm B's accepted REBOOT", "a pass missing arm B's refused REBOOT",
            'a REBOOT over record.aecp')


@dataclass
class Record:
    """One AECP record: its start in bus cycles, its CPU cycles, its command's type and its status (None if
    unanswered)."""
    start: int
    cycles: int
    command: int | None
    status: int | None = None


@dataclass
class Leg:
    """One run.py leg: its point, its variant, its clocks and each group's AECP records."""
    point: str
    variant: str
    sys_hz: int
    cpu_hz: int
    groups: dict[str, list[Record]] = field(default_factory=dict)


def rule(cycles: int, cpu_hz: int) -> int:
    """A measured record's stated cost by the rule: its time at the CPU clock, plus 5 %, rounded up to 5 us."""
    return int(math.ceil(cycles * 1e6 / cpu_hz * 1.05 / 5 - 1e-9) * 5)


def point_name(spec: dict) -> str:
    """The stated-cost point of a build: 1x1/1if, 8x8/2if, or 8x8/1if (#894's 8x8 follow-up, reported)."""
    eight = '8x8' in spec['shape']
    return ('8x8/2if' if spec['interfaces'] == 2 else '8x8/1if') if eight else '1x1/1if'


def statements(point: str, root: Path = ROOT) -> dict[str, int]:
    """Each class's stated cost in us at a point, and the pace in ms."""
    import edit_rows
    import load_grade
    import rows_tiers
    pace = rows_tiers.point_inputs(root, '1x1/1if').pace_ms
    return {'long': rows_tiers.LONG_RECORD_US[point], 'paced': edit_rows.EDIT_RECORD_US[point],
            'other': load_grade.GRADED[point]['record.aecp'], 'pace_ms': pace}


def named(spans: list[tuple[int, int]], answers: list[tuple[int, int, int]]) -> list[Record]:
    """Each span (its start in bus cycles, its CPU cycles) named by the first response (its commit in bus cycles,
    command, status) at or after its start and before the next span's, else unanswered (the module's docstring)."""
    out = []
    for k, (start, cycles) in enumerate(spans):
        stop = spans[k + 1][0] if k + 1 < len(spans) else None
        hit = next(((cmd, st) for c, cmd, st in answers if c >= start and (stop is None or c < stop)), (None, None))
        out.append(Record(start, cycles, *hit))
    return out


def read_leg(results: Path) -> tuple[Leg, dict]:
    """A results directory's leg: its build.json (beside it or in its parent) and each graded group's AECP records."""
    import grade
    import scenario
    spec_path = next(p for p in (results / 'build.json', results.parent / 'build.json') if p.is_file())
    spec = json.loads(spec_path.read_text())
    leg = Leg(point_name(spec), spec.get('variant') or 'none', spec['sys_hz'], spec['cpu_hz'])
    aecp = scenario.CH['aecp']
    for log in sorted(results.glob('*.log')):
        text = log.read_text(errors='replace')
        if 'RESULT' not in text[-4000:]:
            continue
        spans = [(int(f[1]), int(f[3])) for f in (line.split() for line in text.splitlines())
                 if len(f) > 4 and f[0] == 'SPAN' and f[-1] == 'aecp_mbx:frame']
        parsed = grade.parse(text[:text.rfind('\n') + 1], leg.sys_hz, leg.cpu_hz)
        answers = sorted((c, (fr[36] << 8 | fr[37]) & 0x7FFF, fr[16] >> 3) for c, ch, _, fr in parsed.tx
                         if ch == aecp and len(fr) >= 38 and fr[15] & 1 and not (fr[15] & 0x0F == 1 and fr[36] & 0x80))
        leg.groups[log.stem] = named(spans, answers)
    return leg, spec


def held(leg: Leg, group: str, kind: str, command: int | None = None) -> bool:
    """Whether the formal measurement holds a leg's group's record of a class and command (the module's docstring)."""
    if leg.point == '8x8/1if':
        return False
    return leg.variant in ('none', 'answering-every-port') or (leg.variant == 'answering-ports' and (
        group in HELD_IN_ARM_B or (group == 'aecp-fanout' and (kind == 'paced' or command in HELD_COMMANDS)) or
        (group == REBOOT_GROUP and command == REBOOT)))


def paceable(r: Record) -> str | None:
    """The name of a record the pace holds the next one after, or None: an edit, or an accepted SET_CONFIGURATION."""
    if r.command in EDITS:
        return EDITS[r.command]
    return 'SET_CONFIGURATION' if r.command == SET_CONFIGURATION and r.status in ACCEPTED else None


def classes(leg: Leg, group: str, stated: dict[str, int]) -> list[tuple[str, Record, int, int, str]]:
    """Each record of a group: its class, the record, its cost by the rule, its class's stated cost and why."""
    out = []
    records = leg.groups[group]
    window = (stated['pace_ms'] - 1) * leg.sys_hz // 1000
    for k, r in enumerate(records):
        cost = rule(r.cycles, leg.cpu_hz)
        name = paceable(r)
        if group == LONG_GROUP:
            out.append(('long', r, cost, stated['long'], 'the largest legal command\'s'))
        elif name is not None:
            following = records[k + 1].start - r.start if k + 1 < len(records) else None
            if following is None or following > window:
                out.append(('paced', r, cost, stated['paced'], f'{name}, paced'))
            else:
                out.append(('other', r, cost, stated['other'], f'{name} not paced: the next record '
                                                                f'{following * 1000 / leg.sys_hz:.3f} ms after it'))
        else:
            name = f'0x{r.command:04x}' if r.command is not None else 'unanswered'
            out.append(('other', r, cost, stated['other'], f'command {name}'))
    return out


def findings(legs: list[Leg], groups_of_arm: list[str] | None,
             stated_at: Callable[[str], dict[str, int]] = statements) -> tuple[list[str], list[str]]:
    """The pass's findings, which refuse it, and the reported lines of the legs not held."""
    out, reported = [], []
    arm = [leg for leg in legs if leg.point == '1x1/1if' and leg.variant == 'none']
    if groups_of_arm is not None:
        if not arm:
            out.append('the pass runs no arm A leg at 1x1/1if')
        ran = {g for leg in arm for g in leg.groups}
        out += [f'the pass is missing {g}, a group of arm A at 1x1/1if, on which each stated cost measured over the '
                'arm depends' for g in groups_of_arm if g not in ran]
        ports = [leg for leg in legs if leg.point == '1x1/1if' and leg.variant == 'answering-ports']
        fanout = [r for leg in ports for r in leg.groups.get('aecp-fanout', [])]
        for command, name in HELD_COMMANDS.items():
            got = [r for r in fanout if r.command == command and (command != SET_CONFIGURATION or r.status in ACCEPTED)]
            if not got:
                what = 'an accepted SET_CONFIGURATION' if command == SET_CONFIGURATION else f'a {name}'
                out.append(f"the pass is missing arm B's {name}: no answering-ports leg at 1x1/1if ran {what} in "
                           'aecp-fanout, whose accepted path no other arm reaches')
        reboots = [r for leg in ports for r in leg.groups.get(REBOOT_GROUP, []) if r.command == REBOOT]
        for what, ran in (('accepted', any(r.status == 0 for r in reboots)),
                          ('refused', any(r.status not in (0, None) for r in reboots))):
            if not ran:
                out.append(f"the pass is missing arm B's {what} REBOOT: no answering-ports leg at 1x1/1if ran one in "
                           f'{REBOOT_GROUP}, whose accepted path needs that arm\'s reset port')
    for leg in legs:
        stated = stated_at(leg.point) if leg.point != '8x8/1if' else stated_at('1x1/1if')
        for group in sorted(leg.groups):
            for kind, r, cost, bound, why in classes(leg, group, stated):
                if cost <= bound:
                    continue
                line = (f'{leg.point} {leg.variant} {group}: a record of {r.cycles:,} CPU cycles, {cost} us by the '
                        f'rule, over the {kind} record\'s {bound} us ({why})')
                (out if held(leg, group, kind, r.command) else reported).append(line)
    return out, reported


MS = 100_000  # bus cycles a millisecond at 100 MHz


def fanout(spans: list[tuple[float, int]], answers: list[tuple[float, int, int]]) -> list[Record]:
    """A synthetic aecp-fanout: spans (ms, CPU cycles) named by responses (ms, command, status), as read_leg names."""
    return named([(round(s * MS), c) for s, c in spans], [(round(a * MS), cmd, st) for a, cmd, st in answers])


def synthetic() -> tuple[list[Leg], list[str], dict[str, int]]:
    """A complete pass whose every record is within its class, the arm's group list, and statements: arm A's REMOVE
    at 240 us by the rule, over record.aecp and within the paced record, paced by the ADD 9 ms after it; arm B's
    accepted SET_CONFIGURATION at 295, paced by its SET_STREAM_INFO 9 ms after it, both held; arm B's SET_NAME at
    350 reported, not held; and arm B's REBOOTs, refused at 160 and accepted at 210, held as ordinary records."""
    hz = 100_000_000
    stated = {'long': 975, 'paced': 300, 'other': 235, 'pace_ms': 8}
    a = fanout([(0, 20_000), (10, 22_500), (19, 21_000), (28, 15_000)],
               [(0.1, 0x10, 0), (10.1, 0x2D, 0), (19.1, 0x2C, 0), (28.1, 0x04, 0)])
    arm = Leg('1x1/1if', 'none', hz, hz, {'aecp-fanout': a, 'aecp': [Record(0, 18_000, 0x10, 0)],
                                          LONG_GROUP: [Record(0, 91_000, 0x2D, 0)]})
    b = fanout([(0, 33_000), (10, 28_000), (19, 20_000)], [(0.1, 0x10, 0), (10.4, 0x06, 0), (19.1, 0x0E, 0)])
    reboot = fanout([(0, 15_000), (10, 20_000)], [(0.1, REBOOT, 11), (10.1, REBOOT, 0)])
    ports = Leg('1x1/1if', 'answering-ports', hz, hz, {'aecp-fanout': b, REBOOT_GROUP: reboot})
    return [arm, ports], ['aecp-fanout', 'aecp', LONG_GROUP], stated


def controls() -> list[str]:
    """Each planted defect not refused, and the synthetic pass refused or its labelled arm's record not reported."""
    import copy
    legs, arm, stated = synthetic()
    at = lambda point: stated  # noqa: E731
    escaped = []
    found, reported = findings(legs, arm, at)
    if found or len(reported) != 1:
        escaped.append(CONTROLS[5])

    def refused(plant: Callable[[list[Leg]], object], words: str) -> bool:
        """Whether the pass with the defect planted is refused on the words."""
        planted = copy.deepcopy(legs)
        plant(planted)
        return any(words in f for f in findings(planted, arm, at)[0])

    def unanswered(p: list[Leg]) -> None:
        """Arm A's first record answers nothing and costs 245 us by the rule: named by the REMOVE's response after
        it, it would be held paced, at 300."""
        p[0].groups['aecp-fanout'] = fanout([(0, 23_000), (10, 22_500), (19, 21_000), (28, 15_000)],
                                            [(10.1, 0x2D, 0), (19.1, 0x2C, 0), (28.1, 0x04, 0)])
    plants = (
        (lambda p: p[0].groups.pop('aecp-fanout'), 'the pass is missing aecp-fanout'),
        (lambda p: setattr(p[0].groups['aecp-fanout'][2], 'start', 17 * MS - 1), 'REMOVE_AUDIO_MAPPINGS not paced'),
        (lambda p: setattr(p[0].groups['aecp-fanout'][1], 'cycles', 29_000), '(REMOVE_AUDIO_MAPPINGS, paced)'),
        (lambda p: setattr(p[0].groups['aecp'][0], 'cycles', 22_400), 'over the other record'),
        (lambda p: setattr(p[0].groups[LONG_GROUP][0], 'cycles', 93_000), 'over the long record'),
        None,
        (lambda p: p[1].groups['aecp-fanout'].pop(1), "missing arm B's SET_CONFIGURATION"),
        (lambda p: p[1].groups['aecp-fanout'].pop(2), "missing arm B's SET_STREAM_INFO"),
        (lambda p: setattr(p[1].groups['aecp-fanout'][2], 'start', 17 * MS - 1), 'SET_CONFIGURATION not paced'),
        (lambda p: setattr(p[1].groups['aecp-fanout'][1], 'cycles', 29_000), '(SET_CONFIGURATION, paced)'),
        (unanswered, 'command unanswered'),
        (lambda p: p[1].groups[REBOOT_GROUP].pop(1), "missing arm B's accepted REBOOT"),
        (lambda p: p[1].groups[REBOOT_GROUP].pop(0), "missing arm B's refused REBOOT"),
        (lambda p: setattr(p[1].groups[REBOOT_GROUP][1], 'cycles', 23_000), f'{REBOOT_GROUP}: a record of 23,000'),
    )
    for name, entry in zip(CONTROLS, plants):
        if entry is not None and not refused(*entry):
            escaped.append(name)
    return escaped


def checks() -> list[tuple[str, bool, str]]:
    """The harness self-test's checks of this one (load_grade.ceiling_checks): every planted defect refused."""
    escaped = controls()
    return [(f'the record classes refuse {name}', name not in escaped, 'escaped' if name in escaped else 'refused')
            for name in CONTROLS]


def main(argv: list[str]) -> int:
    """Hold a pass's legs, or plant each control."""
    if argv == ['--selftest']:
        escaped = controls()
        for name in escaped:
            print(f'ESCAPED {name}')
        print(f'record classes: {len(CONTROLS) - len(escaped)} of {len(CONTROLS)} planted controls refused')
        return int(bool(escaped))
    if not argv or any(a.startswith('-') for a in argv):
        print(__doc__)
        return 2
    import run
    import scenario
    legs, arm = [], None
    for d in map(Path, argv):
        leg, spec = read_leg(d.resolve())
        legs.append(leg)
        if leg.point == '1x1/1if' and leg.variant == 'none' and arm is None:
            arm = [g.name for g in run.all_groups(scenario.point('1x1', spec), spec)]
        print(f'{d.name}: {leg.point} {leg.variant}, {len(leg.groups)} groups, '
              f'{sum(len(v) for v in leg.groups.values())} AECP records')
    found, reported = findings(legs, arm if arm is not None else [])
    for point in sorted({leg.point for leg in legs}):
        s = statements(point if point != '8x8/1if' else '1x1/1if')
        dearest = {}
        for leg in legs:
            if leg.point != point:
                continue
            for group in leg.groups:
                for kind, r, cost, bound, why in classes(leg, group, s):
                    key = (kind, held(leg, group, kind, r.command))
                    if key not in dearest or r.cycles > dearest[key][0]:
                        dearest[key] = (r.cycles, cost, bound, f'{leg.variant} {group}: {why}')
        for (kind, is_held), (cycles, cost, bound, where) in sorted(dearest.items()):
            print(f'{point} {"held" if is_held else "reported"} {kind}: the dearest {cycles:,} CPU cycles, {cost} us '
                  f'by the rule, stated {bound} us ({where})')
    for line in reported:
        print('REPORTED', line)
    for line in found:
        print('REFUSED', line)
    print('RESULT: FAIL' if found else 'RESULT: PASS')
    return int(bool(found))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
