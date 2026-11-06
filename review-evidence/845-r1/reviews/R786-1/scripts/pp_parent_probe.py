#!/usr/bin/env python3
"""Disposable probe: rewrite pp_shadow's [U] group in a COPY of the tree.

The pp_shadow harness elaborates the real milan_datapath, so a stimulus on
i_link_up, LINK_CTRL and the MAC RX port reaches the processor's listener
through eff_link_w and KL_pp_shadow, the path the parent owns. This replaces
the body of grade_a_registered_talker_as_a_bound_sink_reads_it() with the cases
of the pin page's table and stops the run once they are graded.

Usage: python3 -I pp_parent_probe.py <copy>/tb/verilator/pp_shadow/sim_main.cpp [--no-adp]
--no-adp leaves the talker undiscovered, the form of the probe2_* receipts.
"""
import sys
from pathlib import Path

HEAD = "    void grade_a_registered_talker_as_a_bound_sink_reads_it() {\n"
TAIL = "    //! BIND_RX (CONNECT_RX_COMMAND, msg 6) for STREAM_INPUT 0, then the\n"

BODY = r'''    void grade_a_registered_talker_as_a_bound_sink_reads_it() {
        printf("[PROBE] the pin page's cases through milan_datapath\n");
        const uint32_t link = axi_read(0x71c);
        axi_write(0x71c, link | 4);                  // the guard out of eff_link
        run_idle(300);
        auto flap = [&]() {
            dut->i_link_up = 0; run_idle(200);
            dut->i_link_up = 1; run_idle(300);
        };
        auto decl = [&](uint64_t sid, bool failed) {
            uint8_t mf[64];
            const size_t mn = build_msrp_talker(mf, sid, 1, failed);
            inject_rx(mf, mn, 400);
            run_idle(3000);
        };
        //! MSRP frames carrying a Listener attribute (type 3) for U_SID
        auto listener_frames = [&](size_t from) {
            unsigned n = 0;
            uint8_t sid[8];
            put64be(sid, U_SID);
            for (size_t i = from; i < tx_frames.size(); i++) {
                const std::vector<uint8_t>& b = tx_frames[i].bytes;
                if (b.size() < 40 || b[12] != 0x22 || b[13] != 0xEA) continue;
                for (size_t k = 15; k + 14 < b.size(); k++) {
                    if (b[k] == 3 && b[k + 1] == 8
                        && memcmp(&b[k + 6], sid, 8) == 0) { n++; break; }
                }
            }
            return n;
        };
        const uint64_t X1 = U_SID + 0x100, X2 = U_SID + 0x200;

        flap();
        printf("[PROBE] C2 a value arriving while both registrars are taken\n");
        decl(X1, false);
        decl(X2, false);
        decl(U_SID, false);
        bind_sink_zero_over_acmp();
        grade_talker_arm("C2 not held: nothing applied at the settle", 0);
        decl(U_SID, false);
        grade_talker_arm("C2 the talker's next declaration registers", 1);

        //! probing_status of STREAM_INPUT 0 over GET_STREAM_INFO, printed
        uint16_t qseq = 0x0B00;
        auto pbsta = [&](const char* tag) {
            const std::vector<uint8_t> b = gsi_input0(qseq++);
            const unsigned v = b.size() >= 94 ? (b[90] >> 5) : 0xFFu;
            const unsigned fl = b.size() >= 94 ? (b[42] & G_STREAM_FLAGS) : 0xFFu;
            printf("  [i]    %s: probing_status %u, the three stream flags 0x%02X\n", tag, v, fl);
            return v;
        };
        //! the first probe at the talker after `from`, answered as the talker
        //! does; the milliseconds waited, or -1 when none left in `limit_ms`
        auto resettle = [&](size_t from, int limit_ms) {
            for (int ms = 0; ms < limit_ms; ms += 10) {
                for (size_t i = tx_frames.size(); i-- > from; ) {
                    const std::vector<uint8_t>& b = tx_frames[i].bytes;
                    if (tx_frames[i].end_cycle == 0) continue;
                    if (classify(tx_frames[i]) != FR_ACMP || b.size() < 70) continue;
                    if ((b[15] & 0xF) != 0 || get_be(b, 34, 8) != U_TALKER_EID) continue;
                    const uint16_t pseq = static_cast<uint16_t>(get_be(b, 62, 2));
                    uint8_t f[70];
                    memset(f, 0, sizeof f);
                    put64be(f, 0x91E0F0010000ull << 16);
                    const uint8_t tsrc[6] = {0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
                    memcpy(f + 6, tsrc, 6);
                    f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFC; f[15] = 0x01;
                    f[17] = 44;
                    put64be(f + 18, U_SID);
                    put64be(f + 26, 0xC0FFEE00DEADBEEFull);
                    put64be(f + 34, U_TALKER_EID);
                    put64be(f + 42, TEST_EID);
                    memcpy(f + 54, U_DMAC, 6);
                    put16be(f + 62, pseq);
                    put16be(f + 66, U_VID);
                    inject_rx(f, 70, 400);
                    run_idle(20000);
                    return ms;
                }
                run_idle(10 * PP_MS_CYCLES);
            }
            return -1;
        };

        //! the talker's ENTITY_AVAILABLE, so the sink's discovery holds it
        auto adp_talker = [&]() {
            uint8_t f[82];
            memset(f, 0, sizeof f);
            const uint8_t da[6] = {0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
            const uint8_t sa[6] = {0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
            memcpy(f, da, 6); memcpy(f + 6, sa, 6);
            f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFA; f[15] = 0x00;
            f[16] = static_cast<uint8_t>(31u << 3);  // valid_time 62 s
            f[17] = 56;
            put64be(f + 18, U_TALKER_EID);
            inject_rx(f, sizeof f, 400);
            run_idle(1000);
        };
        printf("[PROBE] C4 a link change, a settled input\n");
        adp_talker();
        pbsta("C4 before the link change");
        size_t mark = tx_frames.size();
        dut->i_link_up = 0; run_idle(200);
        grade_talker_arm("C4 i_link_up low ends the registration", 0);
        pbsta("C4 link down");
        dut->i_link_up = 1; run_idle(300);
        grade_talker_arm("C4 i_link_up high finds nothing registered", 0);
        pbsta("C4 link up");
        decl(U_SID, false);
        pbsta("C4 the talker declared again, no probe answered");
        printf("  [i]    C4 ACMPL_STATE after that declaration: 0x%08X\n", axi_read(A_ACMPL_STATE));
        {
            const int ms = resettle(mark, 8000);
            printf("  [i]    C4 first probe after the link change at +%d ms (answered)\n", ms);
            ck_true("C4 the input re-probes the talker after a link change", ms >= 0,
                    "CONNECT_TX_COMMAND seen");
        }
        pbsta("C4 the probe answered");
        grade_talker_arm("C4 the declaration held meanwhile applies at the re-settle", 1);

        printf("[PROBE] C5 the parent's other eff_link term: LINK_CTRL[0] alone\n");
        mark = tx_frames.size();
        axi_write(0x71c, (link | 4) & ~1u);
        run_idle(200);
        grade_talker_arm("C5 LINK_CTRL[0] low alone ends the registration", 0);
        pbsta("C5 LINK_CTRL[0] low");
        axi_write(0x71c, link | 4);
        run_idle(300);
        decl(U_SID, false);
        {
            const int ms = resettle(mark, 8000);
            printf("  [i]    C5 first probe at +%d ms (answered)\n", ms);
        }
        grade_talker_arm("C5 the declaration held meanwhile applies at the re-settle", 1);

        printf("[PROBE] C3 a re-bind, both port registrars holding other values\n");
        mark = tx_frames.size();
        flap();
        {
            const int ms = resettle(mark, 8000);
            printf("  [i]    C3 first probe at +%d ms (answered)\n", ms);
        }
        decl(X1, false);
        decl(X2, false);
        decl(U_SID, false);
        grade_talker_arm("C3 settled: the sink's own registrar registers", 1);
        ck("C3 UNBIND_RX SUCCESS", gsi_acmp_rx(0x08, 0x0A01), 0u);
        grade_talker_arm("C3 unbound: reports nothing", 0);
        bind_sink_zero_over_acmp();
        grade_talker_arm("C3 re-bind keeps the registration", 1);

        printf("[PROBE] C1 Advertise registered before the settle\n");
        ck("C1 UNBIND_RX SUCCESS", gsi_acmp_rx(0x08, 0x0A02), 0u);
        flap();
        decl(U_SID, false);
        size_t at = tx_frames.size();
        bind_sink_zero_over_acmp();
        grade_talker_arm("C1 Advertise applied at the settle", 1);
        printf("  [i]    C1 Listener frames for the stream since the bind: %u\n",
               listener_frames(at));
        ck_true("C1 a Listener declaration left within the bind's window",
                listener_frames(at) > 0, "Listener attribute on the wire");

        printf("[PROBE] C1f Failed registered before the settle\n");
        ck("C1f UNBIND_RX SUCCESS", gsi_acmp_rx(0x08, 0x0A03), 0u);
        flap();
        decl(U_SID, true);
        at = tx_frames.size();
        bind_sink_zero_over_acmp();
        grade_talker_arm("C1f Failed applied at the settle", 2);
        printf("  [i]    C1f Listener frames for the stream since the bind: %u\n",
               listener_frames(at));
        ck_true("C1f a Listener declaration left within the bind's window",
                listener_frames(at) > 0, "Listener attribute on the wire");

        printf("[PROBE] END\n");
        fflush(nullptr);
        _Exit(0);
    }

'''


def main() -> int:
    path = Path(sys.argv[1])
    text = path.read_text()
    start = text.index(HEAD)
    end = text.index(TAIL, start)
    body = BODY
    if "--no-adp" in sys.argv:
        body = body.replace("        adp_talker();\n", "")
    path.write_text(text[:start] + body + text[end:])
    print(f"probe planted in {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
