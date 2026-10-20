#!/usr/bin/env python3
"""Undo the round-2 item-3 wording edits (R665-1-F3 and the R666-1 RESIDUE table)
in the working tree, so items 1 and 2 can be committed first: usage split_c3.py <repo>.
Each pair is (final text, text before item 3); every final text must occur once."""
import sys
from pathlib import Path
repo = Path(sys.argv[1])
UNDO = [
 ('hdl/srp/KL_srp_listener_fsm.sv',
  "//                the applicant already holds keeps that applicant (LA or\n"
  "//                LO + New! is VN, so a re-probe that re-registers before\n"
  "//                tx! sends New, and one that does not sends the owed Lv\n"
  "//                or Empty). A settle on another stream_id while the\n"
  "//                applicant is LA or LO arms the matcher at once but\n"
  "//                leaves the applicant on the old value until its next\n"
  "//                tx! sends the owed Lv (or s):\n",
  "//                the applicant already holds keeps that applicant (LA +\n"
  "//                New! is VN, so a re-probe that re-registers before tx!\n"
  "//                sends New, and one that does not sends the Lv). A settle\n"
  "//                on another stream_id while the applicant is LA or LO\n"
  "//                arms the matcher at once but leaves the applicant on the\n"
  "//                old value until its next tx! sends the owed Lv (or s):\n"),
 ('docs/architecture/10_srp_engine.md',
  "keeps the applicant: the next tx! sends what it owes (the Lv from LA, the Empty from LO), unless the talker registers again first, when New! takes LA or LO to VN and the tx! sends New |",
  "keeps the applicant: the next tx! sends the Lv, unless the talker registers again first, when New! takes LA to VN and the tx! sends New |"),
 ('tb/srp_top/mutants.py',
  "    # the leave copy at both elaboration arms\n    ('listener-rebind",
  "    # the leave copy at both elaboration arms (walk_main.cpp WK11)\n    ('listener-rebind"),
 ('tb/acmp_listener/sim_main.cpp',
  "  // A TalkerFailed rise in SETTLED_RSV_OK takes no invented arc, and (issue\n"
  "  // #189) is the in-place Advertise<->Failed swap: GET_RX_STATE's\n"
  "  // REGISTERING_FAILED follows it in both directions (Milan Table 5.39,\n"
  "  // 802.1Q 35.2.6), with no state change, frame or strobe\n",
  "  // B4: REF-BUG guard — a TalkerFailed rise in SETTLED_RSV_OK takes no\n"
  "  // invented arc, and (issue #189) is the in-place Advertise<->Failed swap:\n"
  "  // GET_RX_STATE's REGISTERING_FAILED follows it in both directions (Milan\n"
  "  // Table 5.39, 802.1Q 35.2.6), with no state change, frame or strobe\n"),
 ('tb/pp_top/sim_main.cpp',
  "  // ---- the in-place Advertise <-> Failed swap (issue #189) ----------------\n",
  "  // ---- AS5b, AS5c: the in-place Advertise <-> Failed swap (issue #189) ----\n"),
 ('tb/pp_top/sim_main.cpp',
  "  // ---- a rebind settled before tx! still sends the old Lv (#188) ---------\n",
  "  // ---- AS7: a rebind settled before tx! still sends the old Lv (#188) ----\n"),
 ('tb/srp_stream_fsms/sim_main.cpp',
  "// ==== an A15 settle never abandons the owed Listener Leave ==============\n",
  "// ==== M. an A15 settle never abandons the owed Listener Leave ===========\n"),
 ('tb/srp_stream_fsms/sim_main.cpp', "  // The rebind: ", "  // RB1, the rebind: "),
 ('tb/srp_stream_fsms/sim_main.cpp', "  // The re-probe: ", "  // RB2, the re-probe: "),
 ('tb/srp_stream_fsms/sim_main.cpp', "  // The same re-probe, ", "  // RB3: the same re-probe, "),
 ('tb/srp_stream_fsms/walk_main.cpp',
  "//   and the leave copy (issue #188): a settle on another stream of a sink\n"
  "//       still declaring is its old stream_id's Lv!, so the next walk sends\n"
  "//       one Leave per such sink, naming the stream_id it held, read from\n"
  "//       the leave copy, and the new streams declare only after it; a second\n"
  "//       settle onto a third stream before that walk keeps the one it held.\n",
  "//   WK11 a settle on another stream of a sink still declaring is its old\n"
  "//       stream_id's Lv! (issue #188): the next walk sends one Leave per such\n"
  "//       sink, naming the stream_id it held, read from the leave copy, and the\n"
  "//       new streams declare only after it; a second settle onto a third\n"
  "//       stream before that walk keeps the one it held.\n"),
 ('tb/srp_stream_fsms/walk_main.cpp',
  "    // Every sink but k was still declaring; sink k was already torn down.\n",
  "    // WK11: every sink but k was still declaring; sink k left with WK7\n"),
 ('tb/srp_stream_fsms/walk_main.cpp',
  "    // after the Leave of the stream it held\n    h.advertise(next);",
  "    // after the Leave of the stream it held (WK11)\n    h.advertise(next);"),
]
for rel, final, before in UNDO:
    p = repo / rel
    t = p.read_text()
    assert t.count(final) == 1, (rel, final[:50], t.count(final))
    p.write_text(t.replace(final, before, 1))
    print('undone', rel, final[:44].strip())
