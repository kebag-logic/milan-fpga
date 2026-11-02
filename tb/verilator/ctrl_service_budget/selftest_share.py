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
    windows = [g for g in save_window.groups(p) if '@' in g.name]
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
            *phase_checks()]


def phase_checks() -> list[Check]:
    """A save's window opens inside its flash phase of the first save, or is refused (grade.save_phase)."""
    erase, page, ms = grade.FLASH_ERASE, grade.FLASH_PROGRAM, scenario.MS
    first = [(10 * ms, erase), (30 * ms, page), (50 * ms, page), (70 * ms, page)]

    def opens(phase: str, start_ms: float, flash: list) -> bool:
        """Whether a window opening at start_ms is graded inside phase."""
        try:
            grade.save_phase(grade.Log(100_000_000, 100_000_000, flash=flash), f'backlog-adp@{phase}-0',
                             int(start_ms * ms))
        except grade.Refusal:
            return False
        return True
    later = first + [(200 * ms, erase), (220 * ms, page)]
    cases = [('blank', 20, first, True), ('blank', 5, first, False), ('blank', 40, first, False),
             ('program', 40, first, True), ('program', 80, first, True), ('program', 20, first, False),
             ('program', 105, first, False), ('verify', 105, first, True), ('verify', 60, first, False),
             ('verify', 105, first + [(110 * ms, page)], False), ('verify', 105, later, True)]
    got = [opens(*case[:3]) for case in cases]
    want = [case[3] for case in cases]
    return [("a save's window is refused unless it opens inside its flash phase of the first save: the blank check "
             "between the erase and the first page, the program phase within 30 ms of a page, the verify 30 ms or "
             "more after its last page with no later page", got == want, str(got))]
