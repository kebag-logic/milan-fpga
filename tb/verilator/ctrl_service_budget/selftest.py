# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The budget grader's portable self-test (#665 S2; the method of #397 round 2).

It needs Python and PyYAML (the mailbox contract) and nothing built. It
regrades the committed trace fixture.log, which the 'fixture' group
recorded on the test SoC, against the rows oracle.json pins; it checks the
clock conversion, the exact-budget boundary, a timer path's origin, the
last-end rule, tags, interfaces, sequence ids and the normative wait on
synthetic traces; and it plants an over-budget path in the recorded trace.
Then it mutates each grader rule in turn and requires a named check to fail.

Regenerate the fixture only through its generator, from a fresh 'fixture'
group run:

    python3 -B tb/verilator/ctrl_service_budget/selftest.py --write-fixture RESULTS/fixture.log BUILD/build.json
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import re
import sys
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import grade  # noqa: E402
import scenario  # noqa: E402

FIXTURE_LOG = HERE / 'fixture.log'
ORACLE = HERE / 'oracle.json'
SYS_HZ, CPU_HZ = 100_000_000, 50_000_000
PINNED = ('status', 'start_sys', 'end_sys', 'sys_cycles', 'cpu_cycles', 'ms', 'within_t_svc', 'within_ceiling',
          'pass_cycles', 'pass_mbx_accesses', 'passes')
#: FR_NFR.md 3.4.1's ceilings, restated here on purpose: a changed table must fail.
CEILINGS = {'adp': 200.0, 'disc': 20.0, 'acmp': 20.0, 'aecp': 24.0, 'notify': 24.0, 'maap': 50.0, 'srp': 18.0}


def fixture_group(oracle: dict) -> scenario.Group:
    """The 'fixture' group of the point the oracle pins."""
    p = scenario.Point(**oracle['point'])
    return scenario.fixture_groups(p)[0]


def regraded(oracle: dict) -> dict:
    """The committed trace, graded now."""
    return grade.grade(FIXTURE_LOG.read_text(), fixture_group(oracle), SYS_HZ, CPU_HZ)


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


def acmp_response(sequence: int, message: str = 'GET_RX_STATE_RESPONSE') -> bytes:
    """An ACMP response frame with that sequence_id."""
    return scenario.f.acmp(scenario.f.ACMP[message], 0x020000000001, scenario.f.Acmp(sequence=sequence))


def checks() -> list[tuple[str, bool, str]]:
    """Every named check and whether it holds."""
    out = []
    oracle = json.loads(ORACLE.read_text())
    digest = hashlib.sha256(FIXTURE_LOG.read_bytes()).hexdigest()
    out.append(('fixture digest', digest == oracle['fixture_sha256'], digest))
    rows = {r['probe']: r for r in regraded(oracle)['probes']}
    for name, pinned in oracle['rows'].items():
        got = {k: rows.get(name, {}).get(k) for k in PINNED}
        out.append((f'fixture row {name}', got == pinned, f'{got} != {pinned}' if got != pinned else ''))
    g = grade.Grader(grade.Log(SYS_HZ, CPU_HZ))
    out.append(('clock conversion', (g.cpu_cycles(1_000_000), g.cpu_cycles(3), g.ms(1_000_000)) == (500_000, 2, 10.0),
                f'{g.cpu_cycles(1_000_000)}, {g.cpu_cycles(3)}, {g.ms(1_000_000)}'))
    out.append(('ceilings pinned', scenario.CEILING_MS == CEILINGS and scenario.T_SVC_MS == 10.0,
                f'{scenario.CEILING_MS} {scenario.T_SVC_MS}'))
    acmp = scenario.CH['acmp']
    probe = scenario.Probe('s.cmd.if0', 'GET_RX_STATE', 'acmp', f'rxc:{acmp}', [f'resp:{acmp}:41'])
    frame_lines = ['MARK 1000 s.cmd.if0', 'RXS 1100 0 70 s.cmd.if0', 'RXE 1169', 'RXC 1173 1']
    for delta, within, name in ((1_000_000, True, 'exact budget passes'), (1_000_001, False, 'one cycle over misses')):
        r = one(synthetic(frame_lines + tx_record(acmp, 0, acmp_response(0x41), 0, 1173 + delta)), probe)
        out.append((name, r.get('within_t_svc') is within and r.get('sys_cycles') == delta, str(r)))
    # Tags: the probe's own frame, the second on the channel, starts the path.
    lines = ['MARK 1000 s.cmd.if0', 'RXS 1100 0 70 -', 'RXE 1169', 'RXC 1173 1', 'RXS 1200 0 70 s.cmd.if0',
             'RXE 1269', 'RXC 1273 1', *tx_record(acmp, 0, acmp_response(0x41), 0, 5273)]
    r = one(synthetic(lines), probe)
    out.append(('tagged start', r.get('start_sys') == 1273, str(r)))
    # Sequence and interface: an earlier response to another command, or on the other interface, is not the end.
    lines = frame_lines + tx_record(acmp, 1, acmp_response(0x41), 0, 2000) + \
        tx_record(acmp, 0, acmp_response(0x40), 20, 3000) + tx_record(acmp, 0, acmp_response(0x41), 40, 4000)
    r = one(synthetic(lines), probe)
    out.append(('sequence and interface', r.get('end_sys') == 4000, str(r)))
    # The last required output ends the path.
    both = scenario.Probe('s.cmd.if0', 'BIND_RX', 'acmp', f'rxc:{acmp}', [f'resp:{acmp}:41', 'arm:1'])
    arm = f'PASS 2 5000 2500 50 instr=10 store_mbx=1 W 6000:{scenario.TMR_CMD_WORD:x}:{1 << 30 | 0x100 | 1:x}'
    r = one(synthetic(frame_lines + tx_record(acmp, 0, acmp_response(0x41), 0, 2000) + [arm]), both)
    out.append(('last end decides', r.get('end_sys') == 6000, str(r)))
    # A timer path starts at its armed deadline, not when the record is posted or taken.
    timer = scenario.Probe('s.timer.if0', 'TMR_NO_RESP', 'acmp', 'deadline:1', ['arm:1'])
    lines = ['MARK 1000 s.timer.if0', 'MS 300000 3', 'EVW 300400 0 00000001', 'EVW 300401 1 00010007',
             'EVW 300402 2 00000003', 'EVW 300403 3 00000003',
             f'PASS 1 300500 150250 50 instr=10 store_mbx=1 W 310000:{scenario.TMR_CMD_WORD:x}:{1 << 30 | 1:x}']
    r = one(synthetic(lines), timer)
    out.append(('timer origin is the armed deadline', r.get('start_sys') == 300000 and r.get('sys_cycles') == 10000,
                str(r)))
    # A normative wait W extends the bound to W + T_svc (3.4.1), and nothing more.
    waited = scenario.Probe('s.cmd.if0', 'Domain', 'srp', f'rxc:{acmp}', [f'resp:{acmp}:41'], wait_ms=200.0)
    for delta, within, name in ((21_000_000, True, 'W + T_svc passes'), (21_000_001, False, 'W + T_svc + 1 misses')):
        r = one(synthetic(frame_lines + tx_record(acmp, 0, acmp_response(0x41), 0, 1173 + delta)), waited)
        out.append((name, r.get('within_t_svc') is within, str(r)))
    # A planted over-budget path in the recorded trace: the BIND_RX response moved past T_svc.
    text = FIXTURE_LOG.read_text()
    row = oracle['rows']['fixture.bind_rx.if0']
    late = row['start_sys'] + 1_000_001
    planted = re.sub(rf'^TXC {row["end_sys"]} ', f'TXC {late} ', text, count=1, flags=re.M)
    planted = re.sub(rf'\b{row["end_sys"]}:', f'{late}:', planted)
    rows = {r['probe']: r for r in grade.grade(planted, fixture_group(oracle), SYS_HZ, CPU_HZ)['probes']}
    hit = rows['fixture.bind_rx.if0']
    caught = (hit.get('status') == 'measured' and hit.get('within_t_svc') is False
              and hit.get('sys_cycles', 0) > 1_000_000)
    out.append(('planted over-budget path is caught', caught, str({k: hit.get(k) for k in PINNED})))
    return out


@contextlib.contextmanager
def mutant(name: str) -> Iterator[None]:
    """One grader rule replaced by a plausible defect."""
    original_start = grade.Grader.start
    original_end = grade.Grader.end
    if name == 'marker: the frame tag is ignored':
        def _start(self: grade.Grader, probe: scenario.Probe, interface: int, after: int, before: int) -> int | None:
            ch = int(probe.start.split(':')[1]) if probe.start.startswith('rxc') else -1
            hits = [c for c, k, _, _ in self.log.rxc if after <= c < before and k == ch]
            return hits[0] if hits else original_start(self, probe, interface, after, before)
        with patch.object(grade.Grader, 'start', _start):
            yield
    elif name == 'marker: a timer path starts when its record is posted':
        def _start(self: grade.Grader, probe: scenario.Probe, interface: int, after: int, before: int) -> int | None:
            if probe.start.startswith('deadline'):
                slot = int(probe.start.split(':')[1])
                for cycle, w in self.log.records:
                    if after <= cycle < before and w[0] & 0xFF == grade.EV_TIMER and (w[1] >> 16) & 0xFF == slot:
                        return cycle
                return None
            return original_start(self, probe, interface, after, before)
        with patch.object(grade.Grader, 'start', _start):
            yield
    elif name == 'marker: any response on the channel ends the path':
        def _end(self: grade.Grader, spec: str, probe: scenario.Probe, interface: int, start: int,
                 before: int) -> int | None:
            if spec.startswith('resp'):
                spec = 'tx:' + spec.split(':')[1]
            return original_end(self, spec, probe, interface, start, before)
        with patch.object(grade.Grader, 'end', _end):
            yield
    elif name == 'marker: the interface is ignored':
        def _end(self: grade.Grader, spec: str, probe: scenario.Probe, interface: int, start: int,
                 before: int) -> int | None:
            if spec.startswith('resp'):
                ch, seq = (int(v, 16) if k else int(v) for k, v in enumerate(spec.split(':')[1:]))
                hits = [c for c, k, _, fr in self.log.tx if start <= c < before and k == ch
                        and grade.response_sequence(fr) == seq]
                return hits[0] if hits else None
            return original_end(self, spec, probe, interface, start, before)
        with patch.object(grade.Grader, 'end', _end):
            yield
    elif name == 'marker: the first required output ends the path':
        with patch.object(grade, 'combine_ends', min):
            yield
    elif name == 'clock ratio: CPU cycles equal bus cycles':
        with patch.object(grade.Grader, 'cpu_cycles', lambda self, n: n):
            yield
    elif name == 'clock ratio: inverted':
        with patch.object(grade.Grader, 'cpu_cycles', lambda self, n: n * self.log.sys_hz // self.log.cpu_hz):
            yield
    elif name == 'clock ratio: milliseconds from the CPU clock':
        with patch.object(grade.Grader, 'ms', lambda self, n: n * 1000.0 / self.log.cpu_hz):
            yield
    elif name == 'deadline: T_svc 20 ms':
        with patch.object(scenario, 'T_SVC_MS', 20.0):
            yield
    elif name == 'deadline: strictly below the budget':
        original = grade.verdicts

        def _verdicts(ms: float, probe: scenario.Probe) -> dict:
            v = original(ms, probe)
            return dict(v, within_t_svc=ms < v['t_svc_ms'])
        with patch.object(grade, 'verdicts', _verdicts):
            yield
    elif name == 'deadline: the normative wait is not added':
        original = grade.verdicts

        def _verdicts(ms: float, probe: scenario.Probe) -> dict:
            v = original(ms, probe)
            return dict(v, within_t_svc=ms <= scenario.T_SVC_MS)
        with patch.object(grade, 'verdicts', _verdicts):
            yield
    elif name == 'deadline: the ACMP ceiling is the transaction timeout':
        with patch.dict(scenario.CEILING_MS, {'acmp': 200.0}):
            yield
    else:
        raise KeyError(name)


MUTANTS = ('marker: the frame tag is ignored', 'marker: a timer path starts when its record is posted',
           'marker: any response on the channel ends the path', 'marker: the interface is ignored',
           'marker: the first required output ends the path', 'clock ratio: CPU cycles equal bus cycles',
           'clock ratio: inverted', 'clock ratio: milliseconds from the CPU clock', 'deadline: T_svc 20 ms',
           'deadline: strictly below the budget', 'deadline: the normative wait is not added',
           'deadline: the ACMP ceiling is the transaction timeout')


def write_fixture(log: Path, build: Path) -> None:
    """Trim a 'fixture' group log to what its probes read, then pin its graded rows."""
    spec = json.loads(build.read_text())
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
    ORACLE.write_text(json.dumps(oracle, indent=1) + '\n')
    print(f'wrote {FIXTURE_LOG.name} ({FIXTURE_LOG.stat().st_size} B) and {ORACLE.name}: {len(oracle["rows"])} rows')


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
    for name in MUTANTS:
        with mutant(name):
            try:
                failed = [n for n, ok, _ in checks() if not ok]
            except (grade.Refusal, KeyError, ValueError, IndexError, TypeError) as error:
                failed = [f'refused: {error}']
        if failed:
            print(f'MUTANT caught: {name}: {failed[0]}')
        else:
            print(f'MUTANT ESCAPED: {name}')
            failures += 1
    print(f'self-test: {failures} failures')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
