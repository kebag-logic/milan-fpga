# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE SHAPES (#894; the ruling issuecomment-6867393730, item (b)): the static shape an image is built at, as its
builder states it, and tier 2's slice, THE TRANSMIT's builds' stated costs, an SRP record's stated cost and THE RETRY's
round costs that ctrl_loop.h lists for it (the ruling issuecomment-6871343905, item (b)(ii): CTRL_LOOP_SRP_UNIT_US per
shape; the ruling issuecomment-6878014227, item 1: a round's cold start and a refused attempt per shape).

A shape is (interfaces, talker sources, listener sinks): MBX_N_IF, from the mailbox contract the builder compiles an
image against, and CTRL_SRP_SOURCES and CTRL_SRP_SINKS, which srp_entity.py writes from the configuration into the shape
header the builder force-includes into every unit an image compiles (srp_arms.prepared). ctrl_loop.h lists each shape
with its CTRL_LOOP_SLICE_US, CTRL_LOOP_BUILD_PASS_US, CTRL_LOOP_BUILD_ONE_PASS_US, CTRL_LOOP_SRP_UNIT_US,
CTRL_LOOP_RETRY_COLD_US and CTRL_LOOP_RETRY_ATTEMPT_US, and a shape not listed fails the build there (its #error).
AECP_ROUND_COLD_US (aecp_mbx.h) and AECP_ATTEMPT_US (aecp.h) are the last two by name, so every point reads its own
shape's, never the interface count's (retry_findings). A compile given no shape header is at the shipping shape's
streams, the ones ctrl_loop.h states as CTRL_LOOP_SOURCES and CTRL_LOOP_SINKS without one (default), which must be what
srp_entity.py writes for the shipping configuration (srp_arms.DEFAULT_ENTITY; findings).

The shape header also states the AEM descriptors that bear AECP's change notices (CTRL_AEM_STREAM_INPUTS and the rest),
from which aecp.h derives AECP_NOTICES_MOST, the most notices a datapath reset can leave pending (#894's ruling
issuecomment-6871343905, item (b)(iv)): findings holds it at each point to the notices the descriptors hold, counted
apart from aecp.h (notices_held), at one interface exactly. And it states the key domain of an AUDIO_MAP edit, which
sizes the map edits' direct index (aecp_maps.c; #894's ruling issuecomment-6870437042, item 1), as its single source
in every unit an image compiles (the ruling issuecomment-6871343905, item (c)): aecp_entity_gen.h states it only for a
compile given no shape header, by the same derivation (key_findings).

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
import functools
import re
import sys
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
#: Where the table is, and the constants each listed shape states, in its order.
HEADER = 'sw/firmware/ctrl/loop/ctrl_loop.h'
NAMES = ('CTRL_LOOP_SLICE_US', 'CTRL_LOOP_BUILD_PASS_US', 'CTRL_LOOP_BUILD_ONE_PASS_US', 'CTRL_LOOP_SRP_UNIT_US',
         'CTRL_LOOP_RETRY_COLD_US', 'CTRL_LOOP_RETRY_ATTEMPT_US')
SLICE, BUILD, BUILD_ONE, SRP_UNIT, RETRY_COLD, RETRY_ATTEMPT = NAMES
#: THE RETRY's round costs AECP reads, each where it is defined and the name of the table's it must be: a round's cold
#: start, which the adapter admits a round at, and a refused attempt's, which the core charges (#894's ruling
#: issuecomment-6878014227, item 1).
RETRY = {'AECP_ROUND_COLD_US': ('sw/firmware/ctrl/aecp/aecp_mbx.h', RETRY_COLD),
         'AECP_ATTEMPT_US': ('sw/firmware/ctrl/aecp/aecp.h', RETRY_ATTEMPT)}
#: The most a slice may be, in microseconds: the ruling issuecomment-6867393730, item (b), which re-rules the cap from
#: 1,300 us; a design parameter, the rows and the load the owner's gate.
SLICE_MOST_US = 1600
#: The shipping configuration, a compile's shape without a shape header (srp_arms.DEFAULT_ENTITY).
DEFAULT_CONFIG = 'configs/endstation_ax7101_1x1_tdm8.yaml'
#: Each point the model and the flip check name, as the image builder builds it: its configuration and interfaces, the
#: same pairs as the harness's points (run.py, POINTS); its shape is what the builder writes for them (of_point).
BUILT = {'1x1/1if': ('endstation_ax7101_1x1_tdm8', 1), '8x8/1if': ('endstation_ax7101_8x8', 1),
         '8x8/2if': ('endstation_ax7101_8x8', 2)}
#: Where AECP_NOTICES_MOST is derived, and the notice-bearing descriptors the shape header states, by descriptor_type
#: (IEEE 1722.1-2021 Table 7-1: STREAM_INPUT, STREAM_OUTPUT, AVB_INTERFACE, CLOCK_DOMAIN;
#: srp_entity.NOTICE_DESCRIPTORS).
AECP_HEADER = 'sw/firmware/ctrl/aecp/aecp.h'
NOTICE_DESCRIPTORS = {5: 'CTRL_AEM_STREAM_INPUTS', 6: 'CTRL_AEM_STREAM_OUTPUTS', 9: 'CTRL_AEM_AVB_INTERFACES',
                      36: 'CTRL_AEM_CLOCK_DOMAINS'}
#: The key domain of an AUDIO_MAP edit (aecp_shape.key_domain), which the shape header states and aecp_entity_gen.h only
#: where a compile has none (its #ifndef CTRL_SRP_ENTITY_H).
KEY_DOMAIN = ('AECP_ENTITY_KEY_STREAMS', 'AECP_ENTITY_KEY_STREAM_CHANNELS', 'AECP_ENTITY_KEY_CLUSTERS',
              'AECP_ENTITY_KEY_CLUSTER_CHANNELS')
KEY_GUARD = '#ifndef CTRL_SRP_ENTITY_H'
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


@functools.lru_cache(maxsize=None)
def header_of(config: Path, root: Path = ROOT) -> str:
    """The shape header the builder writes for a configuration (srp_entity.emit), once a configuration."""
    where = str(root / "sw/firmware/ctrl/srp")
    if where not in sys.path:
        sys.path.insert(0, where)
    import srp_entity
    return srp_entity.emit(config)


def of_config(config: Path, n_if: int, root: Path = ROOT) -> Shape:
    """The shape the builder states for a configuration at that many interfaces: the interfaces, and the streams its own
    shape header writer emits (srp_entity.emit)."""
    return Shape(n_if, *streams(header_of(config, root)))


def descriptors(header: str) -> dict[str, int]:
    """The notice-bearing AEM descriptor counts a shape header states, by name (NOTICE_DESCRIPTORS)."""
    return {name: int(n) for name, n in re.findall(r'^#define (CTRL_AEM_\w+) (\d+)u$', header, re.M)}


@functools.lru_cache(maxsize=None)
def aecp_header_of(config: Path, root: Path = ROOT) -> str:
    """The AEM image's header the builder writes for a configuration (aecp_entity.emit), once a configuration."""
    where = str(root / "sw/firmware/ctrl/aecp")
    if where not in sys.path:
        sys.path.insert(0, where)
    import aecp_entity
    return aecp_entity.emit(config)


def key_domain(text: str) -> dict[str, int]:
    """The key domain a generated header's text states (KEY_DOMAIN), by name."""
    return {name: int(n) for name, n in re.findall(rf'^#define ({"|".join(KEY_DOMAIN)}) (\d+)u$', text, re.M)}


def key_findings(root: Path = ROOT) -> list[str]:
    """The map edits' key domain at each point and at the shipping configuration: the shape header not stating all of
    it, aecp_entity_gen.h stating any of it outside its KEY_GUARD (an image would read two sources), or the two not the
    same (a host arm's table and an image's would differ)."""
    out = []
    for point, config in [*((p, c) for p, (c, _) in BUILT.items()), ('the shipping configuration', None)]:
        path = root / (DEFAULT_CONFIG if config is None else f'configs/{config}.yaml')
        shape, aem = key_domain(header_of(path, root)), aecp_header_of(path, root)
        missing = [name for name in KEY_DOMAIN if name not in shape]
        if missing:
            out.append(f'{point}: the shape header does not state {", ".join(missing)}, the map edits\' key domain')
        guarded = aem.split(KEY_GUARD, 1)[1].split('#endif', 1)[0] if KEY_GUARD in aem else ''
        outside = [name for name in key_domain(aem.replace(guarded, '')) if name in KEY_DOMAIN]
        if outside:
            out.append(f'{point}: aecp_entity_gen.h states {", ".join(outside)} outside {KEY_GUARD}, beside the shape '
                       'header')
        for name, value in key_domain(guarded or aem).items():
            if name in shape and shape[name] != value:
                out.append(f'{point}: the shape header states {name} {shape[name]}, not the image\'s {value}')
    return out


def evaluated(text: str, name: str, values: dict[str, int], last: bool = False) -> int:
    """A constant of a header's text, each name it reads `values`' or the text's own #define, its first (the branch a
    shape header selects) or with `last` its last (a compile's with no shape header), a ternary on a comparison taken,
    and the arithmetic evaluated (rows_grade.arithmetic)."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    from rows_grade import arithmetic
    defines: dict[str, str] = {}
    for m in re.finditer(r'^#define (\w+) (.+)$', text, re.M):
        if last or m[1] not in defines:
            defines[m[1]] = m[2].split('//')[0].strip()

    def value(key: str) -> int:
        """One name's value."""
        if key in values:
            return values[key]
        body = re.sub(r'[A-Z][A-Z0-9_]+', lambda m: str(value(m[0])), re.sub(r'(\d+)u\b', r'\1', defines[key]))
        pick = re.fullmatch(r'\((.+?) == (\d+) \? (.+) : (.+)\)', body)
        return arithmetic(pick[3] if arithmetic(pick[1]) == int(pick[2]) else pick[4]) if pick else arithmetic(body)
    return value(name)


def aecp_text(root: Path, texts: dict[str, str] | None = None) -> str:
    """aecp.h's text, or its planted copy."""
    return (texts or {}).get(AECP_HEADER) or (root / AECP_HEADER).read_text()


def notices_most(config: Path, n_if: int, root: Path = ROOT, texts: dict[str, str] | None = None) -> int:
    """AECP_NOTICES_MOST as aecp.h derives it for an image of a configuration at that many interfaces, through the shape
    header the builder writes for it."""
    return evaluated(aecp_text(root, texts), 'AECP_NOTICES_MOST',
                     {**descriptors(header_of(config, root)), 'MBX_N_IF': n_if})


def notices_held(config: Path, root: Path = ROOT) -> int:
    """The notices a configuration's descriptors hold, counted apart from aecp.h: each notice-bearing descriptor the
    shape header states, times the notices the harness reads a descriptor of its kind for (notice_window.KINDS)."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import notice_window
    counts = descriptors(header_of(config, root))
    return sum(len(commands) * counts[NOTICE_DESCRIPTORS[kind]] for kind, commands in notice_window.KINDS)


def of_point(point: str, root: Path = ROOT) -> Shape:
    """The shape the builder states for a point the model names (BUILT)."""
    config, n_if = BUILT[point]
    return of_config(root / 'configs' / f'{config}.yaml', n_if, root)


def findings(root: Path = ROOT, texts: dict[str, str] | None = None) -> list[str]:
    """Each way the table breaks its rules: a slice over the cap or one that cannot hold a build of one or an SRP record
    (ctrl_loop.c's _Static_assert), a build of both not over the slice that holds one build only or not under two builds
    of one, a point whose shape is not listed, a listed shape whose polls poll_grade.py does not state, and a default
    that is not the shipping configuration's streams; AECP_NOTICES_MOST (notice_findings); and the map edits' key
    domain (key_findings)."""
    text = text_of(root, texts)
    try:
        table = listed(text)
        default = default_streams(text)
    except ValueError as refused:
        named = [p for p in BUILT if f'the shape {tuple(of_point(p, root))}' in str(refused)]
        return [f'{refused}' + (f' ({", ".join(named)})' if named else '')]
    out = []
    for s, c in table.items():
        name = f'the shape {tuple(s)}'
        if c[SLICE] > SLICE_MOST_US:
            out.append(f'{name}: a slice of {c[SLICE]} us, over the ruling\'s {SLICE_MOST_US} us')
        if c[BUILD_ONE] > c[SLICE]:
            out.append(f'{name}: a build of one of {c[BUILD_ONE]} us, over its slice of {c[SLICE]} us')
        if c[SRP_UNIT] > c[SLICE]:
            out.append(f'{name}: an SRP record of {c[SRP_UNIT]} us, over its slice of {c[SLICE]} us')
        if c[BUILD] >= 2 * c[BUILD_ONE] and c[SLICE] < c[BUILD]:
            out.append(f'{name}: a build of both of {c[BUILD]} us, not under two builds of one of {c[BUILD_ONE]} us, '
                       'where its slice holds one build')
    for point in BUILT:
        s = of_point(point, root)
        if s not in table:
            out.append(f'{point}: the builder states the shape {tuple(s)}, which ctrl_loop.h does not list')
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import run
    if sorted(BUILT.values()) != sorted(run.POINTS.values()):
        out.append(f'the model\'s points are built at {sorted(BUILT.values())}, not at the harness\'s points\' '
                   f'{sorted(run.POINTS.values())} (run.py, POINTS)')
    shipping = of_config(root / DEFAULT_CONFIG, 1, root)
    if default != (shipping.sources, shipping.sinks):
        out.append(f'ctrl_loop.h takes {default} streams with no shape header, not the shipping configuration\'s '
                   f'{(shipping.sources, shipping.sinks)}')
    import poll_grade
    if set(poll_grade.STATED_US) != set(table):
        out.append(f'poll_grade.py states the polls at {sorted(map(tuple, poll_grade.STATED_US))}, not at the shapes '
                   f'ctrl_loop.h lists, {sorted(map(tuple, table))}')
    return out + notice_findings(root, texts) + key_findings(root) + retry_findings(root, texts)


def retry_findings(root: Path = ROOT, texts: dict[str, str] | None = None) -> list[str]:
    """THE RETRY's round costs keyed on the shape (#894's ruling issuecomment-6878014227, item 1): AECP_ROUND_COLD_US
    and AECP_ATTEMPT_US each defined once as the name the table states it by (RETRY), not a figure of its own nor a
    ternary on the interface count; and at each point, each evaluated as its header derives it there, the costs the
    table lists for that point's shape. A point whose cost falls back to the interface count's, or to one figure at
    every shape, is named with both figures."""
    out = []
    table = listed(text_of(root, texts))
    for name, (path, shaped) in RETRY.items():
        text = (texts or {}).get(path) or (root / path).read_text()
        found = re.findall(rf'^#define {name} (.+)$', text, re.M)
        body = found[0].split('//')[0].strip() if found else None
        where = path.rsplit('/', 1)[-1]
        if len(found) != 1 or body != shaped:
            how = (f'keys {name} on the interface count (MBX_N_IF)' if body and 'MBX_N_IF' in body else
                   f'states {name} as {body!r}' if body else f'does not define {name}')
            out.append(f'{where} {how}, not as {shaped}, which THE SHAPES state for each shape'
                       if len(found) <= 1 else f'{where} defines {name} {len(found)} times')
        for point in BUILT:
            s = of_point(point, root)
            if s not in table or not found:
                continue
            want = table[s][shaped]
            try:
                got = evaluated(text, name, {**table[s], 'MBX_N_IF': s.interfaces})
            except (KeyError, ValueError, SyntaxError):
                got = None
            if got != want:
                out.append(f'{point}: {name} is {got} us at its shape {tuple(s)}, not the {want} us THE SHAPES state '
                           f'for it ({shaped})')
    return out


def notice_findings(root: Path = ROOT, texts: dict[str, str] | None = None) -> list[str]:
    """AECP_NOTICES_MOST (aecp.h) at each point under the notices its descriptors hold, or at one interface not those
    exactly; with no shape header not the shipping configuration's; and a load point counting other descriptors with
    counters than the shape header states (load_grade.POINTS)."""
    import load_grade
    out = []
    for point, (config, n_if) in BUILT.items():
        path = root / 'configs' / f'{config}.yaml'
        most, held = notices_most(path, n_if, root, texts), notices_held(path, root)
        if most < held:
            out.append(f'{point}: AECP_NOTICES_MOST is {most}, under the {held} notices its descriptors hold')
        elif n_if == 1 and most != held:
            out.append(f'{point}: AECP_NOTICES_MOST is {most}, not the {held} notices its descriptors hold')
        counted = sum(descriptors(header_of(path, root)).values())
        if load_grade.POINTS[point]['counter_descriptors'] != counted:
            out.append(f'{point}: load_grade.py counts {load_grade.POINTS[point]["counter_descriptors"]} descriptors '
                       f'with counters, not the {counted} the shape header states')
    alone, shipping = evaluated(aecp_text(root, texts), 'AECP_NOTICES_HELD', {}, last=True), \
        notices_held(root / DEFAULT_CONFIG, root)
    if alone != shipping:
        out.append(f'aecp.h holds {alone} notices with no shape header, not the shipping configuration\'s {shipping}')
    return out


def report(root: Path = ROOT) -> list[str]:
    """Every listed shape's costs, and each point's shape."""
    table = listed(text_of(root))
    lines = ['| Shape (interfaces, sources, sinks) | Slice, us | Build of both, us | Build of one, us | SRP record, us '
             '| THE RETRY: cold start, us | refused attempt, us | Points |', '|---|---:|---:|---:|---:|---:|---:|---|']
    points = {p: of_point(p, root) for p in BUILT}
    for s, c in table.items():
        named = ', '.join(p for p, at_ in points.items() if at_ == s) or 'none the model names'
        lines.append(f'| {tuple(s)} | {c[SLICE]} | {c[BUILD]} | {c[BUILD_ONE]} | {c[SRP_UNIT]} | {c[RETRY_COLD]} '
                     f'| {c[RETRY_ATTEMPT]} | {named} |')
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
    block = ''.join(f'#define {name} {one[name]}u\n' for name in NAMES)
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
        'an SRP record over its slice': planted(block, block.replace(f'{SRP_UNIT} {one[SRP_UNIT]}u',
                                                                     f'{SRP_UNIT} {one[SLICE] + 5}u')),
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
    # the model's points built at another configuration than the harness's
    from unittest import mock
    with mock.patch.dict(BUILT, {next(iter(BUILT)): ('endstation_arty_4x4', 1)}):
        if not any('not at the harness' in f for f in findings(root)):
            escaped.append('a model point built at another configuration than the harness\'s')
    # a point whose shape is not listed
    point = next(iter(BUILT))
    s = of_point(point, root)
    head = f'CTRL_LOOP_SHAPE({s.interfaces}u, {s.sources}u, {s.sinks}u)'
    if not any(point in f for f in findings(root, planted(head, f'CTRL_LOOP_SHAPE({s.interfaces}u, 3u, 3u)'))):
        escaped.append('a point whose shape is not listed')
    # a listed shape whose polls poll_grade.py does not state: it would be graded at none
    import poll_grade
    with mock.patch.dict(poll_grade.STATED_US):
        del poll_grade.STATED_US[of_point('8x8/1if', root)]
        if not any('poll_grade.py states the polls' in f for f in findings(root)):
            escaped.append('a listed shape whose polls are not stated')
    return escaped + notice_controls(root) + key_controls(root) + retry_controls(root)


def retry_controls(root: Path = ROOT) -> list[str]:
    """Each planted defect of THE RETRY's keying retry_findings (or the table's rules) must refuse, each by the point
    whose cost falls back and in words that name it: the planted names that escaped."""
    escaped = []
    point = '8x8/1if'
    s = of_point(point, root)
    mine = listed(text_of(root))[s]
    for name, (path, shaped) in RETRY.items():
        if mine[shaped] == listed(text_of(root))[shape(s.interfaces, root)][shaped]:
            escaped.append(f'{point}\'s {name} not apart from the interface count\'s, so no plant can tell them')
    text = {path: (root / path).read_text() for path, _ in RETRY.values()}
    loop = text_of(root)
    block = ''.join(f'#define {name} {mine[name]}u\n' for name in NAMES)
    one, two = (listed(loop)[shape(n, root)][RETRY_COLD] for n in (1, 2))

    def planted(path: str, old: str, new: str) -> dict[str, str]:
        """One file with one substitution, refused if it does not apply once."""
        body = loop if path == HEADER else text[path]
        if body.count(old) != 1:
            raise AssertionError(f'control fixture {old!r} does not occur exactly once in {path}')
        return {path: body.replace(old, new)}
    cold, attempt = RETRY['AECP_ROUND_COLD_US'][0], RETRY['AECP_ATTEMPT_US'][0]
    plants = {
        'a round\'s cold start keyed on the interface count (earlier rule)': (planted(
            cold, f'#define AECP_ROUND_COLD_US {RETRY_COLD}\n',
            f'#define AECP_ROUND_COLD_US (MBX_N_IF == 1u ? {one}u : {two}u)\n'),
            f'{point}: AECP_ROUND_COLD_US is {one} us at its shape {tuple(s)}, not the {mine[RETRY_COLD]} us'),
        'a refused attempt one figure at every shape (earlier rule)': (planted(
            attempt, f'#define AECP_ATTEMPT_US {RETRY_ATTEMPT}\n', '#define AECP_ATTEMPT_US 34u\n'),
            f'{point}: AECP_ATTEMPT_US is 34 us at its shape {tuple(s)}, not the {mine[RETRY_ATTEMPT]} us'),
        'a shape\'s round costs falling back to the interface count': (planted(
            HEADER, block, block.replace(f'#define {RETRY_COLD} {mine[RETRY_COLD]}u\n',
                                         f'#define {RETRY_COLD} (MBX_N_IF == 1u ? {one}u : {two}u)\n')),
            f'for the shape {tuple(s)} ({point})'),
    }
    for name, (texts, words) in plants.items():
        if not any(words in f for f in findings(root, texts)):
            escaped.append(name)
    return escaped


def key_controls(root: Path = ROOT) -> list[str]:
    """Each planted defect of the key domain's single source key_findings must refuse: the planted names that
    escaped."""
    from unittest import mock
    escaped = []
    shape, aem = header_of, aecp_header_of
    eight = root / 'configs' / f'{BUILT["8x8/1if"][0]}.yaml'
    lines = re.compile(r'^#define AECP_ENTITY_KEY_\w+ \d+u\n', re.M)
    plants = {
        'the shape header not stating the map edits\' key domain': (
            {'header_of': lambda c, r=ROOT: lines.sub('', shape(c, r))},
            'the shape header does not state AECP_ENTITY_KEY_STREAMS'),
        'aecp_entity_gen.h stating the key domain beside the shape header': (
            {'aecp_header_of': lambda c, r=ROOT: aem(c, r).replace(KEY_GUARD + '\n', '', 1)},
            'outside #ifndef CTRL_SRP_ENTITY_H'),
        'the shape header\'s key domain not the image\'s': (
            {'header_of': lambda c, r=ROOT: shape(c, r).replace('#define AECP_ENTITY_KEY_STREAMS 9u',
                                                                '#define AECP_ENTITY_KEY_STREAMS 2u')
             if c == eight else shape(c, r)},
            '8x8/1if: the shape header states AECP_ENTITY_KEY_STREAMS 2, not the image\'s 9'),
    }
    for name, (patched, words) in plants.items():
        with mock.patch.dict(globals(), patched):
            if not any(words in f for f in key_findings(root)):
                escaped.append(name)
    return escaped


def notice_controls(root: Path = ROOT) -> list[str]:
    """Each planted defect of AECP_NOTICES_MOST's derivation notice_findings must refuse: the planted names that
    escaped."""
    text = aecp_text(root)
    escaped = []

    def planted(old: str, new: str) -> dict[str, str]:
        """aecp.h with one substitution, refused if it does not apply once."""
        if text.count(old) != 1:
            raise AssertionError(f'control fixture {old!r} does not occur exactly once in {AECP_HEADER}')
        return {AECP_HEADER: text.replace(old, new)}
    plants = {
        # the earlier rule: one interface's most typed at the 1x1's count, under the 8x8's 40 at 8x8/1if
        'the notices most typed at the 1x1\'s 12 at one interface (earlier rule)': (planted(
            '#define AECP_NOTICES_MOST (MBX_N_IF == 1u ? AECP_NOTICES_HELD : 40u)',
            '#define AECP_NOTICES_MOST (MBX_N_IF == 1u ? 12u : 40u)'), '8x8/1if: AECP_NOTICES_MOST is 12, under'),
        'an AVB interface\'s notices counted as two': (planted(
            '3u * CTRL_AEM_AVB_INTERFACES', '2u * CTRL_AEM_AVB_INTERFACES'), 'notices its descriptors hold'),
        'two interfaces\' most under the 8x8\'s descriptors': (planted(
            'AECP_NOTICES_HELD : 40u)', 'AECP_NOTICES_HELD : 12u)'), '8x8/2if: AECP_NOTICES_MOST is 12, under'),
        'the notices with no shape header not the shipping configuration\'s': (planted(
            '#define AECP_NOTICES_HELD (2u * AECP_NOTICE_STREAMS + 3u * 1u + 1u)',
            '#define AECP_NOTICES_HELD (2u * AECP_NOTICE_STREAMS + 3u * 1u)'), 'with no shape header'),
    }
    for name, (texts, words) in plants.items():
        if not any(words in f for f in notice_findings(root, texts)):
            escaped.append(name)
    import load_grade
    from unittest import mock
    with mock.patch.dict(load_grade.POINTS, {'8x8/1if': dict(load_grade.POINTS['8x8/1if'], counter_descriptors=18)}):
        if not any('8x8/1if: load_grade.py counts 18' in f for f in notice_findings(root)):
            escaped.append('a load point counting other descriptors with counters than the shape header states')
    return escaped


#: The planted defects controls() plants, in its order.
CONTROLS = ('a shape the table does not list', 'a slice over the cap', 'a build of one over its slice',
            'an SRP record over its slice', 'the table with no #error', 'a shape listed twice',
            'a cost missing from a shape',
            'the default streams not the shipping configuration\'s', 'a build of both at two builds of one',
            'the slice cap not the ruling\'s 1,600 us',
            'a model point built at another configuration than the harness\'s', 'a point whose shape is not listed',
            'a listed shape whose polls are not stated',
            'the notices most typed at the 1x1\'s 12 at one interface (earlier rule)',
            'an AVB interface\'s notices counted as two', 'two interfaces\' most under the 8x8\'s descriptors',
            'the notices with no shape header not the shipping configuration\'s',
            'a load point counting other descriptors with counters than the shape header states',
            'the shape header not stating the map edits\' key domain',
            'aecp_entity_gen.h stating the key domain beside the shape header',
            'the shape header\'s key domain not the image\'s',
            'a round\'s cold start keyed on the interface count (earlier rule)',
            'a refused attempt one figure at every shape (earlier rule)',
            'a shape\'s round costs falling back to the interface count')


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
