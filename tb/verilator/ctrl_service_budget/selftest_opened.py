# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""selftest_opened.py - the self-test's checks of #884's ruling, A and B (channel_gate.py), and the committed trace's
own clocks, channel gate and trim, which selftest.py grades, completes its synthetic logs with and writes it by.

A row's defined load covers the channels the image opened, read from its FILTER_EN write (sim_main.cpp's OPEN
lines); an opened channel with no load frame is refused; a log with no FILTER_EN write is refused, never read as
every channel; and the image's last gate is the one read.
"""
from __future__ import annotations

import re
from collections.abc import Callable
from types import ModuleType

import channel_gate
import grade
import scenario

Check = tuple[str, bool, str]
#: The channels the committed trace's image opened: the five the fixture image binds, gptp not among them.
FIXTURE_OPENED = frozenset({'adp', 'acmp', 'aecp', 'maap', 'srp'})
#: A gPTP image's gptp records in each composed window: its bucket's burst, one in the fixture's (#884).
GPTP_AT_ONCE = {'backlog': 16, 'backlog-adp': 16, 'backlog-adp-refill': 16, 'backlog-owed': 16, 'fixture': 1}


def fixture_clocks(oracle: dict) -> tuple[int, int]:
    """The system and CPU clocks the committed trace was recorded at (selftest.write_fixture pins them): its cycles
    are graded at its own SoC's clocks, not at the synthetic logs' SYS_HZ and CPU_HZ."""
    return oracle['clocks']['sys_hz'], oracle['clocks']['cpu_hz']


def fixture_kept(text: str) -> list[str]:
    """A 'fixture' group log trimmed to what its probes read (selftest.write_fixture). The saved-state store's traced
    calls (SPAN, CALL) are nvm_split_target's and go. A tick, PC or fetch line stays only at an event record's third
    word and the millisecond after it: a timer path's start is its deadline's tick, and the next tick must be there
    too, or a start planted a millisecond late reads the deadline's own and the plant is lost."""
    records = re.findall(r'^EVW \d+ \d+ ([0-9a-f]+)$', text, re.M)
    ticks = {int(records[k + 2], 16) + late for k in range(0, len(records) - 3, 4) for late in (0, 1)}
    return [line for line in text.splitlines() if not line.startswith(('SPAN ', 'CALL '))
            and (not line.startswith(('MS ', 'PC ', 'FETCH ')) or int(line.split()[2]) in ticks)]


def fixture_open() -> str:
    """The OPEN line a synthetic log carries: the committed trace's channel gate, so its image opened the same."""
    return f'OPEN 0 {sum(1 << c.ident for c in grade.CONTRACT.channels if c.name in channel_gate.fixture()):x}'


def planted_probe(group: scenario.Group, rows: dict[str, dict], text: str) -> tuple[str, dict]:
    """The committed trace's probe that fixture_checks moves one cycle past its 20 ms budget: the first with that
    budget whose window, to the next mark, still holds the moved response, so the plant is graded and not lost.
    On the split SoC the trace's paths are short and so are its windows, BIND_RX's among them (#884)."""
    marks = sorted(int(cycle) for cycle in re.findall(r'^MARK (\d+) ', text, re.M))
    budget = {p.name: grade.budget_ms(p) for p in group.probes}
    for name, row in rows.items():
        late = row['start_sys'] + 2_000_001
        if budget.get(name) == 20.0 and next((m for m in marks if m > row['start_sys']), late + 1) > late:
            return name, row
    raise ValueError('no probe of the committed trace has a 20 ms budget and a window that holds the plant')


def refused(action: Callable[[], object], words: str = '') -> bool:
    """Whether the grader refuses the action, with words in its message."""
    try:
        action()
    except grade.Refusal as error:
        return words in str(error)
    return False


def opened_checks() -> list[Check]:
    """A and B, on the committed trace and on copies of it with its gate removed or replaced."""
    text = (channel_gate.HERE / 'fixture.log').read_text()
    opened = channel_gate.opened(channel_gate.writes(text))
    with_gptp = opened | {'gptp'}
    gptp = next(c for c in grade.CONTRACT.channels if c.name == 'gptp')
    load = grade.defined_load('backlog-adp', with_gptp)
    out = [("the fixture's image opened its five channels, gptp unopened", opened == FIXTURE_OPENED,
            str(sorted(opened))),
           ('an image that opens gptp carries its admitted burst in the composed rows',
            load.get('gptp') == min(gptp.burst, grade.room('gptp'))
            and {k: v for k, v in load.items() if k != 'gptp'} == grade.defined_load('backlog-adp', opened), str(load)),
           ('an unopened channel carries no defined load', 'gptp' not in grade.defined_load('backlog-adp', opened),
            str(grade.defined_load('backlog-adp', opened)))]
    frame = grade.LOAD_FRAME_BYTES.pop('gptp')
    try:
        unframed = refused(lambda: grade.defined_load('backlog-adp', with_gptp), 'no load frame defines')
    finally:
        grade.LOAD_FRAME_BYTES['gptp'] = frame
    out.append(('an opened channel with no load frame is refused', unframed, ''))
    bare = '\n'.join(ln for ln in text.splitlines() if not ln.startswith('OPEN ')) + '\n'
    out.append(('a log with no FILTER_EN write is refused, never read as every channel',
                refused(lambda: channel_gate.opened(grade.parse(bare, 1, 1).opened), 'no FILTER_EN write'), ''))
    last = channel_gate.opened(grade.parse(text + 'OPEN 1 3\n', 1, 1).opened)
    out.append(("the image's last gate is the one read", last == frozenset({'adp', 'acmp'}), str(sorted(last))))
    return out


def gptp_load_check(defined: dict[str, dict[str, int]]) -> Check:
    """A gPTP image's defined loads: each row's `defined` (selftest.DEFINED) and its GPTP_AT_ONCE gptp records."""
    opened = channel_gate.fixture() | {'gptp'}
    derived = {name: {k: v for k, v in grade.defined_load(name, opened).items() if v} for name in defined}
    want = {name: {**load, 'gptp': GPTP_AT_ONCE[name]} for name, load in defined.items()}
    return "a gPTP image's defined loads, restated", derived == want, str(derived)


def gptp_point_check(build: ModuleType, points: dict[str, tuple[str, int]], ledgered: dict) -> Check:
    """A gPTP image's ledgered point (build.GPTP_LEDGERED_POINTS) at each of the harness's `points` and at the shapes'
    other interface counts: 8x8's two, each a name `ledgered` (ctrl_memory.LEDGERED) holds, and none at 1x1."""
    named = {label: build.ledgered_point(*points[label], True) for label in sorted(points)}
    others = {(shape, n): build.ledgered_point(shape, n, True) for shape, _ in points.values() for n in (1, 2)
              if (shape, n) not in points.values()}
    return ("a gPTP image's ledgered point is named at 8x8 only, at each interface count, as the planner ledgers it",
            named == {'1x1': None, '8x8': '8x8-two-interfaces-gptp', '8x8-1if': '8x8-one-interface-gptp'} and
            others == {('endstation_ax7101_1x1_tdm8', 2): None} and
            all(named[k] in ledgered for k in ('8x8', '8x8-1if')), f'{named}; other points {others}')
