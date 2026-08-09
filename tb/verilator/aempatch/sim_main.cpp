/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * E4 — the AEM dynamic-state ingest port (CSR 0x7C8-0x7D4).
 *
 * WHAT THIS SUITE IS FOR. Milan v1.2 requires eleven pieces of dynamic state
 * to survive a power cycle. Saving them always worked; putting them BACK did
 * not, because KL_aecp_aem_store's write port had exactly one master (the
 * SET_* write-back). This suite gates the master that closes that loop, and
 * it insists on the property that makes the port safe rather than merely
 * present: a restore is accepted ONLY while the entity is silent.
 *
 * THE CENTRAL TEST IS A ROUND TRIP, NOT A REGISTER POKE. Phase [P1] writes a
 * stream format in through the CSR port with ADP disabled, brings the
 * advertiser up, and then reads the value back the way a real controller
 * would — a GET_STREAM_FORMAT over the AECP frame path. Anything less would
 * prove the fabric stored a byte somewhere, not that the entity now ANSWERS
 * with the restored value, and the second is the clause's actual requirement.
 *
 * Every negative leg checks TWO things: the verdict names the right refusal,
 * AND the store did not move. A port that reports a rejection while writing
 * anyway is the failure mode that would be hardest to see on silicon.
 *
 * Exit 0 = all pass.
 */

#include "Vaempatch_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>

static Vaempatch_wrap* dut;
static long checks = 0, fails = 0;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-56s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-56s = %ld\n", what, got); }
}
static void ckh(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-56s got=%016llx exp=%016llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    } else {
        printf("  [ ok ] %-56s = %016llx\n", what, (unsigned long long)got);
    }
}

// ------------------------------------------------------------------ //
// The group under test (REGISTER_MAP.md 0x7C8)                        //
// ------------------------------------------------------------------ //
#define A_AEMP_SEL   0x7C8
#define A_AEMP_FIELD 0x7CC
#define A_AEMP_DATA  0x7D0
#define A_AEMP_CTRL  0x7D4

// verdicts (stat[7:4]) — KL_aem_patch VD_*
#define VD_NONE   0
#define VD_ACCEPT 1
#define VD_ADP    2
#define VD_DESC   3
#define VD_FIELD  4
#define VD_LEN    5
#define VD_VALUE  6

// field codes
#define FLD_FORMAT   0
#define FLD_SAMPRATE 1
#define FLD_CLKSRC   2
#define FLD_PRESOFF  3
#define FLD_NAME     4

static int st_state (uint32_t s) { return  s        & 0x7; }
static int st_verdict(uint32_t s){ return (s >>  4) & 0xF; }
static int st_bytes (uint32_t s) { return (s >>  8) & 0xF; }
static int st_words (uint32_t s) { return (s >> 12) & 0x7; }
static int st_field (uint32_t s) { return (s >> 16) & 0x7; }
static int st_gate  (uint32_t s) { return (s >> 19) & 0x1; }
static int st_done  (uint32_t s) { return (s >> 30) & 0x1; }
static int st_busy  (uint32_t s) { return (s >> 31) & 0x1; }

static void csr_wr(uint32_t addr, uint32_t data) {
    dut->wr_addr_i = addr; dut->wr_data_i = data; dut->wr_p_i = 1;
    tick();
    dut->wr_p_i = 0;
    tick();
}
static uint32_t csr_rd(uint32_t addr) {
    dut->rd_addr_i = addr; dut->eval();
    return dut->rd_data_o;
}

// ------------------------------------------------------------------ //
// Identity + AECP frame plumbing (same recipe as tb/verilator/aecp)   //
// ------------------------------------------------------------------ //
static const uint8_t ENT_MAC[6] = {0x02,0x00,0x00,0xff,0xfe,0x01};
static const uint8_t CTL_MAC[6] = {0x68,0x05,0xca,0x95,0xb2,0xd1};
static const uint64_t ENTITY_ID = 0x020000fffe000001ULL;
static const uint64_t CTLR_ID   = 0x6805ca95b2d10000ULL;

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

//! One reusable stimulus buffer for the whole run. build_aem_cmd() fills it
//! through a reference and clear() keeps its capacity, so the command bytes
//! cost ONE allocation for the entire simulation instead of a malloc plus
//! three or four reallocs on every transaction.
static std::vector<uint8_t> stim;

//! Fill `out` with an AEM command frame and hand back a reference to it, so a
//! call site reads `feed_rx(build_aem_cmd(stim, ...))` and reuses one buffer.
static const std::vector<uint8_t>& build_aem_cmd(std::vector<uint8_t>& out,
                                    uint16_t cmd, uint16_t seq,
                                    const std::vector<uint8_t>& payload) {
    size_t want = AEM_HDR_BYTES + payload.size();
    out.clear();                                // clear KEEPS the capacity
    out.reserve(want < ETH_MIN_BYTES ? ETH_MIN_BYTES : want);
    std::vector<uint8_t>& f = out;
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

//! Widest AEM response this suite collects (a READ_DESCRIPTOR reply), used to
//! size the collector once instead of growing it a beat at a time.
static const size_t AEM_RESP_BYTES = 600;

static std::vector<uint8_t> collect_resp(int budget = 6000) {
    std::vector<uint8_t> b;
    b.reserve(AEM_RESP_BYTES);
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

static int r_status(const std::vector<uint8_t>& b) {
    return b.size() > 16 ? (b[16] >> 3) & 0x1F : -1;
}
static uint64_t r_fmt(const std::vector<uint8_t>& b) {
    if (b.size() < 50) return 0;
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) v = (v << 8) | b[42+i];
    return v;
}
static uint32_t r_u32(const std::vector<uint8_t>& b) {   // payload word @ 42
    if (b.size() < 46) return 0xFFFFFFFFu;
    uint32_t v = 0;
    for (int i = 0; i < 4; i++) v = (v << 8) | b[42+i];
    return v;
}
static uint16_t r_u16(const std::vector<uint8_t>& b) {   // payload half @ 42
    if (b.size() < 44) return 0xFFFFu;
    return (uint16_t)((b[42] << 8) | b[43]);
}

static uint16_t g_seq = 0x4000;
static std::vector<uint8_t> xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
    feed_rx(build_aem_cmd(stim, cmd, g_seq++, pl));
    return collect_resp();
}

static const uint16_t CMD_GET_FMT  = 9;
static const uint16_t CMD_SET_FMT  = 8;
static const uint16_t CMD_GET_RATE = 21;
static const uint16_t CMD_GET_CLK  = 23;
static const uint16_t D_AUDIO_UNIT = 0x0002;
static const uint16_t D_IN         = 0x0005;
static const uint16_t D_OUT        = 0x0006;
static const uint16_t D_CLK_DOMAIN = 0x0024;

static std::vector<uint8_t> di_pl(uint16_t type, uint16_t idx) {
    std::vector<uint8_t> pl; pl.reserve(4);     // two u16 fields, exactly
    put_be16(pl, type); put_be16(pl, idx); return pl;
}
static std::vector<uint8_t> sf_pl(uint16_t type, uint16_t idx, uint64_t fmt) {
    auto pl = di_pl(type, idx); pl.reserve(12); put_be64(pl, fmt);
    return pl;
}

// ------------------------------------------------------------------ //
// The entity shape this suite is built against (8x8, AX7101).         //
// Values mirror gen/aecp_aem_rom.svh AEM_STRIN_FMT_C / AEM_RATES_C —   //
// see the Makefile's -I ordering note for why the shape is pinned.     //
// ------------------------------------------------------------------ //
static const uint64_t FMT_MASK = ~((0x3FFULL << 22) | (1ULL << 52));
static const uint64_t AAF_REF  = 0x0205022002006000ULL;   // declared, 8ch
static const uint64_t CRF_REF  = 0x041060010000BB80ULL;   // the CRF sink
static uint64_t aaf_ch(unsigned n) { return (AAF_REF & FMT_MASK) | ((uint64_t)n << 22); }
static const uint32_t RATE_48K = 0x0000BB80;

// ------------------------------------------------------------------ //
// ADP enable == cfg_adp_enable == "the patch port is closed"          //
// ------------------------------------------------------------------ //
static void adp(int on) {
    dut->enable_i = on ? 1 : 0;
    for (int i = 0; i < 4; i++) tick();
}

//! Drive one complete patch transaction and return the verdict. `nw` payload
//! words are pushed MSW-first; passing nw deliberately wrong is how the
//! length legs are built.
static uint32_t patch(uint16_t dtype, uint16_t didx, int field,
                      const uint32_t* w, int nw) {
    csr_wr(A_AEMP_SEL,   ((uint32_t)dtype << 16) | didx);
    csr_wr(A_AEMP_FIELD, (uint32_t)field);
    for (int i = 0; i < nw; i++) csr_wr(A_AEMP_DATA, w[i]);
    csr_wr(A_AEMP_CTRL,  0x1);                     // commit
    for (int i = 0; i < 200; i++) {                // burst is <= 8 store writes
        if (!st_busy(csr_rd(A_AEMP_CTRL))) break;
        tick();
    }
    return csr_rd(A_AEMP_CTRL);
}
static uint32_t patch64(uint16_t dtype, uint16_t didx, int field, uint64_t v) {
    uint32_t w[2] = { (uint32_t)(v >> 32), (uint32_t)(v & 0xFFFFFFFFu) };
    return patch(dtype, didx, field, w, 2);
}

//! Read a stream format back the way a controller does. The advertiser has to
//! be up for the AECP engine to answer, which is exactly the boot order the
//! port enforces: restore first, advertise second, controller reads third.
static uint64_t get_fmt(uint16_t type, uint16_t idx, int* status = nullptr) {
    adp(1);
    auto r = xact(CMD_GET_FMT, di_pl(type, idx));
    if (status) *status = r_status(r);
    uint64_t v = r_fmt(r);
    adp(0);
    return v;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new Vaempatch_wrap;

    dut->rst_n = 0;
    dut->enable_i = 0;
    dut->wr_p_i = 0; dut->wr_addr_i = 0; dut->wr_data_i = 0; dut->rd_addr_i = 0;
    dut->rx_tvalid_i = 0; dut->rx_tdata_i = 0; dut->rx_tkeep_i = 0;
    dut->rx_tlast_i = 0; dut->m_axis_tready = 1;
    dut->entity_id_i = ENTITY_ID;
    { uint64_t m = 0; for (int i = 0; i < 6; i++) m = (m << 8) | ENT_MAC[i];
      dut->station_mac_i = m; }
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 8; i++) tick();

    printf("== E4 AEM dynamic-state ingest port (CSR 0x7C8-0x7D4) ==\n");

    // ---------------------------------------------------------------- //
    printf("\n[P0] reset state — nothing attempted, nothing busy\n");
    {
        uint32_t s = csr_rd(A_AEMP_CTRL);
        ck("[P0] verdict NONE", st_verdict(s), VD_NONE);
        ck("[P0] not busy",     st_busy(s),    0);
        ck("[P0] not done",     st_done(s),    0);
        ck("[P0] 0 words staged", st_words(s), 0);
        ck("[P0] gate open (ADP disabled)", st_gate(s), 0);
        ck("[P0] SEL reads 0 (write-only)",   (long)csr_rd(A_AEMP_SEL),   0);
        ck("[P0] FIELD reads 0 (write-only)", (long)csr_rd(A_AEMP_FIELD), 0);
        ck("[P0] DATA reads 0 (write-only)",  (long)csr_rd(A_AEMP_DATA),  0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[P1] THE ROUND TRIP — Milan 5.3.8.1 STREAM_INPUT format\n");
    printf("     restore with ADP down, advertise, read back over AECP\n");
    {
        int stat = 0;
        ckh("[P1] IN[3] boots at the declared 8ch default",
            get_fmt(D_IN, 3, &stat), AAF_REF);
        ck ("[P1] that GET was SUCCESS", stat, 0);

        uint32_t s = patch64(D_IN, 3, FLD_FORMAT, aaf_ch(2));
        ck("[P1] patch IN[3] -> 2ch ACCEPTED", st_verdict(s), VD_ACCEPT);
        ck("[P1] 8 bytes written",             st_bytes(s),   8);
        ck("[P1] engine idle again",           st_busy(s),    0);

        //! THE CLAUSE. Not "a byte moved" — the entity now ANSWERS with the
        //! restored value over the same command a controller would use.
        ckh("[P1] GET_STREAM_FORMAT(IN,3) returns the restored 2ch",
            get_fmt(D_IN, 3), aaf_ch(2));

        //! and only that descriptor moved: the port resolves ONE byte range
        ckh("[P1] IN[2] untouched (per-descriptor isolation)",
            get_fmt(D_IN, 2), AAF_REF);
        ckh("[P1] IN[4] untouched (per-descriptor isolation)",
            get_fmt(D_IN, 4), AAF_REF);
        ckh("[P1] OUT[3] untouched (input/output tables are separate)",
            get_fmt(D_OUT, 3), AAF_REF);
    }

    // ---------------------------------------------------------------- //
    printf("\n[P2] THE GATE — a write arriving while advertising is REFUSED\n");
    {
        adp(1);
        uint32_t s = patch64(D_IN, 3, FLD_FORMAT, aaf_ch(6));
        ck("[P2] verdict ADP (refused, not queued)", st_verdict(s), VD_ADP);
        ck("[P2] gate bit set in status",            st_gate(s),    1);
        ck("[P2] engine never went busy",            st_busy(s),    0);
        adp(0);

        //! mutation anchor: the refusal must be a REFUSAL, not a deferral.
        //! If the gate merely stalled the port, the value would appear here.
        ckh("[P2] IN[3] STILL the 2ch from [P1] — nothing was applied",
            get_fmt(D_IN, 3), aaf_ch(2));

        //! and the refused transfer left no residue that a later commit
        //! could pick up: staging is dropped, not held
        uint32_t s2 = csr_rd(A_AEMP_CTRL);
        ck("[P2] 0 words staged after the refusal", st_words(s2), 0);
        csr_wr(A_AEMP_CTRL, 0x1);                  // bare commit, no payload
        for (int i = 0; i < 20; i++) tick();
        ck("[P2] a bare re-commit cannot finish the refused transfer",
           st_verdict(csr_rd(A_AEMP_CTRL)), VD_LEN);
        ckh("[P2] IN[3] still 2ch after the bare re-commit",
            get_fmt(D_IN, 3), aaf_ch(2));
    }

    // ---------------------------------------------------------------- //
    printf("\n[P3] VALIDATION — the same acceptance the AECP SET applies\n");
    {
        //! 5.3.8.1: "shall always be using a format that is one of the
        //! supported formats". A restore that installs an undeclared format
        //! is a worse break than the revert it fixes.
        uint32_t s = patch64(D_IN, 3, FLD_FORMAT, aaf_ch(9));
        ck("[P3] 9 channels REFUSED (family bound is 1..8)", st_verdict(s), VD_VALUE);
        ckh("[P3] store unmoved after the refusal", get_fmt(D_IN, 3), aaf_ch(2));

        s = patch64(D_IN, 3, FLD_FORMAT, aaf_ch(0));
        ck("[P3] 0 channels REFUSED", st_verdict(s), VD_VALUE);

        s = patch64(D_IN, 3, FLD_FORMAT, CRF_REF);
        ck("[P3] a CRF format on an AAF sink REFUSED", st_verdict(s), VD_VALUE);
        ckh("[P3] store still 2ch", get_fmt(D_IN, 3), aaf_ch(2));

        s = patch64(D_IN, 3, FLD_FORMAT, aaf_ch(2) | (1ULL << 52));
        ck("[P3] the ut (up-to) bit REFUSED — a SET must be concrete",
           st_verdict(s), VD_VALUE);

        //! the CRF sink is index 8 in this shape and takes its OWN reference
        s = patch64(D_IN, 8, FLD_FORMAT, CRF_REF);
        ck("[P3] CRF sink IN[8] accepts its exact declared format",
           st_verdict(s), VD_ACCEPT);
        s = patch64(D_IN, 8, FLD_FORMAT, aaf_ch(2));
        ck("[P3] CRF sink REFUSES an AAF format", st_verdict(s), VD_VALUE);

        //! talker truth: a Stream Output accepts ONLY its declared format
        s = patch64(D_OUT, 3, FLD_FORMAT, AAF_REF);
        ck("[P3] OUT[3] accepts its declared format", st_verdict(s), VD_ACCEPT);
        s = patch64(D_OUT, 3, FLD_FORMAT, aaf_ch(2));
        ck("[P3] OUT[3] REFUSES a family variant (declared == transmitted)",
           st_verdict(s), VD_VALUE);
    }

    // ---------------------------------------------------------------- //
    printf("\n[P4] ADDRESSING — the port cannot reach a descriptor it has no table for\n");
    {
        uint32_t s = patch64(D_IN, 9, FLD_FORMAT, aaf_ch(2));
        ck("[P4] IN[9] (past AEM_N_STRIN_C) REFUSED", st_verdict(s), VD_DESC);
        s = patch64(D_IN, 0x7FFF, FLD_FORMAT, aaf_ch(2));
        ck("[P4] a wild index REFUSED",               st_verdict(s), VD_DESC);
        s = patch64(D_OUT, 9, FLD_FORMAT, AAF_REF);
        ck("[P4] OUT[9] REFUSED",                     st_verdict(s), VD_DESC);
        s = patch64(0x0014, 0, FLD_FORMAT, aaf_ch(2));   // AUDIO_CLUSTER
        ck("[P4] a descriptor type with no format field REFUSED",
           st_verdict(s), VD_DESC);
        ckh("[P4] nothing moved through any of them", get_fmt(D_IN, 3), aaf_ch(2));
    }

    // ---------------------------------------------------------------- //
    printf("\n[P5] LENGTH — a short or long payload is named, never truncated\n");
    {
        uint32_t one = (uint32_t)(aaf_ch(2) >> 32);
        uint32_t s = patch(D_IN, 3, FLD_FORMAT, &one, 1);
        ck("[P5] format with 1 word REFUSED (wants 2)", st_verdict(s), VD_LEN);
        uint32_t three[3] = { one, 0, 0 };
        s = patch(D_IN, 3, FLD_FORMAT, three, 3);
        ck("[P5] format with 3 words REFUSED",          st_verdict(s), VD_LEN);
        ckh("[P5] store unmoved by either", get_fmt(D_IN, 3), aaf_ch(2));
    }

    // ---------------------------------------------------------------- //
    printf("\n[P6] Milan 5.3.5.1 sampling rate + 5.3.11.1 clock source\n");
    {
        uint32_t w = RATE_48K;
        uint32_t s = patch(D_AUDIO_UNIT, 0, FLD_SAMPRATE, &w, 1);
        ck("[P6] AUDIO_UNIT[0] rate 48k ACCEPTED", st_verdict(s), VD_ACCEPT);
        ck("[P6] 4 bytes written",                 st_bytes(s),   4);
        adp(1);
        auto r = xact(CMD_GET_RATE, di_pl(D_AUDIO_UNIT, 0));
        ck("[P6] GET_SAMPLING_RATE SUCCESS", r_status(r), 0);
        ck("[P6] reads back 48000",          (long)r_u32(r), (long)RATE_48K);
        adp(0);

        w = 0x0000AC44;                                   // 44100, undeclared
        s = patch(D_AUDIO_UNIT, 0, FLD_SAMPRATE, &w, 1);
        ck("[P6] an undeclared rate REFUSED", st_verdict(s), VD_VALUE);
        w = RATE_48K;
        s = patch(D_CLK_DOMAIN, 0, FLD_SAMPRATE, &w, 1);
        ck("[P6] rate on the wrong descriptor REFUSED", st_verdict(s), VD_DESC);

        //! clock source 2 = the CRF stream. Payload is left-aligned: the
        //! 16-bit field sits in the TOP half of the pushed word.
        w = 0x0002 << 16;
        s = patch(D_CLK_DOMAIN, 0, FLD_CLKSRC, &w, 1);
        ck("[P6] CLOCK_DOMAIN[0] source 2 ACCEPTED", st_verdict(s), VD_ACCEPT);
        ck("[P6] 2 bytes written",                   st_bytes(s),   2);
        adp(1);
        r = xact(CMD_GET_CLK, di_pl(D_CLK_DOMAIN, 0));
        ck("[P6] GET_CLOCK_SOURCE SUCCESS", r_status(r), 0);
        ck("[P6] reads back source 2",      (long)r_u16(r), 2);
        adp(0);

        w = 0x0003 << 16;
        s = patch(D_CLK_DOMAIN, 0, FLD_CLKSRC, &w, 1);
        ck("[P6] source 3 REFUSED (only 0..2 exist)", st_verdict(s), VD_VALUE);
    }

    // ---------------------------------------------------------------- //
    printf("\n[P7] HONESTY — fields this port does NOT serve say so by name\n");
    {
        uint64_t v = 0;
        uint32_t s = patch64(D_OUT, 0, FLD_PRESOFF, v);
        ck("[P7] 5.3.7.6 presentation offset REFUSED (VD_FIELD, not silence)",
           st_verdict(s), VD_FIELD);
        s = patch64(D_IN, 0, FLD_NAME, v);
        ck("[P7] 5.3.13 names REFUSED (VD_FIELD)", st_verdict(s), VD_FIELD);
        s = patch64(D_IN, 0, 5, v);
        ck("[P7] an unassigned field code REFUSED", st_verdict(s), VD_FIELD);
        s = patch64(D_IN, 0, 7, v);
        ck("[P7] field code 7 REFUSED",             st_verdict(s), VD_FIELD);
        ckh("[P7] and none of them wrote anything", get_fmt(D_IN, 3), aaf_ch(2));

        //! The clock-source patch above moved the DESCRIPTOR, which is what
        //! GET_CLOCK_SOURCE serves and what 5.3.11.1 is about. It does NOT
        //! move the builder's live clk_src_r shadow — that register file has
        //! no slave port yet. Asserting the limitation keeps it visible
        //! instead of letting a future reader assume the restore is total.
        ck("[P7] KNOWN GAP: the live clock selector is still boot-default",
           (long)dut->clk_src_o, 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[P8] Milan 5.3.4.1 / 5.3.4.2 — the state that must NOT come back\n");
    {
        //! These two clauses require the OPPOSITE of persistence: the locked
        //! state and the registered-controller list are CLEARED by a power
        //! cycle. The port satisfies them by CONSTRUCTION — there is no field
        //! code that resolves to either, so the refusal below is not a
        //! policy someone can forget to apply, it is the absence of a table
        //! entry. [P7] already showed codes 3..7 refuse; this states WHY the
        //! absence matters, and that the only reachable ranges are the three
        //! served fields.
        for (int f = 0; f < 8; f++) {
            if (f == FLD_FORMAT || f == FLD_SAMPRATE || f == FLD_CLKSRC) continue;
            uint32_t s = patch64(0x0000 /* ENTITY */, 0, f, 0xFFFFFFFFFFFFFFFFULL);
            char lbl[80];
            snprintf(lbl, sizeof lbl,
                     "[P8] ENTITY field %d unreachable (5.3.4.1/5.3.4.2)", f);
            ck(lbl, st_verdict(s), VD_FIELD);
        }
        //! ENTITY with a SERVED field code still fails on the descriptor,
        //! so there is no path at all from this port to entity-global state
        uint32_t s = patch64(0x0000, 0, FLD_FORMAT, aaf_ch(2));
        ck("[P8] ENTITY + format code REFUSED on the descriptor",
           st_verdict(s), VD_DESC);
        ckh("[P8] the descriptor image is where [P1] left it",
            get_fmt(D_IN, 3), aaf_ch(2));
    }

    // ---------------------------------------------------------------- //
    printf("\n[P9] ABORT + the straddle case\n");
    {
        //! abort drops staged words without writing
        csr_wr(A_AEMP_SEL,   ((uint32_t)D_IN << 16) | 5);
        csr_wr(A_AEMP_FIELD, FLD_FORMAT);
        csr_wr(A_AEMP_DATA,  (uint32_t)(aaf_ch(4) >> 32));
        csr_wr(A_AEMP_DATA,  (uint32_t)(aaf_ch(4) & 0xFFFFFFFFu));
        ck("[P9] 2 words staged", st_words(csr_rd(A_AEMP_CTRL)), 2);
        csr_wr(A_AEMP_CTRL, 0x2);                  // abort
        for (int i = 0; i < 8; i++) tick();
        ck("[P9] abort clears the staging", st_words(csr_rd(A_AEMP_CTRL)), 0);
        ck("[P9] abort clears the verdict", st_verdict(csr_rd(A_AEMP_CTRL)), VD_NONE);
        ckh("[P9] IN[5] never moved", get_fmt(D_IN, 5), AAF_REF);

        //! a transfer that straddles the advertiser coming up cannot be
        //! completed afterwards with half its words from before
        csr_wr(A_AEMP_SEL,   ((uint32_t)D_IN << 16) | 5);
        csr_wr(A_AEMP_FIELD, FLD_FORMAT);
        csr_wr(A_AEMP_DATA,  (uint32_t)(aaf_ch(4) >> 32));
        adp(1);
        csr_wr(A_AEMP_DATA,  (uint32_t)(aaf_ch(4) & 0xFFFFFFFFu));
        ck("[P9] the word that arrived while advertising was refused",
           st_verdict(csr_rd(A_AEMP_CTRL)), VD_ADP);
        adp(0);
        csr_wr(A_AEMP_CTRL, 0x1);                  // commit what is left
        for (int i = 0; i < 40; i++) tick();
        ck("[P9] the straddled commit is REFUSED on length",
           st_verdict(csr_rd(A_AEMP_CTRL)), VD_LEN);
        ckh("[P9] IN[5] still the boot default", get_fmt(D_IN, 5), AAF_REF);
    }

    // ---------------------------------------------------------------- //
    printf("\n[P10] a second restore overwrites the first (idempotent replay)\n");
    {
        uint32_t s = patch64(D_IN, 3, FLD_FORMAT, aaf_ch(4));
        ck("[P10] re-patch IN[3] -> 4ch ACCEPTED", st_verdict(s), VD_ACCEPT);
        ckh("[P10] GET now returns 4ch", get_fmt(D_IN, 3), aaf_ch(4));
        s = patch64(D_IN, 3, FLD_FORMAT, AAF_REF);
        ck("[P10] restore the 8ch default ACCEPTED", st_verdict(s), VD_ACCEPT);
        ckh("[P10] GET back to the declared default", get_fmt(D_IN, 3), AAF_REF);

        //! and a normal controller SET still works afterwards — the patch
        //! port did not take the store's write port away from the AECP path
        adp(1);
        auto r = xact(CMD_SET_FMT, sf_pl(D_IN, 3, aaf_ch(2)));
        ck("[P10] SET_STREAM_FORMAT still SUCCESS after patching",
           r_status(r), 0);
        adp(0);
        ckh("[P10] and its write-back landed", get_fmt(D_IN, 3), aaf_ch(2));
    }

    printf("\n----------------------------------------------------------\n");
    printf("aem patch: %ld checks, %ld failures\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
