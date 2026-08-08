/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * sim_odmap_tdm8 - the SHIPPING ax7101_1x1_tdm8 shape's dynamic
 * STREAM_PORT_OUTPUT leg (task #32 item 3).
 *
 * WIRE TRUTH (VERSION 0x002D silicon): on this shape an ADD_AUDIO_MAPPINGS
 * for SPO0 with the byte-exact Figure 7-71 record {stream_index 0,
 * stream_channel 0, cluster_offset 8, cluster_channel 0} landed the
 * capture-map write at KEY 1 (a second ADD with sc=1 landed at KEY 2):
 * the snap read key0=0x0000 / key1=0x1400 / key2=0x1400 and the wire
 * carried the pilot tone shifted +1 channel, while GET_AUDIO_MAP echoed
 * the CORRECT records. Every prior odmap witness (sim_odmap.cpp) ran the
 * gen_odmap_shape.py TB shape - the tdm8 config had NO aecp sim leg, so
 * this replays the exact silicon sequence on the exact silicon tables:
 * seed settles, ADD {0,0,8,0} -> slot 0 must take the cluster-8 TONE
 * template, ADD {0,1,8,0} -> slot 1, then GET echoes both records.
 *
 * SHAPE (configs/generated/endstation_ax7101_1x1_tdm8): ONE dynamic
 * STREAM_PORT_OUTPUT, 17 clusters (8 ring/host + TONE at cluster_offset 8
 * + 8 more), KEYS=8, PCBASE=0, PSTR=0, SCH=8; identity seed = keys 0..7
 * onto clusters 0..7 (ring templates 0x1300..0x1B03).
 *
 * VERDICT this leg established: the builder's key math is straight on the
 * tdm8 tables for the silicon sequence AND the campaign priors (u=1
 * replay re-commits, retries, input-engine interleaves) - and the
 * silicon's own GET/store views (correct records) already certified the
 * builder state, because GET is served from ov_r/oco_r, written from the
 * SAME odk_key_q register, in the SAME cycle, that drives the slot port.
 * The uniform +1 (which also holed key 0 out of the boot seed) therefore
 * sat on the write-address side; the RTL fix hoists the seeder's
 * block-local `automatic` key-resolve temporaries - the file's twice-
 * purged synthesis hazard class, and the only such construct left on
 * this path - to module-scope wires (KL_aecp_response_builder.sv,
 * w_odsd_*). This leg pins the port contract those views relied on, on
 * the shape that shipped without one.
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

//! capture-crossbar mirror recorder: every odmap_wr_p_o pulse (key, word)
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
static int r_be16(const std::vector<uint8_t>& b, size_t off){
    return b.size() > off+1 ? (b[off]<<8 | b[off+1]) : -1;
}

static uint16_t seq = 0x7100;
static std::vector<uint8_t> xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
    feed_rx(aem_cmd(cmd, seq++, pl));
    return collect_resp();
}

static const uint16_t CMD_REG_UNSOL = 36, CMD_DEREG_UNSOL = 37;
static const uint16_t CMD_GET_MAP = 43, CMD_ADD_MAP = 44, CMD_RM_MAP = 45;
static const uint16_t SPO = 0x000F, SPI = 0x000E;
static int r_u(const std::vector<uint8_t>& b){
    return b.size() > 36 ? (b[36] >> 7) & 1 : -1;
}

static std::vector<uint8_t> gm_pl(uint16_t t, uint16_t i, uint16_t page) {
    std::vector<uint8_t> pl;
    put_be16(pl, t); put_be16(pl, i); put_be16(pl, page); put_be16(pl, 0);
    return pl;
}
//! byte-exact Figure 7-71 payload: desc_type(2) desc_index(2)
//! number_of_mappings(2) reserved(2) then {si,sc,co,cc} big-endian
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

//! tdm8 power-on channel entries == AEM_ODMAP_CSRC_C[0..7] (ring identity)
static const int SEED_W[8] = {0x1300, 0x1B00, 0x1301, 0x1B01,
                              0x1302, 0x1B02, 0x1303, 0x1B03};
static const int TONE_W = 0x1400;   //! AEM_ODMAP_CSRC_C[8], the pilot tone
static long wr_key(int slot, int word) { return (long)slot * 65536 + word; }

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
    // gh #58 stream-command law truth vectors: wake unbound / not streaming
    dut->lstn_bound_v_i = 0; dut->out_streaming_v_i = 0;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|ENT_MAC[i]; dut->station_mac_i = m; }
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) tick();

    printf("== AECP odmap on the SHIPPING tdm8 shape (task #32 item 3) ==\n");

    printf("\n[1] boot: the seeder settles first (the silicon order)\n");
    {
        for (int i = 0; i < 24; i++) tick();   // seed: one channel/IDLE cycle
        auto w = take_wrs();
        ck("seed wrote all 8 identity channel entries", (long)w.size(), 8);
        for (int s = 0; s < 8 && w.size() == 8; s++) {
            char nm[80];
            snprintf(nm, sizeof nm, "seed key %d word 0x%04X", s, SEED_W[s]);
            ck(nm, wr_key(w[s].slot, w[s].word), wr_key(s, SEED_W[s]));
        }
    }

    printf("\n[2] THE silicon record: ADD {SPO,0,nmaps=1,[0,0,8,0]}\n");
    {
        take_wrs();
        auto r = xact(CMD_ADD_MAP, am_pl(SPO, 0, {{{0,0,8,0}}}));
        ck("ADD {0,0,8,0} SUCCESS", r_status(r), 0);
        auto w = take_wrs();
        ck("exactly one capture-map write", (long)w.size(), 1);
        if (w.size() == 1) {
            //! silicon carried this write at KEY 1 - the +1 defect
            ck("slot IS the stream channel: key 0 (silicon: 1)",
               w[0].slot, 0);
            ck("word = cluster-8 TONE template 0x1400", w[0].word, TONE_W);
        }
    }

    printf("\n[3] the second silicon ADD: [0,1,8,0] -> slot 1\n");
    {
        take_wrs();
        auto r = xact(CMD_ADD_MAP, am_pl(SPO, 0, {{{0,1,8,0}}}));
        ck("ADD {0,1,8,0} SUCCESS", r_status(r), 0);
        auto w = take_wrs();
        ck("exactly one capture-map write", (long)w.size(), 1);
        if (w.size() == 1) {
            ck("slot 1 (silicon: 2)", w[0].slot, 1);
            ck("word = the same TONE template", w[0].word, TONE_W);
        }
    }

    printf("\n[4] GET_AUDIO_MAP echoes both records at their channels\n");
    {
        auto r = xact(CMD_GET_MAP, gm_pl(SPO, 0, 0));
        ck("GET SPO0 page0 SUCCESS", r_status(r), 0);
        ck("number_of_maps = 1", r_be16(r, 44), 1);
        ck("n = 8 (replaced, not added)", r_be16(r, 46), 8);
        ck("row0 {0,0,8,0}", row_is(r, 50, 0, 0,0,8,0), 1);
        ck("row1 {0,1,8,0}", row_is(r, 50, 1, 0,1,8,0), 1);
        ck("row2 keeps identity {0,2,2,0}", row_is(r, 50, 2, 0,2,2,0), 1);
        ck("row7 keeps identity {0,7,7,0}", row_is(r, 50, 7, 0,7,7,0), 1);
    }

    //! ================================================================
    //! CAMPAIGN PRIORS - the silicon ADD never ran on a virgin entity:
    //! controllers were REGISTERED (u=1 replays re-run the commit from
    //! the held cbuf), REMOVEs/input-side edits/GETs interleaved, and
    //! controllers retried on timeout. Each prior is replayed here with
    //! every capture-map pulse audited, so a key shift that needs prior
    //! state cannot hide.
    //! ================================================================
    printf("\n[5] u=1 replay re-runs the commit: same key, same word\n");
    {
        feed_rx(aem_cmd2(CTL2_MAC, CTLR2_ID, CMD_REG_UNSOL, seq++, {}));
        auto r = collect_resp();
        ck("ctlr2 REGISTER SUCCESS", r_status(r), 0);
        take_wrs();
        r = xact(CMD_ADD_MAP, am_pl(SPO, 0, {{{0,2,8,0}}}));
        ck("ADD {0,2,8,0} SUCCESS", r_status(r), 0);
        auto u = collect_resp();
        ck("replay (u=1) arrived at ctlr2", r_u(u), 1);
        auto w = take_wrs();
        for (auto& x : w) printf("       wr slot=%d word=0x%04X\n", x.slot, x.word);
        ck("live + replay re-commit = two writes", (long)w.size(), 2);
        long bad = 0;
        for (auto& x : w) if (x.slot != 2 || x.word != TONE_W) bad++;
        ck("every write is slot 2 word 0x1400 (no +1)", bad, 0);
    }

    printf("\n[6] REMOVE under replay: the disarm also re-runs on key\n");
    {
        take_wrs();
        auto r = xact(CMD_RM_MAP, am_pl(SPO, 0, {{{0,2,8,0}}}));
        ck("REMOVE {0,2,8,0} SUCCESS", r_status(r), 0);
        collect_resp();                       // drain the u=1 replay
        auto w = take_wrs();
        for (auto& x : w) printf("       wr slot=%d word=0x%04X\n", x.slot, x.word);
        long bad = 0;
        for (auto& x : w) if (x.slot != 2 || x.word != 0x0000) bad++;
        ck("every disarm write is slot 2 word 0x0000", bad, 0);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 0, {{{0,2,2,0}}}));
        ck("identity ch2 restored SUCCESS", r_status(r), 0);
        collect_resp();
        take_wrs();
        feed_rx(aem_cmd2(CTL2_MAC, CTLR2_ID, CMD_DEREG_UNSOL, seq++, {}));
        r = collect_resp();
        ck("ctlr2 DEREGISTER SUCCESS", r_status(r), 0);
    }

    printf("\n[7] campaign order: GET first, input-engine interleave\n");
    {
        auto r = xact(CMD_GET_MAP, gm_pl(SPO, 0, 0));
        ck("inspect GET SUCCESS", r_status(r), 0);
        take_wrs();
        //! render-side edit between output edits (the listener chmap ops)
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,0,0,0}}}));
        ck("input ADD {0,0,0,0} SUCCESS", r_status(r), 0);
        ck("input engine touched NO capture slot", (long)take_wrs().size(), 0);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 0, {{{0,3,8,0}}}));
        ck("ADD {0,3,8,0} SUCCESS", r_status(r), 0);
        { auto w = take_wrs();
          ck("one write", (long)w.size(), 1);
          if (w.size()==1) ck("slot 3 (not 4)",
                              wr_key(w[0].slot, w[0].word), wr_key(3, TONE_W)); }
        r = xact(CMD_RM_MAP, am_pl(SPO, 0, {{{0,3,8,0}}}));
        ck("REMOVE {0,3,8,0} SUCCESS", r_status(r), 0);
        { auto w = take_wrs();
          ck("one write", (long)w.size(), 1);
          if (w.size()==1) ck("slot 3 zeroed",
                              wr_key(w[0].slot, w[0].word), wr_key(3, 0x0000)); }
        r = xact(CMD_ADD_MAP, am_pl(SPO, 0, {{{0,3,3,0}}}));
        ck("identity ch3 restored SUCCESS", r_status(r), 0);
        take_wrs();
    }

    printf("\n[8] controller retry (same sequence_id) stays on key\n");
    {
        take_wrs();
        feed_rx(aem_cmd(CMD_ADD_MAP, 0x7F00, am_pl(SPO, 0, {{{0,4,8,0}}})));
        auto r = collect_resp();
        ck("ADD {0,4,8,0} SUCCESS", r_status(r), 0);
        feed_rx(aem_cmd(CMD_ADD_MAP, 0x7F00, am_pl(SPO, 0, {{{0,4,8,0}}})));
        r = collect_resp();
        ck("retry answered SUCCESS", r_status(r), 0);
        auto w = take_wrs();
        for (auto& x : w) printf("       wr slot=%d word=0x%04X\n", x.slot, x.word);
        long bad = 0;
        for (auto& x : w) if (x.slot != 4 || x.word != TONE_W) bad++;
        ck("every retry-span write is slot 4 word 0x1400", bad, 0);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 0, {{{0,4,4,0}}}));
        ck("identity ch4 restored SUCCESS", r_status(r), 0);
        take_wrs();
        r = xact(CMD_GET_MAP, gm_pl(SPO, 0, 0));
        ck("final GET n=8", r_be16(r, 46), 8);
        ck("row0 stays {0,0,8,0}", row_is(r, 50, 0, 0,0,8,0), 1);
        ck("row1 stays {0,1,8,0}", row_is(r, 50, 1, 0,1,8,0), 1);
        ck("row2 back to identity {0,2,2,0}", row_is(r, 50, 2, 0,2,2,0), 1);
    }

    printf("\n----------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
