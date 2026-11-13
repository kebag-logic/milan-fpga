# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of THE RETRY's round costs (round_grade.py; #665, a stated cost is an upper bound): every
round held to AECP_ROUND_COLD_US + n x AECP_NOTICE_US + k x AECP_ATTEMPT_US at its point, n and k read off the calls
inside it, and a round over that failing the run whatever findings it records; and of THE TIERS' slices
(slice_grade.py, #894), each held to CTRL_LOOP_SLICE_US."""
from __future__ import annotations

import argparse
import re
from collections.abc import Callable

import build
import datapath_window
import grade
import round_grade
import run
import scenario
import slice_grade

Check = tuple[str, bool, str]
#: What the testbench prints for the round's span and the calls in it (build.py's SPAN and CALL tables).
ROUND, ATTEMPT, BUILT = 'ctrl_loop:round_of', 'aecp_command', 'aecp:finish'


def header_us(interfaces: int) -> dict[str, int]:
    """The round's costs as the headers state them, read here apart from round_grade.stated_us."""
    text = ''.join((scenario.ROOT / 'sw/firmware/ctrl/aecp' / name).read_text() for name in ('aecp.h', 'aecp_mbx.h'))
    macro = lambda name: re.search(rf'^#define {name} (.+)$', text, re.M).group(1)
    pick = lambda name: int(re.findall(r'(\d+)u', macro(name))[1 if interfaces == 1 else 2])
    return dict(cold=pick('AECP_ROUND_COLD_US'), notice=pick('AECP_NOTICE_US'),
                attempt=int(macro('AECP_ATTEMPT_US').rstrip('u')))


def round_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int) -> list[Check]:
    """A round at its stated cost fits it and one a cycle over does not, by notices built and attempts refused; then
    the slices' checks (slice_checks), a round being one of them, and the datapath events' (datapath_checks), whose
    sink cost the rows charge beside the rounds."""
    us = header_us(2)
    limit = lambda n, k: (us['cold'] + n * us['notice'] + k * us['attempt']) * cpu_hz // 1_000_000

    def held(cycles: int, built: int, refused: int, outside: int = 0, interfaces: int = 2) -> dict:
        """The grade of one round of those CPU cycles, its notices and refused attempts, and calls outside it."""
        start = 5000
        lines = [f'PASS 1 {2 * start - 100} {start - 50} {cycles + 100} instr=10 store_mbx=1 W {2 * start}:1:0',
                 f'SPAN {2 * start} {start} {cycles} 00001000 {ROUND}']
        calls = [BUILT] * built + [ATTEMPT] * (built + refused)
        lines += [f'CALL {2 * (start + 1 + n)} {start + 1 + n} {name}' for n, name in enumerate(calls)]
        lines += [f'CALL {2 * (start + cycles + 1 + n)} {start + cycles + 1 + n} {ATTEMPT}'
                  for n in range(outside)]
        lines += [f'CALL {2 * (start - 2 - n)} {start - 2 - n} {BUILT}' for n in range(outside)]
        return grade.grade(synthetic(lines), scenario.Group('g'), sys_hz, cpu_hz, interfaces)['passes']['rounds']

    got = round_grade.stated_us(1), round_grade.stated_us(2)
    out = [("each point's round costs are its headers' own, a notice to 16 recipients cheaper than one to 32",
            got == (header_us(1), us) and got[0]['notice'] < us['notice'], str(got)),
           ('the testbench traces the round and the calls that count its notices and attempts',
            ('ctrl_loop', 'round_of') in build.SPAN_SYMBOLS and {'aecp_command', ('aecp', 'finish')} <=
            set(build.CALL_SYMBOLS), '')]
    fits, misses = [], []
    for n, k in ((0, 0), (1, 0), (4, 0), (2, 3), (0, 6)):
        at, over = held(limit(n, k), n, k), held(limit(n, k) + 1, n, k)
        fits.append(at['over'] == [] and at['rounds'] == 1)
        misses.append([(o['notices'], o['refused']) for o in over['over']] == [(n, k)])
    out.append(('a round at its stated cost, by notices built and attempts refused, fits it and one a cycle over it '
                'does not', all(fits) and all(misses), str((fits, misses))))
    out.append(('calls outside a round count none of its notices or attempts',
                held(limit(0, 0), 0, 0, outside=3)['over'] == [] and held(limit(0, 0) + 1, 0, 0, outside=3)['over'],
                ''))
    one = held(limit(1, 0), 1, 0, interfaces=1)
    out.append(("a round at one interface is held to that point's costs",
                [o['cycles'] for o in one['over']] == [limit(1, 0)], str(one)))
    named = run.stated_misses([dict(group='g', passes=dict(rounds=held(limit(2, 3) + 1, 2, 3)))])
    out.append(('a round over its stated cost is named, with its notices, its refused attempts and the cost it passed',
                named == [f'g: a round of 2 notice(s) and 3 refused attempt(s), {limit(2, 3) + 1:,} CPU cycles, '
                          f'over its stated {limit(2, 3):,}'], str(named)))
    args = argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=True,
                              record_share_findings=True)
    out.append(('a round over its stated cost fails a run whatever findings it records',
                run.verdict(args, [scenario.Group('g')], [], [], [], named) == 1, ''))
    return out + slice_checks(synthetic, sys_hz, cpu_hz) + datapath_checks(synthetic, sys_hz, cpu_hz)


def slice_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int) -> list[Check]:
    """THE TIERS' slices (slice_grade.py; #665's decision of 2026-11-09, item 1): SRP's records from their pass's start,
    a pass given whole to a build with its round, and every other round, each at the stated length fitting it and a
    cycle over it refused, and a slice over it failing the run whatever findings it records."""
    header = (scenario.ROOT / 'sw/firmware/ctrl/loop/ctrl_loop.h').read_text()
    us = [int(n) for n in re.search(r'^#define CTRL_LOOP_SLICE_US \(MBX_N_IF == 1u \? (\d+)u : (\d+)u\)', header,
                                    re.M).groups()]
    limit = us[1] * cpu_hz // 1_000_000
    start = 5000

    def held(kind: str, cycles: int, interfaces: int = 2) -> dict:
        """The grade of one slice of that kind and CPU cycles, in a pass that starts at cpu cycle start."""
        lines = {'srp': [f'PASS 1 {2 * start} {start} {cycles + 300} instr=10 store_mbx=1 W {2 * start + 2}:1:0',
                         f'SPAN {2 * start + 20} {start + 10} {cycles - 110} 00001000 srp_mbx:receive',
                         f'SPAN {2 * start + 2 * cycles - 160} {start + cycles - 80} 80 00001000 srp_mbx:receive'],
                 'build': [f'PASS 1 {2 * start} {start} {cycles} instr=10 store_mbx=1 W {2 * start + 2}:1:0',
                           f'ENTRY {2 * start + 20} build_mrpdu',
                           f'SPAN {2 * start + 2 * cycles - 400} {start + cycles - 200} 150 00001000 {ROUND}'],
                 'round': [f'PASS 1 {2 * start - 100} {start - 50} {cycles + 100} instr=10 store_mbx=1 '
                           f'W {2 * start}:1:0', f'SPAN {2 * start} {start} {cycles} 00001000 {ROUND}']}[kind]
        return grade.grade(synthetic(lines), scenario.Group('g'), sys_hz, cpu_hz, interfaces)['passes']['slices']

    kinds = lambda s: [o['kind'] for o in s['over']]
    one = us[0] * cpu_hz // 1_000_000
    out = [("each point's slice is ctrl_loop.h's stated length at it, 800 us at 1x1/1if and 1,300 us at 8x8/2if",
            [slice_grade.stated_us(1), slice_grade.stated_us(2)] == us == [800, 1300], str(us)),
           ("a slice at one interface is held to that point's length",
            [o['kind'] for o in held('build', one + 1, 1)['over']] == ['build'] and not held('build', one, 1)['over'],
            ''),
           ("the testbench traces SRP's record handler and THE RETRY's round",
            {('srp_mbx', 'receive'), ('ctrl_loop', 'round_of')} <= set(build.SPAN_SYMBOLS), '')]
    for kind in ('srp', 'build', 'round'):
        at, over = held(kind, limit), held(kind, limit + 1)
        out.append((f"a slice of {run.SLICE_KINDS[kind]} at the stated length fits it and one a cycle over does not",
                    kinds(at) == [] and kinds(over) == [kind] and over['longest'][kind] == limit + 1
                    and at['slices'] == 1, str((at, over))))
    out.append(("SRP's slice runs from its pass's start, not from its first record",
                kinds(held('srp', limit + 1)) == ['srp'] and held('srp', limit + 1)['over'][0]['cycles'] == limit + 1,
                ''))
    out.append(("a round in a pass given whole to a build is that slice's, not one of its own",
                held('build', limit)['slices'] == 1, str(held('build', limit))))
    named = run.stated_misses([dict(group='g', passes=dict(slices=held('build', limit + 1)))])
    out.append(('a slice over the stated length is named, with what it held and the length it passed',
                named == [f"g: a tier-2 slice of THE TRANSMIT's build of {limit + 1:,} CPU cycles, over the stated "
                          f"slice {limit:,}"], str(named)))
    args = argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=True,
                              record_share_findings=True)
    out.append(('a slice over the stated length fails a run whatever findings it records',
                run.verdict(args, [scenario.Group('g')], [], [], [], named) == 1, ''))
    return out


def datapath_checks(synthetic: Callable[[list[str]], str], sys_hz: int, cpu_hz: int) -> list[Check]:
    """The datapath's change events (#894, datapath_window.py): the testbench's pulse lines graded, not refused, each a
    pad of its kind and interface, and the group posting each kind on every interface eight times."""
    lines = ['PASS 1 1000 500 100 instr=10 store_mbx=1 W 1001:1:0', 'DATAPATH 1100 avb 1', 'DATAPATH 1200 amap 0']
    try:
        log = grade.parse(synthetic(lines), sys_hz, cpu_hz)
        pads = [(k, i) for _, k, i in log.pads]
    except grade.Refusal as error:
        pads = [str(error)]
    p = scenario.Point('8x8', 'endstation_ax7101_8x8', 2, 1, 2, 8, 8)
    script = datapath_window.groups(p)[0].script()
    posted = {kind: script.count(f'datapath {kind} ') for kind in ('avb', 'asp', 'amap')}
    printed = 'std::printf("DATAPATH %llu %s %u\\n", ull(sys_), kinds[kind], i);' in \
        (scenario.ROOT / 'tb/verilator/ctrl_service_budget/sim_main.cpp').read_text()
    graded = printed and pads == [('DATAPATH-avb', 1), ('DATAPATH-amap', 0)]
    return [("a datapath change pulse's line, as the testbench prints it, is graded as a pad of its kind and "
             "interface, not refused", graded, str((printed, pads))),
            ('the datapath-events group posts each kind on every interface eight times',
             posted == {'avb': 16, 'asp': 16, 'amap': 16}, str(posted))]
