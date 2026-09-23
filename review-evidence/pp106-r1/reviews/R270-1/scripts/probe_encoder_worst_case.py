#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe (not a fix): add worst-case LeaveAll drains to a DISPOSABLE
copy of tb/srp_encoder/sim_main.cpp.

Usage: probe_encoder_worst_case.py <tree>   (edits <tree>/tb/srp_encoder only)

W1: 12 lone Talker Failed entries (non-successor values) with LeaveAll: the
    largest single-message drain plus three LeaveAll-only messages
    (expected 528 B, against the RTL's WORST_BYTES_C bound of 558 B and the
    576 B standard slot).
W2: 12 entries alternating Talker Failed / Talker Advertise with LeaveAll
    (12 message shells plus two LeaveAll-only messages).
W3: 7 Talker Failed and 5 Talker Advertise in 11 messages with LeaveAll.
Each frame is compared byte-exact with the suite's independent packer and
read by its independent parser; the probe prints each frame length.
"""
import sys
from pathlib import Path

f = Path(sys.argv[1]) / "tb/srp_encoder/sim_main.cpp"
s = f.read_text()

decl = "  void take_one_leaveall_per_drain();\n"
assert s.count(decl) == 1
s = s.replace(decl, decl + "  void probe_worst_case_leaveall_frames();\n")

call = "\n  take_one_leaveall_per_drain();\n"
assert s.count(call) == 1
s = s.replace(call, call + "  probe_worst_case_leaveall_frames();\n")

anchor = "void SrpSuite::domain_declares_adopts_and_ignores_repeats() {"
assert s.count(anchor) == 1
probe = r'''
void SrpSuite::probe_worst_case_leaveall_frames() {
  auto tf = [](int k) {                  // lone Talker Failed, no successor
    Ev e = typed_ev(2);
    e.val[7] = uint8_t(0x10 + 2 * k);
    return e;
  };
  auto ta = [](int k) {                  // lone Talker Advertise
    Ev e = typed_ev(1);
    e.val[7] = uint8_t(0x40 + 2 * k);
    return e;
  };
  const char* names[3] = {"W1 12 x TF", "W2 TF/TA alternating",
                          "W3 7 TF + 5 TA in 11 messages"};
  for (int w = 0; w < 3; ++w) {
    std::vector<Ev> evs;
    if (w == 0) {
      for (int k = 0; k < 12; ++k) evs.push_back(tf(k));
    } else if (w == 1) {
      for (int k = 0; k < 12; ++k) evs.push_back((k & 1) ? ta(k) : tf(k));
    } else {
      evs.push_back(tf(0)); evs.push_back(tf(1));
      for (int k = 0; k < 5; ++k) { evs.push_back(ta(k)); evs.push_back(tf(k + 2)); }
    }
    d->enc_leaveall_i = 1; h.tick(); d->enc_leaveall_i = 0;
    for (auto& e : evs) CHECK(h.push_enc(e), "%s push accepted", names[w]);
    CHECK(h.capture_pdu(0, got), "%s PDU captured", names[w]);
    check_pdu(names[w], got, model_pdu(evs, true, OWN_MAC));
    std::vector<PVec> vs;
    CHECK(parse_pdu(got, vs), "%s parses", names[w]);
    printf("PROBE %s: %zu entries, frame %zu B (standard slot 576 B)\n",
           names[w], evs.size(), got.size());
  }
}

'''
s = s.replace(anchor, probe + anchor)
f.write_text(s)
print("probe inserted into", f)
