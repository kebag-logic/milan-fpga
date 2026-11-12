# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The datapath's change events in the CPU budget harness (#894): the three coalesced events of mailbox.yaml's event
types 6 to 8, AVB_INFO_CHANGED and AS_PATH_CHANGED an interface each and AMAP_LIVE_WRITE the live map, posted through
the testbench's datapath change pads (split_soc.DATAPATH_PADS, sim_main.cpp's `datapath <avb|asp|amap> <if>` step).
Their sinks' cost is what the rows by every source charge each source an ordinary pass (rows_tiers.DATAPATH_US)."""
from __future__ import annotations

import scenario


def groups(p: scenario.Point) -> list[scenario.Group]:
    """Each event pulsed alone on every interface 2 ms after the last, so each is a pass's one event, eight times
    each."""
    g = scenario.Group('datapath-events', sim_ms=900)
    scenario.ready(g, p)
    for _ in range(8):
        for kind in ('avb', 'asp', 'amap'):
            for i in range(p.interfaces):
                g.add(f'datapath {kind} {i}', f'wait cycles {2 * scenario.MS}')
    g.add('wait quiet 3 within 2000000')
    return [g]
