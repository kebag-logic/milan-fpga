# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Read a group's observation log and grade every probe against T_svc and its ceiling.

The clock ratio, the markers and the deadlines live in one place each
(Grader.cpu_cycles, Grader.start/end, scenario.T_SVC_MS and CEILING_MS), so
the self-test can mutate each of them and require a named failure.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import scenario

TX_RING = {n: (ch.tx_base // 4, ch.tx_words) for n, ch in enumerate(scenario.CONTRACT.channels)}
EV_TIMER, EV_LINK, EV_GM, EV_TICK = (next(e.value for e in scenario.CONTRACT.event_types if e.name == name)
                                     for name in ('TIMER', 'LINK', 'GM', 'TICK'))


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
    rxc: list[tuple[int, int, int, str]] = field(default_factory=list)  # cycle, channel, interface, tag
    pads: list[tuple[int, str, int]] = field(default_factory=list)
    records: list[tuple[int, list[int]]] = field(default_factory=list)
    writes: list[tuple[int, int, int]] = field(default_factory=list)
    tx: list[tuple[int, int, int, bytes]] = field(default_factory=list)  # cycle, channel, interface, frame
    wire: list[tuple[int, int, int, bytes]] = field(default_factory=list)
    passes: list[Pass] = field(default_factory=list)
    idle: list[tuple[int, int, int]] = field(default_factory=list)
    steps: list[tuple[int, str]] = field(default_factory=list)
    summary: dict[str, str] = field(default_factory=dict)
    modules: dict[str, int] = field(default_factory=dict)
    code: dict[str, str] = field(default_factory=dict)
    traps: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    result: str = ''


def parse(text: str, sys_hz: int, cpu_hz: int) -> Log:
    """Every observation line; a line the testbench does not print is refused."""
    log = Log(sys_hz, cpu_hz)
    pending_rx: list[tuple[int, str]] = []   # interface and tag of frames whose last byte has passed
    rxs = (0, '-')
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
            rxs = (int(rest[1]), rest[3] if len(rest) > 3 else '-')
        elif kind == 'RXE':
            pending_rx.append((*rxs, int(rest[0])))
        elif kind == 'RXC':
            # The commit belongs to the oldest frame whose last byte passed and that was not refused.
            cycle = int(rest[0])
            while len(pending_rx) > 1 and pending_rx[0][2:] and pending_rx[0][2] < cycle - 64:
                pending_rx.pop(0)
            interface, tag = pending_rx.pop(0)[:2] if pending_rx else (-1, '-')
            log.rxc.append((cycle, int(rest[1]), interface, tag))
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
            log.wire.append((int(rest[0]), int(rest[1]), int(rest[2]), bytes.fromhex(rest[3])))
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
        elif kind == 'IDLE':
            # The testbench flushes a run of idle passes just before the work pass that ends it.
            log.idle.append(tuple(int(v) for v in rest))
            idle_max = int(rest[2])
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

    # ---- the markers ----
    def start(self, probe: scenario.Probe, interface: int, after: int, before: int) -> int | None:
        """The system cycle the probe's input occurred, by its start marker."""
        kind, *args = probe.start.split(':')
        if kind == 'rxc':
            ch = int(args[0])
            # A probe's own frames carry its name; any other frame on the ring is not its input.
            hits = [c for c, k, i, tag in self.log.rxc if after <= c < before and k == ch
                    and i in (interface, -1) and tag == probe.name]
        elif kind == 'pad':
            hits = [c for c, k, i in self.log.pads if after <= c < before and k == args[0] and i == interface]
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

    def end(self, spec: str, probe: scenario.Probe, interface: int, start: int, before: int) -> int | None:
        """The system cycle one of the probe's required outputs was committed."""
        kind, *args = spec.split(':')
        if kind in ('tx', 'resp', 'notify', 'acmp_cmd', 'maap'):
            ch = int(args[0])
            frames = [(c, fr) for c, k, i, fr in self.log.tx if start <= c <= before and k == ch and i == interface]
            if kind == 'tx':
                n = int(args[1]) if len(args) > 1 else 1
                return frames[n - 1][0] if len(frames) >= n else None
            if kind == 'resp':
                hits = [c for c, fr in frames if response_sequence(fr) == int(args[1], 16)]
            elif kind == 'notify':
                # A notification goes to each registered controller, on that controller's interface.
                hits = [c for c, k, _, fr in self.log.tx if start <= c <= before and k == ch
                        and len(fr) > 37 and fr[14] == 0xFB and fr[36] & 0x80]
            elif kind == 'maap':
                hits = [c for c, fr in frames if len(fr) > 16 and fr[14] == 0xFE and fr[15] & 0xF == int(args[1])]
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
                hits = [int(taking.start_sys + self.log.sys_hz / self.log.cpu_hz * taking.cycles)]
        elif kind == 'pub':
            hits = [c for c, w, _ in writes if w == int(args[0])]
        else:
            raise Refusal(f'{probe.name}: unknown end marker {spec}')
        return hits[0] if hits else None

    def taking_pass(self, cycle: int) -> Pass | None:
        """The pass that made the write at cycle, or that ended at cycle (a pass_end)."""
        ratio = self.log.sys_hz / self.log.cpu_hz
        for p in self.log.passes:
            if any(c == cycle for c, _, _ in p.writes) or int(p.start_sys + ratio * p.cycles) == cycle:
                return p
        return None

    def pass_bound(self, start: int, taking: Pass) -> int:
        """Bus cycles from the start of the pass running at start to the end of the taking pass.

        Whatever the input's phase in the pass running when it arrives, it is
        taken no later than the following pass, so with the same passes the
        interval cannot exceed this. An unprinted, idle pass running at start
        is charged the longest idle pass of its run.
        """
        ratio = self.log.sys_hz / self.log.cpu_hz
        origin = None
        for p in self.log.passes:
            if p.start_sys <= start < p.start_sys + ratio * p.cycles:
                origin = p.start_sys
            elif p.start_sys > start:
                if origin is None:
                    origin = start - int(ratio * p.idle_before)
                break
        if origin is None:
            raise Refusal('no pass is known to run at the input')
        return int(taking.start_sys + ratio * taking.cycles) - origin

    def window_passes(self, start: int, end: int) -> list[Pass]:
        """The work passes that ran during [start, end]."""
        ratio = self.log.sys_hz / self.log.cpu_hz
        return [p for p in self.log.passes if p.start_sys <= end and p.start_sys + ratio * p.cycles >= start]


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


def interface_of(name: str) -> int:
    """The AVB interface a probe's name ends with (.if<n>)."""
    match = re.search(r'\.if(\d+)$', name)
    return int(match.group(1)) if match else 0


def grade_probe(grader: Grader, probe: scenario.Probe, mark: int, next_mark: int,
                marks: dict[str, int] | None = None) -> dict:
    """One probe's measured interval, its taking pass and its verdicts."""
    i = interface_of(probe.name)
    start = grader.start(probe, i, mark, next_mark)
    row = dict(probe=probe.name, row=probe.row, family=probe.family, interface=i)
    if start is None:
        return dict(row, status='no start', reason=f'no {probe.start} after the mark')
    ends = [grader.end(spec, probe, i, start, next_mark) for spec in probe.ends]
    missing = [spec for spec, e in zip(probe.ends, ends) if e is None]
    if missing:
        return dict(row, status='no end', reason=f'missing {missing}', start_sys=start)
    end = combine_ends(ends)
    elapsed = end - start
    ms = grader.ms(elapsed)
    taking = grader.taking_pass(end)
    row.update(start_sys=start, end_sys=end, sys_cycles=elapsed, cpu_cycles=grader.cpu_cycles(elapsed),
               ms=round(ms, 5), wait_ms=probe.wait_ms, passes=len(grader.window_passes(start, end)),
               **verdicts(ms, probe))
    if taking is not None:
        bound = grader.pass_bound(start, taking)
        row.update(bound_cpu_cycles=grader.cpu_cycles(bound), bound_ms=round(grader.ms(bound), 5),
                   bound_within_t_svc=verdicts(grader.ms(bound), probe)['within_t_svc'])
        loads = sum(taking.count(f'load_{r}') for r in REGIONS)
        stores = sum(taking.count(f'store_{r}') for r in REGIONS)
        fetches = sum(taking.count(f'fetch_{r}') for r in REGIONS)
        row.update(pass_cycles=taking.cycles, pass_instr=taking.count('instr'),
                   pass_mbx_accesses=taking.count('load_mbx') + taking.count('store_mbx'),
                   pass_fetch_share=round(fetches / max(1, fetches + loads + stores), 4),
                   pass_fetch_wait_share=round(sum(taking.wait(f'fetch_{r}') for r in REGIONS)
                                               / max(1, taking.cycles), 4),
                   pass_regions={r: [taking.count(f'fetch_{r}'), taking.count(f'load_{r}'),
                                     taking.count(f'store_{r}')] for r in REGIONS
                                 if taking.count(f'fetch_{r}') + taking.count(f'load_{r}')
                                 + taking.count(f'store_{r}')},
                   pass_modules=dict(sorted(taking.modules.items(), key=lambda kv: -kv[1])[:6]))
    if probe.accesses is not None:
        row['model_accesses'] = probe.accesses
    if probe.also_from:
        origin = (marks or {}).get(probe.also_from)
        if origin is None or not start <= origin <= end:
            return dict(row, status='no origin', reason=f'mark {probe.also_from} is not inside the interval')
        row.update(also_from=probe.also_from, from_origin_cpu_cycles=grader.cpu_cycles(end - origin),
                   from_origin_ms=round(grader.ms(end - origin), 5))
    check = expectation(grader, probe, i, start, next_mark)
    if check:
        return dict(row, status='unexpected response', reason=check)
    row['status'] = 'measured'
    return row


REGIONS = ('rom', 'sram', 'mbx', 'flash', 'csr', 'other')


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
    if kind == 'maap_type':
        return '' if sent(0xFE, (int(args[0]),)) else f'no MAAP type {args[0]}'
    if kind == 'srp_frames':
        return '' if any(w[12:14] in (b'\x22\xea', b'\x88\xf5') for w in frames) else 'no MRPDU'
    raise Refusal(f'{probe.name}: unknown expectation {probe.expect}')


def grade(text: str, group: scenario.Group, sys_hz: int, cpu_hz: int) -> dict:
    """A group's log: every probe, its passes and its run evidence. Refuses a log that did not finish."""
    log = parse(text, sys_hz, cpu_hz)
    if log.result != 'PASS' or log.errors:
        raise Refusal(f'{group.name}: the simulation did not complete: {log.errors or log.result}')
    if log.traps:
        raise Refusal(f'{group.name}: the CPU trapped or saw a bus error: {log.traps[:3]}')
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
    idle_max = max((m for _, _, m in log.idle), default=0)
    # The script's end closes the pass in progress; a zero-length one is that, not an idle pass.
    idle_min = min((m for _, m, _ in log.idle if m), default=0)
    worst = max(log.passes, key=lambda p: p.cycles, default=None)
    composed = None
    if 'composed' in marks and 'composed_end' in marks:
        inside = [p for p in log.passes if marks['composed'] <= p.start_sys <= marks['composed_end']]
        if inside:
            top = max(inside, key=lambda p: p.cycles)
            composed = dict(cycles=top.cycles, ms=round(top.cycles * 1000.0 / cpu_hz, 5),
                            instr=top.count('instr'), passes=len(inside), modules=top.modules)
    return dict(group=group.name, probes=rows, timeouts=timeouts,
                passes=dict(count=int(log.summary.get('passes', 0)), work=len(log.passes),
                            idle_min=idle_min, idle_max=idle_max,
                            worst=dict(cycles=worst.cycles, ms=round(worst.cycles * 1000.0 / cpu_hz, 5),
                                       instr=worst.count('instr'), start_sys=worst.start_sys,
                                       modules=worst.modules) if worst else None,
                            composed=composed),
                summary=log.summary, modules=log.modules, code=log.code)
