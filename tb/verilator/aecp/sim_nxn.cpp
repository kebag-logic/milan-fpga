/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * GET_STREAM_INFO across the SHIP SHAPE (defects D1 + D2).
 *
 * LEVEL: L0 (the AECP responder in isolation) shaped to an L3/L4 property.
 * ORACLE: the clause (IEEE 1722.1-2021 7.4.5 / 7.4.16.2 / 7.4.42.2 / 7.4.44.2,
 *   Milan v1.2 7.3.10) for the sizes, and for D1 the entity's OWN descriptor
 *   directory as observed through READ_DESCRIPTOR - not a second declaration
 *   of the shape, but the answer the other command actually gives on the wire.
 *   Every size expectation here is additionally MEASURED on the Milan-
 *   validated reference device 3CC0C60102030000 (2026-07-28) rather than
 *   pattern-matched from our own behaviour.
 * NEGATIVE CONTROL: build this file against the pre-fix response builder and
 *   173 of its 294 checks fail, split 8 STREAM_OUTPUT + 7 STREAM_INPUT on the
 *   D1 comparison - the exact split Hive reported against silicon.
 *
 * Built against the TRACKED 8x8 config svh
 * (configs/generated/endstation_ax7101_8x8/gen/aecp_aem_rom.svh) — the exact
 * descriptor set the AX7101 gateware carries: 9 STREAM_INPUT (8 AAF + CRF)
 * and 9 STREAM_OUTPUT (8 AAF + CRF). The other two AECP harnesses build 1x1
 * and 1x3 shapes, which is precisely why neither could see either defect.
 *
 * WHAT IS PROVEN HERE, and where it came from (silicon 2026-07-27, gateware
 * 0x0001_0016, Hive + tb/tools/hive_compliance.py against the board):
 *
 *  D1  READ_DESCRIPTOR served STREAM_OUTPUT.0-8 and STREAM_INPUT.0-8
 *      byte-exact and GET_STREAM_INFO answered NO_SUCH_DESCRIPTOR on 1-8
 *      (Hive: 8x STREAM_OUTPUT + 7x STREAM_INPUT). The device contradicted
 *      itself between two commands about the same descriptor. Section [2]
 *      re-implements that comparison as a TB check: for EVERY index, the
 *      two commands must agree on whether the descriptor exists.
 *
 *  D2  A non-success AEM response must still carry the full response
 *      payload. We answered NO_SUCH_DESCRIPTOR with control_data_length 16
 *      where the success response is 68, and Hive logged "Received an
 *      invalid non-success GET_STREAM_INFO AEM response (Incorrect payload
 *      size)" 15 times, continuing only because it was built with
 *      IGNORE_INVALID_NON_SUCCESS_AEM_RESPONSES. The rule is taken from the
 *      controller stack that raises that line — L-Acoustics avdecc
 *      src/protocol/protocolAemPayloads.cpp checkResponsePayload():
 *        status == NOT_IMPLEMENTED -> response REFLECTS THE COMMAND;
 *        any other status          -> response carries the FULL response
 *                                     payload for that command.
 *      Clause: GET_STREAM_INFO Response = IEEE 1722.1-2013/-2021 §7.4.16.2,
 *      Milan v1.2 §7.3.10 fixes it at 56 B -> cdl 68. Every probe below
 *      asserts BOTH the declared control_data_length AND the number of
 *      bytes that actually arrived, because a cdl-only check cannot see a
 *      frame that is shorter than it claims (which is what SET/GET_NAME's
 *      lock path did) and a status-only check cannot see D2 at all.
 *
 * Negative controls are deliberate throughout: out-of-range indices, a
 * descriptor type that EXISTS but is not a stream, an unknown command (the
 * one status that must keep reflecting the command), and a bind-isolation
 * check that the live sink-0 record does not leak into sinks 1..7.
 */

#include "VKL_aecp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>

// AAF sink count of this harness's entity shape (the CRF sink
// past it answers the empty mask)
#define N_AAF_SINKS_TB 8

static VKL_aecp_top* dut;
static long checks = 0, fails = 0;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-52s = %ld\n", what, got); }
}
static void ckh(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=0x%llX exp=0x%llX\n", what,
                                      (unsigned long long)got, (unsigned long long)exp); }
    else            { printf("  [ ok ] %-52s = 0x%llX\n", what, (unsigned long long)got); }
}

static const uint8_t ENT_MAC[6] = {0x02,0x00,0x00,0xff,0xfe,0x01};
static const uint8_t CTL_MAC[6] = {0x68,0x05,0xca,0x95,0xb2,0xd1};
static const uint64_t ENTITY_ID = 0x0200'00ff'fe00'0001ULL;
static const uint64_t CTLR_ID   = 0x6805'ca95'b2d1'0000ULL;
static const uint64_t STA_MAC   = 0x0200'00ff'fe01ULL;   // = ENT_MAC
static const uint64_t DMAC_BASE = 0x91E0'F000'FE01ULL;   // MAAP block base

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
static uint64_t be_at(const std::vector<uint8_t>& b, size_t off, int n) {
    if (b.size() < off + (size_t)n) return 0xDEADBEEFULL;
    uint64_t v = 0;
    for (int i = 0; i < n; i++) v = (v << 8) | b[off + i];
    return v;
}

static uint16_t seq = 0x5000;
static std::vector<uint8_t> xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
    feed_rx(aem_cmd(cmd, seq++, pl));
    return collect_resp();
}

// payload builders
static std::vector<uint8_t> ti_pl(uint16_t type, uint16_t idx) {          // type+index
    std::vector<uint8_t> p; put_be16(p, type); put_be16(p, idx); return p;
}
static std::vector<uint8_t> rd_pl(uint16_t type, uint16_t idx) {          // READ_DESCRIPTOR
    std::vector<uint8_t> p; put_be16(p, 0); put_be16(p, 0);
    put_be16(p, type); put_be16(p, idx); return p;
}

static const uint16_t CMD_READ_DESC  = 0x0004;
static const uint16_t CMD_GET_SI     = 0x000F;
static const uint16_t CMD_GET_AVBIF  = 0x0027;
static const uint16_t CMD_GET_NAME   = 0x0011;   // 1722.1 7.4.18
static const uint16_t IN = 0x0005, OUT = 0x0006;
static const uint16_t AUDIO_UNIT = 0x0002, AVB_INTERFACE = 0x0009;

static const int N_STR = 9;              // 8 AAF + CRF, both directions
static const int CRF_IN = 8;             // AEM_STRIN_CRF_C[8] == 1

// GET_STREAM_INFO response wire offsets (payload starts at 38)
static const int O_TYPE = 38, O_INDEX = 40, O_FLAGS = 42, O_FMT = 46;
static const int O_SID = 54, O_LAT = 62, O_DMAC = 66, O_VLAN = 82;
static const int O_FLAGSEX = 86, O_TRAILER = 90;
static const int SI_FRAME_LEN = 38 + 56;   // 94 bytes on the wire, any status
// READ_DESCRIPTOR response: cfg(2)+reserved(2)+descriptor; current_format is
// at descriptor offset 74 (1722.1-2021 §7.2.6) -> wire 42 + 74
static const int O_RD_FMT = 42 + 74;

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_aecp_top;

    dut->rst_n = 0; dut->enable_i = 1;
    dut->srp_domain_vid_i = 0x002;
    dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    dut->entity_id_i = ENTITY_ID; dut->entity_model_id_i = 0;
    dut->entity_caps_i = 0x00008588; dut->talker_sources_i = N_STR;
    dut->talker_caps_i = 0x4801; dut->listener_sinks_i = N_STR;
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

    printf("== GET_STREAM_INFO on the 8x8 ship shape (D1 index coverage, "
           "D2 response size) ==\n");

    // ------------------------------------------------------------------ //
    printf("\n[1] descriptor directory truth (READ_DESCRIPTOR, 1722.1 7.4.5)\n");
    // The directory is the statement of which {type,index} pairs exist; every
    // later section is compared against THIS.
    bool rd_ok[2][12];
    uint64_t rd_fmt[2][12];
    const uint16_t TYPES[2] = { IN, OUT };
    const char*    TNAME[2] = { "STREAM_INPUT", "STREAM_OUTPUT" };
    for (int t = 0; t < 2; t++) {
        for (int i = 0; i < 12; i++) {
            auto r = xact(CMD_READ_DESC, rd_pl(TYPES[t], i));
            int st = r_status(r);
            rd_ok[t][i]  = (st == 0);
            rd_fmt[t][i] = (st == 0) ? be_at(r, O_RD_FMT, 8) : 0;
            char nm[96];
            snprintf(nm, sizeof nm, "READ_DESCRIPTOR(%s,%d) %s", TNAME[t], i,
                     (i < N_STR) ? "SUCCESS" : "NO_SUCH_DESCRIPTOR");
            ck(nm, st, (i < N_STR) ? 0 : 2);
        }
    }

    // ------------------------------------------------------------------ //
    printf("\n[2] D1: GET_STREAM_INFO agrees with READ_DESCRIPTOR on EVERY "
           "index (the exact contradiction Hive reported 8+7 times)\n");
    for (int t = 0; t < 2; t++) {
        for (int i = 0; i < 12; i++) {
            auto r = xact(CMD_GET_SI, ti_pl(TYPES[t], i));
            char nm[110];
            // (a) same verdict as READ_DESCRIPTOR
            snprintf(nm, sizeof nm, "GSI(%s,%d) status == READ_DESCRIPTOR's",
                     TNAME[t], i);
            ck(nm, (r_status(r) == 0), rd_ok[t][i] ? 1 : 0);
            // (b) D2: 56-byte payload on EVERY status - declared...
            snprintf(nm, sizeof nm, "GSI(%s,%d) cdl 68 (any status)", TNAME[t], i);
            ck(nm, r_cdl(r), 68);
            // (c) ...and actually on the wire
            snprintf(nm, sizeof nm, "GSI(%s,%d) frame 94 B (any status)", TNAME[t], i);
            ck(nm, (long)r.size(), SI_FRAME_LEN);
            // (d) the echoed descriptor_type/index come back verbatim
            //     (1722.1 9.2.2.8/9: the response is matched on them)
            snprintf(nm, sizeof nm, "GSI(%s,%d) echoes type/index", TNAME[t], i);
            ck(nm, (long)be_at(r, O_TYPE, 4),
               ((long)TYPES[t] << 16) | i);
            if (rd_ok[t][i]) {
                // (e) current_format served from THIS descriptor, not from a
                //     hardcoded WB_STREAM_*_FMT_C - compare against the bytes
                //     READ_DESCRIPTOR just returned for the same index
                snprintf(nm, sizeof nm, "GSI(%s,%d) format == descriptor bytes",
                         TNAME[t], i);
                ckh(nm, be_at(r, O_FMT, 8), rd_fmt[t][i]);
                // (f) Milan v1.2 5.4.2.10.1: StreamInfoFlags bit 24 reserved = 0
                snprintf(nm, sizeof nm, "GSI(%s,%d) flags bit24 reserved 0",
                         TNAME[t], i);
                ck(nm, (long)((be_at(r, O_FLAGS, 4) >> 24) & 1), 0);
            } else {
                // (g) the error payload claims nothing: zero flags and a zero
                //     tail. A descriptor that does not exist has no valid
                //     fields, so every *_VALID bit must be 0.
                snprintf(nm, sizeof nm, "GSI(%s,%d) error flags 0", TNAME[t], i);
                ck(nm, (long)be_at(r, O_FLAGS, 4), 0);
                // count a MISSING byte as non-zero: on the pre-fix RTL the
                // frame stopped at 42 B and a "all zero" loop over r.size()
                // would have passed vacuously.
                long nz = 0;
                for (size_t k = O_FLAGS; k < (size_t)SI_FRAME_LEN; k++)
                    if (k >= r.size() || r[k]) nz++;
                snprintf(nm, sizeof nm, "GSI(%s,%d) error tail all zero", TNAME[t], i);
                ck(nm, nz, 0);
            }
        }
    }

    // ------------------------------------------------------------------ //
    printf("\n[3] STREAM_OUTPUT identity per index == what ACMP hands out\n");
    // milan_datapath gives ACMP source uid k stream_dest_mac = MAAP base + k
    // and KL_acmp_tlkr_ctx echoes uid into the stream_id tail. If
    // GET_STREAM_INFO disagreed, a controller that read the info and a
    // listener that bound by ACMP would be pointed at different streams.
    for (int i = 0; i < N_STR; i++) {
        auto r = xact(CMD_GET_SI, ti_pl(OUT, i));
        char nm[96];
        snprintf(nm, sizeof nm, "out%d stream_id {mac,%d}", i, i);
        ckh(nm, be_at(r, O_SID, 8), (STA_MAC << 16) | (uint64_t)i);
        snprintf(nm, sizeof nm, "out%d dest_mac base+%d", i, i);
        ckh(nm, be_at(r, O_DMAC, 6), DMAC_BASE + (uint64_t)i);
        snprintf(nm, sizeof nm, "out%d vlan live", i);
        ck(nm, (long)be_at(r, O_VLAN, 2), 2);
        snprintf(nm, sizeof nm, "out%d msrp_acc_lat default 2 ms", i);
        ck(nm, (long)be_at(r, O_LAT, 4), 2000000);
        snprintf(nm, sizeof nm, "out%d flags 0xF6000000", i);
        ckh(nm, be_at(r, O_FLAGS, 4), 0xF6000000ULL);
    }

    // boundary: a MAAP base whose low byte carries on +1 (the derivation is a
    // 48-bit add, not a byte splice)
    printf("\n[3b] dest_mac derivation carries across the low byte\n");
    dut->aaf_dmac_i = 0x91E0'F000'10FFULL;
    for (int i = 0; i < 4; i++) tick();
    {
        auto r = xact(CMD_GET_SI, ti_pl(OUT, 0));
        ckh("out0 dmac ...10FF", be_at(r, O_DMAC, 6), 0x91E0F00010FFULL);
        r = xact(CMD_GET_SI, ti_pl(OUT, 1));
        ckh("out1 dmac ...1100 (carry)", be_at(r, O_DMAC, 6), 0x91E0F0001100ULL);
        r = xact(CMD_GET_SI, ti_pl(OUT, 8));
        ckh("out8 dmac ...1107 (CRF source)", be_at(r, O_DMAC, 6), 0x91E0F0001107ULL);
    }
    dut->aaf_dmac_i = DMAC_BASE;
    for (int i = 0; i < 4; i++) tick();

    // ------------------------------------------------------------------ //
    printf("\n[4] STREAM_INPUT records: sink 0 live, CRF sink own record, "
           "the rest honestly unbound\n");
    {
        // all sinks unbound at reset
        for (int i = 0; i < N_STR; i++) {
            auto r = xact(CMD_GET_SI, ti_pl(IN, i));
            char nm[96];
            snprintf(nm, sizeof nm, "in%d unbound flags 0xF2000000", i);
            ckh(nm, be_at(r, O_FLAGS, 4), 0xF2000000ULL);
            snprintf(nm, sizeof nm, "in%d unbound stream_id 0", i);
            ckh(nm, be_at(r, O_SID, 8), 0);
            snprintf(nm, sizeof nm, "in%d unbound dest_mac 0", i);
            ckh(nm, be_at(r, O_DMAC, 6), 0);
        }

        // bind sink 0 (the ACMP listener SM) and the CRF sink record
        dut->lstn_bound_i = 1;
        dut->lstn_sid_i   = 0x0200000000010000ULL;
        dut->lstn_dmac_i  = 0x91E0F000FE01ULL;
        dut->lstn_vlan_i  = 2;
        dut->lstn_pbsta_i = 3; dut->lstn_acmpsta_i = 0;
        dut->lstn1_bound_i = 1;
        dut->lstn1_sid_i   = 0x3CC0C6FFFE0102FFULL;
        dut->lstn1_dmac_i  = 0x91E0F0001234ULL;
        for (int i = 0; i < 4; i++) tick();

        // 0xF2000000 identity | CONNECTED(0x04000000). STREAMING_WAIT
        // (0x00000008) stays clear because started_in_r powers on STARTED -
        // the documented START/STOP_STREAMING simplification in the RTL, not
        // something this round changes.
        auto r = xact(CMD_GET_SI, ti_pl(IN, 0));
        ckh("in0 bound flags CONNECTED (no STREAMING_WAIT)",
            be_at(r, O_FLAGS, 4), 0xF6000000ULL);
        ckh("in0 bound stream_id", be_at(r, O_SID, 8), 0x0200000000010000ULL);
        ckh("in0 bound dest_mac", be_at(r, O_DMAC, 6), 0x91E0F000FE01ULL);

        r = xact(CMD_GET_SI, ti_pl(IN, CRF_IN));
        ckh("in8 (CRF) uses ITS OWN bind record",
            be_at(r, O_SID, 8), 0x3CC0C6FFFE0102FFULL);
        ckh("in8 (CRF) dest_mac", be_at(r, O_DMAC, 6), 0x91E0F0001234ULL);

        // NEGATIVE CONTROL: the live records must not leak into the AAF sinks
        // that have no context of their own. If sinks 1..7 reported sink 0's
        // stream we would have replaced "no answer" with a wrong answer.
        for (int i = 1; i < CRF_IN; i++) {
            auto q = xact(CMD_GET_SI, ti_pl(IN, i));
            char nm[96];
            snprintf(nm, sizeof nm, "in%d does NOT inherit sink0/CRF id", i);
            ckh(nm, be_at(q, O_SID, 8), 0);
            snprintf(nm, sizeof nm, "in%d does NOT inherit a dest_mac", i);
            ckh(nm, be_at(q, O_DMAC, 6), 0);
            snprintf(nm, sizeof nm, "in%d reports NOT connected", i);
            ckh(nm, be_at(q, O_FLAGS, 4), 0xF2000000ULL);
        }
        dut->lstn_bound_i = 0; dut->lstn1_bound_i = 0;
        for (int i = 0; i < 4; i++) tick();
    }

    // ------------------------------------------------------------------ //
    printf("\n[5] negative controls on the STATUS side (unchanged behaviour)\n");
    {
        // a descriptor type that EXISTS but is not a stream: still refused.
        // 1722.1 is silent on whether a wrong descriptor TYPE for
        // GET_STREAM_INFO is NO_SUCH_DESCRIPTOR or NOT_IMPLEMENTED (7.4.16.1
        // only says the type shall be STREAM_INPUT/STREAM_OUTPUT), so this
        // round changed the SIZE and left the status exactly where it was.
        auto r = xact(CMD_GET_SI, ti_pl(AUDIO_UNIT, 0));
        ck("GSI(AUDIO_UNIT,0) NO_SUCH_DESCRIPTOR", r_status(r), 2);
        ck("GSI(AUDIO_UNIT,0) still 68 B", r_cdl(r), 68);
        r = xact(CMD_GET_SI, ti_pl(0x7FFF, 0));
        ck("GSI(bogus type) NO_SUCH_DESCRIPTOR", r_status(r), 2);
        ck("GSI(bogus type) still 68 B", r_cdl(r), 68);
        r = xact(CMD_GET_SI, ti_pl(OUT, 0xFFFF));
        ck("GSI(out,65535) NO_SUCH_DESCRIPTOR", r_status(r), 2);
        ck("GSI(out,65535) still 68 B", r_cdl(r), 68);
    }

    // ------------------------------------------------------------------ //
    printf("\n[6] NOT_IMPLEMENTED still REFLECTS THE COMMAND (the one status "
           "that does - la_avdecc checkResponsePayload)\n");
    {
        // If this regressed, every "unknown command" answer would become
        // malformed for a strict controller - the mirror image of D2.
        std::vector<uint8_t> pl;                  // 6-byte payload, cdl 18
        for (int i = 0; i < 6; i++) pl.push_back(0xA5);
        auto r = xact(0x7E, pl);
        ck("unknown command NOT_IMPLEMENTED", r_status(r), 1);
        ck("unknown command cdl == command cdl", r_cdl(r), 18);
        ck("unknown command echoes the payload", (long)be_at(r, 38, 6),
           0xA5A5A5A5A5A5L);
    }

    // ------------------------------------------------------------------ //
    printf("\n[7] the same size rule on the other fixed-shape getters\n");
    {
        // GET_AVB_INFO (1722.1 §7.4.40.2): response >= 20 B payload.
        auto r = xact(CMD_GET_AVBIF, ti_pl(AVB_INTERFACE, 0));
        ck("GET_AVB_INFO(0) SUCCESS", r_status(r), 0);
        ck("GET_AVB_INFO(0) cdl 36 (20 + 1 mapping)", r_cdl(r), 36);
        r = xact(CMD_GET_AVBIF, ti_pl(AVB_INTERFACE, 3));
        ck("GET_AVB_INFO(3) NO_SUCH_DESCRIPTOR", r_status(r), 2);
        ck("GET_AVB_INFO(3) cdl 32 (>= the 20 B minimum)", r_cdl(r), 32);
        ck("GET_AVB_INFO(3) frame 12+32+26 B", (long)r.size(), 38 + 20);
        r = xact(CMD_GET_AVBIF, ti_pl(AUDIO_UNIT, 0));
        ck("GET_AVB_INFO(wrong type) NOT_IMPLEMENTED", r_status(r), 1);
        ck("GET_AVB_INFO(wrong type) reflects command cdl 16", r_cdl(r), 16);

        // GET_NAME (1722.1 §7.4.18.2): response payload 72 B on every status.
        std::vector<uint8_t> gn; put_be16(gn, OUT); put_be16(gn, 0);
        put_be16(gn, 0); put_be16(gn, 0);
        r = xact(CMD_GET_NAME, gn);
        ck("GET_NAME(out0,0) SUCCESS", r_status(r), 0);
        ck("GET_NAME(out0,0) cdl 84", r_cdl(r), 84);
        ck("GET_NAME(out0,0) frame 110 B", (long)r.size(), 38 + 72);
        std::vector<uint8_t> gb; put_be16(gb, OUT); put_be16(gb, 99);
        put_be16(gb, 0); put_be16(gb, 0);
        r = xact(CMD_GET_NAME, gb);
        ck("GET_NAME(out99) NO_SUCH_DESCRIPTOR", r_status(r), 2);
        ck("GET_NAME(out99) cdl still 84", r_cdl(r), 84);
        ck("GET_NAME(out99) frame still 110 B", (long)r.size(), 38 + 72);
        std::vector<uint8_t> gi; put_be16(gi, OUT); put_be16(gi, 0);
        put_be16(gi, 7); put_be16(gi, 0);          // name_index 7 invalid
        r = xact(CMD_GET_NAME, gi);
        ck("GET_NAME(bad name_index) BAD_ARGUMENTS", r_status(r), 7);
        ck("GET_NAME(bad name_index) cdl still 84", r_cdl(r), 84);
        ck("GET_NAME(bad name_index) frame still 110 B", (long)r.size(), 38 + 72);
    }

    // ------------------------------------------------------------------ //
    printf("\n[8] D1 again on the OTHER dynamic-info command: GET_COUNTERS "
           "must answer every descriptor READ_DESCRIPTOR serves\n");
    {
        // Same self-contradiction class as GET_STREAM_INFO. The Milan-
        // validated reference device answers GET_COUNTERS SUCCESS on every
        // served STREAM_INPUT/STREAM_OUTPUT and returns the full 136-byte
        // payload (cdl 148) on error too - measured 2026-07-28, which is
        // where this expectation comes from, not from our own behaviour.
        for (int t = 0; t < 2; t++) {
            for (int i = 0; i < 11; i++) {
                auto r = xact(0x0029, ti_pl(TYPES[t], i));   // GET_COUNTERS
                char nm[110];
                snprintf(nm, sizeof nm, "GET_COUNTERS(%s,%d) status == "
                         "READ_DESCRIPTOR's", TNAME[t], i);
                ck(nm, (r_status(r) == 0), (i < N_STR) ? 1 : 0);
                snprintf(nm, sizeof nm, "GET_COUNTERS(%s,%d) cdl 148", TNAME[t], i);
                ck(nm, r_cdl(r), 148);
                snprintf(nm, sizeof nm, "GET_COUNTERS(%s,%d) frame 174 B", TNAME[t], i);
                ck(nm, (long)r.size(), 38 + 136);
                if (i < N_STR) {
                    // Milan 5.4.2.25 Tables 5.16/5.17: "shall implement
                    // and return the counters" for EACH stream descriptor.
                    // Since 2026-07-28 every STREAM_OUTPUT (the CRF Media
                    // Clock Output at index 8 included) answers its
                    // KL_talker_diag_ctx context behind mask 0x1F, and
                    // every AAF STREAM_INPUT its monitor-mirror context
                    // behind 0xFFF (Milan 1.3 5.3.8.10 adds the tv
                    // tallies to the v1.2 ten). The one truthful EMPTY
                    // mask left is
                    // the CRF Media Clock INPUT (index 8): it has no
                    // monitor context, and 7.4.42.2 makes the empty mask
                    // the statement of that (its counters are a recorded
                    // gap in MILAN_COMPLIANCE_GAPS.md).
                    bool is_out = (TYPES[t] == 0x0006);
                    long want = is_out ? 0x1F
                              : (i < 8) ? 0xFFF : 0;
                    snprintf(nm, sizeof nm, "GET_COUNTERS(%s,%d) valid mask "
                             "%s", TNAME[t], i,
                             want == 0 ? "EMPTY (CRF input, no context)"
                                       : is_out ? "0x1F (Table 5.17)"
                                                : "0xFFF (Milan 1.3)");
                    ck(nm, (long)be_at(r, 42, 4), want);
                }
            }
        }
        // negative control: a descriptor that exists and has NO counters
        auto r = xact(0x0029, ti_pl(0x000B, 0));   // LOCALE
        ck("GET_COUNTERS(LOCALE,0) refused", (r_status(r) == 0), 0);
        ck("GET_COUNTERS(LOCALE,0) still 148", r_cdl(r), 148);
    }

    printf("\n[9] GET_AUDIO_MAP error payload keeps the 12 B floor (§7.4.44.2)\n");
    {
        std::vector<uint8_t> am;
        put_be16(am, 0x000E); put_be16(am, 9); put_be16(am, 0);  // absent port
        auto r = xact(0x002B, am);                               // GET_AUDIO_MAP
        ck("GET_AUDIO_MAP(absent) NO_SUCH_DESCRIPTOR", r_status(r), 2);
        ck("GET_AUDIO_MAP(absent) cdl 24 (12 B payload)", r_cdl(r), 24);
        ck("GET_AUDIO_MAP(absent) frame >= 12+12+26", (long)(r.size() >= 50), 1);
    }

    printf("\n----------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
