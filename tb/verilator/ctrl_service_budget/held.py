# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A record its channel's bucket held (#917): its observation, its attribution and its scenario.

KL_mbx_rx holds a frame that passes and fits and finds its channel's bucket empty: its verdict writes the record past
RX_HEAD (hold_w, an RXH line where a commit's RXC would be) and the channel's next refill commits it (rel_w[c], an RXR
line for channel c). The commit is the held frame's own: never a frame ended since, which the filter or the bucket
refused, nor another channel's. A held record's ingress allowance is one refill period of its channel (mailbox.yaml)
and T_ingress (FR_NFR.md 3.4.1), so its path is measured from its frame's last byte (an rxh:<channel> start) and its
commit must come within that allowance. A commit on a channel holding none, a second hold on a channel holding one and
a commit outside the allowance are refused; a held record never committed by the run's end was not served.
"""
from __future__ import annotations

import answers
import frames as f
import grade
import scenario

#: FR_NFR.md 3.4.1's T_ingress for a record that finds a token: published within 64 mailbox cycles of its last byte.
INGRESS_MS = 1.0
#: The held group starts its burst just after a refill: NOW_MS and every bucket's refill count step on the mailbox's
#: millisecond from reset, so a multiple of AECP's refill period is a refill tick, and the held command waits the
#: whole period. It is past ready()'s settle at every point.
AT_MS = 1000


def allowance_ms(ch: int) -> float:
    """A held record's ingress allowance: one refill period of its channel and T_ingress."""
    return scenario.CONTRACT.channels[ch].refill_ms + INGRESS_MS


def hold(log: grade.Log, pending: list, ch: int, cycle: int) -> None:
    """The frame a hold at cycle belongs to, as a commit's (grade.last_frame); a channel holds one frame."""
    if ch in log.holding:
        raise grade.Refusal(f'a second record held on channel {ch} at {cycle} while one is held')
    log.holding[ch] = (*grade.last_frame(pending, cycle, log.refused, 'hold'), cycle)


def release(log: grade.Log, pending: list, ch: int, cycle: int) -> tuple[int, str, int]:
    """The frame a held record's commit at cycle belongs to: (interface, tag, bytes), the one channel ch holds; the
    frames pending since its hold are not this commit's."""
    del pending
    if ch not in log.holding:
        raise grade.Refusal(f'the held-record commit at {cycle} on channel {ch} follows no held frame')
    interface, tag, size, end, held_at = log.holding.pop(ch)
    allowance = round(allowance_ms(ch) * log.sys_hz / 1000)
    if not end < cycle <= end + allowance:
        raise grade.Refusal(f'the held record {tag} on channel {ch} was committed {cycle - end} cycles after its '
                            f'last byte, outside its allowance of {allowance}')
    log.held.append((end, held_at, cycle, ch, interface, tag, size))
    return interface, tag, size


def observe(kind: str, rest: list[str], pending: list, log: grade.Log) -> None:
    """parse()'s RXH and RXR lines (sim_main.cpp prints RXH <cycle> <channel> and RXR <cycle> <channel>)."""
    cycle, ch = int(rest[0]), int(rest[1])
    if kind == 'RXH':
        hold(log, pending, ch, cycle)
    else:
        log.rxc.append((cycle, ch, *release(log, pending, ch, cycle)))


def unserved(pending: list, log: grade.Log) -> None:
    """At the log's end: every frame still pending was refused, and so was every held record its channel never
    committed, which was not served."""
    log.refused.extend((end, interface, tag, size) for interface, tag, size, end in pending)
    for ch, (interface, tag, size, end, held_at) in sorted(log.holding.items()):
        log.refused.append((end, interface, tag, size))
        log.held.append((end, held_at, -1, ch, interface, tag, size))


def starts(log: grade.Log, probe: scenario.Probe, ch: int, interface: int, after: int, before: int) -> list[int]:
    """An rxh:<channel> start: the last byte of the probe's own frame, held by its channel's bucket and committed. A
    probe frame that was not held is not this path's input."""
    return [end for end, _, commit, k, i, tag, _ in log.held if after <= end < before and k == ch
            and i in (interface, -1) and tag == probe.name and commit >= 0]


def ingress(grader: grade.Grader, probe: scenario.Probe, start: int) -> dict:
    """A held path's row fields: its ingress delay, last byte to commit, and the allowance it was held to."""
    ch = int(probe.start.split(':')[1])
    commit = next(c for e, _, c, k, _, tag, _ in grader.log.held if e == start and k == ch and tag == probe.name)
    return dict(ingress_sys=commit - start, ingress_ms=round(grader.ms(commit - start), 5),
                ingress_allowance_ms=allowance_ms(ch))


def groups(p: scenario.Point) -> list[scenario.Group]:
    """A READ_DESCRIPTOR its channel's bucket has no token for: held, committed at the next refill, measured from
    its last byte, so its ingress delay counts, against the AECP row's bound; its commit is credited to its own
    frame, not to the two frames behind it, one the filter refuses (another target) and one the bucket refuses.

    The burst that empties the bucket is AECP frames the core takes and drops at once: a response of a message type
    with no command contract, addressed to this entity as a controller (aecp.c: ignored), so the held command is
    served by a loop with nothing else to do.
    """
    aecp = scenario.CH['aecp']
    ch = scenario.CONTRACT.channels[aecp]
    if AT_MS % ch.refill_ms:
        raise ValueError(f'AT_MS {AT_MS} is not a refill tick of the {ch.refill_ms} ms bucket')
    g = scenario.Group('aecp-held', sim_ms=AT_MS + 400)
    scenario.ready(g, p)
    g.add(f'wait ms {AT_MS}')
    for n in range(ch.burst):
        body = f.be(p.entity_id, 8) + f.be(0x7C00 + n, 2) + bytes(10)
        filler = f.ethernet(p.mac, scenario.CTL_MAC, f.ETH_AVTP,
                            f.control_header(0xFB, 3, 0, len(body), scenario.CTL1) + body)
        g.add(f'frame 0 {filler.hex()}')
    seq = 0x7D00
    held = f.read_descriptor(f.Aem(p.entity_id, scenario.CTL1, scenario.CTL_MAC, p.mac, seq), 0, 0)
    probe = scenario.Probe('aecp.held.read_descriptor.if0', 'READ_DESCRIPTOR held for a token (#917)', 'aecp',
                           f'rxh:{aecp}', [f'resp:{aecp}:{seq:x}'], expect=answers.aem(0x0004))
    g.probes.append(probe)
    g.add(f'mark {probe.name}', scenario.tagged(f'frame 0 {held.hex()}', probe.name))
    other_target = f.read_descriptor(f.Aem(scenario.CTL2, scenario.CTL1, scenario.CTL_MAC, p.mac, seq + 1), 0, 0)
    behind = f.read_descriptor(f.Aem(p.entity_id, scenario.CTL2, scenario.CTL_MAC, p.mac, seq + 2), 0, 0)
    g.add(f'frame 0 {other_target.hex()}', f'frame 0 {behind.hex()}')
    g.add(f'wait tx {aecp} 1 within {50 * scenario.MS}', 'wait quiet 3 within 2000000', 'mark aecp-held.end')
    return [g]
