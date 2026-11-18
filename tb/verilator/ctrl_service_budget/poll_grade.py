# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The polls by source (#665): a light base every ordinary pass runs, and the heavy work,
each item its own function, which does its work only once its source has posted it, each at a stated cost.

A pass's polls run from the first firmware poll's entry, ADP's, to the last one's return, SRP's delivery (the
composition's order: ADP, ACMP, MAAP, AECP and its delivery, SRP and its delivery; a test fixture's poll comes after
them all). That section less the items inside it is the pass's base, which every ordinary pass is charged. Each item:

  withdraw   SRP's withdrawal of an interface whose link went down (srp_mbx.c, reset_interface), entered in the poll
             that sees the link level change; its source is a link change, one an interface
  rebuild    SRP's new participants for an interface whose link came back (open_interface), one interface a poll; a
             link change, one an interface
  walk       SRP's walk of a registrar whose attributes changed since the last (snapshot: lwSRP's mrp_attr_visit,
             entered only while the interface is stale); its sources are an attribute's state change, which an SRP
             record, a centisecond of lwSRP's timers and a declaration of THE TRANSMIT's make
  reclaim    lwSRP's reclaim of an interface's freed attributes (mrp_reclaim, entered only once a record or a build
             left one to free); its source is an SRP record or a build
  retained   SRP's retry of a record its participant refused for storage (apply_receive, one waits at a time); its
             source is an SRP record
  mrpdu      an MRPDU a build left owed (build_mrpdu, A3 of ctrl_loop.h, one a poll); its source is THE TRANSMIT's build
  acmp       ACMP's owed frame (acmp_mbx.c's poll, which sends one when ACMP owes one: A3); its sources are ACMP's
             responses and commands, from a record, an ADP record or a TMR_NO_RESP. A call that committed no ACMP frame
             sent nothing and is the base's. The item is the send less the offers nested in it (#908): THE KEPT
             COMMAND's redelivery, which runs only after a send (on_poll), offers the kept record and the records
             behind it to acmp_rx, and each offer is an ACMP record's own (below)
  acmp_declined  an offer acmp_rx declined (acmp_mbx.c: on_frame keeps the record, redeliver keeps it kept): a
             decline is told by its successor, since a declined record is kept and no later record is taken while it
             is (on_rx_ready, the redelivery's kept-first order), so the next offer is its re-offer, and an accepted
             one leaves none kept. Its bound: each re-offer follows its own send, and a command is first declined
             only once the one kept before it was accepted, after a send, so in any window the declined offers are at
             most two a sent owed frame and one (DECLINES, held over each log)

ACMP's offers that were accepted are its records' handling, one a command: a ring record's in its handler
(on_frame, record.acmp) and the kept record's in the redelivery, held to the same stated record cost (KEPT).
  aecp       AECP's owed response, a completed command's notification or a probe (aecp.c's transmit, which sends only
             what the core owes); its sources are AECP's records, its applies and its registrations' monitors. A call
             that committed no AECP frame sent nothing and is the base's
  aecp_long  an aecp item whose call committed a notice longer than AECP_FAN_BYTES (aecp.h), an unsolicited
             AEM_RESPONSE (IEEE 1722.1-2021 7.5.2) that fan_out sends a recipient at a time, which a command of the
             largest legal control_data_length answers (9.2.2.6; long_notice.py, #894)

An item nested in another (a walk inside a retained record's apply) is that one's, counted once. Calls outside the polls
(a record's own apply, a build's MRPDU, a round's notices, the LINK event's withdrawal) are their own source's, not the
polls'. A record's own apply, SRP's (apply_receive outside the polls, the record's handler's: RECORD), is the work its
retained retry repeats, so it is held to the same stated cost (#665): an SRP record
dearer than its retry's stated cost fails the gate as the retry would.

Each cost is the most measured over every group at its point plus 5 %, rounded up to 5 us (100 CPU cycles a
microsecond on the split CPU), or where no group stages an item the cost of the measured work that holds it (STATED_US):
a stated cost is an upper bound, and a gate fails when any measured instance exceeds it
(#665). Each item's arrival bound, from its source's protocol timer or
contract rate, is the response-time method's (docs/design/SPLIT_CONTROL_MEMORY.md section 13).
"""
from __future__ import annotations

import functools
import re
from bisect import bisect_left

import grade
import poll_items
import scenario
import shape_costs

#: A pass's first and last firmware poll, and each item's traced function and its sending channel (poll_items).
FIRST, LAST, ITEMS = poll_items.FIRST, poll_items.LAST, poll_items.ITEMS
#: The stated costs in microseconds at each shape ctrl_loop.h lists (THE SHAPES, shape_costs.Shape: MBX_N_IF,
#: CTRL_SRP_SOURCES, CTRL_SRP_SINKS; #894's held-egress ruling, item (b)(iii)), at 1x1/1if and 8x8/2if each
#: the most measured over every group of arm A and the answering-every-port arm at its point plus 5 %, rounded up to
#: 5 us, and the two-interface shapes both 8x8/2if's. No group stages a retained record or an MRPDU
#: its ring refused, so those two have no measured line: a retained record's retry is the apply an SRP record's handler
#: makes, stated at the SRP record's cost (285 and 365 us; 280 at 1x1/1if before AECP's REBOOT, #871), and an owed
#: MRPDU is a part of a build of one, stated at that pass's cost at the image's shape, CTRL_LOOP_BUILD_ONE_PASS_US as
#: THE SHAPES list it (735 us at 1x1/1if and 1,215 at 8x8/2if; #894's shape ruling, item (b)), which stated_us reads
#: where the table holds 0.
#: The SRP record's and AECP's item (a notice to the
#: registered controllers) are measured on the image whose notice is built once and addressed per recipient and whose
#: SRP comparisons are same()'s (#665: the notice and SRP record cuts), over every group of both arms. On the merge
#: of the TSN stack pin move to 715589c (#665), each cost is the larger of its measurement there and this table's:
#: ACMP's item at 1x1/1if takes the adapter's redelivery of the kept command and the records behind it, which a poll
#: that sends an owed frame now runs (acmp_mbx.c). On the merge of dev-soft-core 0fb66211 (#665), each cost, every item
#: the harness holds a pass's polls to, is the larger of its measurement there and this table's: the polls' base 205
#: and 325 us, the walk 35 at 1x1/1if and the rebuild 690 at 8x8/2if. Measured again on the image under THE TIERS
#: (#894), each the larger of that and this table's: ACMP's owed frame 195 and a notice 275 at 8x8/2if. A notice longer
#: than AECP_FAN_BYTES (aecp_long) is measured over the aecp-largest-notice group alone, the one that stages it
#: (long_notice.py, #894): a 550 B notice to 15 controllers, 34,359 CPU cycles at 1x1/1if, and to 31 on the 8x8 shape
#: with the answering-ports arm, 61,935, at the merge of #810's 084cf7a8 (33,815 and 61,578 before it), plus 5 %.
#: ACMP's item is its send less the offers THE KEPT COMMAND's redelivery nests in it, and a declined offer is its own
#: (#908): measured over backlog-owed, the one group that stages owed ACMP frames, on the image that traces acmp_rx at
#: the head ccb47e39, the send at most 4,744 and 6,134 CPU cycles (the whole poll 12,259 and 15,558 there) and a
#: declined offer 1,589 and 1,550, at 1x1/1if and 8x8/2if. Under #894's edit cut ACMP's item at 1x1/1if is 55 us, the
#: larger of this table's and its send of 4,890 CPU cycles in backlog-owed under the one-row edit's cut (4,723 at
#: 7398ec0a), the code after the map edit's moved by the cut, and at 8x8/2if 70 us, its send of 6,193 cycles in
#: backlog-owed (6,239 at 5b264bf2). With SRP's Talker declarations (#895), measured on their merge with that
#: cut, every group of arm A, the answering-every-port and valid-destinations arms and arm B's aecp groups, each
#: cost the larger of that and this table's: the polls' base at 1x1/1if 215 us, 20,282 CPU cycles in acmp-cmd, where
#: #894's own image measures 18,843 (200 us): MAAP's poll and SRP's delivery, which carry the Talker's declarations
#: and each source's stream_id (#905), and the polls around them, 79 instructions more in that pass; on its merge of
#: #894's SET_CONFIGURATION cut, with srp_mbx_gate's repeat call cut (#895), 225 us, 21,094 cycles in save-held
#: (19,793 before the merge), 262 instructions fewer and 49 more instruction refills in that pass than before, not
#: traced, the code's placement (#909); on that image with the 140 ms bound and the slice rule's 900 us (#895), at
#: 8x8/2if the polls' base 345 us, 32,705 cycles in the answering-every-port arm's notice-every-4, and a notice longer
#: than AECP_FAN_BYTES 700 us, 66,481 cycles in the answering-ports arm's aecp-largest-notice (#909, reported).
ONE = dict(base=225, withdraw=90, rebuild=290, walk=35, reclaim=25, retained=285, mrpdu=0, acmp=55, aecp=210,
           aecp_long=365, acmp_declined=20)
TWO = dict(base=345, withdraw=245, rebuild=690, walk=60, reclaim=35, retained=365, mrpdu=0, acmp=70, aecp=275,
           aecp_long=700, acmp_declined=20)
#: 8x8/1if's, one interface's 8x8 streams, each the most measured over every group of arm A on its built image, the
#: answering-every-port arm and the answering-ports arm's aecp-largest-notice on the tree that merges #902 (#894's
#: held-egress ruling, item (b)(iii)) plus 5 %, rounded up to 5 us: the base 21,995 CPU cycles,
#: the withdrawal 10,317, the rebuild 55,813, the walk 4,701, the reclaim 2,604, ACMP's owed frame 6,813 and a declined
#: offer 2,542, a notice 13,297 (the answering-every-port arm) and a long one 30,097; a retained record's retry at the
#: SRP record's measured cost there, 32,421 cycles, 345 us. On the image that merges #902's 234bc149 the walk is 4,905
#: (the srp group) and a notice 13,572 (the answering-every-port arm's notice-every-0), 55 and 145 us by the rule. On
#: the image that merges dev-soft-core 70f4056f (#901, SRP's Talker declarations), over every group of arm A, the
#: answering-every-port, valid-destinations and answering-ports arms, the base is 23,756 (save-held and save-starved)
#: and ACMP's owed frame 7,450 (backlog-owed), 250 and 80 us by the rule, as #901 found the base grown at 1x1/1if.
#: With every Talker declared beside a Listener Ready (srp-talker-held, #930): at 8x8/1if the base 26,255, the walk
#: 11,179, the reclaim 3,292 and a retained record's retry, an SRP record's apply, 42,449, 280, 120, 35 and 450 us by
#: the rule, and at 1x1/1if that apply 26,925, 285 us. Once a Listener's change walks no registrar (#930) the apply,
#: the one of these the cut moves, is 32,618 and 23,144 cycles, 345 and 245 us, so its own measurement states it:
#: 345 at 8x8/1if and 280 at 1x1/1if, an SRP record's there, 285 since AECP's REBOOT merged on the tiers (#871),
#: which 1x1/1if's states (ONE). Measured on that image over every group of every arm,
#: 8x8/1if's reclaim is 3,446 cycles in srp-talker-held, 40 us by the rule.
#: On the composed flip train's final head with attempt 2's cuts (#665's ruling of 2026-11-18, item 2): 8x8/1if base
#: 28,417 CPU cycles (the valid-destinations arm, srp-talker-held), 300 us; 8x8/1if retained 35,350 CPU cycles (the
#: valid-destinations arm, srp-talker-held), 375 us, each by the rule.
EIGHT_ONE = dict(base=300, withdraw=110, rebuild=590, walk=120, reclaim=40, retained=375, mrpdu=0, acmp=80, aecp=145,
                 aecp_long=320, acmp_declined=30)
STATED_US = {shape_costs.Shape(1, 2, 2): ONE, shape_costs.Shape(1, 9, 9): EIGHT_ONE, shape_costs.Shape(2, 2, 2): TWO,
             shape_costs.Shape(2, 9, 9): TWO}


#: An SRP record's own apply (srp_mbx:apply_receive outside the polls), held to the retained item's stated cost.
RECORD = 'record'
#: An aecp item that committed a notice longer than AECP_FAN_BYTES, held to its own stated cost.
LONG = 'aecp_long'
#: ACMP's offers (#908): one acmp_rx declined, held to its own stated cost; the kept record's accepted re-offer, an
#: ACMP record's handling, held to the stated record cost (load_grade.STATED_US' record.acmp); the offers an ACMP item
#: carries, subtracted from it and from the base and held one by one; and the declines over their bound.
DECLINED, KEPT, OFFERS, DECLINES = 'acmp_declined', 'acmp_kept', 'acmp_offers', 'acmp_declines'


@functools.cache
def fan_bytes() -> int:
    """AECP_FAN_BYTES (aecp.h): the longest notice the fan port takes; a longer one goes a recipient at a time."""
    text = (scenario.ROOT / 'sw/firmware/ctrl/aecp/aecp.h').read_text()
    return int(re.search(r'^#define AECP_FAN_BYTES (\d+)u', text, re.M)[1])


def long_notices(log: grade.Log) -> list[int]:
    """The bus cycle of each AECP commit of a notice longer than AECP_FAN_BYTES, sorted: an AEM_RESPONSE (message_type
    1) with the u bit set (IEEE 1722.1-2021 7.5.2), its command_type's top bit."""
    ch = scenario.CH['aecp']
    return sorted(cycle for cycle, c, _, frame in log.tx
                  if c == ch and len(frame) > fan_bytes() and frame[15] & 0x0F == 1 and frame[36] & 0x80)


def stated_us(interfaces: int | shape_costs.Shape) -> dict[str, int]:
    """The base's and each item's stated cost in microseconds at a shape, or at that many interfaces at the shipping
    shape's streams (shape_costs.shape); an owed MRPDU's a build of one's at the shape (shape_costs.at). A shape
    STATED_US does not state is refused."""
    shape = shape_costs.shape(interfaces, scenario.ROOT)
    if shape not in STATED_US:
        raise ValueError(f'poll_grade.py states no polls at the shape {tuple(shape)}')
    out = dict(STATED_US[shape])
    out['mrpdu'] = shape_costs.at(shape, scenario.ROOT)[shape_costs.BUILD_ONE]
    return out


def record_us(interfaces: int | shape_costs.Shape) -> int:
    """An ACMP record's stated cost in microseconds at that many interfaces, the point's at the pin
    (load_grade.STATED_US, the column the rows read), which the kept record's accepted re-offer is held to (KEPT,
    #908)."""
    import load_grade
    return load_grade.STATED_US['1x1/1if' if shape_costs.interfaces(interfaces) == 1 else '8x8/2if']['record.acmp']


def spans(log: grade.Log) -> dict[str, list[tuple[int, int, int]]]:
    """Each traced label's spans, sorted: (CPU cycle it started, CPU cycles, bus cycle it started)."""
    out: dict[str, list[tuple[int, int, int]]] = {}
    for kind, *rest in log.traced:
        if kind == 'SPAN' and len(rest) >= 5:
            out.setdefault(rest[4], []).append((int(rest[1]), int(rest[2]), int(rest[0])))
    for v in out.values():
        v.sort()
    return out


def sections(traced: dict[str, list[tuple[int, int, int]]]) -> list[tuple[int, int, int]]:
    """Each pass's polls: (CPU cycle the first poll entered, the cycle the last returned, the bus cycle it began),
    the last poll the first one after it, before the next pass's first."""
    firsts, lasts = traced.get(FIRST, []), traced.get(LAST, [])
    out = []
    starts = [s for s, _, _ in lasts]
    for k, (start, _, start_sys) in enumerate(firsts):
        nxt = firsts[k + 1][0] if k + 1 < len(firsts) else 1 << 62
        j = bisect_left(starts, start)
        if j < len(lasts) and lasts[j][0] < nxt:
            out.append((start, lasts[j][0] + lasts[j][1], start_sys))
    return out


def committed(log: grade.Log) -> dict[int, list[int]]:
    """Each channel's TX commits, the bus cycles sorted."""
    out: dict[int, list[int]] = {}
    for cycle, ch, _ in log.commits:
        out.setdefault(ch, []).append(cycle)
    for v in out.values():
        v.sort()
    return out


def instances(log: grade.Log, traced: dict, commits: dict[int, list[int]], start: int,
              end: int, longs: list[int] = ()) -> list[tuple[str, int]]:
    """The items inside a pass's polls that did their work, outermost first, each (kind, CPU cycles): an aecp item
    that committed a notice of `longs` (long_notices) is LONG's, and an acmp item is its send, the ACMP offers nested
    in it its OFFERS entry beside it (offers)."""
    found = []
    for kind, (label, channel) in ITEMS.items():
        rows = traced.get(label, [])
        for s, cycles, s_sys in rows[bisect_left(rows, (start, -1, -1)):]:
            if s >= end:
                break
            end_sys = s_sys + cycles * log.sys_hz // log.cpu_hz
            if channel is not None:
                marks = commits.get(scenario.CH[channel], [])
                if bisect_left(marks, end_sys) == bisect_left(marks, s_sys):
                    continue
            long = kind == 'aecp' and bisect_left(longs, end_sys) != bisect_left(longs, s_sys)
            found.append((s, s + cycles, LONG if long else kind))
    out = []
    for kind, s, cycles in outermost(found):
        nested = sum(o[1] for o in offers(traced, s, s + cycles)) if kind == 'acmp' else 0
        out += [(kind, cycles - nested)] + ([(OFFERS, nested)] if nested else [])
    return out


def outermost(found: list[tuple[int, int, str]]) -> list[tuple[str, int, int]]:
    """The items no other contains, each (kind, CPU cycle it started, CPU cycles): one nested in another is that
    one's."""
    outer, reach = [], -1
    for s, e, kind in sorted(found, key=lambda r: (r[0], -r[1])):
        if s >= reach:
            outer.append((kind, s, e - s))
            reach = e
    return outer


def offers(traced: dict, start: int = -1, end: int = 1 << 62) -> list[tuple[int, int, bool, int]]:
    """ACMP's offers that start in [start, end), in order, each (CPU cycle, its cost, whether it was the kept record's
    re-offer, the bus cycle): a ring record's, its handler's span (poll_items.HANDLER, the offer and its keep where it
    declined), and the redelivery's re-offer of the kept record, an acmp_rx call outside any handler (redeliver)."""
    handlers, calls = traced.get(poll_items.HANDLER, []), traced.get(poll_items.OFFER, [])
    out = [(s, c, False, s_sys) for s, c, s_sys in handlers[bisect_left(handlers, (start, -1, -1)):] if s < end]
    for s, c, s_sys in calls[bisect_left(calls, (start, -1, -1)):]:
        if s >= end:
            break
        k = bisect_left(handlers, (s + 1, -1, -1)) - 1
        if k < 0 or not handlers[k][0] <= s < handlers[k][0] + handlers[k][1]:
            out.append((s, c, True, s_sys))
    return sorted(out)


def offered(traced: dict, sends: int, limits: dict) -> tuple[dict, list[dict]]:
    """Each ACMP offer of the log graded (#908): an offer is declined exactly when the next offer is the kept record's
    re-offer (poll_items.OFFER), held to DECLINED's cost; the kept record's accepted re-offer is an ACMP record's
    handling, held to KEPT's; and the declines, at most two a send and one. The heaviest of each and those over."""
    every = offers(traced)
    heaviest, over = {DECLINED: 0, KEPT: 0}, []
    declines = 0
    for k, (_, cycles, kept, s_sys) in enumerate(every):
        declined = k + 1 < len(every) and every[k + 1][2]
        kind = DECLINED if declined else KEPT if kept else None
        declines += declined
        if kind is None:
            continue
        heaviest[kind] = max(heaviest[kind], cycles)
        if cycles > limits[kind]:
            over.append(dict(kind=kind, start_sys=s_sys, cycles=cycles))
    if declines > 2 * sends + 1:
        over.append(dict(kind=DECLINES, start_sys=0, cycles=declines, sends=sends))
    return heaviest, over


def held(log: grade.Log, interfaces: int | shape_costs.Shape) -> dict:
    """Each pass's base and each item against its stated cost in CPU cycles: the passes, the heaviest of each, every
    one over its cost, and each LONG item."""
    limits = {kind: us * log.cpu_hz // 1_000_000 for kind, us in stated_us(interfaces).items()}
    limits[RECORD] = limits['retained']
    limits[KEPT] = record_us(interfaces) * log.cpu_hz // 1_000_000
    traced, commits, longs = spans(log), committed(log), long_notices(log)
    heaviest = dict.fromkeys(limits, 0)
    over = []
    every, sent, sends = sections(traced), [], 0
    for start, end, start_sys in every:
        items = instances(log, traced, commits, start, end, longs)
        base = end - start - sum(cycles for _, cycles in items)
        for kind, cycles in [('base', base), *items]:
            sends += kind == 'acmp'
            if kind == OFFERS:
                continue
            heaviest[kind] = max(heaviest[kind], cycles)
            sent += [(start_sys, cycles)] if kind == LONG else []
            if cycles > limits[kind]:
                over.append(dict(kind=kind, start_sys=start_sys, cycles=cycles))
    # ACMP's offers, wherever they ran: the declined ones and the kept record's accepted re-offer (#908)
    found, beyond = offered(traced, sends, limits)
    heaviest.update(found)
    over += beyond
    # each SRP record's own apply: an apply_receive call in no pass's polls
    polls = [(start, end) for start, end, _ in every]
    for s, cycles, s_sys in traced.get(ITEMS['retained'][0], []):
        k = bisect_left(polls, (s + 1, -1)) - 1
        if k >= 0 and polls[k][0] <= s < polls[k][1]:
            continue
        heaviest[RECORD] = max(heaviest[RECORD], cycles)
        if cycles > limits[RECORD]:
            over.append(dict(kind=RECORD, start_sys=s_sys, cycles=cycles))
    # each LONG item, (the bus cycle its pass's polls began, CPU cycles): a long notice's polls, reported
    return dict(passes=len(every), heaviest=heaviest, limits=limits, over=over, long=sent)
