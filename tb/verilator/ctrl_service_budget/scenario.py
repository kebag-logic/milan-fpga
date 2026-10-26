# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The stimulus groups of the budget and the probes each measures (#665 S2).

A group is one boot of the test SoC and a script of steps; sim_main.cpp
runs it. A probe is one measured path: a `mark` line names it, then its
stimulus, then a bounded wait for its completion. grade.py reads the start
and the end of each probe off the observation log by the probe's rules:

  start  rxc:<ch>         the fabric's receive commit (RX_HEAD) on the channel
         pad:LINK:<if>    the link level changing at the mailbox input
         pad:GM:<if>      the grandmaster-change pulse at the mailbox input
         deadline:<slot>  the armed deadline of the slot's next TIMER record
         tick             the occurrence of the TICK record a pass takes
  end    tx:<ch>[:n]      the n-th accepted TX_HEAD write on the channel
         arm:<slot>       a TMR_CMD arm of the slot; cancel:<slot> its cancel
         tmr:<slot>       any TMR_CMD write of the slot
         resp:<ch>:<seq>  the TX record on the channel answering sequence_id seq
         notify:<ch>      an unsolicited AECP response (IEEE 1722.1-2021 7.5.2)
         acmp_cmd:<ch>:<type>  an ACMP command the firmware originates, e.g. PROBE_TX
         rxtail:<ch>      the RX_TAIL write that releases the record
         pass_end:<ch>    the end of the pass that took the record: its handler runs
                          after the release, inside that pass (ctrl_loop.c service_rx)
         pub:<word>       a write of that publication word

A probe's frames carry its name as their tag, so its start is the commit of
its own frame even when other frames share the ring; a probe may bound its
search by a later mark (until) when probes overlap on purpose.

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


@dataclass
class Group:
    name: str
    steps: list[str] = field(default_factory=list)
    probes: list[Probe] = field(default_factory=list)
    sim_ms: int = 0      # the simulated time the script needs, for the run's bound

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
    """AECP: every descriptor read, the getters and setters, the notification fan-out."""
    aecp = CH['aecp']
    g = Group('aecp', sim_ms=2500)
    ready(g, p)
    seq = [0x6100]

    def cmd(i: int, name: str, command_type: int, payload: bytes, count: int = 1, controller: int = CTL1) -> None:
        """One AEM command probe; count 2 also waits for the notification a state change sends."""
        frame = f.aem_command(f.Aem(p.entity_id, controller, CTL_MAC, p.mac, seq[0]), command_type, payload)
        ends = [f'resp:{aecp}:{seq[0]:x}'] + ([f'notify:{aecp}'] if count > 1 else [])
        seq[0] += 1
        family = 'notify' if count > 1 else 'aecp'
        g.probe(Probe(f'aecp.{name}.if{i}', name, family, f'rxc:{aecp}', ends, expect='aecp_response'),
                f'frame {i} {frame.hex()}', wait=f'tx {aecp} {count} within {50 * MS}')

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
        # A state change by another controller: the response, then the notification to CTL1 (7.5.2).
        name = f'budget if{i}'.encode().ljust(64, b'\0')   # a new value: an identical SET does not notify
        cmd(i, 'set_name', 0x0010, f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + name,
            count=2, controller=CTL2)
        # LOCK_ENTITY (7.4.2.1): flags, locked_id, descriptor_type and descriptor_index (the ENTITY).
        cmd(i, 'lock_entity', 0x0001, f.be(0, 4) + f.be(0, 8) + f.be(0, 2) + f.be(0, 2), controller=CTL2)
        cmd(i, 'unlock_entity', 0x0001, f.be(1, 4) + f.be(0, 8) + f.be(0, 2) + f.be(0, 2), controller=CTL2)
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
                          [f'maap:{maap}:{f.MAAP_PROBE}'], expect=f'maap_type:{f.MAAP_PROBE}'),
                    wait=f'tx {maap} 1 within {800 * MS}', settle='')
        # The last retransmission and the ANNOUNCE leave on the same expiry (the core's B.3 machine).
        g.together([(Probe(f'maap.probe4.if{i}', 'PROBE retransmission (TMR expiry)', 'maap', f'deadline:{slot}',
                           [f'maap:{maap}:{f.MAAP_PROBE}'], expect=f'maap_type:{f.MAAP_PROBE}'), []),
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


def admitted(channel: str, frame: bytes) -> int:
    """Records of this frame a channel admits back to back: its token-bucket burst or
    its receive ring's room, whichever is smaller (the contract's burst and rx_words)."""
    ch = CONTRACT.channels[CH[channel]]
    return min(ch.burst, ch.rx_words // (len(CONTRACT.rx_header) + (len(frame) + 3) // 4))


def backlog_groups(p: Point) -> list[Group]:
    """The four backlog rows (MAILBOX_SPLIT.md:753-758) under the composed maximum load.

    Every receive ring is offered back to back exactly what it admits (admitted()),
    the event ring a run of grandmaster changes on every interface, and each row's
    input is the last of its kind. The owed-frame row holds the egress while eight
    commands arrive. The bound-talker row binds a sink first, in its own group.
    """
    acmp, adp, aecp = CH['acmp'], CH['adp'], CH['aecp']
    disc = f.adp(f.ADP_DISCOVER, 0, CTL_MAC, f.Adp(valid_time=0))
    avail = f.adp(f.ADP_AVAILABLE, TALKER_A, TALKER_A_MAC, f.Adp(valid_time=10, talker_sources=1, talker_caps=0x4001))
    get = lambda seq: acmp_cmd(p, 'GET_RX_STATE', 0, seq)
    read = lambda seq: f.read_descriptor(f.Aem(p.entity_id, CTL1, CTL_MAC, p.mac, seq), 0, 0)
    announce = lambda n: f.maap(f.MAAP_ANNOUNCE, BRIDGE_MAC, (0x91E0F000A000 + 16 * n, 8))

    def load(g: Group) -> None:
        """The event run: fifteen grandmaster changes, alternating the interfaces."""
        for n in range(15):
            g.add(f'gm {n % p.interfaces} 0a0b0c0dfffe{n:04x} 0', 'wait cycles 8')

    out = []
    g = Group('backlog', sim_ms=3000)
    ready(g, p)
    g.add('gap 1', 'mark composed')
    load(g)
    g.probe(Probe('backlog.event.if0', 'an event behind 15 others', 'adp', 'pad:LINK:0', ['cancel:0'],
                  until='composed_end'), 'link 0 0', wait='cycles 1', settle='')
    for n in range(admitted('adp', disc)):
        g.add(f'frame {n % p.interfaces} {disc.hex()}')
    for n in range(admitted('aecp', read(0))):
        g.add(f'frame {n % p.interfaces} {read(0x7100 + n).hex()}')
    for n in range(admitted('maap', announce(0))):
        g.add(f'frame {n % p.interfaces} {announce(n).hex()}')
    count = admitted('acmp', get(0))
    for n in range(count - 1):
        g.add(f'frame 0 {get(0x7200 + n).hex()}')
    g.probe(Probe('backlog.acmp_command.if0', 'an ACMP command behind a full acmp ring', 'acmp', f'rxc:{acmp}',
                  [f'resp:{acmp}:72ff'], until='composed_end'), f'frame 0 {get(0x72ff).hex()}',
            wait=f'tx {acmp} {count} within {200 * MS}', settle='quiet 3 within 50000000')
    g.add('mark composed_end', 'gap 20', f'wait cycles {50 * MS}')
    # A response with 7 frames owed ahead of it (A3): the egress held, the TX ring filled with
    # responses, then, the token bucket refilled, seven more commands and the probe arrive.
    tx_room = CONTRACT.channels[acmp].tx_words // (len(CONTRACT.tx_header) + (len(get(0)) + 3) // 4)
    g.add('txready 0', f'wait cycles {2 * MS}')
    for n in range(tx_room):
        g.add(f'frame 0 {get(0x7300 + n).hex()}')
    g.add(f'wait tx {acmp} {tx_room} within {300 * MS}', f'wait cycles {50 * MS}')
    for n in range(7):
        g.add(f'frame 0 {get(0x7380 + n).hex()}')
    g.probe(Probe('backlog.owed.if0', 'a response with 7 frames owed ahead of it', 'acmp', f'rxc:{acmp}',
                  [f'resp:{acmp}:7387'], until='owed_end', also_from='room'),
            f'frame 0 {get(0x7387).hex()}', f'wait drained within {10 * MS}',
            f'wait cycles {60 * MS}', 'mark room', 'txready 1', wait=f'tx {acmp} 8 within {300 * MS}',
            settle='quiet 3 within 2000000')
    g.add('mark owed_end')
    out.append(g)
    # The bound-talker term: sink 0 bound to TALKER_A and waiting for it (PRB_W_AVAIL, reached
    # through its DEPARTING as acmp-disc does), then the ADP burst ending with its AVAILABLE.
    gone = f.adp(f.ADP_DEPARTING, TALKER_A, TALKER_A_MAC, f.Adp(valid_time=0, talker_sources=1, talker_caps=0x4001))
    g = Group('backlog-adp', sim_ms=2500)
    ready(g, p)
    g.add(f'frame 0 {acmp_cmd(p, "BIND_RX", 0, 0x7000).hex()}', f'wait tx {acmp} 2 within {20 * MS}',
          'wait quiet 3 within 2000000', f'frame 0 {avail.hex()}', 'wait quiet 3 within 2000000',
          f'frame 0 {gone.hex()}', f'wait cycles {50 * MS}', 'wait quiet 3 within 2000000', 'gap 1',
          'mark composed')
    load(g)
    for n in range(admitted('adp', disc) - 1):
        g.add(f'frame {n % p.interfaces} {disc.hex()}')
    # It carries interface 0's grandmaster after the event run (Milan v1.2 Table 5.54 discards a mismatch).
    last_gm = max(n for n in range(15) if n % p.interfaces == 0)
    current = f.adp(f.ADP_AVAILABLE, TALKER_A, TALKER_A_MAC,
                    f.Adp(valid_time=10, talker_sources=1, talker_caps=0x4001, gm_id=0x0A0B0C0DFFFE0000 + last_gm))
    g.probe(Probe('backlog.adp_available.if0', 'an ENTITY_AVAILABLE behind a full adp ring', 'disc', f'rxc:{adp}',
                  [f'arm:{p.interfaces}'], until='composed_end'), f'frame 0 {current.hex()}',
            wait=f'tmr {p.interfaces} 1 within {300 * MS}', settle='quiet 3 within 50000000')
    g.add('mark composed_end')
    out.append(g)
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
    g.probe(Probe('control.discover.if0', 'RCV_ADP_DISCOVER (control)', 'adp', f'rxc:{adp}', ['arm:0'], accesses=31),
            f'frame 0 {disc.hex()}', wait=f'tmr 0 1 within {300 * MS}')
    return [g]


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
    g.probe(Probe('fixture.link_up.if0', 'LINK_UP', 'adp', 'pad:LINK:0', ['arm:0'], accesses=11),
            'link 0 1', wait=f'tmr 0 1 within {300 * MS}')
    g.add(f'wait cycles {100 * MS}', 'wait quiet 3 within 2000000')
    sid = (p.mac << 16) | 0
    bad = bytearray(f.msrp(BRIDGE_MAC, [f.mrp_message(3, f.be(sid, 8), [1], four_packed=[2])]))
    bad[29] = 216
    g.probe(Probe('fixture.malformed.if0', 'malformed MRPDU discard', 'srp', f'rxc:{srp}', [f'pass_end:{srp}']),
            f'frame 0 {bytes(bad).hex()}', wait=f'cycles {30 * MS}')
    g.add(f'frame 0 {f.aem_command(f.Aem(p.entity_id, CTL1, CTL_MAC, p.mac, 0x6100), 0x0024, bytes(4)).hex()}',
          f'wait tx {aecp} 1 within {50 * MS}', 'wait quiet 3 within 2000000')
    name = b'fixture'.ljust(64, b'\0')
    frame = f.aem_command(f.Aem(p.entity_id, CTL2, CTL_MAC, p.mac, 0x6101), 0x0010, bytes(8) + name)
    g.probe(Probe('fixture.set_name.if0', 'SET_NAME', 'notify', f'rxc:{aecp}', [f'resp:{aecp}:6101', f'notify:{aecp}'],
                  expect='aecp_response'), f'frame 0 {frame.hex()}', wait=f'tx {aecp} 2 within {50 * MS}')
    g.probe(Probe('fixture.link_down.if0', 'LINK_DOWN', 'adp', 'pad:LINK:0', ['cancel:0'], accesses=9),
            'link 0 0', wait=f'tmr 0 2 within {300 * MS}')
    g.probe(Probe('fixture.bind_rx.if0', 'BIND_RX', 'acmp', f'rxc:{acmp}',
                  [f'resp:{acmp}:4100', f'acmp_cmd:{acmp}:PROBE_TX', 'arm:1', f'pub:{binding_word(0, 0)}'],
                  accesses=77, expect='acmp_status:BIND_RX_RESPONSE:0'),
            f'frame 0 {acmp_cmd(p, "BIND_RX", 0, 0x4100).hex()}', wait=f'tx {acmp} 2 within {50 * MS}')
    g.probe(Probe('fixture.tmr_no_resp1.if0', 'TMR_DELAY, or the first TMR_NO_RESP', 'acmp', 'deadline:1',
                  [f'acmp_cmd:{acmp}:PROBE_TX', 'arm:1'], accesses=35),
            wait=f'tx {acmp} 1 within {400 * MS}', settle='')
    avail = f.adp(f.ADP_AVAILABLE, TALKER_A, TALKER_A_MAC, f.Adp(valid_time=10, talker_sources=1, talker_caps=0x4001))
    gone = f.adp(f.ADP_DEPARTING, TALKER_A, TALKER_A_MAC, f.Adp(valid_time=0, talker_sources=1, talker_caps=0x4001))
    g.add(f'frame 0 {avail.hex()}', f'wait cycles {60 * MS}')
    g.probe(Probe('fixture.entity_departing.if0', 'ENTITY_DEPARTING from its RX_HEAD (H-DISC)', 'disc', f'rxc:{adp}',
                  ['tmr:1'], accesses=29), f'frame 0 {gone.hex()}', wait=f'cycles {100 * MS}', settle='')
    return [g]


def all_groups(p: Point, build: dict) -> list[Group]:
    """Every group of a point, in the order the tables list them."""
    groups = [*acmp_groups(p), *adp_groups(p), *aecp_groups(p, build), *maap_groups(p), *srp_groups(p),
              *backlog_groups(p), *control_groups(p)]
    return sorted(groups, key=lambda g: -g.sim_ms) + (fixture_groups(p) if p.interfaces == 1 else [])
