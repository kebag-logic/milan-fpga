#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe (not a fix): pin the once-per-MRPDU LeaveAll gate at the two
boundaries the donor suites leave open, in a DISPOSABLE copy of
tb/srp_decoder/sim_main.cpp.

Usage: probe_decoder_gate_boundaries.py <tree>   (edits <tree>/tb/srp_decoder only)

Z1: one Listener message, an unflagged vector then a flagged one: the lane
    fires at the flagged VectorHeader, in DLSDU order (docs 10 §6.5 "follows
    DLSDU order"): timeline E3 L3 E3.
Z2: the same type split across two messages around a flagged Domain message:
    [L JoinIn][D LA JoinMt x2][L LA n=0] -> E3 L4 E4 E4 L3.
Z3: an MRPDU flagged on Listener and then truncated mid-FirstValue
    (malformed, lane fired, prefix stands), followed by a well-formed
    Listener-only LeaveAll MRPDU: the lane fires again for the new MRPDU.
Every check prints "PROBE-Z" so the receipt can grep it.
"""
import sys
from pathlib import Path

f = Path(sys.argv[1]) / "tb/srp_decoder/sim_main.cpp"
s = f.read_text()

decl = "  void a_type_leaves_all_once_per_mrpdu();\n"
assert s.count(decl) == 1
s = s.replace(decl, decl + "  void probe_gate_boundaries();\n")

call = "\n  a_type_leaves_all_once_per_mrpdu();\n"
assert s.count(call) == 1
s = s.replace(call, call + "  probe_gate_boundaries();\n")

anchor = "int SrpDecoderSuite::run() {"
assert s.count(anchor) == 1
probe = r'''
void SrpDecoderSuite::probe_gate_boundaries() {
  // Z1: [Listener: vec no-LA JoinIn A, vec LA JoinIn B]
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 3); P8(p, 8); P16(p, 26);
  P16(p, 0x0001); P64(p, SIDB + 0xD00); P8(p, 36); P8(p, 0x80);
  P16(p, 0x2001); P64(p, SIDB + 0xE00); P8(p, 36); P8(p, 0x80);
  P16(p, 0); P16(p, 0);
  h.feed(p, true);
  CHECK(h.la_lane[kListener - 1] == 1, "PROBE-Z1 Listener lane once got %d",
        h.la_lane[kListener - 1]);
  check_marks("PROBE-Z1 DLSDU order", {{'E', kListener}, {'L', kListener},
                                       {'E', kListener}});
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "PROBE-Z1 done ok");

  // Z2: [L no-LA JoinIn][D LA JoinMt x2][L LA n=0]
  h.clear();
  p.clear();
  P8(p, 0);
  P8(p, 3); P8(p, 8); P16(p, 14);
  P16(p, 0x0001); P64(p, SIDB + 0xF00); P8(p, 36); P8(p, 0x80);
  P16(p, 0);
  P8(p, 4); P8(p, 4); P16(p, 9);
  P16(p, 0x2002); P8(p, 5); P8(p, 2); P16(p, 2); P8(p, 126);
  P16(p, 0);
  P8(p, 3); P8(p, 8); P16(p, 12);
  P16(p, 0x2000); P64(p, 0);
  P16(p, 0); P16(p, 0);
  h.feed(p, true);
  check_marks("PROBE-Z2 second Listener message", {{'E', kListener}, {'L', kDomain},
              {'E', kDomain}, {'E', kDomain}, {'L', kListener}});

  // Z3: flagged Listener vector truncated mid-FirstValue, then a good
  // Listener-only LeaveAll MRPDU
  h.clear();
  p.clear();
  P8(p, 0);
  P8(p, 3); P8(p, 8); P16(p, 14);
  P16(p, 0x2001); P8(p, 0x02); P8(p, 0x00); P8(p, 0x00);   // truncated
  h.feed(p, true);
  CHECK(h.la_lane[kListener - 1] == 1 && h.dones.size() == 1 && h.dones[0].mal,
        "PROBE-Z3 malformed MRPDU: lane fired once, PDU malformed");
  h.clear();
  p.clear();
  P8(p, 0);
  P8(p, 3); P8(p, 8); P16(p, 12);
  P16(p, 0x2000); P64(p, 0);
  P16(p, 0); P16(p, 0);
  h.feed(p, true);
  CHECK(h.la_lane[kListener - 1] == 1,
        "PROBE-Z3 the next MRPDU's Listener LeaveAll fires again got %d",
        h.la_lane[kListener - 1]);
}

'''
s = s.replace(anchor, probe + anchor)
f.write_text(s)
print("probe inserted into", f)
