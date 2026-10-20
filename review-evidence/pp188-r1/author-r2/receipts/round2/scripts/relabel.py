#!/usr/bin/env python3
"""Round-2 comment-label edits (R666-1 RESIDUE table): usage relabel.py <repo>."""
import sys
from pathlib import Path
repo = Path(sys.argv[1])
EDITS = [
 ('tb/acmp_listener/sim_main.cpp',
  "  // B4: REF-BUG guard — a TalkerFailed rise in SETTLED_RSV_OK takes no\n"
  "  // invented arc, and (issue #189) is the in-place Advertise<->Failed swap:\n"
  "  // GET_RX_STATE's REGISTERING_FAILED follows it in both directions (Milan\n"
  "  // Table 5.39, 802.1Q 35.2.6), with no state change, frame or strobe\n",
  "  // A TalkerFailed rise in SETTLED_RSV_OK takes no invented arc, and (issue\n"
  "  // #189) is the in-place Advertise<->Failed swap: GET_RX_STATE's\n"
  "  // REGISTERING_FAILED follows it in both directions (Milan Table 5.39,\n"
  "  // 802.1Q 35.2.6), with no state change, frame or strobe\n"),
 ('tb/pp_top/sim_main.cpp',
  "  // ---- AS5b, AS5c: the in-place Advertise <-> Failed swap (issue #189) ----\n",
  "  // ---- the in-place Advertise <-> Failed swap (issue #189) ----------------\n"),
 ('tb/pp_top/sim_main.cpp',
  "  // ---- AS7: a rebind settled before tx! still sends the old Lv (#188) ----\n",
  "  // ---- a rebind settled before tx! still sends the old Lv (#188) ---------\n"),
 ('tb/srp_stream_fsms/sim_main.cpp',
  "// ==== M. an A15 settle never abandons the owed Listener Leave ===========\n",
  "// ==== an A15 settle never abandons the owed Listener Leave ==============\n"),
 ('tb/srp_stream_fsms/sim_main.cpp', "  // RB1, the rebind: ", "  // The rebind: "),
 ('tb/srp_stream_fsms/sim_main.cpp', "  // RB2, the re-probe: ", "  // The re-probe: "),
 ('tb/srp_stream_fsms/sim_main.cpp', "  // RB3: the same re-probe, ", "  // The same re-probe, "),
 ('tb/srp_stream_fsms/sim_main.cpp', "  // RB4, a settle while parked ", "  // A settle while parked "),
 ('tb/srp_stream_fsms/sim_main.cpp', "  // RB5, a rebind back ", "  // A rebind back "),
 ('tb/srp_stream_fsms/sim_main.cpp', "  // RB6, an LO applicant ", "  // An LO applicant "),
 ('tb/srp_stream_fsms/sim_main.cpp', "  // RB7, a txLA! walk ", "  // A txLA! walk "),
 ('tb/srp_stream_fsms/sim_main.cpp', "  // RB8, received Listener ", "  // Received Listener "),
 ('tb/srp_stream_fsms/walk_main.cpp',
  "//   WK11 a settle on another stream of a sink still declaring is its old\n"
  "//       stream_id's Lv! (issue #188): the next walk sends one Leave per such\n"
  "//       sink, naming the stream_id it held, read from the leave copy, and the\n"
  "//       new streams declare only after it.\n",
  "//   and the leave copy (issue #188): a settle on another stream of a sink\n"
  "//       still declaring is its old stream_id's Lv!, so the next walk sends\n"
  "//       one Leave per such sink, naming the stream_id it held, read from\n"
  "//       the leave copy, and the new streams declare only after it; a second\n"
  "//       settle onto a third stream before that walk keeps the one it held.\n"),
 ('tb/srp_stream_fsms/walk_main.cpp',
  "    // WK11: every sink but k was still declaring; sink k left with WK7\n",
  "    // Every sink but k was still declaring; sink k was already torn down.\n"),
 ('tb/srp_stream_fsms/walk_main.cpp',
  "    // after the Leave of the stream it held (WK11)\n",
  "    // after the Leave of the stream it held\n"),
 ('tb/srp_stream_fsms/walk_main.cpp',
  "    // WK12: every sink settled on a second stream and then a third before\n"
  "    // tx!; the Leave of each still names the stream_id it declared\n",
  "    // Every sink settled on a second stream and then a third before tx!:\n"
  "    // the Leave of each still names the stream_id it declared\n"),
]
for rel, old, new in EDITS:
    p = repo / rel
    t = p.read_text()
    assert t.count(old) == 1, (rel, old[:40], t.count(old))
    p.write_text(t.replace(old, new, 1))
    print('edited', rel, old[:40].strip())
