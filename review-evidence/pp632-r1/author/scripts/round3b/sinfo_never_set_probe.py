#!/usr/bin/env python3
"""Insert a disposable never-set-row probe into tb/verilator/milan_dp/sim_nxn.cpp.

usage: sinfo_never_set_probe.py <sim_nxn.cpp>

Round 3b: the call anchor at 28510858 and later (the case on the timed leg
alone). Runs right after the committed (N6) SET_STREAM_INFO case, in the [NOTIFY]
section of the timed leg, where no controller has ever set the CRF output's
row (output N_STREAMS, 1 on the 1x1 shape): the processor's dynamic store
reads it as 0 with its valid bit clear, and the integrator serves its 2 ms
factory value.
  P1. SET 0 ns on that row: the offset in force moves 2,000,000 -> 0, so
      Milan v1.2 5.4.5.2 expects one push to B;
  P2. GET_STREAM_INFO then reads 0;
  P3. SET 2,000,000 ns: a change back, one push.
The anchor must match exactly once. The edit is never committed.
"""
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text()
call = "        if (timed) prove_set_stream_info_pushes_on_the_offset_stored();\n"
defn = "    // ---- (N6) SET_STREAM_INFO pushes on the offset STORED (#632) --------\n"
for a in (call, defn):
    if text.count(a) != 1:
        sys.exit(f"anchor found {text.count(a)} times: {a!r}")
probe = r'''    // ---- disposable probe: SET_STREAM_INFO on a row never set ----
    void probe_sinfo_never_set_row() {
        const uint32_t aaf = axi_read(A_AAF_CTRL), crf = axi_read(0x750);
        axi_write(A_AAF_CTRL, 0x00020000); axi_write(0x750, 0);
        drain_tx(20000);
        const unsigned ix = static_cast<unsigned>(kNstreamsTb);
        notify_clear();
        std::vector<uint8_t> r = aecp_xact_from(CTL_A, 0x000E, notify_sq++,
                                                si_pl(0x0006, ix, 0x20000000u, 0u));
        drain_tx(NOTIFY_WIN);
        const long p1 = notify_count(0x000E, &CTL_B, 0x0006, static_cast<int>(ix));
        const unsigned long g1 = lat_of(aecp_xact_from(CTL_A, 0x000F, notify_sq++,
                                                       desc_key(0x0006, ix)));
        printf("  [PROBE] P1: SET_STREAM_INFO(output %u, 0 ns) on the never-set row: status %ld, "
               "pushes to B %ld; GET then reads %lu ns\n", ix,
               r.size() >= 38 ? aecp_status(r) : -1L, p1, g1);
        ck("[PROBE] P1 SET 0 on the never-set row (2 ms in force) pushes once", p1, 1);
        ck("[PROBE] P2 GET_STREAM_INFO then reads 0", static_cast<long>(g1), 0);
        notify_clear();
        r = aecp_xact_from(CTL_A, 0x000E, notify_sq++,
                           si_pl(0x0006, ix, 0x20000000u, 2000000u));
        drain_tx(NOTIFY_WIN);
        const long p3 = notify_count(0x000E, &CTL_B, 0x0006, static_cast<int>(ix));
        printf("  [PROBE] P3: SET_STREAM_INFO(output %u, 2,000,000 ns): status %ld, pushes to B %ld\n",
               ix, r.size() >= 38 ? aecp_status(r) : -1L, p3);
        ck("[PROBE] P3 SET 2,000,000 back pushes once", p3, 1);
        notify_clear();
        axi_write(A_AAF_CTRL, aaf); axi_write(0x750, crf);
        drain_tx(20000); notify_clear();
    }

'''
text = text.replace(call, call + "        if (timed) probe_sinfo_never_set_row();\n")
text = text.replace(defn, probe + defn)
path.write_text(text)
print("probe inserted")
