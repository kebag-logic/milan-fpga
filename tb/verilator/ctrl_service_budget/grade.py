# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Read a group's observation log and grade every probe against T_svc and its ceiling.

Each rule a figure rests on lives in one place, so the self-test can mutate
it and require a named failure:

  the clock ratio   Grader.cpu_cycles, Grader.ms, Grader.bus_cycles and
                    Grader.cpu_ms: every conversion between the bus and the
                    CPU clock, and to milliseconds, goes through them
  the markers       Grader.start and Grader.end; owner(), the frame a receive
                    commit belongs to; Grader.recipients and fanout_end(), a
                    notification's required recipients and its end
  the pass bound    Grader.pass_end and Grader.pass_origin
  the fan-out cost  grade_probe's fanout: the last recipient's commit less the
                    first's, over the gaps between the recipients
  the composition   composed() and population(), checked against defined_load(),
                    which derives each row's population from the contract alone;
                    run.composed_maximum() takes the longest pass over every
                    backlog row's window
  the service       releases() and service(): each loaded channel's first and
                    last record to the end of the pass that released it, a
                    record never released reported as starved, and the records
                    ahead of each: its channel's earlier records not yet
                    released at its commit
  the owed frames   owed_ahead(): the responses committed ahead of a probe's
  the deadlines     scenario.T_SVC_MS, scenario.CEILING_MS and verdicts()
  the run           refuse_run(): an incomplete simulation, a trap or a bus error
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import scenario

TX_RING = {n: (ch.tx_base // 4, ch.tx_words) for n, ch in enumerate(scenario.CONTRACT.channels)}
CHANNEL = {n: ch.name for n, ch in enumerate(scenario.CONTRACT.channels)}
EVENT = {e.value: e.name for e in scenario.CONTRACT.event_types}
EV_TIMER = next(v for v, name in EVENT.items() if name == 'TIMER')
RX_HEADER_WORDS = len(scenario.CONTRACT.rx_header)
#: A receive commit follows its own frame's last byte: KL_mbx_rx takes no byte of the next
#: frame until the verdict (KL_mbx_rx.sv, rx_ready_o in RECV_S only).
COMMIT_LATENCY_MAX = 64
CONTRACT = scenario.CONTRACT        # the mailbox contract (mailbox.yaml), not the stimulus
#: The size of each receive channel's record in a defined composed load, from its clause and
#: never from the stimulus: an ADPDU is 68 bytes after the Ethernet header (IEEE 1722.1-2021
#: 6.2.1) and an ACMPDU 56 (Milan v1.2 5.5.2.2); a READ_DESCRIPTOR command (7.4.5.1), a MAAPDU
#: (IEEE 1722-2016 B.2) and an MSRP Listener declaration (IEEE 802.1Q-2018 35.2.2) are padded
#: to the 60-byte frame minimum.
LOAD_FRAME_BYTES = {'adp': 14 + 68, 'acmp': 14 + 56, 'aecp': 60, 'maap': 60, 'srp': 60}
#: The backlog rows (MAILBOX_SPLIT.md:757-762): their composed windows carry the defined
#: composed load, so the composed maximum is taken over them (run.composed_maximum).
BACKLOG_ROWS = ('backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed')
#: The groups whose composed window carries a defined load: the backlog rows and the
#: self-test's short window.
COMPOSED_ROWS = (*BACKLOG_ROWS, 'fixture')


class Refusal(RuntimeError):
    """A log or a probe the grader cannot accept; the message names the rule."""


@dataclass
class Pass:
    index: int
    start_sys: int
    start_cpu: int
    cycles: int
    fields: dict[str, str]
    writes: list[tuple[int, int, int]]
    modules: dict[str, int]
    idle_before: int = 0      # the longest idle pass of the run of idle passes just before this one

    def count(self, key: str) -> int:
        """A counter of the pass; fetch_* fields are count/wait."""
        value = self.fields.get(key, '0')
        return int(value.split('/')[0])

    def wait(self, key: str) -> int:
        """The cycles spent waiting in a fetch_* or wait_* counter of the pass."""
        value = self.fields.get(key, '0/0')
        return int(value.split('/')[1]) if '/' in value else int(value)


@dataclass
class Log:
    sys_hz: int
    cpu_hz: int
    ms: dict[int, int] = field(default_factory=dict)            # NOW_MS -> system cycle it began
    marks: list[tuple[int, str]] = field(default_factory=list)
    rxc: list[tuple[int, int, int, str, int]] = field(default_factory=list)  # cycle, channel, interface, tag, bytes
    refused: list[tuple[int, int, str, int]] = field(default_factory=list)   # last byte, interface, tag, bytes
    entries: list[tuple[int, str]] = field(default_factory=list)            # cycle, function entered
    traced: list[tuple[str, ...]] = field(default_factory=list)              # SPAN and CALL lines' fields
    pads: list[tuple[int, str, int]] = field(default_factory=list)
    records: list[tuple[int, list[int]]] = field(default_factory=list)
    writes: list[tuple[int, int, int]] = field(default_factory=list)
    tx: list[tuple[int, int, int, bytes]] = field(default_factory=list)  # cycle, channel, interface, frame
    wire: list[tuple[int, int, int, bytes]] = field(default_factory=list)  # cycle, channel, interface, frame
    passes: list[Pass] = field(default_factory=list)
    idle: list[tuple[int, int, int]] = field(default_factory=list)
    steps: list[tuple[int, str]] = field(default_factory=list)
    summary: dict[str, str] = field(default_factory=dict)
    modules: dict[str, int] = field(default_factory=dict)
    code: dict[str, str] = field(default_factory=dict)
    traps: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    result: str = ''
    #: The last run of idle passes ends in the pass the script's end cut short (sim_main.cpp
    #: closes the pass in progress, then flushes that run), so it holds no whole idle pass.
    cut_idle: bool = False


def owner(pending: list[tuple[int, str, int, int]], cycle: int, refused: list) -> tuple[int, str, int]:
    """The frame a receive commit at cycle belongs to: (interface, tag, bytes).

    KL_mbx_rx takes no byte of a frame until the previous frame's verdict, so
    the commit belongs to the frame whose last byte passed last; every older
    frame still pending got no commit, so the filter refused it. A commit
    with no frame ended within COMMIT_LATENCY_MAX cycles before it is refused.
    """
    if not pending or not cycle - COMMIT_LATENCY_MAX <= pending[-1][3] <= cycle:
        raise Refusal(f'the receive commit at {cycle} follows no frame')
    frame = pending.pop()
    refused.extend((end, interface, tag, size) for interface, tag, size, end in pending)
    pending.clear()
    return frame[:3]


def parse(text: str, sys_hz: int, cpu_hz: int) -> Log:
    """Every observation line; a line the testbench does not print is refused."""
    log = Log(sys_hz, cpu_hz)
    pending_rx: list[tuple[int, str, int, int]] = []   # interface, tag, bytes, last byte of frames not yet committed
    rxs = (0, '-', 0)
    evt: dict[int, tuple[int, int]] = {}
    commits: list[tuple[int, int, int]] = []
    idle_max = 0
    for line in text.splitlines():
        if not line or line.startswith(('==', 'RESULT', '  [')):
            if line.startswith('RESULT'):
                log.result = line.split()[1]
            continue
        kind, *rest = line.split()
        if kind == 'MS':
            log.ms[int(rest[1])] = int(rest[0])
        elif kind == 'MARK':
            log.marks.append((int(rest[0]), rest[1]))
        elif kind == 'RXS':
            rxs = (int(rest[1]), rest[3] if len(rest) > 3 else '-', int(rest[2]))
        elif kind == 'RXE':
            pending_rx.append((*rxs, int(rest[0])))
        elif kind == 'RXC':
            cycle = int(rest[0])
            log.rxc.append((cycle, int(rest[1]), *owner(pending_rx, cycle, log.refused)))
        elif kind == 'ENTRY':
            log.entries.append((int(rest[0]), rest[1]))
        elif kind in ('SPAN', 'CALL'):
            # The saved-state store's traced calls (#665): nvm_split_target grades them; this grader reads none.
            log.traced.append((kind, *rest))
        elif kind in ('LINK', 'GM'):
            log.pads.append((int(rest[0]), kind, int(rest[1])))
        elif kind == 'EVW':
            cycle, addr, data = int(rest[0]), int(rest[1]), int(rest[2], 16)
            evt[addr] = (cycle, data)
            if addr % 4 == 3 and all(a in evt for a in range(addr - 3, addr + 1)):
                words = [evt.pop(a)[1] for a in range(addr - 3, addr + 1)]
                log.records.append((cycle, words))
        elif kind == 'TXC':
            commits.append((int(rest[0]), int(rest[1]), int(rest[2])))
        elif kind == 'WIRE':
            # sim_main.cpp prints WIRE <cycle> <interface> <channel> <frame>.
            log.wire.append((int(rest[0]), int(rest[2]), int(rest[1]), bytes.fromhex(rest[3])))
        elif kind == 'PASS':
            index, start_sys, start_cpu, cycles = (int(v) for v in rest[:4])
            body = line.split(' W', 1)
            fields = dict(kv.split('=', 1) for kv in body[0].split()[5:] if '=' in kv)
            writes = [tuple(int(x, 16) if k else int(x) for k, x in enumerate(w.split(':')))
                      for w in body[1].split()] if len(body) > 1 else []
            modules = {m.split(':')[0]: int(m.split(':')[1]) for m in fields.pop('mods', '').split(',') if m}
            log.passes.append(Pass(index, start_sys, start_cpu, cycles, fields, writes, modules, idle_max))
            idle_max = 0
            log.writes.extend(writes)
            log.cut_idle = False
        elif kind == 'IDLE':
            # The testbench flushes a run of idle passes just before the work pass that ends it.
            log.idle.append(tuple(int(v) for v in rest))
            idle_max = int(rest[2])
            log.cut_idle = True
        elif kind == 'STEP':
            log.steps.append((int(rest[0]), ' '.join(rest[2:])))
        elif kind == 'SUMMARY':
            log.summary = dict(kv.split('=', 1) for kv in rest)
        elif kind == 'MODULES':
            log.modules = {kv.split(':')[0]: int(kv.split(':')[1]) for kv in rest}
        elif kind == 'CODE':
            log.code = dict(kv.split('=', 1) for kv in rest)
        elif kind in ('TRAP', 'BUSERR'):
            log.traps.append(line)
        elif kind in ('FLASH', 'FLASHOP', 'REPLY', 'TXREADY', 'PC', 'FETCH'):
            continue
        elif kind == 'FAIL:':
            log.errors.append(line)
        else:
            raise Refusal(f'unknown observation line: {line[:80]}')
    log.refused.extend((end, interface, tag, size) for interface, tag, size, end in pending_rx)
    log.writes.sort()
    log.tx = tx_records(log.writes, commits)
    return log


def tx_records(writes: list[tuple[int, int, int]], commits: list[tuple[int, int, int]]) -> list[tuple]:
    """Each committed TX record's cycle, channel, interface and length, off its header word.

    A TX_HEAD write commits every record between the previous head and the
    new one; each record's word 0 holds its length and interface.
    """
    ring: dict[int, dict[int, int]] = {ch: {} for ch in TX_RING}
    head = {ch: 0 for ch in TX_RING}
    out = []
    w = 0
    for cycle, ch, value in sorted(commits):
        while w < len(writes) and writes[w][0] <= cycle:
            _, word, data = writes[w]
            for c, (base, words) in TX_RING.items():
                if base <= word < base + words:
                    ring[c][word - base] = data
            w += 1
        base, words = TX_RING[ch]
        at = head[ch]
        while (value - at) & 0xFFFF:
            w0 = ring[ch].get(at % words)
            if w0 is None:
                raise Refusal(f'TX record header at {at} of channel {ch} was never written')
            length, interface = w0 & 0xFFFF, (w0 >> 16) & 0xF
            frame = bytearray()
            for k in range((length + 3) // 4):      # little-endian lanes, byte k at bits 8k (mbx_wire.h)
                frame += ring[ch].get((at + 2 + k) % words, 0).to_bytes(4, 'little')
            out.append((cycle, ch, interface, bytes(frame[:length])))
            at = (at + 2 + (length + 3) // 4) & 0xFFFF
        head[ch] = value
    return out


def causal(frame: bytes, command: int, descriptor_type: int, descriptor_index: int) -> bool:
    """An unsolicited AEM_RESPONSE (IEEE 1722.1-2021 7.5.2) of that command and descriptor."""
    return (len(frame) > 41 and frame[14] == 0xFB and frame[15] & 0xF == 1 and bool(frame[36] & 0x80)
            and int.from_bytes(frame[36:38], 'big') & 0x7FFF == command
            and int.from_bytes(frame[38:40], 'big') == descriptor_type
            and int.from_bytes(frame[40:42], 'big') == descriptor_index)


def fanout_end(found: dict[tuple[int, int], int | None]) -> int | None:
    """The last required recipient's commit ends a notification fan-out (FR_NFR.md 3.4.1)."""
    cycles = list(found.values())
    return None if not cycles or None in cycles else max(cycles)


class Grader:
    """One place for each rule a measurement rests on."""

    def __init__(self, log: Log) -> None:
        self.log = log

    # ---- the clock conversion: the CPU runs at cpu_hz, the bus at sys_hz ----
    def cpu_cycles(self, sys_cycles: int) -> int:
        """CPU clock cycles in an interval of system cycles, rounded up."""
        return -(-sys_cycles * self.log.cpu_hz // self.log.sys_hz)

    def ms(self, sys_cycles: int) -> float:
        """Milliseconds in an interval of system cycles."""
        return sys_cycles * 1000.0 / self.log.sys_hz

    def bus_cycles(self, cpu_cycles: int) -> int:
        """System cycles in an interval of CPU cycles (the clocks' edges are aligned)."""
        return cpu_cycles * self.log.sys_hz // self.log.cpu_hz

    def cpu_ms(self, cpu_cycles: int) -> float:
        """Milliseconds in an interval of CPU cycles."""
        return cpu_cycles * 1000.0 / self.log.cpu_hz

    # ---- the markers ----
    def start(self, probe: scenario.Probe, interface: int, after: int, before: int) -> int | None:
        """The system cycle the probe's input occurred, by its start marker."""
        kind, *args = probe.start.split(':')
        if kind == 'rxc':
            ch = int(args[0])
            # A probe's own frames carry its name; any other frame on the ring is not its input.
            hits = [c for c, k, i, tag, _ in self.log.rxc if after <= c < before and k == ch
                    and i in (interface, -1) and tag == probe.name]
        elif kind == 'pad':
            hits = [c for c, k, i in self.log.pads if after <= c < before and k == args[0] and i == interface]
        elif kind == 'entry':
            hits = [c for c, name in self.log.entries if after <= c < before and name == args[0]]
        elif kind == 'deadline':
            slot = int(args[0])
            hits = []
            for cycle, w in self.log.records:
                if after <= cycle < before and w[0] & 0xFF == EV_TIMER and (w[1] >> 16) & 0xFF == slot:
                    deadline = w[2]
                    if deadline not in self.log.ms:
                        raise Refusal(f'{probe.name}: the deadline {deadline} ms has no observed tick')
                    hits.append(self.log.ms[deadline])
                    break
        else:
            raise Refusal(f'{probe.name}: unknown start marker {probe.start}')
        return hits[0] if hits else None

    def recipients(self, spec: str, probe: scenario.Probe, start: int,
                   before: int) -> tuple[dict[tuple[int, int], int | None], list[tuple[int, int]]]:
        """Each required recipient's first notification commit (None if absent), and the
        recipients outside the probe's set that the same change notified."""
        ch, command, descriptor_type, descriptor_index = (int(v, 16) if k == 1 else int(v)
                                                          for k, v in enumerate(spec.split(':')[1:]))
        found: dict[tuple[int, int], int | None] = {r: None for r in probe.recipients}
        unexpected = []
        for c, k, i, fr in self.log.tx:
            if start <= c <= before and k == ch and causal(fr, command, descriptor_type, descriptor_index):
                key = (int.from_bytes(fr[26:34], 'big'), i)
                if key not in found:
                    unexpected.append(key)
                elif found[key] is None:
                    found[key] = c
        return found, unexpected

    def end(self, spec: str, probe: scenario.Probe, interface: int, start: int, before: int) -> int | None:
        """The system cycle one of the probe's required outputs was committed."""
        kind, *args = spec.split(':')
        if kind == 'notify':
            return fanout_end(self.recipients(spec, probe, start, before)[0])
        if kind in ('tx', 'resp', 'acmp_cmd', 'maap', 'adp'):
            ch = int(args[0])
            frames = [(c, fr) for c, k, i, fr in self.log.tx if start <= c <= before and k == ch and i == interface]
            if kind == 'tx':
                n = int(args[1]) if len(args) > 1 else 1
                return frames[n - 1][0] if len(frames) >= n else None
            if kind == 'resp':
                hits = [c for c, fr in frames if response_sequence(fr) == int(args[1], 16)]
            elif kind in ('maap', 'adp'):
                subtype = 0xFE if kind == 'maap' else 0xFA
                hits = [c for c, fr in frames if len(fr) > 16 and fr[14] == subtype and fr[15] & 0xF == int(args[1])]
            else:
                hits = [c for c, fr in frames if len(fr) > 16 and fr[14] == 0xFC
                        and fr[15] & 0xF == scenario.f.ACMP[args[1]]]
            return hits[0] if hits else None
        # An output committed in the cycle the next mark is set belongs to this probe.
        writes = [(c, w, v) for c, w, v in self.log.writes if start <= c <= before]
        if kind in ('arm', 'cancel', 'tmr'):
            slot = int(args[0])
            op = {'arm': 1, 'cancel': 2}.get(kind)
            hits = [c for c, w, v in writes if w == scenario.TMR_CMD_WORD and v & 0xFF == slot
                    and (op is None or v >> 30 == op)]
        elif kind in ('rxtail', 'pass_end'):
            hits = [c for c, w, _ in writes if w == scenario.ch_word(int(args[0]), 'RX_TAIL')]
            if kind == 'pass_end' and hits:
                taking = self.taking_pass(hits[0])
                if taking is None:
                    raise Refusal(f'{probe.name}: the release at {hits[0]} belongs to no work pass')
                hits = [self.pass_end(taking)]
        elif kind == 'pub':
            hits = [c for c, w, _ in writes if w == int(args[0])]
        else:
            raise Refusal(f'{probe.name}: unknown end marker {spec}')
        return hits[0] if hits else None

    # ---- the passes and the pass bound ----
    def pass_end(self, p: Pass) -> int:
        """The system cycle a work pass ended: its start plus its CPU cycles on the bus clock."""
        return p.start_sys + self.bus_cycles(p.cycles)

    def taking_pass(self, cycle: int) -> Pass | None:
        """The pass that made the write at cycle, or that ended at cycle (a pass_end)."""
        for p in self.log.passes:
            if any(c == cycle for c, _, _ in p.writes) or self.pass_end(p) == cycle:
                return p
        return None

    def pass_origin(self, start: int) -> int:
        """The start of the pass running at start; an unprinted, idle pass running there is
        charged the longest idle pass of its run."""
        for p in self.log.passes:
            if p.start_sys <= start < self.pass_end(p):
                return p.start_sys
            if p.start_sys > start:
                return start - self.bus_cycles(p.idle_before)
        raise Refusal('no pass is known to run at the input')

    def pass_bound(self, start: int, taking: Pass) -> int:
        """Bus cycles from the start of the pass running at start to the end of the taking pass.

        Whatever the input's phase in the pass running when it arrives, it is
        taken no later than the following pass, so with the same passes the
        interval cannot exceed this.
        """
        return self.pass_end(taking) - self.pass_origin(start)

    def window_passes(self, start: int, end: int) -> list[Pass]:
        """The work passes that ran during [start, end]."""
        return [p for p in self.log.passes if p.start_sys <= end and self.pass_end(p) >= start]

    # ---- the backlog at an input ----
    def ahead(self, probe: scenario.Probe, start: int) -> tuple[str, int]:
        """The ring the probe's input joined and how many records were ahead of it there:
        committed (or posted) before it and not yet released by the core."""
        kind, *args = probe.start.split(':')
        if kind == 'rxc':
            ch = int(args[0])
            sizes = [RX_HEADER_WORDS + (size + 3) // 4 for c, k, _, _, size in self.log.rxc if k == ch and c < start]
            tail = [v for c, w, v in self.log.writes if w == scenario.ch_word(ch, 'RX_TAIL') and c < start]
            released, total = unwrapped(tail), 0
            behind = 0
            for words in sizes:
                total += words
                behind += total > released
            return CHANNEL[ch], behind
        posted = sum(1 for c, _ in self.log.records if c < start)
        tail = [v for c, w, v in self.log.writes if w == scenario.EVT_TAIL_WORD and c < start]
        return 'events', posted - unwrapped(tail) // scenario.CONTRACT.ev_words


def unwrapped(values: list[int]) -> int:
    """The last of a 16-bit free-running index's values, counted from 0 at reset."""
    total, last = 0, 0
    for v in values:
        total += (v - last) & 0xFFFF
        last = v
    return total


def combine_ends(ends: list[int]) -> int:
    """A path ends when its last required output is committed (FR_NFR.md 3.4.1)."""
    return max(ends)


def verdicts(ms: float, probe: scenario.Probe) -> dict:
    """elapsed <= W + T_svc, and the family's ceiling plus W (FR_NFR.md 3.4.1)."""
    budget = scenario.T_SVC_MS + probe.wait_ms
    ceiling = scenario.CEILING_MS[probe.family] + probe.wait_ms
    return dict(t_svc_ms=budget, ceiling_ms=ceiling, within_t_svc=ms <= budget, within_ceiling=ms <= ceiling)


def response_sequence(frame: bytes) -> int | None:
    """The sequence_id of an ACMP response (8.2.1) or a solicited AECP response (9.2.1); else None."""
    if len(frame) > 63 and frame[14] == 0xFC and frame[15] & 1:
        return int.from_bytes(frame[62:64], 'big')
    if len(frame) > 37 and frame[14] == 0xFB and frame[15] & 0xF in (1, 7) and not frame[36] & 0x80:
        return int.from_bytes(frame[34:36], 'big')
    return None


def never_answered(grader: Grader, probe: scenario.Probe, row: dict, start: int) -> dict:
    """An admitted command its firmware took and never answered by the run's end: a measured
    finding whose time is a lower bound, fitting neither T_svc nor its ceiling (3.4.1)."""
    finish = max(int(grader.log.summary.get('sys', 0)), start)
    ring, ahead = grader.ahead(probe, start)
    return dict(row, status='measured', unanswered=True, start_sys=start, end_sys=finish, sys_cycles=finish - start,
                cpu_cycles=grader.cpu_cycles(finish - start), ms=round(grader.ms(finish - start), 5),
                wait_ms=probe.wait_ms, ring=ring, ahead=ahead, **dict(verdicts(grader.ms(finish - start), probe),
                                                                     within_t_svc=False, within_ceiling=False))


def owed_ahead(grader: Grader, probe: scenario.Probe, interface: int, start: int, end: int) -> list[int | None]:
    """The responses the probe's channel committed on its interface after its input and ahead
    of its own response, in commit order (None for a frame that is no response): a response
    with N frames owed ahead of it has exactly the N it owes (MAILBOX_SPLIT.md:757-762)."""
    ch = int(probe.start.split(':')[1])
    own = int(next(s for s in probe.ends if s.startswith('resp')).split(':')[2], 16)
    out = []
    for c, k, i, fr in grader.log.tx:
        if start < c <= end and k == ch and i == interface:
            if response_sequence(fr) == own:
                break
            out.append(response_sequence(fr))
    return out


def interface_of(name: str) -> int:
    """The AVB interface a probe's name ends with (.if<n>)."""
    match = re.search(r'\.if(\d+)$', name)
    return int(match.group(1)) if match else 0


def fan_out(grader: Grader, probe: scenario.Probe, start: int, before: int) -> str:
    """'' when every notification end reached exactly its recipients; else what was wrong."""
    for spec in probe.ends:
        if not spec.startswith('notify'):
            continue
        if not probe.recipients:
            raise Refusal(f'{probe.name}: a notification end needs its recipients')
        found, unexpected = grader.recipients(spec, probe, start, before)
        missing = [f'{ctl:016x}@if{i}' for (ctl, i), c in found.items() if c is None]
        if missing:
            return f'no notification to {missing}'
        if unexpected:
            return f'a notification to {[f"{ctl:016x}@if{i}" for ctl, i in unexpected]}, not a recipient'
    return ''


def grade_probe(grader: Grader, probe: scenario.Probe, mark: int, next_mark: int,
                marks: dict[str, int] | None = None) -> dict:
    """One probe's measured interval, its taking pass and its verdicts."""
    i = interface_of(probe.name)
    start = grader.start(probe, i, mark, next_mark)
    row = dict(probe=probe.name, row=probe.row, family=probe.family, interface=i,
               path=list(probe.path_key()))
    if start is None:
        return dict(row, status='no start', reason=f'no {probe.start} after the mark')
    wrong = fan_out(grader, probe, start, next_mark)
    if wrong.startswith('no notification'):
        return dict(row, status='no end', reason=wrong, start_sys=start)
    ends = [grader.end(spec, probe, i, start, next_mark) for spec in probe.ends]
    missing = [spec for spec, e in zip(probe.ends, ends) if e is None]
    if missing and probe.may_drop and all(spec.startswith('resp') for spec in missing):
        return never_answered(grader, probe, row, start)
    if missing:
        return dict(row, status='no end', reason=f'missing {missing}', start_sys=start)
    end = combine_ends(ends)
    elapsed = end - start
    ms = grader.ms(elapsed)
    taking = grader.taking_pass(end)
    ring, ahead = grader.ahead(probe, start)
    row.update(start_sys=start, end_sys=end, sys_cycles=elapsed, cpu_cycles=grader.cpu_cycles(elapsed),
               ms=round(ms, 5), wait_ms=probe.wait_ms, passes=len(grader.window_passes(start, end)),
               ring=ring, ahead=ahead, **verdicts(ms, probe))
    for spec in probe.ends:
        if spec.startswith('notify'):
            # Every recipient's commit, so the per-recipient cost: last less first, over the gaps.
            cycles = sorted(c for c in grader.recipients(spec, probe, start, next_mark)[0].values() if c is not None)
            row['fanout'] = dict(recipients=len(cycles), first_sys=cycles[0], last_sys=cycles[-1],
                                 per_recipient_cpu_cycles=grader.cpu_cycles(cycles[-1] - cycles[0])
                                 // max(1, len(cycles) - 1)) if cycles else dict(recipients=0)
    if probe.owed:
        row['owed_ahead'] = [f'{s:x}' if s is not None else '-' for s in owed_ahead(grader, probe, i, start, end)]
    if taking is not None:
        bound = grader.pass_bound(start, taking)
        row.update(bound_cpu_cycles=grader.cpu_cycles(bound), bound_ms=round(grader.ms(bound), 5),
                   bound_within_t_svc=verdicts(grader.ms(bound), probe)['within_t_svc'])
        row.update(pass_figures(taking))
    if probe.accesses is not None:
        row['model_accesses'] = probe.accesses
    if probe.also_from:
        origin = (marks or {}).get(probe.also_from)
        if origin is None or not start <= origin <= end:
            return dict(row, status='no origin', reason=f'mark {probe.also_from} is not inside the interval')
        row.update(also_from=probe.also_from, from_origin_cpu_cycles=grader.cpu_cycles(end - origin),
                   from_origin_ms=round(grader.ms(end - origin), 5))
    check = wrong or expectation(grader, probe, i, start, next_mark)
    owed = [f'{s:x}' for s in probe.owed]
    if not check and probe.owed and row['owed_ahead'] != owed:
        check = f'the responses committed ahead of it are {row["owed_ahead"]}, not the owed {owed}'
    if check:
        return dict(row, status='unexpected response', reason=check)
    row['status'] = 'measured'
    return row


REGIONS = ('rom', 'sram', 'mbx', 'flash', 'csr', 'other')


def pass_figures(taking: Pass) -> dict:
    """The taking pass's cycles, instructions, accesses, fetch share, regions and largest modules."""
    loads = sum(taking.count(f'load_{r}') for r in REGIONS)
    stores = sum(taking.count(f'store_{r}') for r in REGIONS)
    fetches = sum(taking.count(f'fetch_{r}') for r in REGIONS)
    return dict(pass_cycles=taking.cycles, pass_instr=taking.count('instr'),
                pass_mbx_accesses=taking.count('load_mbx') + taking.count('store_mbx'),
                pass_fetch_share=round(fetches / max(1, fetches + loads + stores), 4),
                pass_fetch_wait_share=round(sum(taking.wait(f'fetch_{r}') for r in REGIONS)
                                            / max(1, taking.cycles), 4),
                pass_regions={r: [taking.count(f'fetch_{r}'), taking.count(f'load_{r}'),
                                  taking.count(f'store_{r}')] for r in REGIONS
                              if taking.count(f'fetch_{r}') + taking.count(f'load_{r}')
                              + taking.count(f'store_{r}')},
                pass_modules=dict(sorted(taking.modules.items(), key=lambda kv: -kv[1])[:6]))


def expectation(grader: Grader, probe: scenario.Probe, interface: int, start: int, before: int) -> str:
    """'' when the response the probe expects left; else what was wrong."""
    if not probe.expect:
        return ''
    kind, *args = probe.expect.split(':')
    frames = [fr for c, _, i, fr in grader.log.tx if start <= c <= before and i == interface]
    if kind in ('acmp_status', 'acmp_type'):
        want = scenario.f.ACMP[args[0]]
        got = [w for w in frames if len(w) > 16 and w[14] == 0xFC and w[15] & 0xF == want]
        if not got:
            return f'no {args[0]} frame'
        if kind == 'acmp_status' and got[0][16] >> 3 != int(args[1]):
            return f'{args[0]} status {got[0][16] >> 3}'
        return ''
    def sent(subtype: int, types: tuple[int, ...]) -> bool:
        """A frame of that AVTP subtype and one of those message types left."""
        return any(len(w) > 16 and w[14] == subtype and w[15] & 0xF in types for w in frames)
    if kind == 'aecp_response':
        return '' if sent(0xFB, (1, 7)) else 'no AECP response'
    if kind == 'adp_available':
        return '' if sent(0xFA, (0,)) else 'no ENTITY_AVAILABLE'
    if kind == 'adp_departing':
        return '' if sent(0xFA, (1,)) else 'no ENTITY_DEPARTING'
    if kind == 'maap_type':
        return '' if sent(0xFE, (int(args[0]),)) else f'no MAAP type {args[0]}'
    if kind == 'srp_frames':
        return '' if any(w[12:14] in (b'\x22\xea', b'\x88\xf5') for w in frames) else 'no MRPDU'
    raise Refusal(f'{probe.name}: unknown expectation {probe.expect}')


def refuse_run(log: Log, group: scenario.Group) -> None:
    """A simulation that did not finish, or whose CPU trapped or saw a bus error, measures nothing."""
    if log.result != 'PASS' or log.errors:
        raise Refusal(f'{group.name}: the simulation did not complete: {log.errors or log.result}')
    if log.traps:
        raise Refusal(f'{group.name}: the CPU trapped or saw a bus error: {log.traps[:3]}')


def population(log: Log, start: int, end: int) -> dict[str, int]:
    """The records each receive channel committed, and the GM and LINK events posted, in [start, end]."""
    out = {name: 0 for name in [*CHANNEL.values(), 'GM', 'LINK']}
    for c, ch, *_ in log.rxc:
        if start <= c <= end:
            out[CHANNEL[ch]] += 1
    for c, words in log.records:
        name = EVENT.get(words[0] & 0xFF)
        if start <= c <= end and name in out:
            out[name] += 1
    return out


def room(channel: str) -> int:
    """The records of the defined load's size the channel's receive ring holds (mailbox.yaml)."""
    ch = next(c for c in CONTRACT.channels if c.name == channel)
    return ch.rx_words // (RX_HEADER_WORDS + (LOAD_FRAME_BYTES[channel] + 3) // 4)


def defined_load(name: str) -> dict[str, int]:
    """The population a composed row's window must commit, from the contract alone and never
    from the stimulus's declaration (FR_NFR.md 3.4.1: backlog consumes T_svc).

    Every receive channel carries what one instant admits: its token bucket's burst, unless
    its ring holds fewer records of the load's size (KL_mbx_rx.sv). The refill leg's ADP fills
    the ring's room. Grandmaster changes fill the event ring but the row's own event, which in
    'backlog' is the LINK change. The fixture's short window has one record a channel and two
    changes.
    """
    if name not in COMPOSED_ROWS:
        raise Refusal(f'{name}: no defined composed load')
    if name == 'fixture':
        return {**{ch.name: 1 for ch in CONTRACT.channels}, 'GM': 2}
    load = {ch.name: min(ch.burst, room(ch.name)) for ch in CONTRACT.channels}
    load['GM'] = CONTRACT.evt_words // CONTRACT.ev_words - 1
    if name == 'backlog':
        load['LINK'] = 1
    if name == 'backlog-adp-refill':
        load['adp'] = room('adp')
    return load


def check_load(group: scenario.Group, got: dict[str, int], refused: list[tuple[str, int]]) -> None:
    """The composed window must commit exactly its row's defined load: a refused or missing
    record, a channel left out of the stimulus, or one record too many, is not the composed
    maximum."""
    defined = defined_load(group.name)
    want = {name: defined.get(name, 0) for name in got}
    if got != want:
        raise Refusal(f'{group.name}: the composed window committed {got}, its defined load is {want}; '
                      f'refused frames {refused[:8]}')


def releases(log: Log, ch: int) -> list[tuple[int, int, int | None]]:
    """Each record the channel committed, in order: its commit cycle, its interface and the
    cycle of the RX_TAIL write that released its last word, or None if no write did."""
    tail_word = scenario.ch_word(ch, 'RX_TAIL')
    tails = [(c, v) for c, w, v in log.writes if w == tail_word]
    out: list[tuple[int, int, int | None]] = []
    end = released = last = n = 0
    at = None
    for c, k, interface, _, size in log.rxc:
        if k != ch:
            continue
        end += RX_HEADER_WORDS + (size + 3) // 4
        while released < end and n < len(tails):
            at, value = tails[n]
            released += (value - last) & 0xFFFF
            last = value
            n += 1
        out.append((c, interface, at if released >= end else None))
    return out


def unreleased(log: Log, start: int, end: int) -> dict[str, int]:
    """Per channel, the records committed in [start, end] that no release had passed by end."""
    out = {}
    for ch, name in CHANNEL.items():
        left = sum(1 for c, _, r in releases(log, ch) if start <= c <= end and (r is None or r > end))
        if left:
            out[name] = left
    return out


def served(grader: Grader, taking: Pass, released: int) -> int:
    """A released record's service end: the end of the pass whose RX_TAIL write released it."""
    return grader.pass_end(taking)


#: Each receive channel's 3.4.1 family, for its records' service under a composed load.
SERVICE_FAMILY = {'adp': 'adp', 'acmp': 'acmp', 'aecp': 'aecp', 'maap': 'maap', 'srp': 'srp'}


def service(grader: Grader, group: scenario.Group, start: int, end: int) -> list[dict]:
    """Each loaded channel's first and last record of the composed window [start, end], from
    its receive commit to the end of the pass that released it: the handler runs after the
    release, inside that pass (ctrl_loop.c service_rx), and the SRP rows end there too.

    A record released after the window closed is marked out of the window. A record no
    release reached by the run's end is starved: its row carries the time it had waited, a
    lower bound, and fits neither T_svc nor its ceiling. The records ahead of a record are its
    channel's earlier records that no release had passed at its commit.
    """
    finish = max(int(grader.log.summary.get('sys', 0)), end)
    rows = []
    for ch, name in CHANNEL.items():
        records = releases(grader.log, ch)
        inside = [n for n, r in enumerate(records) if start <= r[0] <= end]
        if not inside:
            continue
        for which, n in (('first', inside[0]), ('last', inside[-1])):
            commit, interface, released = records[n]
            probe = scenario.Probe(f'{group.name}.service.{name}.{which}.if{interface}',
                                   f'{name.upper()} record released under the composed load, {which}',
                                   SERVICE_FAMILY[name], f'rxc:{ch}', [], path=f'service.{name}.{which}')
            row = dict(probe=probe.name, row=probe.row, family=probe.family, interface=interface,
                       path=list(probe.path_key()), start_sys=commit, wait_ms=0.0, ring=name,
                       ahead=sum(1 for _, _, r in records[:n] if r is None or r > commit),
                       in_window=released is not None and released <= end, starved=released is None)
            if released is None:
                stop = finish
            else:
                taking = grader.taking_pass(released)
                if taking is None:
                    raise Refusal(f'{probe.name}: the release at {released} belongs to no work pass')
                stop = served(grader, taking, released)
                row.update(pass_figures(taking))
            row.update(end_sys=stop, sys_cycles=stop - commit, cpu_cycles=grader.cpu_cycles(stop - commit),
                       ms=round(grader.ms(stop - commit), 5), passes=len(grader.window_passes(commit, stop)),
                       **verdicts(grader.ms(stop - commit), probe))
            if released is None:
                row.update(within_t_svc=False, within_ceiling=False)
            rows.append(dict(row, status='measured'))
    return rows


def composed_passes(log: Log, start: int, end: int) -> list[Pass]:
    """The work passes that start inside the composed window."""
    return [p for p in log.passes if start <= p.start_sys <= end]


def composed(grader: Grader, group: scenario.Group, marks: dict[str, int]) -> dict | None:
    """The longest pass that starts inside the composed window, whose committed population must
    be the row's defined load exactly (MAAP and SRP included).

    serviced says whether the window released every record of that load: a window that
    closed on a starved channel measured passes without that channel's work, so its longest
    pass is a lower bound, and unreleased names the records. The composed maximum is the
    longest over every backlog row's window, a lower bound while one is not serviced
    (run.composed_maximum).
    """
    if 'composed' not in marks or 'composed_end' not in marks:
        if group.load or group.name in COMPOSED_ROWS:
            raise Refusal(f'{group.name}: the load has no composed window')
        return None
    start, end = marks['composed'], marks['composed_end']
    got = population(grader.log, start, end)
    check_load(group, got, [(tag, size) for c, _, tag, size in grader.log.refused if start <= c <= end])
    inside = composed_passes(grader.log, start, end)
    if not inside:
        raise Refusal(f'{group.name}: no work pass starts inside the composed window')
    top = max(inside, key=lambda p: p.cycles)
    left = unreleased(grader.log, start, end)
    return dict(cycles=top.cycles, ms=round(grader.cpu_ms(top.cycles), 5), instr=top.count('instr'),
                passes=len(inside), start_sys=top.start_sys, modules=top.modules, population=got,
                admission=group.admission, serviced=not left, unreleased=left,
                window_ms=round(grader.ms(end - start), 5))


def grade(text: str, group: scenario.Group, sys_hz: int, cpu_hz: int) -> dict:
    """A group's log: every probe, its passes and its run evidence. Refuses a log that did not finish."""
    log = parse(text, sys_hz, cpu_hz)
    refuse_run(log, group)
    timeouts = [s for _, s in log.steps if s.endswith('TIMEOUT')]
    grader = Grader(log)
    marks = {name: cycle for cycle, name in log.marks}
    order = sorted(log.marks)
    rows = []
    for probe in group.probes:
        if probe.name not in marks:
            raise Refusal(f'{group.name}: probe {probe.name} was never marked')
        at = marks[probe.name]
        if probe.until:
            if probe.until not in marks:
                raise Refusal(f'{group.name}: probe {probe.name} is bounded by an unmarked {probe.until}')
            limit = marks[probe.until]
        else:
            later = [c for c, _ in order if c > at]
            limit = later[0] if later else 1 << 62
        rows.append(grade_probe(grader, probe, at, limit, marks))
    window = composed(grader, group, marks)
    if window is not None:
        rows += service(grader, group, marks['composed'], marks['composed_end'])
    # The script's end closes the pass in progress: the run it flushes holds that cut pass, so
    # neither its minimum nor its maximum is a whole idle pass's.
    whole = log.idle[:-1] if log.cut_idle else log.idle
    idle_max = max((m for _, _, m in whole), default=0)
    idle_min = min((m for _, m, _ in whole if m), default=0)
    worst = max(log.passes, key=lambda p: p.cycles, default=None)
    return dict(group=group.name, probes=rows, timeouts=timeouts,
                passes=dict(count=int(log.summary.get('passes', 0)), work=len(log.passes),
                            idle_min=idle_min, idle_max=idle_max,
                            worst=dict(cycles=worst.cycles, ms=round(grader.cpu_ms(worst.cycles), 5),
                                       instr=worst.count('instr'), start_sys=worst.start_sys,
                                       modules=worst.modules) if worst else None,
                            composed=window),
                summary=log.summary, modules=log.modules, code=log.code)
