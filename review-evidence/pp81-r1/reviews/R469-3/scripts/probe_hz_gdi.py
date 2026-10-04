#!/usr/bin/env python3
"""Reviewer probe (R469-3): add reviewer-only HZ arms to a scratch copy of
tb/pp_top/sim_main.cpp. Grades, at the exact head, the parts of the
GET_DYNAMIC_INFO serialization the lane's HZ8/HZ13 arms do not: the talker
side of the class-wide cross-lock, a batch naming another sink, and the
batch's own answer after it waited. Usage: probe_hz_gdi.py <tree>"""
import sys
from pathlib import Path

src = Path(sys.argv[1]) / "tb/pp_top/sim_main.cpp"
text = src.read_text()
anchor = "  void run() {\n    boot();\n    hz1_every_transaction_presents_its_class_and_key();"
assert text.count(anchor) == 1, "anchor drift"
probe = r'''
  //! R469-3 reviewer probes, never part of the product bench
  void rp_gdi_probes() {
    std::vector<uint8_t> gdi(8, 0);
    putbe(&gdi[0], 4, 2);
    putbe(&gdi[6], 0x000F, 2);
    const auto si2 = ti(DT_SI, 2);
    std::vector<uint8_t> g2 = gdi;
    g2.insert(g2.end(), si2.begin(), si2.end());
    auto a = beside_or_after(8, 1, 0x004B, g2, false,
                             "RP1 GDI with a GET_STREAM_INFO record of "
                             "STREAM_INPUT 2 vs a held UNBIND_RX of sink 1");
    CHECK(status(a) == AECP_SUCCESS && a.size() > 40,
          "RP1b the waited batch answers SUCCESS (status %d, %zu bytes)",
          status(a), a.size());
    std::vector<uint8_t> g1 = gdi;
    const auto si1 = ti(DT_SI, 1);
    g1.insert(g1.end(), si1.begin(), si1.end());
    a = beside_or_after(8, 1, 0x004B, g1, false,
                        "RP2 GDI naming STREAM_INPUT 1 vs a held UNBIND_RX of "
                        "sink 1");
    CHECK(status(a) == AECP_SUCCESS && a.size() > 40,
          "RP2b the waited batch answers SUCCESS (status %d, %zu bytes)",
          status(a), a.size());
    std::vector<uint8_t> go = gdi;
    const auto so1 = ti(DT_SO, 1);
    go.insert(go.end(), so1.begin(), so1.end());
    a = acmp_beside_or_after(0x004B, go, 2, 1, false,
                             "RP3 a DISCONNECT_TX of source 1 vs a held GDI "
                             "naming STREAM_OUTPUT 1");
    CHECK(status(a) == AECP_SUCCESS, "RP3b the held batch answers SUCCESS "
          "(status %d)", status(a));
    a = acmp_beside_or_after(0x004B, go, 2, 2, false,
                             "RP4 a DISCONNECT_TX of source 2 vs a held GDI "
                             "naming STREAM_OUTPUT 1 (over-serialization)");
    a = acmp_beside_or_after(0x004B, go, 4, 1, true,
                             "RP5 a GET_TX_STATE of source 1 vs a held GDI "
                             "naming STREAM_OUTPUT 1 (two reads)");
    a = beside_or_after(10, 2, 0x004B, g1, true,
                        "RP6 GDI naming STREAM_INPUT 1 vs a held GET_RX_STATE "
                        "of sink 2");
    CHECK(status(a) == AECP_SUCCESS, "RP6b the batch answers SUCCESS "
          "(status %d)", status(a));
  }

'''
text = text.replace(anchor, probe + anchor)
end = "    hz13_a_batch_naming_a_sink_waits_for_its_listener_step();\n  }"
assert text.count(end) == 1, "run() end drift"
text = text.replace(end, "    hz13_a_batch_naming_a_sink_waits_for_its_listener_step();\n    rp_gdi_probes();\n  }")
src.write_text(text)
print("planted")
