/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * sim_odmap - DYNAMIC STREAM_PORT_OUTPUT audio maps (USER 08-01: "enable
 * dynamic mapping on stream_output as well").
 *
 * CLAUSES: Milan v1.2 5.4.2.26-28 make GET/ADD/REMOVE_AUDIO_MAPPINGS a
 * SHALL "for each Stream Port Output that has no Audio Map"; 5.3.3.9 lets
 * a config declare exactly that; 5.3.9.1 keeps the output mapping list as
 * standing state bounded by the Stream Output's current format. 1722.1-2021
 * 7.4.45.1/7.4.46.1 make record validity "governed by a set of vendor
 * defined rules" - this engine's rules (port's own stream only, L/R-
 * adjacent record pairs onto one source pair) are asserted here.
 *
 * SHAPE (gen_odmap_shape.py): two 8ch talkers; SPO0 = 8 ring clusters
 * (default policy), SPO1 = 9 clusters (4 loopback from rx stream 1 +
 * 4 ring + 1 mono pilot TONE). Both dynamic, no AUDIO_MAP descriptors.
 * The capture-crossbar mirror (odmap_wr_*) is recorded on every pulse:
 * slot words are KL_chan_map_capture entries {idxh[11:8], en[7], src[6:4],
 * idx[3:0]}.
 *
 * NEGATIVE CONTROL: against the pre-odmap RTL every section below fails -
 * GET served a static-flavored empty map and ADD answered NOT_SUPPORTED.
 */

#include "VKL_aecp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <array>
#include <vector>

static VKL_aecp_top* dut;
static long checks = 0, fails = 0;

//! capture-crossbar mirror recorder: every odmap_wr_p_o pulse (slot, word)
struct OdWr { int slot, word; };
static std::vector<OdWr> g_od_wrs;
static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    if (dut->odmap_wr_p_o)
        g_od_wrs.push_back({(int)dut->odmap_wr_slot_o,
                            (int)dut->odmap_wr_word_o});
}
static std::vector<OdWr> take_wrs() { auto v = g_od_wrs; g_od_wrs.clear(); return v; }
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-56s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-56s = %ld\n", what, got); }
}

static const uint8_t ENT_MAC[6]  = {0x02,0x00,0x00,0xff,0xfe,0x01};
static const uint8_t CTL_MAC[6]  = {0x68,0x05,0xca,0x95,0xb2,0xd1};
static const uint8_t CTL2_MAC[6] = {0x68,0x05,0xca,0x00,0x00,0x22};
static const uint64_t ENTITY_ID = 0x0200'00ff'fe00'0001ULL;
static const uint64_t CTLR_ID   = 0x6805'ca95'b2d1'0000ULL;
static const uint64_t CTLR2_ID  = 0x6805'ca00'0022'0000ULL;

static void put_be64(std::vector<uint8_t>& v, uint64_t x) {
    for (int i = 7; i >= 0; i--) v.push_back((x >> (8*i)) & 0xFF);
}
static void put_be16(std::vector<uint8_t>& v, uint16_t x) {
    v.push_back(x >> 8); v.push_back(x & 0xFF);
}

static std::vector<uint8_t> aem_cmd2(const uint8_t* mac, uint64_t cid,
                                     uint16_t cmd, uint16_t seq,
                                     const std::vector<uint8_t>& payload) {
    std::vector<uint8_t> f;
    for (int i=0;i<6;i++) f.push_back(ENT_MAC[i]);
    for (int i=0;i<6;i++) f.push_back(mac[i]);
    put_be16(f, 0x22F0);
    f.push_back(0xFB);                          // subtype AECP
    f.push_back(0x00);                          // AEM_COMMAND
    uint16_t cdl = 12 + (uint16_t)payload.size();
    f.push_back((cdl >> 8) & 0x7);
    f.push_back(cdl & 0xFF);
    put_be64(f, ENTITY_ID);
    put_be64(f, cid);
    put_be16(f, seq);
    f.push_back((cmd >> 8) & 0x7F);
    f.push_back(cmd & 0xFF);
    for (auto b : payload) f.push_back(b);
    while (f.size() < 60) f.push_back(0x00);
    return f;
}
static std::vector<uint8_t> aem_cmd(uint16_t cmd, uint16_t seq,
                                    const std::vector<uint8_t>& payload) {
    return aem_cmd2(CTL_MAC, CTLR_ID, cmd, seq, payload);
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

static std::vector<uint8_t> collect_resp(int budget = 8000) {
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
static int b_cdl(const std::vector<uint8_t>& b){
    return b.size()>17 ? (((b[16]&0x7)<<8) | b[17]) : -1;
}
static int r_be16(const std::vector<uint8_t>& b, size_t off){
    return b.size() > off+1 ? (b[off]<<8 | b[off+1]) : -1;
}
static int r_u(const std::vector<uint8_t>& b){
    return b.size() > 36 ? (b[36] >> 7) & 1 : -1;
}

static uint16_t seq = 0x7000;
static std::vector<uint8_t> xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
    feed_rx(aem_cmd(cmd, seq++, pl));
    return collect_resp();
}

static const uint16_t CMD_READ = 4, CMD_SET_FMT = 8;
static const uint16_t CMD_REG_UNSOL = 36, CMD_DEREG_UNSOL = 37;
static const uint16_t CMD_GET_MAP = 43, CMD_ADD_MAP = 44, CMD_RM_MAP = 45;
static const uint16_t SPO = 0x000F, STROUT = 0x0006;
static const uint64_t AAF8 = 0x0205022002006000ULL;  // 48k 8ch (reset)
static const uint64_t AAF2 = 0x0205022000806000ULL;  // 48k 2ch (shrink)

static std::vector<uint8_t> gm_pl(uint16_t t, uint16_t i, uint16_t page) {
    std::vector<uint8_t> pl;
    put_be16(pl, t); put_be16(pl, i); put_be16(pl, page); put_be16(pl, 0);
    return pl;
}
static std::vector<uint8_t> am_pl(uint16_t t, uint16_t i,
                                  const std::vector<std::array<uint16_t,4>>& m) {
    std::vector<uint8_t> pl;
    put_be16(pl, t); put_be16(pl, i);
    put_be16(pl, (uint16_t)m.size()); put_be16(pl, 0);
    for (auto& r : m) { for (int k = 0; k < 4; k++) put_be16(pl, r[k]); }
    return pl;
}
static bool row_is(const std::vector<uint8_t>& b, size_t base, int n,
                   uint16_t si, uint16_t sc, uint16_t co, uint16_t cc) {
    size_t o = base + 8*(size_t)n;
    return r_be16(b,o) == si && r_be16(b,o+2) == sc &&
           r_be16(b,o+4) == co && r_be16(b,o+6) == cc;
}
static std::vector<uint8_t> setofmt(uint16_t idx, uint64_t fmt) {
    std::vector<uint8_t> pl;
    put_be16(pl, STROUT); put_be16(pl, idx); put_be64(pl, fmt);
    return xact(CMD_SET_FMT, pl);
}

// the shape's power-on slot words (see gen_odmap_shape.py):
// slots 0..3 ring pairs 0..3 (SPO0), 4..5 loopback rx1 pairs 0..1,
// 6..7 ring pairs 6..7 (SPO1)
static const int SEED_W[8] = {0x0B0, 0x0B1, 0x0B2, 0x0B3,
                              0x1D0, 0x1D1, 0x0B6, 0x0B7};

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_aecp_top;

    dut->rst_n = 0; dut->enable_i = 1;
    dut->srp_domain_vid_i = 0x002;
    dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    dut->entity_id_i = ENTITY_ID; dut->entity_model_id_i = 0;
    dut->entity_caps_i = 0x00008588; dut->talker_sources_i = 2;
    dut->talker_caps_i = 0x4801; dut->listener_sinks_i = 3;
    dut->listener_caps_i = 0x4801; dut->controller_caps_i = 0;
    dut->available_index_i = 7; dut->association_id_i = 0;
    dut->gptp_gm_id_i = 0; dut->gptp_domain_i = 0; dut->pdelay_ns_i = 0;
    dut->link_up_i = 1;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|ENT_MAC[i]; dut->station_mac_i = m; }
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) tick();

    printf("== AECP dynamic audio maps - STREAM_PORT_OUTPUT (USER 08-01) ==\n");

    printf("\n[1] power-on: identity image + capture-crossbar seed\n");
    {
        for (int i = 0; i < 16; i++) tick();     // seed: one pair/IDLE cycle
        auto w = take_wrs();
        ck("seed wrote all 8 identity pair slots", (long)w.size(), 8);
        for (int s = 0; s < 8 && w.size() == 8; s++) {
            char nm[80];
            snprintf(nm, sizeof nm, "seed slot %d word 0x%03X", s, SEED_W[s]);
            ck(nm, w[s].slot*4096 + w[s].word, s*4096 + SEED_W[s]);
        }
        // GET serves the identity as ordinary dynamic mappings
        auto r = xact(CMD_GET_MAP, gm_pl(SPO, 0, 0));
        ck("GET SPO0 page0 SUCCESS", r_status(r), 0);
        ck("number_of_maps = 1 (<= 8 stream channels)", r_be16(r, 44), 1);
        ck("SPO0 identity n=8", r_be16(r, 46), 8);
        ck("SPO0 row0 {0,0,0,0}", row_is(r, 50, 0, 0,0,0,0), 1);
        ck("SPO0 row7 {0,7,7,0}", row_is(r, 50, 7, 0,7,7,0), 1);
        ck("SPO0 cdl 24+64", b_cdl(r), 88);
        r = xact(CMD_GET_MAP, gm_pl(SPO, 1, 0));
        ck("SPO1 identity n=8 (loop+ring mix)", r_be16(r, 46), 8);
        ck("SPO1 row0 {1,0,0,0}", row_is(r, 50, 0, 1,0,0,0), 1);
        ck("SPO1 row4 {1,4,4,0}", row_is(r, 50, 4, 1,4,4,0), 1);
        r = xact(CMD_GET_MAP, gm_pl(SPO, 0, 1));
        ck("map_index 1 BAD_ARGUMENTS (single page)", r_status(r), 7);
        r = xact(CMD_GET_MAP, gm_pl(SPO, 2, 0));
        ck("SPO2 (absent) NO_SUCH_DESCRIPTOR", r_status(r), 2);
    }

    printf("\n[2] 7.2.13: dynamic output ports advertise number_of_maps=0\n");
    {
        std::vector<uint8_t> pl; put_be16(pl,0); put_be16(pl,0);
        put_be16(pl, SPO); put_be16(pl, 1);
        auto r = xact(CMD_READ, pl);
        ck("SPO1 READ SUCCESS", r_status(r), 0);
        ck("SPO1 number_of_maps = 0 (dynamic)", r_be16(r, 58), 0);
        pl.clear(); put_be16(pl,0); put_be16(pl,0);
        put_be16(pl, 0x0017); put_be16(pl, 0);          // AUDIO_MAP[0]
        r = xact(CMD_READ, pl);
        ck("no AUDIO_MAP descriptor survives", r_status(r), 2);
    }

    printf("\n[3] ADD vendor rules (7.4.45.1): all-or-nothing rejects\n");
    {
        take_wrs();
        auto r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,0,0,0}}}));
        ck("odd record count (half a pair) BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{0,0,0,0}}, {{0,1,1,0}}}));
        ck("stream_index 0 is not SPO1's stream BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,0,0,0}}, {{1,2,1,0}}}));
        ck("non-adjacent channels {0,2} BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,0,1,0}}, {{1,1,0,0}}}));
        ck("swapped source halves BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,0,0,0}}, {{1,1,3,0}}}));
        ck("R half from a DIFFERENT source pair BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,8,0,0}}, {{1,9,1,0}}}));
        ck("stream channel 8 of an 8ch format BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,0,9,0}}, {{1,1,10,0}}}));
        ck("cluster_offset 9 of 9 clusters BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,0,0,1}}, {{1,1,1,1}}}));
        ck("cluster_channel != 0 (mono clusters) BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,0,0,0}}, {{1,1,1,0}},
                                             {{1,0,2,0}}, {{1,1,3,0}}}));
        ck("same stream channel twice in one command BAD_ARG", r_status(r), 7);
        ck("no reject reached the fabric", (long)take_wrs().size(), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPO, 1, 0));
        ck("store untouched (identity n=8)", r_be16(r, 46), 8);
    }

    printf("\n[4] ADD round-trips: TONE pair + loopback re-route\n");
    {
        take_wrs();
        //! the mono pilot: BOTH channels of the pair reference cluster 8
        auto r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,4,8,0}}, {{1,5,8,0}}}));
        ck("TONE pair {sc4,sc5}<-cl8 SUCCESS", r_status(r), 0);
        { auto w = take_wrs();
          ck("one pair-slot write", (long)w.size(), 1);
          if (w.size()==1) ck("slot 6 word {en,TONE} 0x0C0",
                              w[0].slot*4096 + w[0].word, 6*4096 + 0x0C0); }
        r = xact(CMD_GET_MAP, gm_pl(SPO, 1, 0));
        ck("rows still 8 (replaced, not added)", r_be16(r, 46), 8);
        ck("row4 now {1,4,8,0}", row_is(r, 50, 4, 1,4,8,0), 1);
        ck("row5 now {1,5,8,0}", row_is(r, 50, 5, 1,5,8,0), 1);

        //! re-route stream 1 channels 0/1 from loop pair 0 to loop pair 1
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,0,2,0}}, {{1,1,3,0}}}));
        ck("loop pair re-route SUCCESS", r_status(r), 0);
        { auto w = take_wrs();
          ck("one pair-slot write", (long)w.size(), 1);
          if (w.size()==1) ck("slot 4 word {idxh1,en,LOOP,idx1} 0x1D1",
                              w[0].slot*4096 + w[0].word, 4*4096 + 0x1D1); }
        r = xact(CMD_GET_MAP, gm_pl(SPO, 1, 0));
        ck("row0 now {1,0,2,0}", row_is(r, 50, 0, 1,0,2,0), 1);
    }

    printf("\n[5] REMOVE: pair-exact, absent refused, slot disarmed\n");
    {
        take_wrs();
        auto r = xact(CMD_RM_MAP, am_pl(SPO, 1, {{{1,4,4,0}}, {{1,5,5,0}}}));
        ck("REMOVE with stale clusters (TONE replaced them) BAD_ARG",
           r_status(r), 7);
        ck("refusal wrote nothing", (long)take_wrs().size(), 0);
        r = xact(CMD_RM_MAP, am_pl(SPO, 1, {{{1,4,8,0}}, {{1,5,8,0}}}));
        ck("REMOVE the TONE pair SUCCESS", r_status(r), 0);
        { auto w = take_wrs();
          ck("one disarm write", (long)w.size(), 1);
          if (w.size()==1) ck("slot 6 word 0 (en=0)",
                              w[0].slot*4096 + w[0].word, 6*4096 + 0x000); }
        r = xact(CMD_GET_MAP, gm_pl(SPO, 1, 0));
        ck("rows now 6", r_be16(r, 46), 6);
        r = xact(CMD_RM_MAP, am_pl(SPO, 1, {{{1,4,8,0}}, {{1,5,8,0}}}));
        ck("REMOVE again (absent) BAD_ARG (7.4.46.1)", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,4,4,0}}, {{1,5,5,0}}}));
        ck("identity ring pair restored", r_status(r), 0);
    }

    printf("\n[6] u=1 replay to registered controllers (7.5.2)\n");
    {
        feed_rx(aem_cmd2(CTL2_MAC, CTLR2_ID, CMD_REG_UNSOL, seq++, {}));
        auto r = collect_resp();
        ck("ctlr2 REGISTER SUCCESS", r_status(r), 0);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,0,0,0}}, {{1,1,1,0}}}));
        ck("output ADD (a change) SUCCESS", r_status(r), 0);
        auto u = collect_resp();
        ck("replay (u=1) arrived at ctlr2", r_u(u), 1);
        ck("replay is the ADD response", r_be16(u, 36) & 0x7FFF, CMD_ADD_MAP);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{1,0,0,0}}, {{1,1,1,0}}}));
        ck("same ADD again SUCCESS", r_status(r), 0);
        u = collect_resp();
        ck("no-change ADD -> NO replay (nochg)", (long)u.size(), 0);
        feed_rx(aem_cmd2(CTL2_MAC, CTLR2_ID, CMD_DEREG_UNSOL, seq++, {}));
        r = collect_resp();
        ck("ctlr2 DEREGISTER SUCCESS", r_status(r), 0);
    }

    printf("\n[7] the channel bound is the DECLARED format (FR-STR-03)\n");
    {
        //! w_out_fmt_ok accepts ONLY the declared output format (the
        //! framer's channel count is an elaboration constant - wire
        //! truth), so the Milan 5.4.2.27 current-format bound can never
        //! move and no talker-side prune path exists to test: a format
        //! shrink is refused at the SET door.
        take_wrs();
        auto r = setofmt(1, AAF2);
        ck("SET_STREAM_FORMAT out1 -> 2ch REFUSED (wire truth)",
           r_status(r), 7);
        ck("...and touched no capture slot", (long)take_wrs().size(), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPO, 1, 0));
        ck("maps untouched by the refused SET (n=8)", r_be16(r, 46), 8);
        r = setofmt(1, AAF8);
        ck("SET_STREAM_FORMAT out1 = declared 8ch SUCCESS", r_status(r), 0);
    }

    printf("\n[8] reset restores the identity default\n");
    {
        auto r = xact(CMD_RM_MAP, am_pl(SPO, 0, {{{0,0,0,0}}, {{0,1,1,0}}}));
        ck("REMOVE an SPO0 identity pair SUCCESS", r_status(r), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPO, 0, 0));
        ck("pre-reset SPO0 n=6", r_be16(r, 46), 6);
        dut->rst_n = 0;
        for (int i = 0; i < 4; i++) tick();
        take_wrs();
        dut->rst_n = 1;
        for (int i = 0; i < 16; i++) tick();
        auto w = take_wrs();
        ck("re-seed wrote all 8 identity pair slots", (long)w.size(), 8);
        r = xact(CMD_GET_MAP, gm_pl(SPO, 0, 0));
        ck("post-reset SPO0 identity n=8", r_be16(r, 46), 8);
        ck("post-reset row0 {0,0,0,0}", row_is(r, 50, 0, 0,0,0,0), 1);
        r = xact(CMD_GET_MAP, gm_pl(SPO, 1, 0));
        ck("post-reset SPO1 identity n=8", r_be16(r, 46), 8);
    }

    printf("\n----------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
