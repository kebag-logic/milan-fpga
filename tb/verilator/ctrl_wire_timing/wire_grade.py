# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The wire-timing grader (#665, #868): every figure read off wire_main.cpp's log, offline.

THE CLOCK. Every stamp is a bus cycle of the shape's sys clock, which the
grader is given (the build's sys_hz). It converts nothing before it has
checked that clock against the log: each pair of consecutive MS lines must be
exactly sys_hz / 1000 cycles apart, KL_mbx's millisecond as the testbench
pulses it. A grader given another clock, or a log whose milliseconds drifted,
is refused, so no figure is ever converted with a shifted clock.

THE WIRE. A received frame is stamped at its first and last beat taken at the
datapath's MAC boundary (RXW), a sent frame at its first and last beat taken
there (TXW), both at 1 Gb/s. The MAC core's and the PHY's own pipeline delays
are outside the simulation, a fixed sub-microsecond each way.

ACMP (#868 item 1; Milan v1.2 5.5.2.3, Table 5.26: each command transaction
times out at 200 ms, replacing IEEE 1722.1-2021 Table 8-1's value):
  - bind: a controller's BIND_RX command (IEEE 1722.1-2021 CONNECT_RX_COMMAND)
    from its first byte in to the last byte out of the BIND_RX_RESPONSE with
    its sequence_id: the controller's transaction at the entity's wire;
  - probe: the PROBE_TX the bind causes, from its mailbox commit (TX_HEAD,
    where the listener's transaction starts) to the entity's handling of the
    talker's PROBE_TX_RESPONSE: the arm (TMR_CMD) of the interface's ACMP
    timer slot that follows both the response's last byte in and the arm the
    PROBE_TX itself made (its Table 5.26 timeout, which the same pass commits
    after the command and which a prompt answer can overtake), before the
    next PROBE_TX's commit. Its wire legs
    are reported apart: the commit to the command's last byte out, the
    talker's turnaround, and the response's last byte in to the handling;
  - the bind to the PROBE_TX it causes: the bind's first byte in to the
    command's last byte out.
Each must be under 200 ms; the margin to 200 ms is the figure. A command
without its answer, or an answer without its command, is a finding.

EGRESS. Each sent frame's mailbox commit (the n-th TX_HEAD write on its
channel is the n-th frame of that channel's protocol at the wire) to its first
and last beat out, per protocol.

Exit codes of main(): 0 a pass, 1 a finding, 2 a refusal.
"""
from __future__ import annotations

import json
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path

#: Milan v1.2 Table 5.26: every ACMP command transaction's timeout, in ms.
ACMP_TIMEOUT_MS = 200.0
#: The mailbox channels (sw/mailbox/mailbox.yaml), by index, and the protocol each one carries at the wire.
CHANNELS = ('adp', 'acmp', 'aecp', 'maap', 'srp')
#: AVTP control subtypes (IEEE 1722-2016 Table 6; IEEE 1722.1-2021 Table B.1).
SUBTYPES = {0xFA: 'adp', 0xFB: 'aecp', 0xFC: 'acmp', 0xFE: 'maap'}
#: ACMP message types (IEEE 1722.1-2021 Table 8-1; Milan v1.2 5.5.2 renames CONNECT_RX as BIND_RX).
PROBE_TX, PROBE_TX_RESPONSE, BIND_RX, BIND_RX_RESPONSE = 0, 1, 6, 7
#: TMR_CMD's fields (sw/mailbox/mailbox.yaml): SLOT [7:0], OP [31:30], 1 an arm.
TMR_ARM = 1
#: The firmware's timer slots (ctrl_app.h): ADP's run of MBX_N_IF slots from 0, then ACMP's, then MAAP's.
ACMP_FIRST_SLOT_IFS = 1


class Refused(Exception):
    """The log cannot be graded: the grade would rest on something it cannot trust."""


@dataclass
class Wire:
    """One frame at the MAC boundary."""
    first: int
    last: int
    data: bytes
    tag: str = '-'

    @property
    def protocol(self) -> str:
        """The protocol the frame carries: the AVTP control subtype, or MSRP and MVRP as srp."""
        ethertype = int.from_bytes(self.data[12:14], 'big')
        if ethertype == 0x22F0:
            return SUBTYPES.get(self.data[14], 'avtp')
        return {0x22EA: 'srp', 0x88F5: 'srp'}.get(ethertype, f'0x{ethertype:04x}')

    @property
    def acmp_type(self) -> int:
        """An ACMP frame's message_type (IEEE 1722.1-2021 8.2.1)."""
        return self.data[15] & 0x0F

    @property
    def acmp_seq(self) -> int:
        """An ACMP frame's sequence_id (IEEE 1722.1-2021 8.2.1.18)."""
        return int.from_bytes(self.data[62:64], 'big')


@dataclass
class Log:
    """The parsed log."""
    ms: list[tuple[int, int]] = field(default_factory=list)
    rx: list[Wire] = field(default_factory=list)
    tx: list[Wire] = field(default_factory=list)
    txc: list[tuple[int, int]] = field(default_factory=list)
    tmr: list[tuple[int, int, int]] = field(default_factory=list)
    ready: int | None = None
    summary: str = ''
    tally: str = ''


def parse(text: str) -> Log:
    """Every line the grade reads; others (UART, CSRW, CSRR, MARK) are kept out."""
    log = Log()
    for line in text.splitlines():
        w = line.split()
        if not w:
            continue
        if w[0] == 'MS':
            log.ms.append((int(w[1]), int(w[2])))
        elif w[0] == 'RXW':
            log.rx.append(Wire(int(w[1]), int(w[2]), bytes.fromhex(w[5]), w[4]))
        elif w[0] == 'TXW':
            log.tx.append(Wire(int(w[1]), int(w[2]), bytes.fromhex(w[4])))
        elif w[0] == 'TXC':
            log.txc.append((int(w[1]), int(w[2])))
        elif w[0] == 'TMR':
            log.tmr.append((int(w[1]), int(w[2], 16), int(w[3])))
        elif w[0] == 'READY' and log.ready is None:
            log.ready = int(w[1])
        elif w[0] == 'SUMMARY':
            log.summary = line
        elif line.startswith('== ctrl_wire_timing: checks:'):
            log.tally = line
    return log


def clock(log: Log, sys_hz: int) -> float:
    """Microseconds per bus cycle, once the log's milliseconds are found exactly sys_hz / 1000 cycles apart."""
    per_ms = sys_hz // 1000
    if sys_hz % 1000 or per_ms <= 0:
        raise Refused(f'the declared clock {sys_hz} Hz has no whole number of cycles per millisecond')
    if len(log.ms) < 2:
        raise Refused('the log has fewer than two milliseconds, so its clock cannot be checked')
    gaps = {b[0] - a[0] for a, b in zip(log.ms, log.ms[1:])}
    steps = {b[1] - a[1] for a, b in zip(log.ms, log.ms[1:])}
    if gaps != {per_ms} or steps != {1}:
        raise Refused(f"the clock is shifted: the log's milliseconds are {sorted(gaps)[:3]} cycles apart, the declared "
                      f'{sys_hz} Hz gives {per_ms}')
    return 1e6 / sys_hz


@dataclass
class Path_:
    """One graded path's samples, in bus cycles."""
    name: str
    clause: str
    bound_ms: float | None
    cycles: list[int] = field(default_factory=list)

    def row(self, us_per_cycle: float) -> dict:
        """The path's distribution in microseconds and milliseconds, with its bound and margin."""
        us = [c * us_per_cycle for c in self.cycles]
        out = dict(path=self.name, clause=self.clause, n=len(us), bound_ms=self.bound_ms)
        if us:
            out.update(min_us=round(min(us), 3), mean_us=round(statistics.fmean(us), 3), max_us=round(max(us), 3),
                       min_ms=round(min(us) / 1000, 4), mean_ms=round(statistics.fmean(us) / 1000, 4),
                       max_ms=round(max(us) / 1000, 4))
            if self.bound_ms is not None:
                out['margin_ms'] = round(self.bound_ms - max(us) / 1000, 4)
        return out


def commits(log: Log) -> dict[int, list[int]]:
    """Each channel's TX_HEAD writes, in order."""
    out: dict[int, list[int]] = {i: [] for i in range(len(CHANNELS))}
    for at, ch in log.txc:
        out[ch].append(at)
    return out


def matched_commits(log: Log) -> list[tuple[Wire, int]]:
    """Each sent frame with its mailbox commit: the n-th TX_HEAD write on a channel is the n-th frame of that
    channel's protocol at the wire. Refused when the counts differ, or a frame leaves before its commit."""
    by_ch = commits(log)
    sent: dict[str, list[Wire]] = {name: [] for name in CHANNELS}
    for w in log.tx:
        if w.protocol not in sent:
            raise Refused(f'a frame of protocol {w.protocol} left the MAC, which no mailbox channel carries')
        sent[w.protocol].append(w)
    out = []
    for i, name in enumerate(CHANNELS):
        if len(sent[name]) > len(by_ch[i]):
            raise Refused(f'{len(sent[name])} {name} frames left the MAC after {len(by_ch[i])} commits on its channel')
        for w, at in zip(sent[name], by_ch[i]):
            if w.first <= at:
                raise Refused(f'a {name} frame left at cycle {w.first}, before its commit at {at}')
            out.append((w, at))
    return out


def arms(log: Log, slot: int) -> list[int]:
    """The cycles of every arm of one timer slot."""
    return [at for at, value, _ in log.tmr if (value >> 30) == TMR_ARM and (value & 0xFF) == slot]


def acmp(log: Log, findings: list[str], interfaces: int) -> list[Path_]:
    """The three ACMP paths (see the module's docstring), on interface 0."""
    slot = ACMP_FIRST_SLOT_IFS * interfaces
    bind = Path_('acmp.bind_rx', 'Milan v1.2 Table 5.26, BIND_RX (CONNECT_RX_COMMAND): first byte in to the '
                 "response's last byte out", ACMP_TIMEOUT_MS)
    cause = Path_('acmp.bind_to_probe_tx', "the BIND_RX's first byte in to its PROBE_TX's last byte out", None)
    probe = Path_('acmp.probe_tx', 'Milan v1.2 Table 5.26, PROBE_TX: its commit to the handling of the '
                  'PROBE_TX_RESPONSE', ACMP_TIMEOUT_MS)
    egress = Path_('acmp.probe_tx.egress', "the PROBE_TX's commit to its last byte out", None)
    turn = Path_('acmp.probe_tx.turnaround', "the talker's turnaround: the command's last byte out to the "
                 "response's first byte in", None)
    ingress = Path_('acmp.probe_tx.ingress', "the response's last byte in to its handling (ACMP's timer arm)", None)
    entity = Path_('acmp.probe_tx.entity', "the transaction less the talker's turnaround: the entity's own part",
                   None)
    commit_of = {id(w): at for w, at in matched_commits(log)}
    responses = [w for w in log.tx if w.protocol == 'acmp' and w.acmp_type == BIND_RX_RESPONSE]
    probes = [w for w in log.tx if w.protocol == 'acmp' and w.acmp_type == PROBE_TX]
    answers = [w for w in log.rx if w.protocol == 'acmp' and w.acmp_type == PROBE_TX_RESPONSE]
    binds = [w for w in log.rx if w.protocol == 'acmp' and w.acmp_type == BIND_RX]
    for cmd in binds:
        resp = [r for r in responses if r.acmp_seq == cmd.acmp_seq and r.first > cmd.last]
        if not resp:
            findings.append(f'ACMP: the BIND_RX {cmd.tag} (sequence_id {cmd.acmp_seq:#06x}) has no BIND_RX_RESPONSE')
            continue
        bind.cycles.append(resp[0].last - cmd.first)
        after = [p for p in probes if p.first > cmd.last]
        if not after:
            findings.append(f'ACMP: the BIND_RX {cmd.tag} caused no PROBE_TX')
            continue
        cause.cycles.append(after[0].last - cmd.first)
    starts = sorted(commit_of[id(p)] for p in probes)
    for p in probes:
        ans = [a for a in answers if a.acmp_seq == p.acmp_seq and a.first > p.last]
        if not ans:
            findings.append(f'ACMP: the PROBE_TX (sequence_id {p.acmp_seq:#06x}) has no PROBE_TX_RESPONSE')
            continue
        start = commit_of[id(p)]
        until = next((s for s in starts if s > start), None)   # the transaction ends before the next PROBE_TX
        window = [at for at in arms(log, slot) if at > start and (until is None or at < until)]
        handled = [at for at in window[1:] if at > ans[0].last]
        if not handled:
            findings.append(f'ACMP: the PROBE_TX_RESPONSE to sequence_id {p.acmp_seq:#06x} was never handled')
            continue
        probe.cycles.append(handled[0] - start)
        egress.cycles.append(p.last - start)
        turn.cycles.append(ans[0].first - p.last)
        ingress.cycles.append(handled[0] - ans[0].last)
        entity.cycles.append(handled[0] - start - (ans[0].first - p.last))
    extra = [a for a in answers if not any(p.acmp_seq == a.acmp_seq for p in probes)]
    for a in extra:
        findings.append(f'ACMP: a PROBE_TX_RESPONSE (sequence_id {a.acmp_seq:#06x}) answers no PROBE_TX')
    return [bind, cause, probe, entity, egress, turn, ingress]


def egress(log: Log) -> list[Path_]:
    """Each protocol's commit to first and last byte out."""
    first = {n: Path_(f'egress.{n}.first', f"a {n} frame's commit to its first byte out", None) for n in CHANNELS}
    last = {n: Path_(f'egress.{n}.last', f"a {n} frame's commit to its last byte out", None) for n in CHANNELS}
    for w, at in matched_commits(log):
        first[w.protocol].cycles.append(w.first - at)
        last[w.protocol].cycles.append(w.last - at)
    return [p for n in CHANNELS for p in (first[n], last[n]) if p.cycles]


def grade(text: str, sys_hz: int, draws: int, interfaces: int = 1) -> tuple[dict, list[str]]:
    """The result and the findings; Refused when the log cannot be graded."""
    log = parse(text)
    if not log.tally.endswith('failures: 0 =='):
        raise Refused(f'the model did not complete: {log.tally or "no tally"}')
    if log.ready is None:
        raise Refused('the firmware never reached its ready line')
    us = clock(log, sys_hz)
    findings: list[str] = []
    paths = acmp(log, findings, interfaces)
    binds = len([w for w in log.rx if w.protocol == 'acmp' and w.acmp_type == BIND_RX])
    if binds != draws:
        findings.append(f'ACMP: the log carries {binds} BIND_RX commands, the run asked for {draws}')
    rows = [p.row(us) for p in paths + egress(log)]
    for r in rows:
        if r.get('bound_ms') is not None and r['n'] and r['max_ms'] >= r['bound_ms']:
            findings.append(f"{r['path']}: {r['max_ms']} ms is not under {r['bound_ms']} ms ({r['clause']})")
        if r.get('bound_ms') is not None and not r['n']:
            findings.append(f"{r['path']}: no sample")
    result = dict(sys_hz=sys_hz, us_per_cycle=us, ready_ms=round(log.ready * us / 1000, 3), draws=draws,
                  rx_frames=len(log.rx), tx_frames=len(log.tx), summary=log.summary, rows=rows)
    return result, findings


def table(result: dict) -> str:
    """The figures as a Markdown table, in microseconds and milliseconds."""
    out = ['| Path | N | min us | mean us | max us | max ms | bound ms | margin ms |',
           '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in result['rows']:
        if not r['n']:
            continue
        out.append(f"| `{r['path']}` | {r['n']} | {r['min_us']:.3f} | {r['mean_us']:.3f} | {r['max_us']:.3f} | "
                   f"{r['max_ms']:.4f} | {r['bound_ms'] if r['bound_ms'] is not None else '-'} | "
                   f"{r.get('margin_ms', '-')} |")
    return '\n'.join(out) + '\n'


def main(argv: list[str]) -> int:
    """wire_grade.py <log> <sys_hz> <draws> <interfaces> [<result.json>]"""
    text = Path(argv[0]).read_text()
    try:
        result, findings = grade(text, int(argv[1]), int(argv[2]), int(argv[3]))
    except Refused as why:
        print(f'REFUSED: {why}')
        return 2
    if len(argv) > 4:
        Path(argv[4]).write_text(json.dumps(dict(result, findings=findings), indent=1) + '\n')
    print(table(result), end='')
    for line in findings:
        print('FINDING', line)
    print(f"ctrl_wire_timing grade: {len(findings)} finding(s), {result['draws']} draws")
    return 1 if findings else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
