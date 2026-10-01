#!/usr/bin/env python3
"""Reviewer probes: add observation-only sections to a SCRATCH copy of tb/pp_top/sim_main.cpp.

P-A (DeadlinePhase, the round-1 probe verbatim): an ADDRESS_ACCESS and an AVC command,
    idle and queued behind a stalled GET_COUNTERS past their deadline: which status the
    answer carries. Called after DL11, so no lane check runs after it.
P-B (HazardPhase, the round-1 probe verbatim): NAME_WR, CLOCK_CFG, IDENTIFY and
    REGISTRY_OP commands whose key names a stream, presented while an ACMP read of that
    stream is held; its STREAM_OUTPUT sub-probe is the one round 1 found inconclusive.
P-C (HazardPhase, new): how many clocks each talker command (and a listener control)
    keeps its scoreboard key, idle and with the TX pool filled.
P-D (HazardPhase, new): a GET_TX_STATE of source 1 followed on the serial ingress by a
    SET_NAME on STREAM_OUTPUT 1 at several gaps: can the SET_NAME meet the talker's
    hold at admission? A GET_RX_STATE of sink 1 followed by a SET_NAME on STREAM_INPUT 1
    is the listener control.
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
  //! R418 probe P-B: the classes the PR said admit no conflict with ACMP
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

  //! R418 probe P-C: clocks each ACMP command keeps its key (observation only)
  void r418_probe_talker_hold() {
    struct T { uint8_t msg; const char* nm; };
    const T ts[] = {{4, "GET_TX_STATE"}, {2, "DISCONNECT_TX"},
                    {12, "GET_TX_CONNECTION"}, {0, "PROBE_TX"},
                    {10, "GET_RX_STATE (listener control)"},
                    {8, "UNBIND_RX (listener control)"}};
    for (const bool stalled : {false, true}) {
      for (const T& x : ts) {
        io.hz_clear();
        if (stalled) fill_tx_pool();
        io.hz_clear();
        const long t0 = send_acmp(x.msg, 1, seq++);
        long adm = -1, end = -1;
        for (int c = 0; c < 20000; ++c) {
          if (adm < 0) {
            const auto* a = last_adm(false);
            if (a != nullptr) adm = a->t;
          }
          if (adm >= 0 && !io.hz_acmp_ends.empty()) {
            end = io.hz_acmp_ends.front();
            break;
          }
          io.step();
        }
        printf("  [R418-PC] %s, %s: frame first byte at 0, admitted at %ld, "
               "hold ended at %ld, key held %ld clocks\n",
               stalled ? "TX pool filled" : "idle", x.nm,
               adm >= 0 ? adm - t0 : -1, end >= 0 ? end - t0 : -1,
               (adm >= 0 && end >= 0) ? end - adm : -1);
        if (stalled) release_mac(); else io.idle(4000);
        io.q_acmp.clear();
        io.q_aecp.clear();
      }
    }
  }

  //! R418 probe P-D: a SET_NAME racing an ACMP read of its stream on the
  //! serial ingress (observation only)
  void r418_probe_talker_race() {
    for (const bool talker : {true, false}) {
      for (const int gap : {0, 16, 64}) {
        io.hz_clear();
        const long ta = send_acmp(talker ? 4 : 10, 1, seq++);
        io.idle(gap);
        const uint16_t s = seq++;
        const long tb = send_aecp(0, AEM_SET_NAME,
                                  name_pl(talker ? DT_SO : DT_SI, 1, "R418 race"), s);
        io.idle(3000);
        const H::Adm* a = nullptr;
        const H::Adm* b = nullptr;
        for (const auto& m : io.hz_adms) {
          if (!m.aecp && a == nullptr) a = &m;
          if (m.aecp && b == nullptr) b = &m;
        }
        long first = -1;
        const auto r = aecp_answer(s, 40, &first);
        printf("  [R418-PD] %s then SET_NAME %s 1, gap %d: ACMP admitted at %ld, "
               "its hold ended at %ld; SET_NAME first byte at %ld, admitted at "
               "%ld, refused %ld clocks, answered status %d\n",
               talker ? "GET_TX_STATE source 1" : "GET_RX_STATE sink 1",
               talker ? "STREAM_OUTPUT" : "STREAM_INPUT", gap,
               a ? a->t - ta : -1, acmp_end() >= 0 ? acmp_end() - ta : -1,
               tb - ta, b ? b->t - ta : -1, io.hz_aecp_refused, status(r));
        io.idle(2000);
        io.q_acmp.clear();
        io.q_aecp.clear();
      }
    }
  }
'''


def once(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new)


src = once(src, "  void dl7_nothing_leaked() {", DL_PROBE + "\n  void dl7_nothing_leaked() {")
src = once(src, "    dl11_every_release_named_a_live_hold();\n",
           "    dl11_every_release_named_a_live_hold();\n    r418_probe_non_aem_forced_status();\n")
src = once(src, "  void hz8_the_other_classes_run_beside_a_stream_step() {",
           HZ_PROBE + "\n  void hz8_the_other_classes_run_beside_a_stream_step() {")
src = once(src, "    hz12_a_stream_named_by_another_class_conflicts_with_its_read();\n",
           "    hz12_a_stream_named_by_another_class_conflicts_with_its_read();\n"
           "    r418_probe_four_classes();\n    r418_probe_talker_hold();\n"
           "    r418_probe_talker_race();\n")
path.write_text(src)
print("patched", path)
