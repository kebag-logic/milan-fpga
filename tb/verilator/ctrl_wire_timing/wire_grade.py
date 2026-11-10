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
are outside the simulation, a fixed sub-microsecond each way. Every figure is
interface 0's, the one with a datapath; the bench's interfaces (RXB, TXB) are
load and presence only.

COMMITS. The n-th TX_HEAD write on a channel is the n-th frame of that channel
to leave KL_mbx on any interface (MTX); interface 0's of those, in order, are
that channel's protocol's frames at the MAC. Refused when the counts differ or
a frame leaves before its commit.

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
    next PROBE_TX's commit. Its wire legs are reported apart: the commit to
    the command's last byte out, the talker's turnaround, and the response's
    last byte in to the handling;
  - the bind to the PROBE_TX it causes: the bind's first byte in to the
    command's last byte out.
Each must be under 200 ms; the margin to 200 ms is the figure. A command
without its answer, or an answer without its command, is a finding, but for
a command the log ends within the bound of, which is reported as censored:
the run did not wait out that command's bound (wire_scenario.TAIL_MS waits
it out after every run's last command).

AECP (#868 item 3; IEEE 1722.1-2021 9.2.1, the AECP response the Issue
names, whose bound is FR_NFR.md 3.4.1's 240 ms, IEEE 1722.1-2021 9.3.2.6 and
Milan v1.2 5.4.3.4, NFR-LAT-02): each AEM or MVU command a draw sends, from
its first byte in to the last byte out of its final response (the response
with its sequence_id and message_type, IN_PROGRESS answers counted apart);
censored as ACMP's.

MAAP (#868 item 2; IEEE 1722-2016 B.3.4.2: strictly 500 ms < probe interval
< 600 ms; B.3.4.1: strictly 30 s < announce interval < 32 s). Each PROBE and
ANNOUNCE after the first PROBE leaves on the expiry of the interface's MAAP
timer slot: the slot's last arm made before the frame's commit whose deadline
had come. Its egress is the timer's millisecond to the frame's first byte out;
each interval is between consecutive PROBEs, or consecutive ANNOUNCEs, first
byte to first byte, and its drawn value is the arm's deadline less the
millisecond it was made in. The firmware draws inside 511 to 589 ms and 30011
to 31989 ms, reserving 11 ms at each endpoint for the egress
(maap/README.md:43-46). Graded: each interval strictly inside its clause, each
drawn value inside its reserved range, each frame's egress and each
interval's error (at the wire less drawn) strictly under the 11 ms reserve.

ADP (#868 item 3; Milan v1.2 Table 5.50: the 5 s advertise timer, then a
0 to 4 s random delay before ENTITY_AVAILABLE; 5.6.3.5.2: the startup delay
0 to 2 s). Each ENTITY_AVAILABLE leaves on the expiry of the interface's ADP
slot (the delay); the arm in the pass that sends it is the advertise timer.
Graded: every advertise arm 5000 ms, every delay drawn inside its range, each
AVAILABLE's egress from its delay's millisecond under FR_NFR.md 3.4.1's
ceiling (400 ms, the startup's 200 ms), and each advertise period at the wire
(consecutive AVAILABLEs, first byte to first byte) inside Table 5.50's 5 to
9 s, widened by two milliseconds' phase below and the ceiling above.

EGRESS. Each sent frame's mailbox commit to its first and last beat out, per
protocol.

LOAD. Each LOAD line, by name: the frames offered and the echoes skipped,
reported so the stated load is in the result.

Exit codes of main(): 0 a pass, 1 a finding, 2 a refusal.
"""
from __future__ import annotations

import bisect
import json
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path

#: Milan v1.2 Table 5.26: every ACMP command transaction's timeout, in ms.
ACMP_TIMEOUT_MS = 200.0
#: The AECP response bound, in ms (FR_NFR.md 3.4.1: IEEE 1722.1-2021 9.3.2.6, Milan v1.2 5.4.3.4).
AECP_RESPONSE_MS = 240.0
#: IEEE 1722-2016 B.3.4.2 and B.3.4.1 (Table B.8): each interval strictly between these, in ms.
MAAP_PROBE_MS = (500.0, 600.0)
MAAP_ANNOUNCE_MS = (30_000.0, 32_000.0)
#: The firmware's reserved draws (maap/README.md:43-44), in ms: 11 ms inside each endpoint.
MAAP_PROBE_DRAW_MS = (511, 589)
MAAP_ANNOUNCE_DRAW_MS = (30_011, 31_989)
MAAP_RESERVE_MS = 11.0
#: Milan v1.2 Table 5.50: the advertise timer and the delay's range; 5.6.3.5.2: the startup delay's, in ms.
ADP_ADVERTISE_MS = 5000
ADP_DELAY_MS = (0, 4000)
ADP_STARTUP_DELAY_MS = (0, 2000)
#: FR_NFR.md 3.4.1's ceilings on the ADP path, in ms: 10 % of min(4 s, 5 s, 20 s), and of the startup's 2 s.
ADP_CEILING_MS = 400.0
ADP_STARTUP_CEILING_MS = 200.0
#: The millisecond phases an advertise period can lose against its timers: one at each of its two arms.
ADP_PHASE_MS = 2.0
#: The mailbox channels (sw/mailbox/mailbox.yaml), by index, and the protocol each one carries at the wire.
CHANNELS = ('adp', 'acmp', 'aecp', 'maap', 'srp')
#: AVTP control subtypes (IEEE 1722-2016 Table 6; IEEE 1722.1-2021 Table B.1).
SUBTYPES = {0xFA: 'adp', 0xFB: 'aecp', 0xFC: 'acmp', 0xFE: 'maap'}
#: ACMP message types (IEEE 1722.1-2021 Table 8-1; Milan v1.2 5.5.2 renames CONNECT_RX as BIND_RX).
PROBE_TX, PROBE_TX_RESPONSE, BIND_RX, BIND_RX_RESPONSE = 0, 1, 6, 7
#: AECP message types (IEEE 1722.1-2021 Table 9-1): AEM and vendor-unique (Milan's MVU) commands and responses.
AECP_RESPONSE_OF = {0: 1, 6: 7}
#: AECP status IN_PROGRESS (IEEE 1722.1-2021 Table 7-170; the firmware's AECP_IN_PROGRESS, aecp.h).
AECP_IN_PROGRESS = 9
#: MAAP message types (IEEE 1722-2016 Table B.4); ADP's (IEEE 1722.1-2021 Table 6-1).
MAAP_PROBE, MAAP_ANNOUNCE = 1, 3
ADP_AVAILABLE = 0
#: TMR_CMD's fields (sw/mailbox/mailbox.yaml): SLOT [7:0], OP [31:30], 1 an arm.
TMR_ARM = 1
#: The firmware's timer slots (ctrl_app.h): ADP's run of MBX_N_IF slots from 0, then ACMP's, then MAAP's.
ADP_FIRST_SLOT_IFS = 0
ACMP_FIRST_SLOT_IFS = 1
MAAP_FIRST_SLOT_IFS = 2
#: The stimulus's tags: the graded commands (wire_scenario.py).
BIND_TAG, AECP_TAG = 'acmp-bind-', 'aecp-'


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
    def kind(self) -> int:
        """An AVTP control frame's message_type (IEEE 1722-2016 Figure 9: the low nibble of byte 15)."""
        return self.data[15] & 0x0F

    @property
    def acmp_seq(self) -> int:
        """An ACMP frame's sequence_id (IEEE 1722.1-2021 8.2.1.18)."""
        return int.from_bytes(self.data[62:64], 'big')

    @property
    def aecp_seq(self) -> int:
        """An AECP frame's sequence_id (IEEE 1722.1-2021 9.2.1.1.8)."""
        return int.from_bytes(self.data[34:36], 'big')

    @property
    def status(self) -> int:
        """An AVTP control frame's status (the five bits above control_data_length)."""
        return self.data[16] >> 3


@dataclass
class Log:
    """The parsed log."""
    ms: list[tuple[int, int]] = field(default_factory=list)
    rx: list[Wire] = field(default_factory=list)
    tx: list[Wire] = field(default_factory=list)
    bench_rx: int = 0
    bench_tx: int = 0
    txc: list[tuple[int, int]] = field(default_factory=list)
    mtx: list[tuple[int, int, int]] = field(default_factory=list)
    tmr: list[tuple[int, int, int]] = field(default_factory=list)
    loads: dict[str, list[int]] = field(default_factory=dict)
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
        elif w[0] == 'RXB':
            log.bench_rx += 1
        elif w[0] == 'TXB':
            log.bench_tx += 1
        elif w[0] == 'TXC':
            log.txc.append((int(w[1]), int(w[2])))
        elif w[0] == 'MTX':
            log.mtx.append((int(w[1]), int(w[2]), int(w[3])))
        elif w[0] == 'TMR':
            log.tmr.append((int(w[1]), int(w[2], 16), int(w[3])))
        elif w[0] == 'LOAD':
            tally = log.loads.setdefault(w[2], [0, 0, 0])
            tally[0] += 1
            tally[1] += int(w[3])
            tally[2] += int(w[4])
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


class Clock:
    """The log's milliseconds: the cycle each NOW_MS value began, and the value at a cycle."""

    def __init__(self, log: Log) -> None:
        self.cycles = [c for c, _ in log.ms]
        self.values = [v for _, v in log.ms]
        self.start = {v: c for c, v in log.ms}

    def at(self, value: int) -> int | None:
        """The cycle NOW_MS became `value`, or None outside the log."""
        return self.start.get(value)

    def now(self, cycle: int) -> int:
        """NOW_MS at a cycle: the last pulse at or before it (0 before the first)."""
        i = bisect.bisect_right(self.cycles, cycle)
        return self.values[i - 1] if i else 0


def commits(log: Log) -> dict[int, list[int]]:
    """Each channel's TX_HEAD writes, in order."""
    out: dict[int, list[int]] = {i: [] for i in range(len(CHANNELS))}
    for at, ch in log.txc:
        out[ch].append(at)
    return out


def matched_commits(log: Log) -> list[tuple[Wire, int]]:
    """Each frame sent at the MAC with its mailbox commit (see COMMITS in the module's docstring)."""
    by_ch = commits(log)
    left: dict[int, list[tuple[int, int]]] = {i: [] for i in range(len(CHANNELS))}
    for at, iface, ch in log.mtx:
        left[ch].append((at, iface))
    sent: dict[str, list[Wire]] = {name: [] for name in CHANNELS}
    for w in log.tx:
        if w.protocol not in sent:
            raise Refused(f'a frame of protocol {w.protocol} left the MAC, which no mailbox channel carries')
        sent[w.protocol].append(w)
    if log.tx and not log.mtx:
        raise Refused("the log has no KL_mbx egress (MTX) lines, so no frame's commit can be found")
    out = []
    for i, name in enumerate(CHANNELS):
        if len(left[i]) > len(by_ch[i]):
            raise Refused(f'{len(left[i])} {name} frames left KL_mbx after {len(by_ch[i])} commits on its channel')
        own = [(at, commit) for (at, iface), commit in zip(left[i], by_ch[i]) if iface == 0]
        if len(sent[name]) > len(own):
            raise Refused(f'{len(sent[name])} {name} frames left the MAC after {len(own)} left KL_mbx on interface 0')
        last = sent[name][-1].first if sent[name] else -1
        lost = [at for at, _ in own[len(sent[name]):] if at < last]   # only the last may still be on its way
        if lost:
            raise Refused(f'a {name} frame left KL_mbx on interface 0 at cycle {lost[0]} and never reached the MAC')
        for w, (out_at, at) in zip(sent[name], own):
            if w.first <= at or out_at <= at:
                raise Refused(f'a {name} frame left at cycle {w.first}, before its commit at {at}')
            if w.last <= out_at:
                raise Refused(f"a {name} frame's last byte left the MAC at cycle {w.last}, before it left KL_mbx at "
                              f'{out_at}')
            out.append((w, at))
    return out


def arms(log: Log, slot: int) -> list[tuple[int, int]]:
    """Every arm of one timer slot: its cycle and deadline."""
    return [(at, deadline) for at, value, deadline in log.tmr if (value >> 30) == TMR_ARM and (value & 0xFF) == slot]


def expiries(log: Log, slot: int, ms: Clock) -> list[tuple[int, int, int]]:
    """Every arm of one timer slot that expired: its cycle, its deadline, and its expiry, the cycle NOW_MS reached
    the deadline, or the arm itself when it had already (a zero delay, Milan v1.2 Table 5.50's lower end). An arm
    expires when no later write of the slot (an arm or a cancel, TMR_CMD) came before its expiry."""
    writes = [(at, value >> 30, deadline) for at, value, deadline in log.tmr if (value & 0xFF) == slot]
    out = []
    for n, (at, op, deadline) in enumerate(writes):
        due = ms.at(deadline)
        if op != TMR_ARM or due is None:
            continue
        due = max(due, at)
        if n + 1 == len(writes) or writes[n + 1][0] >= due:
            out.append((at, deadline, due))
    return out


def expired_arm(fired: list[tuple[int, int, int]], commit: int) -> tuple[int, int, int] | None:
    """The expiry a frame committed at `commit` left on: the slot's latest expiry by then."""
    found = None
    for arm in fired:
        if arm[2] > commit:
            break
        found = arm
    return found


@dataclass
class Window:
    """Where the log ends, and the cycles of a millisecond: a command the log ends within the bound of, unanswered,
    is censored, not a finding (see the module's docstring)."""
    end: int
    per_ms: int
    censored: list[str] = field(default_factory=list)

    def unanswered(self, cmd: Wire, bound_ms: float, findings: list[str], words: str) -> None:
        """A command with no answer: censored when the log ends within its bound, else the finding `words`."""
        if cmd.first + bound_ms * self.per_ms > self.end:
            self.censored.append(cmd.tag)
        else:
            findings.append(words)


def acmp(log: Log, findings: list[str], interfaces: int, commit_of: dict[int, int], window: Window) -> list[Path_]:
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
    responses = [w for w in log.tx if w.protocol == 'acmp' and w.kind == BIND_RX_RESPONSE]
    probes = [w for w in log.tx if w.protocol == 'acmp' and w.kind == PROBE_TX]
    answers = [w for w in log.rx if w.protocol == 'acmp' and w.kind == PROBE_TX_RESPONSE]
    binds = [w for w in log.rx if w.protocol == 'acmp' and w.kind == BIND_RX and w.tag.startswith(BIND_TAG)]
    for cmd in binds:
        resp = [r for r in responses if r.acmp_seq == cmd.acmp_seq and r.first > cmd.last]
        if not resp:
            window.unanswered(cmd, ACMP_TIMEOUT_MS, findings,
                              f'ACMP: the BIND_RX {cmd.tag} (sequence_id {cmd.acmp_seq:#06x}) has no BIND_RX_RESPONSE')
            continue
        bind.cycles.append(resp[0].last - cmd.first)
        after = [p for p in probes if p.first > cmd.last]
        if not after:
            findings.append(f'ACMP: the BIND_RX {cmd.tag} caused no PROBE_TX')
            continue
        cause.cycles.append(after[0].last - cmd.first)
    slot_arms = [at for at, _ in arms(log, slot)]
    starts = sorted(commit_of[id(p)] for p in probes)
    for p in probes:
        ans = [a for a in answers if a.acmp_seq == p.acmp_seq and a.first > p.last]
        if not ans:
            findings.append(f'ACMP: the PROBE_TX (sequence_id {p.acmp_seq:#06x}) has no PROBE_TX_RESPONSE')
            continue
        start = commit_of[id(p)]
        until = next((s for s in starts if s > start), None)   # the transaction ends before the next PROBE_TX
        window = [at for at in slot_arms if at > start and (until is None or at < until)]
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


def aecp(log: Log, findings: list[str], window: Window) -> list[Path_]:
    """Each graded AEM or MVU command's response time (see the module's docstring), and per command."""
    total = Path_('aecp.response', "IEEE 1722.1-2021 9.2.1 (FR_NFR.md 3.4.1's 240 ms): an AEM or MVU command's "
                  "first byte in to its final response's last byte out", AECP_RESPONSE_MS)
    per: dict[str, Path_] = {}
    commands = [w for w in log.rx if w.protocol == 'aecp' and w.tag.startswith(AECP_TAG)]
    interim = 0
    for cmd in commands:
        want = AECP_RESPONSE_OF.get(cmd.kind)
        resp = [r for r in log.tx if r.protocol == 'aecp' and r.kind == want and r.aecp_seq == cmd.aecp_seq
                and r.first > cmd.last]
        interim += sum(1 for r in resp if r.status == AECP_IN_PROGRESS)
        final = [r for r in resp if r.status != AECP_IN_PROGRESS]
        if not final:
            window.unanswered(cmd, AECP_RESPONSE_MS, findings,
                              f'AECP: the command {cmd.tag} (sequence_id {cmd.aecp_seq:#06x}) has no final response')
            continue
        total.cycles.append(final[0].last - cmd.first)
        name = cmd.tag[len(AECP_TAG):].rsplit('-', 1)[0]
        per.setdefault(name, Path_(f'aecp.response.{name}', 'the same, for one command', None)).cycles.append(
            final[0].last - cmd.first)
    if interim:
        findings.append(f'AECP: {interim} IN_PROGRESS answers to commands that change no face state')
    return [total, *per.values()]


def maap(log: Log, findings: list[str], interfaces: int, commit_of: dict[int, int], us: float) -> list[Path_]:
    """MAAP's timer-driven frames and intervals at the wire (see the module's docstring)."""
    ms = Clock(log)
    fired = expiries(log, MAAP_FIRST_SLOT_IFS * interfaces, ms)
    frames = [w for w in log.tx if w.protocol == 'maap' and w.kind in (MAAP_PROBE, MAAP_ANNOUNCE)]
    egress = Path_('maap.egress', "a timer-driven PROBE's or ANNOUNCE's millisecond to its first byte out, "
                   'under the 11 ms reserve (maap/README.md:43-46)', MAAP_RESERVE_MS)
    probe = Path_('maap.probe_interval', 'IEEE 1722-2016 B.3.4.2: consecutive PROBEs, first byte to first byte',
                  MAAP_PROBE_MS[1])
    announce = Path_('maap.announce_interval', 'IEEE 1722-2016 B.3.4.1: consecutive ANNOUNCEs, first byte to '
                     'first byte', MAAP_ANNOUNCE_MS[1])
    error = Path_('maap.interval_error', "an interval at the wire less its drawn value, in magnitude, under the "
                  '11 ms reserve', MAAP_RESERVE_MS)
    drawn: dict[int, int] = {}
    for n, w in enumerate(frames):
        if n == 0 and w.kind == MAAP_PROBE:
            continue   # the first PROBE follows the link (B.3.6.1), not a timer
        arm = expired_arm(fired, commit_of[id(w)])
        if arm is None:
            findings.append(f'MAAP: the frame at cycle {w.first} (type {w.kind}) left on no expired timer')
            continue
        egress.cycles.append(w.first - arm[2])
        drawn[id(w)] = arm[1] - ms.now(arm[0])
    for kind, path, clause, draw in ((MAAP_PROBE, probe, MAAP_PROBE_MS, MAAP_PROBE_DRAW_MS),
                                     (MAAP_ANNOUNCE, announce, MAAP_ANNOUNCE_MS, MAAP_ANNOUNCE_DRAW_MS)):
        same = [w for w in frames if w.kind == kind]
        for a, b in zip(same, same[1:]):
            gap = b.first - a.first
            path.cycles.append(gap)
            gap_ms = gap * us / 1000
            if not clause[0] < gap_ms < clause[1]:
                findings.append(f'{path.name}: {gap_ms:.3f} ms is not strictly inside {clause[0]:.0f} to '
                                f'{clause[1]:.0f} ms ({path.clause})')
            if id(b) not in drawn:
                continue
            d = drawn[id(b)]
            if not draw[0] <= d <= draw[1]:
                findings.append(f'MAAP: an interval drawn at {d} ms, outside the reserved {draw[0]} to {draw[1]} ms '
                                '(maap/README.md:44)')
            error.cycles.append(abs(gap - round(d * 1000 / us)))
    return [egress, probe, announce, error]


def adp(log: Log, findings: list[str], interfaces: int, commit_of: dict[int, int], us: float) -> list[Path_]:
    """ADP's advertise period and each ENTITY_AVAILABLE's egress at the wire (see the module's docstring)."""
    ms = Clock(log)
    slot = ADP_FIRST_SLOT_IFS * interfaces
    fired = expiries(log, slot, ms)
    slot_arms = arms(log, slot)
    frames = [w for w in log.tx if w.protocol == 'adp' and w.kind == ADP_AVAILABLE]
    egress = Path_('adp.egress', "an ENTITY_AVAILABLE's delay millisecond to its first byte out, under "
                   "FR_NFR.md 3.4.1's 400 ms", ADP_CEILING_MS)
    period = Path_('adp.advertise_period', 'Milan v1.2 Table 5.50: consecutive ENTITY_AVAILABLEs, first byte to '
                   'first byte, inside 5 to 9 s', ADP_ADVERTISE_MS + ADP_DELAY_MS[1] + ADP_CEILING_MS)
    for n, w in enumerate(frames):
        arm = expired_arm(fired, commit_of[id(w)])
        if arm is None:
            findings.append(f'ADP: the ENTITY_AVAILABLE at cycle {w.first} left on no expired timer')
            continue
        delay_range, ceiling = (ADP_STARTUP_DELAY_MS, ADP_STARTUP_CEILING_MS) if n == 0 else (ADP_DELAY_MS,
                                                                                              ADP_CEILING_MS)
        drawn = arm[1] - ms.now(arm[0])
        if not delay_range[0] <= drawn <= delay_range[1]:
            findings.append(f'ADP: a delay drawn at {drawn} ms, outside {delay_range[0]} to {delay_range[1]} ms '
                            '(Milan v1.2 Table 5.50, 5.6.3.5.2)')
        delay = w.first - arm[2]
        egress.cycles.append(delay)
        if delay * us / 1000 >= ceiling:
            findings.append(f'adp.egress: {delay * us / 1000:.3f} ms is not under {ceiling} ms (FR_NFR.md 3.4.1)')
        nxt = next(((at, d) for at, d in slot_arms if at > arm[2]), None)   # the advertise timer, the same pass
        if nxt is not None and nxt[1] - ms.now(nxt[0]) != ADP_ADVERTISE_MS:
            findings.append(f'ADP: the advertise timer after the ENTITY_AVAILABLE at cycle {w.first} is '
                            f'{nxt[1] - ms.now(nxt[0])} ms, not 5000 ms (Milan v1.2 Table 5.50)')
    low = ADP_ADVERTISE_MS + ADP_DELAY_MS[0] - ADP_PHASE_MS
    high = ADP_ADVERTISE_MS + ADP_DELAY_MS[1] + ADP_CEILING_MS
    for a, b in zip(frames, frames[1:]):
        gap = b.first - a.first
        period.cycles.append(gap)
        if not low <= gap * us / 1000 < high:
            findings.append(f'adp.advertise_period: {gap * us / 1000:.3f} ms is not inside {low} to {high} ms '
                            '(Milan v1.2 Table 5.50)')
    return [egress, period]


def egress(log: Log, matched: list[tuple[Wire, int]]) -> list[Path_]:
    """Each protocol's commit to first and last byte out."""
    first = {n: Path_(f'egress.{n}.first', f"a {n} frame's commit to its first byte out", None) for n in CHANNELS}
    last = {n: Path_(f'egress.{n}.last', f"a {n} frame's commit to its last byte out", None) for n in CHANNELS}
    for w, at in matched:
        first[w.protocol].cycles.append(w.first - at)
        last[w.protocol].cycles.append(w.last - at)
    return [p for n in CHANNELS for p in (first[n], last[n]) if p.cycles]


#: The paths every run must sample: the bound is checked only where samples exist, so a run that lost its draws or
#: its timers would otherwise pass.
REQUIRED = ('acmp.bind_rx', 'acmp.probe_tx', 'aecp.response', 'maap.egress', 'maap.probe_interval',
            'maap.interval_error', 'adp.egress')


def grade(text: str, sys_hz: int, draws: int, interfaces: int = 1, announces: int = 1) -> tuple[dict, list[str]]:
    """The result and the findings; Refused when the log cannot be graded."""
    log = parse(text)
    if not log.tally.endswith('failures: 0 =='):
        raise Refused(f'the model did not complete: {log.tally or "no tally"}')
    if log.ready is None:
        raise Refused('the firmware never reached its ready line')
    us = clock(log, sys_hz)
    findings: list[str] = []
    matched = matched_commits(log)
    commit_of = {id(w): at for w, at in matched}
    window = Window(log.ms[-1][0], sys_hz // 1000)
    paths = acmp(log, findings, interfaces, commit_of, window) + aecp(log, findings, window) + \
        maap(log, findings, interfaces, commit_of, us) + adp(log, findings, interfaces, commit_of, us)
    binds = len([w for w in log.rx if w.protocol == 'acmp' and w.kind == BIND_RX and w.tag.startswith(BIND_TAG)])
    if binds != draws:
        findings.append(f'ACMP: the log carries {binds} BIND_RX commands, the run asked for {draws}')
    commands = len([w for w in log.rx if w.protocol == 'aecp' and w.tag.startswith(AECP_TAG)])
    if commands != draws:
        findings.append(f'AECP: the log carries {commands} graded commands, the run asked for {draws}')
    sent = len([w for w in log.tx if w.protocol == 'maap' and w.kind == MAAP_ANNOUNCE])
    if sent < announces:
        findings.append(f'MAAP: {sent} ANNOUNCEs left the MAC, the run asked for {announces}')
    rows = [p.row(us) for p in paths + egress(log, matched)]
    for r in rows:
        if r.get('bound_ms') is not None and r['n'] and r['max_ms'] >= r['bound_ms']:
            findings.append(f"{r['path']}: {r['max_ms']} ms is not under {r['bound_ms']} ms ({r['clause']})")
        if r['path'] in REQUIRED and not r['n']:
            findings.append(f"{r['path']}: no sample")
    if announces > 1 and not any(r['path'] == 'maap.announce_interval' and r['n'] for r in rows):
        findings.append('maap.announce_interval: no sample')
    result = dict(sys_hz=sys_hz, us_per_cycle=us, ready_ms=round(log.ready * us / 1000, 3), draws=draws,
                  interfaces=interfaces, announces=announces, rx_frames=len(log.rx), tx_frames=len(log.tx),
                  bench_rx_frames=log.bench_rx, bench_tx_frames=log.bench_tx,
                  simulated_ms=log.ms[-1][1], summary=log.summary, censored=window.censored,
                  load={name: dict(offers=t[0], frames=t[1], skipped=t[2]) for name, t in sorted(log.loads.items())},
                  rows=rows)
    return result, findings


def table(result: dict) -> str:
    """The figures as a Markdown table, in microseconds and milliseconds."""
    out = ['| Path | N | min us | mean us | max us | min ms | mean ms | max ms | bound ms | margin ms |',
           '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in result['rows']:
        if not r['n']:
            continue
        out.append(f"| `{r['path']}` | {r['n']} | {r['min_us']:.3f} | {r['mean_us']:.3f} | {r['max_us']:.3f} | "
                   f"{r['min_ms']:.4f} | {r['mean_ms']:.4f} | {r['max_ms']:.4f} | "
                   f"{r['bound_ms'] if r['bound_ms'] is not None else '-'} | {r.get('margin_ms', '-')} |")
    loads = ', '.join(f"{name}: {t['offers']} offers, {t['frames']} frames, {t['skipped']} echoes skipped"
                      for name, t in result['load'].items()) or 'none'
    censored = ', '.join(result['censored']) or 'none'
    return '\n'.join(out) + (f"\n\nLoad: {loads}. Simulated {result['simulated_ms']} ms. Censored (the log ends "
                              f"within the command's bound, unanswered): {censored}.\n")


def main(argv: list[str]) -> int:
    """wire_grade.py <log> <sys_hz> <draws> <interfaces> <announces> [<result.json>]"""
    text = Path(argv[0]).read_text()
    try:
        result, findings = grade(text, int(argv[1]), int(argv[2]), int(argv[3]), int(argv[4]))
    except Refused as why:
        print(f'REFUSED: {why}')
        return 2
    if len(argv) > 5:
        Path(argv[5]).write_text(json.dumps(dict(result, findings=findings), indent=1) + '\n')
    print(table(result), end='')
    for line in findings:
        print('FINDING', line)
    print(f"ctrl_wire_timing grade: {len(findings)} finding(s), {result['draws']} draws")
    return 1 if findings else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
