#!/usr/bin/env python3
"""R294 round-2 probe Q (disposable): patch tb/pp_top/gsi_internal.hpp in an
EXTRACTED tree so that, after the GI phase's own checks, it runs:
  Q1  re-bind variants from a SETTLED sink (same talker STREAMING_WAIT on /
      repeat / off, another talker with and without a flip, unbind): count the
      unsolicited GET_STREAM_INFO responses per step and print their values
      beside a solicited read.
  Q2  two sinks settled on the SAME stream: fresh Talker Failed, a changed
      FailureInformation, a bridge-only change; unsolicited count per sink,
      values, and Listener New count on the wire.
  Q3  latency-only Talker Advertise refresh: unsolicited count (stated
      residual; compare with the base tree).
  Q4  descriptor index N_STREAM_IN_P (8) of the ten-input image while sink 0
      is settled: internal fields must read zero (sink 0 as control).
Usage: probe_q.py <tree> [--base-hybrid]
--base-hybrid: the tree carries base RTL under the head bench; the harness
must then answer selectors 5/7 instead of stalling them.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
hybrid = "--base-hybrid" in sys.argv[2:]
f = tree / "tb/pp_top/gsi_internal.hpp"
src = f.read_text()

probe = r'''
  // ---- R294-2 probe Q (disposable) ----
  static int q_pb(const std::vector<uint8_t>& f) { return f.size() == 94 ? f[90] >> 5 : -1; }
  static int q_ac(const std::vector<uint8_t>& f) { return f.size() == 94 ? f[90] & 31 : -1; }
  static int q_sw(const std::vector<uint8_t>& f) { return f.size() == 94 ? (f[45] >> 3) & 1 : -1; }
  static int q_code(const std::vector<uint8_t>& f) { return f.size() == 94 ? f[72] : -1; }
  static unsigned long long q_br(const std::vector<uint8_t>& f) {
    return f.size() == 94 ? (unsigned long long)fv_u64(f, 74, 8) : 0ull;
  }
  void q_show(const char* tag, unsigned sink,
              const std::vector<std::vector<uint8_t>>& u) {
    printf("R294-Q %s sink%u unsolicited=%zu", tag, sink, u.size());
    for (const auto& x : u)
      printf(" [pb=%d ac=%d sw=%d code=%d bridge=%016llx]", q_pb(x), q_ac(x),
             q_sw(x), q_code(x), q_br(x));
    const auto s = query(sink);
    printf(" | solicited pb=%d ac=%d sw=%d code=%d bridge=%016llx started=%d\n",
           q_pb(s), q_ac(s), q_sw(s), q_code(s), q_br(s),
           int((io.d->aecp_strm_started_o >> sink) & 1));
    fflush(stdout);
  }
  void q_settle(unsigned sink, const std::vector<uint8_t>& p, uint64_t tk,
                uint64_t s_id, uint64_t d_a) {
    if (p.size() != 70) { printf("R294-Q settle sink%u: no probe\n", sink); return; }
    io.feed(acmp_frame(T1_MAC + (tk - T1_EID), 1, 0, s_id, CTLR_EID, tk, EID,
                       T1_UID, sink, d_a, 0, fv_u64(p, 62, 2), 0, 2));
  }
  void r294_q() {
    io.run_ms(50);
    io.q_aecp.clear();
    // ---- Q1: re-bind variants from SETTLED ----
    binding(0, true);
    discover(0);
    q_settle(0, probe(0), talker(0), sid(0), da(0));
    io.run_ms(50);
    q_show("Q1-pre-settled", 0, input_uns(0, 100));
    binding(0, true, talker(0), 0x0008);
    q_show("Q1a-same-talker-SW-on", 0, input_uns(0, 150));
    binding(0, true, talker(0), 0x0008);
    q_show("Q1b-same-talker-SW-repeat", 0, input_uns(0, 150));
    binding(0, true, talker(0), 0x0000);
    q_show("Q1c-same-talker-SW-off", 0, input_uns(0, 150));
    binding(0, true, talker(0) + 0x77, 0x0008);
    q_show("Q1d-other-talker-from-settled-SW-on", 0, input_uns(0, 150));
    binding(0, true, talker(0) + 0x78, 0x0008);
    q_show("Q1e-other-talker-SW-kept", 0, input_uns(0, 150));
    binding(0, true, talker(0) + 0x79, 0x0000);
    q_show("Q1f-other-talker-SW-off", 0, input_uns(0, 150));
    binding(0, false);
    q_show("Q1g-unbind", 0, input_uns(0, 150));
    io.run_ms(50);
    io.q_aecp.clear();

    // ---- Q2: two sinks on the SAME stream ----
    binding(0, true);
    binding(1, true, talker(0));
    const auto p0 = probe(0);
    const auto p1 = probe(1);
    q_settle(0, p0, talker(0), sid(0), da(0));
    q_settle(1, p1, talker(0), sid(0), da(0));
    io.run_ms(50);
    q_show("Q2-pre-settled", 0, input_uns(0, 100));
    q_show("Q2-pre-settled", 1, input_uns(1, 0));
    io.q_msrp.clear();
    attribute(0, 7, BRIDGE0, true);
    q_show("Q2a-fresh-failed", 0, input_uns(0, 100));
    q_show("Q2a-fresh-failed", 1, input_uns(1, 0));
    printf("R294-Q Q2a listener New for shared sid over 1000 ms = %d\n",
           listener_news(0, 1000));
    io.q_aecp.clear();
    attribute(0, 9, BRIDGE1, true);
    q_show("Q2b-changed-code+bridge", 0, input_uns(0, 100));
    q_show("Q2b-changed-code+bridge", 1, input_uns(1, 0));
    printf("R294-Q Q2b listener New for shared sid over 600 ms = %d\n",
           listener_news(0, 600));
    io.q_aecp.clear();
    attribute(0, 9, BRIDGE1 ^ 1ull, true);
    q_show("Q2c-bridge-only", 0, input_uns(0, 100));
    q_show("Q2c-bridge-only", 1, input_uns(1, 0));
    printf("R294-Q Q2c listener New for shared sid over 600 ms = %d\n",
           listener_news(0, 600));
    io.q_aecp.clear();
    attribute(0, 9, BRIDGE1 ^ 1ull, true);
    q_show("Q2d-unchanged", 0, input_uns(0, 100));
    q_show("Q2d-unchanged", 1, input_uns(1, 0));
    io.q_aecp.clear();

    // ---- Q3: latency-only Advertise refresh (stated residual) ----
    attribute(0, 0, 0, false);
    q_show("Q3-pre-advertise", 0, input_uns(0, 100));
    q_show("Q3-pre-advertise", 1, input_uns(1, 0));
    {
      auto fv = fv_talker(sid(0), da(0), 2, 256, 1, 3, 1, 0x00054321);
      io.feed(mrpdu_frame(true, T1_MAC, {Msg{1, 25, false,
                              {Vec{false, 1, fv, {EV_JOININ}, {}}}}}));
    }
    q_show("Q3-latency-only-refresh", 0, input_uns(0, 200));
    q_show("Q3-latency-only-refresh", 1, input_uns(1, 0));

    // ---- Q4: index N_STREAM_IN_P aliases sink 0 in the 3-bit index ----
    {
      const auto f8 = query(8);
      const auto f0 = query(0);
      printf("R294-Q Q4 index8 size=%zu status=%d pb=%d ac=%d code=%d "
             "bridge=%016llx | sink0 pb=%d\n", f8.size(),
             f8.size() == 94 ? (f8[16] >> 3) & 31 : -1, q_pb(f8), q_ac(f8),
             q_code(f8), q_br(f8), q_pb(f0));
    }
    printf("R294-Q done\n");
  }
'''
anchor = "  void run() {"
assert src.count(anchor) == 1
src = src.replace(anchor, probe + anchor)
call_anchor = "    CHECK(io.gsi_internal_leaks == 0,\n"
assert src.count(call_anchor) == 1
src = src.replace(call_anchor, "    r294_q();\n" + call_anchor)
if hybrid:
    a = "    io.gsi_retired_stuck = true;\n"
    assert src.count(a) == 1
    src = src.replace(a, "    io.gsi_retired_stuck = false;\n")
f.write_text(src)
print("patched", f, "hybrid" if hybrid else "head")
