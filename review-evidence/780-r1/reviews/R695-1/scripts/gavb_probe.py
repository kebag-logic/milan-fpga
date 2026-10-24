"""Insert a disposable GET_AVB_INFO status probe into a COPY of
tb/verilator/pp_shadow/sim_main.cpp (never the reviewed clone).

Usage: python3 -I gavb_probe.py <copy>/tb/verilator/pp_shadow/sim_main.cpp

The probe sends, through milan_datapath / KL_pp_shadow, a GET_AVB_INFO
(0x0027) to CLOCK_DOMAIN 0, to ENTITY 0, to AVB_INTERFACE 0 (exists) and
to AVB_INTERFACE 0x7777 (absent), each at cdl 16, plus a 2-octet command
(cdl 14), and grades the wrong-type rows against NOT_SUPPORTED (11)
echoed at the command's own length (IEEE 1722.1-2021 Table 7-141; processor
issue #200). It prints every observed status with a PROBE tag.
"""
import sys, pathlib
p = pathlib.Path(sys.argv[1])
s = p.read_text()
anchor = "        grade_unassigned_opcode_echoes();\n"
assert s.count(anchor) == 1, "call-site anchor not unique"
s = s.replace(anchor, anchor + "        probe_gavb_status();\n", 1)
fn_anchor = "    void grade_unassigned_opcode_echoes() {\n"
assert s.count(fn_anchor) == 1, "function anchor not unique"
probe = r'''
    int probe_gavb_one(const char* tag, const uint8_t* pl, size_t n,
                       uint16_t seq) {
        uint8_t cf[128];
        size_t at = tx_frames.size();
        size_t cn = build_aecp(cf, 0, TEST_EID, 0x0027, seq, pl, n);
        inject_rx(cf, cn, 400);
        run_idle(20000);
        int k = last_aecp(at);
        if (k < 0) { printf("PROBE %s: SILENCE\n", tag); return -1; }
        const std::vector<uint8_t>& b = tx_frames[k].bytes;
        unsigned st = (b[16] >> 3) & 0x1F;
        unsigned cdl = ((static_cast<unsigned>(b[16]) & 7) << 8) | b[17];
        printf("PROBE %s: status=%u cdl=%u payload0=%04x\n", tag, st, cdl,
               static_cast<unsigned>(get_be(b, 38, 2)));
        return k;
    }
    void probe_gavb_status() {
        uint8_t cd[4] = {0x00, 0x24, 0x00, 0x00};   // CLOCK_DOMAIN 0
        uint8_t en[4] = {0x00, 0x00, 0x00, 0x00};   // ENTITY 0
        uint8_t ai[4] = {0x00, 0x09, 0x00, 0x00};   // AVB_INTERFACE 0
        uint8_t ax[4] = {0x00, 0x09, 0x77, 0x77};   // AVB_INTERFACE absent
        uint8_t sh[2] = {0x00, 0x24};               // cdl 14
        int k = probe_gavb_one("CLOCK_DOMAIN0", cd, 4, 0x0E01);
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            grade_common(b, "PROBE-CD", 0x0027, 0x0E01, 1);
            grade_len(b, "PROBE-CD", 4);
            ck("PROBE-CD: status NOT_SUPPORTED(11)", (b[16] >> 3) & 0x1F, 11u);
            ck("PROBE-CD: descriptor_type echoed", static_cast<uint32_t>(get_be(b, 38, 2)), 0x0024u);
        }
        k = probe_gavb_one("ENTITY0", en, 4, 0x0E02);
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            grade_len(b, "PROBE-EN", 4);
            ck("PROBE-EN: status NOT_SUPPORTED(11)", (b[16] >> 3) & 0x1F, 11u);
        }
        k = probe_gavb_one("AVB_INTERFACE0", ai, 4, 0x0E03);
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            ck("PROBE-AI: status SUCCESS(0)", (b[16] >> 3) & 0x1F, 0u);
        }
        k = probe_gavb_one("AVB_INTERFACE_ABSENT", ax, 4, 0x0E04);
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            ck("PROBE-AX: status NO_SUCH_DESCRIPTOR(2)", (b[16] >> 3) & 0x1F, 2u);
        }
        k = probe_gavb_one("SHORT_CDL14", sh, 2, 0x0E05);
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            ck("PROBE-SH: status BAD_ARGUMENTS(7)", (b[16] >> 3) & 0x1F, 7u);
        }
    }

'''
s = s.replace(fn_anchor, probe + fn_anchor, 1)
p.write_text(s)
print("probe inserted into", p)
