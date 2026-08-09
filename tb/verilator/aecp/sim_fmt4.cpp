/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Per-stream format-table harness on the SHIPPED arty_4x4 listener input
 * count: KL_aecp_top compiled against the 4-AAF-input shape svh
 * (gen_fmt4_shape.py - inputs = [AAF, AAF, AAF, AAF, CRF], one AAF output;
 * per-stream `AEM_PER_STREAM_FMT layout).
 *
 * The point of THIS harness (vs sim_fmt2's 2-AAF shape and sim_nxn's 8x8
 * GET_STREAM_INFO run) is the MIDDLE sinks: it round-trips SET then
 * GET_STREAM_FORMAT on descriptor_index 2 AND 3, the band no other harness
 * touches. On the legacy 2-input else path (gen_fmt4_shape.py --else-arm,
 * which strips `AEM_PER_STREAM_FMT) inputs 2..4 answer NO_SUCH_DESCRIPTOR -
 * that is exactly the "only inputs 0 and 1 work" defect this proves closed.
 *
 * IEEE Std 1722.1-2021 7.4.9/7.4.10: SET/GET_STREAM_FORMAT act per
 * STREAM_INPUT/STREAM_OUTPUT descriptor. 7.4.9.2 rejects only unsupported
 * formats (BAD_ARGUMENTS); the CRF media-clock sink supports exactly its
 * fixed CRF format, so a SET to that value succeeds and any other fails.
 * Exit 0 = all pass.
 */

#include "VKL_aecp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>

// AAF sink count of this harness's entity shape (the CRF sink past them
// answers the Milan-mandatory 0xF3F from the crf_cnt_* ports)
#define N_AAF_SINKS_TB 4

static VKL_aecp_top* dut;
static long checks = 0, fails = 0;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-46s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-46s = %ld\n", what, got); }
}

static const uint8_t ENT_MAC[6] = {0x02,0x00,0x00,0xff,0xfe,0x01};
static const uint8_t CTL_MAC[6] = {0x68,0x05,0xca,0x95,0xb2,0xd1};
static const uint64_t ENTITY_ID = 0x0200'00ff'fe00'0001ULL;
static const uint64_t CTLR_ID   = 0x6805'ca95'b2d1'0000ULL;

static void put_be64(std::vector<uint8_t>& v, uint64_t x) {
    for (int i = 7; i >= 0; i--) v.push_back((x >> (8*i)) & 0xFF);
}
static void put_be16(std::vector<uint8_t>& v, uint16_t x) {
    v.push_back(x >> 8); v.push_back(x & 0xFF);
}

// AECP AEM command frame (wire order), padded to 60 B (same recipe as
// sim_main.cpp / sim_fmt2.cpp).
static std::vector<uint8_t> aem_cmd(uint16_t cmd, uint16_t seq,
                                    const std::vector<uint8_t>& payload) {
    std::vector<uint8_t> f;
    for (int i=0;i<6;i++) f.push_back(ENT_MAC[i]);
    for (int i=0;i<6;i++) f.push_back(CTL_MAC[i]);
    put_be16(f, 0x22F0);
    f.push_back(0xFB);                          // subtype AECP
    f.push_back(0x00);                          // AEM_COMMAND
    uint16_t cdl = 12 + (uint16_t)payload.size();
    f.push_back((cdl >> 8) & 0x7);
    f.push_back(cdl & 0xFF);
    put_be64(f, ENTITY_ID);
    put_be64(f, CTLR_ID);
    put_be16(f, seq);
    f.push_back((cmd >> 8) & 0x7F);
    f.push_back(cmd & 0xFF);
    for (auto b : payload) f.push_back(b);
    while (f.size() < 60) f.push_back(0x00);
    return f;
}

static void feed_rx(const std::vector<uint8_t>& f) {
    int n = f.size();
    for (int off = 0; off < n; off += 8) {
        uint64_t d = 0; uint8_t keep = 0;
        for (int l = 0; l < 8; l++)
            if (off + l < n) { d |= (uint64_t)f[off+l] << (8*l); keep |= (1<<l); }
        dut->rx_tvalid_i = 1;
        dut->rx_tdata_i  = d;
        dut->rx_tkeep_i  = keep;
        dut->rx_tlast_i  = (off + 8 >= n);
        tick();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
}

static std::vector<uint8_t> collect_resp(int budget = 6000) {
    std::vector<uint8_t> b;
    int idle = 0;
    dut->m_axis_tready = 1;
    for (int c = 0; c < budget; c++) {
        dut->eval();
        if (dut->m_axis_tvalid && dut->m_axis_tready) {
            for (int l = 0; l < 8; l++)
                if ((dut->m_axis_tkeep >> l) & 1)
                    b.push_back((dut->m_axis_tdata >> (8*l)) & 0xFF);
            bool last = dut->m_axis_tlast;
            tick();
            if (last) return b;
            idle = 0;
        } else {
            tick();
            if (++idle > 500) return b;
        }
    }
    return b;
}

static int r_status(const std::vector<uint8_t>& b){ return b.size()>16 ? (b[16]>>3)&0x1F : -1; }
static uint64_t r_fmt(const std::vector<uint8_t>& b) {
    if (b.size() < 50) return 0;
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) v = (v << 8) | b[42+i];  // payload fmt @ wire 42
    return v;
}

// SET/GET_STREAM_FORMAT payload: type(2) index(2) [format(8)]
static std::vector<uint8_t> sf_pl(uint16_t type, uint16_t idx) {
    std::vector<uint8_t> pl; put_be16(pl, type); put_be16(pl, idx); return pl;
}
static std::vector<uint8_t> sf_pl(uint16_t type, uint16_t idx, uint64_t fmt) {
    auto pl = sf_pl(type, idx); put_be64(pl, fmt); return pl;
}

static uint16_t seq = 0x4000;
static std::vector<uint8_t> xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
    feed_rx(aem_cmd(cmd, seq++, pl));
    return collect_resp();
}

static const uint16_t CMD_SET_FMT = 8, CMD_GET_FMT = 9;
static const uint16_t IN = 0x0005, OUT = 0x0006;
static const uint64_t AAF2  = 0x0205022000806000ULL;  // 48k INT32 2ch (default)
static const uint64_t AAF8  = 0x0205022002006000ULL;  // concrete 8ch variant
static const uint64_t CRF48 = 0x041060010000BB80ULL;  // CRF 48k

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_aecp_top;

    dut->rst_n = 0; dut->enable_i = 1;
    dut->srp_domain_vid_i = 0x002;
    dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    // the tapped lane's consumer is idle-ready; the gh #65 leg parks it
    dut->rx_tready_i = 1;
    dut->entity_id_i = ENTITY_ID; dut->entity_model_id_i = 0;
    dut->entity_caps_i = 0x00008588; dut->talker_sources_i = 1;
    dut->talker_caps_i = 0x4801; dut->listener_sinks_i = 5;
    dut->listener_caps_i = 0x4801; dut->controller_caps_i = 0;
    dut->available_index_i = 7; dut->association_id_i = 0;
    dut->gptp_gm_id_i = 0; dut->gptp_domain_i = 0; dut->pdelay_ns_i = 0;
    dut->link_up_i = 1;
    for (int w = 0; w < 10; w++) dut->rxdiag_cnt_i[w] = 0;
    for (int w = 0; w < 5; w++)  dut->tkdiag_cnt_i[w] = 0;
    dut->n_aaf_sinks_i = N_AAF_SINKS_TB;
    // gh #58 stream-command law truth vectors: wake unbound / not streaming
    dut->lstn_bound_v_i = 0; dut->out_streaming_v_i = 0;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|ENT_MAC[i]; dut->station_mac_i = m; }
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) tick();

    printf("== AECP per-stream format tables - 4-AAF-input (arty_4x4) shape ==\n");

    printf("\n[1] GET_STREAM_FORMAT every declared input (ROM defaults)\n");
    for (uint16_t i = 0; i < 4; i++) {
        auto r = xact(CMD_GET_FMT, sf_pl(IN, i));
        char nm[64];
        snprintf(nm, sizeof nm, "in%u GET SUCCESS (AAF sink)", i);
        ck(nm, r_status(r), 0);
        snprintf(nm, sizeof nm, "in%u fmt = AAF 2ch default", i);
        ck(nm, r_fmt(r) == AAF2, 1);
    }
    auto r = xact(CMD_GET_FMT, sf_pl(IN, 4));
    ck("in4 (CRF) GET SUCCESS", r_status(r), 0);
    ck("in4 fmt = CRF 48k", r_fmt(r) == CRF48, 1);
    r = xact(CMD_GET_FMT, sf_pl(IN, 5));
    ck("in5 GET NO_SUCH_DESCRIPTOR", r_status(r), 2);

    printf("\n[2] SET_STREAM_FORMAT in2 (MIDDLE sink): round-trip + WB isolation\n");
    r = xact(CMD_SET_FMT, sf_pl(IN, 2, AAF8));
    ck("in2 SET 8ch concrete SUCCESS", r_status(r), 0);
    ck("in2 SET echoes new fmt", r_fmt(r) == AAF8, 1);
    r = xact(CMD_GET_FMT, sf_pl(IN, 2));
    ck("in2 GET readback = 8ch (WB landed at idx 2)", r_fmt(r) == AAF8, 1);
    r = xact(CMD_GET_FMT, sf_pl(IN, 0));
    ck("in0 GET still 2ch (WB isolation below)", r_fmt(r) == AAF2, 1);
    r = xact(CMD_GET_FMT, sf_pl(IN, 1));
    ck("in1 GET still 2ch (WB isolation below)", r_fmt(r) == AAF2, 1);
    r = xact(CMD_GET_FMT, sf_pl(IN, 3));
    ck("in3 GET still 2ch (WB isolation above)", r_fmt(r) == AAF2, 1);
    r = xact(CMD_GET_FMT, sf_pl(IN, 4));
    ck("in4 GET still CRF (WB isolation, CRF)", r_fmt(r) == CRF48, 1);
    r = xact(CMD_SET_FMT, sf_pl(IN, 2, CRF48));
    ck("in2 SET CRF fmt BAD_ARGUMENTS", r_status(r), 7);
    r = xact(CMD_SET_FMT, sf_pl(IN, 2, AAF2 | (9ULL << 22)));
    ck("in2 SET 11ch (2|9) BAD_ARGUMENTS", r_status(r), 7);
    r = xact(CMD_SET_FMT, sf_pl(IN, 2, AAF2));
    ck("in2 SET restore 2ch SUCCESS", r_status(r), 0);
    r = xact(CMD_GET_FMT, sf_pl(IN, 2));
    ck("in2 GET = 2ch again", r_fmt(r) == AAF2, 1);

    printf("\n[3] SET_STREAM_FORMAT in3 (OTHER middle sink): round-trip\n");
    r = xact(CMD_SET_FMT, sf_pl(IN, 3, AAF8));
    ck("in3 SET 8ch concrete SUCCESS", r_status(r), 0);
    r = xact(CMD_GET_FMT, sf_pl(IN, 3));
    ck("in3 GET readback = 8ch (WB landed at idx 3)", r_fmt(r) == AAF8, 1);
    r = xact(CMD_GET_FMT, sf_pl(IN, 2));
    ck("in2 GET still 2ch (WB isolation from idx 3)", r_fmt(r) == AAF2, 1);
    r = xact(CMD_SET_FMT, sf_pl(IN, 3, AAF2));
    ck("in3 SET restore 2ch SUCCESS", r_status(r), 0);
    r = xact(CMD_GET_FMT, sf_pl(IN, 3));
    ck("in3 GET = 2ch again", r_fmt(r) == AAF2, 1);

    printf("\n[4] SET_STREAM_FORMAT in4 (CRF sink): exact-match rule (7.4.9.2)\n");
    r = xact(CMD_SET_FMT, sf_pl(IN, 4, CRF48));
    ck("in4 SET CRF 48k SUCCESS (supported fmt)", r_status(r), 0);
    r = xact(CMD_SET_FMT, sf_pl(IN, 4, AAF2));
    ck("in4 SET AAF BAD_ARGUMENTS (unsupported fmt)", r_status(r), 7);
    r = xact(CMD_SET_FMT, sf_pl(IN, 5, AAF2));
    ck("in5 SET NO_SUCH_DESCRIPTOR", r_status(r), 2);

    printf("\n[5] STREAM_OUTPUT: per-descriptor talker truth\n");
    r = xact(CMD_GET_FMT, sf_pl(OUT, 0));
    ck("out0 GET SUCCESS", r_status(r), 0);
    ck("out0 fmt = wire-true 2ch", r_fmt(r) == AAF2, 1);
    r = xact(CMD_SET_FMT, sf_pl(OUT, 0, AAF2));
    ck("out0 SET wire-true 2ch SUCCESS", r_status(r), 0);
    r = xact(CMD_SET_FMT, sf_pl(OUT, 0, AAF8));
    ck("out0 SET 8ch BAD_ARGUMENTS (wire is 2ch)", r_status(r), 7);
    r = xact(CMD_GET_FMT, sf_pl(OUT, 1));
    ck("out1 GET NO_SUCH_DESCRIPTOR", r_status(r), 2);

    printf("\n[6] gh #58 D1: MIDDLE sink + CRF + output legs of the bound gate\n");
    dut->lstn_bound_v_i = 0x0004;             // ONLY sink 2 bound
    r = xact(CMD_SET_FMT, sf_pl(IN, 2, AAF8));
    ck("in2 (middle) bound -> 12", r_status(r), 12);
    r = xact(CMD_SET_FMT, sf_pl(IN, 2, AAF2));
    ck("in2 bound + same value -> 12 (value-independent)", r_status(r), 12);
    r = xact(CMD_SET_FMT, sf_pl(IN, 1, AAF8));
    ck("in1 SET unaffected (index below)", r_status(r), 0);
    r = xact(CMD_SET_FMT, sf_pl(IN, 3, AAF8));
    ck("in3 SET unaffected (index above)", r_status(r), 0);
    r = xact(CMD_SET_FMT, sf_pl(IN, 1, AAF2));
    ck("in1 restore 2ch", r_status(r), 0);
    r = xact(CMD_SET_FMT, sf_pl(IN, 3, AAF2));
    ck("in3 restore 2ch", r_status(r), 0);
    // CRF leg: sink 4's OWN bit; the exact-match SET refuses while bound
    dut->lstn_bound_v_i = 0x0010;
    r = xact(CMD_SET_FMT, sf_pl(IN, 4, CRF48));
    ck("in4 (CRF) bound -> 12 even for the exact format", r_status(r), 12);
    dut->lstn_bound_v_i = 0;
    r = xact(CMD_SET_FMT, sf_pl(IN, 4, CRF48));
    ck("in4 unbound -> exact-match SET SUCCESS", r_status(r), 0);
    // output leg: 5.3.7.3 streaming gates SET(out0), SIR outranks BAD_ARGS
    dut->out_streaming_v_i = 0x0001;
    r = xact(CMD_SET_FMT, sf_pl(OUT, 0, AAF2));
    ck("out0 STREAMING + wire-true value -> 12", r_status(r), 12);
    r = xact(CMD_SET_FMT, sf_pl(OUT, 0, AAF8));
    ck("out0 STREAMING + bad value -> STILL 12 (SIR > BAD_ARGS)",
       r_status(r), 12);
    dut->out_streaming_v_i = 0;
    r = xact(CMD_SET_FMT, sf_pl(OUT, 0, AAF2));
    ck("out0 idle -> wire-true SET SUCCESS", r_status(r), 0);
    r = xact(CMD_SET_FMT, sf_pl(IN, 2, AAF2));
    ck("in2 unbound restore -> SUCCESS", r_status(r), 0);

    printf("\n----------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
