# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The budget grader self-test's checks of the per-pass share and of the CPU clock (#665), which
selftest.py runs.

The share (share.py) is SRP's 18 ms, the tightest family bound, over nine passes. Synthetic passes
at it and a cycle over it check grade.pass_share, and the run fails on a pass over it even when
every row fits, unless --record-share-findings records it; --record-budget-findings, the rows'
option, does not. The clock checks build through run.main with build.build's toolchain steps
replaced (selftest.built): by default the CPU runs at the product's split CPU clock and build.json
says so; --cpu-hz is a labelled option, named on every line, and a reused build at another clock is
refused. Each check is (name, held, detail), as selftest.py's.
"""
from __future__ import annotations

import argparse
import runpy
import tempfile
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import yaml

import build
import grade
import run
import scenario
import share

ROOT = Path(__file__).resolve().parents[3]
#: The share and the product's split CPU clock, restated here on purpose: a changed value must fail.
SHARE_MS = 2.0
SHARE_CYCLES = {50_000_000: 100_000, 100_000_000: 200_000}
PRODUCT_CPU_HZ = 50_000_000
Check = tuple[str, bool, str]


def share_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int) -> list[Check]:
    """The share's value, a pass at it and a cycle over it, and the run's verdict and table on them."""
    out = []
    got = (share.bound_ms(), share.share_ms(), {hz: share.share_cycles(hz) for hz in SHARE_CYCLES})
    out.append(("the per-pass share is SRP's 18 ms, the tightest family bound, over nine passes: 2.0 ms, "
                '100,000 CPU cycles at 50 MHz', got == (18.0, SHARE_MS, SHARE_CYCLES), str(got)))
    limit = SHARE_CYCLES[cpu_hz]
    lines = [f'PASS {n} {s} {s // 2} {c} instr=10 store_mbx=1 W {s + 100}:1:0' for n, (s, c)
             in enumerate(((1000, limit), (400_000, limit + 1), (900_000, 50)), 1)]
    graded = grade.grade(synthetic(lines), scenario.Group('g'), sys_hz, cpu_hz)
    s = graded['passes']['share']
    got = (s['passes'], s['over'], [p['cycles'] for p in s['over_passes']])
    out.append(('a work pass at the share fits it and one a cycle over it does not', got == (3, 1, [limit + 1]),
                str(s)))
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
    table = run.table([graded], '1x1', 'CPU 50 MHz')
    saved = run.summary('1x1', '0' * 64, [graded], [], [], shares)['share_misses']
    rendered = (f'| g | 3 | 1 | {limit + 1:,} ({(limit + 1) / (cpu_hz / 1000):.3f}) | OVER the share |' in table
                and table.startswith('### 1x1\n\nClock: CPU 50 MHz.\n'))
    out.append(('the table names the clock and each group against the share, and results.json keeps the passes over it',
                rendered and saved == shares, table[:400]))
    return out


def clock_checks(built: Callable[..., tuple[str, dict]], main_verdict: Callable[..., str]) -> list[Check]:
    """The product's split CPU clock by default, the labelled option, and a reuse at another clock."""
    out = []
    contract = runpy.run_path(str(ROOT / 'tb/verilator/nvm_capture_cpu/recipe.py'))['CPU_HZ']
    points = {point: yaml.safe_load((ROOT / 'configs' / f'{shape}.yaml').read_text())['board']['constraints']
              ['milan_clk_hz'] for point, (shape, _) in run.POINTS.items()}
    out.append(("each point's product split CPU clock, its milan_clk_hz, is the bare-metal build contract's 50 MHz",
                set(points.values()) == {contract} == {PRODUCT_CPU_HZ}, str((points, contract))))
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        (root / 'firmware').mkdir()
        (root / 'firmware/adp.c').write_text('c')
        with patch.object(build, 'FIRMWARE_TREES', (str(root / 'firmware'),)):
            runs = {'product': built(root / 'product'), 'option': built(root / 'option', '--cpu-hz', '100000000')}
            got = {name: (verdict, spec.get('cpu_hz'), spec.get('cpu_clock'), spec.get('cpu_hz_option'))
                   for name, (verdict, spec) in runs.items()}
            want = {'product': ('reached', PRODUCT_CPU_HZ, 'product', None),
                    'option': ('reached', 100_000_000, 'option', 100_000_000)}
            out.append(("by default the CPU runs at the product's split CPU clock and build.json says so; another "
                        'clock is a labelled option', got == want, str(got)))
            lines = [build.clock_line(spec) for _, spec in runs.values()]
            out.append(("the clock line names the product's clock, and the option as not the product's",
                        lines == ["CPU 50 MHz, the product's split CPU clock (the Milan clock), bus 100 MHz",
                                  "CPU 100 MHz, a labelled option: not the product's split CPU clock, 50 MHz, "
                                  'bus 100 MHz'], str(lines)))
            cases = [('product', (), True), ('product', ('--cpu-hz', '100000000'), False),
                     ('option', ('--cpu-hz', '100000000'), True), ('option', (), False)]
            verdicts = [main_verdict(root / name, '--reuse-build', *flags) for name, flags, _ in cases]
    wrong = [f'{name} {flags}: {verdict}' for (name, flags, reuse), verdict in zip(cases, verdicts)
             if not (verdict == 'reached' if reuse else verdict.startswith('exit 2:') and 'CPU clock' in verdict)]
    out.append(('the run refuses a reused build at another CPU clock and reuses one at the selected clock', not wrong,
                '; '.join(wrong)))
    return out
