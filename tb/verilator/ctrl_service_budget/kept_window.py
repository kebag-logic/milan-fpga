# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The Talkers SRP keeps for StreamIDs no binding holds (#969; srp_mbx.c keep_talker, count_kept): the records and
builds that run them, at every point, in arm A.

ACMP binds a STREAM_INPUT only once its talker answers the probe (Milan v1.2 5.5.3.5.18 step 4), so a talker's
declarations of every input's stream arrive before any binding, at a power-on and after a link flap alike, and the
receive filter keeps them, one for each STREAM_INPUT of the shape. The fixture's sinks are never bound, so every Talker
the group declares is one no binding holds. On every interface, after the link settles:

- srp.kept_advertise: one MRPDU declaring a Talker Advertise for each STREAM_INPUT, one vector of them (each value its
  predecessor's plus one, IEEE 802.1Q-2018 35.2.2.8.4): each is kept, an lwSRP attribute and its indication each;
- the first of them leaves, and past its leave timer mrp_reclaim frees its block;
- srp.kept_recount: one MRPDU declaring one stream more than the shape's inputs past the kept ones: its count before
  the receive (a kept registration ended and a block was returned since), the first kept in the freed place, and the
  rest past the bound, each a scan of the kept list and refused;
- the participant's LeaveAll timer runs out (10 s, lwSRP's randomised LeaveAllTime, srp_mbx.c's SRP_LEAVEALL_CS),
  so the build that sends the LeaveAll carries each kept attribute (an observed attribute answers a LeaveAll with In,
  Table 10-3); mrpdu_grade.py's LeaveAll row and whole_grade.py's builds grade it, as in every group;
- the link goes down and up, a reset whose new participants keep none, then srp.kept_failed: one MRPDU declaring a
  Talker Failed for each STREAM_INPUT, each kept.

kept_grade.py holds each of the group's SRP records (srp_mbx.c receive, a SPAN line) to ctrl_loop.h's
CTRL_LOOP_SRP_UNIT_US at the point's shape, by the stated rule, and each pass given whole to a build to its stated cost.
"""
from __future__ import annotations

import frames as f
import scenario

NAME = 'srp-kept'
#: The talker the group's Talkers are declared by, and their streams: stream k's StreamID and destination are the
#: first's plus k, as a vector increments them (35.2.2.8.4).
STREAM = 0x0C0D0E0F10020000
STREAM_DA = 0x91E0F000FD00
VID = 2
#: A Talker Failed's FailureInformation: a bridge's ID and Insufficient Bandwidth (35.2.2.8.7, Table 35-6).
BRIDGE_ID = 0x80000E0E0E0E0E01
FAILURE = 1
#: The leave timer's run-out and the reclaim after it (srp_mbx.c create_participants: 500 cs), with a margin.
LEAVE_MS = 6000
#: The participants' first LeaveAll period: lwSRP runs it out between 10 s and 15 s after their creation at link up
#: (IEEE 802.1Q-2018 10.7.11; SRP_LEAVEALL_CS), so the group waits till 16.5 s after the link settles.
SETTLE_MS = 2600
LEAVEALL_MS = 16500
#: The settle after a link change, as scenario.ready's.
LINK_MS = 600


def talker(k: int, failed: bool = False) -> bytes:
    """Stream k's Talker FirstValue (35.2.2.8.2): StreamID, DataFrameParameters, TSpec, PriorityAndRank,
    AccumulatedLatency, and a Failed's FailureInformation."""
    value = (f.be(STREAM + k, 8) + f.be(STREAM_DA + k, 6) + f.be(VID, 2) + f.be(224, 2) + f.be(1, 2) +
             bytes((0x70,)) + f.be(100_000, 4))
    return value + (f.be(BRIDGE_ID, 8) + bytes((FAILURE,)) if failed else b'')


def declared(first: int, count: int, failed: bool = False, event: int = 1) -> bytes:
    """One MRPDU declaring streams first .. first + count - 1, one vector of them, every one the same event."""
    message = f.mrp_message(2 if failed else 1, talker(first, failed), [event] * count)
    return f.msrp(scenario.TALKER_A_MAC, [message])


def groups(p: scenario.Point) -> list[scenario.Group]:
    """The group, every probe on every interface."""
    srp, ms, n = scenario.CH['srp'], scenario.MS, p.sinks
    g = scenario.Group(NAME, sim_ms=650 + LEAVEALL_MS + 2 * LINK_MS * p.interfaces + 1000)
    scenario.ready(g, p)
    g.add(f'wait cycles {SETTLE_MS * ms}', 'wait quiet 3 within 2000000')
    for i in range(p.interfaces):
        g.probe(scenario.Probe(f'srp.kept_advertise.if{i}', 'Talker Advertise RX for every input, no binding (kept)',
                               'srp', f'rxc:{srp}', [f'pass_end:{srp}']),
                f'frame {i} {declared(0, n).hex()}', wait=f'cycles {30 * ms}')
    for i in range(p.interfaces):
        g.add(f'frame {i} {declared(0, 1, event=5).hex()}')
    g.add(f'wait cycles {LEAVE_MS * ms}', 'wait quiet 3 within 2000000')
    for i in range(p.interfaces):
        g.probe(scenario.Probe(f'srp.kept_recount.if{i}', 'Talker RX at the bound after a freed block (count)',
                               'srp', f'rxc:{srp}', [f'pass_end:{srp}']),
                f'frame {i} {declared(n, n + 1).hex()}', wait=f'cycles {30 * ms}')
    g.add(f'wait cycles {(LEAVEALL_MS - SETTLE_MS - LEAVE_MS) * ms}', 'wait quiet 3 within 2000000')
    for i in range(p.interfaces):
        g.add(f'link {i} 0', f'wait cycles {LINK_MS * ms}', 'wait quiet 3 within 2000000',
              f'link {i} 1', f'wait cycles {LINK_MS * ms}', 'wait quiet 3 within 2000000')
    for i in range(p.interfaces):
        g.probe(scenario.Probe(f'srp.kept_failed.if{i}', 'Talker Failed RX for every input, no binding (kept)',
                               'srp', f'rxc:{srp}', [f'pass_end:{srp}']),
                f'frame {i} {declared(0, n, failed=True).hex()}', wait=f'cycles {30 * ms}')
    return [g]
