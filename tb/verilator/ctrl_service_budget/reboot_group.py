# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The answering-ports arm's aecp-reboot group (#871): AECP REBOOT's records, accepted and refused, which
record_classes.py holds as ordinary AECP records. scenario.all_groups runs it."""
from __future__ import annotations

import answers
import frames as f
import scenario


def groups(p: scenario.Point, build: dict) -> list[scenario.Group]:
    """AECP REBOOT's records (IEEE 1722.1-2021 7.4.43; #871), with the answering-ports arm, whose image has a reset
    port as the platform's does (build.VARIANTS). On each interface its refusals in the processor's order: short of
    Figure 7-68's four bytes, a STREAM_INPUT, ENTITY 1, and ENTITY 0 under another controller's lock; then, on the
    first, the accepted REBOOT, answered and notified to every registration (7.5.2), the group's last command: no
    command is taken after its SUCCESS. Every record is held as an ordinary AECP record (record_classes.py).
    """
    if build.get('variant') != 'answering-ports':
        return []
    aecp = scenario.CH['aecp']
    ifs = range(p.interfaces)
    g = scenario.Group('aecp-reboot', sim_ms=1500)
    scenario.ready(g, p)
    controllers = [scenario.FANOUT_CONTROLLER + n for n in range(scenario.registrations())]
    seq = [0x7100]
    for i in ifs:
        for ctl in controllers:
            frame = f.aem_command(f.Aem(p.entity_id, ctl, scenario.CTL_MAC, p.mac, seq[0]), 0x0024, bytes(4))
            g.add(f'frame {i} {frame.hex()}', f'wait tx {aecp} 1 within {50 * scenario.MS}',
                  'wait quiet 3 within 2000000')
            seq[0] += 1
    everyone = tuple((ctl, i) for i in ifs for ctl in controllers)

    def reboot(i: int, name: str, payload: bytes, status: str) -> None:
        """One REBOOT from CTL2 on interface i, to its response; a SUCCESS also to every registration's notice."""
        frame = f.aem_command(f.Aem(p.entity_id, scenario.CTL2, scenario.CTL_MAC, p.mac, seq[0]), 0x002A, payload)
        end = f'resp:{aecp}:{seq[0]:x}'
        seq[0] += 1
        if status == 'SUCCESS':
            probe = scenario.Probe(f'aecp_reboot.{name}.if{i}', 'REBOOT', 'notify', f'rxc:{aecp}',
                                   [end, f'notify:{aecp}:002a:0:0'], expect=answers.aem(0x002A), recipients=everyone)
            g.probe(probe, f'frame {i} {frame.hex()}', wait=f'tx {aecp} {1 + len(everyone)} within {200 * scenario.MS}')
        else:
            probe = scenario.Probe(f'aecp_reboot.{name}.if{i}', answers.refused('REBOOT', status), 'aecp',
                                   f'rxc:{aecp}', [end], expect=answers.aem(0x002A, status))
            g.probe(probe, f'frame {i} {frame.hex()}', wait=f'tx {aecp} 1 within {50 * scenario.MS}')

    def lock(i: int, flags: int) -> None:
        """CTL1's LOCK_ENTITY (7.4.2.1) of the ENTITY on interface i, acquired (flags 0) or released (1), to its
        response and every registration's notice."""
        frame = f.aem_command(f.Aem(p.entity_id, scenario.CTL1, scenario.CTL_MAC, p.mac, seq[0]), 0x0001,
                              f.be(flags, 4) + f.be(0, 8) + f.be(0, 2) + f.be(0, 2))
        g.add(f'frame {i} {frame.hex()}', f'wait tx {aecp} {1 + len(everyone)} within {200 * scenario.MS}',
              'wait quiet 3 within 2000000')
        seq[0] += 1

    for i in ifs:
        reboot(i, 'short', bytes(2), 'BAD_ARGUMENTS')
        reboot(i, 'stream_input', f.be(5, 2) + f.be(0, 2), 'NOT_SUPPORTED')
        reboot(i, 'entity_1', f.be(0, 2) + f.be(1, 2), 'NO_SUCH_DESCRIPTOR')
        lock(i, 0)
        reboot(i, 'locked', f.be(0, 2) + f.be(0, 2), 'ENTITY_LOCKED')
        lock(i, 1)
    reboot(0, 'accepted', f.be(0, 2) + f.be(0, 2), 'SUCCESS')
    return [scenario.paced(g, aecp)]
