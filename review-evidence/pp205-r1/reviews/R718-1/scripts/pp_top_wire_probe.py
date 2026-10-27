#!/usr/bin/env python3
"""Insert a reviewer wire probe into a SCRATCH copy of tb/pp_top/sim_main.cpp.

The probe runs at the end of AcmpPathPhase::run() on its own model (h2) and
feeds, through the full processor top, one talker command of each type for an
out-of-range talker_unique_id (15) with listener fields
0xF1E2D3C4B5A69788 / 0x8C17, plus one GET_TX_STATE for valid source 0 with
the same listener fields. Each unknown-id response is compared byte-exact on
the wire (Milan v1.2 Tables 5.40, 5.44, 5.46 and 5.48); the success response
is graded on status and its listener fields only (Table 5.47).

TALKER_UNKNOWN_ID is status 2 and NOT_SUPPORTED 31 (IEEE 1722.1-2021 Table 8-3).

Usage: pp_top_wire_probe.py PATH/TO/SCRATCH/sim_main.cpp
"""
import sys
from pathlib import Path

ANCHOR = ('    as_rebind_before_tx_sends_the_old_leave();\n'
          '    printf("  AC: %u ms of simulated time on its own model\\n", h2.now_ms());\n')

PROBE = r'''
    // ---- reviewer wire probe (scratch only) ----
    {
      const uint64_t LD = 0xF1E2D3C4B5A69788ULL;
      const uint16_t LU = 0x8C17;
      struct Row { uint8_t msg; uint8_t st; uint16_t flags_in; const char* name; };
      const Row rows[] = {
        {0, 2, 0x0000, "PROBE_TX unknown"},
        {2, 2, 0xFFFF, "DISCONNECT_TX unknown"},
        {4, 2, 0xFFFF, "GET_TX_STATE unknown"},
        {12, 31, 0xFFFF, "GET_TX_CONNECTION unknown"},
      };
      uint16_t seq = 0x7A00;
      for (const Row& r : rows) {
        h2.q_acmp.clear();
        h2.feed(acmp_frame(CTLR_MAC, r.msg, 0, 0, CTLR_EID, EID, LD, 15, LU,
                           0, 0, seq, r.flags_in, 0));
        auto got = h2.wait_any(h2.q_acmp, 400);
        auto want = acmp_frame(OWN_MAC, uint8_t(r.msg | 1), r.st, 0, CTLR_EID,
                               EID, LD, 15, LU, 0, 0, seq, 0, 0);
        CHECK(!got.empty() && got == want, "RWP %s byte-exact", r.name);
        printf("RWP %s: %s\n", r.name,
               got.empty() ? "no response" : (got == want ? "byte-exact" : "MISMATCH"));
        if (!got.empty() && got != want) { dump("got", got); dump("exp", want); }
        ++seq;
      }
      h2.q_acmp.clear();
      h2.feed(acmp_frame(CTLR_MAC, 4, 0, 0, CTLR_EID, EID, LD, 0, LU,
                         0, 0, seq, 0, 0));
      auto ok = h2.wait_any(h2.q_acmp, 400);
      const bool shape = ok.size() >= 66;
      const unsigned st = shape ? unsigned(ok[16] >> 3) : 99u;
      const uint64_t leid = shape ? fv_u64(ok, 42, 8) : 1;
      const uint64_t luid = shape ? fv_u64(ok, 52, 2) : 1;
      CHECK(shape && (ok[15] & 0x0F) == 5 && st == 0 && leid == 0 && luid == 0,
            "RWP GET_TX_STATE source 0 SUCCESS with listener fields 0");
      printf("RWP GET_TX_STATE source 0: status %u leid %016llx luid %04llx\n", st,
             static_cast<unsigned long long>(leid), static_cast<unsigned long long>(luid));
      if (shape) dump("ok", ok);
    }
'''


def main() -> int:
    path = Path(sys.argv[1])
    text = path.read_text()
    if text.count(ANCHOR) != 1:
        print("anchor count", text.count(ANCHOR))
        return 2
    path.write_text(text.replace(ANCHOR, ANCHOR.splitlines(True)[0] + PROBE
                                 + ANCHOR.splitlines(True)[1]))
    print("probe inserted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
