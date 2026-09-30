#!/usr/bin/env python3
"""Reviewer probe: add observation-only sections to a SCRATCH copy of tb/pp_top/sim_main.cpp.

P-A (DeadlinePhase): an ADDRESS_ACCESS and an AVC command, idle and queued behind a
stalled GET_COUNTERS past their deadline: which status the answer carries.
P-B (HazardPhase): NAME_WR, CLOCK_CFG, IDENTIFY and REGISTRY_OP commands whose key
names a stream, presented while an ACMP read of that stream is held.
Usage: probe_patch.py <path to scratch sim_main.cpp>
"""
import sys
from pathlib import Path

path = Path(sys.argv[1])
src = path.read_text()

DL_PROBE = r'''
  //! R418 probe P-A (observation only)
  void r418_probe_non_aem_forced_status() {
    std::vector<uint8_t> tlv(10, 0);
    putbe(&tlv[0], 0x0004, 2);                 // mode READ, length 4, address 0
    for (const uint8_t mt : {uint8_t(2), uint8_t(4)}) {
      const char* nm = mt == 2 ? "ADDRESS_ACCESS" : "AVC";
      io.q_aecp.clear();
      io.dl_clear();
      io.feed(aecp_frame(OWN_MAC, CTLR_MAC, mt, 0, EID, CTLR_EID, 0xA100 + mt,
                         0x0001, tlv));
      long first = -1;
      const auto f0 = answer(0xA100 + mt, &first);
      printf("  [R418-PA] %s idle: %zu bytes, message_type %d, status %d\n", nm,
             f0.size(), f0.size() > 15 ? (f0[15] & 0x0F) : -1, status(f0));
      io.dl_clear();
      io.ctr_hold = 1000;
      (void)send(AEM_GET_COUNTERS, ti(0x0005, 0), 0xA200 + mt);
      io.feed(aecp_frame(OWN_MAC, CTLR_MAC, mt, 0, EID, CTLR_EID, 0xA300 + mt,
                         0x0001, tlv));
      const long tq = static_cast<long>(io.t) - 4;
      const auto fa = answer(0xA200 + mt, &first);
      long qfirst = -1;
      const auto fb = answer(0xA300 + mt, &qfirst);
      io.ctr_hold = 2;
      const bool echoed = fb.size() >= 38 + tlv.size()
          && std::equal(tlv.begin(), tlv.end(), fb.begin() + 38);
      printf("  [R418-PA] %s queued behind the stall: stall status %d; its own "
             "answer %zu bytes, message_type %d, status %d, command echoed %d, "
             "first byte %ld clocks after reception, redirects %d\n", nm,
             status(fa), fb.size(), fb.size() > 15 ? (fb[15] & 0x0F) : -1,
             status(fb), echoed ? 1 : 0, qfirst - tq, io.dl_pre_rises);
    }
  }
'''

HZ_PROBE = r'''
  //! R418 probe P-B: the classes the PR says admit no conflict with ACMP
  void r418_probe_four_classes() {
    std::vector<uint8_t> nsi = ti(DT_SI, 1, 72);
    putbe(&nsi[6], CFGIX, 2);
    auto r = beside_or_after(10, 1, 0x0010, nsi, false,
                             "R418-PB NAME_WR SET_NAME STREAM_INPUT 1 vs held GET_RX_STATE sink 1");
    printf("  [R418-PB] SET_NAME STREAM_INPUT 1: answered status %d, %zu bytes\n",
           status(r), r.size());
    std::vector<uint8_t> nso = ti(DT_SO, 1, 72);
    putbe(&nso[6], CFGIX, 2);
    r = beside_or_after(4, 1, 0x0010, nso, false,
                        "R418-PB NAME_WR SET_NAME STREAM_OUTPUT 1 vs held GET_TX_STATE source 1");
    printf("  [R418-PB] SET_NAME STREAM_OUTPUT 1: answered status %d\n", status(r));
    std::vector<uint8_t> rate = ti(DT_SI, 1, 8);
    putbe(&rate[4], 96000u, 4);
    r = beside_or_after(10, 1, 0x0014, rate, false,
                        "R418-PB CLOCK_CFG SET_SAMPLING_RATE at STREAM_INPUT 1 vs held GET_RX_STATE sink 1");
    printf("  [R418-PB] SET_SAMPLING_RATE(STREAM_INPUT 1): answered status %d\n",
           status(r));
    r = beside_or_after(10, 1, 0x0018, ti(DT_SI, 1, 5), false,
                        "R418-PB IDENTIFY SET_CONTROL at STREAM_INPUT 1 vs held GET_RX_STATE sink 1");
    printf("  [R418-PB] SET_CONTROL(STREAM_INPUT 1): answered status %d\n",
           status(r));
    r = beside_or_after(10, 1, 0x0024, std::vector<uint8_t>(4, 0), true,
                        "R418-PB REGISTRY_OP REGISTER beside held GET_RX_STATE sink 1");
    printf("  [R418-PB] REGISTER beside the held read: answered status %d\n",
           status(r));
  }
'''

def once(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new)

src = once(src, "  void dl7_nothing_leaked() {", DL_PROBE + "\n  void dl7_nothing_leaked() {")
src = once(src, "    dl7_nothing_leaked();\n", "    dl7_nothing_leaked();\n    r418_probe_non_aem_forced_status();\n")
src = once(src, "    hz8_the_other_classes_run_beside_a_stream_step();\n",
           "    hz8_the_other_classes_run_beside_a_stream_step();\n    r418_probe_four_classes();\n")
src = once(src, "  void hz8_the_other_classes_run_beside_a_stream_step() {",
           HZ_PROBE + "\n  void hz8_the_other_classes_run_beside_a_stream_step() {")
path.write_text(src)
print("patched", path)
