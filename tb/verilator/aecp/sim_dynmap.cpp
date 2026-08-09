/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Dynamic audio-map harness (gaps item 8): KL_aecp_top compiled against the
 * dynamic-input-port shape svh (gen_dynmap_shape.py — STREAM_PORT_INPUT[0]
 * map_mode dynamic, no AUDIO_MAP descriptor, number_of_maps=0 per 1722.1-2021
 * 7.2.13; keys=8, page=4 => number_of_maps=2; STREAM_PORT_OUTPUT[0] keeps its
 * static map). Exercises Milan 5.4.2.26-28 / IEEE 7.4.44-46:
 *   - READ_DESCRIPTOR advertises the dynamic capability (n_maps=0)
 *   - GET_AUDIO_MAP paging (fixed number_of_maps, per-page mappings,
 *     map_index out of range -> BAD_ARGUMENTS)
 *   - ADD round-trip + all-or-nothing validation rejects (bad stream_index/
 *     channel/cluster, intra-command same-key conflict, malformed length)
 *   - current-format channel bound follows SET_STREAM_FORMAT
 *   - u=1 replay to registered controllers on change, suppressed on no-change
 *   - REMOVE exact-match semantics, duplicate/unmatched entries ignored
 *   - static output port still refuses ADD/REMOVE (NOT_SUPPORTED) and the
 *     lock rule blocks edits from a non-owning controller
 *   - render taps: cluster 0/1 mappings exported live (dmap_l/r_*_o)
 * Exit 0 = all pass.
 */

#include "VKL_aecp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <array>
#include <vector>

// AAF sink count of this harness's entity shape (the CRF sink
// past it answers the Milan-mandatory 0xF3F from the crf_cnt_* ports)
#define N_AAF_SINKS_TB 1

static VKL_aecp_top* dut;
static long checks = 0, fails = 0;

//! chmap64 fabric-mirror recorder: every dmap_wr_p_o pulse (addr, word)
struct DmapWr { int addr, word; };
static std::vector<DmapWr> g_dmap_wrs;
static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    if (dut->dmap_wr_p_o)
        g_dmap_wrs.push_back({(int)dut->dmap_wr_addr_o, (int)dut->dmap_wr_word_o});
}
static std::vector<DmapWr> take_wrs() { auto v = g_dmap_wrs; g_dmap_wrs.clear(); return v; }
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-52s = %ld\n", what, got); }
}

static const uint8_t ENT_MAC[6]  = {0x02,0x00,0x00,0xff,0xfe,0x01};
static const uint8_t CTL_MAC[6]  = {0x68,0x05,0xca,0x95,0xb2,0xd1};
static const uint8_t CTL2_MAC[6] = {0x68,0x05,0xca,0x95,0xb2,0xd2};
static const uint64_t ENTITY_ID = 0x0200'00ff'fe00'0001ULL;
static const uint64_t CTLR_ID   = 0x6805'ca95'b2d1'0000ULL;
static const uint64_t CTLR2_ID  = 0x6805'ca95'b2d2'0000ULL;

static void put_be64(std::vector<uint8_t>& v, uint64_t x) {
    for (int i = 7; i >= 0; i--) v.push_back((x >> (8*i)) & 0xFF);
}
static void put_be16(std::vector<uint8_t>& v, uint16_t x) {
    v.push_back(x >> 8); v.push_back(x & 0xFF);
}

//! AEM command frame layout: 14 B Ethernet + 4 B AVTP common header + 8 B
//! target_entity_id + 8 B controller_entity_id + 2 B sequence_id + 2 B
//! u/command_type = 38 B ahead of the command_specific payload, and the whole
//! frame is padded up to the 60 B Ethernet minimum.
static const size_t AEM_HDR_BYTES = 38;
static const size_t ETH_MIN_BYTES = 60;

//! Widest AEM response this suite collects (a READ_DESCRIPTOR reply), used to
//! size the collector once instead of growing it a beat at a time.
static const size_t AEM_RESP_BYTES = 600;

//! One reusable stimulus buffer for the whole run. The builder below fills it
//! through a reference and clear() keeps its capacity, so the command bytes
//! cost ONE allocation for the entire simulation instead of a malloc plus
//! three or four reallocs on every transaction.
static std::vector<uint8_t> stim;

//! Fill `out` with an AEM command frame from an arbitrary controller and
//! hand back a reference to it, so a call site reads
//! `feed_rx(build_aem_cmd2(stim, ...))` and reuses one buffer.
static const std::vector<uint8_t>& build_aem_cmd2(std::vector<uint8_t>& out,
                                     const uint8_t* src_mac, uint64_t ctlr,
                                     uint16_t cmd, uint16_t seq,
                                     const std::vector<uint8_t>& payload) {
    size_t want = AEM_HDR_BYTES + payload.size();
    out.clear();                                // clear KEEPS the capacity
    out.reserve(want < ETH_MIN_BYTES ? ETH_MIN_BYTES : want);
    std::vector<uint8_t>& f = out;
    for (int i=0;i<6;i++) f.push_back(ENT_MAC[i]);
    for (int i=0;i<6;i++) f.push_back(src_mac[i]);
    put_be16(f, 0x22F0);
    f.push_back(0xFB);                          // subtype AECP
    f.push_back(0x00);                          // AEM_COMMAND
    uint16_t cdl = 12 + (uint16_t)payload.size();
    f.push_back((cdl >> 8) & 0x7);
    f.push_back(cdl & 0xFF);
    put_be64(f, ENTITY_ID);
    put_be64(f, ctlr);
    put_be16(f, seq);
    f.push_back((cmd >> 8) & 0x7F);
    f.push_back(cmd & 0xFF);
    for (auto b : payload) f.push_back(b);
    while (f.size() < ETH_MIN_BYTES) f.push_back(0x00);
    return out;
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
    b.reserve(AEM_RESP_BYTES);          // one allocation, not one per beat run
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
static int r_u(const std::vector<uint8_t>& b){ return b.size()>36 ? (b[36]>>7)&1 : -1; }
static int r_be16(const std::vector<uint8_t>& b, size_t off){
    return b.size() > off+1 ? (b[off]<<8 | b[off+1]) : -1;
}
//! IEEE 1722-2016 4.4.5.4: control_data_length is "the length (in octets) of
//! the control_data_payload field", which starts after the 8-octet stream_id
//! (target_entity_id) at AVTPDU octet 12 -> frame bytes 16..17.
static int r_cdl(const std::vector<uint8_t>& b) {
    return b.size()>17 ? (((b[16]&0x7)<<8) | b[17]) : -1;
}

static uint16_t seq = 0x5000;
static std::vector<uint8_t> xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
    feed_rx(build_aem_cmd2(stim, CTL_MAC, CTLR_ID, cmd, seq++, pl));
    return collect_resp();
}

static const uint16_t CMD_LOCK = 1, CMD_READ = 4, CMD_SET_FMT = 8;
static const uint16_t CMD_REG_UNSOL = 36, CMD_DEREG_UNSOL = 37;
static const uint16_t CMD_GET_MAP = 43, CMD_ADD_MAP = 44, CMD_RM_MAP = 45;
static const uint16_t SPI = 0x000E, SPO = 0x000F;
static const uint64_t AAF2 = 0x0205022000806000ULL;  // 48k 2ch (reset default)
static const uint64_t AAF8 = 0x0205022002006000ULL;  // 48k 8ch concrete

// GET_AUDIO_MAP payload: type(2) idx(2) map_index(2) reserved(2)
static std::vector<uint8_t> gm_pl(uint16_t t, uint16_t i, uint16_t page) {
    std::vector<uint8_t> pl;
    pl.reserve(8);                              // four u16 fields, exactly
    put_be16(pl, t); put_be16(pl, i); put_be16(pl, page); put_be16(pl, 0);
    return pl;
}
// ADD/REMOVE payload: type(2) idx(2) n(2) reserved(2) + n x {si,sc,co,cc};
// n_override lets a case lie about the count (malformed-length reject)
static std::vector<uint8_t> am_pl(uint16_t t, uint16_t i,
                                  const std::vector<std::array<uint16_t,4>>& m,
                                  int n_override = -1) {
    std::vector<uint8_t> pl;
    pl.reserve(8 + 8 * m.size());               // 8 B header + 8 B per record
    put_be16(pl, t); put_be16(pl, i);
    put_be16(pl, n_override >= 0 ? (uint16_t)n_override : (uint16_t)m.size());
    put_be16(pl, 0);
    for (auto& r : m) { for (int k = 0; k < 4; k++) put_be16(pl, r[k]); }
    return pl;
}
// mapping row at wire offset base (GET resp: base 50; ADD/RM echo: base 46)
static bool row_is(const std::vector<uint8_t>& b, size_t base, int n,
                   uint16_t si, uint16_t sc, uint16_t co, uint16_t cc) {
    size_t o = base + 8*(size_t)n;
    return r_be16(b,o) == si && r_be16(b,o+2) == sc &&
           r_be16(b,o+4) == co && r_be16(b,o+6) == cc;
}

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
    dut->talker_caps_i = 0x4801; dut->listener_sinks_i = 2;
    dut->listener_caps_i = 0x4801; dut->controller_caps_i = 0;
    dut->available_index_i = 7; dut->association_id_i = 0;
    dut->gptp_gm_id_i = 0; dut->gptp_domain_i = 0; dut->pdelay_ns_i = 0;
    dut->link_up_i = 1;
    // Milan 5.4.2.25 per-index counter buses: zero until a case models
    // them (the fabric muxes by gs_diag_idx_o; here the harness owns them)
    for (int w = 0; w < 10; w++) dut->rxdiag_cnt_i[w] = 0;
    for (int w = 0; w < 5; w++)  dut->tkdiag_cnt_i[w] = 0;
    dut->n_aaf_sinks_i = N_AAF_SINKS_TB;
    // gh #58 stream-command law truth vectors: wake unbound / not streaming
    dut->lstn_bound_v_i = 0; dut->out_streaming_v_i = 0;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|ENT_MAC[i]; dut->station_mac_i = m; }
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) tick();

    printf("== AECP dynamic audio maps — AEM_DYNMAP shape ==\n");

    printf("\n[0] power-on fabric seed mirrors the identity default\n");
    {
        // USER directive 08-01: the dynamic store wakes as the IDENTITY
        // map (port p's clusters <- stream p's channels, C = min(clusters,
        // stream channels)); Milan 5.3.3.9 forbids a static AUDIO_MAP on
        // an input port, so the default lives in the dynamic store's reset
        // image, and the render crossbar (which wakes empty) must be
        // seeded to agree - the wire-truth rule. This shape: stream 0 is
        // 2ch, so exactly clusters 0 and 1 wake mapped.
        for (int i = 0; i < 12; i++) tick();     // walker: one key/cycle
        auto w = take_wrs();
        ck("seed wrote exactly the identity keys", (long)w.size(), 2);
        if (w.size() == 2) {
            ck("seed addr0/word {en,st0,ch0}", w[0].addr*256 + w[0].word,
               0*256 + 0x80);
            ck("seed addr1/word {en,st0,ch1}", w[1].addr*256 + w[1].word,
               1*256 + 0x81);
        }
        ck("identity projects to render tap L (en, ch0)",
           dut->dmap_l_en_o*16 + dut->dmap_l_ch_o, 0x10);
        ck("identity projects to render tap R (en, ch1)",
           dut->dmap_r_en_o*16 + dut->dmap_r_ch_o, 0x11);
    }

    printf("\n[1] READ_DESCRIPTOR: 7.2.13 dynamic-map capability\n");
    {
        std::vector<uint8_t> pl; put_be16(pl,0); put_be16(pl,0);
        put_be16(pl, SPI); put_be16(pl, 0);
        auto r = xact(CMD_READ, pl);
        ck("SPI0 READ SUCCESS", r_status(r), 0);
        ck("SPI0 number_of_maps = 0 (dynamic)", r_be16(r, 58), 0);
        ck("SPI0 base_map = 0 (ignored)", r_be16(r, 60), 0);
        pl.clear(); put_be16(pl,0); put_be16(pl,0);
        put_be16(pl, SPO); put_be16(pl, 0);
        r = xact(CMD_READ, pl);
        ck("SPO0 READ SUCCESS", r_status(r), 0);
        ck("SPO0 number_of_maps = 1 (static)", r_be16(r, 58), 1);
        ck("SPO0 base_map = 0 (map renumbered)", r_be16(r, 60), 0);
        pl.clear(); put_be16(pl,0); put_be16(pl,0);
        put_be16(pl, 0x0017); put_be16(pl, 1);          // AUDIO_MAP[1]
        r = xact(CMD_READ, pl);
        ck("AUDIO_MAP[1] gone (NO_SUCH_DESCRIPTOR)", r_status(r), 2);
    }

    printf("\n[2] GET_AUDIO_MAP identity default + paging bounds\n");
    {
        // the store wakes as the identity map ([0] above), served as
        // ordinary dynamic mappings (Milan 5.4.2.26 knows no other kind
        // on an input port): page0 carries the 2ch identity, page1 none
        auto r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("GET page0 SUCCESS", r_status(r), 0);
        ck("number_of_maps = 2 (fixed partition)", r_be16(r, 44), 2);
        ck("page0 number_of_mappings = 2 (identity)", r_be16(r, 46), 2);
        ck("row0 = cl0 <- st0 ch0", row_is(r, 50, 0, 0,0,0,0), 1);
        ck("row1 = cl1 <- st0 ch1", row_is(r, 50, 1, 0,1,1,0), 1);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 1));
        ck("GET page1 SUCCESS", r_status(r), 0);
        ck("page1 number_of_maps = 2", r_be16(r, 44), 2);
        ck("page1 number_of_mappings = 0", r_be16(r, 46), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 2));
        ck("GET page2 BAD_ARGUMENTS (7.4.44.1)", r_status(r), 7);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 1, 0));
        ck("GET SPI1 NO_SUCH_DESCRIPTOR", r_status(r), 2);
        // Milan v1.2 5.4.2.26: "If a PAAD-AE receives a GET_AUDIO_MAP command
        // for a Stream Port Output that has Audio Map(s), the PAAD-AE shall
        // reply with the NOT_SUPPORTED error code." This shape's output port
        // keeps its static Audio Map, so it refuses - the same verdict this
        // file already asserts for ADD/REMOVE in [8], from the
        // identically-worded 5.4.2.27/28. It used to assert SUCCESS and a
        // served row.
        r = xact(CMD_GET_MAP, gm_pl(SPO, 0, 0));
        ck("GET output (has a map) NOT_SUPPORTED (Milan 5.4.2.26)",
           r_status(r), 11);
        ck("output refusal keeps the 7.4.44.2 12 B payload", r_cdl(r), 24);
        ck("output refusal carries no mappings", r_be16(r, 46), 0);
    }

    printf("\n[3] ADD round-trip: swap map (cl0<-ch1, cl1<-ch0)\n");
    {
        auto r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,1,0,0}}, {{0,0,1,0}}}));
        ck("ADD SUCCESS", r_status(r), 0);
        ck("ADD echoes n=2", r_be16(r, 42), 2);
        ck("ADD echo row0 = {0,1,0,0}", row_is(r, 46, 0, 0,1,0,0), 1);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("GET page0 n=2 after ADD", r_be16(r, 46), 2);
        ck("row0 = cl0 <- st0 ch1", row_is(r, 50, 0, 0,1,0,0), 1);
        ck("row1 = cl1 <- st0 ch0", row_is(r, 50, 1, 0,0,1,0), 1);
        ck("render tap L en", dut->dmap_l_en_o, 1);
        ck("render tap L ch = 1", dut->dmap_l_ch_o, 1);
        ck("render tap R en", dut->dmap_r_en_o, 1);
        ck("render tap R ch = 0", dut->dmap_r_ch_o, 0);
    }

    printf("\n[4] ADD validation rejects (all-or-nothing, 5.4.2.27)\n");
    {
        auto r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,2,2,0}}}));
        ck("stream_channel >= current fmt (2ch) BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{1,0,2,0}}}));
        ck("stream_index 1 (no audio channels) BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,0,8,0}}}));
        ck("cluster_offset 8 (of 8) BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,0,2,1}}}));
        ck("cluster_channel 1 (mono clusters) BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,0,3,0}}, {{0,1,3,0}}}));
        ck("same key twice in one command BAD_ARG", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,1,2,0}}, {{0,9,3,0}}}));
        ck("one bad of two BAD_ARG (none added)", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,0,2,0}}}, 2));
        ck("number_of_mappings != frame length BAD_ARG", r_status(r), 7);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("store untouched by the rejects (n still 2)", r_be16(r, 46), 2);
    }

    printf("\n[5] format-bound follows SET_STREAM_FORMAT + real paging\n");
    {
        std::vector<uint8_t> pl; put_be16(pl, 0x0005); put_be16(pl, 0);
        put_be64(pl, AAF8);
        auto r = xact(CMD_SET_FMT, pl);
        ck("SET_STREAM_FORMAT in0 8ch SUCCESS", r_status(r), 0);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,5,5,0}}}));
        ck("ADD cl5 <- ch5 SUCCESS under 8ch fmt", r_status(r), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("page0 (keys 0-3) does NOT list key 5", r_be16(r, 46), 2);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 1));
        ck("page1 (keys 4-7) lists exactly key 5", r_be16(r, 46), 1);
        ck("page1 row0 = {0,5,5,0}", row_is(r, 50, 0, 0,5,5,0), 1);
        r = xact(CMD_RM_MAP, am_pl(SPI, 0, {{{0,5,5,0}}}));
        ck("REMOVE cl5 SUCCESS (state hygiene)", r_status(r), 0);
        pl.clear(); put_be16(pl, 0x0005); put_be16(pl, 0);
        put_be64(pl, AAF2);
        r = xact(CMD_SET_FMT, pl);
        ck("SET_STREAM_FORMAT in0 back to 2ch", r_status(r), 0);
    }

    printf("\n[6] u=1 replay to registered controllers (7.4.45/46)\n");
    {
        feed_rx(build_aem_cmd2(stim, CTL2_MAC, CTLR2_ID, CMD_REG_UNSOL, seq++, {}));
        auto r = collect_resp();
        ck("ctlr2 REGISTER_UNSOLICITED SUCCESS", r_status(r), 0);

        // SET_STREAM_FORMAT above already replayed once; drain nothing more.
        take_wrs();   //! drain earlier sections' fabric-mirror strobes
        feed_rx(build_aem_cmd2(stim, CTL_MAC, CTLR_ID, CMD_ADD_MAP, seq++,
                         am_pl(SPI, 0, {{{0,0,2,0}}})));
        r = collect_resp();
        ck("ADD cl2 SUCCESS (u=0 response)", r_status(r), 0);
        { auto w = take_wrs();
          ck("fabric mirror: ADD -> exactly 1 map write", (long)w.size(), 1);
          if (w.size()==1) { ck("... addr == cluster_offset 2", w[0].addr, 2);
                             ck("... word == {en,strm0,ch0} 0x80", w[0].word, 0x80); } }
        ck("... response u bit = 0", r_u(r), 0);
        auto u = collect_resp();
        ck("replay frame arrived (u=1)", r_u(u), 1);
        ck("replay is the ADD response", r_be16(u, 36) & 0x7FFF, CMD_ADD_MAP);
        ck("replay status SUCCESS", r_status(u), 0);
        ck("replay dst = ctlr2 MAC", memcmp(u.data(), CTL2_MAC, 6), 0);
        { auto w = take_wrs();
          ck("fabric mirror: u=1 replay re-commits idempotently", (long)w.size(), 1);
          if (w.size()==1) ck("... replay word identical 0x80", w[0].word, 0x80); }

        feed_rx(build_aem_cmd2(stim, CTL_MAC, CTLR_ID, CMD_ADD_MAP, seq++,
                         am_pl(SPI, 0, {{{0,0,2,0}}})));
        r = collect_resp();
        ck("same ADD again SUCCESS", r_status(r), 0);
        { auto w = take_wrs();
          ck("fabric mirror: idempotent re-ADD still writes", (long)w.size(), 1); }
        u = collect_resp();
        ck("no-change ADD -> NO replay (nochg rule)", (long)u.size(), 0);

        feed_rx(build_aem_cmd2(stim, CTL_MAC, CTLR_ID, CMD_RM_MAP, seq++,
                         am_pl(SPI, 0, {{{0,0,2,0}}})));
        r = collect_resp();
        ck("REMOVE cl2 SUCCESS", r_status(r), 0);
        { auto w = take_wrs();
          ck("fabric mirror: REMOVE -> 1 clearing write", (long)w.size(), 1);
          if (w.size()==1) { ck("... addr 2, word 0 (en=0)", w[0].addr*256+w[0].word, 2*256+0); } }
        u = collect_resp();
        ck("REMOVE change -> replay (u=1)", r_u(u), 1);
        //! gh #58 D6 (#34): the replay re-runs the walk against a store the
        //! ORIGINAL REMOVE already emptied - the validate pass misses, and
        //! the demote (now command-only) used to turn this u=1 frame into
        //! BAD_ARGUMENTS: a failure announced that never happened. The
        //! status byte was UNCHECKED here; the quartet pins the whole law.
        ck("replay status SUCCESS (7.4.46 rebroadcast)", r_status(u), 0);
        ck("replay is the REMOVE response", r_be16(u, 36) & 0x7FFF, CMD_RM_MAP);
        ck("replay echoes the removed record", row_is(u, 46, 0, 0,0,2,0), 1);
        { auto w = take_wrs();
          ck("replay walked but wrote NOTHING to the fabric",
             (long)w.size(), 0); }

        feed_rx(build_aem_cmd2(stim, CTL_MAC, CTLR_ID, CMD_RM_MAP, seq++,
                         am_pl(SPI, 0, {{{0,0,2,0}}})));
        r = collect_resp();
        //! 7.4.46.1, verbatim: "If any of the mappings in the command are
        //! invalid or not present then the command shall fail with a
        //! BAD_ARGUMENTS status and none of the mappings shall be removed."
        //! Milan 5.4.2.28 overrides that for DUPLICATES only, so an ABSENT
        //! mapping is a refusal, not a silent success (this check asserted
        //! the violation as correct until the 7.4.46.1 read).
        ck("REMOVE of an absent mapping BAD_ARGUMENTS (7.4.46.1)",
           r_status(r), 7);
        { auto w = take_wrs();
          ck("fabric mirror: refused REMOVE -> NO write", (long)w.size(), 0); }
        u = collect_resp();
        ck("... and NO replay (nothing changed)", (long)u.size(), 0);

        // deregister ctlr2: the later cases parse one frame per command
        feed_rx(build_aem_cmd2(stim, CTL2_MAC, CTLR2_ID, CMD_DEREG_UNSOL, seq++, {}));
        r = collect_resp();
        ck("ctlr2 DEREGISTER SUCCESS", r_status(r), 0);
    }

    printf("\n[7] REMOVE semantics: exact match, absent refused, duplicates ignored\n");
    {
        //! wrong stream_channel for that cluster = NOT PRESENT (7.4.46.1)
        auto r = xact(CMD_RM_MAP, am_pl(SPI, 0, {{{0,0,0,0}}}));
        ck("REMOVE cl0 wrong channel: BAD_ARGUMENTS (7.4.46.1)",
           r_status(r), 7);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("cl0 mapping still there (n=2)", r_be16(r, 46), 2);
        r = xact(CMD_RM_MAP, am_pl(SPI, 0, {{{0,1,0,0}}}));
        ck("REMOVE cl0 exact match SUCCESS", r_status(r), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("cl0 gone (n=1)", r_be16(r, 46), 1);
        ck("render tap L en dropped", dut->dmap_l_en_o, 0);
        r = xact(CMD_RM_MAP, am_pl(SPI, 0, {{{0,0,1,0}}, {{0,0,1,0}}}));
        ck("duplicate REMOVE rows SUCCESS (5.4.2.28)", r_status(r), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("cl1 gone too (n=0)", r_be16(r, 46), 0);
        ck("render tap R en dropped", dut->dmap_r_en_o, 0);
    }

    printf("\n[8] static output port + lock rule regressions\n");
    {
        auto r = xact(CMD_ADD_MAP, am_pl(SPO, 0, {{{0,0,0,0}}}));
        ck("ADD on static output NOT_SUPPORTED", r_status(r), 11);
        r = xact(CMD_RM_MAP, am_pl(SPO, 0, {{{0,0,0,0}}}));
        ck("REMOVE on static output NOT_SUPPORTED", r_status(r), 11);

        std::vector<uint8_t> lk(12, 0);   // flags(4)+locked_id(8)
        feed_rx(build_aem_cmd2(stim, CTL2_MAC, CTLR2_ID, CMD_LOCK, seq++, lk));
        r = collect_resp();
        ck("ctlr2 LOCK SUCCESS", r_status(r), 0);
        feed_rx(build_aem_cmd2(stim, CTL_MAC, CTLR_ID, CMD_ADD_MAP, seq++,
                         am_pl(SPI, 0, {{{0,0,2,0}}})));
        r = collect_resp();
        ck("ADD from other controller ENTITY_LOCKED", r_status(r), 3);
        lk[3] = 1;                        // UNLOCK flag
        feed_rx(build_aem_cmd2(stim, CTL2_MAC, CTLR2_ID, CMD_LOCK, seq++, lk));
        r = collect_resp();
        ck("ctlr2 UNLOCK SUCCESS", r_status(r), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("locked ADD left the store empty", r_be16(r, 46), 0);
    }

    printf("\n[9] dynamic edits override the default; reset restores it\n");
    {
        // controller state right now: [7] removed BOTH identity rows (the
        // override in the REMOVE direction). Put a custom row in, then
        // power-cycle: Milan 5.3.10.1 restores the saved list, and with no
        // non-volatile plane the restored image is the identity baseline.
        auto r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,1,3,0}}}));
        ck("custom ADD cl3 <- ch1 SUCCESS", r_status(r), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("pre-reset page0 n=1 (custom, identity stays removed)",
           r_be16(r, 46), 1);
        ck("pre-reset row is the custom one", row_is(r, 50, 0, 0,1,3,0), 1);

        dut->rst_n = 0;
        for (int i = 0; i < 4; i++) tick();
        take_wrs();
        dut->rst_n = 1;
        for (int i = 0; i < 12; i++) tick();     // seed walker replays
        auto w = take_wrs();
        ck("reset re-seeded exactly the identity keys", (long)w.size(), 2);
        if (w.size() == 2)
            ck("... cl0 {en,st0,ch0} again", w[0].addr*256 + w[0].word, 0x80);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("post-reset page0 n=2 (identity restored)", r_be16(r, 46), 2);
        ck("post-reset row0 = cl0 <- st0 ch0", row_is(r, 50, 0, 0,0,0,0), 1);
        ck("post-reset row1 = cl1 <- st0 ch1", row_is(r, 50, 1, 0,1,1,0), 1);
        ck("custom cl3 row did NOT survive the cycle (documented NV gap)",
           r_be16(r, 46) == 2, 1);
    }

    // ---------------------------------------------------------------- //
    // 10. The walk's KEY-RESOLVE / VERDICT cycle contract                //
    //                                                                    //
    // DMAP_SCAN_S resolves the store key - and every value the verdict   //
    // reaches THROUGH that key - one phase before the verdict renders.   //
    // The contract is that the resolve runs again for EVERY record and   //
    // reads the store as it stands BEFORE that record commits. A resolve //
    // that did not re-run would judge record 1 with record 0's key, so   //
    // the witness is order symmetry: the SAME pair of mappings presented //
    // in both orders must reach the same verdict, and two DIFFERENT keys //
    // in one command must land on two different keys.                    //
    // ---------------------------------------------------------------- //
    printf("\n[10] every record resolves its OWN key (walk phase contract)\n");
    {
        auto page = [&](int p) { return xact(CMD_GET_MAP, gm_pl(SPI, 0, p)); };
        // compare two GET_AUDIO_MAP answers ignoring the echoed sequence_id
        auto same_maps = [](const std::vector<uint8_t>& a,
                            const std::vector<uint8_t>& b) {
            if (a.size() != b.size() || a.size() < 38) return 0L;
            return (long)(memcmp(&a[38], &b[38], a.size() - 38) == 0);
        };
        auto p1_before = page(1);              // keys 4..7, empty here

        // (a) one valid + one invalid, BOTH orders: all-or-nothing either
        //     way. A carried-over key makes the good-then-bad order pass.
        auto r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,1,4,0}}, {{0,0,9,0}}}));
        ck("[10a] good-then-bad ADD BAD_ARGUMENTS", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,0,9,0}}, {{0,1,4,0}}}));
        ck("[10a] bad-then-good ADD BAD_ARGUMENTS", r_status(r), 7);
        ck("[10a] neither attempt touched the store",
           same_maps(page(1), p1_before), 1);

        // (b) two DIFFERENT keys in one command land on two different keys
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,0,4,0}}, {{0,1,5,0}}}));
        ck("[10b] two-key ADD SUCCESS", r_status(r), 0);
        auto p1 = page(1);
        ck("[10b] page1 carries TWO rows", r_be16(p1, 46), 2);
        ck("[10b] cl4 <- st0 ch0", row_is(p1, 50, 0, 0,0,4,0), 1);
        ck("[10b] cl5 <- st0 ch1", row_is(p1, 50, 1, 0,1,5,0), 1);

        // (c) REMOVE present + absent, both orders: 7.4.46.1 refuses whole
        r = xact(CMD_RM_MAP, am_pl(SPI, 0, {{{0,0,4,0}}, {{0,1,6,0}}}));
        ck("[10c] present-then-absent REMOVE BAD_ARGUMENTS", r_status(r), 7);
        ck("[10c] ...and removed nothing", same_maps(page(1), p1), 1);
        r = xact(CMD_RM_MAP, am_pl(SPI, 0, {{{0,1,6,0}}, {{0,0,4,0}}}));
        ck("[10c] absent-then-present REMOVE BAD_ARGUMENTS", r_status(r), 7);
        ck("[10c] ...and removed nothing", same_maps(page(1), p1), 1);

        // (d) and the pair really was two independent entries
        r = xact(CMD_RM_MAP, am_pl(SPI, 0, {{{0,0,4,0}}, {{0,1,5,0}}}));
        ck("[10d] both removed in one command SUCCESS", r_status(r), 0);
        ck("[10d] page1 empty again", same_maps(page(1), p1_before), 1);
    }

    printf("\n----------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
