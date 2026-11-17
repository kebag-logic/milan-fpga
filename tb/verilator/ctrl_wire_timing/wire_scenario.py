# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The wire-timing stimulus (#665, #868): each draw's frames at the MAC boundary, in wire_main.cpp's script.

The frames and identities are the CPU budget harness's (frames.py and
scenario.py, imported read only). Each draw: a controller (CTL1) binds this
entity's STREAM_INPUT 0 to a remote talker (TALKER_A), the talker answers the
PROBE_TX the bind causes with scenario.probe_answer's PROBE_TX_RESPONSE, the
controller unbinds, then sends one AEM command (AECP_COMMANDS, in turn). The
testbench sends the talker's answer a turnaround after the command's last byte
has left: the talker's and the network's own time, which differs per draw, as
does the bind's phase in a millisecond, so the draws meet the entity's loop at
different phases (Draw). Seed 0 steps both by fixed primes; another seed draws
them from its own generator. Every link is raised before the boot, so MAAP
acquires on interface 0 while the draws run (IEEE 1722-2016 B.3) and ADP
advertises (Milan v1.2 5.6.3.5).

THE LOAD (#868): the CPU budget harness's composed load
(scenario.composed_load), every receive channel's admitted burst at once but
the measured path's own, alternating the interfaces as it does. It is offered
right before each bind (ACMP's path) and each AEM command (AECP's), and a
lead before every deadline the firmware arms on interface 0's MAAP and ADP
timer slots (onarm), so the burst is in the loop when the timer expires. Three
parts differ from that harness's, each stated:
  - its ADP records are ENTITY_DISCOVERs for another entity: a global one
    restarts this entity's advertise cycle at every burst (Milan v1.2
    5.6.3.5.4), so no advertise period would ever complete under load; the
    frame, its channel and its parse to the target check are the same;
  - its MAAP records echo their interface's last ANNOUNCE as a conflicting
    PROBE, as that harness's do; wire_main.cpp keeps each echo's newest
    match, so the ANNOUNCE is found whenever one has been sent, and only
    before an interface's first ANNOUNCE are its echoes skipped (the LOAD
    line counts them per interface, and the grader finds a skip after it): a
    conflicting PROBE while probing restarts the acquisition (B.3.6.5) whose
    intervals are measured;
  - a deadline's burst leaves out the ACMP and AECP records, the channels
    whose received records the draws measure (DRAW_CHANNELS). That harness
    never loads a measured path's own channel, and a deadline's burst can land
    with a draw's command: the 1x1 campaign at 79997664d5 measured it twice,
    an ADP deadline's 12 GET_RX_STATEs filling ACMP's ring (room 12) 56 us
    before a BIND_RX (seed 3) and 0.26 us before a PROBE_TX_RESPONSE (seed 4),
    which KL_mbx then dropped. The draws' own bursts are whole.
The grandmaster changes of that harness's other rows are not part of the
composed load; interface 0's would need the gPTP plane tb_split_top builds off.

A run without load (none) offers none of it.

Script steps (wire_main.cpp):
  link <if> <0|1>                    the interface's link level
  wait ready | ms <n> | cycles <n> | now <ms> | sent <count> <off>:<byte>...
  frame <if> <tag> <hex>             a frame offered: at the MAC boundary (0), at KL_mbx's (past 0)
  reply <tag> <cycles> <off>:<byte>... <off>=<hex>...
                                     answer each frame sent at the MAC that matches;
                                     a rule replaces the one of its tag
  defload <name> <item>...           <if>/<hex>, or <if>/echo/<sel>,.../<off>=<hex>...
  load <name>                        offer the load now
  onarm <slot> <lead> <name>         offer it <lead> cycles before every deadline the slot is armed with
  mark <label>
  end
"""
from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import frames as f  # noqa: E402  the CPU budget harness's frame builders, read only
import scenario as budget  # noqa: E402  its identities, the talker's answer and the composed load, read only

#: Each draw's spacing: the bind waits BIND_WAIT_MS, the unbind UNBIND_WAIT_MS, the AEM command AECP_WAIT_MS. For
#: seed 0 each draw's bind starts PHASE_STEP_CYCLES later in a millisecond than the one before, and the talker's
#: turnaround (bus cycles from the PROBE_TX's last byte out to its answer's first byte in) is TURNAROUND_STEP_CYCLES
#: longer, both modulo one millisecond, so the draws sample the loop's phase at both inputs. The turnaround stays
#: under 1 ms.
BIND_WAIT_MS = 60
UNBIND_WAIT_MS = 20
AECP_WAIT_MS = 20
DRAW_MS = BIND_WAIT_MS + UNBIND_WAIT_MS + AECP_WAIT_MS
PHASE_STEP_CYCLES = 7919
TURNAROUND_STEP_CYCLES = 6007
MS_CYCLES = 100_000
#: Settling after the ready line, before the first draw: the boot's last publications and the link's first frames.
SETTLE_MS = 30
#: A deadline-triggered load is offered this many bus cycles (200 us) before the timer's millisecond, so its frames
#: have arrived and the loop is working through them when the timer expires.
LOAD_LEAD_CYCLES = 20_000
#: The run's tail after its last draw and ANNOUNCE: the longest response bound it grades (AECP's 240 ms, FR_NFR.md
#: 3.4.1; ACMP's is 200 ms), so every command's answer, or its absence, falls inside the log.
TAIL_MS = 250
#: The ANNOUNCEs a run ends after: one for the CI run (its acquisition's three probe intervals and the first
#: ANNOUNCE's egress), two for a campaign unit (one B.3.4.1 announce interval).
CI_ANNOUNCES = 1
CAMPAIGN_ANNOUNCES = 2
#: A campaign unit's draws: enough to keep the stimulus running past the latest second ANNOUNCE the firmware can
#: draw (the first by about 2 s of boot and acquisition, then at most 31,989 ms, maap/README.md:44).
CAMPAIGN_DRAWS = 342
#: AECP status SUCCESS (IEEE 1722.1-2021 Table 7-170); ACMP's SUCCESS is the same value (Table 8-3).
SUCCESS = 0
#: The AEM commands each draw sends, in turn (IEEE 1722.1-2021 7.4; Milan v1.2 5.4.3): the CPU budget harness's
#: aecp_groups rows, each command_type with its payload and the status its final response must carry (the grader
#: finds any other). MVU is Milan's vendor-unique GET_MILAN_INFO. GET_AVB_INFO is 0x0027 on AVB_INTERFACE 0
#: (descriptor_type 9), its 7.4.40.1 command a descriptor_type and a descriptor_index (#868).
AECP_COMMANDS = (
    ('read_descriptor_entity', 0x0004, f.be(0, 2) + bytes(2) + f.be(0, 2) + f.be(0, 2), SUCCESS),
    ('get_configuration', 0x0007, bytes(4), SUCCESS),
    ('get_counters', 0x0029, f.be(9, 2) + f.be(0, 2), SUCCESS),
    ('get_avb_info', 0x0027, f.be(9, 2) + f.be(0, 2), SUCCESS),
    ('get_name', 0x0011, bytes(8), SUCCESS),
    ('mvu_get_milan_info', None, bytes(2), SUCCESS),
)


def aecp_statuses() -> dict[str, int]:
    """Each graded AEM command's name and the status its final response must carry (AECP_COMMANDS)."""
    return {name: status for name, _, _, status in AECP_COMMANDS}
#: The MAAP and ADP slots of interface 0 (ctrl_app.h): ADP's run of MBX_N_IF slots from 0, then ACMP's, then MAAP's.
ADP_SLOT = 0
MAAP_FIRST_SLOT_IFS = 2


@dataclass(frozen=True)
class Draw:
    """One bind, probe, unbind and AEM command: its sequence_ids, its phase offset and the talker's turnaround."""
    index: int
    bind_seq: int
    unbind_seq: int
    aecp_seq: int
    phase_cycles: int
    turnaround_cycles: int


def draws(n: int, seed: int = 0) -> list[Draw]:
    """N draws, each with its own sequence_ids and phase."""
    rng = random.Random(seed)
    out = []
    for k in range(n):
        if seed == 0:
            phase, turn = (k * PHASE_STEP_CYCLES) % MS_CYCLES, (k * TURNAROUND_STEP_CYCLES) % MS_CYCLES
        else:
            phase, turn = rng.randrange(MS_CYCLES), rng.randrange(MS_CYCLES)
        out.append(Draw(k, (0x4100 + 2 * k) & 0xFFFF, (0x4101 + 2 * k) & 0xFFFF, (0x6100 + k) & 0xFFFF, phase, turn))
    return out


def probe_reply(turnaround_cycles: int) -> str:
    """The talker's answer as a reply rule: a PROBE_TX from this entity (an AVTP control frame, subtype 0xFC,
    message_type 0) answered with scenario.probe_answer's PROBE_TX_RESPONSE patches, after the turnaround."""
    terms = budget.probe_answer(0).split()[3:]   # drop 'reply <interface> <channel>'
    match = ['12:22', '13:f0', '14:fc'] + [t for t in terms if ':' in t]
    patch = [t for t in terms if '=' in t]
    return ' '.join(['reply', 'talker-probe-tx-response', str(turnaround_cycles), *match, *patch])


def aecp_command(p: budget.Point, k: int, seq: int) -> tuple[str, bytes]:
    """Draw k's AEM command: its name and frame, from CTL1."""
    name, command_type, payload, _ = AECP_COMMANDS[k % len(AECP_COMMANDS)]
    to = f.Aem(p.entity_id, budget.CTL1, budget.CTL_MAC, p.mac, seq)
    frame = f.mvu_command(to, 0x0000, payload) if command_type is None else f.aem_command(to, command_type, payload)
    return name, frame


#: The other entity the load's ENTITY_DISCOVERs name (see the module's docstring).
OTHER_ENTITY = budget.TALKER_A
#: The channels whose received records the draws measure: a deadline's burst leaves them out (see the docstring).
DRAW_CHANNELS = ('acmp', 'aecp')


def channel_of(frame: bytes) -> str:
    """A frame's mailbox channel: the AVTP control subtype, or MSRP and MVRP as srp."""
    if frame[12:14] == b'\x22\xf0':
        return {0xFA: 'adp', 0xFB: 'aecp', 0xFC: 'acmp', 0xFE: 'maap'}.get(frame[14], 'avtp')
    return 'srp' if frame[12:14] in (b'\x22\xea', b'\x88\xf5') else 'other'


def load_items(p: budget.Point, own: str, leave_out: tuple[str, ...] = ()) -> list[str]:
    """The composed load but `own`'s channel and `leave_out`'s, as defload items (see the module's docstring)."""
    g = budget.Group(f'load-{own}')
    budget.composed_load(g, p, own)
    discover = f.adp(f.ADP_DISCOVER, 0, budget.CTL_MAC, f.Adp(valid_time=0))
    elsewhere = f.adp(f.ADP_DISCOVER, OTHER_ENTITY, budget.CTL_MAC, f.Adp(valid_time=0))
    items = []
    for step in g.steps:
        w = step.split()
        if w[0] == 'frame':
            frame = bytes.fromhex(w[2])
            if channel_of(frame) in leave_out:
                continue
            items.append(f'{w[1]}/{(elsewhere if frame == discover else frame).hex()}')
        elif w[0] == 'reply':   # reply <if> <maap channel> 15:<type> on=<if> <off>=<hex>...: an echo of that frame
            selectors = ['12:22', '13:f0', f'14:{0xFE:02x}', w[3]]
            patches = [t for t in w[4:] if '=' in t and not t.startswith('on=')]
            items.append(f'{w[1]}/echo/{",".join(selectors)}/{"/".join(patches)}')
        else:
            raise ValueError(f'a composed load step this harness cannot offer: {step}')
    return items


def load_lines(p: budget.Point) -> list[str]:
    """The loads' definitions and the deadline triggers on interface 0's MAAP and ADP slots."""
    lines = [f'defload {own} {" ".join(load_items(p, own, () if own in DRAW_CHANNELS else DRAW_CHANNELS))}'
             for own in ('acmp', 'aecp', 'maap', 'adp')]
    lines += [f'onarm {MAAP_FIRST_SLOT_IFS * p.interfaces} {LOAD_LEAD_CYCLES} maap',
              f'onarm {ADP_SLOT} {LOAD_LEAD_CYCLES} adp']
    return lines


def deadline_load_channels(text: str) -> dict[str, set[str]]:
    """Each deadline-triggered load of a script (its onarm lines) with the channels its frames reach."""
    triggered = {line.split()[3] for line in text.splitlines() if line.startswith('onarm ')}
    out = {}
    for line in text.splitlines():
        w = line.split()
        if w and w[0] == 'defload' and w[1] in triggered:
            out[w[1]] = {channel_of(bytes.fromhex(item.split('/')[1])) if item.split('/')[1] != 'echo' else 'maap'
                         for item in w[2:]}
    return out


def deadline_loads_clear(text: str) -> list[str]:
    """Each deadline-triggered load of a script that reaches a draw's channel (see the module's docstring)."""
    return [f'the deadline load {name} reaches the {", ".join(sorted(reach & set(DRAW_CHANNELS)))} channel, '
            "whose received records the draws measure"
            for name, reach in sorted(deadline_load_channels(text).items()) if reach & set(DRAW_CHANNELS)]


def announce_match() -> str:
    """A MAAP ANNOUNCE sent at the MAC (IEEE 1722-2016 Table B.4): its EtherType, subtype and message_type."""
    return f'12:22 13:f0 14:fe 15:{f.MAAP_ANNOUNCE:02x}'


def limit_ms(n: int, announces: int = CI_ANNOUNCES) -> int:
    """The run's time limit: the boot's bound (the split boot simulation's), every draw, and, for a second
    ANNOUNCE, the longest announce interval the firmware draws, with a margin."""
    return 2000 + n * (DRAW_MS + 2) + SETTLE_MS + TAIL_MS + (32_000 if announces > 1 else 0)


def script(p: budget.Point, n: int, seed: int = 0, load: bool = False, announces: int = CI_ANNOUNCES) -> str:
    """The stimulus for N draws at one point, ending TAIL_MS after both its last draw and the `announces`-th ANNOUNCE
    at the MAC."""
    lines = [f'# ctrl_wire_timing: ACMP and AECP draws, MAAP and ADP timers (#868); seed {seed}, '
             f'load {"composed" if load else "none"}']
    lines += [f'link {i} 1' for i in range(p.interfaces)]
    if load:
        lines += load_lines(p)
    lines += ['wait ready', f'wait ms {SETTLE_MS}', 'mark draws']
    for d in draws(n, seed):
        bind = budget.acmp_cmd(p, 'BIND_RX', 0, d.bind_seq)
        unbind = budget.acmp_cmd(p, 'UNBIND_RX', 0, d.unbind_seq)
        name, command = aecp_command(p, d.index, d.aecp_seq)
        lines += [f'wait cycles {d.phase_cycles}', probe_reply(d.turnaround_cycles)]
        lines += ['load acmp'] if load else []
        lines += [f'frame 0 acmp-bind-{d.index} {bind.hex()}', f'wait ms {BIND_WAIT_MS}',
                  f'frame 0 acmp-unbind-{d.index} {unbind.hex()}', f'wait ms {UNBIND_WAIT_MS}']
        lines += ['load aecp'] if load else []
        lines += [f'frame 0 aecp-{name}-{d.index} {command.hex()}', f'wait ms {AECP_WAIT_MS}']
    lines += ['mark draws-end', f'wait sent {announces} {announce_match()}', f'wait ms {TAIL_MS}', 'mark end', 'end']
    return '\n'.join(lines) + '\n'


def identity(spec: dict) -> budget.Point:
    """The point's identity from its image's generated entity header (the CPU budget harness's point())."""
    return budget.point(spec['point'], {'elf': spec['elf'], 'shape': spec['shape'], 'interfaces': spec['interfaces']})


# The frames the grader decodes: ACMP's message types (IEEE 1722.1-2021 Table 8-1, Milan v1.2 5.5.2).
ACMP = f.ACMP
CTL1 = budget.CTL1
