# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""THE 100 Mb/s EGRESS: the census's commits through the shipping transmit queue at the link rate.

PR #1020's 100 Mb/s ruling (comment 7216971645) makes FR_NFR 3.4.1's `T_egress` a held row at 100 Mb/s, and #1004
carries its items 2(a) and 2(b) as a merge gate (comment 7216972073):

(a) every commit's free-space test keeps its census outcome. The firmware reads TX_TAIL in three places, not only the
    free-space test: `mbx_tx_begin` (sw/firmware/ctrl/mbx/mbx.c), AECP's completions in its poll
    (sw/firmware/ctrl/aecp/aecp_mbx.c: a counter notice's next time and an accepted REBOOT's last cookie) and REBOOT's
    drain (sw/firmware/ctrl/plat/ctrl_plat.c, `drained`). A replay of the instant-egress census through this queue
    changes the free-space outcome in 11 of its 159 cases, so by the ruling's item 3 the census runs with egress
    drained at link rate through the queue (egress_queue.hpp decides the mailbox's ready), and every one of the three
    reads is the firmware's own against the link-rate tail. The grade checks the testbench's queue against this one:
    the replay of each case's commits reproduces every departure the testbench printed (EGRESS) within AGREE_PS.
(b) the largest commit-to-last-octet wait plus 5 %, plus the fixed path measured on the shipping chain at the MII rate,
    is at most BOUND_US. The wait is each record's own, from its TX_HEAD commit (TXC) to its last octet; a record
    whose wait meets a held egress (a `txready 0` window, the held-egress rows' ledger, egress_ledger.py) and every
    record queued behind it until the queue empties are left to that ledger. The shape's SR stream is swept over
    PHASES phases of its period by the replay; the testbench runs phase 0. Its gPTP frames are a burst every
    GPTP_PERIOD_PS, and the grade adds the burst's whole wire time to the largest wait, so a burst at any phase is
    bounded. The fixed path, the converted MII chain's own latency from its boundary to its last octet less the
    frame's wire time, is MII_FIXED_NS (egress_fixed.py measures it again).

Every queue parameter is read from its source (`params`). `--selftest` plants each defect the grade must catch.
`--structural` prints the AECP admission burst's figures: a notice's 16 registrations at the largest frame.

usage: python3 -I egress_mii.py RESULTS... | --selftest | --structural
"""

from __future__ import annotations

import dataclasses
import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOC = ROOT / 'sw/litex/milan_soc.py'
DATAPATH = ROOT / 'hdl/milan/milan_datapath.sv'
CONTRACT = ROOT / 'sw/firmware/ctrl/mbx/mbx_contract.h'
CONFIGS = ROOT / 'configs'

#: The bound (b) holds the wait to, us, and the ruling's margin on the largest wait.
BOUND_US, MARGIN = 1000, 1.05
#: The replay's SR phases, each 1/PHASES of the period apart; the testbench runs phase 0.
PHASES = 8
#: How far the replay's departures may sit from the testbench's, ps: the two models agree to the datapath cycle, and
#: the mailbox's head is visible to its merge one cycle after the commit the testbench prints.
AGREE_PS = 200_000
#: KL_mbx_tx (hdl/milan/mailbox/KL_mbx_tx.sv): a record committed at cycle c is pending at c + 1; from IDLE its first
#: byte is offered after IDLE, the scan's N_CH + 1 steps, PICK, W0, W1 and LOAD; a LOAD follows every fourth byte; DONE
#: and IDLE follow the last.
MBX_VISIBLE, MBX_LEAD, MBX_AFTER = 1, 11, 2
#: The byte crossing's latency in datapath cycles: LiteX's AsyncFIFOBuffered, two synchronizer stages and its output
#: register (milan_soc._axis_dp_cdc, buffered=True).
CROSS_DP = 3
#: The SR stream's frame: destination, source, 802.1Q tag and EtherType (18), the AAF header (24, IEEE 1722-2016
#: 7.3), and the samples of one class A interval (125 us, 6 at 48 kHz) at 32 bits a channel (Milan v1.2 6.4).
SR_HEADER, AAF_HEADER, SAMPLE_BYTES, SR_PERIOD_PS = 18, 24, 4, 125_000_000
#: gPTP's frames, each a 14-byte Ethernet header and its message (IEEE 802.1AS-2020 11.4, 10.6, 10.5.3.2.8): Sync
#: 44, Follow_Up 76, Announce 76 with a one-entry path trace, Pdelay_Req, Pdelay_Resp and Pdelay_Resp_Follow_Up 54,
#: Signaling 60. All of them every 125 ms, the Sync interval, though only Sync and Follow_Up come that often.
GPTP_MESSAGES, ETH_HEADER, GPTP_PERIOD_PS = (44, 76, 76, 54, 54, 54, 60), 14, 125_000_000_000
#: The converted MII chain's fixed path, ns: from its boundary's last beat to the frame's last octet, less that
#: frame's wire time, the most over every length and clock phase egress_fixed.py runs.
MII_FIXED_NS = 320
#: The AECP admission burst (aecp.h): a notice's recipients, the registrations of one interface, at its largest frame.
AECP_CH, AECP_RECIPIENTS, AECP_FRAME = 2, 16, 1514


@dataclasses.dataclass(frozen=True)
class Params:
    """The queue below the mailbox, field for field EgressParams in egress_queue.hpp."""
    sys_ps: int
    dp_ps: int
    octet_ps: int
    lane_bytes: int
    cross_dp: int
    gap_dp: int
    sf_beats: int
    sf_frames: int
    preamble: int
    fcs: int
    gap_octets: int
    min_frame: int
    sr_bytes: tuple
    sr_period_ps: int
    gptp_bytes: tuple
    gptp_period_ps: int
    ring_words: tuple

    def line(self) -> str:
        """The EGRESSQ line egress_queue.hpp prints for these parameters."""
        return (f'EGRESSQ sys_ps={self.sys_ps} dp_ps={self.dp_ps} octet_ps={self.octet_ps} lane={self.lane_bytes} '
                f'cross={self.cross_dp} gap={self.gap_dp} sf={self.sf_beats}/{self.sf_frames} frame={self.preamble}/'
                f'{self.fcs}/{self.gap_octets}/{self.min_frame} sr={len(self.sr_bytes)}/{self.sr_period_ps} '
                f'gptp={len(self.gptp_bytes)}/{self.gptp_period_ps}')

    def wire_ps(self, length: int) -> int:
        """A frame's preamble, padded bytes and FCS on the wire, ps."""
        return (self.preamble + max(length, self.min_frame) + self.fcs) * self.octet_ps


def soc_constant(name: str, text: str) -> list[int]:
    """The integer terms of one module-level constant of milan_soc.py, in source order."""
    found = re.search(rf'^{name} = ([0-9 +]+)$', text, re.M)
    if not found:
        raise ValueError(f'milan_soc.py states no {name}')
    return [int(t) for t in found.group(1).split('+')]


def link_mbps(shape: str) -> int | None:
    """The shape's PHY rate, Mb/s, when it is a 100 Mb/s MII point; None at a gigabit point."""
    phy = yaml.safe_load((CONFIGS / f'{shape}.yaml').read_text())['board']['constraints']['phy']
    if phy == 'mii-100':
        return 100
    if phy == 'gmii-1g':
        return None
    raise ValueError(f'{shape}: an unknown PHY {phy}')


def sr_frames(shape: str) -> tuple:
    """Each talker's frame of one class A interval, bytes."""
    cfg = yaml.safe_load((CONFIGS / f'{shape}.yaml').read_text())
    samples = cfg['clocking']['sampling_rate_hz'] * SR_PERIOD_PS // 10**12
    return tuple(SR_HEADER + AAF_HEADER + t['channels'] * samples * SAMPLE_BYTES for t in cfg['streams']['talkers'])


def params(spec: dict) -> Params | None:
    """The queue at the build's point, each figure from its source; None at a gigabit point, whose egress the
    testbench leaves instant."""
    mbps = link_mbps(spec['shape'])
    if mbps is None:
        return None
    soc = SOC.read_text()
    gap = re.search(r'tx_ifg_gasket\s*#\(.*?\.GAP_CYCLES\((\d+)\)\)\s*ctl_ifg', DATAPATH.read_text(), re.S)
    if not gap:
        raise ValueError('milan_datapath.sv: no ctl_ifg gasket with a GAP_CYCLES')
    pad_less_fcs, fcs, preamble, ifg = soc_constant('_ETH_FRAME_OVERHEAD_OCTETS', soc)
    contract = CONTRACT.read_text()
    names = re.search(r'#define MBX_CH_TX_WORDS_TBL \{([^}]*)\}', contract).group(1).split(',')
    words = tuple(int(re.search(rf'#define {n.strip()} (\d+)u', contract).group(1)) for n in names)
    return Params(sys_ps=10**12 // spec['sys_hz'], dp_ps=10**12 // spec['milan_hz'], octet_ps=8 * 10**6 // mbps,
                  lane_bytes=soc_constant('_AXIS_CDC_DEPTH', soc)[0] + 1, cross_dp=CROSS_DP,
                  gap_dp=int(gap.group(1)) + 1, sf_beats=soc_constant('_MAC_TX_SF_PAYLOAD_DEPTH', soc)[0],
                  sf_frames=soc_constant('_MAC_TX_SF_PARAM_DEPTH', soc)[0], preamble=preamble, fcs=fcs,
                  gap_octets=ifg, min_frame=pad_less_fcs, sr_bytes=sr_frames(spec['shape']),
                  sr_period_ps=SR_PERIOD_PS, gptp_bytes=tuple(ETH_HEADER + m for m in GPTP_MESSAGES),
                  gptp_period_ps=GPTP_PERIOD_PS, ring_words=words)


def header_lines(spec: dict) -> list[str]:
    """budget_config.hpp's egress lines: whether the point drains at link rate, and its queue."""
    p = params(spec)
    if p is None:
        return ['constexpr bool egress_link = false;', 'inline EgressParams egress_params() { return {}; }']
    fields = [f'p.{f.name} = {getattr(p, f.name)}u;' for f in dataclasses.fields(Params)
              if isinstance(getattr(p, f.name), int)]
    lists = [f'p.{n} = {{{", ".join(f"{b}u" for b in getattr(p, n))}}};' for n in ('sr_bytes', 'gptp_bytes')]
    return ['constexpr bool egress_link = true;',
            'inline EgressParams egress_params() { EgressParams p; ' + ' '.join(fields + lists) + ' return p; }']


class Queue:
    """egress_queue.hpp's EgressQueue, cycle for cycle, with quiet stretches crossed in one step."""

    def __init__(self, p: Params, phase_ps: int = 0) -> None:
        self.p = p
        self.lane: list = []
        self.others: list = []
        self.fifo: list = []
        self.next_dp = self.gap_until = self.wire_free = self.used = self.beats = self.other_left = 0
        self.sr_next, self.gptp_next = phase_ps, 0
        self.beat_bytes = self.frame_bytes = 0
        self.beat_ready = self.beat_last = False
        self.frame: tuple = (0, 0, 0)
        self.lock = self.last = None
        self.departed: list = []

    def ready(self) -> bool:
        """Whether the crossing takes a mailbox byte at the next edge."""
        return len(self.lane) < self.p.lane_bytes

    def take(self, sys: int, last: bool, ch: int) -> None:
        """A mailbox byte taken at sys cycle sys."""
        self.lane.append((sys * self.p.sys_ps + self.p.cross_dp * self.p.dp_ps, last, ch, sys))

    def advance(self, until: int) -> None:
        """Every datapath cycle up to ps until. A quiet queue steps to its next arrival at once, and an SR or gPTP
        frame entering a FIFO with room for it, the control lane empty, takes its beats but the last in one step: the
        cycles cycle() would run, with the frees and arrivals they meet caught up by the next."""
        dp = self.p.dp_ps
        while self.next_dp <= until:
            if not self.lane and not self.beat_ready:
                if self.lock is None and not self.others:
                    target = min(self.sr_next, self.gptp_next, until + 1)
                    if target > self.next_dp:
                        self.next_dp += -(-(target - self.next_dp) // dp) * dp
                        continue
                elif self.lock == 'other' and self.used + self.other_left <= self.p.sf_beats:
                    k = min(self.other_left - 1, (until - self.next_dp) // dp + 1)
                    if k > 0:
                        self.used, self.beats, self.other_left = self.used + k, self.beats + k, self.other_left - k
                        self.next_dp += k * dp
                        continue
            self.cycle(self.next_dp)
            self.next_dp += dp

    def cycle(self, t: int) -> None:
        """One datapath cycle: arrivals, one beat into the FIFO, then the packer."""
        p = self.p
        while self.fifo and self.fifo[0][1] <= t:
            self.used -= self.fifo.pop(0)[0]
        while self.sr_next <= t:
            self.others.extend(p.sr_bytes)
            self.sr_next += p.sr_period_ps
        while self.gptp_next <= t:
            self.others.extend(p.gptp_bytes)
            self.gptp_next += p.gptp_period_ps
        held = self.beat_ready
        if self.lock is None:
            self.grant(t, held)
        if self.lock == 'control' and held and self.used < p.sf_beats:
            self.used += 1
            self.beats += 1
            self.beat_ready = False
            if self.beat_last:
                self.complete(t, self.frame[0], True)
                self.gap_until = t + p.gap_dp * p.dp_ps
                self.lock = None
        elif self.lock == 'other' and self.used < p.sf_beats:
            self.used += 1
            self.beats += 1
            self.other_left -= 1
            if self.other_left == 0:
                self.complete(t, self.others.pop(0), False)
                self.lock = None
        if not held and self.lane and self.lane[0][0] <= t:
            self.pack()

    def grant(self, t: int, held: bool) -> None:
        """A frame boundary: the control lane's frame or the next other frame, alternating when both wait."""
        control, other = held and t >= self.gap_until, bool(self.others)
        if (not control and not other) or len(self.fifo) >= self.p.sf_frames:
            return
        self.lock = 'control' if control and (not other or self.last != 'control') else 'other'
        self.last, self.beats = self.lock, 0
        if self.lock == 'other':
            self.other_left = (self.others[0] + 7) // 8

    def pack(self) -> None:
        """The packer takes one byte; its eighth, or the frame's last, finishes a beat."""
        _, last, ch, sys = self.lane.pop(0)
        self.beat_bytes += 1
        self.frame_bytes += 1
        if last or self.beat_bytes == 8:
            self.beat_ready, self.beat_last, self.beat_bytes = True, last, 0
            if last:
                self.frame, self.frame_bytes = (self.frame_bytes, ch, sys), 0

    def complete(self, t: int, length: int, control: bool) -> None:
        """A frame whose last beat entered the FIFO at t takes its turn on the wire."""
        start = max(t, self.wire_free)
        end = start + self.p.wire_ps(length)
        self.wire_free = end + self.p.gap_octets * self.p.octet_ps
        self.fifo.append((self.beats, end))
        if control:
            self.departed.append((self.frame[2], self.frame[1], length, t, end))


@dataclasses.dataclass
class Record:
    """One record the census committed: when, on which channel, its words and frame, and where it went."""
    commit: int
    ch: int
    words: int
    length: int
    wire: int
    egress: tuple | None = None
    held: bool = False


def parse(text: str) -> dict:
    """The lines a grade reads: the queue, commits, departures, the testbench's egress and its holds."""
    out = dict(queue=None, txc=[], wire=[], egress=[], holds=[])
    for line in text.splitlines():
        head = line[:8]
        if head.startswith('TXC '):
            out['txc'].append(tuple(int(f) for f in line.split()[1:4]))
        elif head.startswith('WIRE '):
            f = line.split()
            out['wire'].append((int(f[1]), int(f[3]), len(f[4]) // 2))
        elif head.startswith('EGRESS '):
            out['egress'].append(tuple(int(f) for f in line.split()[1:6]))
        elif head.startswith('TXREADY '):
            out['holds'].append(tuple(int(f) for f in line.split()[1:3]))
        elif head.startswith('EGRESSQ '):
            out['queue'] = line.strip()
    return out


def records(log: dict) -> list[Record]:
    """Each departed record, matched to its commit, in the order the mailbox served them."""
    per_ch: dict = {}
    for t, ch, n in log['wire']:
        per_ch.setdefault(ch, []).append((t, n))
    egress = {(e[0], e[1]): e for e in log['egress']}
    head: dict = {}
    taken: dict = {}
    out = []
    for t, ch, h in log['txc']:
        delta, head[ch] = (h - head.get(ch, 0)) & 0xffff, h
        while delta > 0:
            k = taken.get(ch, 0)
            if k >= len(per_ch.get(ch, [])):
                raise ValueError(f'channel {ch}: a commit at {t} with no departure left')
            wire, n = per_ch[ch][k]
            taken[ch], words = k + 1, 2 + (n + 3) // 4
            if words > delta:
                raise ValueError(f'channel {ch}: a {words}-word record over a {delta}-word commit at {t}')
            delta -= words
            out.append(Record(t, ch, words, n, wire, egress.get((wire, ch))))
    left = {ch: len(v) - taken.get(ch, 0) for ch, v in per_ch.items() if len(v) != taken.get(ch, 0)}
    if left:
        raise ValueError(f'departures with no commit: {left}')
    return sorted(out, key=lambda r: r.wire)


def hold_windows(holds: list) -> list[tuple]:
    """The script's `txready 0` windows as the edges they hold, [first, end) in sys cycles: a TXREADY line takes
    effect at the next edge."""
    out, start = [], None
    for t, ready in holds:
        if not ready and start is None:
            start = t + 1
        elif ready and start is not None:
            out.append((start, t + 1))
            start = None
    return out + ([(start, 1 << 62)] if start is not None else [])


def replay(recs: list[Record], holds: list, p: Params, phase_ps: int) -> list[tuple]:
    """Each record through KL_mbx_tx and the queue, as (its last byte's edge, its last beat in, its last octet), in
    recs' order: the mailbox serves them in the census's order, each once committed and the one before it sent, and
    offers each byte until the crossing takes it, as the testbench's edge order has it (ready from the edge before)."""
    q, windows, free_at, tails = Queue(p, phase_ps), hold_windows(holds), 0, []
    sp = p.sys_ps
    for r in recs:
        e, sent = max(r.commit + MBX_VISIBLE, free_at) + MBX_LEAD, 0
        while sent < r.length:
            held = next((end for first, end in windows if first <= e < end), None)
            if held is not None:
                e = held
                continue
            q.advance((e - 1) * sp)
            ok = q.ready()
            q.advance(e * sp)
            if ok:
                sent += 1
                q.take(e, sent == r.length, r.ch)
                e += 2 if sent % 4 == 0 and sent < r.length else 1
            else:
                e += 1
        tails.append(e - 1)
        free_at = e - 1 + MBX_AFTER
    q.advance((free_at + 1) * sp + 64 * p.wire_ps(1514) + 2 * p.gptp_period_ps // 10**3)
    per_ch: dict = {}
    for d in q.departed:
        per_ch.setdefault(d[1], []).append(d)
    taken: dict = {}
    out = []
    for r, tail in zip(recs, tails):
        k = taken.get(r.ch, 0)
        taken[r.ch] = k + 1
        d = per_ch[r.ch][k]
        out.append((tail, d[3], d[4]))
    return out


def mark_held(recs: list[Record], windows: list, ends: list) -> None:
    """A record whose commit-to-last-octet wait meets a hold, and every record committed while a held one waits, is
    the held-egress ledger's (egress_ledger.py), not this row's."""
    order = sorted(range(len(recs)), key=lambda i: recs[i].commit)
    held_until = -1
    for i in order:
        r = recs[i]
        meets = any(first <= ends[i] and r.commit < end for first, end in windows)
        r.held = meets or r.commit < held_until
        if r.held:
            held_until = max(held_until, ends[i])


def grade_case(text: str, p: Params) -> dict:
    """One case's grade: its queue as stated, the replay's agreement with the testbench, and its largest unheld wait
    over the SR phases."""
    log = parse(text)
    if log['queue'] != p.line():
        return dict(refused=f'the testbench ran another queue: {log["queue"]!r}, the sources state {p.line()!r}')
    recs = records(log)
    missing = sum(r.egress is None for r in recs)
    if missing:
        return dict(refused=f'{missing} record(s) with no EGRESS departure')
    sp, windows = p.sys_ps, hold_windows(log['holds'])
    ends = [r.egress[4] // sp + 1 for r in recs]
    mark_held(recs, windows, ends)
    first = replay(recs, log['holds'], p, 0)
    agree = max((max(abs(t - r.wire) * sp, abs(end - r.egress[4])) for (t, _, end), r in zip(first, recs)), default=0)
    worst = (0, 0, None)
    for phase in range(PHASES):
        run = first if phase == 0 else replay(recs, log['holds'], p, phase * p.sr_period_ps // PHASES)
        for (_, _, end), r in zip(run, recs):
            wait = max(end, r.egress[4] if phase == 0 else 0) - r.commit * sp
            if not r.held and wait > worst[0]:
                worst = (wait, phase, r)
    wait, phase, r = worst
    return dict(records=len(recs), held=sum(r.held for r in recs), agree_ps=agree, wait_ps=wait, phase=phase,
                at=None if r is None else dict(commit=r.commit, ch=r.ch, length=r.length),
                queued=most_queued([(x.commit * sp, x.egress[4]) for x in recs if not x.held]))


def most_queued(spans: list[tuple[int, int]]) -> int:
    """The most records committed and not yet on the wire at once, from (commit, last octet) in ps."""
    events = sorted([(c, 1) for c, _ in spans] + [(e, -1) for _, e in spans], key=lambda x: (x[0], x[1]))
    most = now = 0
    for _, step in events:
        now += step
        most = max(most, now)
    return most


def gptp_wire_ps(p: Params) -> int:
    """The gPTP burst's whole time on the wire, its gaps included, ps."""
    return sum(p.wire_ps(n) + p.gap_octets * p.octet_ps for n in p.gptp_bytes)


def verdict(rows: dict, p: Params, margin: float = MARGIN) -> tuple[bool, list[str]]:
    """Whether every case agrees and was graded, and whether (b) holds: the largest wait and the gPTP burst, plus the
    margin, plus the fixed path, within BOUND_US."""
    lines, ok = [], True
    for case, row in sorted(rows.items()):
        if 'refused' in row:
            ok = False
            lines.append(f'REFUSED {case}: {row["refused"]}')
        elif row['agree_ps'] > AGREE_PS:
            ok = False
            lines.append(f'DISAGREE {case}: the replay departs {row["agree_ps"]} ps from the testbench')
    graded = [r for r in rows.values() if 'wait_ps' in r]
    wait = max((r['wait_ps'] for r in graded), default=0)
    total_us = (margin * (wait + gptp_wire_ps(p)) / 1000 + MII_FIXED_NS) / 1000
    lines.append(f'EGRESS100 wait {wait / 10**6:.3f} us + gPTP {gptp_wire_ps(p) / 10**6:.2f} us, x {margin}, '
                 f'+ fixed {MII_FIXED_NS / 1000:.2f} us = {total_us:.3f} us, bound {BOUND_US} us; most records '
                 f'queued at once {max((r.get("queued", 0) for r in graded), default=0)}')
    ok = ok and bool(graded) and total_us <= BOUND_US
    return ok, lines


def burst(p: Params, ch: int, length: int, count: int) -> list[tuple]:
    """count frames of length on ch, each committed as soon as its ring has room for it (the firmware's free-space
    test at the link-rate tail, at its earliest): (commit, last octet) of each, sys cycles and ps."""
    words, recs = 2 + (length + 3) // 4, []
    for _ in range(count):
        commit = 0
        if recs:
            done = replay(recs, [], p, 0)
            used = [(r, t) for r, (t, _, _) in zip(recs, done)]
            commit = recs[-1].commit
            while sum(r.words for r, t in used if t >= commit) + words > p.ring_words[ch]:
                commit = min(t for r, t in used if t >= commit) + 1
        recs.append(Record(commit, ch, words, length, 0))
        for i, r in enumerate(recs):
            r.wire = i
    return [(r.commit, end) for r, (_, _, end) in zip(recs, replay(recs, [], p, 0))]


def structural(p: Params) -> list[str]:
    """The AECP admission burst at the point, and the rings at their capacity of the least record."""
    sp, out = p.sys_ps, []
    aecp = burst(p, AECP_CH, AECP_FRAME, AECP_RECIPIENTS)
    waits = [end - c * sp for c, end in aecp]
    out.append(f'AECP admission burst: {AECP_RECIPIENTS} x {AECP_FRAME} B on a {p.ring_words[AECP_CH]}-word ring, '
               f'one record at a time: largest wait {max(waits) / 10**6:.2f} us, first commit to last octet '
               f'{aecp[-1][1] / 10**6:.2f} us')
    least = 2 + (14 + 3) // 4
    recs = []
    for ch, words in enumerate(p.ring_words):
        recs += [Record(0, ch, least, 14, 0) for _ in range(words // least)]
    for i, r in enumerate(recs):
        r.wire = i
    full = replay(recs, [], p, 0)
    out.append(f'rings at capacity: {len(recs)} records of the 14-byte frame committed together: the last octet '
               f'{max(end for _, _, end in full) / 10**6:.2f} us after the commit')
    return out


def testbench_log(p: Params, commits: list[tuple], holds: tuple = ()) -> str:
    """A log as the testbench prints it for commits [(sys, ch, length)], its departures this module's own replay,
    so a grade of it agrees by construction until a control plants a defect."""
    heads: dict = {}
    recs = []
    for t, ch, n in commits:
        heads[ch] = heads.get(ch, 0) + 2 + (n + 3) // 4
        recs.append((t, ch, heads[ch], n))
    order = [Record(t, ch, 2 + (n + 3) // 4, n, i) for i, (t, ch, _, n) in enumerate(recs)]
    done = replay(order, list(holds), p, 0)
    lines = [p.line()] + [f'TXREADY {t} {v}' for t, v in holds]
    lines += [f'TXC {t} {ch} {h}' for t, ch, h, _ in recs]
    for r, (tail, t_in, end) in zip(order, done):
        lines += [f'WIRE {tail} 0 {r.ch} ' + '00' * r.length, f'EGRESS {tail} {r.ch} {r.length} {t_in} {end}']
    return '\n'.join(lines) + '\n'


def plants(p: Params) -> dict:
    """Each defect a control must catch. 'model' changes the queue both the testbench log and the grade run, a
    defect of the shared model; 'graded' changes only the grade's, a grade drifted from its testbench."""
    def changed(**kw: object) -> Params:
        """p with some fields changed."""
        return dataclasses.replace(p, **kw)
    return {'wire-twice-as-fast': dict(model=changed(octet_ps=p.octet_ps // 2)),
            'no-gasket': dict(model=changed(gap_dp=1)),
            'nine-frame-fifo': dict(model=changed(sf_frames=p.sf_frames + 1)),
            'no-sr-stream': dict(model=changed(sr_bytes=())),
            'grade-drifted': dict(graded=changed(lane_bytes=p.lane_bytes + 1)),
            'held-counted': dict(mark=lambda recs, windows, ends: None),
            'no-margin': dict(margin=1.0),
            'no-gptp': dict(gptp=False)}


def controls(p: Params, defect: dict) -> list[tuple[str, bool]]:
    """Each control's name and whether it held under defect (an empty dict is the shipping grade)."""
    shipped = globals()['mark_held']
    if 'mark' in defect:
        globals()['mark_held'] = defect['mark']
    try:
        return run_controls(p, defect.get('model', p), defect)
    finally:
        globals()['mark_held'] = shipped


def departures(text: str) -> list[tuple[int, int]]:
    """Each EGRESS line's last beat in and last octet, ps."""
    return [(int(f[4]), int(f[5])) for f in (l.split() for l in text.splitlines()) if f and f[0] == 'EGRESS']


def run_controls(p: Params, m: Params, defect: dict) -> list[tuple[str, bool]]:
    """The controls: each writes a testbench log with the model's queue m, grades it with the grade's queue, and
    holds the result to what the sources' queue p gives by hand."""
    graded = defect.get('graded', m)
    quiet = (p.sr_period_ps * 8 + 20 * 10**6) // p.sys_ps  # 20 us after an SR frame, the gPTP burst long gone
    one = testbench_log(m, [(quiet, 2, 64)])
    (t_in, end), = departures(one)
    row = grade_case(one, graded)
    out = [('an isolated frame leaves its wire time after its last beat', end - t_in == p.wire_ps(64)),
           ('the grade runs the testbench\'s queue and agrees with it', row.get('agree_ps') == 0)]
    (in0, _), (in1, _) = departures(testbench_log(m, [(quiet, 2, 64), (quiet + 1, 2, 64)]))
    out.append(('two frames enter the FIFO a gasket apart', in1 - in0 >= p.gap_dp * p.dp_ps))
    slow = dataclasses.replace(m, octet_ps=m.octet_ps * 64, gap_dp=1, sr_bytes=(), gptp_bytes=())
    many = departures(testbench_log(slow, [(1000 + i, i % 5, 14) for i in range(p.sf_frames + 1)]))
    out.append(('the FIFO holds its frames to their last octet', many[p.sf_frames][0] >= many[0][1]))
    at = p.sr_period_ps * 4
    late = departures(testbench_log(dataclasses.replace(m, gptp_bytes=()), [(at // p.sys_ps - 20, 2, 64)]))
    sr_end = at + p.wire_ps(p.sr_bytes[0]) + p.gap_octets * p.octet_ps
    out.append(('the SR stream is in the queue', late[0][1] - p.wire_ps(64) >= sr_end))
    hold = testbench_log(m, [(1000, 1, 64), (2000, 1, 64)], holds=((900, 0), (900 + 60 * 10**9 // m.sys_ps, 1)))
    out.append(('a held egress is the ledger\'s, not the row\'s', grade_case(hold, graded).get('wait_ps', 1 << 62) == 0))
    gptp = gptp_wire_ps(p)
    edge = int((BOUND_US * 1000 - MII_FIXED_NS) * 1000 / MARGIN) - gptp + 1000
    rows = {'edge': dict(records=1, held=0, agree_ps=0, wait_ps=edge, phase=0, at=None)}
    used = p if defect.get('gptp', True) else dataclasses.replace(p, gptp_bytes=())
    out.append(('a wait just past the bound less its margin and gPTP fails',
                not verdict(rows, used, defect.get('margin', MARGIN))[0]))
    return out


def selftest(p: Params) -> int:
    """The controls on the shipping grade, then each plant caught by at least one of them."""
    clean = controls(p, {})
    for name, ok in clean:
        print(f'{"PASS" if ok else "FAIL"} {name}')
    failed = sum(not ok for _, ok in clean)
    for name, defect in plants(p).items():
        caught = [c for c, ok in controls(p, defect) if not ok]
        print(f'{"CAUGHT" if caught else "MISSED"} {name}' + (f': {"; ".join(caught)}' if caught else ''))
        failed += not caught
    total = len(clean) + len(plants(p))
    print(f'egress_mii selftest: {total - failed} of {total} passed')
    return int(bool(failed))


def arty_spec() -> dict:
    """The Arty point's clocks and shape, as its census builds them."""
    cfg = yaml.safe_load((CONFIGS / 'endstation_arty_current.yaml').read_text())['board']['constraints']
    return dict(shape='endstation_arty_current', sys_hz=cfg['sys_clk_hz'], milan_hz=cfg['milan_clk_hz'])


def main(argv: list[str]) -> int:
    """Grade every case of each build directory given (its build.json and results/*.log)."""
    if argv in (['--selftest'], ['--structural']):
        p = params(arty_spec())
        if argv == ['--selftest']:
            return selftest(p)
        print('\n'.join(structural(p)))
        return 0
    if not argv:
        print(__doc__)
        return 2
    rows: dict = {}
    p = None
    for build in map(Path, argv):
        p = params(json.loads((build / 'build.json').read_text()))
        if p is None:
            print(f'SKIP {build}: a gigabit point, whose egress is instant')
            continue
        for log in sorted((build / 'results').glob('*.log')):
            case = f'{build.name}/{log.stem}'
            rows[case] = grade_case(log.read_text(errors='replace'), p)
            print(f'GRADED {case}: {json.dumps(rows[case])}', flush=True)
    if p is None:
        return 2
    ok, lines = verdict(rows, p)
    print('\n'.join(lines))
    print(f'RESULT: {"PASS" if ok else "FAIL"} cases={len(rows)}')
    return int(not ok)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
