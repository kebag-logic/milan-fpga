# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The budget grader self-test's checks of the per-pass share and of the CPU clock (#665), which
selftest.py runs.

The share (share.py) is T_svc's 20 ms, the tightest family bound, over ten passes. Synthetic passes
at it and a cycle over it check grade.pass_share, and the run fails on a pass over it even when
every row fits, unless --record-share-findings records it; --record-budget-findings, the rows'
option, does not. The clock checks build through run.main with build.build's toolchain steps
replaced (selftest.built): the CPU runs in the split placement's clock domain, sys, at the bus
clock, and build.json and every line say so; a build whose SoC puts the CPU on the Milan clock is
refused, and so is a reused build that records its CPU there or records no domain. A pass that
writes nothing to the mailbox is held to the share by its run's longest (sim_main.cpp's IDLE line).
A save in a composed window (save_window.py) is staged at eight tick phases of each flash phase,
after the save's own flash event, and its window carries backlog-adp's load; an aged window opens with
THE STEP's age at its limit or one short of it, at eight delays across the whole tick, and is graded
only with that age proven off its log; a change while a save is in flight is timed against the bound
with that save in flight. Each check is (name, held, detail), as selftest.py's.
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
import save_grade
import save_window
import scenario
import share
import whole_grade

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
    out.append(("the per-pass share is T_svc's 20 ms, the tightest family bound, over ten passes: 2.0 ms, "
                "200,000 CPU cycles at the product's 100 MHz", got == (20.0, SHARE_MS, SHARE_CYCLES), str(got)))
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


def stated_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int) -> list[Check]:
    """A pass given whole to a build or an aged step against the cost THE RETRY's search counts from, and what is not
    held to one: a pass whose round did something, and a pass that built nothing."""
    limits = {kind: us * cpu_hz // 1_000_000 for kind, us in whole_grade.stated_us(2).items()}

    def held(cycles: int, builds: int = 0, aged: bool = False, aecp: int = 0) -> dict:
        """The grade of a pass of those cycles, its builds, whether an aged step's, its AECP modules' cycles."""
        step = 'step=1 store=5 aged=1 ' if aged else ''
        lines = [f'PASS 1 1000 500 {cycles} instr=10 store_mbx=1 {step}mods=aecp:{aecp},srp_mbx:9 W 1001:1:0']
        lines += [f'ENTRY {1002 + k} build_mrpdu' for k in range(builds)]
        return grade.grade(synthetic(lines), scenario.Group('g'), sys_hz, cpu_hz)['passes']['stated']

    kinds = lambda s: [o['kind'] for o in s['over']]
    out = [("a build of one MRPDU has a cost of its own, under a build of two's", limits['build-one'] < limits['build'],
            str(limits)),
           ('each point has its own stated costs',
            whole_grade.stated_us(1)['build'] < whole_grade.stated_us(2)['build'], '')]
    for kind, flags in (('build', dict(builds=2)), ('build-one', dict(builds=1)), ('step', dict(aged=True))):
        at, over = held(limits[kind], **flags), held(limits[kind] + 1, **flags)
        out.append((f'a {kind} pass at its stated cost fits it and one a cycle over it does not',
                    kinds(at) == [] and kinds(over) == [kind] and over['heaviest'][kind] == limits[kind] + 1,
                    str((at, over))))
    heavy = max(limits.values()) + 1
    idle = whole_grade.ROUND_IDLE_CYCLES
    out.append(("a pass whose round did something is not its work alone, and a pass that neither built nor stepped has "
                "no stated cost",
                kinds(held(heavy, builds=2, aecp=idle + 1)) == [] and kinds(held(heavy, aged=True, aecp=idle + 1)) == []
                and kinds(held(heavy)) == [], ''))
    out.append(('a round that found nothing to do leaves the pass its work alone',
                kinds(held(heavy, builds=2, aecp=500)) == ['build'], ''))
    quiet = [f'STEPPASS 2 2000 1000 {limits["step"] + 1} store=5 aged=1']
    alone = grade.grade(synthetic(quiet), scenario.Group('g'), sys_hz, cpu_hz)['passes']['stated']
    out.append(('an aged step in a pass that wrote nothing to the mailbox is held too', kinds(alone) == ['step'],
                str(alone)))
    over = held(limits['build'] + 1, builds=2)
    named = run.stated_misses([dict(group='g', passes=dict(stated=over))])
    out.append(('a pass over its stated cost is named, with the cost it passed',
                named == [f"g: a build pass of {limits['build'] + 1:,} CPU cycles, over its stated "
                          f"{limits['build']:,}"], str(named)))
    args = argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=True,
                              record_share_findings=True)
    out.append(('a pass over its stated cost fails a run whatever findings it records',
                run.verdict(args, [scenario.Group('g')], [], [], [], named) == 1, ''))
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
            *aged_staging_checks(p, want), *second_checks(p), *phase_checks(), *bound_checks(), *held_checks()]


def aged_staging_checks(p: scenario.Point, want: dict) -> list[Check]:
    """Each flash phase's aged windows: after the save's own flash event, a grandmaster change as every pass starts,
    two of the store's steps, the age's centiseconds, a delay, then the window, at the age limit and one short of
    it, at eight delays spread evenly across the whole tick."""
    ms = scenario.MS
    seen: dict[tuple[str, int], list[float]] = {}
    shaped = []
    for g in save_window.aged_windows(p):
        n = next(k for k, step in enumerate(g.steps) if step.startswith('wait flash '))
        phase, age = g.name.partition('@')[2].partition('-')[0], save_window.aged_age(g.name)
        opening = g.steps[n:n + 6 + len(scenario.OPEN_WINDOW)]
        shaped.append(opening[0].partition(' within ')[0] == f'wait {want[phase][0]}'
                      and opening[1] == 'flood gm 1' and opening[2] == f'wait steps 2 within {200 * ms}'
                      and opening[3] == f'wait ticks {age} within {40 * ms}' and opening[5] == 'flood gm 0'
                      and opening[6:] == list(scenario.OPEN_WINDOW)
                      and grade.defined_load(g.name) == grade.defined_load('backlog-adp'))
        seen.setdefault((phase, age), []).append(int(opening[4].split()[-1]) / ms)
    tick = save_window.TICK_MS
    spread = [round((n + 0.5) * tick / 8, 6) for n in range(8)]
    got = {key: [round(d, 6) for d in sorted(delays)] for key, delays in seen.items()}
    expect = {(phase, age): spread for phase in want for age in (2, 1)}
    return [("each flash phase's aged window opens after the save's own flash event, a grandmaster change as every "
             "pass starts, two of the store's steps and its age's centiseconds, at the age limit (two) and one short "
             "of it, eight delays spread evenly across the whole tick, with backlog-adp's defined load",
             got == expect and all(shaped) and len(shaped) == 48, str((got, shaped.count(False))))]


def second_checks(p: scenario.Point) -> list[Check]:
    """A change while a save is in flight: under the flood, a SET_NAME just after a step, then 1,035 ms later, after
    the next step, a SET_NAME of the entity to another value, timed against the bound with that save in flight."""
    ms = scenario.MS
    g = save_window.second(p, 13_256)
    first, again = (f'frame 0 {save_window.set_name(p, v).hex()}' for v in (b'save', b'again'))
    k = g.steps.index('mark save.change')
    got = g.steps[k - 2:k + 6]
    want = ['flood gm 1', f'wait steps 1 within {100 * ms}', 'mark save.change', first,
            f'wait cycles {1035 * ms}', f'wait steps 1 within {100 * ms}', 'mark save.second', again]
    return [("a change while a save is in flight is a SET_NAME of the entity to another value, 1,035 ms and one step "
             "after a first just after a step, under a grandmaster change as every pass starts, timed against the "
             "bound with that save of two records in flight", got == want and first != again and 'flood gm 0' in
             g.steps and g.save == dict(image=13_256, records=2, flight=2), str((got, g.save)))]


def aged_checks(sys_hz: int, cpu_hz: int) -> list[Check]:
    """An aged window's opening age, proven off its log, and the aged step among its records (save_grade.aged_window),
    or a refusal."""
    def tick(cycle: int, count: int) -> list[str]:
        """A TICK record of count centiseconds posted at cycle, its four EVW words."""
        return [f'EVW {cycle} {k} {v:08x}' for k, v in enumerate((save_grade.EV_TICK, count, 0, 0))]

    adp = scenario.CH['adp']
    tail = scenario.ch_word(adp, 'RX_TAIL')
    words = grade.RX_HEADER_WORDS + (82 + 3) // 4

    def graded(name: str, ticks: list[tuple[int, int]], gap: bool = False, aged: str | None = 'read-back',
               drained: bool = False) -> object:
        """The window [5000, 9000] after the step at 1000, its passes between them work passes but for gap's; with
        drained, its one record released at 5600, before its aged step."""
        record = [f'RXS 5050 0 82 -', 'RXE 5132', f'RXC 5136 {adp}'] if drained else []
        release = f' 5600:{tail:x}:{words:x}' if drained else ''
        lines = ['STEPPASS 10 1000 500 80000 store=76000 aged=1', 'PASS 11 2000 1000 5000 instr=10 W 2100:1:0',
                 *([] if gap else ['PASS 12 3000 1500 5000 instr=10 W 3100:1:0']),
                 'PASS 13 4000 2000 5000 instr=10 W 4100:1:0', *(w for c, n in ticks for w in tick(c, n)),
                 'MARK 5000 composed', *record, f'PASS 14 5500 2750 5000 instr=10 W 5600:1:0{release}']
        if aged == 'work':
            # an aged step's pass that writes to the mailbox, as THE RETRY's round after the step does
            lines += ['PASS 15 6000 3000 79000 instr=10 step=1 store=76500 aged=1 W 6900:1:0',
                      'FLASHRD 6100 6200 ee0000 128']
        elif aged == 'plain':
            # the step a pass that took nothing runs, before it ages
            lines += ['STEPPASS 15 6000 3000 77000 store=76500 aged=0', 'FLASHRD 6100 6200 ee0000 128']
        elif aged:
            lines += ['STEPPASS 15 6000 3000 77000 store=76500 aged=1',
                      {'read-back': 'FLASHRD 6100 6200 ee0000 128', 'issue': 'FLASHOP 6100 2 ee0100 256'}[aged]]
        lines += ['PASS 16 7000 3500 5000 instr=10 W 7100:1:0', 'MARK 9000 composed_end']
        log = grade.parse('\n'.join(lines) + '\n', sys_hz, cpu_hz)
        try:
            return save_grade.aged_window(grade.Grader(log), scenario.Group(name), 5000, 9000)
        except grade.Refusal:
            return None
    verify, program, short = 'backlog-adp@verify-aged2-0', 'backlog-adp@program-aged2-0', 'backlog-adp@verify-aged1-0'
    two = [(3000, 1), (4500, 1)]
    inside = [*two, (6500, 1)]
    cases = [graded(verify, two), graded(verify, [(3000, 1)]), graded(verify, [(3000, 2)]),
             graded(verify, two, gap=True), graded(verify, inside, aged=None), graded(program, inside),
             graded(program, two, aged='issue'), graded(short, [(3000, 1)], aged=None),
             graded(verify, [(900, 1), *two]), graded(verify, inside, drained=True), graded(verify, two, aged='work'),
             graded(verify, two, aged=None), graded(verify, inside, aged='plain'), graded(program, inside, aged='plain')]
    got = [None if c is None else (c['age'], [(a['start_ms'], a['kind']) for a in c['among']],
                                   [(a['start_ms'], a['kind']) for a in c['after']]) for c in cases]
    at = round(1000 / sys_hz * 1000, 3)
    want = [(2, [(at, 'read-back')], []), None, (2, [(at, 'read-back')], []), None, None, None,
            (2, [(at, 'issue')], []), (1, [], []), (2, [(at, 'read-back')], []), (2, [], [(at, 'read-back')]),
            (2, [(at, 'read-back')], []), (2, [], []), (2, [], []), None]
    out = [("an aged window is graded only at the age its name declares, the centiseconds its TICK records carried "
            "since its last step, every pass between them a work pass, and, at the age limit, with a step taking its "
            "phase's heavy step (a read-back, a page's issue) in it once a centisecond came in it, aged among its "
            "records or, where it drains before its next centisecond, after the last of them, its pass a work pass or "
            "not, or run by a pass that took nothing; one short of it needs none, nor does a window that closes before "
            "its next centisecond", got == want, str(got))]
    control = argparse.Namespace(cpu_regions='cover', mutation='store-step-aged-heavier', record_budget_findings=False,
                                 record_share_findings=False)
    groups = [scenario.Group('backlog-adp@verify-aged2-3'), scenario.Group('backlog')]
    miss = 'backlog-adp@verify-aged2-3.service.srp.last.if0: 0.4 ms over its budget 20 ms'
    cases = (([miss], []), ([], []), (['backlog.service.srp.last.if0: x'], []), ([miss], ['refused']))
    verdicts = [run.verdict(control, groups, refusals, misses, [], []) for misses, refusals in cases]
    out.append(("the heavier aged step's plant is caught by an aged window's row over its budget, and escapes with "
                "every row within it, a miss in another group only, or a refusal", verdicts == [0, 1, 1, 1],
                str(verdicts)))
    return out


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
    flooded = synthetic_save(ms, [30, 90, 150], [200, 230, 260, 290, 320, 350])
    cases = [('blank', 20, first, True), ('blank', 5, first, False), ('blank', 40, first, False),
             ('program', 40, first, True), ('program', 80, first, True), ('program', 20, first, False),
             ('program', 105, first, False), ('verify', 105, first, True), ('verify', 60, first, False),
             ('verify', 105, another, False), ('verify', 105, later, True), ('verify', 145, first, True),
             ('verify', 155, first, False), ('program', 80, flooded, True), ('program', 160, flooded, True),
             ('program', 185, flooded, False)]
    got = [opens(*case[:3]) for case in cases]
    want = [case[3] for case in cases]
    return [("a save's window is refused unless it opens inside its flash phase of the first save: the blank check "
             "between the erase and the first page, the program phase within 30 ms of a page or before a later one, "
             "as a flooded save's pages 60 ms apart, the verify 30 ms or more after its last page with no later page "
             "and before its read-backs have read back every programmed byte", got == want, str(got))]


def bound_checks() -> list[Check]:
    """A save's stated worst case, restated here on purpose (#665): a changed age limit or step count must fail."""
    got = (save_window.step_age(), save_window.CHANGED, save_window.steps(13_256, 2), save_window.bound_ms(13_256, 2),
           save_window.steps(3_336, 2), save_window.bound_ms(3_336, 2))
    flight = tuple(save_window.bound_ms(image, 2, flight=2) for image in (13_256, 3_336, 768))
    return [("a save's stated worst case is its 1,000 ms first-dirty window, then each of its steps at most three "
             "ticks after the one before (THE STEP's age limit, two centiseconds, plus one), and 10 ms: for a SET_NAME "
             "of the entity, which marks its two names, 12,110 ms at 8x8/2if (370 steps of a 13,256-byte container) "
             "and 4,070 ms at 1x1 (102 of 3,336 bytes)", got == (2, 2, 370, 12_110, 102, 4_070), str(got)),
            ("a change marked while a save is in flight, after its capture took the change's first record, waits for "
             "the rest of that save, its steps less two, or its own first-dirty window where that is longer, then its "
             "own: for a SET_NAME of the entity beside another's save, 22,150 ms at 8x8/2if (368 and 370 steps), "
             "6,070 ms at 1x1 (100 and 102), and a 768-byte container's 1,820 ms, its window the longer",
             flight == (22_150, 6_070, 1_820), str(flight))]


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
    return out + second_time_checks(sys_hz, cpu_hz)


def second_time_checks(sys_hz: int, cpu_hz: int) -> list[Check]:
    """A change while a save is in flight, timed from its mark to durable in the save after the first, against the
    bound with that save in flight, and refused unless marked after the first's first-dirty window and before the
    first save's erase (save_grade.save_time, save_grade.in_flight)."""
    ms = sys_hz // 1000
    group = scenario.Group('second', save=dict(image=768, records=2, flight=2))

    def timed(second_ms: int) -> dict | None:
        """The second change's grade, marked at second_ms, the two saves erasing at 1,200 and 2,000 ms."""
        ops, runs, _ = synthetic_save(ms, [1300, 1500, 1700], [1210, 1220, 1230, 1240, 1250, 1260,
                                                               1800, 1810, 1820, 1830, 1840, 1850], erase=1200)
        ops2, runs2, _ = synthetic_save(ms, [2100, 2300, 2500], [2010, 2020, 2030, 2040, 2050, 2060,
                                                                 2600, 2610, 2620, 2630, 2640, 2650], erase=2000)
        moved = 0x10000
        lines = ['MARK 0 save.change', f'MARK {second_ms * ms} save.second',
                 *(f'FLASHOP {c} {op} {a:06x} {n}' for c, op, a, n in ops),
                 *(f'FLASHOP {c} {op} {a + moved:06x} {n}' for c, op, a, n in ops2),
                 *(f'FLASHRD {a} {b} {c:06x} {n}' for a, b, c, n in runs),
                 *(f'FLASHRD {a} {b} {c + moved:06x} {n}' for a, b, c, n in runs2),
                 f'SUMMARY passes=1 sys={3000 * ms}', 'RESULT: PASS']
        try:
            return grade.grade('\n'.join(lines) + '\n', group, sys_hz, cpu_hz)['save']
        except grade.Refusal:
            return None
    marked, early, late = timed(1100), timed(900), timed(1300)
    got = (marked and (marked['ms'], marked['bound_ms'], marked['within'], marked['flight']), early, late)
    return [("a change marked while a save is in flight is timed from its mark to durable in the next save, against "
             "the bound with that save in flight, and refused when marked inside the first change's first-dirty "
             "window or after the save in flight erased its slot", got == ((1550.7, 1_820, True, 2), None, None),
             str(got))]


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
    first: dict[str, float] = {}
    for when, channel, _ in save_window.held_arrivals(p, run_ms):
        first.setdefault(channel, when)
    refill = scenario.CONTRACT.channels[scenario.CH['aecp']].refill_ms
    starts = {name: round(first[name] - save_window.OFFSET_MS * n, 6) for name, n in scenario.CH.items()}
    offered = {name: sum(1 for _, channel, _ in save_window.arrivals(p, run_ms - 5 * (name == 'aecp'))
                         if channel == name) + (name == 'aecp') for name in scenario.CH}
    declared = all(g.save == dict(image=13_256, records=2, loaded=True, offered=offered) for g in (held, starved))
    return [("every receive channel is held at its contract refill rate with its bursts through a save's stated worst "
             "case: admission's records at once, again every as many refill periods, each channel's bursts apart",
             not wrong, '; '.join(wrong)),
            ("save-starved adds a grandmaster change as every pass starts from its change, save-held does not, and "
             "both time their save against the point's container", flood and declared,
             str((starved.steps[change(starved):change(starved) + 3], held.save, starved.save))),
            ("the held AECP channel's first burst comes one refill period after the change, so the SET_NAME's token is "
             "back before it, and every other channel's at the change", starts == {
                 name: refill if name == 'aecp' else 0 for name in scenario.CH}, str(starts))]


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
             got == (3, 120_000, 95_000, 9000), str(s)), *aged_checks(sys_hz, cpu_hz)]
