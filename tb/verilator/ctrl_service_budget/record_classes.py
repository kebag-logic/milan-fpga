# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A final pass's AECP records held to their stated costs by class, and the pass held to every group they depend on
(#894's round 11: the one-row map edit's record had grown past record.aecp in the one group that measures it,
aecp-fanout, which no pass had run since round 4).

Each AECP record is a span of the record handler (aecp_mbx.c, frame), from entry to return; its command is that of
the first solicited AECP response committed at or after its start (grade.parse, Log.tx). Each is held, by the rule
(its cycles at the CPU clock, plus 5 %, rounded up to 5 us), to its class's stated cost at the leg's point:
  long    every record of aecp-largest-notice, the largest legal command's: rows_tiers.LONG_RECORD_US;
  edit    an ADD or REMOVE_AUDIO_MAPPINGS elsewhere that is paced, the next AECP record starting more than
          AECP_PACE_MS - 1 ms after it (the gate compares whole milliseconds, aecp_mbx.c, ready), or none following:
          edit_rows.EDIT_RECORD_US, which the tier model charges at most edits(w, P) of in a window;
  other   every other record, and an edit that is not paced, which the pace's count does not bound:
          load_grade.GRADED's record.aecp.
The legs held are the formal measurement's (#665, README: the labelled arms are never it): arm A's, every group, the
answering-every-port arm's, and in the answering-ports arm (arm B) its aecp group, the load gate's leg, and
aecp-largest-notice, which the 8x8 shape runs there; the rest (arm B's other groups, the 8x8-1if point) are reported
by class, not held. A pass is refused unless its arm A legs at 1x1/1if together ran every group of the arm
(run.all_groups): each stated cost measured over the arm depends on every one of them.

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
LONG_GROUP = 'aecp-largest-notice'
#: The answering-ports arm's groups the formal measurement holds (above).
HELD_IN_ARM_B = ('aecp', LONG_GROUP)
#: The planted defects controls() plants, in its order.
CONTROLS = ('a pass missing a group of arm A', 'an unpaced edit charged at the edit record',
            'an edit over its record', 'an ordinary record over record.aecp', 'a long record over its record',
            "a labelled arm's record held")


@dataclass
class Record:
    """One AECP record: its start in bus cycles, its CPU cycles and its command's type (None if unanswered)."""
    start: int
    cycles: int
    command: int | None


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
    """The stated-cost point of a build: 1x1/1if, 8x8/2if, or 8x8/1if (lane 894b's, reported)."""
    eight = '8x8' in spec['shape']
    return ('8x8/2if' if spec['interfaces'] == 2 else '8x8/1if') if eight else '1x1/1if'


def statements(point: str, root: Path = ROOT) -> dict[str, int]:
    """Each class's stated cost in us at a point, and the pace in ms."""
    import edit_rows
    import load_grade
    import rows_tiers
    pace = rows_tiers.point_inputs(root, '1x1/1if').pace_ms
    return {'long': rows_tiers.LONG_RECORD_US[point], 'edit': edit_rows.EDIT_RECORD_US[point],
            'other': load_grade.GRADED[point]['record.aecp'], 'pace_ms': pace}


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
        answers = sorted((c, (fr[36] << 8 | fr[37]) & 0x7FFF) for c, ch, _, fr in parsed.tx
                         if ch == aecp and len(fr) >= 38 and fr[15] & 1 and not (fr[15] & 0x0F == 1 and fr[36] & 0x80))
        records = []
        for start, cycles in spans:
            command = next((cmd for c, cmd in answers if c >= start), None)
            records.append(Record(start, cycles, command))
        leg.groups[log.stem] = records
    return leg, spec


def held(leg: Leg, group: str) -> bool:
    """Whether the formal measurement holds a leg's group (the module's docstring)."""
    if leg.point == '8x8/1if':
        return False
    return leg.variant in ('none', 'answering-every-port') or (leg.variant == 'answering-ports' and
                                                               group in HELD_IN_ARM_B)


def classes(leg: Leg, group: str, stated: dict[str, int]) -> list[tuple[str, Record, int, int, str]]:
    """Each record of a group: its class, the record, its cost by the rule, its class's stated cost and why."""
    out = []
    records = leg.groups[group]
    window = (stated['pace_ms'] - 1) * leg.sys_hz // 1000
    for k, r in enumerate(records):
        cost = rule(r.cycles, leg.cpu_hz)
        if group == LONG_GROUP:
            out.append(('long', r, cost, stated['long'], 'the largest legal command\'s'))
        elif r.command in EDITS:
            following = records[k + 1].start - r.start if k + 1 < len(records) else None
            if following is None or following > window:
                out.append(('edit', r, cost, stated['edit'], f'{EDITS[r.command]}, paced'))
            else:
                out.append(('other', r, cost, stated['other'], f'{EDITS[r.command]} not paced: the next record '
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
    for leg in legs:
        stated = stated_at(leg.point) if leg.point != '8x8/1if' else stated_at('1x1/1if')
        for group in sorted(leg.groups):
            for kind, r, cost, bound, why in classes(leg, group, stated):
                if cost <= bound:
                    continue
                line = (f'{leg.point} {leg.variant} {group}: a record of {r.cycles:,} CPU cycles, {cost} us by the '
                        f'rule, over the {kind} record\'s {bound} us ({why})')
                (out if held(leg, group) else reported).append(line)
    return out, reported


def synthetic() -> tuple[list[Leg], list[str], dict[str, int]]:
    """A complete pass whose every record is within its class, the arm's group list, and statements: the REMOVE at
    240 us by the rule, over record.aecp and within the edit record, paced by the ADD 9 ms after it."""
    hz, ms = 100_000_000, 100_000
    stated = {'long': 975, 'edit': 240, 'other': 235, 'pace_ms': 8}
    fanout = [Record(0, 20_000, 0x10), Record(10 * ms, 22_500, 0x2D), Record(19 * ms, 21_000, 0x2C),
              Record(28 * ms, 15_000, 0x04)]
    arm = Leg('1x1/1if', 'none', hz, hz, {'aecp-fanout': fanout, 'aecp': [Record(0, 18_000, 0x10)],
                                          LONG_GROUP: [Record(0, 91_000, 0x2D)]})
    ports = Leg('1x1/1if', 'answering-ports', hz, hz, {'aecp-fanout': [Record(0, 33_000, 0x06)]})
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
    plants = (
        (lambda p: p[0].groups.pop('aecp-fanout'), 'the pass is missing aecp-fanout'),
        (lambda p: setattr(p[0].groups['aecp-fanout'][2], 'start', 10 * 100_000 + 7 * 100_000 - 1),
         'not paced'),
        (lambda p: setattr(p[0].groups['aecp-fanout'][1], 'cycles', 23_000), 'over the edit record'),
        (lambda p: setattr(p[0].groups['aecp'][0], 'cycles', 22_400), 'over the other record'),
        (lambda p: setattr(p[0].groups[LONG_GROUP][0], 'cycles', 93_000), 'over the long record'),
    )
    for name, (plant, words) in zip(CONTROLS, plants):
        if not refused(plant, words):
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
                    key = (kind, held(leg, group))
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
