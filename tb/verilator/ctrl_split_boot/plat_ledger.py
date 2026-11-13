#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The target platform's image at every point, against the memory ledger (#665).

Builds, all outside the checkout under --build-dir:
  1. each shape's flash port map and the csr.csv of the split SoC's export it is generated from (the CPU budget
     harness's build.flash_map, as the split boot simulation builds them);
  2. the bare-metal runtime archives, once (the split boot simulation's runtime());
  3. the platform image (ctrl_plat_image.py) at each of POINTS, against its shape's csr.csv and flash map, naming the
     override the point takes (ctrl_memory.LEDGERED, --ledgered-point) where POINTS names one.
Then grades each image, each check apart, so that one finding does not hide another (#665: a stale ctrl_plat size in
the platform's override refused its 8x8 image with two interfaces by its key, so that image's plan, past the tiles
the override then held, was never read):
  LINK   ctrl_plat_image.py exited 0, and the image's plan as it plans it, with the point's override, is accepted;
  KEY    the image's ctrl_plat is the size ctrl_memory_ledger.py records for its point (the memory test's cases), and
         at an override's point the image carries every symbol of that override at its listed size;
  TILES  the image's plan, read with no budget, is within its override's tiles, or without one within
         ctrl_memory.BUDGET_TILES, the 56-RAMB36 budget;
  LEDGER every override of the platform's image (an entry that lists ctrl_plat) is linked at a point.
--controls grades a finished run's images again, in this process, under each planted ledger of CONTROLS, and
requires each to be graded as the control says: the findings of its kinds at its points and none other. --self-test
builds and grades, then runs the controls.

Exit 0 when every point passes (and, with --self-test, every control is graded as it requires); 1 = a finding;
2 = refused.
"""
from __future__ import annotations

import argparse
import contextlib
import dataclasses
import math
import sys
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'sw/litex'))
import ctrl_memory  # noqa: E402
import ctrl_memory_ledger as ledgers  # noqa: E402

BUDGET = ROOT / 'tb/verilator/ctrl_service_budget'
IMAGE = ROOT / 'sw/firmware/ctrl/test/ctrl_plat_image.py'


class Point(NamedTuple):
    """One point of the ledger: its shape, its interfaces, the override it takes (None for the budget) and the name of
    ctrl_memory_ledger.py's record of its ctrl_plat size."""

    shape: str
    interfaces: int
    override: str | None
    plat: str


#: The four points the ledger names (ctrl_memory_ledger.PLAT_*): the shipping 1x1 shape and the 8x8 one, each with
#: one and two interfaces; the 8x8 image with two interfaces takes the platform's override.
POINTS = (Point('endstation_ax7101_1x1_tdm8', 1, None, 'PLAT_1X1_1'),
          Point('endstation_ax7101_1x1_tdm8', 2, None, 'PLAT_1X1_2'),
          Point('endstation_ax7101_8x8', 1, None, 'PLAT_8X8_1'),
          Point('endstation_ax7101_8x8', 2, 'platform-8x8-two-interfaces', 'PLAT_8X8_2'))


def name(point: Point) -> str:
    """The point's directory and label: its shape and its interfaces."""
    return f"{'8x8' if '8x8' in point.shape else '1x1'}-if{point.interfaces}"


def run(argv: list[str], log: Path, cwd: Path = ROOT) -> int:
    """One build step in the foreground, its whole output in its log; its exit status."""
    import subprocess
    print('COMMAND', ' '.join(argv), flush=True)
    with log.open('w') as sink:
        return subprocess.run(argv, cwd=cwd, stdout=sink, stderr=subprocess.STDOUT, check=False).returncode


def maps(out: Path, shape: str) -> tuple[Path, Path]:
    """The shape's split SoC csr.csv and flash port map (build.flash_map's two exports, the second's csr.csv)."""
    sys.path.insert(0, str(BUDGET))
    import build as budget_build
    generated = budget_build.flash_map(out / shape / 'split-soc/flash-map', shape)
    return generated.parent / 'mapped/soc/csr.csv', generated


def link(out: Path, point: Point, csr_csv: Path, flash_map: Path, archives: tuple[Path, Path]) -> int:
    """The platform image at one point, naming its override where it takes one; ctrl_plat_image.py's exit status,
    saved beside its log."""
    where = out / name(point)
    rc = run([sys.executable, '-B', str(IMAGE), '--config', str(ROOT / 'configs' / f'{point.shape}.yaml'),
              '--interfaces', str(point.interfaces), '--csr-csv', str(csr_csv), '--flash-map', str(flash_map),
              '--output', str(where), '--libc', str(archives[0]), '--compiler-runtime', str(archives[1]),
              *([] if point.override is None else ['--ledgered-point', point.override])], where.with_suffix('.log'))
    where.with_suffix('.rc').write_text(f'{rc}\n')
    return rc


def build(out: Path) -> None:
    """Every map, the runtime and every point's link (build steps refuse by raising; a link's refusal is graded)."""
    sys.path.insert(0, str(HERE))
    import run as boot
    out.mkdir(parents=True, exist_ok=True)
    archives = boot.runtime(out)
    for shape in dict.fromkeys(p.shape for p in POINTS):
        csr_csv, flash_map = maps(out, shape)
        for point in (p for p in POINTS if p.shape == shape):
            link(out, point, csr_csv, flash_map, archives)


def refused(log: Path) -> str:
    """The REFUSED line a link printed, or its last line."""
    lines = log.read_text().splitlines() if log.is_file() else ['no log']
    return next((ln for ln in lines if ln.startswith('REFUSED')), lines[-1] if lines else 'an empty log')


def overrides() -> set[str]:
    """The ledger's overrides of the platform's image: each entry whose symbols list ctrl_plat."""
    return {n for n, p in ctrl_memory.LEDGERED.items() if any(s == 'ctrl_plat' for s, _ in p.symbols)}


def grade_point(out: Path, point: Point) -> Iterator[str]:
    """Each finding at one point: LINK, KEY and TILES, each read apart."""
    where = out / name(point)
    rc = (where.with_suffix('.rc')).read_text().strip() if where.with_suffix('.rc').is_file() else 'none'
    elf = where / 'ctrl_app.elf'
    if not elf.is_file():
        yield f'LINK {name(point)}: no image (exit {rc}: {refused(where.with_suffix(".log"))})'
        return
    if rc != '0':
        yield f'LINK {name(point)}: ctrl_plat_image.py exited {rc}: {refused(where.with_suffix(".log"))}'
    image = ctrl_memory.read_elf(elf)
    try:
        ctrl_memory.plan(image, ledgered=point.override)
    except ctrl_memory.Refusal as error:
        yield f'LINK {name(point)}: its plan is refused ({error})'
    carried = image.symbols.get('ctrl_plat', (0, None))[1]
    recorded = getattr(ledgers, point.plat)
    if carried != recorded:
        yield f'KEY {name(point)}: ctrl_memory_ledger.{point.plat} records {recorded:,} B, the image carries {carried}'
    held = None if point.override is None else ctrl_memory.LEDGERED.get(point.override)
    if point.override is not None and held is None:
        yield f'KEY {name(point)}: the ledger holds no {point.override!r}'
    elif held is not None:
        listed = dict(held.symbols)
        actual = {s: image.symbols.get(s, (0, None))[1] for s in listed}
        if actual != listed:
            yield f'KEY {name(point)}: {point.override!r} lists {listed}, the image carries {actual}'
    tiles = ctrl_memory.plan(image, budget=math.inf).tiles
    limit = ctrl_memory.BUDGET_TILES if held is None else held.tiles
    if tiles > limit:
        yield (f'TILES {name(point)}: {tiles:g} RAMB36 past the {limit:g} '
               f'{"budget" if held is None else "its override ledgers"}')


def grade(out: Path) -> tuple[list[str], list[str]]:
    """Every point's findings and its report line, and LEDGER: every platform override linked at a point."""
    findings, report = [], []
    for point in POINTS:
        found = list(grade_point(out, point))
        findings += found
        elf = out / name(point) / 'ctrl_app.elf'
        if elf.is_file():
            image = ctrl_memory.read_elf(elf)
            plan = ctrl_memory.plan(image, budget=math.inf)
            report.append(f'POINT {name(point)}: rom {plan.rom_bytes:,} B, sram {plan.ram_bytes:,} B, '
                          f'{plan.tiles:g} RAMB36 ({point.override or "the 56-RAMB36 budget"}), ctrl_plat '
                          f'{image.symbols.get("ctrl_plat", (0, None))[1]} B: {"PASS" if not found else "FAIL"}')
    unlinked = overrides() - {p.override for p in POINTS}
    if unlinked:
        findings.append(f'LEDGER: {sorted(unlinked)} override(s) of the platform\'s image linked at no point')
    return findings, report


@contextlib.contextmanager
def planted(module: object, attribute: str, value: object) -> Iterator[None]:
    """`module.attribute` set to `value` for the block, then restored."""
    saved = getattr(module, attribute)
    setattr(module, attribute, value)
    try:
        yield
    finally:
        setattr(module, attribute, saved)


def entry(change: Callable[[ctrl_memory.Ledgered], ctrl_memory.Ledgered]) -> dict[str, ctrl_memory.Ledgered]:
    """The ledger with the platform's 8x8 two-interface entry changed."""
    held = ctrl_memory.LEDGERED
    point = POINTS[-1].override
    return {**held, point: change(held[point])}


def stale(p: ctrl_memory.Ledgered) -> ctrl_memory.Ledgered:
    """The entry's ctrl_plat size 64 B short, a step of the struct's 64-byte alignment."""
    return dataclasses.replace(p, symbols=tuple((s, n - 64 if s == 'ctrl_plat' else n) for s, n in p.symbols))


def short(out: Path) -> Callable[[ctrl_memory.Ledgered], ctrl_memory.Ledgered]:
    """The entry's tiles half a tile under its image's plan."""
    plan = ctrl_memory.plan(ctrl_memory.read_elf(out / name(POINTS[-1]) / 'ctrl_app.elf'), budget=math.inf)
    return lambda p: dataclasses.replace(p, tiles=plan.tiles - 0.5)


class Control(NamedTuple):
    """A planted ledger: what it plants (a context over the run's directory) and the findings it must give, as
    (kind, point) pairs."""

    plant: Callable[[Path], contextlib.AbstractContextManager]
    want: frozenset[tuple[str, str]]


LAST, FIRST, ONE8 = name(POINTS[-1]), name(POINTS[0]), name(POINTS[2])
#: The planted ledgers: a stale key alone, a plan past its tiles alone, both at once (the case that hid, #665), a
#: stale record in ctrl_memory_ledger.py, the budget under a point's plan (read by TILES; the link plans against
#: ctrl_memory.plan's own default, which a rebinding of the name does not move), the override not taken, and an
#: override of the platform's image that no point links.
CONTROLS = {
    'stale-key': Control(lambda out: planted(ctrl_memory, 'LEDGERED', entry(stale)),
                         frozenset({('LINK', LAST), ('KEY', LAST)})),
    'past-its-tiles': Control(lambda out: planted(ctrl_memory, 'LEDGERED', entry(short(out))),
                              frozenset({('LINK', LAST), ('TILES', LAST)})),
    'stale-key-past-its-tiles': Control(lambda out: planted(ctrl_memory, 'LEDGERED',
                                                            entry(lambda p: short(out)(stale(p)))),
                                        frozenset({('LINK', LAST), ('KEY', LAST), ('TILES', LAST)})),
    'stale-record': Control(lambda out: planted(ledgers, POINTS[0].plat, getattr(ledgers, POINTS[0].plat) - 64),
                            frozenset({('KEY', FIRST)})),
    'budget-under-a-point': Control(lambda out: planted(ctrl_memory, 'BUDGET_TILES', ctrl_memory.plan(
        ctrl_memory.read_elf(out / ONE8 / 'ctrl_app.elf'), budget=math.inf).tiles - 0.5),
                                    frozenset({('TILES', ONE8)})),
    'override-not-taken': Control(lambda out: planted(sys.modules[__name__], 'POINTS',
                                                      (*POINTS[:-1], POINTS[-1]._replace(override=None))),
                                  frozenset({('LINK', LAST), ('TILES', LAST), ('LEDGER', '')})),
    'override-unlinked': Control(lambda out: planted(ctrl_memory, 'LEDGERED', {
        **ctrl_memory.LEDGERED, 'platform-8x8-one-interface': dataclasses.replace(
            ctrl_memory.LEDGERED[POINTS[-1].override], symbols=(('ctrl_plat', ledgers.PLAT_8X8_1),))}),
        frozenset({('LEDGER', '')})),
}


def kinds(findings: list[str]) -> set[tuple[str, str]]:
    """Each finding's kind and point."""
    out = set()
    for finding in findings:
        kind, _, rest = finding.partition(' ')
        out.add((kind.rstrip(':'), '' if kind.endswith(':') else rest.partition(':')[0]))
    return out


def controls(out: Path) -> int:
    """Each planted ledger graded on the run's images; the number not graded as it requires."""
    wrong = 0
    for label, control in CONTROLS.items():
        with control.plant(out):
            findings, _ = grade(out)
        got = kinds(findings)
        ok = got == control.want
        wrong += not ok
        print(f'CONTROL {label}: {"as required" if ok else "WRONG"} (findings {sorted(got)}, required '
              f'{sorted(control.want)}): {findings}')
    print(f'plat_ledger controls: {len(CONTROLS) - wrong} of {len(CONTROLS)} as required')
    return wrong


def main() -> int:
    """Build and grade every point, or grade the controls on a finished run, or both."""
    parser = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--regrade', action='store_true', help='grade the images of an earlier run in --build-dir')
    parser.add_argument('--controls', action='store_true',
                        help='grade every planted ledger (CONTROLS) on the finished run in --build-dir')
    parser.add_argument('--self-test', action='store_true', help='build and grade, then grade every control')
    args = parser.parse_args()
    out = args.build_dir.resolve()
    if out == ROOT or ROOT in out.parents:
        parser.error('use an external scratch build directory')
    try:
        if not (args.regrade or args.controls):
            build(out)
        if args.controls:
            return 1 if controls(out) else 0
        findings, report = grade(out)
        wrong = controls(out) if args.self_test else 0
    except (RuntimeError, OSError, ValueError, KeyError) as error:
        print(f'REFUSED: {error}')
        return 2
    print('\n'.join(report))
    for finding in findings:
        print(f'FINDING: {finding}')
    print(f'plat_ledger: {"FAIL" if findings else "PASS"} ({len(findings)} finding(s))')
    return 1 if findings or wrong else 0


if __name__ == '__main__':
    raise SystemExit(main())
