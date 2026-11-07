# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The budget grader's portable self-test (#665; the method of #397).

It needs Python and PyYAML (the mailbox contract) and nothing built. It
regrades the committed trace fixture.log, which the 'fixture' group
recorded on the test SoC, against oracle.json: every probe's row, its pass
bound and backlog, each loaded channel's service, the worst pass, the
composed maximum and the composed window's population. Synthetic traces
check each marker, the notification fan-out and its cost a recipient, the
owed responses, the records ahead of a served record, the clock
conversion, the pass bound, the deadlines and the composition; synthetic
windows check the composed maximum over the backlog rows, its lower bound,
the rows a run did not include, and the record results.json carries and
the table renders. The real scenario's composed windows are counted
against the defined loads restated here, its fan-out against the
firmware's registration capacity read here, and its controls against
their paths. The run's exit status, the regrade's refusal of an absent
log, the reuse attestation, the instruction cache's observers and XIP link
script, and the fetch L1 and arm the run builds, records and reuses run on
temporary files.
Then each rule is mutated in turn, and a named check must fail; a mutant of
a headline figure (the worst pass, the composed maximum, a pass bound)
fails on that figure.

Regenerate the fixture only through its generator, from a fresh 'fixture'
group run at 1x1 on the cacheless core it was recorded on (--fetch-l1 none):

    python3 -B tb/verilator/ctrl_service_budget/selftest.py --write-fixture RESULTS/fixture.log BUILD/build.json
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import types
from collections.abc import Callable, Iterator
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
import grade  # noqa: E402
import run  # noqa: E402
import scenario  # noqa: E402
import selftest_mutants  # noqa: E402

FIXTURE_LOG = HERE / 'fixture.log'
ORACLE = HERE / 'oracle.json'
SYS_HZ, CPU_HZ = 100_000_000, 50_000_000
PINNED = ('status', 'start_sys', 'end_sys', 'sys_cycles', 'cpu_cycles', 'ms', 'within_t_svc', 'within_ceiling',
          'pass_cycles', 'pass_mbx_accesses', 'passes', 'bound_cpu_cycles', 'bound_ms', 'bound_within_t_svc',
          'ring', 'ahead')
#: FR_NFR.md 3.4.1's ceilings, restated here on purpose: a changed table must fail.
CEILINGS = {'adp': 200.0, 'disc': 20.0, 'acmp': 20.0, 'aecp': 24.0, 'notify': 24.0, 'maap': 50.0, 'srp': 18.0}
#: Each composed row's defined load, restated here on purpose (README, Backlog rows): every
#: channel's records one instant admits (ADP, AECP, SRP at their bucket's burst; ACMP, MAAP at
#: their ring's room), the refill leg's ADP at the ring's room, fifteen GM changes and the
#: event row's LINK change. A changed contract, rule or stimulus must fail.
AT_ONCE = {'adp': 8, 'acmp': 12, 'aecp': 16, 'maap': 7, 'srp': 32, 'GM': 15}
DEFINED = {'backlog': {**AT_ONCE, 'LINK': 1}, 'backlog-adp': AT_ONCE, 'backlog-adp-refill': {**AT_ONCE, 'adp': 11},
           'backlog-owed': AT_ONCE, 'fixture': {'adp': 1, 'acmp': 1, 'aecp': 1, 'maap': 1, 'srp': 1, 'GM': 2}}
FIRMWARE_AECP_H = HERE.parents[2] / 'sw/firmware/ctrl/aecp/aecp.h'
AECP, ACMP, ADP = scenario.CH['aecp'], scenario.CH['acmp'], scenario.CH['adp']
CTL1, CTL3 = scenario.CTL1, 0x0A0B0C0D0E0F0003
Check = tuple[str, bool, str]


def fixture_group(oracle: dict) -> scenario.Group:
    """The 'fixture' group of the point the oracle pins."""
    return scenario.fixture_groups(scenario.Point(**oracle['point']))[0]


def regraded(oracle: dict, text: str | None = None) -> dict:
    """The committed trace (or a planted copy of it), graded now."""
    return grade.grade(text or FIXTURE_LOG.read_text(), fixture_group(oracle), SYS_HZ, CPU_HZ)


def headline(result: dict) -> dict:
    """The pass figures the oracle pins: the worst pass and the composed maximum."""
    passes = result['passes']
    composed = passes['composed'] or {}
    return dict(worst_cycles=passes['worst']['cycles'], worst_ms=passes['worst']['ms'],
                composed_cycles=composed.get('cycles'), composed_ms=composed.get('ms'),
                composed_passes=composed.get('passes'), population=composed.get('population'),
                serviced=composed.get('serviced'), unreleased=composed.get('unreleased'),
                idle_min=passes['idle_min'], idle_max=passes['idle_max'])


def synthetic(lines: list[str]) -> str:
    """A minimal log in the testbench's line format, completed."""
    return '\n'.join([*lines, 'SUMMARY passes=1', 'RESULT: PASS']) + '\n'


def one(log: str, probe: scenario.Probe) -> dict:
    """A synthetic log's single probe, graded."""
    group = scenario.Group('synthetic', probes=[probe])
    return grade.grade(log, group, SYS_HZ, CPU_HZ)['probes'][0]


def tx_record(ch: int, interface: int, frame: bytes, at: int, cycle: int) -> list[str]:
    """The ring writes of one TX record at word index at, then its TX_HEAD commit."""
    base, words = grade.TX_RING[ch]
    data = [len(frame) | interface << 16 | 2 << 28, 0]
    padded = frame + bytes(-len(frame) % 4)
    data += [int.from_bytes(padded[k:k + 4], 'little') for k in range(0, len(padded), 4)]
    writes = ' '.join(f'{cycle - len(data) - 1 + n}:{base + (at + n) % words:x}:{v:x}' for n, v in enumerate(data))
    head = at + len(data)
    return [f'PASS 1 {cycle - 100} {(cycle - 100) // 2} 50 instr=10 load_mbx=3 store_mbx={len(data) + 1} '
            f'W {writes} {cycle}:{scenario.ch_word(ch, "TX_HEAD"):x}:{head:x}', f'TXC {cycle} {ch} {head}']


def tx_sequence(ch: int, records: list[tuple[int, bytes, int]]) -> list[str]:
    """Consecutive TX records of one channel: (interface, frame, commit cycle) each."""
    lines, at = [], 0
    for interface, frame, cycle in records:
        lines += tx_record(ch, interface, frame, at, cycle)
        at += 2 + (len(frame) + 3) // 4
    return lines


def acmp_response(sequence: int, message: str = 'GET_RX_STATE_RESPONSE', status: int = 0) -> bytes:
    """An ACMP response frame with that sequence_id."""
    return scenario.f.acmp(scenario.f.ACMP[message], 0x020000000001,
                           scenario.f.Acmp(sequence=sequence, status=status))


def aem_response(controller: int, sequence: int, command: int = 0x0010, unsolicited: bool = False,
                 descriptor: tuple[int, int] = (0, 0)) -> bytes:
    """An AEM_RESPONSE (9.2.1.2) to controller; unsolicited sets the u bit (7.5.2)."""
    payload = scenario.f.be(descriptor[0], 2) + scenario.f.be(descriptor[1], 2) + bytes(4)
    frame = bytearray(scenario.f.aem_command(scenario.f.Aem(1, controller, 2, 3, sequence), command, payload))
    frame[15] = 1
    if unsolicited:
        frame[36] |= 0x80
    return bytes(frame)


def received(ch: int, tag: str, at: int = 1100) -> list[str]:
    """A 70-byte frame tagged tag whose receive commit lands 4 cycles after its last byte."""
    return [f'RXS {at} 0 70 {tag}', f'RXE {at + 69}', f'RXC {at + 73} {ch}']


def differences(got: dict, pinned: dict) -> str:
    """The fields that differ, each as got (pinned)."""
    return ', '.join(f'{k} {got.get(k)} (pinned {pinned.get(k)})' for k in pinned if got.get(k) != pinned.get(k))


def fixture_checks() -> list[Check]:
    """The committed trace against the oracle: digest, rows, pass figures, and a planted path."""
    oracle = json.loads(ORACLE.read_text())
    digest = hashlib.sha256(FIXTURE_LOG.read_bytes()).hexdigest()
    out = [('fixture digest', digest == oracle['fixture_sha256'], digest)]
    result = regraded(oracle)
    rows = {r['probe']: r for r in result['probes']}
    for name, pinned in oracle['rows'].items():
        got = {k: rows.get(name, {}).get(k) for k in PINNED}
        out.append((f'fixture row {name}', got == pinned, differences(got, pinned)))
    got = headline(result)
    out.append(('fixture passes: worst pass and composed maximum', got == oracle['passes'],
                differences(got, oracle['passes'])))
    # A planted over-budget path in the recorded trace: the BIND_RX response moved past T_svc.
    row = oracle['rows']['fixture.bind_rx.if0']
    late = row['start_sys'] + 1_000_001
    planted = re.sub(rf'^TXC {row["end_sys"]} ', f'TXC {late} ', FIXTURE_LOG.read_text(), count=1, flags=re.M)
    planted = re.sub(rf'\b{row["end_sys"]}:', f'{late}:', planted)
    hit = {r['probe']: r for r in regraded(oracle, planted)['probes']}['fixture.bind_rx.if0']
    caught = hit.get('status') == 'measured' and hit.get('within_t_svc') is False and hit.get('sys_cycles', 0) > 1e6
    out.append(('planted over-budget path is caught', caught, str({k: hit.get(k) for k in PINNED})))
    # A composed load with one channel left out (the MAAP record's commit deleted) is refused by name.
    window = re.findall(r'^MARK (\d+) composed(?:_end)?$', FIXTURE_LOG.read_text(), re.M)
    maap = scenario.CH['maap']
    dropped = [line for line in FIXTURE_LOG.read_text().splitlines()
               if not (line.startswith('RXC ') and line.endswith(f' {maap}')
                       and int(window[0]) <= int(line.split()[1]) <= int(window[1]))]
    try:
        regraded(oracle, '\n'.join(dropped) + '\n')
        refused = ''
    except grade.Refusal as error:
        refused = str(error)
    out.append(('a composed load missing one channel is refused', "'maap': 0" in refused, refused or 'accepted'))
    # The same window whose stimulus also declares no MAAP record: the defined load still wants one.
    group = fixture_group(oracle)
    group.load.pop('maap')
    out.append(('a window short of its defined load is refused although it declares it',
                "'maap': 0" in refusal(lambda: grade.grade('\n'.join(dropped) + '\n', group, SYS_HZ, CPU_HZ)), ''))
    # The unchanged window against a defined load one MAAP record smaller: one too many is refused.
    smaller = dict(grade.defined_load('fixture'), maap=0)
    with patch.object(grade, 'defined_load', lambda name: smaller):
        refused = refusal(lambda: regraded(oracle))
    out.append(('a composed window that committed more than its load is refused', "'maap': 1" in refused,
                refused or 'accepted'))
    # SRP's release inside the window deleted: the record is starved, by name, and fits nothing.
    tail = f':{scenario.ch_word(scenario.CH["srp"], "RX_TAIL"):x}:'
    starved_text = re.sub(r' (\d+)' + re.escape(tail) + r'[0-9a-f]+',
                          lambda m: '' if int(window[0]) <= int(m.group(1)) <= int(window[1]) else m.group(0),
                          FIXTURE_LOG.read_text())
    result = regraded(oracle, starved_text)
    rows = [r for r in result['probes'] if '.service.srp.' in r['probe']]
    window_row = result['passes']['composed']
    out.append(('a starved channel is reported by name, and its window reports its load unreleased',
                len(rows) == 2 and all(r['starved'] and r['status'] == 'measured' and r['within_t_svc'] is False
                                       and r['within_ceiling'] is False for r in rows)
                and window_row['serviced'] is False and window_row['unreleased'] == {'srp': 1},
                str((rows, window_row.get('unreleased')))))
    return out


def refusal(action: Callable[[], object]) -> str:
    """The grader's refusal of an action, or '' if it was accepted."""
    try:
        action()
    except grade.Refusal as error:
        return str(error)
    return ''


def marker_checks() -> list[Check]:
    """The start and end markers, the commit's frame, the clock conversion and the deadlines."""
    out = []
    g = grade.Grader(grade.Log(SYS_HZ, CPU_HZ))
    conversions = (g.cpu_cycles(1_000_000), g.cpu_cycles(3), g.ms(1_000_000), g.bus_cycles(500_000), g.cpu_ms(500_000))
    out.append(('clock conversion', conversions == (500_000, 2, 10.0, 1_000_000, 10.0), str(conversions)))
    out.append(('ceilings pinned', scenario.CEILING_MS == CEILINGS and scenario.T_SVC_MS == 10.0,
                f'{scenario.CEILING_MS} {scenario.T_SVC_MS}'))
    probe = scenario.Probe('s.cmd.if0', 'GET_RX_STATE', 'acmp', f'rxc:{ACMP}', [f'resp:{ACMP}:41'])
    frame_lines = ['MARK 1000 s.cmd.if0', *received(ACMP, 's.cmd.if0')]
    for delta, within, name in ((1_000_000, True, 'exact budget passes'), (1_000_001, False, 'one cycle over misses')):
        r = one(synthetic(frame_lines + tx_record(ACMP, 0, acmp_response(0x41), 0, 1173 + delta)), probe)
        out.append((name, r.get('within_t_svc') is within and r.get('sys_cycles') == delta, str(r)))
    # Tags: the probe's own frame, the second on the channel, starts the path.
    lines = ['MARK 1000 s.cmd.if0', *received(ACMP, '-'), *received(ACMP, 's.cmd.if0', 1200),
             *tx_record(ACMP, 0, acmp_response(0x41), 0, 5273)]
    out.append(('tagged start', one(synthetic(lines), probe).get('start_sys') == 1273, ''))
    # A refused frame leaves no commit: the commit after it is the next frame's, even within 64 cycles.
    lines = ['MARK 1000 s.cmd.if0', 'RXS 1000 0 60 -', 'RXE 1059', 'RXS 1060 0 60 s.cmd.if0', 'RXE 1119',
             f'RXC 1123 {ACMP}', *tx_record(ACMP, 0, acmp_response(0x41), 0, 5000)]
    r = one(synthetic(lines), probe)
    out.append(('a receive commit belongs to the frame it follows', r.get('start_sys') == 1123, str(r)))
    try:
        one(synthetic(['MARK 1000 s.cmd.if0', f'RXC 1123 {ACMP}']), probe)
        orphan = False
    except grade.Refusal:
        orphan = True
    out.append(('a receive commit that follows no frame is refused', orphan, ''))
    # Sequence and interface: an earlier response to another command, or on the other interface, is not the end.
    lines = frame_lines + tx_record(ACMP, 1, acmp_response(0x41), 0, 2000) + \
        tx_record(ACMP, 0, acmp_response(0x40), 20, 3000) + tx_record(ACMP, 0, acmp_response(0x41), 40, 4000)
    out.append(('sequence and interface', one(synthetic(lines), probe).get('end_sys') == 4000, ''))
    # The last required output ends the path.
    both = scenario.Probe('s.cmd.if0', 'BIND_RX', 'acmp', f'rxc:{ACMP}', [f'resp:{ACMP}:41', 'arm:1'])
    arm = f'PASS 2 5000 2500 50 instr=10 store_mbx=1 W 6000:{scenario.TMR_CMD_WORD:x}:{1 << 30 | 0x100 | 1:x}'
    r = one(synthetic(frame_lines + tx_record(ACMP, 0, acmp_response(0x41), 0, 2000) + [arm]), both)
    out.append(('last end decides', r.get('end_sys') == 6000, str(r)))
    # The expected response is checked: a BIND_RX answered with a failure status is refused.
    bind = scenario.Probe('s.cmd.if0', 'BIND_RX', 'acmp', f'rxc:{ACMP}', [f'resp:{ACMP}:41'],
                          expect='acmp_status:BIND_RX_RESPONSE:0')
    r = one(synthetic(frame_lines + tx_record(ACMP, 0, acmp_response(0x41, 'BIND_RX_RESPONSE', 1), 0, 2000)), bind)
    out.append(('the expected response is checked', r.get('status') == 'unexpected response', str(r)))
    out += timing_checks()
    return out


def timing_checks() -> list[Check]:
    """A timer path's origin, a function entry's start, the normative wait and the pass bound."""
    out = []
    timer = scenario.Probe('s.timer.if0', 'TMR_NO_RESP', 'acmp', 'deadline:1', ['arm:1'])
    lines = ['MARK 1000 s.timer.if0', 'MS 300000 3', 'EVW 300400 0 00000001', 'EVW 300401 1 00010007',
             'EVW 300402 2 00000003', 'EVW 300403 3 00000003',
             f'PASS 1 300500 150250 50 instr=10 store_mbx=1 W 310000:{scenario.TMR_CMD_WORD:x}:{1 << 30 | 1:x}']
    r = one(synthetic(lines), timer)
    out.append(('timer origin is the armed deadline', r.get('start_sys') == 300000 and r.get('sys_cycles') == 10000,
                str(r)))
    # A test-only entry starts at its own function's entry, and an ADPDU of its type ends it.
    shutdown = scenario.Probe('s.shutdown.if0', 'SHUTDOWN', 'adp', 'entry:adp_mbx_set_enable',
                              [f'adp:{ADP}:{scenario.f.ADP_DEPARTING}'], expect='adp_departing')
    departing = scenario.f.adp(scenario.f.ADP_DEPARTING, 1, 2, scenario.f.Adp(valid_time=0))
    lines = ['MARK 1000 s.shutdown.if0', 'ENTRY 4000 other_function', 'ENTRY 5000 adp_mbx_set_enable',
             *tx_record(ADP, 0, departing, 0, 6000)]
    r = one(synthetic(lines), shutdown)
    out.append(('an entry start is its own function\'s', r.get('start_sys') == 5000 and r.get('status') == 'measured',
                str(r)))
    # A normative wait W extends the bound to W + T_svc and the ceiling to W + ceiling (3.4.1), and nothing more.
    waited = scenario.Probe('s.cmd.if0', 'Domain', 'srp', f'rxc:{ACMP}', [f'resp:{ACMP}:41'], wait_ms=200.0)
    frame_lines = ['MARK 1000 s.cmd.if0', *received(ACMP, 's.cmd.if0')]
    for delta, within, ceiling, name in ((21_000_000, True, True, 'W + T_svc passes'),
                                         (21_000_001, False, True, 'W + T_svc + 1 misses, within W + ceiling'),
                                         (21_800_001, False, False, 'W + ceiling + 1 is over the ceiling')):
        r = one(synthetic(frame_lines + tx_record(ACMP, 0, acmp_response(0x41), 0, 1173 + delta)), waited)
        out.append((name, r.get('within_t_svc') is within and r.get('within_ceiling') is ceiling, str(r)))
    # The pass bound runs from the start of the pass running at the input (1000, for 1000 CPU
    # cycles) to the end of the taking pass (3000, 500 CPU cycles): 3000 bus cycles, 1500 CPU cycles.
    probe = scenario.Probe('s.cmd.if0', 'GET_RX_STATE', 'acmp', f'rxc:{ACMP}', [f'rxtail:{ACMP}'])
    tail = scenario.ch_word(ACMP, 'RX_TAIL')
    lines = ['PASS 1 1000 500 1000 instr=10 store_mbx=1 W 1500:1:0', 'MARK 1900 s.cmd.if0',
             'RXS 1900 0 60 s.cmd.if0', 'RXE 1959', f'RXC 1963 {ACMP}',
             f'PASS 2 3000 1500 500 instr=10 store_mbx=1 W 3500:{tail:x}:11']
    r = one(synthetic(lines), probe)
    out.append(('the pass bound runs from the running pass at the bus ratio',
                (r.get('bound_cpu_cycles'), r.get('bound_ms')) == (1500, 0.03), str(r)))
    return out


def notification(lines_after: list[tuple[int, bytes, int]], recipients: tuple = ((CTL1, 0), (CTL1, 1))) -> dict:
    """SET_NAME's probe over a solicited response and the notifications given as (interface, frame, cycle)."""
    probe = scenario.Probe('s.notify.if0', 'SET_NAME', 'notify', f'rxc:{AECP}',
                           [f'resp:{AECP}:41', f'notify:{AECP}:0010:0:0'], expect='aecp_response',
                           recipients=recipients)
    records = [(0, aem_response(0x0A0B0C0D0E0F0002, 0x41), 201173), *lines_after]
    records.sort(key=lambda record: record[2])
    lines = ['MARK 1000 s.notify.if0', *received(AECP, 's.notify.if0'), *tx_sequence(AECP, records)]
    return one(synthetic(lines), probe)


def notify_checks() -> list[Check]:
    """A notification fan-out ends at the last required recipient's commit (FR_NFR.md 3.4.1, 7.5.2)."""
    to = lambda ctl, seq=0, **kw: aem_response(ctl, seq, unsolicited=True, **kw)
    out = []
    r = notification([(0, to(CTL1), 401173), (1, to(CTL1, 1), 601173)])
    out.append(('two recipients across interfaces end at the last', r.get('end_sys') == 601173 and
                r.get('status') == 'measured', str(r)))
    r = notification([(0, to(CTL1), 401173), (1, to(CTL1, 1), 1401173)])
    out.append(('a late recipient misses T_svc', r.get('ms') == 14.0 and r.get('within_t_svc') is False, str(r)))
    r = notification([(0, to(CTL1), 401173)])
    out.append(('a missing recipient is refused', r.get('status') == 'no end', str(r)))
    r = notification([(0, to(CTL1), 401173), (0, to(CTL1, 1), 601173)])
    out.append(('a duplicate does not stand in for another recipient', r.get('status') == 'no end', str(r)))
    r = notification([(0, to(CTL1), 401173), (1, to(CTL1, 1), 601173), (0, to(CTL3, 2), 701173)])
    out.append(('a notification to a controller outside the set is refused',
                r.get('status') == 'unexpected response' and 'not a recipient' in r.get('reason', ''), str(r)))
    r = notification([(0, to(CTL1), 401173), (1, to(CTL1, 7, command=0x0029), 501173),
                      (1, to(CTL1, 8, descriptor=(0, 1)), 551173), (1, to(CTL1, 1), 901173)])
    out.append(('unrelated unsolicited responses do not end it', r.get('end_sys') == 901173, str(r)))
    # Three recipients, 400,000 bus cycles first to last: 200,000 CPU cycles over two gaps.
    r = notification([(0, to(CTL1), 401173), (1, to(CTL1, 1), 601173), (0, to(CTL3, 2), 801173)],
                     recipients=((CTL1, 0), (CTL1, 1), (CTL3, 0)))
    out.append(("a fan-out's cost a recipient is its first to last commit over the gaps between them",
                r.get('fanout') == dict(recipients=3, first_sys=401173, last_sys=801173,
                                        per_recipient_cpu_cycles=100_000), str(r.get('fanout'))))
    return out


def composition_checks() -> list[Check]:
    """The records ahead of an input, and the table's worst instance and counts per path."""
    out = []
    # Two ACMP records committed before the probe's, one of them released: one is ahead of it.
    probe = scenario.Probe('s.cmd.if0', 'GET_RX_STATE', 'acmp', f'rxc:{ACMP}', [f'resp:{ACMP}:41'])
    tail = scenario.ch_word(ACMP, 'RX_TAIL')
    lines = [*received(ACMP, '-', 100), *received(ACMP, '-', 300),
             f'PASS 1 400 200 50 instr=10 store_mbx=1 W 450:{tail:x}:14', 'MARK 1000 s.cmd.if0',
             *received(ACMP, 's.cmd.if0'), *tx_record(ACMP, 0, acmp_response(0x41), 0, 5000)]
    r = one(synthetic(lines), probe)
    out.append(('records ahead of an input', (r.get('ring'), r.get('ahead')) == ('acmp', 1), str(r)))
    # Two ACMP records of a composed window, released one a pass: the second committed before
    # the first's release has it ahead; committed after that release, it has none.
    got = []
    for second in (1300, 1600):
        lines = ['MARK 1000 composed', *received(ACMP, '-', 1100), *received(ACMP, '-', second),
                 f'PASS 1 1500 750 100 instr=10 store_mbx=1 W 1550:{tail:x}:14',
                 f'PASS 2 2000 1000 100 instr=10 store_mbx=1 W 2050:{tail:x}:28', 'MARK 100000 composed_end']
        with patch.object(grade, 'defined_load', lambda name: {'acmp': 2}):
            rows = grade.grade(synthetic(lines), scenario.Group('synthetic'), SYS_HZ, CPU_HZ)['probes']
        got.append([(r['probe'].split('.', 1)[1], r['ahead']) for r in rows])
    want = [[('service.acmp.first.if0', 0), ('service.acmp.last.if0', 1)],
            [('service.acmp.first.if0', 0), ('service.acmp.last.if0', 0)]]
    out.append(("a served record's records ahead are those not yet released at its commit", got == want,
                str(got)))
    row = lambda name, ms, within, group: dict(probe=name, row='r', status='measured', path=['p.x', 0], ms=ms,
                                               within_t_svc=within, group=group, bound_ms=ms, ring='acmp', ahead=0,
                                               within_ceiling=True)
    results = [dict(group='a', probes=[row('a.x.if0', 10.5, False, 'a')], timeouts=[]),
               dict(group='b', probes=[row('b.x.if0', 12.0, False, 'b'), row('b.y.if0', 11.0, False, 'b')],
                    timeouts=[])]
    results[1]['probes'][1]['path'] = ['p.y', 0]
    worst = {e['path']: e for e in run.paths(results)}
    out.append(('each path reports its worst instance', worst['p.x']['worst']['probe'] == 'b.x.if0'
                and worst['p.x']['instances'] == 2, str(worst)))
    tally = run.counts(results)
    out.append(('misses are counted per path and per probe instance',
                tally == dict(paths=2, path_misses=2, instances=3, instance_misses=3), str(tally)))
    # A record never released, whose time is a lower bound, is worse than any time measured.
    starved = dict(row('c.x.if0', 600.0, False, 'c'), starved=True)
    results = [dict(group='c', probes=[starved], timeouts=[]),
               dict(group='d', probes=[row('d.x.if0', 700.0, False, 'd')], timeouts=[])]
    worst = run.paths(results)[0]['worst']
    out.append(("a starved instance is its path's worst", worst['probe'] == 'c.x.if0'
                and run.verdict_word(worst).startswith('STARVED'), str(worst)))
    return out


def maximum_checks() -> list[Check]:
    """The composed maximum over synthetic backlog windows: its lower bound, the backlog rows a run
    did not include, and the record results.json carries and the table renders."""
    window = lambda group, cycles, done: dict(group=group, probes=[], timeouts=[], passes=dict(composed=dict(
        cycles=cycles, ms=cycles / 50_000, passes=3, window_ms=100.0, serviced=done, unreleased={} if done
        else {'srp': 32})))
    record = lambda top, group, unreleased, best, not_run=(): dict(
        cycles=top, ms=top / 50_000, group=group, windows=4 - len(not_run), rows=4, not_run=list(not_run),
        partial=bool(not_run), lower_bound=bool(unreleased), unreleased=list(unreleased),
        released=dict(cycles=best[0], ms=best[0] / 50_000, group=best[1]) if best else None)
    out = []
    # Every backlog window, the longest of them with SRP unreleased, so a lower bound; the released
    # windows' longest stands beside it, and the fixture's short window is no backlog row. Then
    # every window released, so no lower bound.
    full = [window('fixture', 9_000_000, True), window('backlog', 700_000, True),
            window('backlog-adp', 1_500_000, False), window('backlog-adp-refill', 1_200_000, False),
            window('backlog-owed', 600_000, True)]
    released = [window('backlog', 700_000, True), window('backlog-adp', 650_000, True),
                window('backlog-adp-refill', 680_000, True), window('backlog-owed', 600_000, True)]
    at_least = record(1_500_000, 'backlog-adp', ['backlog-adp', 'backlog-adp-refill'], (700_000, 'backlog'))
    got = [run.composed_maximum(full), run.composed_maximum(released)]
    out.append(('the composed maximum is the longest pass of every backlog window, a lower bound while one '
                'left its load unreleased', got == [at_least, record(700_000, 'backlog', [], (700_000, 'backlog'))],
                str(got)))
    # The longest window released its load and a shorter one did not: still a lower bound.
    shorter = [window('backlog', 1_800_000, True), window('backlog-adp', 1_500_000, False),
               window('backlog-adp-refill', 1_200_000, True), window('backlog-owed', 600_000, True)]
    got = run.composed_maximum(shorter)
    out.append(('the composed maximum is a lower bound while a window shorter than the longest left its load '
                'unreleased', got == record(1_800_000, 'backlog', ['backlog-adp'], (1_800_000, 'backlog')),
                str(got)))
    # The answering-ports arm's three backlog rows, without the refill row, and one row alone: each run
    # names the rows it did not include.
    three = [window('backlog', 740_260, True), window('backlog-adp', 645_058, True),
             window('backlog-owed', 582_392, True)]
    partial = record(740_260, 'backlog', [], (740_260, 'backlog'), ['backlog-adp-refill'])
    got = [run.composed_maximum(three), run.composed_maximum(three[:1])]
    want = [partial, record(740_260, 'backlog', [], (740_260, 'backlog'),
                            ['backlog-adp', 'backlog-adp-refill', 'backlog-owed'])]
    out.append(('a run without every backlog row names the rows not run, and its composed maximum is partial',
                got == want, str(got)))
    # results.json's record is the one the table renders: a lower bound over every window, a partial
    # figure, and both at once (an unreleased window run alone).
    both = record(1_500_000, 'backlog-adp', ['backlog-adp'], None, ['backlog', 'backlog-adp-refill', 'backlog-owed'])
    cases = ((full, at_least, 'Composed maximum over the 4 backlog windows: at least 1,500,000 CPU cycles '
              '(30.000 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).',
              '700,000 (14.000 ms), backlog.'),
             (three, partial, 'Composed maximum over 3 of 4 backlog windows, a partial figure (backlog-adp-refill '
              'not run): 740,260 CPU cycles (14.805 ms), backlog.', '740,260 (14.805 ms), backlog.'),
             (full[2:3], both, 'Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, '
              'backlog-adp-refill, backlog-owed not run): at least 1,500,000 CPU cycles (30.000 ms), backlog-adp, '
              'a lower bound (load unreleased in backlog-adp).', 'none.'))
    wrong = []
    for results, top, line, best in cases:
        saved = run.summary('1x1', '0' * 64, results, [], [])['composed_maximum']
        lines = [text for text in run.table(results, '1x1').splitlines()
                 if text.startswith(('Composed maximum', 'Over the windows'))]
        if saved != top or lines != [line, f'Over the windows that released their whole load only: {best}']:
            wrong.append(f'results.json {saved}; table {lines}')
    out.append(("results.json's composed maximum is the record the table renders, with its lower-bound and "
                'partial labels', not wrong, '; '.join(wrong)))
    return out


def window_checks() -> list[Check]:
    """The composed maximum and the worst pass wherever their pass falls, and the owed responses."""
    out = []
    # Three passes inside the window, the longest neither first nor last; the run's longest is its last.
    lines = ['MARK 1000 composed', *[f'PASS {n} {s} {s // 2} {c} instr=10 store_mbx=1 W {s + 100}:1:0' for n, (s, c)
                                     in enumerate(((2000, 100), (5000, 900), (20000, 300)), 1)],
             'MARK 100000 composed_end', 'PASS 4 200000 100000 5000 instr=10 store_mbx=1 W 200100:1:0']
    with patch.object(grade, 'defined_load', lambda name: {}):
        passes = grade.grade(synthetic(lines), scenario.Group('synthetic'), SYS_HZ, CPU_HZ)['passes']
    got = (passes['composed']['cycles'], passes['composed']['passes'], passes['worst']['cycles'])
    out.append(("the composed maximum is the window's longest pass, wherever it falls", got[:2] == (900, 3), str(got)))
    out.append(("the worst pass includes the run's last pass", got[2] == 5000, str(got)))
    # The run of idle passes the script's end flushes holds the pass it cut short: no idle pass.
    lines = ['PASS 1 1000 500 100 instr=10 store_mbx=1 W 1050:1:0', 'IDLE 3 1000 2000',
             'PASS 5 9000 4500 100 instr=10 store_mbx=1 W 9050:1:0', 'IDLE 2 50 3000']
    passes = grade.grade(synthetic(lines), scenario.Group('synthetic'), SYS_HZ, CPU_HZ)['passes']
    idle = (passes['idle_min'], passes['idle_max'])
    out.append(("the pass the script's end cuts is no idle pass", idle == (1000, 2000), str(idle)))
    # A response with two frames owed ahead of it: exactly those two, in order, before its own.
    probe = scenario.Probe('s.owed.if0', 'owed', 'acmp', f'rxc:{ACMP}', [f'resp:{ACMP}:41'], owed=(0x31, 0x32))
    cases = (((0x31, 0x32), 'measured'), ((0x31,), 'unexpected response'), ((0x31, 0x32, 0x33), 'unexpected response'),
             ((0x32, 0x31), 'unexpected response'))
    for ahead, status in cases:
        records = [(0, acmp_response(s), 2000 + 1000 * n) for n, s in enumerate((*ahead, 0x41))]
        r = one(synthetic(['MARK 1000 s.owed.if0', *received(ACMP, 's.owed.if0'), *tx_sequence(ACMP, records)]), probe)
        out.append((f'the responses owed ahead are checked: {[f"{s:x}" for s in ahead]}', r.get('status') == status,
                    str({k: r.get(k) for k in ('status', 'reason', 'owed_ahead')})))
    # A command the firmware may drop: never answered is a measured, unbounded finding; answered
    # is an ordinary path; and a probe that may not drop is refused without its response.
    lines = ['MARK 1000 s.cmd.if0', *received(ACMP, 's.cmd.if0')]
    got = []
    for drop, tail in ((True, []), (True, tx_record(ACMP, 0, acmp_response(0x41), 0, 5000)), (False, [])):
        probe = scenario.Probe('s.cmd.if0', 'behind', 'acmp', f'rxc:{ACMP}', [f'resp:{ACMP}:41'], may_drop=drop)
        r = one(synthetic(lines + tail), probe)
        got.append((r.get('status'), r.get('unanswered'), r.get('within_t_svc'), r.get('within_ceiling')))
    out.append(('a command never answered is reported, unbounded, where it may be dropped',
                got == [('measured', True, False, False), ('measured', None, True, True), ('no end', None, None, None)],
                str(got)))
    return out


def channel_of(frame: bytes) -> str:
    """The receive channel a stimulus frame is for, from its EtherType and AVTP subtype."""
    ethertype = int.from_bytes(frame[12:14], 'big')
    if ethertype in (scenario.f.ETH_MSRP, scenario.f.ETH_MVRP):
        return 'srp'
    if ethertype != scenario.f.ETH_AVTP:
        return '-'
    return {0xFA: 'adp', 0xFB: 'aecp', 0xFC: 'acmp', 0xFE: 'maap'}[frame[14]]


def stimulus(group: scenario.Group) -> dict[str, int]:
    """What the group's script sends inside its composed window: records per channel, GM and LINK events."""
    out: dict[str, int] = {}
    inside = False
    names = [ch.name for ch in scenario.CONTRACT.channels]
    for step in group.steps:
        words = step.split()
        inside = {'mark composed': True, 'mark composed_end': False}.get(step, inside)
        if not inside or words[0] not in ('frame', 'reply', 'gm', 'link'):
            continue
        name = (channel_of(bytes.fromhex(words[2])) if words[0] == 'frame' else names[int(words[2])]
                if words[0] == 'reply' else words[0].upper())
        out[name] = out.get(name, 0) + 1
    return out


def points(oracle: dict) -> list[scenario.Point]:
    """The oracle's one-interface point and the same entity with two interfaces."""
    one_if = scenario.Point(**oracle['point'])
    return [one_if, scenario.Point(**dict(oracle['point'], interfaces=2))]


def load_checks() -> list[Check]:
    """Every composed window of the real scenario against its defined load, restated here."""
    oracle = json.loads(ORACLE.read_text())
    out = []
    derived = {name: {k: v for k, v in grade.defined_load(name).items() if v} for name in DEFINED}
    out.append(('the defined loads, restated', derived == DEFINED, str(derived)))
    sent, declared = {}, {}
    for p in points(oracle):
        for g in [*scenario.backlog_groups(p), *(scenario.fixture_groups(p) if p.interfaces == 1 else [])]:
            sent[f'{g.name}@{p.interfaces}'] = stimulus(g)
            declared[f'{g.name}@{p.interfaces}'] = {k: v for k, v in g.load.items() if v}
    want = {key: DEFINED[key.split('@')[0]] for key in sent}
    out.append(("every composed window's stimulus is its defined load", sent == want,
                ', '.join(f'{k} {v} (defined {want[k]})' for k, v in sent.items() if v != want[k])))
    out.append(('every composed window declares its defined load', declared == want,
                ', '.join(f'{k} {v} (defined {want[k]})' for k, v in declared.items() if v != want[k])))
    owed = [pr for g in scenario.backlog_groups(points(oracle)[0]) for pr in g.probes if pr.owed]
    out.append(('the owed row has seven responses owed ahead of its own',
                [(pr.owed, pr.ends) for pr in owed] == [(tuple(range(0x7380, 0x7387)), [f'resp:{ACMP}:7387'])],
                str([(pr.name, pr.owed, pr.ends) for pr in owed])))
    behind = [pr for g in scenario.backlog_groups(points(oracle)[0]) for pr in g.probes if pr.may_drop]
    out.append(('every command behind the owed input is a path that reports a drop',
                [pr.ends for pr in behind] == [[f'resp:{ACMP}:{0x7390 + n:x}'] for n in range(4)],
                str([(pr.name, pr.ends) for pr in behind])))
    return out


def path_checks() -> list[Check]:
    """A control is another instance of its functional path, counted once, at its worst."""
    oracle = json.loads(ORACLE.read_text())
    out, strays = [], []
    for p in points(oracle):
        groups = [*scenario.adp_groups(p), *scenario.control_groups(p), *scenario.shutdown_groups(p)]
        functional = {pr.path_key() for g in groups if not g.name.startswith('control') for pr in g.probes}
        strays += [pr.name for g in groups if g.name.startswith('control') for pr in g.probes
                   if pr.path_key() not in functional]
    out.append(("a control instance is its functional path", not strays, str(strays)))
    # The two-interface SHUTDOWN arm: two paths, three instances; the control's miss is if0's worst.
    times = {'adp.shutdown.if0': 0.58, 'adp.shutdown.if1': 1.17, 'control.shutdown.if0': 24.9}
    results = [dict(group=g.name, timeouts=[], probes=[
        dict(probe=pr.name, row=pr.row, status='measured', path=list(pr.path_key()), ms=times[pr.name],
             within_t_svc=times[pr.name] <= 10, within_ceiling=True, ring='events', ahead=0)
        for pr in g.probes]) for g in scenario.shutdown_groups(points(oracle)[1])]
    worst = {(e['path'], e['interface']): e['worst']['probe'] for e in run.paths(results)}
    tally = run.counts(results)
    out.append(('repeated instances of one path: one path, its worst instance, every miss',
                tally == dict(paths=2, path_misses=1, instances=3, instance_misses=1)
                and worst[('adp.shutdown', 0)] == 'control.shutdown.if0', str((tally, worst))))
    return out


def image_header(tmp: Path) -> Path:
    """A minimal generated AEM header: an AUDIO_UNIT at 48 kHz, a CLOCK_DOMAIN of three sources
    and a two-row map on each STREAM_PORT 0, in aecp_entity_gen.h's layout; returns the ELF path."""
    be = scenario.f.be
    audio = bytearray(152)
    audio[0:2], audio[136:148] = be(2, 2), be(48000, 4) + be(144, 2) + be(1, 2) + be(48000, 4)
    domain = bytearray(88)
    domain[0:2], domain[72:82] = be(36, 2), be(76, 2) + be(3, 2) + be(0, 2) + be(1, 2) + be(2, 2)
    entries = (be(0, 2) + be(2, 2) + be(1, 2) + be(148, 2) + be(64, 4) + be(0xFFFF, 2) + be(152, 2)
               + be(0, 2) + be(36, 2) + be(1, 2) + be(82, 2) + be(216, 4) + be(0xFFFF, 2) + be(88, 2))
    image = bytes(8) + be(2, 2) + bytes(2) + be(32, 4) + bytes(16) + entries + audio + domain
    (tmp / 'aecp_entity_gen.h').write_text(
        '#define AECP_ENTITY_MAPS_INIT(rows) { \\\n\t{14,0,0,8,(rows)+0,0,8,aecp_map_defaults+0,2}, \\\n'
        '\t{15,0,0,176,(rows)+8,0,17,aecp_map_defaults+2,2}, \\\n}\n'
        'static const struct aecp_mapping aecp_map_defaults[] = {\n\t{0,0,0,0},\n\t{0,7,7,0},\n\t{0,0,0,0},\n'
        '\t{0,7,7,0},\n};\nstatic const unsigned char aecp_entity_image[] = {\n\t'
        + ','.join(f'0x{b:02x}' for b in image) + ',\n};\n')
    return tmp / 'ctrl_app.elf'


def fanout_checks() -> list[Check]:
    """The fan-out group registers the firmware's whole capacity on every interface, and each of
    its notifications is required of every registration, from a requester outside them."""
    oracle = json.loads(ORACLE.read_text())
    capacity = int(re.search(r'#define AECP_REGISTRATIONS (\d+)u', FIRMWARE_AECP_H.read_text()).group(1))
    wrong = []
    with tempfile.TemporaryDirectory() as tmp:
        elf = image_header(Path(tmp))
        for p in points(oracle):
            for variant in ('none', 'answering-ports'):
                g = scenario.aecp_fanout_groups(p, dict(elf=str(elf), variant=variant))[0]
                registered, requesters, mark = set(), {}, ''
                for step in g.steps:
                    words = step.split()
                    if words[0] == 'mark':
                        mark = words[1]
                    if words[0] != 'frame':
                        continue
                    frame = bytes.fromhex(words[2])
                    if frame[14] == 0xFB and int.from_bytes(frame[36:38], 'big') & 0x7FFF == 0x0024:
                        registered.add((int.from_bytes(frame[26:34], 'big'), int(words[1])))
                    elif mark:
                        requesters[mark] = int.from_bytes(frame[26:34], 'big') if frame[14] == 0xFB else None
                per_if = [sum(1 for _, i in registered if i == k) for k in range(p.interfaces)]
                notify = [pr for pr in g.probes if pr.family == 'notify']
                if per_if != [capacity] * p.interfaces or not notify:
                    wrong.append(f'{p.interfaces} interfaces, {variant}: {per_if} registered, {len(notify)} fan-outs')
                wrong += [f'{pr.name}: {len(pr.recipients)} recipients of {len(registered)}' for pr in notify
                          if set(pr.recipients) != registered or len(pr.recipients) != len(registered)]
                wrong += [f'{name}: requester {ctl:016x} is registered' for name, ctl in requesters.items()
                          if ctl is not None and ctl in {c for c, _ in registered}]
    out = [("the fan-out group registers the firmware's capacity, every registration a recipient", not wrong,
            '; '.join(wrong) + f' (capacity {capacity})')]
    return out


def run_checks() -> list[Check]:
    """The run's exit status, the regrade's refusal of an absent log or script, and a trap's refusal."""
    out = []
    args = lambda record: argparse.Namespace(cpu_regions='cover', mutation='none', record_budget_findings=record)
    g = scenario.Group('g')
    out.append(('a T_svc miss fails the run unless recorded',
                (run.verdict(args(False), [g], [], ['m']), run.verdict(args(True), [g], [], ['m'])) == (1, 0), ''))
    out.append(('a refusal fails the run, recorded or not',
                (run.verdict(args(True), [g], ['r'], []), run.verdict(args(False), [g], ['r'], [])) == (1, 1), ''))
    out.append(('a clean run passes; a run of no group fails',
                (run.verdict(args(False), [g], [], []), run.verdict(args(True), [], [], [])) == (0, 1), ''))
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        groups = [scenario.Group(name, steps=['wait cycles 1']) for name in ('kept', 'nolog', 'noscript', 'stale')]
        for g in groups:
            if g.name != 'noscript':
                (out_dir / f'{g.name}.txt').write_text(g.script() if g.name != 'stale' else 'end\n')
            if g.name != 'nolog':
                (out_dir / f'{g.name}.log').write_text('RESULT: PASS\n')
        kept, _, refusals = run.recorded(groups, out_dir)
        named = sorted(r.split(':')[0] for r in refusals)
        out.append(('a regrade refuses each absent log or script, and a stale script, by name',
                    [g.name for g in kept] == ['kept'] and named == ['nolog', 'noscript', 'stale'], str(refusals)))
    try:
        grade.grade(synthetic(['TRAP 100 0 1 00006880']), scenario.Group('t'), SYS_HZ, CPU_HZ)
        trapped = ''
    except grade.Refusal as error:
        trapped = str(error)
    out.append(('a CPU trap is refused', 'trapped' in trapped, trapped))
    out += as_built_checks()
    return out


def as_built_checks() -> list[Check]:
    """The as-built control (#791) is caught by an instruction or a load access fault, and by
    nothing else: a clean boot and a trap of any other cause are refused."""
    boot = scenario.boot_fault_groups()[0]
    as_built = argparse.Namespace(cpu_regions='as-built', mutation='none', record_budget_findings=False)

    def control(traps: list[str]) -> int:
        """The control's exit status on a boot-fault log with these trap lines."""
        try:
            grade.grade(synthetic(traps), boot, SYS_HZ, CPU_HZ)
            refusals = []
        except grade.Refusal as error:
            refusals = [str(error)]
        with contextlib.redirect_stdout(io.StringIO()):
            return run.verdict(as_built, [boot], refusals, [])
    caught = {cause: control([f'TRAP 330592 0 {cause} 00006880']) for cause in (1, 5)}
    others = {line: control([line] if line else []) for line in
              ('', 'TRAP 166 0 2 00000024', 'TRAP 166 0 7 00000020', 'TRAP 166 0 15 00000020',
               'TRAP 166 1 5 00000020', 'BUSERR 166 load 00000020')}
    return [('the as-built control is caught by an instruction access fault (cause 1) and by a load access '
             'fault (cause 5)', caught == {1: 0, 5: 0}, str(caught)),
            ('the as-built control escapes on a clean boot and on a trap of any other cause',
             set(others.values()) == {1}, str(others))]


def reuse_checks() -> list[Check]:
    """A reused build is refused when any recorded input changed, is missing, was never
    recorded or does not resolve; an unchanged one is reused."""
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        bdir, external, tree = root / 'build', root / 'litex' / 'netlist.v', root / 'firmware'
        files = {'image/ctrl_app.elf': b'elf', 'gateware/sim_rom_bank0.init': b'00000013\n', 'gateware/sim.v': b'v',
                 'runtime/libc.a': b'a', 'native/Vsim': b'model', 'budget_config.hpp': b'h',
                 **{f'split-soc/flash-map/{name}': b'map' for name in build.FLASH_MAP_FILES}}
        for name, data in {**files, '../litex/netlist.v': b'cpu', '../firmware/adp.c': b'c'}.items():
            (bdir / name).parent.mkdir(parents=True, exist_ok=True)
            (bdir / name).write_bytes(data)
        spec = dict(elf=str(bdir / 'image/ctrl_app.elf'), sources=[str(bdir / 'gateware/sim.v'), str(external)],
                    flash_map=str(bdir / 'split-soc/flash-map'),
                    shape='endstation_ax7101_1x1_tdm8', executable_sha256=hashlib.sha256(b'model').hexdigest())

        def attempt(edit: Callable[[], None]) -> str:
            """Record the build, apply one edit, and try to reuse it: '' when reused, else the refusal."""
            with patch.object(build, 'FIRMWARE_TREES', (str(tree),)):
                spec['inputs'] = build.digest(build.run_inputs(bdir, spec), bdir)
                spec['inputs']['tree:firmware'] = build.tree_digest([build.ROOT / t for t in build.FIRMWARE_TREES])
                spec['inputs']['tree:config'] = build.tree_digest([build.ROOT / 'configs' / (spec['shape'] + '.yaml')])
                (bdir / 'build.json').write_text(json.dumps(spec))
                saved = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
                edit()
                try:
                    build.reused(bdir)
                    return ''
                except RuntimeError as error:
                    return str(error)
                finally:
                    for p in root.rglob('*'):
                        if p.is_file() and p not in saved:
                            p.unlink()
                    for p, data in saved.items():
                        p.write_bytes(data)

        out.append(('an unchanged build is reused', attempt(lambda: None) == '', attempt(lambda: None)))
        for name, edit, word in (
                ('the image', lambda: (bdir / 'image/ctrl_app.elf').write_bytes(b'elf2'), 'changed'),
                ('a ROM file', lambda: (bdir / 'gateware/sim_rom_bank0.init').write_bytes(b'0000006f\n'), 'changed'),
                ("the flash port's map", lambda: (bdir / 'split-soc/flash-map/flash_port.json').write_bytes(b'map2'),
                 'changed'),
                ('the SoC Verilog', lambda: (bdir / 'gateware/sim.v').write_bytes(b'v2'), 'changed'),
                ('the CPU netlist', lambda: external.write_bytes(b'cpu2'), 'changed'),
                ('a firmware source', lambda: (tree / 'adp.c').write_bytes(b'c2'), 'changed'),
                ('a deleted ROM file', lambda: (bdir / 'gateware/sim_rom_bank0.init').unlink(), 'missing'),
                ('an unrecorded ROM file', lambda: (bdir / 'gateware/sim_rom_bank1.init').write_bytes(b'0'),
                 'never recorded'),
                ('the native model', lambda: (bdir / 'native/Vsim').write_bytes(b'model2'), 'native model'),
                ('a key that does not resolve', lambda: (bdir / 'build.json').write_text(json.dumps(
                    dict(spec, inputs={**spec['inputs'], 'ctrl_app.elf': '0' * 64}))), 'does not resolve')):
            refused = attempt(edit)
            out.append((f'reuse refuses {name}', word in refused, refused or 'reused'))
    return out


def build_checks() -> list[Check]:
    """The ledgered point is named at its own point only, and every labelled arm and control plant
    applies to the checkout's sources (each a scratch copy, never the tree)."""
    sys.path.insert(0, str(HERE.parents[2] / 'sw/litex'))
    import ctrl_memory
    named = {label: build.ledgered_point(*run.POINTS[label]) for label in sorted(run.POINTS)}
    others = {(shape, n): build.ledgered_point(shape, n) for shape, _ in run.POINTS.values() for n in (1, 2)
              if (shape, n) not in run.POINTS.values()}
    out = [('the ledgered point is named at 8x8 with two interfaces only, as the planner ledgers it',
            named == {'1x1': None, '8x8': '8x8-two-interfaces'} and named['8x8'] in ctrl_memory.LEDGERED
            and not any(others.values()), f'{named}; other points {others}')]
    with tempfile.TemporaryDirectory() as tmp:
        failed = []
        for name, apply in [*[(v, build.variant_fixture) for v in build.VARIANTS],
                            *[(m, build.mutated_source) for m in build.MUTATIONS]]:
            try:
                apply(Path(tmp) / name, name)
            except RuntimeError as error:
                failed.append(str(error))
        out.append(("every labelled arm and control plant applies to the checkout's sources", not failed,
                    '; '.join(failed)))
    return out


def cache_checks() -> list[Check]:
    """The instruction cache's build (#665): the fetch observers follow the CPU's fetch plugin, a
    refill's beats come from the netlist, and the XIP arm keeps the reset entry and the flash
    driver in rom."""
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        netlist = Path(tmp) / 'VexiiRiscvLitex_x.v'
        cached = dict(fetch_l1_geometry=[64, 1], netlist=netlist.stem, sources=[str(netlist)])
        netlist.write_text("assign FetchL1Plugin_logic_bus_cmd_payload_address = "
                           "{FetchL1Plugin_logic_refill_slots_0_address[31 : 6],6'h0};\n")
        rows, beats = build.fetch_bus(cached)
        plain_rows, plain_beats = build.fetch_bus(dict(fetch_l1_geometry=None))
        names = {name for name, *_ in rows}
        out.append(('the fetch observers follow the CPU\'s fetch plugin',
                    all('FetchL1Plugin' in v for n, _, _, v in rows if n.startswith('fetch_'))
                    and not names & {'fetch_cmd_id', 'fetch_rsp_id'} and plain_rows == list(build.ACCESSORS),
                    str(rows)))
        out.append(('a refill\'s beats are read off the netlist', (beats, plain_beats) == (16, 1),
                    str((beats, plain_beats))))
        netlist.write_text('assign FetchL1Plugin_logic_bus_cmd_payload_address = 32\'h0;\n')
        try:
            build.fetch_bus(cached)
            refused = ''
        except RuntimeError as error:
            refused = str(error)
        out.append(('a cached netlist without its line-aligned refill address is refused', 'refill' in refused,
                    refused or 'accepted'))
    script = build.xip_script((build.ROOT / 'sw/firmware/ctrl/plat/ctrl_split.ld').read_text(), 0x20410000,
                              0x21000000)
    out.append(('the XIP arm keeps the reset entry and the flash driver in rom and moves the other code to flash',
                '\t.entry : { KEEP(*(.text.start)) *-nvm_flash_litespi.o(.text .text.*) } > rom\n' in script
                and '\t.text : ALIGN(4) { *(.text .text.*) } > flash\n' in script
                and 'MEMORY { flash (rx) : ORIGIN = 0x20410000, LENGTH = 0xbf0000 }' in script, script[:400]))
    return out


class Reached(Exception):
    """run.main got past its build or its reuse refusal and began to set up its groups."""


def write(path: Path, data: bytes) -> Path:
    """One temporary build file, written; returns its path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def main_verdict(bdir: Path, *flags: str) -> str:
    """run.main at 1x1 on bdir with the flags: 'reached' once it sets up its groups, else how it
    exited and its last line."""
    def reached(*a: object) -> None:
        """scenario.point in the run's place: the run got this far, so stop it here."""
        raise Reached
    said = io.StringIO()
    argv = ['run.py', '--point', '1x1', '--build-dir', str(bdir), *flags]
    with patch.object(sys, 'argv', argv), patch.dict(os.environ), patch.object(scenario, 'point', reached), \
            contextlib.redirect_stdout(said), contextlib.redirect_stderr(said):
        try:
            status = f'returned {run.main()}'
        except Reached:
            return 'reached'
        except SystemExit as error:
            status = f'exit {error.code}'
    last = said.getvalue().strip().rpartition('\n')[2]
    return f'{status}: {last}'


def built(bdir: Path, *flags: str) -> tuple[str, dict]:
    """run.main building bdir with the flags, build.build's toolchain steps replaced: its verdict
    and the build.json it wrote.

    The image, the XIP relink, the symbols and the native model are placeholder
    files, the SoC export records the selection it is handed, as
    split_soc.build records it in soc.json, and the ledgered plan patches
    nothing. The run's selection, the mailbox contract, the input digests and
    build.json are run.main's and build.build's own.
    """
    soc = types.ModuleType('split_soc')
    soc.FLASH_MAP = Path('split-soc/flash-map')
    soc.fixture_addresses = lambda flash_map: {'flash': 0x01000000}
    soc.build = lambda build_dir, shape, elf, n_if, cpu_regions, fetch_l1: dict(
        sources=[], shape=shape, interfaces=n_if, cpu_regions=cpu_regions, fetch_l1=fetch_l1)
    soc.ledgered_plan = lambda name: contextlib.nullcontext()
    stubs = dict(
        flash_map=lambda generated, shape: [write(generated / name, b'map') for name in build.FLASH_MAP_FILES]
        and generated,
        firmware=lambda out, *a: write(out / 'image/ctrl_app.elf', b'elf'),
        xip_image=lambda out, elf, window: (write(out / 'xip/ctrl_app.elf', b'xip'),
                                            write(out / 'xip/ctrl_app_rom.elf', b'rom'),
                                            write(out / 'flash.bin', b'code')),
        symbols=lambda elf: dict.fromkeys(('ctrl_loop_service', 'main', *build.ENTRY_SYMBOLS), 0),
        verilate=lambda out, *a: (write(out / 'native/Vsim', b'model'), write(out / 'budget_config.hpp', b'h')))
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.dict(sys.modules, split_soc=soc))
        stack.enter_context(patch.object(sys, 'path', list(sys.path)))
        for name, stub in stubs.items():
            stack.enter_context(patch.object(build, name, stub))
        verdict = main_verdict(bdir, *flags)
    record = bdir / 'build.json'
    return verdict, json.loads(record.read_text()) if record.is_file() else {}


def cache_build_checks() -> list[Check]:
    """The instruction cache's build identity (#665), on temporary files: the run builds and records
    the fetch L1 and the arm it selected, and it refuses a reused build of another, reuses the
    selected one, and takes a build that records no fetch L1 as the cacheless one."""
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        write(root / 'firmware/adp.c', b'c')
        with patch.object(build, 'FIRMWARE_TREES', (str(root / 'firmware'),)):
            selections = {'xip': ('64x1', True), 'plain': ('none', False)}
            runs = {name: built(root / name, '--fetch-l1', fetch_l1, *(['--xip'] if xip else []))
                    for name, (fetch_l1, xip) in selections.items()}
            recorded = {name: (verdict, (spec.get('fetch_l1'), spec.get('xip')))
                        for name, (verdict, spec) in runs.items()}
            out.append(('the run builds and records the fetch L1 and the arm it selected',
                        recorded == {name: ('reached', selection) for name, selection in selections.items()},
                        str(recorded)))
            cases = [('xip', ('--fetch-l1', '64x1', '--xip'), True), ('xip', ('--xip',), False),
                     ('xip', ('--fetch-l1', '64x1'), False), ('plain', ('--fetch-l1', 'none'), True),
                     ('plain', (), False), ('plain', ('--fetch-l1', 'none', '--xip'), False)]
            got = [main_verdict(root / name, '--reuse-build', *flags) for name, flags, _ in cases]
            # A build made before the cache records neither key; build.json is no attested input.
            (root / 'plain/build.json').write_text(json.dumps(
                {k: v for k, v in runs['plain'][1].items() if k not in ('fetch_l1', 'xip')}))
            cases += [('no fetch L1 recorded', ('--fetch-l1', 'none'), True), ('no fetch L1 recorded', (), False)]
            got += [main_verdict(root / 'plain', '--reuse-build', *flags) for _, flags, _ in cases[-2:]]
    refused = lambda verdict: verdict.startswith('exit 2:') and 'fetch L1 or arm' in verdict
    wrong = [f'{name} {" ".join(flags) or "(split)"}: {verdict}' for (name, flags, reuse), verdict in zip(cases, got)
             if not (verdict == 'reached' if reuse else refused(verdict))]
    out.append(('the run refuses a reused build of another fetch L1 or arm and reuses the selected one; '
                'a build with no fetch L1 is cacheless', not wrong, '; '.join(wrong)))
    return out


def checks() -> list[Check]:
    """Every named check and whether it holds."""
    return [*fixture_checks(), *marker_checks(), *notify_checks(), *composition_checks(), *maximum_checks(),
            *window_checks(), *load_checks(), *path_checks(), *fanout_checks(), *run_checks(), *reuse_checks(),
            *build_checks(), *cache_checks(), *cache_build_checks()]


def write_fixture(log: Path, build_json: Path) -> None:
    """Trim a 'fixture' group log to what its probes read, then pin its graded rows and pass figures."""
    spec = json.loads(build_json.read_text())
    p = scenario.point('1x1', spec)
    if spec['interfaces'] != 1:
        raise SystemExit('the fixture is the one-interface point')
    text = log.read_text()
    records = re.findall(r'^EVW \d+ \d+ ([0-9a-f]+)$', text, re.M)
    deadlines = {int(records[k + 2], 16) for k in range(0, len(records) - 3, 4)}
    kept = [line for line in text.splitlines()
            if not line.startswith(('MS ', 'PC ', 'FETCH ')) or int(line.split()[2]) in deadlines]
    FIXTURE_LOG.write_text('\n'.join(kept) + '\n')
    oracle = dict(point=dict(label='fixture', shape=p.shape, interfaces=p.interfaces, entity_id=p.entity_id,
                             mac=p.mac, sources=p.sources, sinks=p.sinks),
                  fixture_sha256=hashlib.sha256(FIXTURE_LOG.read_bytes()).hexdigest(), rows={})
    graded = grade.grade(FIXTURE_LOG.read_text(), scenario.fixture_groups(p)[0], spec['sys_hz'], spec['cpu_hz'])
    for r in graded['probes']:
        if r['status'] != 'measured':
            raise SystemExit(f'fixture probe {r["probe"]} is not measured: {r}')
        oracle['rows'][r['probe']] = {k: r.get(k) for k in PINNED}
    oracle['passes'] = headline(graded)
    ORACLE.write_text(json.dumps(oracle, indent=1) + '\n')
    print(f'wrote {FIXTURE_LOG.name} ({FIXTURE_LOG.stat().st_size} B) and {ORACLE.name}: {len(oracle["rows"])} rows')


@contextlib.contextmanager
def mutated(name: str) -> Iterator[None]:
    """One rule replaced by its mutant (selftest_mutants.MUTANTS)."""
    with contextlib.ExitStack() as stack:
        for p in selftest_mutants.MUTANTS[name]():
            stack.enter_context(p)
        yield


def main(argv: list[str] | None = None) -> int:
    """Write the fixture, or run every check and every mutant."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-fixture', nargs=2, type=Path, metavar=('LOG', 'BUILD_JSON'))
    args = parser.parse_args(argv)
    if args.write_fixture:
        write_fixture(*args.write_fixture)
        return 0
    failures = 0
    for name, ok, detail in checks():
        print(f'{"PASS" if ok else "FAIL"}: {name}' + ('' if ok else f': {detail[:300]}'))
        failures += not ok
    for name in selftest_mutants.MUTANTS:
        with mutated(name):
            try:
                failed = [(n, detail) for n, ok, detail in checks() if not ok]
            except (grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as error:
                failed = [(f'refused: {error}', '')]
        if failed:
            print(f'MUTANT caught: {name}: {failed[0][0]}' + (f' ({failed[0][1][:160]})' if failed[0][1] else ''))
        else:
            print(f'MUTANT ESCAPED: {name}')
            failures += 1
    print(f'self-test: {failures} failures')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
