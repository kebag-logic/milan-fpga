#!/usr/bin/env python3
"""Insert a disposable [PROBE] into a COPY of tb/verilator/milan_dp/sim_nxn.cpp.

usage: sinfo_notify_probe.py <copy-of-sim_nxn.cpp>

The probe runs inside the [NOTIFY] section after controllers A and B have
registered (Milan v1.2 5.4.5). From controller A it sets output 0's
presentation offset (SET_STREAM_INFO, MSRP_ACC_LAT_VALID) and counts the
unsolicited SET_STREAM_INFO frames controller B receives:
  1. 2,000,000 ns (baseline);
  2. 2,010,000 ns: a real change;
  3. 2,010,000 ns again: no state modified, so 5.4.5.2 expects no push;
  4. 2,020,834 ns, the value GET_STREAM_INFO reads back after step 2: the
     stored offset changes (2,010,000 -> 2,020,834) and the applied one
     changes (97 -> 98 periods), so one push is expected.
It restores 2,000,000 ns and the talker enables afterwards. Exactly one
anchor each must match. The copy is never committed.
"""
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text()
call_anchor = "        prove_a_no_op_set_pushes_nothing();\n"
def_anchor = "    // ---- (N3) the no-op gate: storing the value held pushes nothing ----\n"
for a in (call_anchor, def_anchor):
    if text.count(a) != 1:
        sys.exit(f"anchor found {text.count(a)} times: {a!r}")
probe = r'''    // ---- disposable reviewer probe: the SET_STREAM_INFO push gate ----
    void probe_sinfo_rounding_push_gate() {
        const uint32_t aaf = axi_read(A_AAF_CTRL), crf = axi_read(0x750);
        axi_write(A_AAF_CTRL, 0x00020000); axi_write(0x750, 0);
        drain_tx(20000);
        const unsigned target = 0;
        auto sinfo = [&](uint32_t lat) {
            const std::vector<uint8_t> r = aecp_xact_from(CTL_A, 0x000E, notify_sq++,
                                                          si_pl(0x0006, target, 0x20000000u, lat));
            return r.size() >= 38 ? aecp_status(r) : -1L;
        };
        auto gsi = [&]() {
            return lat_of(aecp_xact_from(CTL_A, 0x000F, notify_sq++, desc_key(0x0006, target)));
        };
        long st[4]; long n[4]; unsigned long g[4];
        const uint32_t lat[4] = {2000000u, 2010000u, 2010000u, 2020834u};
        for (int i = 0; i < 4; i++) {
            notify_clear();
            st[i] = sinfo(lat[i]);
            drain_tx(NOTIFY_WIN);
            n[i] = notify_count(0x000E, &CTL_B);
            g[i] = gsi();
            printf("  [PROBE] step %d: SET_STREAM_INFO(%u ns) from A status %ld; unsolicited "
                   "SET_STREAM_INFO to B: %ld; GET_STREAM_INFO then reads %lu ns\n",
                   i + 1, lat[i], st[i], n[i], g[i]);
        }
        ck("[PROBE] a real change 2,000,000 -> 2,010,000 pushes once", n[1], 1);
        ck("[PROBE] GET_STREAM_INFO reads the applied 2,020,834", static_cast<long>(g[1]), 2020834L);
        ck("[PROBE] the same 2,010,000 again modifies nothing and pushes nothing (5.4.5.2)", n[2], 0);
        ck("[PROBE] 2,020,834 changes the stored and applied offset and pushes once", n[3], 1);
        ck("[PROBE] ...and the applied offset moved to 98 periods", static_cast<long>(g[3]), 2041667L);
        sinfo(2000000u); drain_tx(NOTIFY_WIN); notify_clear();
        axi_write(A_AAF_CTRL, aaf); axi_write(0x750, crf);
        drain_tx(20000); notify_clear();
    }

'''
text = text.replace(call_anchor, call_anchor + "        probe_sinfo_rounding_push_gate();\n")
text = text.replace(def_anchor, probe + def_anchor)
path.write_text(text)
print("probe inserted")
