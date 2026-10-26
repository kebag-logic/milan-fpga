# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The stimulus groups of the budget and the probes each measures (#665).

A group is one boot of the test SoC and a script of steps; sim_main.cpp
runs it. A probe is one measured path: a `mark` line names it, then its
stimulus, then a bounded wait for its completion. grade.py reads the start
and the end of each probe off the observation log by the probe's rules:

  start  rxc:<ch>         the fabric's receive commit (RX_HEAD) on the channel
         pad:LINK:<if>    the link level changing at the mailbox input
         pad:GM:<if>      the grandmaster-change pulse at the mailbox input
         deadline:<slot>  the armed deadline of the slot's next TIMER record
         entry:<symbol>   the first commit of that function's entry (a test-only entry)
  end    tx:<ch>[:n]      the n-th accepted TX_HEAD write on the channel
         arm:<slot>       a TMR_CMD arm of the slot; cancel:<slot> its cancel
         tmr:<slot>       any TMR_CMD write of the slot
         resp:<ch>:<seq>  the TX record on the channel answering sequence_id seq
         notify:<ch>:<command_type>:<descriptor_type>:<descriptor_index>
                          the unsolicited AECP responses that command's change causes,
                          one to each of the probe's recipients (IEEE 1722.1-2021 7.5.2);
                          the last recipient's commit ends it (FR_NFR.md 3.4.1)
         acmp_cmd:<ch>:<type>  an ACMP command the firmware originates, e.g. PROBE_TX
         maap:<ch>:<type>  a MAAP frame of that message type; adp:<ch>:<type> an ADPDU
         rxtail:<ch>      the RX_TAIL write that releases the record
         pass_end:<ch>    the end of the pass that took the record: its handler runs
                          after the release, inside that pass (ctrl_loop.c service_rx)
         pub:<word>       a write of that publication word

A probe's frames carry its name as their tag, so its start is the commit of
its own frame even when other frames share the ring; a probe may bound its
search by a later mark (until) when probes overlap on purpose.

A group's load is the population its stimulus declares for its composed
window: the records per receive channel and the GM and LINK events. grade.py
never trusts it: it refuses a window whose committed population is not the
row's defined load, which it derives from the contract alone
(grade.defined_load), and the self-test counts every window's stimulus
against that definition, so a channel left out of the stimulus and its
declaration together still fails.

The paths, their clauses and their ceilings come from FR_NFR.md 3.4.1 and
MAILBOX_SPLIT.md; every address comes from the mailbox contract.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import frames as f

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'sw/mailbox'))
from mailbox_model import load  # noqa: E402

CONTRACT = load()
CH = {ch.name: n for n, ch in enumerate(CONTRACT.channels)}
REG = {r.name: r.offset for r in CONTRACT.registers}
CH_REG = {r.name: r.offset for r in CONTRACT.ch_registers}
PUB_REG = {r.name: r.offset for r in CONTRACT.pub_registers}
SINK_REG = {r.name: r.offset for r in CONTRACT.pub_sink_registers}
MS = 100_000                       # system cycles per millisecond at the 100 MHz bus


def word(byte_offset: int) -> int:
    """The host port's word address of a window byte offset."""
    return byte_offset // 4


def ch_word(ch: int, name: str) -> int:
    """The word address of a channel register."""
    return word(CONTRACT.ch_base + ch * CONTRACT.ch_stride + CH_REG[name])


def pub_word(interface: int, name: str) -> int:
    """The word address of an interface's publication register (contract 2.2)."""
    return word(CONTRACT.pub_base + interface * CONTRACT.pub_stride + PUB_REG[name])


def binding_word(interface: int, sink: int) -> int:
    """The word address of a sink's BINDING publication register."""
    return word(CONTRACT.pub_base + interface * CONTRACT.pub_stride + CONTRACT.pub_sink_base
                + sink * CONTRACT.pub_sink_stride + SINK_REG['BINDING'])


TMR_CMD_WORD = word(REG['TMR_CMD'])
EVT_TAIL_WORD = word(REG['EVT_TAIL'])

#: The project budget and each path family's normative ceiling, FR_NFR.md 3.4.1.
T_SVC_MS = 10.0
CEILING_MS = {
    'adp': 200.0,     # Milan v1.2 5.6.3.5.2: 2 s random window x 10 % (the whole ADP function)
    'disc': 20.0,     # Milan v1.2 5.5.2.3, Table 5.26: a resulting ACMP action, 200 ms x 10 %
    'acmp': 20.0,     # Milan v1.2 5.5.2.3, Table 5.26: 200 ms transaction timeout x 10 %
    'aecp': 24.0,     # IEEE 1722.1-2021 9.3.2.6: 240 ms response x 10 %
    'notify': 24.0,   # Milan v1.2 5.4.5.2; IEEE 1722.1-2021 7.5.2: the related 240 ms interval
    'maap': 50.0,     # IEEE 1722-2016 B.3.4.2, Table B.8: 500 ms probe interval x 10 %
    'srp': 18.0,      # IEEE 802.1Q-2018 10.7.11, Milan v1.2 Table 4.3: JoinTime 180 ms x 10 %
}


@dataclass
class Probe:
    """One measured path instance."""
    name: str            # e.g. adp.discover.if0
    row: str             # the table row it measures
    family: str          # key of CEILING_MS
    start: str
    ends: list[str]      # every listed end must occur; the path ends at the last of them
    wait_ms: float = 0.0  # a normative wait W the path may include (3.4.1: elapsed <= W + T_svc)
    expect: str = ''     # an expected response check, see grade.py
    accesses: int | None = None  # the host model's measured or bound accesses in the pass, for comparison
    until: str = ''      # a later mark bounding the search; '' is the next mark
    also_from: str = ''  # a mark the interval is also reported from (the row's own origin)
    #: A notification's required recipients: (controller entity_id, interface), each
    #: registered for unsolicited notifications on that interface (IEEE 1722.1-2021 7.5.2).
    recipients: tuple[tuple[int, int], ...] = ()
    path: str = ''       # the path it is an instance of; '' is the name without .if<n>
    #: The sequence_ids of the responses owed ahead of the probe's: exactly these, in this
    #: order, must be committed on its channel between its input and its response.
    owed: tuple[int, ...] = ()
    #: An admitted command the firmware may take and never answer under the load: a missing
    #: response is then a measured finding, never answered (unbounded), not a refusal.
    may_drop: bool = False

    def path_key(self) -> tuple[str, int]:
        """The path and interface this probe measures; the tables report each one's worst instance."""
        base, _, suffix = self.name.rpartition('.if')
        return (self.path or base, int(suffix) if suffix.isdigit() else 0)


@dataclass
class Group:
    name: str
    steps: list[str] = field(default_factory=list)
    probes: list[Probe] = field(default_factory=list)
    sim_ms: int = 0      # the simulated time the script needs, for the run's bound
    #: The composed window's required population: records per receive channel, and
    #: 'GM' and 'LINK' events (grade.py counts each between composed and composed_end).
    load: dict[str, int] = field(default_factory=dict)
    #: Each loaded channel's admission for the records it was offered (admission()).
    admission: dict[str, dict] = field(default_factory=dict)

    def offer(self, channel: str, step: str, frame: bytes) -> None:
        """One record of the composed load: a frame (or a reply) step the channel must commit."""
        self.steps.append(step)
        self.load[channel] = self.load.get(channel, 0) + 1
        self.admission.setdefault(channel, admission(channel, frame))

    def add(self, *steps: str) -> None:
        """Steps with no probe."""
        self.steps.extend(steps)

    def probe(self, probe: Probe, *stimulus: str, wait: str, settle: str = 'quiet 3 within 2000000') -> None:
        """Mark, stimulate, wait for the completion (bounded), then let the loop settle."""
        self.probes.append(probe)
        self.steps.append(f'mark {probe.name}')
        self.steps.extend(tagged(step, probe.name) for step in stimulus)
        self.steps.append(f'wait {wait}')
        if settle:
            self.steps.append(f'wait {settle}')

    def together(self, entries: list[tuple[Probe, list[str]]], waits: list[str],
                 settle: str = 'quiet 3 within 2000000') -> None:
        """Probes that run at once, one per interface: every mark and stimulus, then
        every wait, then a barrier mark that bounds each probe's search."""
        barrier = f'{self.name}.barrier{sum(1 for s in self.steps if s.startswith("mark ") and ".barrier" in s)}'
        for probe, stimulus in entries:
            probe.until = barrier
            self.probes.append(probe)
            self.steps.append(f'mark {probe.name}')
            self.steps.extend(tagged(step, probe.name) for step in stimulus)
        self.steps.extend(f'wait {w}' for w in waits)
        if settle:
            self.steps.append(f'wait {settle}')
        self.steps.append(f'mark {barrier}')

    def script(self) -> str:
        """The stimulus script sim_main.cpp runs."""
        return '\n'.join([*self.steps, 'end']) + '\n'


def tagged(step: str, tag: str) -> str:
    """A frame or reply step carrying the probe's name, so its commit is found by name."""
    if step.startswith('frame '):
        return f'{step} {tag}'
    if step.startswith('reply '):
        return f'{step} tag={tag}'
    return step


@dataclass(frozen=True)
class Point:
    """A measured shape: its config, AVB interface count and identity."""
    label: str
    shape: str
    interfaces: int
    entity_id: int
    mac: int
    sources: int
    sinks: int


def point(label: str, build: dict) -> Point:
    """The point's identity from the generated entity header of its image."""
    import re
    header = Path(build['elf']).with_name('adp_entity_gen.h').read_text()
    values = {k: int(v, 16) for k, v in re.findall(r'\.(\w+) = (0x[0-9A-Fa-f]+)', header)}
    return Point(label, build['shape'], build['interfaces'], values['entity_id'], values['mac'],
                 values['talker_stream_sources'], values['listener_stream_sinks'])


CTL1 = 0x0A0B0C0D0E0F0001          # a controller entity
CTL2 = 0x0A0B0C0D0E0F0002
CTL_MAC = 0x0A0B0C0D0E01
TALKER_A = 0x0C0D0E0F10110001     # a remote talker a sink binds
TALKER_A_MAC = 0x0C0D0E0F1001
LISTENER_B = 0x0D0E0F1011120002   # a remote listener our source answers
BRIDGE_MAC = 0x0E0E0E0E0E01
STREAM_A = 0x0C0D0E0F10010000
STREAM_A_DA = 0x91E0F000FE01


def ready(g: Group, p: Point, link: bool = True) -> None:
    """Boot to the open mailbox and let its startup settle; optionally raise every link.

    ADP arms its startup TMR_DELAY at open, link up or not (Milan v1.2 5.6.3.5.2),
    so no probe may start before that arm has been made.
    """
    g.add('wait ready', 'mark booted', f'wait cycles {50 * MS}', 'wait quiet 3 within 2000000')
    if link:
        for i in range(p.interfaces):
            g.add(f'link {i} 1')
        g.add(f'wait cycles {600 * MS}', 'wait quiet 3 within 2000000', 'mark settled')


def acmp_cmd(p: Point, msg: str, sink: int, seq: int, controller: int = CTL1) -> bytes:
    """A controller's listener command to a sink of this entity, about TALKER_A."""
    return f.acmp(f.ACMP[msg], CTL_MAC, f.Acmp(controller=controller, talker=TALKER_A, listener=p.entity_id,
                                              talker_uid=1, listener_uid=sink, sequence=seq))


def talker_cmd(p: Point, msg: str, source: int, seq: int) -> bytes:
    """A talker command to a source of this entity, for LISTENER_B."""
    return f.acmp(f.ACMP[msg], CTL_MAC, f.Acmp(controller=CTL1, talker=p.entity_id, listener=LISTENER_B,
                                              talker_uid=source, listener_uid=3, sequence=seq))


def probe_answer(interface: int, status: int = 0) -> str:
    """The talker's PROBE_TX_RESPONSE to the last PROBE_TX the firmware sent (8.2.1).

    The command's own fields are echoed; the message type, status, stream_id,
    stream_dest_address and stream_vlan_id are the talker's answer.
    """
    acmp_ch = CH['acmp']
    status_len = (status << 11) | 44
    return (f'reply {interface} {acmp_ch} 15:{f.ACMP["PROBE_TX"]:02x} 6={TALKER_A_MAC:012x} '
            f'15={f.ACMP["PROBE_TX_RESPONSE"]:02x} '
            f'16={status_len:04x} 18={STREAM_A:016x} 54={STREAM_A_DA:012x} 66=0002')


def advertised(g: Group, p: Point) -> None:
    """Links up, then each interface's startup ENTITY_AVAILABLE (TMR_DELAY 0 to 2 s, 5.6.3.5.2)."""
    adp = CH['adp']
    ifs = range(p.interfaces)
    g.together([(Probe(f'adp.link_up.if{i}', 'LINK_UP', 'adp', f'pad:LINK:{i}', [f'arm:{i}'], accesses=11),
                 [f'link {i} 1']) for i in ifs], [f'tmr {i} 1 within {300 * MS}' for i in ifs], settle='')
    g.together([(Probe(f'adp.tmr_delay.if{i}', 'TMR_DELAY expiry', 'adp', f'deadline:{i}',
                       [f'tx:{adp}', f'arm:{i}'], accesses=39, expect=f'adp_available:{i}'), []) for i in ifs],
               [f'tx {adp} {p.interfaces} within {2200 * MS}', f'cycles {20 * MS}'])


def adp_groups(p: Point) -> list[Group]:
    """ADP's rows (MAILBOX_SPLIT.md:495-502), every interface at once, one timer per group."""
    adp = CH['adp']
    ifs = range(p.interfaces)
    every = lambda what: [what.format(i=i) for i in ifs]

    out = []
    g = Group('adp-link', sim_ms=2800)
    ready(g, p, link=False)
    advertised(g, p)
    g.together([(Probe(f'adp.link_down.if{i}', 'LINK_DOWN', 'adp', f'pad:LINK:{i}', [f'cancel:{i}'], accesses=9),
                 [f'link {i} 0']) for i in ifs], [f'tmr {i} 2 within {300 * MS}' for i in ifs])
    out.append(g)
    g = Group('adp-gm', sim_ms=2800)
    ready(g, p, link=False)
    advertised(g, p)
    g.together([(Probe(f'adp.gm_change.if{i}', 'GM_CHANGE', 'adp', f'pad:GM:{i}', [f'arm:{i}'], accesses=11),
                 [f'gm {i} 0a0b0c0dfffe0e{i:02x} 0']) for i in ifs], [f'tmr {i} 1 within {300 * MS}' for i in ifs])
    out.append(g)
    g = Group('adp-discover', sim_ms=2800)
    ready(g, p, link=False)
    advertised(g, p)
    disc = f.adp(f.ADP_DISCOVER, 0, CTL_MAC, f.Adp(valid_time=0))
    g.together([(Probe(f'adp.discover.if{i}', 'RCV_ADP_DISCOVER', 'adp', f'rxc:{adp}', [f'arm:{i}'], accesses=31),
                 [f'frame {i} {disc.hex()}']) for i in ifs], [f'tmr {i} 1 within {300 * MS}' for i in ifs])
    out.append(g)
    g = Group('adp-advertise', sim_ms=7800)
    ready(g, p, link=False)
    advertised(g, p)
    g.together([(Probe(f'adp.tmr_advertise.if{i}', 'TMR_ADVERTISE expiry', 'adp', f'deadline:{i}', [f'arm:{i}'],
                       accesses=11), []) for i in ifs],
               [f'cycles {4800 * MS}', *[f'tmr {i} 1 within {700 * MS}' for i in ifs]], settle='')
    out.append(g)
    del every
    return out


def acmp_groups(p: Point) -> list[Group]:
    """ACMP's rows (MAILBOX_SPLIT.md:645-657): commands, the timer paths and discovery."""
    acmp, adp = CH['acmp'], CH['adp']
    ifs = range(p.interfaces)
    slot = lambda i: p.interfaces + i               # ACMP's slot of interface i (ctrl_app.h)
    def avail(valid: int = 10, index: int = 0) -> bytes:
        """TALKER_A's ENTITY_AVAILABLE (6.2.1) with its valid_time and available_index."""
        return f.adp(f.ADP_AVAILABLE, TALKER_A, TALKER_A_MAC,
                     f.Adp(valid_time=valid, talker_sources=1, talker_caps=0x4001, available_index=index))
    gone = f.adp(f.ADP_DEPARTING, TALKER_A, TALKER_A_MAC, f.Adp(valid_time=0, talker_sources=1, talker_caps=0x4001))
    out = []

    def bind(g: Group, seq: int) -> None:
        """Sink i bound to TALKER_A on interface i (the fixture puts sink n on interface n % N_IF)."""
        g.add(*[f'frame {i} {acmp_cmd(p, "BIND_RX", i, seq + i).hex()}' for i in ifs],
              f'wait tx {acmp} {2 * p.interfaces} within {40 * MS}', 'wait quiet 3 within 2000000')

    g = Group('acmp-cmd', sim_ms=2500)
    ready(g, p)
    seq = 0x4100
    for i in ifs:
        k = i
        g.probe(Probe(f'acmp.bind_rx.if{i}', 'BIND_RX', 'acmp', f'rxc:{acmp}',
                      [f'resp:{acmp}:{seq:x}', f'acmp_cmd:{acmp}:PROBE_TX', f'arm:{slot(i)}',
                       f'pub:{binding_word(i, k)}'], accesses=77, expect='acmp_status:BIND_RX_RESPONSE:0'),
                f'frame {i} {acmp_cmd(p, "BIND_RX", k, seq).hex()}', wait=f'tx {acmp} 2 within {20 * MS}')
        seq += 1
        g.probe(Probe(f'acmp.probe_tx_response.if{i}', 'PROBE_TX_RESPONSE', 'acmp', f'rxc:{acmp}',
                      [f'arm:{slot(i)}'], accesses=32), probe_answer(i), wait=f'tmr {slot(i)} 1 within {300 * MS}')
        g.probe(Probe(f'acmp.get_rx_state.if{i}', 'GET_RX_STATE', 'acmp', f'rxc:{acmp}', [f'resp:{acmp}:{seq:x}'],
                      accesses=47, expect='acmp_type:GET_RX_STATE_RESPONSE'),
                f'frame {i} {acmp_cmd(p, "GET_RX_STATE", k, seq).hex()}', wait=f'tx {acmp} 1 within {20 * MS}')
        seq += 1
        g.probe(Probe(f'acmp.unbind_rx.if{i}', 'UNBIND_RX', 'acmp', f'rxc:{acmp}',
                      [f'resp:{acmp}:{seq:x}', f'tmr:{slot(i)}'], accesses=50,
                      expect='acmp_status:UNBIND_RX_RESPONSE:0'),
                f'frame {i} {acmp_cmd(p, "UNBIND_RX", k, seq).hex()}', wait=f'tx {acmp} 1 within {20 * MS}')
        seq += 1
        for msg in ('PROBE_TX', 'GET_TX_STATE', 'DISCONNECT_TX', 'GET_TX_CONNECTION'):
            g.probe(Probe(f'acmp.{msg.lower()}.if{i}', msg, 'acmp', f'rxc:{acmp}', [f'resp:{acmp}:{seq:x}'],
                          accesses=48, expect=f'acmp_type:{msg}_RESPONSE'),
                    f'frame {i} {talker_cmd(p, msg, i, seq).hex()}', wait=f'tx {acmp} 1 within {20 * MS}')
            seq += 1
    out.append(g)

    g = Group('acmp-noresp', sim_ms=6800)
    ready(g, p)
    bind(g, 0x4200)
    g.together([(Probe(f'acmp.tmr_no_resp1.if{i}', 'TMR_DELAY, or the first TMR_NO_RESP', 'acmp', f'deadline:{slot(i)}',
                       [f'acmp_cmd:{acmp}:PROBE_TX', f'arm:{slot(i)}'], accesses=35), []) for i in ifs],
               [f'cycles {300 * MS}'], settle='')
    g.together([(Probe(f'acmp.tmr_no_resp2.if{i}', 'the second TMR_NO_RESP', 'acmp', f'deadline:{slot(i)}',
                       [f'arm:{slot(i)}'], accesses=14), []) for i in ifs],
               [f'cycles {150 * MS}', *[f'tmr {slot(i)} 1 within {300 * MS}' for i in ifs]])
    g.add(*[f'frame {i} {avail().hex()}' for i in ifs], 'wait quiet 3 within 2000000')
    g.together([(Probe(f'acmp.tmr_retry.if{i}', 'TMR_RETRY', 'acmp', f'deadline:{slot(i)}', [f'arm:{slot(i)}'],
                       accesses=14), []) for i in ifs],
               [f'cycles {3900 * MS}', *[f'tmr {slot(i)} 1 within {600 * MS}' for i in ifs]], settle='')
    g.together([(Probe(f'acmp.tmr_delay.if{i}', 'TMR_DELAY', 'acmp', f'deadline:{slot(i)}',
                       [f'acmp_cmd:{acmp}:PROBE_TX', f'arm:{slot(i)}'], accesses=35), []) for i in ifs],
               [f'cycles {1100 * MS}'])
    out.append(g)

    g = Group('acmp-notk', sim_ms=11500)
    ready(g, p)
    bind(g, 0x4300)
    g.add(*[probe_answer(i) for i in ifs], 'wait quiet 3 within 2000000')
    g.add(*[f'frame {i} {avail().hex()}' for i in ifs], 'wait quiet 3 within 2000000')
    g.together([(Probe(f'acmp.tmr_no_tk.if{i}', 'TMR_NO_TK', 'acmp', f'deadline:{slot(i)}', [f'arm:{slot(i)}'],
                       accesses=14), []) for i in ifs],
               [f'cycles {9800 * MS}', *[f'tmr {slot(i)} 1 within {700 * MS}' for i in ifs]])
    out.append(g)

    g = Group('acmp-disc', sim_ms=3800)
    ready(g, p)
    bind(g, 0x4400)
    g.add(*[f'frame {i} {avail().hex()}' for i in ifs], 'wait quiet 3 within 2000000')
    g.together([(Probe(f'acmp.entity_departing.if{i}', 'ENTITY_DEPARTING from its RX_HEAD (H-DISC)', 'disc',
                       f'rxc:{adp}', [f'tmr:{slot(i)}'], accesses=29), [f'frame {i} {gone.hex()}']) for i in ifs],
               [f'cycles {150 * MS}'])
    g.together([(Probe(f'acmp.entity_available.if{i}', 'ENTITY_AVAILABLE from its RX_HEAD (H-DISC)', 'disc',
                       f'rxc:{adp}', [f'arm:{slot(i)}'], accesses=35), [f'frame {i} {avail().hex()}']) for i in ifs],
               [f'tmr {slot(i)} 1 within {300 * MS}' for i in ifs])
    g.add(f'wait tx {acmp} {p.interfaces} within {1200 * MS}', *[probe_answer(i) for i in ifs],
          'wait quiet 3 within 2000000', *[f'frame {i} {avail(1, 1).hex()}' for i in ifs],
          'wait quiet 3 within 2000000')
    g.together([(Probe(f'acmp.tmr_no_adp.if{i}', 'TMR_NO_ADP (H-DISC)', 'disc', f'deadline:{slot(i)}',
                       [f'arm:{slot(i)}'], accesses=12), []) for i in ifs],
               [f'cycles {1900 * MS}', *[f'tmr {slot(i)} 1 within {600 * MS}' for i in ifs]])
    out.append(g)
    return out


def descriptors(build: dict) -> list[tuple[int, int, int, int]]:
    """(configuration, type, index, length) of every descriptor in the image's AEM table.

    The table is the one aecp_image.c validates: at the be32 offset at byte 12,
    be16 count at byte 8, 16-byte rows of configuration, type, count, length.
    """
    import re
    header = Path(build['elf']).with_name('aecp_entity_gen.h').read_text()
    body = header[header.index('aecp_entity_image[] = {'):]
    body = body[:body.index('};')]
    image = bytes(int(v, 0) for v in re.findall(r'0x[0-9a-fA-F]+|\b\d+\b', body.split('{', 1)[1]))
    offset, count = int.from_bytes(image[12:16], 'big'), int.from_bytes(image[8:10], 'big')
    out, first = [], {}
    for row in range(count):
        e = image[offset + 16 * row:offset + 16 * row + 16]
        config, kind, number, length = (int.from_bytes(e[k:k + 2], 'big') for k in (0, 2, 4, 6))
        for n in range(number):
            out.append((config, kind, first.get((config, kind), 0) + n, length))
        first[(config, kind)] = first.get((config, kind), 0) + number
    return out


def aecp_groups(p: Point, build: dict) -> list[Group]:
    """AECP's solicited responses (H-AECP): every descriptor read, the getters and the setters.

    Each probe ends at its response. The fan-out a setter's change causes is
    aecp_fanout_groups' path, measured at the firmware's registration capacity.
    """
    aecp = CH['aecp']
    g = Group('aecp', sim_ms=2500)
    ready(g, p)
    seq = [0x6100]

    def cmd(i: int, name: str, command_type: int, payload: bytes, controller: int = CTL1,
            notices: int = 0) -> None:
        """One AEM command probe, ending at its response; its wait also lets the change's notices leave."""
        frame = f.aem_command(f.Aem(p.entity_id, controller, CTL_MAC, p.mac, seq[0]), command_type, payload)
        ends = [f'resp:{aecp}:{seq[0]:x}']
        seq[0] += 1
        g.probe(Probe(f'aecp.{name}.if{i}', name, 'aecp', f'rxc:{aecp}', ends, expect='aecp_response'),
                f'frame {i} {frame.hex()}', wait=f'tx {aecp} {1 + notices} within {50 * MS}')

    rows = descriptors(build)
    last = {}
    for row in rows:                          # one per type: the last index, whose read walks farthest
        last[(row[0], row[1])] = row
    for i in range(p.interfaces):
        cmd(i, 'register_unsolicited', 0x0024, bytes(4))
        for config, kind, index, length in (sorted(last.values()) if i == 0 else sorted(last.values())[:3]):
            frame = f.read_descriptor(f.Aem(p.entity_id, CTL1, CTL_MAC, p.mac, seq[0]), kind, index, config)
            end = f'resp:{aecp}:{seq[0]:x}'
            seq[0] += 1
            g.probe(Probe(f'aecp.read_descriptor.t{kind}.i{index}.c{config}.if{i}',
                          f'READ_DESCRIPTOR ({length} B)', 'aecp', f'rxc:{aecp}', [end],
                          expect='aecp_response'),
                    f'frame {i} {frame.hex()}', wait=f'tx {aecp} 1 within {50 * MS}')
        cmd(i, 'get_configuration', 0x0007, bytes(4))
        cmd(i, 'entity_available', 0x0002, bytes(20))
        cmd(i, 'get_name', 0x0011, bytes(8))
        cmd(i, 'get_counters', 0x0029, f.be(9, 2) + f.be(0, 2))
        cmd(i, 'get_avb_info', 0x0028, f.be(9, 2) + f.be(0, 2) + bytes(16))
        cmd(i, 'unknown_command', 0x7FF0, bytes(4))
        mvu = f.mvu_command(f.Aem(p.entity_id, CTL1, CTL_MAC, p.mac, seq[0]), 0x0000, bytes(2))
        end = f'resp:{aecp}:{seq[0]:x}'
        seq[0] += 1
        g.probe(Probe(f'aecp.mvu_get_milan_info.if{i}', 'MVU GET_MILAN_INFO', 'aecp', f'rxc:{aecp}',
                      [end], expect='aecp_response'),
                f'frame {i} {mvu.hex()}', wait=f'tx {aecp} 1 within {50 * MS}')
        # A state change by another controller: its response, then a notice to CTL1 on every
        # interface it has registered on so far (7.5.2), which the wait lets leave.
        name = f'budget if{i}'.encode().ljust(64, b'\0')   # a new value: an identical SET does not notify
        cmd(i, 'set_name', 0x0010, f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + name,
            controller=CTL2, notices=i + 1)
        # LOCK_ENTITY (7.4.2.1): flags, locked_id, descriptor_type and descriptor_index (the ENTITY).
        cmd(i, 'lock_entity', 0x0001, f.be(0, 4) + f.be(0, 8) + f.be(0, 2) + f.be(0, 2), controller=CTL2)
        cmd(i, 'unlock_entity', 0x0001, f.be(1, 4) + f.be(0, 8) + f.be(0, 2) + f.be(0, 2), controller=CTL2)
    return [g]


def registrations() -> int:
    """The registrations for unsolicited notifications the firmware keeps per interface (aecp.h)."""
    import re
    text = (ROOT / 'sw/firmware/ctrl/aecp/aecp.h').read_text()
    return int(re.search(r'#define AECP_REGISTRATIONS (\d+)u', text).group(1))


def descriptor_value(build: dict, kind: int, index: int) -> bytes:
    """A descriptor's bytes in the image's AEM table, from its descriptor_type (aecp_image.c)."""
    import re
    header = Path(build['elf']).with_name('aecp_entity_gen.h').read_text()
    body = header[header.index('aecp_entity_image[] = {'):]
    body = body[:body.index('};')]
    image = bytes(int(v, 0) for v in re.findall(r'0x[0-9a-fA-F]+|\b\d+\b', body.split('{', 1)[1]))
    offset, count = int.from_bytes(image[12:16], 'big'), int.from_bytes(image[8:10], 'big')
    for row in range(count):
        e = image[offset + 16 * row:offset + 16 * row + 16]
        rtype, number, length = (int.from_bytes(e[k:k + 2], 'big') for k in (2, 4, 6))
        base, stride = int.from_bytes(e[8:12], 'big'), int.from_bytes(e[14:16], 'big')
        for n in range(number):
            value = image[base + n * stride:base + n * stride + length]
            if rtype == kind and int.from_bytes(value[2:4], 'big') == index:
                return value
    raise KeyError(f'no descriptor {kind}:{index} in the image')


def map_edit(build: dict, port_type: int) -> bytes | None:
    """An ADD/REMOVE_AUDIO_MAPPINGS payload (IEEE 1722.1-2021 7.4.45.1) for the STREAM_PORT 0 of
    that type: one mapping, its map's last default row. None when that map holds no row: the
    live map starts with its defaults (aecp.c), and a map of capacity 0 can never change."""
    import re
    header = Path(build['elf']).with_name('aecp_entity_gen.h').read_text()
    maps = re.findall(r'\{(\d+),(\d+),(\d+),\d+,\(rows\)\+\d+,\d+,(\d+),aecp_map_defaults\+(\d+),(\d+)\}', header)
    _, _, _, capacity, first, number = next(m for m in maps if m[:3] == (str(port_type), '0', '0'))
    if not int(capacity) or not int(number):
        return None
    defaults = header[header.index('aecp_map_defaults[] = {'):]
    rows = re.findall(r'\{(\d+),(\d+),(\d+),(\d+)\}', defaults[:defaults.index('};')])
    mapping = b''.join(f.be(int(v), 2) for v in rows[int(first) + int(number) - 1])
    return f.be(port_type, 2) + f.be(0, 2) + f.be(1, 2) + f.be(0, 2) + mapping


#: The controllers aecp_fanout_groups registers on every interface, up to the capacity.
FANOUT_CONTROLLER = 0x0A0B0C0D0E0F1000


def aecp_fanout_groups(p: Point, build: dict) -> list[Group]:
    """Every notification fan-out the image completes, at the firmware's registration capacity.

    AECP_REGISTRATIONS controllers register on every interface, then CTL2, which
    is not registered, sends each state-changing command that the image
    notifies: every registration receives it (IEEE 1722.1-2021 7.5.2; aecp.c,
    transmit), and the fan-out ends at the last recipient's commit
    (FR_NFR.md 3.4.1, H-NOTIFY). Each command changes its value, since an
    unchanged SET does not notify. With the answering-ports arm, whose stream
    observation answers, the group also measures the setters the unmodified
    fixture refuses for want of it (SET_CONFIGURATION, SET_STREAM_INFO) and
    BIND_RX's GET_STREAM_INFO notice, which arm A's AECP retries forever.
    """
    aecp, acmp = CH['aecp'], CH['acmp']
    ifs = range(p.interfaces)
    g = Group('aecp-fanout', sim_ms=2600)
    ready(g, p)
    controllers = [FANOUT_CONTROLLER + n for n in range(registrations())]
    seq = [0x5100]
    for i in ifs:
        for ctl in controllers:
            frame = f.aem_command(f.Aem(p.entity_id, ctl, CTL_MAC, p.mac, seq[0]), 0x0024, bytes(4))
            g.add(f'frame {i} {frame.hex()}', f'wait tx {aecp} 1 within {50 * MS}', 'wait quiet 3 within 2000000')
            seq[0] += 1
    everyone = tuple((ctl, i) for i in ifs for ctl in controllers)

    def fanout(i: int, name: str, command_type: int, payload: bytes, path: str = '') -> None:
        """One state-changing command from CTL2 on interface i, to its response and every registration's notice."""
        frame = f.aem_command(f.Aem(p.entity_id, CTL2, CTL_MAC, p.mac, seq[0]), command_type, payload)
        selector = f'{command_type:04x}:{int.from_bytes(payload[0:2], "big")}:{int.from_bytes(payload[2:4], "big")}'
        g.probe(Probe(f'aecp_fanout.{name}.if{i}', name, 'notify', f'rxc:{aecp}',
                      [f'resp:{aecp}:{seq[0]:x}', f'notify:{aecp}:{selector}'], expect='aecp_response',
                      recipients=everyone, path=path),
                f'frame {i} {frame.hex()}', wait=f'tx {aecp} {1 + len(everyone)} within {200 * MS}')
        seq[0] += 1

    rate = descriptor_value(build, 2, 0)[136:140]                  # AUDIO_UNIT current_sampling_rate (7.2.3)
    domain = descriptor_value(build, 36, 0)                        # CLOCK_DOMAIN (7.2.32)
    start, number = int.from_bytes(domain[72:74], 'big'), int.from_bytes(domain[74:76], 'big')
    sources = [int.from_bytes(domain[start + 2 * k:start + 2 * k + 2], 'big') for k in range(number)]
    answering = build.get('variant') == 'answering-ports'
    # Dynamic map edits (Milan v1.2 5.4.2.27/.28): an input map with a row, and an output map
    # with the answering arm (an output edit is refused unless its stream is observed not running).
    edits = [(suffix, edit) for suffix, edit in (('', map_edit(build, 14)),
                                                 ('_output', map_edit(build, 15) if answering else None)) if edit]
    for i in ifs:
        name = f'fanout if{i}'.encode().ljust(64, b'\0')
        fanout(i, 'set_name', 0x0010, f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + name)
        fanout(i, 'set_clock_source', 0x0016, f.be(36, 2) + f.be(0, 2) + f.be(sources[(i + 1) % number], 2)
               + f.be(0, 2))
        # The IDENTIFY control (Milan v1.2 5.3.12): on, then off.
        fanout(i, 'set_control_identify_on', 0x0018, f.be(26, 2) + f.be(0, 2) + bytes((255,)),
               path='aecp_fanout.set_control')
        fanout(i, 'set_control_identify_off', 0x0018, f.be(26, 2) + f.be(0, 2) + bytes((0,)),
               path='aecp_fanout.set_control')
        for suffix, edit in edits:            # one default row removed, then added back
            fanout(i, f'remove_audio_mappings{suffix}', 0x002D, edit)
            fanout(i, f'add_audio_mappings{suffix}', 0x002C, edit)
        if i == 0:
            # Only the first SET of a value notifies: the image's one rate, the configuration in use.
            fanout(i, 'set_sampling_rate', 0x0014, f.be(2, 2) + f.be(0, 2) + rate)
            if answering:
                fanout(i, 'set_configuration', 0x0006, f.be(0, 2) + f.be(0, 2))
        if answering:
            # MSRP_ACC_LAT_VALID (7.4.15.1) on STREAM_OUTPUT 0, a new latency on each interface.
            info = f.be(6, 2) + f.be(0, 2) + f.be(0x2000_0000, 4) + bytes(16) + f.be(1_000_000 + i, 4)
            fanout(i, 'set_stream_info', 0x000E, info.ljust(84, b'\0'))
        # LOCK_ENTITY (7.4.2.1) acquired, then released: its notice's first halfwords are its flags.
        fanout(i, 'lock_entity', 0x0001, f.be(0, 4) + f.be(0, 8) + f.be(0, 2) + f.be(0, 2))
        fanout(i, 'unlock_entity', 0x0001, f.be(1, 4) + f.be(0, 8) + f.be(0, 2) + f.be(0, 2))
    if answering:
        # A cross-channel fan-out: BIND_RX's response, then its STREAM_INPUT's GET_STREAM_INFO
        # notice to every registration (H-NOTIFY; Milan v1.2 Table 5.22).
        for i in ifs:
            g.probe(Probe(f'aecp_fanout.bind_rx_stream_info.if{i}', 'BIND_RX -> GET_STREAM_INFO notice', 'notify',
                          f'rxc:{acmp}', [f'resp:{acmp}:{0x5f00 + i:x}', f'notify:{aecp}:000f:5:{i}'],
                          recipients=everyone),
                    f'frame {i} {acmp_cmd(p, "BIND_RX", i, 0x5f00 + i).hex()}',
                    wait=f'tx {aecp} {len(everyone)} within {200 * MS}')
    return [g]


def maap_groups(p: Point) -> list[Group]:
    """MAAP (IEEE 1722-2016 Annex B): probing, announce and the DEFEND of a conflicting PROBE."""
    maap = CH['maap']
    g = Group('maap', sim_ms=3500 * p.interfaces)
    ready(g, p, link=False)
    for i in range(p.interfaces):
        slot = 2 * p.interfaces + i
        g.probe(Probe(f'maap.probe1.if{i}', 'first PROBE (LINK_UP)', 'maap', f'pad:LINK:{i}', [f'tx:{maap}'],
                      expect=f'maap_type:{f.MAAP_PROBE}'), f'link {i} 1',
                wait=f'tx {maap} 1 within {100 * MS}', settle='')
        for n in (2, 3):
            g.probe(Probe(f'maap.probe{n}.if{i}', 'PROBE retransmission (TMR expiry)', 'maap', f'deadline:{slot}',
                          [f'maap:{maap}:{f.MAAP_PROBE}'], expect=f'maap_type:{f.MAAP_PROBE}',
                          path='maap.probe_retransmission'),
                    wait=f'tx {maap} 1 within {800 * MS}', settle='')
        # The last retransmission and the ANNOUNCE leave on the same expiry (the core's B.3 machine).
        g.together([(Probe(f'maap.probe4.if{i}', 'last PROBE retransmission (TMR expiry)', 'maap',
                           f'deadline:{slot}', [f'maap:{maap}:{f.MAAP_PROBE}'], expect=f'maap_type:{f.MAAP_PROBE}'),
                     []),
                    (Probe(f'maap.announce.if{i}', 'ANNOUNCE (TMR expiry)', 'maap', f'deadline:{slot}',
                           [f'maap:{maap}:{f.MAAP_ANNOUNCE}'], expect=f'maap_type:{f.MAAP_ANNOUNCE}'), [])],
                   [f'tx {maap} 2 within {800 * MS}'])
        # Another entity PROBEs the announced range (B.3.5.5): this entity DEFENDs it (B.3.6.6).
        g.probe(Probe(f'maap.defend.if{i}', 'conflicting PROBE -> DEFEND', 'maap', f'rxc:{maap}', [f'tx:{maap}'],
                      expect=f'maap_type:{f.MAAP_DEFEND}'),
                f'reply {i} {maap} 15:{f.MAAP_ANNOUNCE:02x} 6={BRIDGE_MAC:012x} 15={f.MAAP_PROBE:02x}',
                wait=f'tx {maap} 1 within {50 * MS}')
    return [g]


def srp_groups(p: Point) -> list[Group]:
    """SRP on lwSRP: startup declarations, Listener Ready to licence, malformed, Domain."""
    srp = CH['srp']
    g = Group('srp', sim_ms=4500)
    ready(g, p, link=False)
    for i in range(p.interfaces):
        g.probe(Probe(f'srp.startup.if{i}', 'startup declarations (LINK_UP)', 'srp', f'pad:LINK:{i}',
                      [f'tx:{srp}:2'], expect='srp_frames'),
                f'link {i} 1', wait=f'tx {srp} 2 within {100 * MS}')
    # Listener Ready grants a licence only to an Advertise, after MAAP has allocated the address.
    g.add(f'wait cycles {2600 * MS}', 'wait quiet 3 within 2000000')
    for i in range(p.interfaces):
        sid = (p.mac << 16) | 0
        ready_listener = f.mrp_message(3, f.be(sid, 8), [1], four_packed=[2])
        # The fixture's sources stay unallocated (ctrl_aecp_image.c), so they are declared as
        # Talker Failed and no licence follows: the path ends at the record's release.
        g.probe(Probe(f'srp.listener_ready.if{i}', 'Listener Ready RX (registrar)', 'srp', f'rxc:{srp}',
                      [f'pass_end:{srp}']),
                f'frame {i} {f.msrp(BRIDGE_MAC, [ready_listener]).hex()}', wait=f'cycles {30 * MS}')
        bad = bytearray(f.msrp(BRIDGE_MAC, [f.mrp_message(3, f.be(sid, 8), [1], four_packed=[2])]))
        bad[29] = 216                     # a reserved ThreePackedEvents value (10.8.2.10)
        g.probe(Probe(f'srp.malformed.if{i}', 'malformed MRPDU discard', 'srp', f'rxc:{srp}', [f'pass_end:{srp}']),
                f'frame {i} {bytes(bad).hex()}', wait=f'cycles {30 * MS}')
        domain = f.mrp_message(4, f.domain_value(6, 4, 3), [1])
        g.probe(Probe(f'srp.domain.if{i}', 'Domain RX -> declarations (JoinTime wait)', 'srp', f'rxc:{srp}',
                      [f'pub:{pub_word(i, "SR_DOMAIN")}', f'tx:{srp}'], wait_ms=200.0),
                f'frame {i} {f.msrp(BRIDGE_MAC, [domain]).hex()}', wait=f'tx {srp} 1 within {300 * MS}')
    return [g]


def admission(channel: str, frame: bytes) -> dict:
    """What KL_mbx_rx admits of a channel's records of this frame's size.

    The token bucket starts full, passes burst records back to back and then
    refills one per refill_ms (KL_mbx_rx.sv, buckets); the ring holds room
    records of this size whatever the rate. So room bounds what the ring can
    hold, and at_once = min(burst, room) is what one instant admits. Where
    the burst is below the room (bounded False), sustained arrivals at the
    refill rate can fill the ring past its burst, so a backlog of at_once
    records is an observation, never a bound.
    """
    ch = CONTRACT.channels[CH[channel]]
    words = len(CONTRACT.rx_header) + (len(frame) + 3) // 4
    room = ch.rx_words // words
    return dict(burst=ch.burst, refill_ms=ch.refill_ms, record_words=words, room=room,
                at_once=min(ch.burst, room), bounded=room <= ch.burst)


def listener_ready(p: Point) -> bytes:
    """A bridge's Listener Ready for this entity's first stream (IEEE 802.1Q-2018 35.2.2.8)."""
    sid = (p.mac << 16) | 0
    return f.msrp(BRIDGE_MAC, [f.mrp_message(3, f.be(sid, 8), [1], four_packed=[2])])


#: A MAAPDU's size (B.2), the size of the conflicting PROBEs maap_conflict() replies.
MAAP_PDU = f.maap(f.MAAP_PROBE, BRIDGE_MAC, (0, 1))


def maap_conflict(interface: int, select: int = f.MAAP_ANNOUNCE) -> str:
    """A bridge's PROBE of the range the interface's MAAP last sent (IEEE 1722-2016 B.3.6.6).

    It copies that interface's own last ANNOUNCE (or PROBE), so its range
    overlaps the filter's MAAP range; only the source and the type change.
    In DEFEND the entity answers it with a DEFEND, in PROBE it re-probes.
    """
    return (f'reply {interface} {CH["maap"]} 15:{select:02x} on={interface} '
            f'6={BRIDGE_MAC:012x} 15={f.MAAP_PROBE:02x}')


def gm_run(g: Group, p: Point, count: int = 15) -> None:
    """Grandmaster changes back to back, alternating the interfaces: GM events of the load."""
    for n in range(count):
        g.add(f'gm {n % p.interfaces} 0a0b0c0dfffe{n:04x} 0', 'wait cycles 8')
    g.load['GM'] = g.load.get('GM', 0) + count


def composed_load(g: Group, p: Point, own: str, counts: dict[str, int] | None = None,
                  maap_select: int = f.MAAP_ANNOUNCE) -> None:
    """Every receive channel's admitted burst at once, but own's, which the row loads itself.

    Each channel is offered admission()'s at_once records (counts overrides
    a channel's number), alternating the interfaces; ACMP's go to sink 0,
    on interface 0. MAAP's are conflicting PROBEs of each interface's own
    range, so the range filter passes them; SRP's are srp_groups' Listener
    Ready. grade.py requires the window to commit exactly this population.
    """
    disc = f.adp(f.ADP_DISCOVER, 0, CTL_MAC, f.Adp(valid_time=0))
    read = lambda seq: f.read_descriptor(f.Aem(p.entity_id, CTL1, CTL_MAC, p.mac, seq), 0, 0)
    get = lambda seq: acmp_cmd(p, 'GET_RX_STATE', 0, seq)
    srp = listener_ready(p)
    frames = {'adp': lambda n: (f'frame {n % p.interfaces} {disc.hex()}', disc),
              'aecp': lambda n: (f'frame {n % p.interfaces} {read(0x7100 + n).hex()}', read(0)),
              'maap': lambda n: (maap_conflict(n % p.interfaces, maap_select), MAAP_PDU),
              'srp': lambda n: (f'frame {n % p.interfaces} {srp.hex()}', srp),
              'acmp': lambda n: (f'frame 0 {get(0x7200 + n).hex()}', get(0))}
    for channel, make in frames.items():
        if channel == own:
            continue
        number = (counts or {}).get(channel, admission(channel, make(0)[1])['at_once'])
        for n in range(number):
            g.offer(channel, *make(n))


def announced(g: Group) -> None:
    """MAAP's PROBEs and ANNOUNCE on every interface after ready()'s link up (B.3.4.2, Table B.8)."""
    g.add(f'wait cycles {2000 * MS}', 'wait quiet 3 within 2000000')


def bound_talker_groups(p: Point) -> list[Group]:
    """The bound-talker row (an ENTITY_AVAILABLE behind the adp ring), at the burst and with the
    bucket refilling up to the ring's room (backlog-adp-refill, observed)."""
    acmp, adp = CH['acmp'], CH['adp']
    disc = f.adp(f.ADP_DISCOVER, 0, CTL_MAC, f.Adp(valid_time=0))
    gone = f.adp(f.ADP_DEPARTING, TALKER_A, TALKER_A_MAC, f.Adp(valid_time=0, talker_sources=1, talker_caps=0x4001))
    avail = f.adp(f.ADP_AVAILABLE, TALKER_A, TALKER_A_MAC, f.Adp(valid_time=10, talker_sources=1, talker_caps=0x4001))
    out = []
    # The bound-talker term: sink 0 bound to TALKER_A and waiting for it (PRB_W_AVAIL, reached
    # through its DEPARTING as acmp-disc does), then the loads ending with its AVAILABLE.
    last_gm = max(n for n in range(15) if n % p.interfaces == 0)
    # It carries interface 0's grandmaster after the event run (Milan v1.2 Table 5.54 discards a mismatch).
    current = f.adp(f.ADP_AVAILABLE, TALKER_A, TALKER_A_MAC,
                    f.Adp(valid_time=10, talker_sources=1, talker_caps=0x4001, gm_id=0x0A0B0C0DFFFE0000 + last_gm))
    at_once, room = admission('adp', disc)['at_once'], admission('adp', disc)['room']
    for name, refills in (('backlog-adp', 0), ('backlog-adp-refill', room - at_once)):
        g = Group(name, sim_ms=4000)
        ready(g, p)
        announced(g)
        g.add(f'frame 0 {acmp_cmd(p, "BIND_RX", 0, 0x7000).hex()}', f'wait tx {acmp} 2 within {20 * MS}',
              'wait quiet 3 within 2000000', f'frame 0 {avail.hex()}', 'wait quiet 3 within 2000000',
              f'frame 0 {gone.hex()}', f'wait cycles {50 * MS}', 'wait quiet 3 within 2000000', 'gap 1',
              'mark composed')
        gm_run(g, p)
        composed_load(g, p, own='adp')
        for n in range(at_once - 1):
            g.offer('adp', f'frame {n % p.interfaces} {disc.hex()}', disc)
        # The refill leg: one more record per refill period, up to the ring's room with the input.
        refill = CONTRACT.channels[adp].refill_ms
        for n in range(refills):
            g.add(f'wait cycles {refill * MS}')
            g.offer('adp', f'frame {n % p.interfaces} {disc.hex()}', disc)
        if refills:
            g.add(f'wait cycles {refill * MS}')
            probe = Probe('backlog.adp_available_refill.if0',
                          'an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed)', 'disc',
                          f'rxc:{adp}', [f'arm:{p.interfaces}'], until='composed_end')
        else:
            probe = Probe('backlog.adp_available.if0', 'an ENTITY_AVAILABLE behind a full adp ring', 'disc',
                          f'rxc:{adp}', [f'arm:{p.interfaces}'], until='composed_end')
        g.probe(probe, f'frame 0 {current.hex()}', wait=f'tmr {p.interfaces} 1 within {400 * MS}',
                settle='quiet 3 within 50000000')
        g.load['adp'] += 1
        g.add('mark composed_end')
        out.append(g)
    return out


#: The responses owed ahead of the owed-frame row's (MAILBOX_SPLIT.md:753-758, A3).
OWED_AHEAD = 7


def owed_group(p: Point) -> Group:
    """The owed-frame row (a response with 7 frames owed ahead of it) under the composed load."""
    acmp = CH['acmp']
    get = lambda seq: acmp_cmd(p, 'GET_RX_STATE', 0, seq)
    # A response with 7 frames owed ahead of it (A3): the egress held and the TX ring filled
    # with responses; then, the token bucket refilled, the load arrives: seven commands, the
    # probe and the rest of the ACMP ring's admitted burst behind it, so the probe's response
    # is the eighth owed. The egress returns 60 ms later.
    g = Group('backlog-owed', sim_ms=4000)
    ready(g, p)
    announced(g)
    tx_room = CONTRACT.channels[acmp].tx_words // (len(CONTRACT.tx_header) + (len(get(0)) + 3) // 4)
    g.add('txready 0', f'wait cycles {2 * MS}')
    for n in range(tx_room):
        g.add(f'frame 0 {get(0x7300 + n).hex()}')
    g.add(f'wait tx {acmp} {tx_room} within {300 * MS}', f'wait cycles {50 * MS}', 'gap 1', 'mark composed')
    gm_run(g, p)
    composed_load(g, p, own='acmp')
    for n in range(OWED_AHEAD):
        g.offer('acmp', f'frame 0 {get(0x7380 + n).hex()}', get(0))
    behind = admission('acmp', get(0))['at_once'] - OWED_AHEAD - 1
    probe = Probe('backlog.owed.if0', 'a response with 7 frames owed ahead of it', 'acmp', f'rxc:{acmp}',
                  [f'resp:{acmp}:{0x7380 + OWED_AHEAD:x}'], until='composed_end', also_from='room',
                  owed=tuple(0x7380 + n for n in range(OWED_AHEAD)))
    g.probe(probe, f'frame 0 {get(0x7380 + OWED_AHEAD).hex()}', wait=f'drained within {10 * MS}', settle='')
    g.load['acmp'] += 1
    # Each command behind the input is a path too: the core owes at most ACMP_OWED_MAX
    # responses (tsn-c-stack acmp.h), so one it takes beyond them may never be answered.
    for n in range(behind):
        name = f'backlog.owed_behind{n}.if0'
        g.probes.append(Probe(name, 'an ACMP command behind the owed input', 'acmp', f'rxc:{acmp}',
                              [f'resp:{acmp}:{0x7390 + n:x}'], until='composed_end', path='backlog.owed_behind',
                              may_drop=True))
        g.add(f'mark {name}')
        g.offer('acmp', f'frame 0 {get(0x7390 + n).hex()} {name}', get(0))
    g.add(f'wait drained within {10 * MS}', f'wait cycles {60 * MS}', 'mark room', 'txready 1',
          f'wait tx {acmp} {OWED_AHEAD + 1 + behind} within {300 * MS}', 'wait quiet 3 within 50000000',
          'mark composed_end')
    return g


def backlog_groups(p: Point) -> list[Group]:
    """The four backlog rows (MAILBOX_SPLIT.md:753-758), each under the composed maximum load.

    Every group's composed window carries every receive channel's admitted
    burst at once (composed_load, MAAP and SRP included) and fifteen
    grandmaster changes, and each row's input is the last of its own
    channel's records. The event and ACMP rows are at their rings' room, a
    bound; the ADP ring takes its burst, fewer records than it holds, so its
    row is observed at that backlog, and backlog-adp-refill adds the bucket's
    refill-rate arrivals up to the ring's room before the input (observed,
    not a bound). The bound-talker rows bind a sink first; the owed-frame
    row holds the egress while its commands arrive with the load.
    """
    acmp = CH['acmp']
    get = lambda seq: acmp_cmd(p, 'GET_RX_STATE', 0, seq)
    out = []

    g = Group('backlog', sim_ms=4000)
    ready(g, p)
    announced(g)
    g.add('gap 1', 'mark composed')
    gm_run(g, p)
    g.probe(Probe('backlog.event.if0', 'an event behind 15 others', 'adp', 'pad:LINK:0', ['cancel:0'],
                  until='composed_end'), 'link 0 0', wait='cycles 1', settle='')
    g.load['LINK'] = 1
    composed_load(g, p, own='acmp')
    count = admission('acmp', get(0))['at_once']
    for n in range(count - 1):
        g.offer('acmp', f'frame 0 {get(0x7200 + n).hex()}', get(0))
    g.probe(Probe('backlog.acmp_command.if0', 'an ACMP command behind a full acmp ring', 'acmp', f'rxc:{acmp}',
                  [f'resp:{acmp}:72ff'], until='composed_end'), f'frame 0 {get(0x72ff).hex()}',
            wait=f'tx {acmp} {count} within {300 * MS}', settle='quiet 3 within 50000000')
    g.load['acmp'] += 1
    g.add('mark composed_end')
    out.append(g)

    out += bound_talker_groups(p)
    out.append(owed_group(p))
    return out


def control_groups(p: Point) -> list[Group]:
    """The planted over-budget control's path: RCV_ADP_DISCOVER in WAITING to its TMR_DELAY arm.

    The arm is made by ADP's receive handler after its work, so a slower handler
    delays it. With the ordinary image the path fits T_svc; with build.py's
    slow-adp-rx it must miss it, by name (run.py --mutation slow-adp-rx).
    """
    adp = CH['adp']
    g = Group('control', sim_ms=2800)
    ready(g, p, link=False)
    advertised(g, p)
    disc = f.adp(f.ADP_DISCOVER, 0, CTL_MAC, f.Adp(valid_time=0))
    g.probe(Probe('control.discover.if0', 'RCV_ADP_DISCOVER (control)', 'adp', f'rxc:{adp}', ['arm:0'], accesses=31,
                  path='adp.discover'), f'frame 0 {disc.hex()}', wait=f'tmr 0 1 within {300 * MS}')
    return [g]


#: NOW_MS at which build.py's shutdown-entry variant disables ADP, once.
SHUTDOWN_MS = 2500


def shutdown_groups(p: Point) -> list[Group]:
    """SHUTDOWN -> ENTITY_DEPARTING committed (MAILBOX_SPLIT.md:502), through a test-only entry.

    The linked image never disables ADP, so this path has no input in it.
    build.py's shutdown-entry variant (a scratch copy of the fixture, never the
    formal image) adds a poll that calls adp_mbx_set_enable(false) once, at
    NOW_MS SHUTDOWN_MS. The path starts at that call's entry and ends at each
    interface's ENTITY_DEPARTING commit (IEEE 1722.1-2021 6.2.5.2.2). The
    control group's probe is another instance of the same path, adp.shutdown,
    which slow-adp-shutdown must push over T_svc (run.py --mutation
    slow-adp-shutdown).
    """
    adp = CH['adp']
    out = []
    for name, prefix, ifs in (('adp-shutdown', 'adp', range(p.interfaces)), ('control-shutdown', 'control', [0])):
        g = Group(name, sim_ms=SHUTDOWN_MS + 300)
        ready(g, p)
        g.together([(Probe(f'{prefix}.shutdown.if{i}', 'SHUTDOWN', 'adp', 'entry:adp_mbx_set_enable',
                           [f'adp:{adp}:{f.ADP_DEPARTING}'], accesses=29, expect='adp_departing',
                           path='adp.shutdown'), []) for i in ifs],
                   [f'ms {SHUTDOWN_MS + 50}'])
        out.append(g)
    return out


def boot_fault_groups() -> list[Group]:
    """The region-decode control: 30 ms of boot and no probe. With the regions as built the CPU
    faults on its first fetch above 0x8000 (cause 1) and restarts; grade.py refuses the trap."""
    g = Group('boot-fault', sim_ms=30)
    g.add('wait ms 30')
    return [g]


def fixture_groups(p: Point) -> list[Group]:
    """One short boot whose probes use every start and end marker once: the self-test's trace.

    The bind comes last: after it the fixture's AECP retries its change notices
    every millisecond, and the earlier probes stay clear of that.
    """
    acmp, adp, aecp, srp = CH['acmp'], CH['adp'], CH['aecp'], CH['srp']
    g = Group('fixture', sim_ms=2500)
    ready(g, p, link=False)
    g.probe(Probe('fixture.link_up.if0', 'LINK_UP', 'adp', 'pad:LINK:0', ['arm:0'], accesses=11,
                  path='adp.link_up'),
            'link 0 1', wait=f'tmr 0 1 within {300 * MS}')
    g.add(f'wait cycles {100 * MS}', 'wait quiet 3 within 2000000')
    sid = (p.mac << 16) | 0
    bad = bytearray(f.msrp(BRIDGE_MAC, [f.mrp_message(3, f.be(sid, 8), [1], four_packed=[2])]))
    bad[29] = 216
    g.probe(Probe('fixture.malformed.if0', 'malformed MRPDU discard', 'srp', f'rxc:{srp}', [f'pass_end:{srp}'],
                  path='srp.malformed'),
            f'frame 0 {bytes(bad).hex()}', wait=f'cycles {30 * MS}')
    g.add(f'frame 0 {f.aem_command(f.Aem(p.entity_id, CTL1, CTL_MAC, p.mac, 0x6100), 0x0024, bytes(4)).hex()}',
          f'wait tx {aecp} 1 within {50 * MS}', 'wait quiet 3 within 2000000')
    # A short composed window: one record on every receive channel and two GM events, so the
    # self-test pins a composed maximum and its population.
    g.add('gap 1', 'mark composed')
    gm_run(g, p, 2)
    composed_load(g, p, own='', counts={c: 1 for c in CH}, maap_select=f.MAAP_PROBE)
    g.add('wait quiet 3 within 2000000', 'mark composed_end')
    name = b'fixture'.ljust(64, b'\0')
    frame = f.aem_command(f.Aem(p.entity_id, CTL2, CTL_MAC, p.mac, 0x6101), 0x0010, bytes(8) + name)
    # The fan-out's markers on one registration: the capacity's path is aecp_fanout.set_name.
    g.probe(Probe('fixture.set_name.if0', 'SET_NAME fan-out to one registered controller', 'notify', f'rxc:{aecp}',
                  [f'resp:{aecp}:6101', f'notify:{aecp}:0010:0:0'], expect='aecp_response',
                  recipients=((CTL1, 0),), path='fixture.set_name_one_recipient'),
            f'frame 0 {frame.hex()}', wait=f'tx {aecp} 2 within {50 * MS}')
    g.probe(Probe('fixture.link_down.if0', 'LINK_DOWN', 'adp', 'pad:LINK:0', ['cancel:0'], accesses=9,
                  path='adp.link_down'),
            'link 0 0', wait=f'tmr 0 2 within {300 * MS}')
    g.probe(Probe('fixture.bind_rx.if0', 'BIND_RX', 'acmp', f'rxc:{acmp}',
                  [f'resp:{acmp}:4100', f'acmp_cmd:{acmp}:PROBE_TX', 'arm:1', f'pub:{binding_word(0, 0)}'],
                  accesses=77, expect='acmp_status:BIND_RX_RESPONSE:0', path='acmp.bind_rx'),
            f'frame 0 {acmp_cmd(p, "BIND_RX", 0, 0x4100).hex()}', wait=f'tx {acmp} 2 within {50 * MS}')
    g.probe(Probe('fixture.tmr_no_resp1.if0', 'TMR_DELAY, or the first TMR_NO_RESP', 'acmp', 'deadline:1',
                  [f'acmp_cmd:{acmp}:PROBE_TX', 'arm:1'], accesses=35, path='acmp.tmr_no_resp1'),
            wait=f'tx {acmp} 1 within {400 * MS}', settle='')
    # They carry interface 0's grandmaster after the window's GM run (Milan v1.2 Table 5.54 discards a mismatch).
    gm = 0x0A0B0C0DFFFE0001
    avail = f.adp(f.ADP_AVAILABLE, TALKER_A, TALKER_A_MAC,
                  f.Adp(valid_time=10, talker_sources=1, talker_caps=0x4001, gm_id=gm))
    gone = f.adp(f.ADP_DEPARTING, TALKER_A, TALKER_A_MAC,
                 f.Adp(valid_time=0, talker_sources=1, talker_caps=0x4001, gm_id=gm))
    g.add(f'frame 0 {avail.hex()}', f'wait cycles {60 * MS}')
    g.probe(Probe('fixture.entity_departing.if0', 'ENTITY_DEPARTING from its RX_HEAD (H-DISC)', 'disc', f'rxc:{adp}',
                  ['tmr:1'], accesses=29, path='acmp.entity_departing'),
            f'frame 0 {gone.hex()}', wait=f'cycles {100 * MS}', settle='')
    return [g]


def all_groups(p: Point, build: dict) -> list[Group]:
    """Every group of a point's build, longest first; the shutdown-entry variant has only its own."""
    if build.get('variant') == 'shutdown-entry':
        return shutdown_groups(p)
    groups = [*acmp_groups(p), *adp_groups(p), *aecp_groups(p, build), *aecp_fanout_groups(p, build),
              *maap_groups(p), *srp_groups(p), *backlog_groups(p), *control_groups(p)]
    return sorted(groups, key=lambda g: -g.sim_ms) + (fixture_groups(p) if p.interfaces == 1 else [])
