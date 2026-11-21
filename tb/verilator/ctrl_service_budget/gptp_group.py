# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gptp_group.py - the gPTP end station ports' groups (contract 2.5; #884, #665 F6), only in an image built with them.

An image built --with-gptp opens the gptp channel and runs one IEEE 802.1AS end station port an interface. These
groups give interface 0 a peer (sim_main.cpp's `gptp` op): a grandmaster that syncs the entity (`gptp-slave`) or a
slave the entity syncs as grandmaster (`gptp-master`). Both peers answer the entity's Pdelay_Req as a 500 ns link
with a 20 us turnaround and send their own, each message at its Milan v1.2 4.2.6.2.2 Table 4.1 interval; the
testbench's timestamp unit stamps every event message both ways. The run's PASS lines then carry the ports' cycles
pass by pass (the gptp and gptp_mbx modules), and each group probes the responder's turnaround: a Pdelay_Req's
receive commit to the Pdelay_Resp's transmit commit, against the provisional gptp bound (scenario.CEILING_MS).
"""
from __future__ import annotations

import scenario
from scenario import MS, Group, Point, Probe, ready

#: the peer's own port identity (sim_main.cpp's peer_clock) and a request of its own, sequenceId 0x7777
PEER_CLOCK = 0x02AABBFFFE000001
SIM_MS = 1700


def pdelay_req(seq: int) -> bytes:
    """A peer's Pdelay_Req (IEEE 802.1AS-2020 11.4.5), majorSdoId 1, versionPTP 2."""
    f = bytearray(14 + 54)
    f[0:6] = (0x0180C200000E).to_bytes(6, 'big')
    f[6:12] = (0x02AABB000001).to_bytes(6, 'big')
    f[12:14] = (0x88F7).to_bytes(2, 'big')
    f[14], f[15] = 0x12, 0x12
    f[16:18] = (54).to_bytes(2, 'big')
    f[34:42] = PEER_CLOCK.to_bytes(8, 'big')
    f[42:44] = (1).to_bytes(2, 'big')
    f[44:46] = seq.to_bytes(2, 'big')
    f[46] = 5
    return bytes(f)


def groups(p: Point, build: dict) -> list[Group]:
    """A grandmaster peer and a slave peer on interface 0, the entity's ports up for SIM_MS each."""
    if not build.get('gptp'):
        return []
    gptp = next(c.ident for c in scenario.CONTRACT.channels if c.name == 'gptp')
    out = []
    for name, role in (('gptp-slave', 'gm'), ('gptp-master', 'slave')):
        g = Group(name, sim_ms=SIM_MS + 300)
        ready(g, p, link=False)
        for i in range(p.interfaces):
            g.add(f'link {i} 1')
        # asCapable takes the entity's own two exchanges, at link-up and a second later (Milan v1.2 4.2.6.2.4)
        g.add(f'gptp {role} 0', f'wait cycles {1300 * MS}', 'mark gptp_settled')
        g.probe(Probe('gptp.pdelay_resp.if0', 'Pdelay_Req -> Pdelay_Resp (responder turnaround)', 'gptp',
                      f'rxc:{gptp}', [f'gptp:{gptp}:3:7777']),
                f'frame 0 {pdelay_req(0x7777).hex()}', wait=f'tx {gptp} 1 within {20 * MS}')
        g.add(f'wait cycles {300 * MS}')
        out.append(g)
    return out
