# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""SRP's Talker declarations as each source's validity moves them (#895; Milan v1.2 4.3.3.1, 5.3.7.4): the passes that
declare a Talker when a probe opens its source's DA gate, and that withdraw it when the probe window ends or MAAP loses
the range.

build.py's valid-destinations variant (a scratch copy of the size fixture, never the formal image) makes the fixture's
ACMP source port report each source's destination as the target platform's does, valid once MAAP holds its interface's
range, at base + n (Milan v1.2 5.5.4.1). So a PROBE_TX for a source is answered SUCCESS, its DA gate opens, and the
composition hands the gate to SRP, which declares the source's Talker Advertise at once, in a pass given whole to THE
TRANSMIT. Each probe's row runs from the command's commit to SRP's next frame, the declaration, with a JoinTime's wait
for its transmit opportunity (JOIN_MS). With no Listener, the 15 s probe window then closes every gate and SRP
withdraws every Talker in its own passes. The second group probes the same way, then makes each interface lose its
range: a peer ANNOUNCEs it from a MAC for which compare_MAC is FALSE (IEEE 1722-2016 Table B.7, B.3.6.4), MAAP restarts
on a new range, its DA gate closes, and SRP withdraws the interface's Talkers; the row runs from the ANNOUNCE's commit
to MAAP's new PROBE and SRP's Leave, with the same wait. whole_grade.py holds each such pass to THE TRANSMIT's stated
build cost and share.py to the per-pass share, as for every group.
"""
from __future__ import annotations

import answers
import frames as f
import scenario

#: The fixture's edits, each (unique anchor, replacement): the source port valid once MAAP holds the range.
FIXTURE_EDITS = (
    ('static void source(void *ctx, unsigned n, struct acmp_source_state *out)\n'
     '{ (void)ctx; (void)n; out->dest_mac_valid=false; }\n',
     'static void source(void *ctx, unsigned n, struct acmp_source_state *out);\n'),
    ('    (void)ctx; (void)count;\n    image_allocation[interface] = valid ? base : 0;\n}\n',
     '    (void)ctx;\n    image_allocation[interface] = valid ? base : 0;\n'
     '    image_count[interface] = valid ? count : 0u;\n}\n'
     'static void source(void *ctx, unsigned n, struct acmp_source_state *out)\n'
     '{\n    (void)ctx;\n    const unsigned i = n % MBX_N_IF;\n'
     '    out->dest_mac_valid = image_allocation[i] != 0u && n < image_count[i];\n'
     '    out->stream = (struct acmp_stream){image_entity.mac << 16 | n, image_allocation[i] + n, 2u};\n'
     '    out->asking_failed = false;\n}\n'),
    ('static volatile uint64_t image_allocation[MBX_N_IF];\n',
     'static volatile uint64_t image_allocation[MBX_N_IF];\nstatic volatile uint16_t image_count[MBX_N_IF];\n'),
)
#: The simulated time the group needs: MAAP's range, a probe a source, and the probe window's end.
SIM_MS = 21000
#: The probe window, Milan v1.2 4.3.3.1 (acmp.c's da_fresh_ms), and the wait past it.
WINDOW_MS = 16000
#: The wait for each restarted range's PROBEs and ANNOUNCE (B.3.4.2, Table B.8: 3 x 500 ms), and the loss group's time.
RANGE_MS = 2500
LOSS_MS = 9000
#: The JoinTime a declaration or a Leave may wait for its transmit opportunity (IEEE 802.1Q-2018 10.7.4.1, Table 10-7;
#: Milan v1.2 Table 4.3; srp_mbx.c's SRP_JOIN_CS): each row's normative wait, as the srp group's Domain row states it.
JOIN_MS = 200.0
#: The peer that takes each range: a unicast MAC whose octet-wise reverse, 0x0e, is below that of any MAC with a nonzero
#: octet past its first, so compare_MAC is FALSE on every interface and the core restarts (IEEE 1722-2016 B.3.6.4).
PEER_MAC = 0x0E0000000000


def reversed_mac(mac: int) -> int:
    """A MAC's octets in reverse order, as compare_MAC compares them (IEEE 1722-2016 B.3.6.4)."""
    return int.from_bytes(mac.to_bytes(6, 'big')[::-1], 'big')


def declared(g: scenario.Group, p: scenario.Point) -> None:
    """Ready, MAAP's ranges held, then a PROBE_TX for every source: each a row of its own on its interface."""
    srp, acmp, ms = scenario.CH['srp'], scenario.CH['acmp'], scenario.MS
    scenario.ready(g, p)
    g.add(f'wait cycles {2600 * ms}', 'wait quiet 3 within 2000000')
    seq = 0x5300
    for n in range(p.sources):
        i = n % p.interfaces
        g.probe(scenario.Probe(f'srp.talker_declare.s{n}.if{i}', 'PROBE_TX -> Talker Advertise (JoinTime wait)',
                               'srp', f'rxc:{acmp}', [f'resp:{acmp}:{seq:x}', f'tx:{srp}'], wait_ms=JOIN_MS,
                               expect=answers.acmp('PROBE_TX_RESPONSE', 'SUCCESS')),
                f'frame {i} {scenario.talker_cmd(p, "PROBE_TX", n, seq).hex()}', wait=f'tx {srp} 1 within {300 * ms}')
        seq += 1


def groups(p: scenario.Point) -> list[scenario.Group]:
    """The probe window's end, then a range lost on every interface, each after a PROBE_TX for every source."""
    srp, maap, ms = scenario.CH['srp'], scenario.CH['maap'], scenario.MS
    window = scenario.Group('srp-talker', sim_ms=SIM_MS)
    declared(window, p)
    window.add(f'wait cycles {WINDOW_MS * ms}', 'wait quiet 3 within 2000000')
    if reversed_mac(PEER_MAC) >= reversed_mac(p.mac):
        raise ValueError(f'the peer {PEER_MAC:012x} does not take the range of {p.mac:012x} (B.3.6.4)')
    loss = scenario.Group('srp-talker-loss', sim_ms=LOSS_MS + 1000 * p.interfaces)
    declared(loss, p)
    for i in range(p.interfaces):
        loss.probe(scenario.Probe(f'srp.talker_loss.if{i}', 'range lost -> Talker Leave (JoinTime wait)', 'srp',
                                  f'rxc:{maap}', [f'tx:{maap}', f'tx:{srp}'], wait_ms=JOIN_MS,
                                  expect=f'maap_type:{f.MAAP_PROBE}'),
                   f'reply {i} {maap} 15:{f.MAAP_ANNOUNCE:02x} on={i} 6={PEER_MAC:012x}',
                   wait=f'tx {srp} 1 within {300 * ms}')
    loss.add(f'wait cycles {RANGE_MS * ms}', 'wait quiet 3 within 2000000')
    return [window, loss]
