# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The budget grader self-test's checks of the per-pass share and of the CPU clock (#665), which
selftest.py runs.

The share (share.py) is SRP's 18 ms, the tightest family bound, over nine passes. Synthetic passes
at it and a cycle over it check grade.pass_share, and the run fails on a pass over it even when
every row fits, unless --record-share-findings records it; --record-budget-findings, the rows'
option, does not. The clock checks build through run.main with build.build's toolchain steps
replaced (selftest.built): the CPU runs in the split placement's clock domain, sys, at the bus
clock, and build.json and every line say so; a build whose SoC puts the CPU on the Milan clock is
refused, and so is a reused build that records its CPU there or records no domain. A pass that
writes nothing to the mailbox is held to the share by its run's longest (sim_main.cpp's IDLE line).
A save in a composed window (save_window.py) is staged at eight tick phases of each flash phase,
after the save's own flash event, and its window carries backlog-adp's load. Each check is
(name, held, detail), as selftest.py's.
"""
from __future__ import annotations

import argparse
import json
import runpy
import tempfile
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import yaml

import build
import grade
import run
import save_window
import scenario
import share

ROOT = Path(__file__).resolve().parents[3]
#: The share and the product's split CPU clock, the bus clock, restated here on purpose (#665, owner
#: decision 2026-10-30): a changed value must fail. The Milan datapath clock stays the bare-metal
#: build contract's.
SHARE_MS = 2.0
SHARE_CYCLES = {50_000_000: 100_000, 100_000_000: 200_000}
PRODUCT_CPU_HZ = 100_000_000
MILAN_HZ = 50_000_000
Check = tuple[str, bool, str]


def share_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int) -> list[Check]:
    """The share's value, a pass at it and a cycle over it, and the run's verdict and table on them."""
    out = []
    got = (share.bound_ms(), share.share_ms(), {hz: share.share_cycles(hz) for hz in SHARE_CYCLES})
    out.append(("the per-pass share is SRP's 18 ms, the tightest family bound, over nine passes: 2.0 ms, "
                "200,000 CPU cycles at the product's 100 MHz", got == (18.0, SHARE_MS, SHARE_CYCLES), str(got)))
    limit = SHARE_CYCLES[cpu_hz]
    lines = [f'PASS {n} {s} {s // 2} {c} instr=10 store_mbx=1 W {s + 100}:1:0' for n, (s, c)
             in enumerate(((1000, limit), (400_000, limit + 1), (900_000, 50)), 1)]
    graded = grade.grade(synthetic(lines), scenario.Group('g'), sys_hz, cpu_hz)
    s = graded['passes']['share']
    got = (s['passes'], s['over'], [p['cycles'] for p in s['over_passes']])
    out.append(('a work pass at the share fits it and one a cycle over it does not', got == (3, 1, [limit + 1]),
                str(s)))
    quiet = grade.grade(synthetic([lines[0], f'IDLE 4 50 {limit + 1}', lines[2]]), scenario.Group('g'), sys_hz,
                        cpu_hz)['passes']['share']
    named = run.share_misses([dict(group='g', passes=dict(share=quiet, worst=dict(cycles=limit, ms=2.0)))])
    out.append(('a pass that writes nothing to the mailbox is held to the share too: a run of them whose longest is '
                'a cycle over it is a pass over it, and named', (quiet['over'], quiet['idle_over'],
                                                                quiet['idle_longest']) == (1, 1, limit + 1)
                and named and named[0].endswith(f'1 run(s) of passes with no mailbox write, the longest {limit + 1:,}'),
                str((quiet, named))))
    s2 = grade.grade(synthetic(lines), scenario.Group('g'), sys_hz, 2 * cpu_hz)['passes']['share']
    out.append(('the share is CPU time: at twice the CPU clock it is twice the cycles',
                (s2['cycles'], s2['over']) == (2 * limit, 0), str(s2)))
    args = lambda rows, passes: argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=rows,
                                                    record_share_findings=passes)
    shares = run.share_misses([graded])
    g = scenario.Group('g')
    verdicts = [run.verdict(args(*flags), [g], [], [], shares) for flags in ((False, False), (True, False),
                                                                             (False, True))]
    verdicts.append(run.verdict(args(False, False), [g], [], [], []))
    named = shares == [f'g: 1 of 3 work passes over the per-pass share 2.000 ms ({limit:,} CPU cycles); the longest '
                       f'{limit + 1:,} ({(limit + 1) / (cpu_hz / 1000):.3f} ms)']
    out.append(('a pass over the share fails a run whose rows all fit, unless --record-share-findings records it; '
                '--record-budget-findings does not', verdicts == [1, 1, 0, 0] and named, str((verdicts, shares))))
    control = argparse.Namespace(cpu_regions='cover', mutation='store-step-unbounded', record_budget_findings=False,
                                 record_share_findings=False)
    got = [run.verdict(control, [g], *case) for case in (([], [], shares), ([], ['g.x.if0: 20.1 ms'], shares),
                                                          ([], ['h.x.if0: 20.1 ms'], shares), (['refused'], [], shares),
                                                          ([], [], []))]
    out.append(('the planted store step is caught by a group with a pass over the share and every row of its own '
                'within its budget, and escapes with only a row over it there too, a refusal, or no pass over the '
                'share', got == [0, 1, 0, 1, 1], str(got)))
    table = run.table([graded], '1x1', 'CPU 50 MHz')
    saved = run.summary('1x1', '0' * 64, [graded], [], [], shares)['share_misses']
    rendered = (f'| g | 3 | 1 | {limit + 1:,} ({(limit + 1) / (cpu_hz / 1000):.3f}) | OVER the share |' in table
                and table.startswith('### 1x1\n\nClock: CPU 50 MHz.\n'))
    out.append(('the table names the clock and each group against the share, and results.json keeps the passes over it',
                rendered and saved == shares, table[:400]))
    return out


def clock_checks(built: Callable[..., tuple[str, dict]], main_verdict: Callable[..., str]) -> list[Check]:
    """The split CPU on the bus clock, the refusal of one on the Milan clock, built or reused."""
    out = []
    contract = runpy.run_path(str(ROOT / 'tb/verilator/nvm_capture_cpu/recipe.py'))['CPU_HZ']
    points = {point: yaml.safe_load((ROOT / 'configs' / f'{shape}.yaml').read_text())['board']['constraints']
              for point, (shape, _) in run.POINTS.items()}
    got = {point: (c['sys_clk_hz'], c['milan_clk_hz']) for point, c in points.items()}
    out.append(("each point's split CPU clock is its bus clock, sys_clk_hz, 100 MHz; its Milan datapath clock stays "
                "the bare-metal build contract's 50 MHz", set(got.values()) == {(PRODUCT_CPU_HZ, contract)}
                and contract == MILAN_HZ, str((got, contract))))
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        (root / 'firmware').mkdir()
        (root / 'firmware/adp.c').write_text('c')
        with patch.object(build, 'FIRMWARE_TREES', (str(root / 'firmware'),)):
            verdict, spec = built(root / 'product')
            got = (verdict, spec.get('cpu_cd'), spec.get('cpu_hz'), spec.get('sys_hz'))
            out.append(("the CPU runs in the split placement's clock domain, sys, at the bus clock, and build.json "
                        'says so', got == ('reached', 'sys', PRODUCT_CPU_HZ, PRODUCT_CPU_HZ), str(got)))
            line = build.clock_line(spec) if spec else ''
            out.append(('the clock line names the CPU on sys at the product clock',
                        line == "CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz", line))
            with patch.object(build, 'Core', lambda *a, core=build.Core: core(*a, cpu_cd='milan')):
                verdict, spec = built(root / 'milan')
            out.append(('a build whose SoC puts the CPU on the Milan clock is refused and records nothing',
                        verdict.startswith('returned 1') and 'not on the bus clock' in verdict
                        and 'milan clock domain' in verdict and not spec, verdict))
            record = root / 'product/build.json'
            kept = record.read_text() if record.is_file() else '{}'
            cases = [('on sys', None, True), ('on the Milan clock', dict(cpu_cd='milan', cpu_hz=MILAN_HZ), False),
                     ('on sys at half the bus clock', dict(cpu_hz=MILAN_HZ), False),
                     ('with no domain recorded', dict(cpu_cd=None), False)]
            verdicts = []
            for _, edit, _ in cases:
                record.write_text(kept if edit is None else json.dumps(
                    {k: v for k, v in {**json.loads(kept), **edit}.items() if v is not None}))
                verdicts.append(main_verdict(root / 'product', '--reuse-build'))
    wrong = [f'{name}: {verdict}' for (name, _, reuse), verdict in zip(cases, verdicts)
             if not (verdict == 'reached' if reuse else verdict.startswith('returned 1') and 'bus clock' in verdict)]
    out.append(('the run reuses a build on sys and refuses one recorded on the Milan clock, off the bus clock or '
                'with no CPU domain', not wrong, '; '.join(wrong)))
    return out


def save_checks() -> list[Check]:
    """A save in a composed window: each flash phase at eight tick phases, after the save's own event."""
    p = scenario.Point('8x8', 'endstation_ax7101_8x8', 2, 1, 2, 8, 8)
    want = {'blank': ('flash erase 1', 10), 'program': ('flash program 1', 20),
            'verify': (f'flash idle {30 * scenario.MS}', 10)}
    seen: dict[str, list] = {}
    windows = save_window.windows(p)
    for g in windows:
        n = next(k for k, step in enumerate(g.steps) if step.startswith('wait flash '))
        opens = g.steps[n + 2:n + 5] == list(scenario.OPEN_WINDOW)
        seen.setdefault(g.name.partition('@')[2].rpartition('-')[0], []).append(
            (g.steps[n].removeprefix('wait ').partition(' within ')[0], int(g.steps[n + 1].split()[-1]), opens))
    got = {}
    for phase, rows in seen.items():
        delays = sorted(d for _, d, _ in rows)
        steps = {b - a for a, b in zip(delays, delays[1:])}
        got[phase] = ({e for e, _, _ in rows}, len(delays), sum(steps) * len(delays) if len(steps) == 1 else 0,
                      all(o for *_, o in rows))
    expect = {phase: ({event}, 8, period * scenario.MS, True) for phase, (event, period) in want.items()}
    loads = [grade.defined_load(g.name) == grade.defined_load('backlog-adp') for g in windows]
    return [("each flash phase of a save is staged at eight tick phases spread evenly across its heavy step's "
             "period, the window opening after the save's own flash event", got == expect, str(got)),
            ("a save's window carries backlog-adp's defined load", all(loads) and len(loads) == 24, str(loads)),
            *phase_checks(), *bound_checks(), *held_checks()]


#: The journal slot a synthetic save writes, the flash device's journal (sim_main.cpp, flash.hpp).
SLOT = 0xEE0000


def synthetic_save(ms: int, pages: list[int], reads: list[int], page_bytes: int = 256,
                   erase: int = 10) -> tuple[list, list, list]:
    """A synthetic first save: its erase, pages of page_bytes programmed at the given ms, each read-back of 128
    bytes at the given ms, lasting 0.7 ms; the FLASHOP and FLASHRD records grade.parse makes of them."""
    ops = [(erase * ms, grade.FLASH_ERASE, SLOT, 0)]
    ops += [(t * ms, grade.FLASH_PROGRAM, SLOT + n * page_bytes, page_bytes) for n, t in enumerate(pages)]
    runs = [(t * ms, t * ms + 7 * ms // 10, SLOT + (n * 128) % (len(pages) * page_bytes), 128)
            for n, t in enumerate(reads)]
    return ops, runs, [(c, op) for c, op, _, _ in ops]


def phase_checks() -> list[Check]:
    """A save's window opens inside its flash phase of the first save, or is refused (grade.save_phase)."""
    ms = scenario.MS

    def opens(phase: str, start_ms: float, save: tuple) -> bool:
        """Whether a window opening at start_ms is graded inside phase."""
        ops, runs, flash = save
        try:
            grade.save_phase(grade.Log(100_000_000, 100_000_000, flash=flash, flash_ops=ops, reads=runs),
                             f'backlog-adp@{phase}-0', int(start_ms * ms))
        except grade.Refusal:
            return False
        return True
    verify = [100, 110, 120, 130, 140, 150]
    first = synthetic_save(ms, [30, 50, 70], verify)
    another = synthetic_save(ms, [30, 50, 70, 110], verify)
    later = synthetic_save(ms, [30, 50, 70], verify)
    later = (later[0] + [(200 * ms, grade.FLASH_ERASE, SLOT + 0x10000, 0),
                         (220 * ms, grade.FLASH_PROGRAM, SLOT + 0x10000, 256)], later[1], later[2])
    cases = [('blank', 20, first, True), ('blank', 5, first, False), ('blank', 40, first, False),
             ('program', 40, first, True), ('program', 80, first, True), ('program', 20, first, False),
             ('program', 105, first, False), ('verify', 105, first, True), ('verify', 60, first, False),
             ('verify', 105, another, False), ('verify', 105, later, True), ('verify', 145, first, True),
             ('verify', 155, first, False)]
    got = [opens(*case[:3]) for case in cases]
    want = [case[3] for case in cases]
    return [("a save's window is refused unless it opens inside its flash phase of the first save: the blank check "
             "between the erase and the first page, the program phase within 30 ms of a page, the verify 30 ms or "
             "more after its last page with no later page and before its read-backs have read back every "
             "programmed byte", got == want, str(got))]


def bound_checks() -> list[Check]:
    """A save's stated worst case, restated here on purpose (#665): a changed age limit or step count must fail."""
    got = (save_window.step_age(), save_window.CHANGED, save_window.steps(13_256, 2), save_window.bound_ms(13_256, 2),
           save_window.steps(3_336, 2), save_window.bound_ms(3_336, 2))
    return [("a save's stated worst case is its 1,000 ms first-dirty window, then each of its steps at most three "
             "ticks after the one before (THE STEP's age limit, two centiseconds, plus one), and 10 ms: for a SET_NAME "
             "of the entity, which marks its two names, 12,110 ms at 8x8/2if (370 steps of a 13,256-byte container) "
             "and 4,070 ms at 1x1 (102 of 3,336 bytes)", got == (2, 2, 370, 12_110, 102, 4_070), str(got))]


def save_time_checks(sys_hz: int, cpu_hz: int) -> list[Check]:
    """A save timed from its change to durable against its stated worst case (save_grade.save_time), and the run's
    verdict on a save over it; the age limit's plant caught by a starved save not durable within it."""
    ms = sys_hz // 1000
    group = scenario.Group('s', save=dict(image=768, records=2))
    bound = save_window.bound_ms(768, 2)

    def timed(last_read_ms: int | None, end_ms: int) -> dict:
        """The save's grade, its verify's last read-back at last_read_ms (None: never), the run ending at end_ms."""
        verify = [bound - 100 + 10 * k for k in range(5)] if last_read_ms is None else \
            [last_read_ms - 10 * k for k in range(5, -1, -1)]
        reads = [1000, 1010, 1020, 1030, 1040, 1050, *verify]
        ops, runs, _ = synthetic_save(ms, [1100, 1300, 1500], reads, erase=900)
        lines = ['MARK 0 save.change', 'FLOOD 5 gm 1 0',
                 *(f'FLASHOP {c} {op} {a:06x} {n}' for c, op, a, n in ops),
                 *(f'FLASHRD {a} {b} {c:06x} {n}' for a, b, c, n in runs), f'FLASHPOLL {950 * ms}',
                 f'SUMMARY passes=1 sys={end_ms * ms}', 'RESULT: PASS']
        return grade.grade('\n'.join(lines) + '\n', group, sys_hz, cpu_hz)['save']
    within, over, never = timed(1700, 1800), timed(bound + 50, bound + 100), timed(None, bound + 100)
    got = [(s['within'], s['ms'] is not None) for s in (within, over, never)]
    out = [("a save is timed from its change to the last read-back that completes its verify: durable within its "
            "stated worst case, over it, or never in the run, each named", got == [(True, True), (False, True),
                                                                               (False, False)]
            and within['ms'] == 1700.7 and within['bound_ms'] == bound and within['flooded'], str((within, over,
                                                                                                   never)))]
    late = run.save_misses([dict(group='s', save=over), dict(group='t', save=within), dict(group='u', save=never)])
    args = argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=True,
                              record_share_findings=True)
    g = scenario.Group('g')
    verdicts = [run.verdict(args, [g], [], [], [], late), run.verdict(args, [g], [], [], [], [])]
    out.append(('a save not durable within its stated worst case fails the run, whatever the options record',
                verdicts == [1, 0] and [m.partition(':')[0] for m in late] == ['s', 'u'], str((verdicts, late))))
    control = argparse.Namespace(cpu_regions='cover', mutation='store-step-ageless', record_budget_findings=False,
                                 record_share_findings=False)
    cases = ((['save-starved: x'], []), ([], []), (['save-held: x'], []), (['save-starved: x'], ['refused']))
    got = [run.verdict(control, [g], refusals, [], [], late) for late, refusals in cases]
    out.append(("the age limit's plant is caught by save-starved's save not durable within its stated worst case, and "
                "escapes with every save within it, only save-held's late, or a refusal", got == [0, 1, 1, 1],
                str(got)))
    return out


def held_checks() -> list[Check]:
    """The two loaded saves: every receive channel at its contract refill rate with its bursts through the stated
    worst case, and the starved one with a grandmaster change as every pass starts."""
    p = scenario.Point('8x8', 'endstation_ax7101_8x8', 2, 1, 2, 8, 8)
    run_ms = save_window.bound_ms(13_256, 2) + 500
    seen: dict[str, list[float]] = {}
    for when, channel, _ in save_window.arrivals(p, run_ms):
        seen.setdefault(channel, []).append(when)
    wrong = []
    for name, n in scenario.CH.items():
        ch = scenario.CONTRACT.channels[n]
        times = seen.get(name, [])
        instants = sorted(set(times))
        at_once = {times.count(t) for t in instants}
        periods = {round(b - a, 6) for a, b in zip(instants, instants[1:])}
        size = next(iter(at_once)) if len(at_once) == 1 else 0
        rate = len(times) * ch.refill_ms / run_ms
        if not (size and periods == {size * ch.refill_ms} and instants[0] == save_window.OFFSET_MS * n
                and instants[-1] + size * ch.refill_ms >= run_ms and 0.98 < rate < 1.02 + size * ch.refill_ms / run_ms):
            wrong.append(f'{name}: {sorted(at_once)} at once, periods {sorted(periods)}, first {instants[:1]}, '
                         f'rate {rate:.3f} of the refill')
    held, starved = (save_window.loaded(p, name, flood, 13_256) for name, flood in (('save-held', False),
                                                                                  ('save-starved', True)))
    change = lambda g: g.steps.index('mark save.change')
    flood = (starved.steps[change(starved) + 2] == 'flood gm 1' and 'flood gm 0' in starved.steps
             and not any(step.startswith('flood') for step in held.steps))
    offered = {name: sum(1 for _, channel, _ in save_window.arrivals(p, run_ms) if channel == name) + (name == 'aecp')
               for name in scenario.CH}
    declared = all(g.save == dict(image=13_256, records=2, loaded=True, offered=offered) for g in (held, starved))
    return [("every receive channel is held at its contract refill rate with its bursts through a save's stated worst "
             "case: admission's records at once, again every as many refill periods, each channel's bursts apart",
             not wrong, '; '.join(wrong)),
            ("save-starved adds a grandmaster change as every pass starts from its change, save-held does not, and "
             "both time their save against the point's container", flood and declared,
             str((starved.steps[change(starved):change(starved) + 3], held.save, starved.save)))]


def held_load_checks(sys_hz: int, cpu_hz: int) -> list[Check]:
    """A held group commits every record its load offered from its change on, or is refused (save_grade.held_load)."""
    lines = ['MARK 0 save.change', 'RXS 10 0 82 -', 'RXE 92', 'RXC 96 0', 'RXS 200 0 82 -', 'RXE 282',
             'SUMMARY passes=1 sys=1000', 'RESULT: PASS']

    def graded(adp: int) -> bool:
        """Whether the log grades for a group that offered adp ADP records."""
        offered = {name: adp if name == 'adp' else 0 for name in scenario.CH}
        group = scenario.Group('h', save=dict(image=768, records=2, loaded=True, offered=offered))
        try:
            grade.grade('\n'.join(lines) + '\n', group, sys_hz, cpu_hz)
        except grade.Refusal:
            return False
        return True
    got = (graded(1), graded(2))
    return [("a held group is refused unless its receive channels commit every record its load offered from its "
             "change: one committed, one refused by the filter, of two offered", got == (True, False), str(got))]


def step_checks(sys_hz: int, cpu_hz: int) -> list[Check]:
    """The passes that carry the store's step, those that write nothing to the mailbox (STEPPASS) and the work
    passes with step=1, counted, with the longest and the longest step (save_grade.step_figures)."""
    lines = ['PASS 1 1000 500 5000 instr=10 store_mbx=1 step=1 store=3000 W 1100:1:0',
             'STEPPASS 2 9000 4500 120000 store=95000', 'STEPPASS 3 20000 10000 8000 store=7000', 'IDLE 2 8000 120000',
             'PASS 4 40000 20000 9000 instr=10 store_mbx=1 W 40100:1:0', 'SUMMARY passes=4 sys=50000', 'RESULT: PASS']
    s = grade.grade('\n'.join(lines) + '\n', scenario.Group('g'), sys_hz, cpu_hz)['passes']['steps']
    got = (s['passes'], s['cycles'], s['store_cycles'], s['start_sys'])
    return [("every pass that carries the store's step is counted, a pass that writes nothing to the mailbox and a "
             "work pass alike, with the longest of them and the longest step's own CPU time",
             got == (3, 120_000, 95_000, 9000), str(s))]
