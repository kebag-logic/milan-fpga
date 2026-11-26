# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The long-window CPU load of every source at its stated arrival bound, by the response-time method's own terms
(#665; docs/design/SPLIT_CONTROL_MEMORY.md section 13), at 1x1/1if, 8x8/2if and 32x32/2if, held to a stated ceiling.

The load is the work the sources bring per millisecond of a window long enough that their bursts no longer count:
each source's arrival rate, from a contract rate (sw/mailbox/mailbox.yaml, read from the tree) or a protocol timer
(each clause below, its value read from the tree where the tree states it), times its stated cost. A pass's own cost
(its events' fixed part and its polls' base) is not a source, so it is not a term: it is reported beside the load.
At or above 1.0 no ordering of the work bounds a row; CEILING leaves room for the rows: 0.70 (#665, option D) at
1x1/1if, which this gate holds for merge, at the pin and with tsn-c-stack#32 (COLUMNS), each named in what it finds.
8x8/2if is held to the same 0.70 by the flip check, flip_grade.py, read at the pin, a check apart from the merge gates
(#665, #890); this table reports it. 32x32/2if is reported, not held: the more-compute image, #872 (decision D, #665);
the table gives the compute its load with tsn-c-stack#32 would need for 0.70, its load over 0.70, since every stated
cost is CPU time at the split CPU's clock. No term is kept as a margin: each has its source, and one without a source
fails.

Two columns of stated costs (#665): STATED_US at this tree's TSN stack pin, and STATED_US_DONOR, measured with
tsn-c-stack#32 (the ACMP core's completion walking only the sinks an entry changed) applied at the pin in a scratch
build. The gate holds 1x1/1if in both: the pin's column is the image that merges, and the donor's the load the pin
move owes, which carries tsn-c-stack #28, #31 and #32. The donor's column may state below the pin's only a cost whose
work runs the ACMP core's walk (WALK); any other such cost fails.

The pin already carries tsn-c-stack#32 (#930): 715589c is the merge of tsn-c-stack PR #34, which closed #32, and its
src/ and include/ are the donor's 9043b926, which the donor's column was measured on. So both columns state one
image's costs. The pin's column holds as well what images built before the pin moved measured for the five costs the
walk moves (WALK), the larger, since a statement never goes down; the donor's holds only what images carrying #32
measured. A ceiling is read at the pin's column (flip_grade.py's REPORTED point, the merge gate's own reading).

The terms (per millisecond):
  rec.<channel>  aecp, acmp, adp, maap: one record a refill, the fabric's limiter (mailbox.yaml `rate`), per channel
                 and not per stream, so the same at every shape; the burst is a window's first records, not a rate.
  srp            SRP's records, one a refill as rec.<channel>'s, and its retries of a record its participant refused
                 for storage (srp_mbx.c, the poll, #665: the retained retry's rule): a retry only once a pool
                 returned a block or lwSRP reported an Applicant or Registrar change of the interface since the
                 refusal, and at most one a centisecond, a TICK dispatched since the last (mailbox.yaml tick_ms); no
                 other SRP record is taken while one waits (srp_mbx.c's ready), for at most SRP_RX_RETRY_MS. The
                 retries come at the TICK's rate whatever the records', so SRP's channel brings both. The rule's
                 lines are read from the tree (RETRY_RULE): a retry it does not bound has no source.
  item.reclaim   lwSRP's reclaim of an interface's freed attributes (mrp_reclaim, entered after an SRP record or a
                 build left one to free): two participants a record or a build.
  item.aecp      AECP's owed frame, by what each source sends (#665): an AECP record's
                 response, to one recipient, with a command that changed something its notice to the registered
                 controllers, at most AECP_REGISTRATIONS an AVB interface (Milan v1.2 5.4.5.1; aecp.c, fan_out),
                 the larger of the two once a record; and a registration's probe, its own frame, once its 250 ms
                 retry (aecp.c; Milan v1.2 5.4.5.3), every interface's registrations.
  notices        each descriptor's COUNTERS_CHANGED notice, once a holdoff_ms (Milan v1.2 5.4.5.2, Table 5.22;
                 mailbox.yaml counters_changed), in THE RETRY's rounds, each a round's own at its stated costs
                 (aecp_mbx.h: AECP_ROUND_COLD_US and AECP_NOTICE_US, which round_grade.py holds every round to).
  item.acmp      ACMP's owed frame: one an ACMP record, one an ADP record (a bound talker's ENTITY_AVAILABLE, Milan
                 v1.2 5.6.4.1) and one a sink's TMR_NO_RESP (Milan v1.2 5.5.2.3, Table 5.26: ACMP_TMR_NO_RESP_MS);
                 its send less the offers THE KEPT COMMAND's redelivery nests in it, whose accepted ones are ACMP's
                 records, a command once (rec.acmp, #908).
  item.acmp_declined  ACMP's declined offers (acmp_mbx.c: a command acmp_rx declines is kept and offered again
                 after a send): at most two an owed frame sent, so twice item.acmp's rate (poll_grade.py, #908).
  ticks          a TICK a centisecond (mailbox.yaml tick_ms), each its consumers at the larger of their measured and
                 their stated cost (ctrl_loop.h, CTRL_LOOP_TICK_US).
  item.walk      an interface's registrar walk, at most one an interface a centisecond of lwSRP's timers, and one a
                 build's declaration.
  builds         THE TRANSMIT's builds, one a JoinTime a participant (IEEE 802.1Q-2018 10.7.4.1, Table 10-7; Milan v1.2
                 Table 4.3; srp_mbx.c, SRP_JOIN_CS): the interfaces' builds of both MRPDUs or twice as many of one,
                 whichever costs more.
  item.mrpdu     an MRPDU a build's ring had no room for (A3 of ctrl_loop.h): at most two a build.
  steps          THE STEP: one aged step each CTRL_LOOP_STEP_AGE + 1 centiseconds (ctrl_loop.h).
  timers         each timer slot at its own expiry rate, the sinks that can be due within a window at their timers:
                 ADP's (its advertise timer once ADP_ADVERTISE_MS, Milan v1.2 5.6.3.5.9, Table 5.50; one an ADP
                 record, which re-arms its delay, Milan v1.2 5.6.3.5.3; each bound sink's discovery
                 aging at the least valid time, 2 s, IEEE 1722.1-2021 6.2.2.5), ACMP's (a sink's TMR_NO_RESP, Milan
                 v1.2 5.5.2.3, Table 5.26), MAAP's probe (IEEE 1722-2016 B.3.4.2, Table B.8: MAAP_PROBE_BASE_MS less
                 MAAP_PROBE_VARIATION_MS) and AECP's (a registration's probe retry, 250 ms, Milan v1.2 5.4.5.3; a
                 descriptor's COUNTERS_CHANGED once a holdoff_ms, Milan v1.2 5.4.5.2, Table 5.22, mailbox.yaml).
  gm             the grandmaster event, coalesced (mailbox.yaml): at most one an interface an Announce and one a peer
                 delay exchange, each at its message interval (IEEE 802.1AS-2011 10.7.2.2, initialLogAnnounceInterval
                 0: 1 s; 11.5.2.2, initialLogPdelayReqInterval 0: 1 s), and one an announce receipt timeout (10.7.3.2,
                 announceReceiptTimeout 3 intervals).

Not terms, each with its reason: a LINK change has no arrival rate (a row's definition, R5, counts one an interface);
THE RETRY's rounds otherwise drain a queue a datapath reset leaves, at most AECP_NOTICES_MOST, a burst and not a rate,
and AVB_INFO_CHANGED, AS_PATH_CHANGED and AMAP_LIVE_WRITE are coalesced events with no contract rate (mailbox.yaml);
a pass's own cost is no source.

usage: python3 -I load_grade.py [--check] [--selftest]
  --check      print the load table and exit 1 if any point is over its ceiling
  --selftest   plant each control and exit 1 unless every one is refused
"""
from __future__ import annotations

import argparse
import functools
import math
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shape_costs  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
#: The ceiling the merge gate holds a point's load to (#665, option D): 1x1/1if. 8x8/2if is the
#: flip check's (flip_grade.FLIP, #665, #890); 32x32/2if is reported, not held: the
#: more-compute image, #872 (decision D, #665).
CEILING = {
    'arty-1x1': 0.7,'1x1/1if': 0.70}
#: What the table says in a point's ceiling column where CEILING holds none: the flip check's, or none.
FLIPPED = 'the flip check, {:.2f} at the pin (flip_grade.py)'
PENDING = 'reported: the more-compute image, #872'
#: The load the compute factor is reported against: the ceiling the held points are held to.
TARGET = 0.70
#: Each point's counts: interfaces, sinks an interface (counted all on each), registrations an interface
#: (aecp.h, AECP_REGISTRATIONS) and the descriptors with counters (each stream's, each AVB interface's and each clock
#: domain's; aecp.h, AECP_NOTICES_MOST's terms), at a point an image is built at the descriptors the shape header states
#: (shape_costs.findings holds them to it: the 8x8's 18 streams, one AVB interface and one clock domain).
POINTS = {
    'arty-1x1': {'n_if': 1, 'sources': 1, 'sinks_per_if': 2, 'registrations': 16, 'counter_descriptors': 5},
    '1x1/1if': dict(n_if=1, sinks_per_if=2, registrations=16, counter_descriptors=6),
          '8x8/2if': dict(n_if=2, sinks_per_if=8, registrations=16, counter_descriptors=20),
          '8x8/1if': dict(n_if=1, sinks_per_if=8, registrations=16, counter_descriptors=20),
          '32x32/2if': dict(n_if=2, sinks_per_if=16, registrations=16, counter_descriptors=68)}
#: The points whose stated costs are another's, the nearest shape each is measured at in both columns (#894's shape
#: ruling, item (b): 8x8/1if's load at most 0.75): 8x8/1if's records, events and THE STEP's pass are
#: 8x8/2if's, the 8x8 shape's at two interfaces, measured over every group of both arms there, as #894 derived that
#: load; THE TRANSMIT's builds and an owed MRPDU, a build of one's, are its own shape's (ctrl_loop.h, THE SHAPES), and
#: the polls' base and items its own shape's (poll_grade.STATED_US; the held-egress ruling, item (b)(iii)),
#: each measured on its built image on the tree that merges #902. stated() reads them so; its own measurement of the
#: rest is owed to #872.
NEAREST = {'8x8/1if': '8x8/2if'}
#: A NEAREST point's own statements, where its measurement passes its nearest point's (#894's ledger ruling, item 4):
#: the nearest point supplies a cost only while the point's measurement is within it, so where it is not, the point
#: states its own by the rule, in either column; the nearest point's table is untouched. OWN_MEASURED is each one's
#: measurement, CPU cycles and where: 8x8/1if's ADP record on the image that merges #902's 234bc149, 12,210 cycles,
#: 130 us by the rule, over 8x8/2if's 125 us in the tsn-c-stack#32 column (its pin column states 240); and its MAAP
#: record on the image that merges dev-soft-core 70f4056f (#901, SRP's Talker declarations), 16,323 cycles in the
#: valid-destinations arm's range lost to a peer's ANNOUNCE, 175 us by the rule, over 8x8/2if's 155 in both columns;
#: its SRP record, where a Listener Ready licenses a declared Talker (srp-talker-held), measured 42,663 cycles, 450 us
#: by the rule, over 8x8/2if's 365, until a Listener's change walked no registrar (#930): on that image it is 32,936,
#: 350 us, within 365, so 8x8/2if's supplies it again, as the cut's own measurement states the cost it moves. So with
#: 1x1/1if's record.srp, 290 us for that group's 27,170 cycles before the cut and 280 after it, over its 23,503.
#: On the composed flip train's final head with attempt 2's cuts (#665's ruling of 2026-11-18, item 2): 8x8/1if
#: record.maap 16,682 CPU cycles (the valid-destinations arm, srp-talker-loss), 180 us; 8x8/2if event.AECP 11,404 CPU
#: cycles (the answering-every-port arm, notice-burst-6: aecp.c arm()'s walk of the registry and the live notices),
#: 120 us; 8x8/2if events_none 4,069 CPU cycles (the valid-destinations arm, srp-talker-held), 45 us; 8x8/2if
#: record.maap 14,770 CPU cycles (the valid-destinations arm, srp-talker-loss), 160 us, each by the rule.
#: 8x8/1if's record.srp there, 35,547 CPU cycles (the valid-destinations arm, srp-talker-held), 375 us by the rule,
#: and ctrl_loop.h's CTRL_LOOP_SRP_UNIT_US with it (srp_unit), the unit following its record on the image that
#: carries it (#665's ruling of 2026-11-18, re-ruled, item 2b).
#: On the composed flip train's final head with attempt 2's cuts (#665's ruling of 2026-11-18, item 2): 8x8/1if
#: record.adp 12,779 CPU cycles (arm A, backlog-adp-refill, on the image that carries the unit at 375 us), 135 us,
#: each by the rule.
#: With a STREAM_OUTPUT's Listener registration notice (#957): 8x8/1if record.maap 17,259 CPU cycles (the
#: valid-destinations arm, srp-talker-loss; 16,176 on the flip train's head in the same group), 185 us by the rule. The
#: record runs none of the change's code: the 8 bytes each 8x8 interface's SRP state grew move the data after it.
OWN = {'8x8/1if': {'record.adp': 135, 'record.maap': 185, 'record.srp': 375}}
OWN_MEASURED = {'8x8/1if': {'record.adp': (12_779, 'arm A, backlog-adp-refill, unit 375 us'),
                            'record.maap': (17_259, 'the valid-destinations arm, srp-talker-loss'),
                            'record.srp': (35_547, 'the valid-destinations arm, srp-talker-held')}}
#: The stated costs in microseconds at each point at this tree's TSN stack pin, each the most measured over every
#: instance plus 5 %, rounded up to 5 us (100 CPU cycles a microsecond on the split CPU at sys, 100 MHz). At 1x1/1if and
#: 8x8/2if the polls' base and items are poll_grade.py's, which the harness holds every measured pass to, and THE
#: TRANSMIT's builds and THE STEP's pass are ctrl_loop.h's; the records', the events', a centisecond's consumers',
#: AECP's owed frames' and a pass's events' fixed part are this table's, the largest of four traced measurements: every
#: group of arm A on bc98d727's image; arm A's groups but the save groups, with the answering-every-port arm's, on
#: a30c9986's image (docs/design/SPLIT_CONTROL_MEMORY.md section 14); arm A's groups but the save groups on 3a1d14c2's
#: image, its SRP retry bounded by its source, with the answering-every-port arm's at 8x8/2if; and every group of arm A
#: and of the answering-every-port arm on this tree's image, its notice built once and addressed per recipient and its
#: SRP comparisons same()'s (#665: the notice and SRP record cuts), whose measurement alone states the three
#: costs those cuts move, an SRP record, its retained retry and a notice (section 13, the long-window load), measured
#: again with every row's response stated and the aecp group in arm A and arm B (#882), which moved no cost, and
#: again on the image whose record commits judge their own move (#665), which moved none of this column's, and again
#: on the image under THE TIERS (#894) at 1x1/1if and 8x8/2if, every group of arm A and of the answering-every-port
#: arm and arm B's aecp group, each cost the larger of that and this table's: at 1x1/1if an AECP record 235 us (205),
#: ADP's timer slot 115 (110), the TICK 40 to 45 and a pass's events' fixed part 25 to 30; at 8x8/2if AECP's timer
#: slot 105 (95) and a notice 275 (270), on the plan that 8x8/2if image is measured with (section 5);
#: on the merge of the TSN stack pin move to 715589c (#665), each cost the larger of that measurement and this
#: table's (the polls' and AECP's own at poll_grade.py's, which the redelivery's ACMP item restates), and again on the
#: merge of dev-soft-core 0fb66211 (#665), 8x8/2if on the image whose round's cold start is 185 us, each cost the larger
#: of that measurement and this table's; and again with SRP's Talker declarations (#895), every group of arm A, the
#: answering-every-port arm, the valid-destinations arm and arm B's aecp group, each cost the larger of that and this
#: table's: MAAP's record, a range lost to a peer's ANNOUNCE that restarts the core, 90 to 115 and 130 to 150 us, AECP's
#: timer slot at 1x1/1if 60 to 65, a TICK at 8x8/2if 40 to 45; on its merge with #810 each cost the larger of the two
#: sides', and on its merge with THE TIERS (#894) each cost the one of the side that moved it from their merge base
#: 084cf7a8, MAAP's record #895's and every other #894's (#895); measured again on that merge, the same groups, each
#: cost the larger of that and this table's: AECP's timer slot 65 to 75 and a TICK 45 to 50 at 1x1/1if, and at 8x8/2if
#: AECP's timer slot 105 to 115, a TICK 40 to 55, a pass's events' fixed part 30 to 35 and MAAP's record 150 to 155, the
#: code's placement the merge moves, not traced (#909); an AECP record stays #894's 235 us, which #894 checks (#895, the
#: ruling of 2026-11-14 on its composition, item 2); under #894's edit cut a TICK at 1x1/1if 45 to 50 us, the larger of
#: this table's and one TICK of 4,617 CPU cycles in arm A's backlog-adp@program-0 at 7398ec0a, AECP's sink sending an
#: owed frame inside it (the same TICK under the one-row edit's cut is 3,242; its most in the cut's arm A 4,612), and
#: ACMP's owed frame 50 to 55 us (poll_grade.py); at 8x8/2if, on its legs, a pass's events' fixed part 30 to 35 (2,859
#: cycles in notice-every-0; 2,093 at 5b264bf2) and ACMP's owed frame 65 to 70; on #895's merge of that cut (9606b3a9)
#: each cost the one of the side that moved it from their merge base 7398ec0a, the larger where both did (#895);
#: measured again on that merge, every group of arm A, the answering-every-port and valid-destinations arms and arm B's
#: aecp groups, each cost the larger of that and this table's: a pass's events' fixed part at 1x1/1if 30 to 35 us, 3,041
#: CPU cycles in notice-burst-0 (2,623 at #895's merge before that cut), not traced, the code's placement the cut moves
#: (#909), and the polls' base 205 to 215 (poll_grade.py), each in both columns (#895); and with the 1x1/1if slice at
#: the rule's 950 us, every group of every arm at both points, each cost the larger of that and this table's: MAAP's
#: timer slot at 8x8/2if 215 to 225 us, 21,120 CPU cycles in arm A's save group (19,993 at #895's merge with the tiers),
#: and a pass's events' fixed part there 35 to 40, 3,437 cycles in acmp-noresp, on the image with the 140 ms bound, not
#: traced, in both columns (#895); under #894's SET_CONFIGURATION cut (f275b619, paced at fe0cef5b), over every group of
#: arm A and of the answering-every-port arm, AECP's timer slot at 1x1/1if 65 to 70, both columns, the larger of this
#: table's and 6,206 CPU cycles in that arm's notice-burst-5 (5,753 at 9606b3a9, the same work, its fetches moved by the
#: cut's code), and with the SRP drain's record cost at the load gate's (ctrl_loop.h, a47cd3f2) a TICK at 1x1/1if 50 to
#: 55, both columns, 4,784 CPU cycles in arm A's backlog-adp@program-0; on #895's merge of that cut each cost the one of
#: the side that moved it from their merge base 9606b3a9, the larger where both did: AECP's timer slot at 1x1/1if #895's
#: 75, a TICK there #894's 55 (#895); with GET_AS_PATH read through the face (#897), over every group of arm A and of
#: the answering-every-port arm and arm B's legs on #894's tiers (234bc149), an AECP record at 1x1/1if 235 to 245, both
#: columns, 23,051 CPU cycles, that arm's SET_NAME in each of its sixteen groups (22,236 at 234bc149, the same work,
#: its fetches moved by the read's code), and on its merge of dev-soft-core 70f4056f (#901) each cost the one of the
#: side that moved it from their merge base 234bc149: an AECP record at 1x1/1if #897's 245, every other #895's (#897);
#: and on the merge of #894's tiers into AECP's REBOOT (#871), whose image moves the hot code, over every 1x1/1if
#: leg (all of arm A, the answering-every-port arm and arm B), both columns, each the larger of that and this
#: table's: SRP's record 285 us (26,865 CPU cycles in arm A's backlog-adp@blank-aged1-2), AECP's 240 (22,531, a
#: SET_NAME in the answering-every-port arm's notice-burst-0), a pass's events' fixed part 40 (3,627 in its
#: notice-burst-1), and a retained record's retry at SRP's record cost, 285; on that lane's merge of dev-soft-core
#: cb96336d (#898) each cost the one of the side that moved it from their merge base 41ca9f87, the larger where
#: both did: an AECP record at 1x1/1if #897's 245, a pass's events' fixed part #871's 40 (#871).
#: 32x32/2if is measured on the 32x32 simulation shape (#859), arm A's groups but the
#: save groups, each cost the larger of a30c9986's image's and this tree's. No group stages a retained record's retry,
#: an owed MRPDU or a registration's probe at any point, so they are stated at this table's SRP record cost, at a build
#: of one's (poll_grade.py's at 1x1/1if and 8x8/2if) and at a response's; the 32x32 shape has no saved state, so THE
#: STEP's pass is stated there at ctrl_loop.h's two-interface cost.
#: On the SRP cut's head (#665's ruling of 2026-11-20, item 3), measured over every arm and group, each 1x1/1if cost
#: it exceeds raised by the rule and the AECP notice item restated from its measurement by ruling item 4, as the owner
#: decided on 2026-11-20 (#665, ruling item 4), in both columns: an AECP record 250 us (23,726 CPU cycles, a
#: SET_STREAM_INFO in the declaring-outputs arm's aecp-fanout; the cut's code moves AECP's), a centisecond 170
#: (15,976 in valid-destinations' srp-talker-held) and the AECP notice item 150 (14,084 in the declaring-outputs
#: arm's aecp-fanout; 210 before). With a waiting SET_STREAM_FORMAT's running check made again (#950), whose code
#: moves AECP's, measured over every arm and group, 1x1/1if's AECP record raised by the rule in both columns: 255 us
#: (23,858 CPU cycles, the same SET_STREAM_INFO).
STATED_US = {
    'arty-1x1': {
        'record.srp': 300, 'record.aecp': 285, 'record.acmp': 240, 'record.adp': 120, 'record.maap': 120,
        'event.ADP': 95, 'event.ACMP': 165, 'event.MAAP': 155, 'event.AECP': 85, 'event.TICK': 45, 'event.GM': 40,
        'centisecond': 150, 'events_none': 40, 'item.retained': 300, 'item.aecp.notice': 205,
        'item.aecp.response': 45, 'item.aecp.probe': 45},
    '1x1/1if': {'record.srp': 285, 'record.aecp': 255, 'record.acmp': 280, 'record.adp': 105, 'record.maap': 115,
                'event.ADP': 115, 'event.ACMP': 185, 'event.MAAP': 165, 'event.AECP': 75, 'event.TICK': 55,
                'event.GM': 40, 'centisecond': 170, 'events_none': 40, 'item.retained': 285, 'item.aecp.notice': 150,
                'item.aecp.response': 60, 'item.aecp.probe': 60},
    '8x8/2if': {'record.srp': 365, 'record.aecp': 265, 'record.acmp': 440, 'record.adp': 240, 'record.maap': 160,
                'event.ADP': 120, 'event.ACMP': 350, 'event.MAAP': 225, 'event.AECP': 120, 'event.TICK': 55,
                'event.GM': 320, 'centisecond': 510, 'events_none': 45, 'item.retained': 365, 'item.aecp.notice': 275,
                'item.aecp.response': 65, 'item.aecp.probe': 65},
    '32x32/2if': {'record.srp': 865, 'record.aecp': 215, 'record.acmp': 980, 'record.adp': 735, 'record.maap': 205,
                  'event.ADP': 105, 'event.ACMP': 845, 'event.MAAP': 300, 'event.AECP': 55, 'event.TICK': 45,
                  'event.GM': 30, 'centisecond': 960, 'events_none': 20, 'base': 590, 'item.reclaim': 100,
                  'item.retained': 865, 'item.mrpdu': 7485, 'item.acmp': 665, 'item.acmp_declined': 0,
                  'item.aecp.notice': 350,
                  'item.aecp.response': 65, 'item.aecp.probe': 65, 'item.walk': 135,
                  'build': 10810, 'build_one': 7485, 'step': 1030}}
#: The stated costs with tsn-c-stack#32 at the pin (a scratch build of this tree's image whose stack is the pin with the
#: donor's change), the graded column, each cost stated at every point: each cost whose work runs the ACMP core's
#: completion walk (an ACMP record, an ADP record, ACMP's timer slot, ACMP's owed frame and the polls' base, through
#: SRP's delivery) its measurement there; every other cost the larger of that measurement and STATED_US's with the
#: polls' and the headers' (stated()). Measured on arm A's groups but the save groups, at 32x32/2if on the 32x32
#: simulation shape; at 1x1/1if and 8x8/2if on 3a1d14c2's image and on this tree's, each cost the larger of the two but
#: for the three the cuts move, which are this tree's. The answering-every-port arm does not fit the 8x8/2if ledger with
#: the donor (section 5), so the costs only that arm stages are STATED_US's. On the image whose record commits judge
#: their own move (#665), 1x1/1if is measured again, each cost the larger of that and this table's (ACMP's timer slot
#: 170 us, THE TRANSMIT's build 920); arm A's 8x8/2if image with the donor was over that point's ledger there. On the
#: merge of the pin move, whose pin 715589c carries tsn-c-stack#32 (its src/ and include/ the donor's 9043b926), both
#: points are measured on the pin's own legs, each cost the larger of that, this column's and, for a cost the walk does
#: not move, the pin's column. On the merge of dev-soft-core 0fb66211 (#665) both points are measured again on the
#: pin's legs, each cost the larger of that, this column's and the pin's; ctrl_loop.h states THE TRANSMIT's builds
#: at 1x1/1if at 1,010 and 725 us, and an owed MRPDU is a build of one's, so this column's are those; under #894's
#: SET_CONFIGURATION cut ctrl_loop.h states the build of one at 1x1/1if at 735 us, so this column's are 735. Every cost
#: that STATED_US's measurement on the image under THE TIERS (#894), or with GET_AS_PATH's read (#897), raised is
#: raised here with it, the larger.
#: Again so with SRP's Talker declarations (#895, the pin's legs above): beside the pin's moves, the polls' base 155 to
#: 160 and 285 to 290 us, and at 1x1/1if ACMP's owed frame 120 to 125 and the registrar walk 20 to 25. On #895's merge
#: with THE TIERS each cost is the one of the side that moved it from their merge base 084cf7a8: MAAP's record #895's,
#: every other #894's, ACMP's owed frame among them, itemised (#894); measured again on that merge, each cost
#: STATED_US's measurement raised is raised here with it, the larger: AECP's timer slot 75 and a TICK 50 at 1x1/1if,
#: and at 8x8/2if AECP's timer slot 110 to 115, a pass's events' fixed part 30 to 35 and MAAP's record 150 to 155, its
#: TICK's 85 the larger (#895); on #895's merge of #894's edit cut each cost the one of the side that moved it from
#: their merge base 7398ec0a, the larger where both did: ACMP's owed frame #894's, 55 and 70 us; measured again on
#: that merge, each cost STATED_US's measurement raised is raised here with it: a pass's events' fixed part 35 us and
#: the polls' base 215 at 1x1/1if, and MAAP's timer slot 225 at 8x8/2if; on its merge of #894's SET_CONFIGURATION
#: cut each cost the one of the side that moved it from their merge base 9606b3a9, the larger where both did: AECP's
#: timer slot 75 and a TICK 55 at 1x1/1if, a build of one and an owed MRPDU #894's 735; measured again on that merge
#: with srp_mbx_gate's repeat call cut, the polls' base 215 to 225 at 1x1/1if (poll_grade.py; #895); on that image
#: with the 140 ms bound and the slice rule's 900 us, at 8x8/2if a pass's events' fixed part 35 to 40 and the
#: polls' base 325 to 345 (poll_grade.py; #895, reported). On the merge of dev-soft-core 70f4056f each cost is the
#: one of the side that moved it from the merge base 234bc149: an AECP record at 1x1/1if #897's 245 (#897). On the SRP
#: cut's head, as STATED_US states (#665's owner decision of 2026-11-20, ruling item 4), and ADP's record
#: at 1x1/1if 105 us here too (9,585 CPU cycles in the answering-ports arm's backlog-adp-refill). With a waiting
#: SET_STREAM_FORMAT's running check made again (#950), the AECP record as STATED_US states it, 255 us.
STATED_US_DONOR = {
    'arty-1x1': {
        'record.srp': 300, 'record.aecp': 285, 'record.acmp': 240, 'record.adp': 120, 'record.maap': 120,
        'event.ADP': 95, 'event.ACMP': 165, 'event.MAAP': 155, 'event.AECP': 85, 'event.TICK': 45, 'event.GM': 40,
        'centisecond': 150, 'events_none': 40, 'item.retained': 300, 'item.aecp.notice': 205,
        'item.aecp.response': 45, 'item.aecp.probe': 45},
    '1x1/1if': {'record.srp': 285, 'record.aecp': 255, 'record.acmp': 265, 'record.adp': 105, 'record.maap': 115,
                'event.ADP': 115, 'event.ACMP': 170, 'event.MAAP': 170, 'event.AECP': 75, 'event.TICK': 55,
                'event.GM': 40, 'centisecond': 170, 'events_none': 40, 'item.aecp.notice': 150,
                'item.aecp.response': 60, 'item.aecp.probe': 60, 'base': 225, 'item.reclaim': 25, 'item.retained': 285,
                'item.mrpdu': 735, 'item.acmp': 55, 'item.walk': 35, 'build': 1010, 'build_one': 735, 'step': 975},
    '8x8/2if': {'record.srp': 365, 'record.aecp': 265, 'record.acmp': 305, 'record.adp': 125, 'record.maap': 160,
                'event.ADP': 120, 'event.ACMP': 210, 'event.MAAP': 225, 'event.AECP': 120, 'event.TICK': 85,
                'event.GM': 320, 'centisecond': 510, 'events_none': 45, 'item.aecp.notice': 275,
                'item.aecp.response': 65, 'item.aecp.probe': 65, 'base': 345, 'item.reclaim': 40, 'item.retained': 365,
                'item.mrpdu': 1215, 'item.acmp': 70, 'item.walk': 60, 'build': 2035, 'build_one': 1215, 'step': 1030},
    '32x32/2if': {'record.srp': 865, 'record.aecp': 215, 'record.acmp': 425, 'record.adp': 270, 'record.maap': 205,
                  'event.ADP': 105, 'event.ACMP': 330, 'event.MAAP': 300, 'event.AECP': 55, 'event.TICK': 45,
                  'event.GM': 30, 'centisecond': 960, 'events_none': 20, 'base': 570, 'item.reclaim': 105,
                  'item.retained': 865, 'item.mrpdu': 7485, 'item.acmp': 105, 'item.acmp_declined': 0,
                  'item.aecp.notice': 350,
                  'item.aecp.response': 65, 'item.aecp.probe': 65, 'item.walk': 140,
                  'build': 10810, 'build_one': 7485, 'step': 1030}}
#: The column stated() and the controls read by default: the donor's, the load the pin move owes.
GRADED = STATED_US_DONOR
#: The columns the merge gate holds each point of CEILING at, each to the ceiling, and names in what it finds: this
#: tree's pin, the image that merges, and the donor's (#665: 1x1/1if at the pin and with tsn-c-stack#32, each at most
#: 0.70).
COLUMNS = (('at the pin', STATED_US), ('with tsn-c-stack#32', STATED_US_DONOR))
#: Each column's name and the table it must read, by identity: unbound() refuses any other binding (#665).
BOUND = (('at the pin', 'STATED_US'), ('with tsn-c-stack#32', 'STATED_US_DONOR'))
#: The costs whose work runs the ACMP core's completion walk, which tsn-c-stack#32 changes: the donor column may state
#: these below the pin's, and no other (a cost #32 does not touch measured lower there is the measurement's spread).
WALK = ('record.acmp', 'record.adp', 'event.ACMP', 'item.acmp', 'base')
#: The headers the rows by every source read the loop's and AECP's constants from (rows_grade.header).
ROW_HEADERS = ('sw/firmware/ctrl/loop/ctrl_loop.h', 'sw/firmware/ctrl/aecp/aecp.h', 'sw/firmware/ctrl/aecp/aecp_mbx.h')
#: The least valid_time an ADPDU may carry, in ms: one unit of two seconds (IEEE 1722.1-2021 6.2.2.5), the
#: shortest a bound sink's discovery aging can run.
ADP_LEAST_VALID_MS = 2000
#: The grandmaster event's sources an interface, each once an interval, in ms: an Announce
#: (initialLogAnnounceInterval 0, IEEE 802.1AS-2011 10.7.2.2), a peer delay exchange (initialLogPdelayReqInterval
#: 0, 11.5.2.2) and an announce receipt timeout (announceReceiptTimeout 3 intervals, 10.7.3.2).
GM_INTERVALS_MS = (1000, 1000, 3000)
#: The poll items the load counts (poll_grade.py's names); AECP's owed frame is the table's, by what each source sends.
ITEMS = ('base', 'reclaim', 'retained', 'mrpdu', 'acmp', 'walk', 'acmp_declined')
#: THE TRANSMIT's and THE STEP's stated costs (ctrl_loop.h), at a point the headers state them for.
HEADER_COSTS = ('CTRL_LOOP_BUILD_PASS_US', 'CTRL_LOOP_BUILD_ONE_PASS_US', 'CTRL_LOOP_STEP_PASS_US')
#: The retained receive's retry rule (#665), each part as the tree states it, read with
#: its white space folded: the poll retries only once a pool returned a block or an Applicant or Registrar of the
#: interface moved since the refusal, and spends the centisecond's retry; the centisecond's consumer gives it back; a
#: refusal records what it saw; each change is marked and each return counted; and the poll is the only retry.
RETRY_RULE = {
    'a retry only once the refusal\'s inputs changed, one a centisecond':
        ('sw/firmware/ctrl/srp/srp_mbx.c', 'if (!i->moved && ctrl_pool_returned == m->pending_freed) { '
         'expire_receive(m); } else if (!m->retry_spent) { m->retry_spent = true; '
         'if (apply_receive(m,&m->pending_rx)) {'),
    'a centisecond\'s retry': ('sw/firmware/ctrl/srp/srp_mbx.c', 'shlan_timer_tick(); m->retry_spent = false;'),
    'what a refusal saw': ('sw/firmware/ctrl/srp/srp_mbx.c', '++m->refused; // What the refusal saw, after every '
                           'change of its own (poll). i->moved = false; m->pending_freed = ctrl_pool_returned; '
                           'return false;'),
    # the observer marks every change, after the SRP cut's reclaim test and creation count (#665's ruling of
    # 2026-11-20, item 3)
    'each Applicant or Registrar change marked': ('sw/firmware/ctrl/srp/srp_mbx.c',
                                                  '++i->fresh; } i->moved = true;'),
    'each returned block counted': ('sw/firmware/ctrl/port/ctrl_pool.c', 'bin->free_count++; ctrl_pool_returned++;'),
}


def macros(root: Path, n_if: int | shape_costs.Shape) -> dict[str, int]:
    """The integer constants the load reads from the tree, at a shape's interfaces or at that many; THE TRANSMIT's
    builds as ctrl_loop.h lists them at the shape, or with an interface count at the shipping shape's streams
    (shape_costs.at, THE SHAPES; #894's shape ruling, item (b))."""
    text = ''.join((root / p).read_text() for p in (
        'sw/firmware/ctrl/loop/ctrl_loop.h', 'sw/firmware/ctrl/srp/srp_mbx.c', 'sw/firmware/ctrl/aecp/aecp_mbx.h',
        'third_party/tsn-c-stack/include/acmp.h', 'third_party/tsn-c-stack/include/maap.h',
        'third_party/tsn-c-stack/include/adp.h'))
    found = {m[1]: m[2].split('//')[0].strip() for m in re.finditer(r'^#define (\w+) (.+)$', text, re.M)}
    found.update({name: f'{us}u' for name, us in shape_costs.at(n_if, root).items()})
    count = shape_costs.interfaces(n_if)

    def value(name: str) -> int:
        """A plain integer, a ternary on the interface count, or another constant's name (srp_mbx.c's SRP_JOIN_CS is
        ctrl_loop.h's CTRL_LOOP_JOIN_CS, #894's contingent ruling of 2026-11-13, item 3)."""
        body = found[name]
        if body in found:
            return value(body)
        plain = re.fullmatch(r'\(?(\d+)u?\)?', body)
        if plain:
            return int(plain[1])
        pick = re.fullmatch(r'\(MBX_N_IF == (\d+)u \? (\d+)u : (\d+)u\)', body)
        if pick is None:
            raise ValueError(f'{name} is {body!r}, neither an integer nor a ternary on MBX_N_IF')
        return int(pick[2] if count == int(pick[1]) else pick[3])
    names = (*HEADER_COSTS, 'CTRL_LOOP_TICK_US', 'CTRL_LOOP_STEP_AGE', 'SRP_RX_RETRY_MS', 'SRP_JOIN_CS',
             'ACMP_TMR_NO_RESP_MS', 'MAAP_PROBE_BASE_MS', 'MAAP_PROBE_VARIATION_MS', 'ADP_ADVERTISE_MS',
             'AECP_NOTICE_US', 'AECP_ROUND_COLD_US')
    return {n: value(n) for n in names}


#: The points whose SRP drain ctrl_loop.h's CTRL_LOOP_SRP_UNIT_US bounds: the slice starts an SRP record only while it
#: has that left (ctrl_loop.c), so it is the load gate's record.srp there, the dearer of the two columns' (#894),
#: read at the point's shape as THE SHAPES list it (shape_costs.at), never by its interface count; at 8x8/1if the
#: record.srp its NEAREST point's records state (stated).
SRP_UNIT_POINTS = ('1x1/1if', '8x8/2if', '8x8/1if', 'arty-1x1')
SRP_UNIT_HEADER = shape_costs.HEADER


def srp_unit(root: Path, texts: dict[str, str] | None = None) -> list[str]:
    """Each point whose SRP drain limit (CTRL_LOOP_SRP_UNIT_US at its shape, from the header or its planted copy) is
    not the load gate's record.srp there: a limit below it starts a record the slice has no room for."""
    out = []
    for point in SRP_UNIT_POINTS:
        try:
            got = shape_costs.at(shape_costs.of_point(point, root), root, texts)[shape_costs.SRP_UNIT]
        except ValueError as refused:
            out.append(f'{point}: {refused}')
            continue
        want = max(stated(root, point, column)['record.srp'] for _, column in COLUMNS)
        if got != want:
            out.append(f"{point}: ctrl_loop.h states CTRL_LOOP_SRP_UNIT_US {got} us, not the load gate's record.srp "
                       f'{want} us')
    return out


def unit_planted(header: str, shape: shape_costs.Shape, us: int) -> str:
    """The header with the SRP drain's limit in one shape's block of THE SHAPES stated as us."""
    lines = header.splitlines(keepends=True)
    head = f'CTRL_LOOP_SHAPE({shape.interfaces}u, {shape.sources}u, {shape.sinks}u)'
    k = next(k for k, line in enumerate(lines) if line.startswith(('#if ', '#elif ')) and head in line)
    k += next(j for j, line in enumerate(lines[k:]) if line.startswith('#define CTRL_LOOP_SRP_UNIT_US '))
    lines[k] = f'#define CTRL_LOOP_SRP_UNIT_US {us}u\n'
    return ''.join(lines)


def rule_us(cycles: int) -> int:
    """A measured cost's statement by the rule: its time at 100 MHz plus 5 %, rounded up to 5 us."""
    return int(math.ceil(cycles * 1.05 / 100 / 5 - 1e-9) * 5)


def own_findings(root: Path) -> list[str]:
    """Each NEAREST point's own statement not its measurement's by the rule, and each column that states the point a
    cost under that measurement (OWN, OWN_MEASURED)."""
    out = []
    for point, costs in OWN_MEASURED.items():
        for k, (cycles, where) in costs.items():
            want, own = rule_us(cycles), OWN.get(point, {}).get(k)
            if own != want:
                out.append(f"{point}: its own {k} is stated {own} us, not its measurement's {want} us by the rule "
                           f'({cycles:,} CPU cycles, {where})')
            for name, column in COLUMNS:
                got = stated(root, point, column)[k]
                if got < want:
                    out.append(f"{point}: {k} is {got} us {name}, under its measurement's {want} us by the rule "
                               f'({cycles:,} CPU cycles, {where})')
    return out


def probe_retry_ms(root: Path) -> int:
    """A registration's probe retry (aecp.c: its deadline now + this, Milan v1.2 5.4.5.3)."""
    return int(re.search(r'\.deadline = now\(a\) \+ (\d+)u;', (root / 'sw/firmware/ctrl/aecp/aecp.c').read_text())[1])


def retry_unbounded(root: Path, texts: dict[str, str] | None = None) -> list[str]:
    """Each part of the retry rule the tree does not state, and a second retry site: a retry it does not bound."""
    def folded(path: str) -> str:
        """The file's text (or its planted copy), its white space folded."""
        return ' '.join(((texts or {}).get(path) or (root / path).read_text()).split())
    out = [name for name, (path, line) in RETRY_RULE.items() if line not in folded(path)]
    if folded('sw/firmware/ctrl/srp/srp_mbx.c').count('apply_receive(m,&m->pending_rx)') != 1:
        out.append('the poll the only retry')
    return out


@functools.lru_cache(maxsize=4)
def parsed(text: str) -> dict:
    """A YAML text's document, parsed once a text: the contract is read by every load and row the checks plant."""
    return yaml.safe_load(text)


def contract(root: Path) -> dict:
    """Each receive channel's refill in ms, the TICK period and the counters' holdoff, from the mailbox contract."""
    text = (root / 'sw/mailbox/mailbox.yaml').read_text()
    y = parsed(text)
    holdoff = re.search(r'^\s+holdoff_ms: (\d+)', text, re.M)
    return dict(refill={c['name']: c['rate']['refill_ms'] for c in y['channels']}, tick_ms=y['tick_ms'],
                holdoff_ms=int(holdoff[1]))


def shape(point: str, root: Path = ROOT) -> int | shape_costs.Shape:
    """The shape a point is built at (shape_costs.of_point), or for a point no image is built at its interface
    count."""
    return shape_costs.of_point(point, root) if point in shape_costs.BUILT else POINTS[point]['n_if']


def stated(root: Path, point: str, table: dict | None = None) -> dict[str, float]:
    """A point's stated costs: the table's, or its NEAREST point's, the polls' (poll_grade.py) and the headers'
    where the table has none; THE TRANSMIT's builds, an owed MRPDU and, at a NEAREST point, the polls at the point's own
    shape."""
    import poll_grade
    near = NEAREST.get(point, point)
    c = dict((table or GRADED)[near])
    if near != point:
        c.update({k: us for k, us in OWN.get(point, {}).items() if c.get(k, 0) < us})
    if point in shape_costs.BUILT:
        polls = poll_grade.stated_us(shape(point, root))
        for k in ITEMS:
            key = 'base' if k == 'base' else f'item.{k}'
            c[key] = polls[k] if near != point else c.get(key, polls[k])
        h = macros(root, shape(point, root))
        own = {'build': h['CTRL_LOOP_BUILD_PASS_US'], 'build_one': h['CTRL_LOOP_BUILD_ONE_PASS_US'],
               'item.mrpdu': poll_grade.stated_us(shape(point, root))['mrpdu']}
        if near != point:
            c.update(own)
        for k, us in own.items():
            c.setdefault(k, us)
        c.setdefault('step', (macros(root, POINTS[near]['n_if']) if near != point else h)['CTRL_LOOP_STEP_PASS_US'])
    return c


def load(root: Path, point: str, table: dict | None = None) -> dict[str, float]:
    """Each term's CPU microseconds per millisecond of a long window (a share of the CPU, in thousandths)."""
    s, k, h = POINTS[point], contract(root), macros(root, shape(point, root))
    c, n_if, refill = stated(root, point, table), POINTS[point]['n_if'], contract(root)['refill']
    join_ms = 10 * h['SRP_JOIN_CS']
    both, one = n_if * c['build'], 2 * n_if * c['build_one']
    builds, n_builds = (both, n_if) if both >= one else (one, 2 * n_if)
    out = {f'rec.{ch}': c[f'record.{ch}'] / refill[ch] for ch in ('aecp', 'acmp', 'adp', 'maap')}
    # SRP's channel: its records, and a retained record's retries at the TICK's rate (the retry's own rule)
    out['srp'] = c['record.srp'] / refill['srp'] + c['item.retained'] / k['tick_ms']
    out['item.reclaim'] = c['item.reclaim'] * 2 * (1 / refill['srp'] + n_builds / join_ms)
    probe = probe_retry_ms(root)
    # AECP's owed frame by what each source sends: a record's response, or a command's with its notice; a probe's frame
    record_frame = max(c['item.aecp.response'], c['item.aecp.notice'])
    out['item.aecp'] = record_frame / refill['aecp'] + n_if * s['registrations'] * c['item.aecp.probe'] / probe
    out['notices'] = s['counter_descriptors'] * (h['AECP_ROUND_COLD_US'] + h['AECP_NOTICE_US']) / k['holdoff_ms']
    no_resp = h['ACMP_TMR_NO_RESP_MS']
    sends = 1 / refill['acmp'] + 1 / refill['adp'] + n_if * s['sinks_per_if'] / no_resp
    out['item.acmp'] = c['item.acmp'] * sends
    out['item.acmp_declined'] = c['item.acmp_declined'] * 2 * sends
    out['ticks'] = (c['event.TICK'] + max(c['centisecond'], h['CTRL_LOOP_TICK_US'])) / k['tick_ms']
    out['item.walk'] = c['item.walk'] * (n_if / k['tick_ms'] + n_builds / join_ms)
    out['builds'] = builds / join_ms
    out['item.mrpdu'] = 2 * n_builds * c['item.mrpdu'] / join_ms
    out['steps'] = c['step'] / (k['tick_ms'] * (h['CTRL_LOOP_STEP_AGE'] + 1))
    maap_ms = h['MAAP_PROBE_BASE_MS'] - h['MAAP_PROBE_VARIATION_MS']
    adp = c['event.ADP'] * (1 / refill['adp'] + 1 / h['ADP_ADVERTISE_MS'] + s['sinks_per_if'] / ADP_LEAST_VALID_MS)
    acmp = c['event.ACMP'] * s['sinks_per_if'] / no_resp
    aecp = c['event.AECP'] * (n_if * s['registrations'] / probe + s['counter_descriptors'] / k['holdoff_ms'])
    out['timers'] = n_if * (adp + acmp + c['event.MAAP'] / maap_ms) + aecp
    out['gm'] = n_if * c['event.GM'] * sum(1 / ms for ms in GM_INTERVALS_MS)
    return {term: us / 1000 for term, us in out.items()}


def documented() -> set[str]:
    """The terms the module's docstring names, each with its source: a line of its term list."""
    terms = __doc__.split('The terms (per millisecond):')[1].split('Not terms')[0]
    found = set(re.findall(r'^  ([a-z][\w.<>]*) {2,}', terms, re.M))
    channels = re.search(r'^  rec\.<channel> +([a-z, ]+):', terms, re.M)
    return (found - {'rec.<channel>'}) | {f'rec.{ch.strip()}' for ch in channels[1].split(',')}


def unsourced(terms: dict[str, float]) -> list[str]:
    """Each term the load counts with no source in the term list: a term without a source is not kept."""
    return sorted(set(terms) - documented())


def pass_own_us(root: Path, point: str, table: dict | None = None) -> float:
    """A pass's own cost, reported beside the load: its events' fixed part and its polls' base."""
    c = stated(root, point, table)
    return c['events_none'] + c['base']


def below_pin(root: Path, table: dict | None = None, pin_table: dict | None = None) -> list[str]:
    """Each cost the graded column states below the pin's that tsn-c-stack#32 does not move (not in WALK)."""
    out = []
    graded = table or GRADED
    for point in graded:
        pin, donor = stated(root, point, pin_table or STATED_US), stated(root, point, graded)
        out += [f'{point}: the graded column states {key} at {donor[key]} us, below the pin\'s {pin[key]}, and '
                f'tsn-c-stack#32 does not move it' for key in sorted(pin) if key not in WALK and
                donor.get(key, pin[key]) < pin[key]]
    return out


def unbound() -> list[str]:
    """COLUMNS not bound as BOUND says, each column's name to its own table and no column more or fewer, as one
    finding naming the table each name reads (#665: a swap prints each HELD line with the other column's load and holds
    neither by its name, so --check itself refuses it)."""
    tables = {'STATED_US': STATED_US, 'STATED_US_DONOR': STATED_US_DONOR}
    if len(COLUMNS) == len(BOUND) and all(name == want and table is tables[source]
                                          for (name, table), (want, source) in zip(COLUMNS, BOUND)):
        return []
    read = [(name, next((n for n, t in tables.items() if table is t), 'another table')) for name, table in COLUMNS]
    return [f"a column's name bound to the other's table, or a column not the gate's: {read}, not {list(BOUND)}"]


def findings(root: Path, table: dict | None = None, ceiling: dict | None = None,
             texts: dict[str, str] | None = None, pin: dict | None = None) -> list[str]:
    """Each point over its ceiling in either column the gate holds it at (COLUMNS: at the pin, and with
    tsn-c-stack#32; `pin` and `table` stand in for them), each named; each point whose table lacks a cost the load
    needs, a term without its source (one the term list does not name, or SRP's retries where the tree states no rule
    that bounds them), a graded cost below the pin's that tsn-c-stack#32 does not move, and a column bound to another
    table than its name's (unbound)."""
    out = unbound() + srp_unit(root, texts) + own_findings(root)
    out += [f'the term srp has no source: srp_mbx.c states no {part}' for part in retry_unbounded(root, texts)]
    out += below_pin(root, table, pin)
    planted = {'at the pin': pin, 'with tsn-c-stack#32': table}
    for point, top in (ceiling or CEILING).items():
        for name, column in COLUMNS:
            try:
                terms = load(root, point, planted[name] or column)
            except KeyError as missing:
                out.append(f'{point}: no stated cost {missing} {name}')
                continue
            out += [f'{point}: the term {term} has no source in the term list' for term in unsourced(terms)
                    if name == COLUMNS[0][0]]
            total = sum(terms.values())
            if total > top:
                out.append(f'{point}: the load {total:.3f} {name} is over its ceiling {top:.2f}')
    return out


def ceiling(point: str) -> str:
    """A point's ceiling as the table prints it: the merge gate's, the flip check's (FLIPPED), or PENDING."""
    import flip_grade
    return f'{CEILING[point]:.2f}, both columns' if point in CEILING else \
        FLIPPED.format(flip_grade.FLIP[point]) if point in flip_grade.FLIP else PENDING


def report(root: Path, table: dict | None = None) -> list[str]:
    """The load table: each point's load at the pin and with tsn-c-stack#32 (graded), its ceiling, the compute the
    graded load would need for TARGET (its load over TARGET, at least 1), its pass's own cost and every graded term by
    share."""
    lines = ["| Point | Load at the pin | Load at the donor's measured costs (the pin carries tsn-c-stack#32) | "
             f'Ceiling | Compute for {TARGET:.2f} (with tsn-c-stack#32) | A pass\'s own cost, us | Terms by share '
             '(with tsn-c-stack#32) |',
             '|---|---:|---:|---:|---:|---:|---|']
    for point in POINTS:
        try:
            pin, terms = load(root, point, STATED_US), load(root, point, table)
        except KeyError as missing:
            lines.append(f'| {point} | none | none | {ceiling(point)} | | | no stated cost {missing} |')
            continue
        ranked = sorted(terms.items(), key=lambda t: -t[1])
        total = sum(terms.values())
        lines.append(f"| {point} | {sum(pin.values()):.3f} | {total:.3f} | {ceiling(point)} | "
                     f"{max(1.0, total / TARGET):.2f}x | {pass_own_us(root, point, table):.0f} | "
                     + ', '.join(f'{t} {v:.3f}' for t, v in ranked) + ' |')
    return lines


def held(root: Path) -> list[str]:
    """Each point the gate holds, in each column it holds it at: its load and its ceiling."""
    return [f'HELD {point} {name}: the load {sum(load(root, point, column).values()):.3f}, its ceiling {top:.2f}'
            for point, top in CEILING.items() for name, column in COLUMNS]


def controls(root: Path) -> list[str]:
    """Each planted defect the gate must refuse: the planted names that escaped."""
    base = {p: dict(GRADED[p]) for p in GRADED}
    # a ceiling every planted table fits, at both points the ruling holds at 0.70 (this gate's and the flip check's)
    fit = {p: 10.0 for p in ('1x1/1if', '8x8/2if')}
    escaped = []
    # a point's load over its ceiling: a cost raised until the total passes it
    raised = {p: dict(v) for p, v in base.items()}
    raised['8x8/2if']['record.acmp'] = 100_000
    if not any('8x8/2if: the load' in f for f in findings(root, raised, {'8x8/2if': 10.0})):
        escaped.append('a cost over the ceiling')
    # each point held at 0.70 (#665: the long-window ceiling, option D): 1x1/1if by this gate as it stands,
    # 8x8/2if by the flip check at the pin (#890); a cost raised at each until the
    # load passes 0.70 must fail the check that holds it
    import flip_grade
    over = {p: dict(v) for p, v in base.items()}
    over['1x1/1if']['record.acmp'] = 100_000
    pin = {p: dict(v) for p, v in STATED_US.items()}
    pin['8x8/2if']['record.acmp'] = 100_000
    if CEILING != {'1x1/1if': 0.70, 'arty-1x1': 0.70} or \
            not any('1x1/1if: the load' in f for f in findings(root, over)) or \
            flip_grade.FLIP.get('8x8/2if') != 0.70 or not any('8x8/2if: the load' in f
                                                              for f in flip_grade.findings(root, pin)):
        escaped.append('a held point not held')
    # a rise at the pin alone (#665: 1x1/1if held at the pin as well as with tsn-c-stack#32): an ACMP record, a cost
    # the donor's walk may state lower, raised in the pin's column only until the pin's load passes 0.70, the donor's
    # column at its own; the gate refuses it, naming the pin's column
    risen = {p: dict(v) for p, v in STATED_US.items()}
    risen['1x1/1if']['record.acmp'] = 2000
    found = findings(root, pin=risen)
    if not any(f.startswith('1x1/1if: the load') and ' at the pin is over' in f for f in found) or \
            sum(load(root, '1x1/1if', risen).values()) <= 0.70 or \
            any('with tsn-c-stack#32 is over' in f for f in found):
        escaped.append('a rise at the pin alone')
    # a cost the load needs, missing from a point's table
    dropped = {p: dict(v) for p, v in base.items()}
    dropped['8x8/2if'].pop('event.ACMP')
    if not any("no stated cost 'event.ACMP'" in f for f in findings(root, dropped, fit)):
        escaped.append('a stated cost missing')
    # the retry's own rule: a retained record is retried once a centisecond at most, whatever its records, so SRP's
    # channel brings its records and those retries both (one of them alone is not the rule)
    c8, k = stated(root, '8x8/2if', base), contract(root)
    rule = c8['record.srp'] / k['refill']['srp'] + c8['item.retained'] / k['tick_ms']
    if not load(root, '8x8/2if', base)['srp'] >= rule / 1000 - 1e-9:
        escaped.append('the retained retry counted once a record')
    # the retry's source: a tree whose poll retries with nothing changed, or every pass a change allows, states no rule
    # that bounds the retries, so the term srp has none (#665: the retained retry's rule)
    srp = (root / 'sw/firmware/ctrl/srp/srp_mbx.c').read_text()
    for name, old, new in (('a retry with nothing changed',
                            'if (!i->moved && ctrl_pool_returned == m->pending_freed) {', 'if (false) {'),
                           ('a retry every pass', '                m->retry_spent = true;\n', '')):
        planted = {'sw/firmware/ctrl/srp/srp_mbx.c': srp.replace(old, new)}
        refused = any('the term srp has no source' in f for f in findings(root, base, fit, planted))
        if srp.count(old) != 1 or not refused:
            escaped.append(name)
    # a timer slot counted once an ordinary pass rather than at its expiry rate: ACMP's slot brings each sink's
    # TMR_NO_RESP once ACMP_TMR_NO_RESP_MS, so doubling the sinks adds at least that many more expiries
    one = load(root, '8x8/2if', base)['timers']
    s = POINTS['8x8/2if']
    s['sinks_per_if'] *= 2
    try:
        two = load(root, '8x8/2if', base)['timers']
    finally:
        s['sinks_per_if'] //= 2
    acmp = s['n_if'] * s['sinks_per_if'] * base['8x8/2if']['event.ACMP'] / macros(root, 2)['ACMP_TMR_NO_RESP_MS']
    if not two - one >= acmp / 1000 - 1e-9:
        escaped.append('a timer slot counted per pass')
    # AECP's owed frame charged by what each source sends (#665): a probe costs its own
    # frame, so a dearer probe raises the term by every registration's retries of it and a dearer notice by the records'
    # share alone; one charge for every source (a notice's fan-out to 32 recipients, #665)
    # moves both together
    raised = {p: dict(v) for p, v in base.items()}
    raised['8x8/2if']['item.aecp.probe'] += 1000
    probes = POINTS['8x8/2if']['n_if'] * POINTS['8x8/2if']['registrations'] / probe_retry_ms(root)
    up = load(root, '8x8/2if', raised)['item.aecp'] - load(root, '8x8/2if', base)['item.aecp']
    noticed = {p: dict(v) for p, v in base.items()}
    noticed['8x8/2if']['item.aecp.notice'] += 1000
    more = load(root, '8x8/2if', noticed)['item.aecp'] - load(root, '8x8/2if', base)['item.aecp']
    if abs(up - probes) > 1e-9 or abs(more - 1 / contract(root)['refill']['aecp']) > 1e-9:
        escaped.append('one owed-frame charge for every AECP source')
    # a term the load counts with no source in its term list (#665: no term without its source)
    if 'item.unsourced' not in unsourced({**load(root, '8x8/2if', base), 'item.unsourced': 0.0}):
        escaped.append('a term without a source')
    # the graded column, tsn-c-stack#32's (#665): a cost the donor does not move stated
    # below the pin's (an SRP record, whose work runs no ACMP walk) must be refused; a cost its walk runs may be lower
    lowered = {p: dict(v) for p, v in base.items()}
    lowered['8x8/2if']['record.srp'] = stated(root, '8x8/2if', STATED_US)['record.srp'] - 5
    walked = {p: dict(v) for p, v in base.items()}
    walked['8x8/2if']['record.acmp'] = 5
    if not any('8x8/2if: the graded column states record.srp' in f for f in findings(root, lowered, fit)) or \
            below_pin(root, walked) or GRADED is not STATED_US_DONOR:
        escaped.append('the graded column below the pin where tsn-c-stack#32 moves nothing')
    return escaped + srp_unit_controls(root, base, fit) + own_controls(root, base, fit) + binding_controls(root)


def own_controls(root: Path, base: dict, fit: dict) -> list[str]:
    """8x8/1if's own ADP record left out (its nearest point's 125 us then supplies it in the tsn-c-stack#32 column) and
    stated under its measurement, each refused by name by --check itself (findings); the head's refused by none."""
    from unittest import mock
    escaped = []
    if own_findings(root):
        return ["8x8/1if's own ADP record not stated", "8x8/1if's own ADP record not its measurement's by the rule"]
    # the measurement's statement by the rule, read from OWN_MEASURED, so a measurement restated moves the control too
    measured = rule_us(OWN_MEASURED['8x8/1if']['record.adp'][0])
    with mock.patch.dict(OWN, {'8x8/1if': {}}):
        if not any(f"8x8/1if: record.adp is 125 us with tsn-c-stack#32, under its measurement's {measured} us" in f
                   for f in findings(root, base, fit)):
            escaped.append("8x8/1if's own ADP record not stated")
    with mock.patch.dict(OWN, {'8x8/1if': {'record.adp': 125}}):
        if not any(f"8x8/1if: its own record.adp is stated 125 us, not its measurement's {measured} us" in f
                   for f in findings(root, base, fit)):
            escaped.append("8x8/1if's own ADP record not its measurement's by the rule")
    return escaped


def srp_unit_controls(root: Path, base: dict, fit: dict) -> list[str]:
    """The SRP drain's limit (ctrl_loop.h) below the load gate's record.srp, planted in each point's own block of THE
    SHAPES, refused by name by --check itself (findings); the head's own limits refused by none."""
    header = (root / SRP_UNIT_HEADER).read_text()
    one = unit_planted(header, shape_costs.of_point('1x1/1if', root), 250)
    two = unit_planted(header, shape_costs.of_point('8x8/2if', root), 300)
    # 8x8/1if at its own measured record, 345 us, under the 365 us its NEAREST point's records state
    eight = unit_planted(header, shape_costs.of_point('8x8/1if', root), 345)
    if srp_unit(root) or not all(any(f'{point}: ctrl_loop.h states CTRL_LOOP_SRP_UNIT_US' in f
                                     for f in findings(root, base, fit, {SRP_UNIT_HEADER: planted}))
                                 for point, planted in (('1x1/1if', one), ('8x8/2if', two), ('8x8/1if', eight))):
        return ["the SRP drain's record cost not the load gate's"]
    return []


def binding_controls(root: Path) -> list[str]:
    """Each column's name bound to its own table, refused by --check itself (findings): the head's own binding holds,
    and the tables swapped, a column dropped and an equal copy that is not the donor's table are each refused; the
    control's name if any escapes."""
    escaped = []
    me = sys.modules[__name__]
    pin, donor = (BOUND[0][0], STATED_US), (BOUND[1][0], STATED_US_DONOR)
    refused = []
    for planted in (((pin[0], donor[1]), (donor[0], pin[1])), (pin,), (pin, (donor[0], dict(donor[1])))):
        saved, me.COLUMNS = me.COLUMNS, planted
        try:
            refused.append(any("a column's name bound to the other's table" in f for f in findings(root)))
        finally:
            me.COLUMNS = saved
    if unbound() or not all(refused):
        escaped.append("a column's name bound to the other's table")
    return escaped


#: Each arrival bound's period the load reads from the tree, and the terms it sets: halving the period must raise
#: those terms, so a term that does not read its source is refused (each arrival bound's plant).
PERIODS = {'refill.aecp': ('rec.aecp', 'item.aecp'), 'refill.acmp': ('rec.acmp', 'item.acmp'),
           'refill.adp': ('rec.adp', 'item.acmp', 'timers'), 'refill.maap': ('rec.maap',),
           'refill.srp': ('srp', 'item.reclaim'), 'tick_ms': ('ticks', 'item.walk', 'steps', 'srp'),
           'holdoff_ms': ('timers', 'notices'), 'SRP_JOIN_CS': ('builds', 'item.mrpdu', 'item.reclaim', 'item.walk'),
           'CTRL_LOOP_STEP_AGE': ('steps',), 'ACMP_TMR_NO_RESP_MS': ('item.acmp', 'timers'),
           'MAAP_PROBE_BASE_MS': ('timers',), 'ADP_ADVERTISE_MS': ('timers',), 'probe': ('item.aecp', 'timers')}


def halved(name: str) -> tuple:
    """The module's readers with one period halved, as (macros, contract, probe_retry_ms)."""
    m0, c0, p0 = macros, contract, probe_retry_ms

    def m(root: Path, n_if: int) -> dict[str, int]:
        """macros, the period halved if it is one of the headers'."""
        out = m0(root, n_if)
        if name in out:
            out[name] = max(0, out[name] // 2) if name == 'CTRL_LOOP_STEP_AGE' else out[name] / 2
        return out

    def c(root: Path) -> dict:
        """contract, the period halved if it is one of the contract's."""
        out = c0(root)
        if name.startswith('refill.'):
            out['refill'] = dict(out['refill'], **{name[7:]: out['refill'][name[7:]] / 2})
        elif name in out:
            out[name] = out[name] / 2
        return out
    return m, c, (lambda root: p0(root) / 2) if name == 'probe' else p0


def period_controls(root: Path) -> list[str]:
    """Each arrival bound whose halved period leaves its terms' load unchanged: a term not read from its source."""
    escaped = []
    point = '8x8/2if'
    before = load(root, point)
    for name, terms in PERIODS.items():
        g = globals()
        saved = g['macros'], g['contract'], g['probe_retry_ms']
        g['macros'], g['contract'], g['probe_retry_ms'] = halved(name)
        try:
            after = load(root, point)
        finally:
            g['macros'], g['contract'], g['probe_retry_ms'] = saved
        if not sum(after[k] for k in terms) > sum(before[k] for k in terms):
            escaped.append(f'the period {name} not read')
    return escaped


#: The planted defects controls() plants, in its order.
CONTROLS = ('a cost over the ceiling', 'a held point not held', 'a rise at the pin alone', 'a stated cost missing',
            'the retained retry counted once a record',
            'a retry with nothing changed', 'a retry every pass', 'one owed-frame charge for every AECP source',
            'a timer slot counted per pass', 'a term without a source',
            'the graded column below the pin where tsn-c-stack#32 moves nothing',
            "the SRP drain's record cost not the load gate's", "8x8/1if's own ADP record not stated",
            "8x8/1if's own ADP record not its measurement's by the rule", "a column's name bound to the other's table")


def ceiling_checks() -> list[tuple[str, bool, str]]:
    """The harness self-test's checks of this gate, of the flip check and of a pass's record classes: every planted
    defect refused."""
    import flip_grade
    import record_classes
    import arty_grade
    escaped = controls(ROOT) + period_controls(ROOT)
    names = (*CONTROLS, *(f'the period {name} not read' for name in PERIODS))
    return [(f'the load gate refuses {name}', name not in escaped, 'escaped' if name in escaped else 'refused')
            for name in names] + flip_grade.flip_checks() + record_classes.checks() + arty_grade.checks()


def main() -> int:
    """Print the load table and refuse a point over its ceiling, or plant each control and refuse an escape."""
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    rc = 0
    if args.selftest:
        escaped = controls(ROOT) + period_controls(ROOT)
        for name in escaped:
            print(f'ESCAPED {name}')
        total = len(CONTROLS) + len(PERIODS)
        print(f'load gate: {total - len(escaped)} of {total} planted controls refused')
        rc |= bool(escaped)
    if args.check or not args.selftest:
        print('\n'.join(report(ROOT) + held(ROOT)))
        found = findings(ROOT)
        for line in found:
            print('OVER', line)
        print('RESULT: FAIL' if found else 'RESULT: PASS')
        rc |= bool(found)
    return rc


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.exit(main())
