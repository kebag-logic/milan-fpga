# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The tier-1 side of the tier model (rows_tiers.py, THE TIERS): the passes and records ahead of each row's work in
tier 1 under each order a Design names, and the tier-1 channels' own rows (#894's ruling of 2026-11-13, item 2: each
tier-1 channel's last record of its burst by every source). A module of the model alone: rows_tiers reads the tree
and solves the rows; every function here takes a point's inputs (rows_tiers.Inputs) and a design (rows_tiers.Design)."""
from __future__ import annotations

import math
import re
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from rows_tiers import Design, Inputs

#: The tier-1 channels: the response channels (#665: AECP, ACMP and ADP) and MAAP, which the tiers ruling names in
#: neither tier and which is counted with tier 1, the side that lengthens R4. rows_tiers.unrowed holds them to the
#: channels the loop serves.
TIER1 = ('aecp', 'acmp', 'adp', 'maap')
#: The orders whose takes are each channel's quota a pass (Design.quota).
QUOTA_ORDERS = ('aecp-quota', 'wrr')
#: The largest legal AECPDU in octets: a control_data_length of 524 following the target_entity_id (IEEE 1722.1-2021
#: 9.2.2.6), the 8-octet target_entity_id, the AVTP control header's 4 and the Ethernet header's 14; ADD_AUDIO_MAPPINGS
#: or REMOVE_AUDIO_MAPPINGS of 63 mappings answers one that long, a notice over AECP_FAN_BYTES. A slot that holds it
#: (AECP_OWED_BYTES, the tree's) queues every legal notice.
LONG_NOTICE_BYTES = 550
#: The rows solved as a tier-1 channel's (channel_passes, channel_records) beside R4, each with its bound in ms (#894,
#: the owner's decision of 2026-11-13, option A; FR_NFR.md 3.4.1): ACMP's, ADP's and MAAP's 30 ms by every source, 15 %
#: of ACMP's 200 ms command timeout (Milan v1.2 5.5.2.3, Table 5.26), where neither ADP (a random 0 to 4 s delay before
#: AVAILABLE, Milan v1.2 5.6.3.5.4) nor MAAP (500 to 600 ms between probes, IEEE 1722-2016 B.3.4.2) has a response
#: deadline; and tier 1's 20 ms for AECP's with its largest legal notice, the one row that counts it, which THE PACE
#: restates at the response time less the fabric's allowances, 238 ms (paced_rows.PACED_BOUNDS; #894's pace ruling of
#: 2026-11-13, item 1, and its egress ruling, item 1).
CHANNEL_BOUNDS = {'R4L': 20, 'ACMP': 30, 'ADP': 30, 'MAAP': 30}
#: THE TRANSMIT's MRPDU rows: tx, and txL with every AECP notice the largest legal one (#894's ruling of 2026-11-13 on
#: option A: the MRPDU's bound is the specs', so the largest legal notice is one of its sources).
TX_ROWS = ('tx', 'txL')


def queue_passes(i: Inputs, burst: int, first_us: float, drain: float = 0.0) -> int:
    """The passes AECP-first takes a burst of state-changing commands in under the owed-notice queue (#894, the ruling's
    condition (c)): each pass its records while tier 1 has spent at most CTRL_LOOP_DRAIN_US (or `drain`, what the
    others' quotas leave), the first pass after the queue's first notice, and only while the queue has a slot of its
    depth (i.owed); each pass's poll sends one queued notice and frees its slot (aecp.c, notices)."""
    record, drain = i.c['record.aecp'], drain or i.h['CTRL_LOOP_DRAIN_US']
    left, queued, passes, ahead = burst, 0, 0, first_us
    while left > 0:
        taken = min(left, i.owed - queued, max(1, math.floor((drain - ahead) / record) + 1))
        left -= taken
        queued = max(0, queued + taken - 1)
        passes += 1
        ahead = 0.0
    return passes


def aecp_passes(i: Inputs, d: Design, ticks: int, notice: float) -> int:
    """AECP's passes for its burst: one record a pass under the tree's notify rule, else its cap (past it,
    aecp-first), and under the queue the depth too (queue_passes)."""
    h, c, _, rate, _ = i[:5]
    aecp, cap = rate['aecp'][0], h['CTRL_LOOP_RX_PER_PASS']
    if d.aecp == 'notify' or (d.aecp == 'queue' and i.owed == 0):
        return aecp
    if d.tier1 == 'turn':
        return math.ceil(aecp / cap) + ticks
    if d.aecp == 'queue':
        return queue_passes(i, aecp, notice) + 1
    return math.ceil((aecp * c['record.aecp'] + notice) / h['CTRL_LOOP_DRAIN_US']) + 1


def per_pass(i: Inputs, d: Design) -> dict[str, int]:
    """Each tier-1 channel's most records a pass while another holds records: its quota under QUOTA_ORDERS, AECP's
    under aecp-quota as many as it starts in what the pass's tier-1 time less the others' quotas leaves; else the
    cap."""
    h, c = i.h, i.c
    if d.tier1 not in QUOTA_ORDERS:
        return dict.fromkeys(TIER1, d.cap or h['CTRL_LOOP_RX_PER_PASS'])
    q = dict(zip(TIER1, d.quota))
    if d.tier1 == 'aecp-quota':
        q['aecp'] = max(1, math.floor(aecp_time(i, d) / c['record.aecp']) + 1)
    return q


def aecp_time(i: Inputs, d: Design) -> float:
    """What a pass's tier-1 time leaves AECP under aecp-quota, in us: CTRL_LOOP_DRAIN_US less the others' quotas."""
    return i.h['CTRL_LOOP_DRAIN_US'] - sum(n * i.c[f'record.{o}'] for o, n in zip(TIER1, d.quota) if o != 'aecp')


def quota_fits(i: Inputs, d: Design) -> bool:
    """Whether a design's pass takes every quota or cap it credits within CTRL_LOOP_DRAIN_US: wrr's weights' stated
    work, aecp-quota's room for an AECP record beside the others' quotas, and under aecp-first and others-first the
    other channels' caps, which a pass takes in turn (ctrl_loop.c: a channel cut by the time takes less)."""
    drain, c = i.h['CTRL_LOOP_DRAIN_US'], i.c
    if d.tier1 == 'wrr':
        return sum(n * c[f'record.{o}'] for o, n in zip(TIER1, d.quota)) <= drain
    if d.tier1 == 'aecp-quota':
        return aecp_time(i, d) >= c['record.aecp']
    if d.tier1 in ('aecp-first', 'others-first'):
        return sum(per_pass(i, d)[o] * c[f'record.{o}'] for o in TIER1 if o != 'aecp') <= drain
    return True


def channel(row: str) -> str:
    """A tier-1 channel row's channel."""
    return 'aecp' if row in ('R4', 'R4L') else row.lower()


def held_back(row: str, i: Inputs, d: Design) -> bool:
    """Whether the row's AECP burst takes a record a pass: R4L's notices each wait in the response buffer (the buffer
    rule with the tree's slot, i.slot, under the largest legal notice, a queue of none, or a rule before the queue)."""
    return row == 'R4L' and ((d.long == 'buffer' and i.slot < LONG_NOTICE_BYTES) or i.owed == 0 or d.aecp != 'queue')


def channel_passes(row: str, i: Inputs, d: Design, ticks: int, notice: float, arrive: Callable[[str], int]) -> int:
    """The ordinary passes to the last record of a tier-1 channel's burst: the pass running as it arrives, the passes
    of every channel's records the order serves first, and the channel's own at its records a pass, one lost to each
    centisecond (THE TICK's cap)."""
    h, c, rate = i.h, i.c, i.rate
    x, drain, q = channel(row), h['CTRL_LOOP_DRAIN_US'], per_pass(i, d)
    if x != 'aecp':
        first = math.ceil((arrive('aecp') * c['record.aecp'] + notice) / drain) if d.tier1 == 'aecp-first' else 0
        return first + math.ceil(rate[x][0] / q[x]) + ticks + 1
    if held_back(row, i, d):
        own = rate['aecp'][0]
    elif d.tier1 == 'aecp-quota' and i.owed:
        own = queue_passes(i, rate['aecp'][0], notice, aecp_time(i, d)) + 1
    elif d.tier1 == 'wrr':
        own = math.ceil(rate['aecp'][0] / q['aecp']) + ticks
    else:
        own = aecp_passes(i, d._replace(tier1='aecp-first' if d.tier1 == 'others-first' else d.tier1), ticks, notice)
    first = sum(arrive(o) * c[f'record.{o}'] for o in TIER1 if o != 'aecp') if d.tier1 == 'others-first' else 0
    return math.ceil((first + notice) / drain) * (first > 0) + own + 1


def edit_terms(i: Inputs, w_ms: float | None, records: int) -> dict[str, float]:
    """The edits among a row's AECP records in a window of w_ms (edit_rows.terms), none where w_ms is None."""
    import edit_rows  # here: edit_rows reads paced_rows, which reads this module
    return edit_rows.terms(i, w_ms, records) if w_ms is not None else {}


def channel_records(row: str, i: Inputs, d: Design, passes: int, arrive: Callable[[str], int],
                    w_ms: float | None = None) -> dict[str, float]:
    """A tier-1 channel row's records: its own burst ('aecp' for AECP's, else 'own'), and each other tier-1 channel's
    ahead of its last, every one the order serves first (AECP's under aecp-first, the others' for AECP's under
    others-first), the pass running's for AECP's under aecp-first with its notices queued, and otherwise at most its
    records a pass in each of the row's passes; in a window of w_ms, the edits among AECP's (edit_rows.terms)."""
    c, rate, x, q = i.c, i.rate, channel(row), per_pass(i, d)
    drain = i.h['CTRL_LOOP_DRAIN_US']

    def reach(o: str) -> int:
        """The records of channel o that may precede the row's last."""
        if (d.tier1 == 'aecp-first' and o == 'aecp') or (d.tier1 == 'others-first' and x == 'aecp'):
            return arrive(o)
        if d.tier1 == 'others-first' and o == 'aecp':
            return math.floor(drain / c['record.aecp']) + 1
        if d.tier1 == 'aecp-first' and x == 'aecp' and not held_back(row, i, d):
            return q[o]
        return passes * q[o]
    ahead = {o: min(arrive(o), reach(o)) * c[f'record.{o}'] for o in TIER1 if o != x}
    aecp = rate['aecp'][0] if x == 'aecp' else min(arrive('aecp'), reach('aecp'))
    out = {'aecp': aecp * c['record.aecp']} if x == 'aecp' else \
        {'own': rate[x][0] * c[f'record.{x}'], 'aecp': ahead.pop('aecp')}
    out['others'] = sum(ahead.values())
    return {**out, **edit_terms(i, w_ms, aecp)}


def tx_passes(i: Inputs, d: Design, ticks: int, notice: float, arrive: Callable[[str], int]) -> int:
    """THE TRANSMIT's build waits for every tier-1 record arriving in its window, then is tier 2's first unit: the
    passes tier 1 takes them in, by its time a pass, or under QUOTA_ORDERS at each channel's quota."""
    if d.tier1 in QUOTA_ORDERS:
        q = per_pass(i, d)
        return max(math.ceil(arrive(o) / q[o]) for o in TIER1) + ticks + 2
    work = sum(arrive(o) * i.c[f'record.{o}'] for o in TIER1) + notice
    return math.ceil(work / i.h['CTRL_LOOP_DRAIN_US']) + ticks + 2


def tier1_busy(i: Inputs, d: Design) -> int:
    """The ordinary passes tier 1 holds a tier-2 row's work back for: its largest burst at its records a pass, or
    under QUOTA_ORDERS each channel's at its quota."""
    q = per_pass(i, d)
    if d.tier1 in QUOTA_ORDERS:
        return max(math.ceil(i.rate[o][0] / q[o]) for o in TIER1)
    return math.ceil(max(i.rate[o][0] for o in TIER1) / q['aecp'])


def channel_row(row: str, d: Design) -> bool:
    """Whether a row is solved as a tier-1 channel's (channel_passes, channel_records): an added channel row, or R4
    under an order the loop before this module's channel rows did not state."""
    return row in CHANNEL_BOUNDS or (row == 'R4' and d.tier1 not in ('turn', 'aecp-first'))


def tier1_records(row: str, i: Inputs, d: Design, passes: int, arrive: Callable[[str], int],
                  w_ms: float | None = None) -> dict[str, float]:
    """The tier-1 records ahead of the row's work in its window, AECP's apart, and for R4 AECP's own burst and for the
    MRPDU row its build; in a window of w_ms, the edits among AECP's (edit_rows.terms), which a LONG_ROWS row, None,
    charges at the largest legal command's record instead (paced_rows.record)."""
    h, c = i[0], i[1]
    if channel_row(row, d):
        return channel_records(row, i, d, passes, arrive, w_ms)
    q = per_pass(i, d)
    cap = q['aecp']
    if row == 'R4':
        # `turn`: each other channel its cap in each of AECP's passes; `aecp-first`: only the pass running as the burst
        # arrives, whose tier-1 records may still be in hand
        reach = (passes - 1) * cap if d.tier1 == 'turn' else cap
        count = {o: i[3]['aecp'][0] if o == 'aecp' else min(arrive(o), reach) for o in TIER1}
        out = {}
    elif row == 'first':
        # the pass running as the retry falls due: its tier-1 records, each channel's cap
        count = {o: min(arrive(o), q[o]) for o in TIER1}
        out = {}
    elif row in TX_ROWS:
        whole = d.slice_us >= h['CTRL_LOOP_BUILD_PASS_US']
        count = {o: arrive(o) for o in TIER1}
        out = {'builds': h['CTRL_LOOP_BUILD_PASS_US' if whole else 'CTRL_LOOP_BUILD_ONE_PASS_US']}
    else:
        count = {o: min(arrive(o), passes * q[o]) for o in TIER1}
        out = {}
    out = {'aecp': count['aecp'] * c['record.aecp'],
           'others': sum(count[o] * c[f'record.{o}'] for o in TIER1 if o != 'aecp'), **out}
    return {**out, **edit_terms(i, w_ms, count['aecp'])}


def join_cs(text: str) -> int:
    """The join time a header's text arms, CTRL_LOOP_JOIN_CS (ctrl_loop.h), in centiseconds."""
    return int(re.search(r'^#define CTRL_LOOP_JOIN_CS (\d+)u', text, re.M)[1])


#: The fabric's allowances ctrl_loop.h states, in ms (FR_NFR.md 3.4.1; #894's egress ruling of 2026-11-13, item 1).
ALLOWANCES = ('CTRL_LOOP_T_INGRESS_MS', 'CTRL_LOOP_T_EGRESS_MS')


def allowance(text: str, name: str) -> int:
    """One of the fabric's allowances (ALLOWANCES) a header's text states, in ms."""
    return int(re.search(rf'^#define {name} (\d+)u', text, re.M)[1])


def built_value(text: str, name: str, n_if: int, burst: int) -> int:
    """A built constant of a header's text at that many interfaces: `(MBX_N_IF == 1u ? a : b)`, a number, or derived
    from the join time and the egress allowance, `(240u - 10u * CTRL_LOOP_JOIN_CS - CTRL_LOOP_T_EGRESS_MS)` (#894's
    contingent ruling of 2026-11-13, item 3; its egress ruling, item 1); the burst a name of the mailbox contract
    (MBX_CH_AECP_RATE_BURST)."""
    body = re.search(rf'^#define {name} (.+)$', text, re.M)[1].split('//')[0].strip()
    body = re.sub(r'(\d+)u\b', r'\1', body).replace('MBX_CH_AECP_RATE_BURST', str(burst))
    body = body.replace('CTRL_LOOP_JOIN_CS', str(join_cs(text))) if 'CTRL_LOOP_JOIN_CS' in body else body
    for known in ALLOWANCES:
        body = body.replace(known, str(allowance(text, known))) if known in body else body
    pick = re.fullmatch(r'\(MBX_N_IF == 1 \? (\d+) : (\d+)\)', body)
    derived = re.fullmatch(r'\((\d+) - (\d+) \* (\d+)(?: - (\d+))?\)', body)
    if pick:
        return int(pick[1] if n_if == 1 else pick[2])
    return int(derived[1]) - int(derived[2]) * int(derived[3]) - int(derived[4] or 0) if derived else int(body)


def tx_budget_ms(text: str) -> int:
    """THE TRANSMIT's bound a header's text derives (ctrl_loop.h): Milan v1.2 Table 4.3's 240 ms JoinTime maximum less
    the armed join time and the egress allowance, so a requested opportunity is on the wire within it."""
    return 240 - 10 * join_cs(text) - allowance(text, 'CTRL_LOOP_T_EGRESS_MS')
