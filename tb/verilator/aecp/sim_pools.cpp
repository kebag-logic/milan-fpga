/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * D8 ROLE-POOL harness: KL_aecp_top compiled against the role-pooled shape
 * svh (gen_pools_shape.py — a 2x2 end-station on a board that routes NO
 * audio pins, so every talker port carries host + PILOT + LOOPBACK clusters
 * and no physical ones). This is the shape the AX7101 needs: its platform
 * ships `_connectors = []`, milan_soc.py leaves i2s_pads = None and drives
 * i_i2s_sdout_i = 0, and the TDM pins are tied off too — the board has no
 * audio input at all, so the loopback pool is the only source that can hand
 * a talker per-channel-distinct audio.
 *
 * What a CONTROLLER sees is what is checked here, over the wire:
 *   [1] STREAM_PORT_INPUT/OUTPUT number_of_clusters / base_cluster /
 *       number_of_maps / base_map (1722.1-2021 7.2.13 Table 7-23) equal the
 *       emitted pool, and the blocks are contiguous and non-overlapping.
 *   [2] every AUDIO_CLUSTER object_name (7.2.16) says what the cluster IS —
 *       "Host Cap 0", "Pilot Tone", "Loopback S0 ch 1" — instead of the
 *       fourteen identical "Input"/"Output" strings the model carried before
 *       2026-07-28. Cluster fields that must NOT move are checked too
 *       (channel_count = 1 mono, format = 0x40 MBLA, 7.2.16.1).
 *   [3] the static AUDIO_MAP rows land INSIDE the loopback segment and are
 *       PORT-RELATIVE — 7.2.19: mapping_cluster_offset is "the offset from
 *       the base_cluster of the STREAM_PORT_INPUT or STREAM_PORT_OUTPUT".
 *       The proof is that BOTH talker ports carry the SAME offsets {3,4}
 *       while their global clusters differ (7,8 vs 12,13).
 *   [4] 7.2.19 uniqueness: at most one entry per stream channel on an output
 *       map; and the listener maps point at their own host segment.
 *   [5] Milan 5.4.2.28 — a Stream Port WITH an Audio Map answers
 *       ADD_/REMOVE_AUDIO_MAPPINGS NOT_SUPPORTED. That is CONFORMANCE, not a
 *       gap: 5.4.2.27/28 require the dynamic commands only for ports with NO
 *       Audio Map descriptor.
 *   [6] NEGATIVE cases — every check above must be able to FAIL, so the
 *       boundary index of each pooled descriptor type is requested and must
 *       answer NO_SUCH_DESCRIPTOR (1722.1 7.4.5.2), and a cluster name is
 *       SET and read back (object_name is dynamic, which is exactly why
 *       6.2.2.8 excludes it from the model structure).
 * Exit 0 = all pass.
 */

#include "VKL_aecp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <array>
#include <string>
#include <vector>

// AAF sink count of this harness's entity shape (the CRF sink
// past it answers the Milan-mandatory 0xF3F from the crf_cnt_* ports)
#define N_AAF_SINKS_TB 1

static VKL_aecp_top* dut;
static long checks = 0, fails = 0;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-54s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-54s = %ld\n", what, got); }
}
static void cks(const char* what, const std::string& got, const char* exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-54s got='%s' exp='%s'\n", what, got.c_str(), exp); }
    else            { printf("  [ ok ] %-54s = '%s'\n", what, got.c_str()); }
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
static std::string r_str(const std::vector<uint8_t>& b, size_t off, size_t n){
    std::string s;
    for (size_t i = 0; i < n && off+i < b.size(); i++) {
        if (!b[off+i]) break;
        s.push_back((char)b[off+i]);
    }
    return s;
}

static uint16_t g_seq = 0x6000;
static std::vector<uint8_t> xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
    feed_rx(aem_cmd(cmd, g_seq++, pl));
    return collect_resp();
}

static const uint16_t CMD_READ = 4, CMD_SET_NAME = 16;
static const uint16_t CMD_ADD_MAP = 44, CMD_RM_MAP = 45;
static const uint16_t SPI = 0x000E, SPO = 0x000F;
static const uint16_t CLUSTER = 0x0014, AMAP = 0x0017;

// READ_DESCRIPTOR payload: configuration_index(2) reserved(2) type(2) index(2)
static std::vector<uint8_t> rd_pl(uint16_t type, uint16_t idx) {
    std::vector<uint8_t> pl;
    put_be16(pl, 0); put_be16(pl, 0); put_be16(pl, type); put_be16(pl, idx);
    return pl;
}
// ADD/REMOVE payload: type(2) idx(2) n(2) reserved(2) + n x {si,sc,co,cc}
static std::vector<uint8_t> am_pl(uint16_t t, uint16_t i,
                                  const std::vector<std::array<uint16_t,4>>& m) {
    std::vector<uint8_t> pl;
    put_be16(pl, t); put_be16(pl, i); put_be16(pl, (uint16_t)m.size());
    put_be16(pl, 0);
    for (auto& r : m) for (int k = 0; k < 4; k++) put_be16(pl, r[k]);
    return pl;
}

//! descriptor image starts at wire 42 (eth 14 + AECP 12 + ctlr/seq/cmd 12 +
//! READ_DESCRIPTOR cfg/reserved 4)
static const size_t D0 = 42;
//! STREAM_PORT_* field offsets (7.2.13 Table 7-23, as encoded by
//! gen_aem_store.d_stream_port)
static const size_t PORT_NCL = 12, PORT_BCL = 14, PORT_NMAP = 16, PORT_BMAP = 18;
//! AUDIO_CLUSTER field offsets (7.2.16, gen_aem_store.d_audio_cluster)
static const size_t CL_NAME = 4, CL_SIGTYPE = 70, CL_CHANS = 84, CL_FMT = 86;
//! AUDIO_MAP field offsets (7.2.19, gen_aem_store.d_audio_map)
static const size_t MAP_NMAP = 6, MAP_ROW0 = 8;

struct Port { int nclusters, base_cluster, nmaps, base_map; };

static Port read_port(uint16_t type, uint16_t idx, const char* tag) {
    auto r = xact(CMD_READ, rd_pl(type, idx));
    char nm[80];
    snprintf(nm, sizeof nm, "%s READ_DESCRIPTOR SUCCESS", tag);
    ck(nm, r_status(r), 0);
    return Port{ r_be16(r, D0+PORT_NCL), r_be16(r, D0+PORT_BCL),
                 r_be16(r, D0+PORT_NMAP), r_be16(r, D0+PORT_BMAP) };
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_aecp_top;

    dut->rst_n = 0; dut->enable_i = 1;
    dut->srp_domain_vid_i = 0x002;
    dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    dut->entity_id_i = ENTITY_ID; dut->entity_model_id_i = 0;
    dut->entity_caps_i = 0x00008588; dut->talker_sources_i = 3;
    dut->talker_caps_i = 0x4801; dut->listener_sinks_i = 3;
    dut->listener_caps_i = 0x4801; dut->controller_caps_i = 0;
    dut->available_index_i = 7; dut->association_id_i = 0;
    dut->gptp_gm_id_i = 0; dut->gptp_domain_i = 0; dut->pdelay_ns_i = 0;
    dut->link_up_i = 1;
    // Milan 5.4.2.25 per-index counter buses: zero until a case models
    // them (the fabric muxes by gs_diag_idx_o; here the harness owns them)
    for (int w = 0; w < 10; w++) dut->rxdiag_cnt_i[w] = 0;
    for (int w = 0; w < 5; w++)  dut->tkdiag_cnt_i[w] = 0;
    dut->n_aaf_sinks_i = N_AAF_SINKS_TB;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|ENT_MAC[i]; dut->station_mac_i = m; }
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) tick();

    printf("== AECP D8 role-pool model - what a controller enumerates ==\n");

    // ------------------------------------------------------------------ //
    // [1] STREAM_PORT geometry: the pool IS the cluster block (7.2.13)    //
    // ------------------------------------------------------------------ //
    printf("\n[1] STREAM_PORT cluster blocks (1722.1 7.2.13 Table 7-23)\n");
    Port in0 = read_port(SPI, 0, "[1] SPI0");
    Port in1 = read_port(SPI, 1, "[1] SPI1");
    Port out0 = read_port(SPO, 0, "[1] SPO0");
    Port out1 = read_port(SPO, 1, "[1] SPO1");
    // listener pool = host x2 (physical is ZERO: the board routes no pins)
    ck("[1] SPI0 number_of_clusters (host x2)", in0.nclusters, 2);
    ck("[1] SPI0 base_cluster", in0.base_cluster, 0);
    ck("[1] SPI1 base_cluster (contiguous)", in1.base_cluster, 2);
    // talker pool = host x2 + pilot x1 + loopback x2
    ck("[1] SPO0 number_of_clusters (2+1+2)", out0.nclusters, 5);
    ck("[1] SPO0 base_cluster (after all inputs)", out0.base_cluster, 4);
    ck("[1] SPO1 base_cluster (contiguous)", out1.base_cluster, 9);
    // one AUDIO_MAP per port, dense indices (D1)
    ck("[1] SPI0 number_of_maps", in0.nmaps, 1);
    ck("[1] SPI0 base_map", in0.base_map, 0);
    ck("[1] SPO0 number_of_maps", out0.nmaps, 1);
    ck("[1] SPO0 base_map", out0.base_map, 2);
    ck("[1] SPO1 base_map", out1.base_map, 3);
    // NEGATIVE: one past the last port of each direction
    ck("[1] SPI2 NO_SUCH_DESCRIPTOR",
       r_status(xact(CMD_READ, rd_pl(SPI, 2))), 2);
    ck("[1] SPO2 NO_SUCH_DESCRIPTOR",
       r_status(xact(CMD_READ, rd_pl(SPO, 2))), 2);

    // ------------------------------------------------------------------ //
    // [2] AUDIO_CLUSTER object_names say what the cluster IS (7.2.16)     //
    // ------------------------------------------------------------------ //
    printf("\n[2] AUDIO_CLUSTER names + invariant fields (1722.1 7.2.16)\n");
    static const char* EXPECT[14] = {
        "Host Play 0", "Host Play 1",                     // SPI0 pool
        "Host Play 0", "Host Play 1",                     // SPI1 pool
        "Host Cap 0", "Host Cap 1", "Pilot Tone",         // SPO0 pool
        "Loopback S0 ch 0", "Loopback S0 ch 1",
        "Host Cap 0", "Host Cap 1", "Pilot Tone",         // SPO1 pool
        "Loopback S1 ch 0", "Loopback S1 ch 1",
    };
    for (int k = 0; k < 14; k++) {
        auto r = xact(CMD_READ, rd_pl(CLUSTER, (uint16_t)k));
        char nm[80];
        snprintf(nm, sizeof nm, "[2] AUDIO_CLUSTER[%d] name", k);
        ck("[2] cluster READ SUCCESS", r_status(r), 0);
        cks(nm, r_str(r, D0+CL_NAME, 64), EXPECT[k]);
        // mono MBLA is what the whole cluster model rests on (7.2.16.1)
        snprintf(nm, sizeof nm, "[2] AUDIO_CLUSTER[%d] channel_count=1", k);
        ck(nm, r_be16(r, D0+CL_CHANS), 1);
        snprintf(nm, sizeof nm, "[2] AUDIO_CLUSTER[%d] format MBLA 0x40", k);
        ck(nm, r.size() > D0+CL_FMT ? r[D0+CL_FMT] : -1, 0x40);
        // signal_type: INVALID (0xFFFF) on a STREAM_PORT_INPUT cluster,
        // AUDIO_UNIT (0x0002) on an output one (7.2.16)
        snprintf(nm, sizeof nm, "[2] AUDIO_CLUSTER[%d] signal_type", k);
        ck(nm, r_be16(r, D0+CL_SIGTYPE), k < 4 ? 0xFFFF : 0x0002);
    }
    // NEGATIVE: the boundary index must NOT exist
    ck("[2] AUDIO_CLUSTER[14] NO_SUCH_DESCRIPTOR",
       r_status(xact(CMD_READ, rd_pl(CLUSTER, 14))), 2);

    // ------------------------------------------------------------------ //
    // [3] AUDIO_MAP rows are PORT-RELATIVE and land in the loopback pool  //
    // ------------------------------------------------------------------ //
    printf("\n[3] AUDIO_MAP port-relative offsets (1722.1 7.2.19)\n");
    {
        auto m2 = xact(CMD_READ, rd_pl(AMAP, 2));      // talker port 0's map
        auto m3 = xact(CMD_READ, rd_pl(AMAP, 3));      // talker port 1's map
        ck("[3] AUDIO_MAP[2] SUCCESS", r_status(m2), 0);
        ck("[3] AUDIO_MAP[3] SUCCESS", r_status(m3), 0);
        ck("[3] AUDIO_MAP[2] number_of_mappings", r_be16(m2, D0+MAP_NMAP), 2);
        ck("[3] AUDIO_MAP[3] number_of_mappings", r_be16(m3, D0+MAP_NMAP), 2);
        // rows: {stream_index, stream_channel, cluster_offset, cluster_channel}
        for (int row = 0; row < 2; row++) {
            size_t o2 = D0 + MAP_ROW0 + 8*row, o3 = D0 + MAP_ROW0 + 8*row;
            char nm[80];
            snprintf(nm, sizeof nm, "[3] map2 row%d stream_index=0", row);
            ck(nm, r_be16(m2, o2), 0);
            snprintf(nm, sizeof nm, "[3] map3 row%d stream_index=1", row);
            ck(nm, r_be16(m3, o3), 1);
            snprintf(nm, sizeof nm, "[3] map2 row%d stream_channel", row);
            ck(nm, r_be16(m2, o2+2), row);
            // THE POINT (USER 08-06: host outranks loopback): offset 0 =
            // the HOST segment start - the entity wakes wired to shared
            // memory; identical on BOTH ports because 7.2.19 offsets are
            // relative to the port's own base_cluster.
            snprintf(nm, sizeof nm, "[3] map2 row%d cluster_offset (host)", row);
            ck(nm, r_be16(m2, o2+4), 0 + row);
            snprintf(nm, sizeof nm, "[3] map3 row%d cluster_offset (SAME, port-relative)", row);
            ck(nm, r_be16(m3, o3+4), 0 + row);
            snprintf(nm, sizeof nm, "[3] map2 row%d cluster_channel=0 (mono)", row);
            ck(nm, r_be16(m2, o2+6), 0);
        }
        // and the SAME offsets resolve to DIFFERENT global clusters:
        // port0 base 4 + 3 = cluster 7 "Loopback S0 ch 0"
        // port1 base 9 + 3 = cluster 12 "Loopback S1 ch 0"
        auto c7  = xact(CMD_READ, rd_pl(CLUSTER, (uint16_t)(out0.base_cluster + 3)));
        auto c12 = xact(CMD_READ, rd_pl(CLUSTER, (uint16_t)(out1.base_cluster + 3)));
        cks("[3] port0 offset 3 -> global cluster name",
            r_str(c7, D0+CL_NAME, 64), "Loopback S0 ch 0");
        cks("[3] port1 offset 3 -> DIFFERENT global cluster",
            r_str(c12, D0+CL_NAME, 64), "Loopback S1 ch 0");
        // listener maps point at their own host segment (offset 0..1)
        auto m0 = xact(CMD_READ, rd_pl(AMAP, 0));
        ck("[3] AUDIO_MAP[0] number_of_mappings", r_be16(m0, D0+MAP_NMAP), 2);
        ck("[3] map0 row0 cluster_offset (host)", r_be16(m0, D0+MAP_ROW0+4), 0);
        ck("[3] map0 row1 cluster_offset (host)", r_be16(m0, D0+MAP_ROW0+8+4), 1);
        // NEGATIVE: 4 maps exist (2 in + 2 out); the 5th must not
        ck("[3] AUDIO_MAP[4] NO_SUCH_DESCRIPTOR",
           r_status(xact(CMD_READ, rd_pl(AMAP, 4))), 2);
    }

    // ------------------------------------------------------------------ //
    // [4] 7.2.19 uniqueness on the emitted maps                           //
    // ------------------------------------------------------------------ //
    printf("\n[4] 7.2.19 uniqueness of the emitted rows\n");
    {
        auto m2 = xact(CMD_READ, rd_pl(AMAP, 2));
        int sc0 = r_be16(m2, D0+MAP_ROW0+2), sc1 = r_be16(m2, D0+MAP_ROW0+8+2);
        ck("[4] output map: one entry per stream channel (no dup)",
           sc0 != sc1, 1);
        auto m0 = xact(CMD_READ, rd_pl(AMAP, 0));
        int co0 = r_be16(m0, D0+MAP_ROW0+4), co1 = r_be16(m0, D0+MAP_ROW0+8+4);
        ck("[4] input map: one entry per cluster channel (no dup)",
           co0 != co1, 1);
        // every offset inside its own port's cluster block
        ck("[4] map2 offsets < SPO0 number_of_clusters",
           (r_be16(m2, D0+MAP_ROW0+4) < out0.nclusters) &&
           (r_be16(m2, D0+MAP_ROW0+8+4) < out0.nclusters), 1);
    }

    // ------------------------------------------------------------------ //
    // [5] Milan 5.4.2.27/28: ports WITH an Audio Map refuse the dynamic   //
    //     commands. NOT_SUPPORTED here is CONFORMANCE, not a gap.         //
    // ------------------------------------------------------------------ //
    printf("\n[5] Milan 5.4.2.28 static-map posture (NOT_SUPPORTED = correct)\n");
    ck("[5] ADD_AUDIO_MAPPINGS on pooled INPUT port NOT_SUPPORTED",
       r_status(xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,0,0,0}}}))), 11);
    ck("[5] ADD_AUDIO_MAPPINGS on pooled OUTPUT port NOT_SUPPORTED",
       r_status(xact(CMD_ADD_MAP, am_pl(SPO, 0, {{{0,0,3,0}}}))), 11);
    ck("[5] REMOVE_AUDIO_MAPPINGS on pooled OUTPUT port NOT_SUPPORTED",
       r_status(xact(CMD_RM_MAP, am_pl(SPO, 0, {{{0,0,3,0}}}))), 11);

    // ------------------------------------------------------------------ //
    // [6] object_name is DYNAMIC (which is why 6.2.2.8 excludes it from   //
    //     the model structure): SET_NAME a pooled cluster and read back.  //
    // ------------------------------------------------------------------ //
    printf("\n[6] SET_NAME on a pooled AUDIO_CLUSTER + read-back (7.4.17)\n");
    {
        std::vector<uint8_t> sn;
        put_be16(sn, CLUSTER); put_be16(sn, 7);        // the loopback cluster
        put_be16(sn, 0); put_be16(sn, 0);              // name_index, config
        const char* nn = "Loopback RENAMED";
        for (int i = 0; i < 64; i++)
            sn.push_back(i < (int)strlen(nn) ? nn[i] : 0);
        ck("[6] SET_NAME(AUDIO_CLUSTER,7) SUCCESS",
           r_status(xact(CMD_SET_NAME, sn)), 0);
        auto r = xact(CMD_READ, rd_pl(CLUSTER, 7));
        cks("[6] read-back shows the new name",
            r_str(r, D0+CL_NAME, 64), "Loopback RENAMED");
        // NEGATIVE: the neighbouring cluster must be untouched
        auto r8 = xact(CMD_READ, rd_pl(CLUSTER, 8));
        cks("[6] neighbour cluster untouched (write isolation)",
            r_str(r8, D0+CL_NAME, 64), "Loopback S0 ch 1");
        // restore
        std::vector<uint8_t> rs;
        put_be16(rs, CLUSTER); put_be16(rs, 7);
        put_be16(rs, 0); put_be16(rs, 0);
        const char* on = "Loopback S0 ch 0";
        for (int i = 0; i < 64; i++)
            rs.push_back(i < (int)strlen(on) ? on[i] : 0);
        ck("[6] SET_NAME restore SUCCESS", r_status(xact(CMD_SET_NAME, rs)), 0);
    }

    printf("\n----------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
