# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE SHAPES (#894; the ruling issuecomment-6867393730, item (b)): the static shape an image is built at, as its
builder states it, and tier 2's slice and THE TRANSMIT's builds' stated costs that ctrl_loop.h lists for it.

A shape is (interfaces, talker sources, listener sinks): MBX_N_IF, from the mailbox contract the builder compiles an
image against, and CTRL_SRP_SOURCES and CTRL_SRP_SINKS, which srp_entity.py writes from the configuration into the shape
header the builder force-includes into every unit an image compiles (srp_arms.prepared). ctrl_loop.h lists each shape
with its CTRL_LOOP_SLICE_US, CTRL_LOOP_BUILD_PASS_US and CTRL_LOOP_BUILD_ONE_PASS_US, and a shape not listed fails the
build there (its #error). A compile given no shape header is at the shipping shape's streams, the ones ctrl_loop.h
states as CTRL_LOOP_SOURCES and CTRL_LOOP_SINKS without one (default), which must be what srp_entity.py writes for the
shipping configuration (srp_arms.DEFAULT_ENTITY; findings).

The harness and the model key these costs on the shape the builder writes for a point's configuration and interfaces
(of_config, of_point), never on the point's name. A shape given as an integer is that many interfaces at the shipping
shape's streams (shape), as a compile with no shape header is, so a check written on the interface count reads the
same costs it read before the shapes were listed.

usage: python3 -I shape_costs.py [--check] [--selftest]
  --check     print every listed shape and its costs, each point's shape, and exit 1 on a finding
  --selftest  plant each control and exit 1 unless every one is refused
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[3]
#: Where the table is, and the constants each listed shape states, in its order.
HEADER = 'sw/firmware/ctrl/loop/ctrl_loop.h'
NAMES = ('CTRL_LOOP_SLICE_US', 'CTRL_LOOP_BUILD_PASS_US', 'CTRL_LOOP_BUILD_ONE_PASS_US')
SLICE, BUILD, BUILD_ONE = NAMES
#: The most a slice may be, in microseconds: the ruling issuecomment-6867393730, item (b), which re-rules the cap from
#: 1,300 us; a design parameter, the rows and the load the owner's gate.
SLICE_MOST_US = 1600
#: The shipping configuration, a compile's shape without a shape header (srp_arms.DEFAULT_ENTITY).
DEFAULT_CONFIG = 'configs/endstation_ax7101_1x1_tdm8.yaml'
#: Each point the model and the flip check name, as the image builder builds it: its configuration and interfaces, the
#: same pairs as the harness's points (run.py, POINTS); its shape is what the builder writes for them (of_point).
BUILT = {'1x1/1if': ('endstation_ax7101_1x1_tdm8', 1), '8x8/1if': ('endstation_ax7101_8x8', 1),
         '8x8/2if': ('endstation_ax7101_8x8', 2)}
#: The words the build fails with at a shape the table does not list (ctrl_loop.h's #error).
UNLISTED = 'THE SHAPES: the shape (MBX_N_IF, CTRL_SRP_SOURCES, CTRL_SRP_SINKS) is not one ctrl_loop.h lists'


class Shape(NamedTuple):
    """A static shape: the interfaces, the talker sources and the listener sinks an image is built at."""

    interfaces: int
    sources: int
    sinks: int


def text_of(root: Path, texts: dict[str, str] | None = None) -> str:
    """ctrl_loop.h's text, or its planted copy."""
    return (texts or {}).get(HEADER) or (root / HEADER).read_text()


def listed(text: str) -> dict[Shape, dict[str, int]]:
    """Each shape the header's table lists and its costs in microseconds; a table that is not one #if chain of
    CTRL_LOOP_SHAPE tests, each stating NAMES once as plain numbers, ending in #else and the #error, is refused."""
    lines = text.splitlines()
    starts = [k for k, line in enumerate(lines) if re.match(r'#(?:el)?if CTRL_LOOP_SHAPE\(', line)]
    if not starts or not lines[starts[0]].startswith('#if '):
        raise ValueError('ctrl_loop.h has no table of shapes')
    out: dict[Shape, dict[str, int]] = {}
    k = starts[0]
    while True:
        head = re.match(r'#(?:el)?if CTRL_LOOP_SHAPE\((\d+)u, (\d+)u, (\d+)u\)', lines[k])
        if head is None:
            raise ValueError(f'ctrl_loop.h lists a shape not as three numbers: {lines[k]!r}')
        shape = Shape(*map(int, head.groups()))
        if shape in out:
            raise ValueError(f'ctrl_loop.h lists the shape {tuple(shape)} twice')
        costs: dict[str, int] = {}
        k += 1
        while not re.match(r'#(?:elif|else|endif)\b', lines[k]):
            define = re.fullmatch(r'#define (\w+) (\d+)u', lines[k].split('//')[0].strip())
            if define is None or define[1] not in NAMES or define[1] in costs:
                raise ValueError(f'ctrl_loop.h states {lines[k]!r} for the shape {tuple(shape)}')
            costs[define[1]] = int(define[2])
            k += 1
        if tuple(costs) != NAMES:
            raise ValueError(f'ctrl_loop.h states {", ".join(costs) or "nothing"} for the shape {tuple(shape)}, '
                             f'not {", ".join(NAMES)}')
        out[shape] = costs
        if lines[k].startswith('#else'):
            break
        if not lines[k].startswith('#elif'):
            raise ValueError('ctrl_loop.h\'s table of shapes ends with no #else')
    if not re.fullmatch(rf'#error "{re.escape(UNLISTED)}"', lines[k + 1].strip()) or lines[k + 2] != '#endif':
        raise ValueError('ctrl_loop.h\'s table of shapes does not fail the build at a shape it does not list')
    return out


def default_streams(text: str) -> tuple[int, int]:
    """The sources and sinks ctrl_loop.h takes with no shape header: CTRL_LOOP_SOURCES and CTRL_LOOP_SINKS of the
    #else of its #ifdef CTRL_SRP_SOURCES."""
    pick = re.search(r'^#ifdef CTRL_SRP_SOURCES\n#define CTRL_LOOP_SOURCES CTRL_SRP_SOURCES\n'
                     r'#define CTRL_LOOP_SINKS CTRL_SRP_SINKS\n#else\n#define CTRL_LOOP_SOURCES (\d+)u\n'
                     r'#define CTRL_LOOP_SINKS (\d+)u\n#endif$', text, re.M)
    if pick is None:
        raise ValueError('ctrl_loop.h takes the shape header\'s streams in no form this module reads')
    return int(pick[1]), int(pick[2])


def shape(given: int | Shape, root: Path = ROOT, texts: dict[str, str] | None = None) -> Shape:
    """A Shape as given, or that many interfaces at the streams a compile with no shape header takes."""
    if isinstance(given, Shape):
        return given
    return Shape(int(given), *default_streams(text_of(root, texts)))


def interfaces(given: int | Shape) -> int:
    """The interface count of a Shape or of an integer."""
    return given.interfaces if isinstance(given, Shape) else int(given)


def at(given: int | Shape, root: Path = ROOT, texts: dict[str, str] | None = None) -> dict[str, int]:
    """The costs ctrl_loop.h lists for a shape, in microseconds; a shape it does not list is refused by the build's
    own words."""
    text = text_of(root, texts)
    s = shape(given, root, texts)
    table = listed(text)
    if s not in table:
        raise ValueError(f'{UNLISTED}: {tuple(s)}')
    return dict(table[s])


def streams(header: str) -> tuple[int, int]:
    """The sources and sinks a shape header states (srp_entity.py's text)."""
    found = dict(re.findall(r'^#define (CTRL_SRP_SOURCES|CTRL_SRP_SINKS) (\d+)u$', header, re.M))
    return int(found['CTRL_SRP_SOURCES']), int(found['CTRL_SRP_SINKS'])


def of_config(config: Path, n_if: int, root: Path = ROOT) -> Shape:
    """The shape the builder states for a configuration at that many interfaces: the interfaces, and the streams its own
    shape header writer emits (srp_entity.emit)."""
    where = str(root / "sw/firmware/ctrl/srp")
    if where not in sys.path:
        sys.path.insert(0, where)
    import srp_entity
    return Shape(n_if, *streams(srp_entity.emit(config)))


def of_point(point: str, root: Path = ROOT) -> Shape:
    """The shape the builder states for a point the model names (BUILT)."""
    config, n_if = BUILT[point]
    return of_config(root / 'configs' / f'{config}.yaml', n_if, root)


def findings(root: Path = ROOT, texts: dict[str, str] | None = None) -> list[str]:
    """Each way the table breaks its rules: a slice over the cap or one that cannot hold a build of one, a build of both
    not over the slice that holds one build only or not under two builds of one, a point whose shape is not listed,
    and a default that is not the shipping configuration's streams."""
    text = text_of(root, texts)
    try:
        table = listed(text)
        default = default_streams(text)
    except ValueError as refused:
        return [str(refused)]
    out = []
    for s, c in table.items():
        name = f'the shape {tuple(s)}'
        if c[SLICE] > SLICE_MOST_US:
            out.append(f'{name}: a slice of {c[SLICE]} us, over the ruling\'s {SLICE_MOST_US} us')
        if c[BUILD_ONE] > c[SLICE]:
            out.append(f'{name}: a build of one of {c[BUILD_ONE]} us, over its slice of {c[SLICE]} us')
        if c[BUILD] >= 2 * c[BUILD_ONE] and c[SLICE] < c[BUILD]:
            out.append(f'{name}: a build of both of {c[BUILD]} us, not under two builds of one of {c[BUILD_ONE]} us, '
                       'where its slice holds one build')
    for point in BUILT:
        s = of_point(point, root)
        if s not in table:
            out.append(f'{point}: the builder states the shape {tuple(s)}, which ctrl_loop.h does not list')
    shipping = of_config(root / DEFAULT_CONFIG, 1, root)
    if default != (shipping.sources, shipping.sinks):
        out.append(f'ctrl_loop.h takes {default} streams with no shape header, not the shipping configuration\'s '
                   f'{(shipping.sources, shipping.sinks)}')
    return out


def report(root: Path = ROOT) -> list[str]:
    """Every listed shape's costs, and each point's shape."""
    table = listed(text_of(root))
    lines = ['| Shape (interfaces, sources, sinks) | Slice, us | Build of both, us | Build of one, us | Points |',
             '|---|---:|---:|---:|---|']
    points = {p: of_point(p, root) for p in BUILT}
    for s, c in table.items():
        named = ', '.join(p for p, at_ in points.items() if at_ == s) or 'none the model names'
        lines.append(f'| {tuple(s)} | {c[SLICE]} | {c[BUILD]} | {c[BUILD_ONE]} | {named} |')
    lines.append(f'with no shape header: {default_streams(text_of(root))} streams')
    return lines


def controls(root: Path = ROOT) -> list[str]:
    """Each planted defect the table's checks must refuse: the planted names that escaped."""
    text = text_of(root)
    escaped = []

    def planted(old: str, new: str) -> dict[str, str]:
        """The header with one substitution, refused if it does not apply once."""
        if text.count(old) != 1:
            raise AssertionError(f'control fixture {old!r} does not occur exactly once in {HEADER}')
        return {HEADER: text.replace(old, new)}

    first = next(iter(listed(text)))
    one = listed(text)[first]
    block = (f'#define {SLICE} {one[SLICE]}u\n#define {BUILD} {one[BUILD]}u\n'
             f'#define {BUILD_ONE} {one[BUILD_ONE]}u\n')
    unlisted = Shape(first.interfaces, 3, 3)
    try:
        at(unlisted, root)
        escaped.append('a shape the table does not list')
    except ValueError as refused:
        if UNLISTED not in str(refused):
            escaped.append('a shape the table does not list')
    plants = {
        'a slice over the cap': planted(f'#define {SLICE} {one[SLICE]}u\n', f'#define {SLICE} {SLICE_MOST_US + 5}u\n'),
        'a build of one over its slice': planted(block, block.replace(f'{BUILD_ONE} {one[BUILD_ONE]}u',
                                                                      f'{BUILD_ONE} {one[SLICE] + 5}u')),
        'the table with no #error': planted(f'#error "{UNLISTED}"\n', '#define CTRL_LOOP_SHAPE_UNLISTED 1u\n'),
        'a shape listed twice': planted(block + '#elif', block + f'#elif CTRL_LOOP_SHAPE({first.interfaces}u, '
                                        f'{first.sources}u, {first.sinks}u)\n' + block + '#elif'),
        'a cost missing from a shape': planted(block, block.replace(f'#define {BUILD} {one[BUILD]}u\n', '')),
        'the default streams not the shipping configuration\'s': planted(
            '#else\n#define CTRL_LOOP_SOURCES ', '#else\n#define CTRL_LOOP_SOURCES 1'),
    }
    for name, texts in plants.items():
        if not findings(root, texts):
            escaped.append(name)
    # a build of both at two builds of one where the slice holds one build: the load's and the rows' max() would take
    # the both-branch and count half the builds the built design makes
    for s, c in listed(text).items():
        if c[SLICE] < c[BUILD]:
            line = f'#define {BUILD} {c[BUILD]}u\n#define {BUILD_ONE} {c[BUILD_ONE]}u\n'
            if text.count(line) == 1 and not findings(root, {HEADER: text.replace(
                    line, f'#define {BUILD} {2 * c[BUILD_ONE]}u\n#define {BUILD_ONE} {c[BUILD_ONE]}u\n')}):
                escaped.append('a build of both at two builds of one')
            break
    # the cap itself, the ruling's (issuecomment-6867393730, item (b): re-ruled from 1,300 to 1,600 us)
    if SLICE_MOST_US != 1600:
        escaped.append('the slice cap not the ruling\'s 1,600 us')
    # a point whose shape is not listed
    point = next(iter(BUILT))
    s = of_point(point, root)
    head = f'CTRL_LOOP_SHAPE({s.interfaces}u, {s.sources}u, {s.sinks}u)'
    if not any(point in f for f in findings(root, planted(head, f'CTRL_LOOP_SHAPE({s.interfaces}u, 3u, 3u)'))):
        escaped.append('a point whose shape is not listed')
    return escaped


#: The planted defects controls() plants, in its order.
CONTROLS = ('a shape the table does not list', 'a slice over the cap', 'a build of one over its slice',
            'the table with no #error', 'a shape listed twice', 'a cost missing from a shape',
            'the default streams not the shipping configuration\'s', 'a build of both at two builds of one',
            'the slice cap not the ruling\'s 1,600 us', 'a point whose shape is not listed')


def shape_checks() -> list[tuple[str, bool, str]]:
    """The harness self-test's checks of the table: its findings at the tree none, and every planted defect refused."""
    found = findings(ROOT)
    escaped = controls(ROOT)
    return ([('the table of shapes holds its rules at the tree', not found, '; '.join(found) or 'none')] +
            [(f'the table of shapes refuses {name}', name not in escaped, 'escaped' if name in escaped else 'refused')
             for name in CONTROLS])


def main() -> int:
    """Print the table and its findings, or plant each control and refuse an escape."""
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    rc = 0
    if args.selftest:
        escaped = controls(ROOT)
        for name in escaped:
            print(f'ESCAPED {name}')
        print(f'the table of shapes: {len(CONTROLS) - len(escaped)} of {len(CONTROLS)} planted controls refused')
        rc |= bool(escaped)
    if args.check or not args.selftest:
        print('\n'.join(report(ROOT)))
        found = findings(ROOT)
        for line in found:
            print('FINDING', line)
        print('RESULT: FAIL' if found else 'RESULT: PASS')
        rc |= bool(found)
    return rc


if __name__ == '__main__':
    sys.exit(main())
