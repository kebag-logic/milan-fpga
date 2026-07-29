/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * GET_AUDIO_MAP on the SHIP SHAPE - the port-relative bounds of 1722.1-2021
 * 7.2.19, and the descriptor over-read that broke them (defect A).
 *
 * LEVEL: L0 (the AECP responder in isolation) shaped to an L4 property - what
 *   an independent controller sees when it enumerates ports and asks each one
 *   for its map.
 *
 * ORACLE: the entity's OWN descriptor set, read back through READ_DESCRIPTOR.
 *   Not a second declaration of the shape and not this harness's idea of it:
 *   for every port, THE PORT'S OWN STREAM_PORT descriptor supplies base_map,
 *   number_of_clusters and base_cluster, and THAT AUDIO_MAP descriptor
 *   supplies the mapping bytes GET_AUDIO_MAP must answer with.
 *
 * THE CLAUSES, QUOTED (the standards are on this machine at
 * /home/alex/standards; earlier rounds paraphrased them because
 * $STANDARDS_DIR was unset and the text was believed unavailable):
 *
 *   IEEE Std 1722.1-2021, Table 7-33 / Table 7-162, mapping_cluster_offset:
 *     "The offset from the base_cluster of the STREAM_PORT_INPUT or
 *      STREAM_PORT_OUTPUT for mapping[0]."
 *     -> the offsets are PORT-RELATIVE. Section [3] and [5].
 *
 *   IEEE Std 1722.1-2021, 7.2.19 (STREAM_PORT_INPUT paragraph):
 *     "There is at most one entry for each mapping_cluster_offset and
 *      mapping_cluster_channel, but there may be multiple entries for each
 *      mapping_stream_index and mapping_stream_channel."
 *     ...and the OUTPUT paragraph swaps the two halves, which is why the
 *     model gate checks a DIFFERENT rule per direction.
 *
 *   IEEE Std 1722.1-2021, 7.2.19:
 *     "The mappings field is variable length data and shall be accessed by
 *      using the mappings_offset field as any fields added in the future will
 *      be added before the mappings field."
 *     -> section [1] reads mappings_offset instead of assuming 8.
 *
 *   IEEE Std 1722.1-2021, 7.4.44.1:
 *     "If the map_index is beyond the range of available maps then it returns
 *      a BAD_ARGUMENT status in the response."
 *     -> section [6]. This arm used to answer NO_SUCH_DESCRIPTOR.
 *
 *   IEEE Std 1722.1-2021, 7.4.44.2:
 *     "The number_of_mappings field is set to the number of mappings
 *      contained in the mappings field."
 *     -> sections [2] and [4]: the count is not a constant, it is a statement
 *     about the bytes that follow, and it has to be true of them.
 *
 *   Milan Specification v1.2, 5.4.2.26 GET_AUDIO_MAP:
 *     "For each Stream Port Input and for each Stream Port Output that has no
 *      Audio Map, the PAAD-AE shall implement the GET_AUDIO_MAP command as
 *      specified in [ATDECC, Clause 7.4.44]. If a PAAD-AE receives a
 *      GET_AUDIO_MAP command for a Stream Port Output that has Audio Map(s),
 *      the PAAD-AE shall reply with the NOT_SUPPORTED error code."
 *     -> our STREAM_PORT_OUTPUTs DO carry Audio Map descriptors, so the
 *     conformant answer on all eight of them is NOT_SUPPORTED. That is both
 *     the Milan rule AND the end of the over-read, since the port that
 *     over-read is an output port. Section [2].
 *
 *   IEEE Std 1722-2016, 4.4.5.4:
 *     "The 11-bit control_data_length field contains the length (in octets)
 *      of the control_data_payload field."
 *     The control AVTPDU puts stream_id (here target_entity_id) at octets
 *     4..11, so control_data_payload starts at octet 12 and cdl = 12 +
 *     message-specific payload, with the frame 14 + 12 + cdl. Sections [2]
 *     and [6] assert both.
 *
 * WHY THIS SHAPE AND NOT THE DEPLOYED 1x1 ONE. At the 1x1 arty_current shape
 *   AUDIO_MAP[1] IS the output port's map and holds 8 mappings, so the
 *   pre-fix constants (descriptor index 1, 8 mappings, 64 bytes) were
 *   accidentally correct and sim_main's section [18] passed. The defect is
 *   only representable where the AUDIO_MAP indices and the port indices stop
 *   coinciding - the 8x8 ship shape, where the 8 input ports own AUDIO_MAP
 *   0..7 and the 8 output ports own AUDIO_MAP 8..15.
 *
 * NEGATIVE CONTROL (methodology R2), measured 2026-07-28. Build this file
 *   against the pre-fix KL_aecp_response_builder and 48 of its 218 checks
 *   fail, split 37 STREAM_PORT_INPUT + 11 STREAM_PORT_OUTPUT:
 *     - all 8 "OUTPUT NOT_SUPPORTED (Milan 5.4.2.26)" fail. Port 0 failed by
 *       SERVING - with number_of_mappings 8 where its descriptor says 2, cdl
 *       88 where 12+12+8*2 = 40, and 48 octets read past the end of a
 *       24-octet descriptor, which IS the over-read; ports 1..7 failed by
 *       answering NO_SUCH_DESCRIPTOR, the wrong refusal.
 *     - 7 input ports (1..7) fail "SUCCESS": the pre-fix arm answered port
 *       index 0 only, so 7 of the 8 ports READ_DESCRIPTOR serves refused
 *       their own dynamic-info command - the same self-contradiction Hive
 *       reported 8+7 times for GET_STREAM_INFO, one command over. Their
 *       number_of_maps / number_of_mappings / cdl / served-bytes checks fail
 *       with them.
 *     - both map_index-out-of-range checks fail: the arm answered
 *       NO_SUCH_DESCRIPTOR where 7.4.44.1 says BAD_ARGUMENT.
 *   The output-port failures are the same defect tb/tools/hive_compliance.py
 *   C9 measured on gateware 0x0001_0016 on 2026-07-28 against the real board
 *   (8 mappings, cluster_offset 0..7, on a port declaring 2 clusters).
 *
 * MEASURED ON SILICON, and what it cost: the response carried 64 bytes of
 *   mapping region out of a descriptor holding 16, so 40 octets of whatever
 *   followed AUDIO_MAP[1] in the descriptor ROM went on the wire to any
 *   controller that asked. Section [4] is the check that would notice that -
 *   it compares the served bytes against the descriptor's own bytes rather
 *   than against a constant, so bytes from beyond the descriptor cannot pass.
 */
#include "VKL_aecp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
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
    if (got != exp) { fails++; printf("  [FAIL] %-58s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-58s = %ld\n", what, got); }
}

static const uint8_t ENT_MAC[6] = {0x02,0x00,0x00,0xff,0xfe,0x01};
static const uint8_t CTL_MAC[6] = {0x68,0x05,0xca,0x95,0xb2,0xd1};
static const uint64_t ENTITY_ID = 0x0200'00ff'fe00'0001ULL;
static const uint64_t CTLR_ID   = 0x6805'ca95'b2d1'0000ULL;
static const uint64_t STA_MAC   = 0x0200'00ff'fe01ULL;
static const uint64_t DMAC_BASE = 0x91E0'F000'FE01ULL;

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

static std::vector<uint8_t> collect_resp(int budget = 20000) {
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
            if (++idle > 2000) return b;
        }
    }
    return b;
}

static int r_status(const std::vector<uint8_t>& b){ return b.size()>16 ? (b[16]>>3)&0x1F : -1; }
static int r_cdl(const std::vector<uint8_t>& b) {
    return b.size()>17 ? (((b[16]&0x7)<<8) | b[17]) : -1;
}
static long be_at(const std::vector<uint8_t>& b, size_t off, int n) {
    if (b.size() < off + (size_t)n) return -1;      // MISSING is never 0
    long v = 0;
    for (int i = 0; i < n; i++) v = (v << 8) | b[off + i];
    return v;
}

static uint16_t seq = 0x7000;
static std::vector<uint8_t> xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
    feed_rx(aem_cmd(cmd, seq++, pl));
    return collect_resp();
}
static std::vector<uint8_t> rd_pl(uint16_t type, uint16_t idx) {
    std::vector<uint8_t> p; put_be16(p, 0); put_be16(p, 0);
    put_be16(p, type); put_be16(p, idx); return p;
}
static std::vector<uint8_t> am_pl(uint16_t type, uint16_t idx, uint16_t map) {
    std::vector<uint8_t> p; put_be16(p, type); put_be16(p, idx);
    put_be16(p, map); put_be16(p, 0); return p;
}

static const uint16_t CMD_READ_DESC    = 0x0004;
static const uint16_t CMD_GET_AUDIO_MAP = 0x002B;   // 1722.1-2021 7.4.44
static const uint16_t D_SP_IN = 0x000E, D_SP_OUT = 0x000F;
static const uint16_t D_AUDIO_MAP = 0x0017, D_AUDIO_CLUSTER = 0x0014;

//! wire offset of the descriptor inside a READ_DESCRIPTOR response:
//! 38 (AEM payload) + configuration_index(2) + reserved(2)
static const int O_DESC = 42;
//! GET_AUDIO_MAP response payload (7.4.44.2), from wire byte 38:
//! descriptor_type(2) descriptor_index(2) map_index(2)
//! number_of_maps(2) number_of_mappings(2) reserved(2), then the mappings
static const int O_NMAPS = 44, O_NMAPPINGS = 46, O_ROWS = 50;

//! STREAM_PORT descriptor field offsets (7.2.13): number_of_clusters at 12,
//! base_cluster at 14, number_of_maps at 16, base_map at 18
static const int SP_NCLUST = 12, SP_BASECL = 14, SP_NMAPS = 16, SP_BASEMAP = 18;
//! AUDIO_MAP descriptor (7.2.19): mappings_offset at 4, number_of_mappings
//! at 6, then number_of_mappings x 8-octet rows
static const int AM_OFF = 4, AM_N = 6, AM_ROWS = 8;
//! AUDIO_CLUSTER channel_count (7.2.16) at descriptor offset 84: type(2)
//! index(2) object_name(64) localized_description(2) signal_type(2)
//! signal_index(2) signal_output(2) path_latency(4) block_latency(4). Offset
//! 70 is signal_type, which reads 0xFFFF on an input cluster and 0x0002 on an
//! output one - both wide enough that a "cluster_channel < it" check passes
//! vacuously. This offset is CHECKED below rather than trusted.
static const int AC_CHANNELS = 84;

static const int N_PORTS = 8;      // 8x8 ship shape, both directions

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_aecp_top;

    dut->rst_n = 0; dut->enable_i = 1;
    dut->srp_domain_vid_i = 0x002;
    dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    dut->entity_id_i = ENTITY_ID; dut->entity_model_id_i = 0;
    dut->entity_caps_i = 0x00008588; dut->talker_sources_i = 9;
    dut->talker_caps_i = 0x4801; dut->listener_sinks_i = 9;
    dut->listener_caps_i = 0x4801; dut->controller_caps_i = 0;
    dut->available_index_i = 7; dut->association_id_i = 0;
    dut->gptp_gm_id_i = 0; dut->gptp_domain_i = 0; dut->pdelay_ns_i = 0;
    dut->link_up_i = 1;
    // Milan 5.4.2.25 per-index counter buses: zero until a case models
    // them (the fabric muxes by gs_diag_idx_o; here the harness owns them)
    for (int w = 0; w < 10; w++) dut->rxdiag_cnt_i[w] = 0;
    for (int w = 0; w < 5; w++)  dut->tkdiag_cnt_i[w] = 0;
    dut->n_aaf_sinks_i = N_AAF_SINKS_TB;
    dut->station_mac_i = STA_MAC;
    dut->aaf_dmac_i = DMAC_BASE;
    dut->aaf_vid_i  = 2;
    dut->talker_active_i = 0; dut->listener_observed_i = 0;
    dut->lstn_bound_i = 0; dut->lstn1_bound_i = 0;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) tick();

    printf("== GET_AUDIO_MAP port-relative bounds on the 8x8 ship shape "
           "(defect A) ==\n");

    // ------------------------------------------------------------------ //
    // [1] The oracle: every port's OWN descriptor, and the AUDIO_MAP its
    //     own base_map names. Everything after this is compared to THIS.
    // ------------------------------------------------------------------ //
    printf("\n[1] port descriptors and the AUDIO_MAP each one's base_map "
           "names (READ_DESCRIPTOR, 1722.1 7.4.5 / 7.2.13)\n");
    struct Port {
        int nclust, basecl, nmaps, basemap;
        int desc_n;                       // AUDIO_MAP's own number_of_mappings
        int moff;                         // its own mappings_offset (7.2.19)
        std::vector<uint8_t> rows;        // its mapping bytes, verbatim
    };
    Port P[2][N_PORTS];
    const uint16_t PT[2]    = { D_SP_IN, D_SP_OUT };
    const char*    PNAME[2] = { "STREAM_PORT_INPUT", "STREAM_PORT_OUTPUT" };
    for (int d = 0; d < 2; d++) {
        for (int i = 0; i < N_PORTS; i++) {
            auto r = xact(CMD_READ_DESC, rd_pl(PT[d], i));
            char nm[110];
            snprintf(nm, sizeof nm, "READ_DESCRIPTOR(%s,%d) SUCCESS", PNAME[d], i);
            ck(nm, r_status(r), 0);
            Port& p = P[d][i];
            p.nclust  = be_at(r, O_DESC + SP_NCLUST,  2);
            p.basecl  = be_at(r, O_DESC + SP_BASECL,  2);
            p.nmaps   = be_at(r, O_DESC + SP_NMAPS,   2);
            p.basemap = be_at(r, O_DESC + SP_BASEMAP, 2);
            // 7.2.13: a port with static maps declares number_of_maps >= 1
            snprintf(nm, sizeof nm, "%s.%d declares number_of_maps 1", PNAME[d], i);
            ck(nm, p.nmaps, 1);
            // ...and THAT map descriptor is the oracle for what it must serve
            auto m = xact(CMD_READ_DESC, rd_pl(D_AUDIO_MAP, p.basemap));
            snprintf(nm, sizeof nm, "READ_DESCRIPTOR(AUDIO_MAP,%d) SUCCESS "
                     "(%s.%d base_map)", p.basemap, PNAME[d], i);
            ck(nm, r_status(m), 0);
            p.desc_n = be_at(m, O_DESC + AM_N, 2);
            // 7.2.19: the mappings "shall be accessed by using the
            // mappings_offset field"; Table 7-32 says "This field is 8 for
            // this version of AEM". Read it, then check it is that 8 - the
            // rows below are located with the value READ, not the constant.
            p.moff = be_at(m, O_DESC + AM_OFF, 2);
            snprintf(nm, sizeof nm, "AUDIO_MAP[%d] mappings_offset 8 "
                     "(Table 7-32, this version of AEM)", p.basemap);
            ck(nm, p.moff, AM_ROWS);
            // Table 7-32: "The maximum value of this field is 62 for this
            // version of AEM."
            snprintf(nm, sizeof nm, "AUDIO_MAP[%d] number_of_mappings <= 62",
                     p.basemap);
            ck(nm, (long)(p.desc_n <= 62), 1);
            // DEFECT B's shape at the descriptor tier: the descriptor must
            // actually HOLD the mappings it declares. A controller that
            // trusts the count and reads past the end is the over-read.
            snprintf(nm, sizeof nm, "AUDIO_MAP[%d] holds the %d mappings it "
                     "declares", p.basemap, p.desc_n);
            ck(nm, (long)(m.size() >= (size_t)(O_DESC + p.moff + 8 * p.desc_n)), 1);
            p.rows.assign(m.begin() + O_DESC + p.moff,
                          m.begin() + O_DESC + p.moff + 8 * p.desc_n);
        }
    }

    // ------------------------------------------------------------------ //
    // [2] Milan v1.2 5.4.2.26 splits this command BY DIRECTION:
    //       "For each Stream Port Input and for each Stream Port Output that
    //        has no Audio Map, the PAAD-AE shall implement the GET_AUDIO_MAP
    //        command as specified in [ATDECC, Clause 7.4.44]. If a PAAD-AE
    //        receives a GET_AUDIO_MAP command for a Stream Port Output that
    //        has Audio Map(s), the PAAD-AE shall reply with the NOT_SUPPORTED
    //        error code."
    //     Every output port of this shape HAS an Audio Map (section [1]
    //     proved number_of_maps = 1 and read the descriptor), so all eight
    //     must refuse - and refusing is also what ends the over-read, since
    //     the port that over-read was an output port.
    //     Input ports must serve, and must serve THEIR OWN count.
    // ------------------------------------------------------------------ //
    printf("\n[2] Milan 5.4.2.26: inputs serve their OWN map, outputs WITH a "
           "map answer NOT_SUPPORTED\n");
    std::vector<uint8_t> GOT[2][N_PORTS];
    for (int d = 0; d < 2; d++) {
        for (int i = 0; i < N_PORTS; i++) {
            Port& p = P[d][i];
            auto r = xact(CMD_GET_AUDIO_MAP, am_pl(PT[d], i, 0));
            GOT[d][i] = r;
            char nm[120];
            if (d == 1) {
                snprintf(nm, sizeof nm, "GET_AUDIO_MAP(%s,%d) NOT_SUPPORTED "
                         "(Milan 5.4.2.26, port HAS Audio Map)", PNAME[d], i);
                ck(nm, r_status(r), 11);
                // the refusal still keeps the 7.4.44.2 12-octet payload
                snprintf(nm, sizeof nm, "GET_AUDIO_MAP(%s,%d) refusal cdl 24",
                         PNAME[d], i);
                ck(nm, r_cdl(r), 24);
                snprintf(nm, sizeof nm, "GET_AUDIO_MAP(%s,%d) refusal carries "
                         "no mappings", PNAME[d], i);
                ck(nm, be_at(r, O_NMAPPINGS, 2), 0);
                continue;
            }
            // a descriptor READ_DESCRIPTOR serves must answer its own
            // dynamic-info command (the C2/C6 self-consistency rule)
            snprintf(nm, sizeof nm, "GET_AUDIO_MAP(%s,%d,0) SUCCESS", PNAME[d], i);
            ck(nm, r_status(r), 0);
            snprintf(nm, sizeof nm, "GET_AUDIO_MAP(%s,%d) number_of_maps 1", PNAME[d], i);
            ck(nm, be_at(r, O_NMAPS, 2), 1);
            snprintf(nm, sizeof nm, "GET_AUDIO_MAP(%s,%d) number_of_mappings "
                     "== descriptor's %d", PNAME[d], i, p.desc_n);
            ck(nm, be_at(r, O_NMAPPINGS, 2), p.desc_n);
            // IEEE 1722-2016 4.4.5.4: "The 11-bit control_data_length field
            // contains the length (in octets) of the control_data_payload
            // field." The control AVTPDU puts stream_id (target_entity_id)
            // at octets 4..11, so the payload starts at octet 12 and cdl =
            // controller_entity_id(8) + sequence_id(2) + command_type(2) +
            // message payload = 12 + payload; 7.4.44.2 fixes that payload at
            // 12 + 8*number_of_mappings. Cross-checked on the reference
            // device: GET_STREAM_INFO's 56 B payload reads cdl 68.
            snprintf(nm, sizeof nm, "GET_AUDIO_MAP(%s,%d) cdl 12+12+8*%d",
                     PNAME[d], i, p.desc_n);
            ck(nm, r_cdl(r), 12 + 12 + 8 * p.desc_n);
            // ...and the frame really carries it: 14 (Ethernet) + 12 + cdl.
            // Short frames are what a strict controller drops however right
            // the status byte is.
            snprintf(nm, sizeof nm, "GET_AUDIO_MAP(%s,%d) frame is as long as "
                     "it claims", PNAME[d], i);
            ck(nm, (long)(r.size() >= (size_t)(26 + r_cdl(r))), 1);
        }
    }

    // ------------------------------------------------------------------ //
    // [3] The 7.2.19 bounds, asserted per FIELD against the descriptor that
    //     bounds it. This is the property, not a status byte (methodology
    //     R4): each of the four mapping fields has a DIFFERENT owner.
    // ------------------------------------------------------------------ //
    printf("\n[3] every mapping is inside its OWN port's bounds (Table 7-33: "
           "\"The offset from the base_cluster of the STREAM_PORT_INPUT or "
           "STREAM_PORT_OUTPUT\")\n");
    for (int d = 0; d < 1; d++) {   // outputs refuse (Milan 5.4.2.26)
        for (int i = 0; i < N_PORTS; i++) {
            Port& p = P[d][i];
            auto& r = GOT[d][i];
            long n = be_at(r, O_NMAPPINGS, 2);
            long bad_off = 0, bad_ch = 0, bad_si = 0;
            for (long k = 0; k < n; k++) {
                long si = be_at(r, O_ROWS + 8*k + 0, 2);
                long co = be_at(r, O_ROWS + 8*k + 4, 2);
                long cc = be_at(r, O_ROWS + 8*k + 6, 2);
                // cluster_offset < the ANSWERING port's number_of_clusters.
                // Bounding it by anything else - a global cluster count, the
                // other direction's port, a constant - is what let 0..7 out
                // of a 2-cluster port look fine everywhere else.
                if (co < 0 || co >= p.nclust) bad_off++;
                // cluster_channel < channel_count of AUDIO_CLUSTER
                // [base_cluster + cluster_offset] (7.2.16)
                if (co >= 0 && co < p.nclust) {
                    auto c = xact(CMD_READ_DESC,
                                  rd_pl(D_AUDIO_CLUSTER, p.basecl + co));
                    // a cluster that does not answer is a FAILURE, not a
                    // skip: an unreadable bound is an unasserted bound
                    // (methodology R5, a structural zero is not a
                    // measurement). This is exactly how the bound was dead
                    // in tb/tools/hive_compliance.py C9, which addressed
                    // AUDIO_CLUSTER as 0x0016 (SENSOR_CLUSTER) and therefore
                    // never read one.
                    long chans = (r_status(c) == 0)
                               ? be_at(c, O_DESC + AC_CHANNELS, 2) : -1;
                    if (chans < 1 || cc < 0 || cc >= chans) bad_ch++;
                }
                // stream_index < the stream descriptors this direction has
                if (si < 0 || si >= 9) bad_si++;
            }
            char nm[110];
            snprintf(nm, sizeof nm, "%s.%d: cluster_offset < its own "
                     "number_of_clusters %d", PNAME[d], i, p.nclust);
            ck(nm, bad_off, 0);
            snprintf(nm, sizeof nm, "%s.%d: cluster_channel < that cluster's "
                     "channel_count", PNAME[d], i);
            ck(nm, bad_ch, 0);
            snprintf(nm, sizeof nm, "%s.%d: stream_index addresses a stream "
                     "that exists", PNAME[d], i);
            ck(nm, bad_si, 0);
        }
    }

    // ------------------------------------------------------------------ //
    // [4] THE OVER-READ CHECK. The served mapping region must be the
    //     descriptor's own bytes - not a prefix of them, not a constant
    //     number of them, and above all not bytes from past its end. A
    //     bounds check alone would have missed this if the neighbouring
    //     descriptor happened to hold in-range numbers.
    // ------------------------------------------------------------------ //
    printf("\n[4] the served bytes ARE the port's own AUDIO_MAP bytes "
           "(the 48-octet over-read, silicon 2026-07-28)\n");
    for (int d = 0; d < 1; d++) {   // outputs refuse (Milan 5.4.2.26)
        for (int i = 0; i < N_PORTS; i++) {
            Port& p = P[d][i];
            auto& r = GOT[d][i];
            long diff = 0;
            for (size_t k = 0; k < p.rows.size(); k++) {
                size_t w = O_ROWS + k;
                if (w >= r.size() || r[w] != p.rows[k]) diff++;
            }
            // ...and NOTHING beyond them: a response longer than the
            // descriptor's own mapping region is carrying ROM that does not
            // belong to this port.
            long extra = (long)r.size() - (long)(O_ROWS + p.rows.size());
            char nm[110];
            snprintf(nm, sizeof nm, "%s.%d served rows == AUDIO_MAP[%d] bytes",
                     PNAME[d], i, p.basemap);
            ck(nm, diff, 0);
            snprintf(nm, sizeof nm, "%s.%d serves NO byte past its own map",
                     PNAME[d], i);
            ck(nm, extra <= 0 ? 0 : extra, 0);
        }
    }

    // ------------------------------------------------------------------ //
    // [5] Two ports carrying the SAME port-relative offsets onto DIFFERENT
    //     global clusters - the 7.2.19 property that makes every
    //     declaration-vs-declaration comparison blind to defect A. If the
    //     offsets were global these would have to differ.
    // ------------------------------------------------------------------ //
    printf("\n[5] different ports, same port-relative offsets, different "
           "global clusters (Table 7-33)\n");
    {
        long o00 = be_at(GOT[0][0], O_ROWS + 4, 2);
        long o10 = be_at(GOT[0][1], O_ROWS + 4, 2);
        ck("INPUT.0 and INPUT.1 publish the SAME first offset", o00, o10);
        ck("...onto DIFFERENT global clusters (base_cluster differs)",
           (long)(P[0][0].basecl != P[0][1].basecl), 1);
        // and the two global clusters they resolve to really are different -
        // the property a global-index model would collapse
        ck("INPUT.0 and INPUT.1 resolve offset 0 to different clusters",
           (long)((P[0][0].basecl + o00) != (P[0][1].basecl + o10)), 1);
    }

    // ------------------------------------------------------------------ //
    // [6] Refusals. A port index past the shape and a map_index past
    //     number_of_maps are both refused, and the refusal still carries the
    //     7.4.44.2 12-byte floor (lane 3's D2 rule: a non-success response
    //     keeps the response's shape). map_index paging: 7.4.44.1.
    // ------------------------------------------------------------------ //
    printf("\n[6] refusals: the right STATUS, and the 7.4.44.2 12 B floor\n");
    {
        // 7.4.44.1: "If the map_index is beyond the range of available maps
        // then it returns a BAD_ARGUMENT status in the response." A port
        // whose number_of_maps is 1 has exactly one index in range, 0 - so
        // map_index 1 is BAD_ARGUMENTS (7), not NO_SUCH_DESCRIPTOR (2),
        // which is what this arm used to answer. Status values are AEM
        // Table 7-127: SUCCESS 0, NO_SUCH_DESCRIPTOR 2, BAD_ARGUMENTS 7,
        // NOT_SUPPORTED 11 (read from hdl/ieee17221/aecp/aecp_pkg.sv, which
        // is the same table the responder encodes).
        struct { uint16_t t; uint16_t i; uint16_t m; int st; const char* why; } BAD[] = {
            { D_SP_IN,  N_PORTS, 0, 2, "port index past the shape (INPUT)"  },
            { D_SP_OUT, N_PORTS, 0, 2, "port index past the shape (OUTPUT)" },
            { D_SP_IN,  0,       1, 7, "map_index 1 on a number_of_maps=1 INPUT port" },
            { D_SP_OUT, 0,       1, 11, "map_index 1 on an OUTPUT port with a map" },
            { 0x0006,   0,       0, 2, "STREAM_OUTPUT is not a STREAM_PORT" },
        };
        for (auto& b : BAD) {
            auto r = xact(CMD_GET_AUDIO_MAP, am_pl(b.t, b.i, b.m));
            char nm[120];
            snprintf(nm, sizeof nm, "%s -> status %d", b.why, b.st);
            ck(nm, r_status(r), b.st);
            snprintf(nm, sizeof nm, "%s cdl 24 (12 B payload)", b.why);
            ck(nm, r_cdl(r), 24);
            snprintf(nm, sizeof nm, "%s frame >= 26+24", b.why);
            ck(nm, (long)(r.size() >= 50), 1);
        }
    }

    printf("\n----------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
