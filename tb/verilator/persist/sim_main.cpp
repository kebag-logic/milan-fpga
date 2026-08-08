/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking harness for the Milan saved-state fast-connect PERSISTENCE
 * JOURNAL replay path (roadmap item 9):
 *
 *     CSR 0x7B8-0x7C4 -> KL_persist_journal -> rest_* (E1) -> KL_acmp_lstn_ctx
 *
 * What this proves, on real RTL and not by inspection:
 *
 *   POSITIVE  a saved journal slot replays into the ACMP listener context
 *             table as the Milan 5.5.3.5.2 entry record, and the sink then
 *             completes a real fast-connect (ADP watch -> PROBE_TX -> probe
 *             response -> SETTLED, stream_active) with NO controller in the
 *             loop. That is "a bound listener from flash".
 *
 *   NEGATIVE  a TORN journal (one bit flipped anywhere in the image, so the
 *             CRC-32 trailer no longer closes) is rejected WHOLE: the engine
 *             raises exactly ZERO rest_req transactions and the context table
 *             is bit-identical afterwards. Never half-applied. Same for a
 *             truncated transfer, an erased slot, a foreign entity_id, an
 *             unreadable format major and an out-of-range shape.
 *
 *   A/B       a rejected image never advances the accepted-SEQ watermark, so
 *             the fall-back to the older intact slot is always admissible;
 *             and a slot that does not beat the watermark is refused (STALE)
 *             so a stale slot cannot roll a fresh binding back.
 *
 * Traceability (Milan v1.2 / IEEE Std 1722.1-2021):
 *   M-ACMP-*  5.5.3.5.2   saved-state entry record {PRB_W_AVAIL, PASSIVE, 0}
 *             5.5.2.6 s1  SRP params CLEARED on load, re-learned by the probe
 *             5.5.1.4     the restored sink waits for the talker's ADPDU
 *             5.5.3.5.3   binding controller_entity_id is part of saved state
 *             5.4         persistent settings
 */

#include "Vpersist_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vpersist_wrap* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-54s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-54s = %ld\n", what, got); }
}
static void ckh(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-54s got=%llx exp=%llx\n", what,
                              (unsigned long long)got, (unsigned long long)exp); }
    else            { printf("  [ ok ] %-54s = %llx\n", what, (unsigned long long)got); }
}

// ------------------------------------------------------------------ clocking
static std::vector<uint8_t> partial;
static long rest_edges = 0;         // rising edges of rest_req_o (transactions)
static int  rest_prev  = 0;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    if (dut->rest_req_o && !rest_prev) rest_edges++;
    rest_prev = dut->rest_req_o;
}

static bool tick_collect(std::vector<uint8_t>* done) {
    bool got = false;
    dut->m_axis_tready = 1;
    dut->eval();
    if (dut->m_axis_tvalid) {
        for (int l = 0; l < 8; l++)
            if ((dut->m_axis_tkeep >> l) & 1)
                partial.push_back((dut->m_axis_tdata >> (8*l)) & 0xFF);
        if (dut->m_axis_tlast) {
            if (done) *done = partial;
            partial.clear();
            got = true;
        }
    }
    tick();
    return got;
}

static void run(int n) { for (int i = 0; i < n; i++) tick_collect(nullptr); }

static std::vector<uint8_t> wait_frame(int budget = 4000) {
    std::vector<uint8_t> f;
    for (int c = 0; c < budget; c++)
        if (tick_collect(&f)) return f;
    return {};
}

// ------------------------------------------------------------------ identity
static const uint64_t US_EID = 0x020000FFFE000003ULL;
static const uint8_t  US_MAC[6] = {0x02,0x00,0x00,0x00,0x00,0x03};
static const uint64_t CT_EID = 0x680500FFFE0000AAULL;
static const uint64_t T1_EID = 0x020000FFFE000001ULL;
static const uint64_t T2_EID = 0x020000FFFE000002ULL;
static const uint64_t T3_EID = 0x020000FFFE000004ULL;
static const uint64_t FOREIGN_EID = 0x020000FFFE0000EEULL;

// ------------------------------------------------------------------ ACMP/ADP
static void put_be(std::vector<uint8_t>& v, uint64_t x, int n) {
    for (int i = n-1; i >= 0; i--) v.push_back((x >> (8*i)) & 0xFF);
}

static std::vector<uint8_t> acmp(uint8_t msg, uint8_t status,
                                 uint64_t sid, uint64_t ctlr, uint64_t talker,
                                 uint64_t lstnr, uint16_t tuid, uint16_t luid,
                                 const uint8_t* dmac, uint16_t seq,
                                 uint16_t flags, uint16_t vlan) {
    std::vector<uint8_t> f = {0x91,0xE0,0xF0,0x01,0x00,0x00,
                              0xAA,0xBB,0xCC,0x00,0x00,0x01,
                              0x22,0xF0, 0xFC};
    f.push_back(msg & 0xF);
    f.push_back((status << 3) | 0);
    f.push_back(44);
    put_be(f, sid, 8);
    put_be(f, ctlr, 8);
    put_be(f, talker, 8);
    put_be(f, lstnr, 8);
    put_be(f, tuid, 2);
    put_be(f, luid, 2);
    for (int i = 0; i < 6; i++) f.push_back(dmac ? dmac[i] : 0);
    put_be(f, 0, 2);
    put_be(f, seq, 2);
    put_be(f, flags, 2);
    put_be(f, vlan, 2);
    put_be(f, 0, 2);
    return f;
}

static std::vector<uint8_t> adp(uint8_t msg, uint64_t eid) {
    std::vector<uint8_t> f = {0x91,0xE0,0xF0,0x01,0x00,0x00,
                              0x02,0x00,0x00,0x00,0x00,0x01,
                              0x22,0xF0, 0xFA};
    f.push_back(msg & 0xF);
    f.push_back(0x1F); f.push_back(56);
    put_be(f, eid, 8);
    while (f.size() < 82) f.push_back(0);
    return f;
}

static void feed(const std::vector<uint8_t>& f) {
    int n = f.size();
    for (int off = 0; off < n; off += 8) {
        uint64_t d = 0; uint8_t keep = 0;
        for (int l = 0; l < 8; l++)
            if (off + l < n) { d |= (uint64_t)f[off+l] << (8*l); keep |= (1<<l); }
        dut->rx_tvalid_i = 1;
        dut->rx_tdata_i  = d;
        dut->rx_tkeep_i  = keep;
        dut->rx_tlast_i  = (off + 8 >= n);
        tick_collect(nullptr);
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
    tick_collect(nullptr);
    tick_collect(nullptr);
}

static int r_msg(const std::vector<uint8_t>& b){ return b.size()>15 ? b[15]&0xF : -1; }
static int r_sta(const std::vector<uint8_t>& b){ return b.size()>16 ? b[16]>>3 : -1; }
static uint64_t r_be(const std::vector<uint8_t>& b, int off, int n) {
    uint64_t v = 0;
    for (int i = 0; i < n; i++) v = (v << 8) | b[off+i];
    return v;
}

// ---------------------------------------------------------------- ctx table
// acmp_lstn_ctx_t packed offsets (LSB first): ctlr[63:0] talker[127:64]
// sid[191:128] dmac[239:192] vlan[251:240] flags[267:252] tuid[283:268]
// tmr[297:284] adp_age[304:298] status[309:305] probing[311:310]
// tk_avail[312] active[313] state[316:314]
static uint32_t ctxw[10];

static uint64_t cbits(int lo, int width) {
    uint64_t v = 0;
    for (int i = width - 1; i >= 0; i--) {
        int b = lo + i;
        v = (v << 1) | ((ctxw[b >> 5] >> (b & 31)) & 1);
    }
    return v;
}
static uint64_t c_ctlr()   { return cbits(0, 64); }
static uint64_t c_talker() { return cbits(64, 64); }
static uint64_t c_sid()    { return cbits(128, 64); }
static uint64_t c_dmac()   { return cbits(192, 48); }
static uint64_t c_vlan()   { return cbits(240, 12); }
static uint64_t c_flags()  { return cbits(252, 16); }
static uint64_t c_tuid()   { return cbits(268, 16); }
static uint64_t c_status() { return cbits(305, 5); }
static uint64_t c_probing(){ return cbits(310, 2); }
static uint64_t c_state()  { return cbits(314, 3); }

static bool tbl_read(int idx) {
    dut->tbl_idx_i = idx;
    dut->tbl_req_i = 1;
    for (int c = 0; c < 100; c++) {
        tick();
        dut->eval();
        if (dut->tbl_gnt_o) {
            for (int w = 0; w < 10; w++) ctxw[w] = dut->tbl_ctx_o[w];
            dut->tbl_req_i = 0;
            tick();
            return true;
        }
    }
    dut->tbl_req_i = 0;
    return false;
}

// ------------------------------------------------------------ CSR bus stubs
static void csr_wr(uint32_t addr, uint32_t data) {
    dut->wr_addr_i = addr; dut->wr_data_i = data; dut->wr_p_i = 1;
    tick_collect(nullptr);
    dut->wr_p_i = 0;
    tick_collect(nullptr);
}
static uint32_t csr_rd(uint32_t addr) {
    dut->rd_addr_i = addr; dut->eval();
    return dut->rd_data_o;
}

#define A_JNL_CTRL 0x7B8u
#define A_JNL_DATA 0x7BCu
#define A_JNL_STAT 0x7C0u
#define A_JNL_SEQ  0x7C4u

// verdict codes (KL_persist_journal VD_*)
enum { VD_NONE=0, VD_ACCEPT=1, VD_MAGIC=2, VD_VER=3, VD_SHAPE=4,
       VD_LEN=5, VD_CRC=6, VD_ENT=7, VD_STALE=8 };

static int  st_verdict(uint32_t s) { return (s >> 4) & 0xF; }
static int  st_nrec(uint32_t s)    { return (s >> 8) & 0xF; }
static int  st_nok(uint32_t s)     { return (s >> 12) & 0xF; }
static int  st_refused(uint32_t s) { return (s >> 16) & 0xFF; }
static int  st_busy(uint32_t s)    { return (s >> 31) & 1; }
static int  st_done(uint32_t s)    { return (s >> 30) & 1; }

// -------------------------------------------------------------- journal image
// CRC-32/ISO-HDLC, identical to Python `zlib.crc32` over the same bytes.
static uint32_t crc32_bytes(const uint8_t* p, size_t n) {
    uint32_t c = 0xFFFFFFFFu;
    for (size_t i = 0; i < n; i++) {
        c ^= p[i];
        for (int b = 0; b < 8; b++) c = (c & 1) ? ((c >> 1) ^ 0xEDB88320u) : (c >> 1);
    }
    return c ^ 0xFFFFFFFFu;
}

#define JNL_MAGIC 0x314A4C4Bu       // hexdump reads "KLJ1"
#define JNL_VER   0x00010000u       // major 1, minor 0
#define REC_W     6u

struct JRec {
    uint64_t talker;
    uint16_t tuid;
    uint16_t vlan;
    uint64_t ctlr;
    uint16_t flags;
    uint8_t  idx;
    bool     valid;
};

//! encode one journal slot image: header, records, CRC-32 trailer
static std::vector<uint32_t> build_slot(uint32_t seq, uint64_t entity,
                                        const std::vector<JRec>& recs,
                                        uint32_t ver = JNL_VER,
                                        uint32_t magic = JNL_MAGIC,
                                        uint32_t rec_w = REC_W,
                                        int n_rec_override = -1) {
    std::vector<uint32_t> w;
    int n_rec = (n_rec_override >= 0) ? n_rec_override : (int)recs.size();
    w.push_back(magic);
    w.push_back(ver);
    w.push_back(seq);
    w.push_back(((rec_w & 0xFF) << 8) | (n_rec & 0xFF));
    w.push_back((uint32_t)(entity & 0xFFFFFFFFu));
    w.push_back((uint32_t)(entity >> 32));
    for (const JRec& r : recs) {
        w.push_back((uint32_t)(r.talker & 0xFFFFFFFFu));
        w.push_back((uint32_t)(r.talker >> 32));
        w.push_back(((uint32_t)(r.vlan & 0xFFF) << 16) | r.tuid);
        w.push_back((uint32_t)(r.ctlr & 0xFFFFFFFFu));
        w.push_back((uint32_t)(r.ctlr >> 32));
        w.push_back((r.valid ? (1u << 30) : 0u) |
                    ((uint32_t)r.flags << 8) | (r.idx & 0xF));
    }
    // CRC over the byte stream exactly as it lands in flash (LE words)
    std::vector<uint8_t> b;
    for (uint32_t x : w) { b.push_back(x & 0xFF); b.push_back((x >> 8) & 0xFF);
                           b.push_back((x >> 16) & 0xFF); b.push_back((x >> 24) & 0xFF); }
    w.push_back(crc32_bytes(b.data(), b.size()));
    return w;
}

//! push one slot image through the CSR ingest group and wait for the verdict
static uint32_t push_slot(const std::vector<uint32_t>& img, int drop_tail = 0) {
    csr_wr(A_JNL_CTRL, 0x1);                     // start
    int n = (int)img.size() - drop_tail;
    for (int i = 0; i < n; i++) csr_wr(A_JNL_DATA, img[i]);
    csr_wr(A_JNL_CTRL, 0x2);                     // end -> verify (+ replay)
    for (int c = 0; c < 4000; c++) {
        uint32_t s = csr_rd(A_JNL_STAT);
        if (!st_busy(s)) return s;
        tick_collect(nullptr);
    }
    return csr_rd(A_JNL_STAT);
}

static const int MS = 10;   // scaled clock: 1 ms = 10 cycles

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new Vpersist_wrap;

    dut->rst_n = 0;
    dut->entity_id_i = US_EID;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|US_MAC[i]; dut->station_mac_i = m; }
    dut->tick_1s_i = 0;
    dut->ta_registered_i = 0; dut->ta_failed_i = 0;
    dut->tbl_req_i = 0; dut->tbl_idx_i = 0;
    dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    dut->wr_addr_i = 0; dut->wr_data_i = 0; dut->wr_p_i = 0; dut->rd_addr_i = 0;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 8; i++) tick();   // ctx-RAM init walk

    printf("== persistence journal -> ACMP bind-restore (N=4, SM mask 1101) ==\n");

    const JRec R0 = { T1_EID, 0x0003, 2, CT_EID, 0x0008, 0, true };
    const JRec R2 = { T2_EID, 0x0005, 2, CT_EID, 0x0000, 2, true };
    const JRec R3 = { T3_EID, 0x0007, 2, CT_EID, 0x0008, 3, true };
    const JRec RREC1 = { T3_EID, 0x0001, 2, CT_EID, 0x0000, 1, true }; // record-only ctx
    const JRec RHOLE = { 0, 0, 0, 0, 0, 3, false };                    // VALID=0

    // ---------------------------------------------------------------- //
    printf("\n[J0] status after reset: idle, no verdict\n");
    {
        uint32_t s = csr_rd(A_JNL_STAT);
        ck("[J0] not busy", st_busy(s), 0);
        ck("[J0] no verdict yet (done=0)", st_done(s), 0);
        ck("[J0] verdict NONE", st_verdict(s), VD_NONE);
        ck("[J0] accepted SEQ 0", (long)csr_rd(A_JNL_SEQ), 0);
    }
    {
        // FORMAT GOLDEN. The one-record slot used by [J3] below, byte-for-byte.
        // The trailer is `zlib.crc32` of the first 48 bytes - pinned here so a
        // refactor of either side (this encoder, the fabric digest, or the
        // on-board journal writer) cannot silently change the on-flash format.
        auto g = build_slot(5, US_EID, {R0});
        ck("[J0] golden slot is 13 words (6 hdr + 6 rec + CRC)", (long)g.size(), 13);
        ckh("[J0] magic word hexdumps as 'KLJ1'", g[0], JNL_MAGIC);
        ckh("[J0] SHAPE = {rec_words 6, n_rec 1}", g[3], 0x0601u);
        ckh("[J0] record CMD word {VALID, flags, idx}", g[11], 0x40000800u);
        ckh("[J0] CRC-32 trailer == zlib.crc32", g[12], 0xC1EBD52Au);
    }

    // ---------------------------------------------------------------- //
    printf("\n[J1] structural rejections leave the table untouched\n");
    long edges0 = rest_edges;
    {   // an ERASED flash slot reads all-ones
        std::vector<uint32_t> img(20, 0xFFFFFFFFu);
        uint32_t s = push_slot(img);
        ck("[J1] erased slot -> VD_MAGIC", st_verdict(s), VD_MAGIC);
    }
    {   // a journal written by a future format
        auto img = build_slot(1, US_EID, {R0}, 0x00020000u);
        ck("[J1] format major 2 -> VD_VER", st_verdict(push_slot(img)), VD_VER);
    }
    {   // record grew: rec_words 8 is NOT parsed as 6
        auto img = build_slot(1, US_EID, {R0}, JNL_VER, JNL_MAGIC, 8);
        ck("[J1] rec_words 8 -> VD_SHAPE", st_verdict(push_slot(img)), VD_SHAPE);
    }
    {   // more records than the engine can stage
        auto img = build_slot(1, US_EID, {R0}, JNL_VER, JNL_MAGIC, REC_W, 9);
        ck("[J1] n_rec 9 > MAX_REC_P -> VD_SHAPE", st_verdict(push_slot(img)), VD_SHAPE);
    }
    {   // n_rec 0: a header with nothing to replay is not a journal
        auto img = build_slot(1, US_EID, {}, JNL_VER, JNL_MAGIC, REC_W, 0);
        ck("[J1] n_rec 0 -> VD_SHAPE", st_verdict(push_slot(img)), VD_SHAPE);
    }
    {   // transfer cut short (power lost mid-read, short mtd read, ...)
        auto img = build_slot(1, US_EID, {R0, R2});
        ck("[J1] truncated transfer -> VD_LEN", st_verdict(push_slot(img, 5)), VD_LEN);
    }
    {   // the image says 1 record but 2 were pushed
        auto img = build_slot(1, US_EID, {R0, R2}, JNL_VER, JNL_MAGIC, REC_W, 1);
        ck("[J1] overlong transfer -> VD_LEN", st_verdict(push_slot(img)), VD_LEN);
    }
    {   // rootfs cloned onto a second board: the journal is not ours
        auto img = build_slot(1, FOREIGN_EID, {R0});
        ck("[J1] foreign entity_id -> VD_ENT", st_verdict(push_slot(img)), VD_ENT);
    }
    ck("[J1] ZERO restore transactions from any of them", rest_edges - edges0, 0);
    for (int i = 0; i < 4; i++) {
        tbl_read(i);
        ck("[J1] ctx still UNBOUND", (long)c_state(), 0);
    }
    ck("[J1] accepted-SEQ watermark still 0", (long)csr_rd(A_JNL_SEQ), 0);

    // ---------------------------------------------------------------- //
    printf("\n[J2] TORN JOURNAL: one flipped bit -> rejected WHOLE\n");
    // 3 records, all targeting probe-SM sinks. Corrupt the LAST record only:
    // a streaming applier would already have injected records 0 and 1 by the
    // time it reached the damage. Nothing may be applied.
    long edges1 = rest_edges;
    {
        auto img = build_slot(4, US_EID, {R0, R2, R3});
        size_t tail = img.size() - 2;             // last record's CMD word
        img[tail] ^= 0x00000100u;                 // flip one flags bit
        uint32_t s = push_slot(img);
        ck("[J2] CRC no longer closes -> VD_CRC", st_verdict(s), VD_CRC);
        ck("[J2] no records counted", st_nrec(s), 0);
        ck("[J2] no records injected", st_nok(s), 0);
    }
    {   // damage in the HEADER's SEQ word: same verdict, still nothing applied
        auto img = build_slot(4, US_EID, {R0, R2, R3});
        img[2] ^= 0x00000001u;
        ck("[J2] flipped SEQ bit -> VD_CRC", st_verdict(push_slot(img)), VD_CRC);
    }
    {   // damage in the CRC TRAILER itself (the classic torn last page)
        auto img = build_slot(4, US_EID, {R0, R2, R3});
        img[img.size()-1] ^= 0x80000000u;
        ck("[J2] flipped CRC trailer -> VD_CRC", st_verdict(push_slot(img)), VD_CRC);
    }
    ck("[J2] ZERO restore transactions from a torn image", rest_edges - edges1, 0);
    for (int i = 0; i < 4; i++) {
        tbl_read(i);
        ck("[J2] ctx NOT half-applied (still UNBOUND)", (long)c_state(), 0);
    }
    ck("[J2] watermark untouched by a rejection", (long)csr_rd(A_JNL_SEQ), 0);

    // ---------------------------------------------------------------- //
    printf("\n[J3] a good slot replays the 5.5.3.5.2 entry record\n");
    {
        auto img = build_slot(5, US_EID, {R0});
        uint32_t s = push_slot(img);
        ck("[J3] verdict ACCEPT", st_verdict(s), VD_ACCEPT);
        ck("[J3] 1 record in the image", st_nrec(s), 1);
        ck("[J3] 1 record injected", st_nok(s), 1);
        ck("[J3] no refusals", st_refused(s), 0);
        ck("[J3] done latched", st_done(s), 1);
        ck("[J3] accepted SEQ published", (long)csr_rd(A_JNL_SEQ), 5);
    }
    tbl_read(0);
    ck("[J3] ctx0 state PRB_W_AVAIL (step 3)", (long)c_state(), 1);
    ck("[J3] probing PASSIVE (step 2)",        (long)c_probing(), 1);
    ck("[J3] ACMP status 0 (step 2)",          (long)c_status(), 0);
    ckh("[J3] talker_entity_id from flash",    c_talker(), T1_EID);
    ck("[J3] talker_unique_id from flash",     (long)c_tuid(), 3);
    ckh("[J3] controller_entity_id (5.5.3.5.3)", c_ctlr(), CT_EID);
    ck("[J3] STREAMING_WAIT flag preserved",   (long)c_flags(), 0x0008);
    ckh("[J3] stream_id CLEARED (5.5.2.6 s1)", c_sid(), 0);
    ckh("[J3] dest MAC CLEARED",               c_dmac(), 0);
    ck("[J3] VLAN CLEARED (re-probed, not restored)", (long)c_vlan(), 0);
    ck("[J3] sink not yet active",             dut->stream_active_o & 1, 0);
    tbl_read(1); ck("[J3] untargeted ctx1 untouched", (long)c_state(), 0);
    tbl_read(2); ck("[J3] untargeted ctx2 untouched", (long)c_state(), 0);

    // ---------------------------------------------------------------- //
    printf("\n[J4] the restored sink fast-connects with NO controller\n");
    feed(adp(0, T1_EID));                       // talker becomes ADP-visible
    run(8);
    tbl_read(0);
    ck("[J4] ENTITY_AVAILABLE -> PRB_W_DELAY (5.5.1.4)", (long)c_state(), 2);
    uint16_t j4_seq = 0;
    {
        auto p = wait_frame(1100 * MS);
        ck("[J4] PROBE_TX emitted after the delay", p.size(), 70);
        ck("[J4] message is CONNECT_TX_COMMAND", r_msg(p), 0);
        ckh("[J4] probe talker = the saved talker", r_be(p, 34, 8), T1_EID);
        ck("[J4] probe tuid = the saved tuid", (long)r_be(p, 50, 2), 3);
        ckh("[J4] probe ctlr = the saved controller", r_be(p, 26, 8), CT_EID);
        ck("[J4] probe luid = the saved sink index", (long)r_be(p, 52, 2), 0);
        j4_seq = (uint16_t)r_be(p, 62, 2);   // 5.5.3.5.18 s1: echo it back
    }
    {
        const uint8_t dmR[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x99};
        feed(acmp(1, 0, 0x1234432112344321ULL, CT_EID, T1_EID, US_EID, 3, 0,
                  dmR, j4_seq, 0, 2));
    }
    tbl_read(0);
    ck("[J4] SETTLED after the probe response", (long)c_state(), 6);
    ckh("[J4] stream_id re-learned from the wire", c_sid(), 0x1234432112344321ULL);
    ckh("[J4] dest MAC re-learned",                c_dmac(), 0x91E0F000FE99ULL);
    ck("[J4] VLAN re-learned",                     (long)c_vlan(), 2);
    ck("[J4] BOUND LISTENER: sink active",         dut->stream_active_o & 1, 1);

    // ---------------------------------------------------------------- //
    printf("\n[J5] STALE guard: an older slot cannot roll the bind back\n");
    {
        auto img = build_slot(4, US_EID, {R2});
        uint32_t s = push_slot(img);
        ck("[J5] SEQ 4 <= accepted 5 -> VD_STALE", st_verdict(s), VD_STALE);
        ck("[J5] watermark unchanged", (long)csr_rd(A_JNL_SEQ), 5);
    }
    tbl_read(2); ck("[J5] its target ctx2 untouched", (long)c_state(), 0);
    {   // equal SEQ is not newer either (idempotent re-push is a no-op)
        auto img = build_slot(5, US_EID, {R2});
        ck("[J5] SEQ 5 == accepted 5 -> VD_STALE", st_verdict(push_slot(img)), VD_STALE);
    }

    // ---------------------------------------------------------------- //
    printf("\n[J6] multi-record replay + per-record refusal accounting\n");
    {
        // ctx2 free (injects), ctx1 is a RECORD-ONLY context (status 2),
        // ctx0 is now SETTLED (status 1 - only a controller rebinds it),
        // plus a VALID=0 hole that must be skipped silently.
        auto img = build_slot(9, US_EID, {R2, RREC1, R0, RHOLE});
        uint32_t s = push_slot(img);
        ck("[J6] verdict ACCEPT", st_verdict(s), VD_ACCEPT);
        ck("[J6] 4 records in the image", st_nrec(s), 4);
        ck("[J6] 1 injected (ctx2 only)", st_nok(s), 1);
        ck("[J6] refusal bitmap = records 1 and 2", st_refused(s), 0x6);
        ck("[J6] watermark advances to 9", (long)csr_rd(A_JNL_SEQ), 9);
    }
    tbl_read(2);
    ck("[J6] ctx2 restored (PRB_W_AVAIL)", (long)c_state(), 1);
    ckh("[J6] ctx2 talker from flash", c_talker(), T2_EID);
    ck("[J6] ctx2 tuid from flash", (long)c_tuid(), 5);
    tbl_read(1);
    ck("[J6] record-only ctx1 refused, untouched", (long)c_state(), 0);
    tbl_read(0);
    ck("[J6] OCCUPIED ctx0 refused, still SETTLED", (long)c_state(), 6);
    ckh("[J6] ctx0 stream_id survived the refusal", c_sid(), 0x1234432112344321ULL);
    tbl_read(3);
    ck("[J6] the VALID=0 hole left ctx3 alone", (long)c_state(), 0);

    // ---------------------------------------------------------------- //
    printf("\n[J7] A/B fall-back: a rejection never blocks the older slot\n");
    {   // slot A is the newer generation but was torn mid-write
        auto a = build_slot(20, US_EID, {R3});
        a[7] ^= 0x00000010u;
        uint32_t s = push_slot(a);
        ck("[J7] torn slot A (SEQ 20) -> VD_CRC", st_verdict(s), VD_CRC);
        ck("[J7] watermark still 9 (never advanced by a reject)",
           (long)csr_rd(A_JNL_SEQ), 9);
    }
    tbl_read(3); ck("[J7] ctx3 untouched by the torn slot", (long)c_state(), 0);
    {   // slot B is intact and still beats the watermark
        auto b = build_slot(10, US_EID, {R3});
        uint32_t s = push_slot(b);
        ck("[J7] intact slot B (SEQ 10) -> ACCEPT", st_verdict(s), VD_ACCEPT);
        ck("[J7] 1 record injected", st_nok(s), 1);
        ck("[J7] watermark 10", (long)csr_rd(A_JNL_SEQ), 10);
    }
    tbl_read(3);
    ck("[J7] ctx3 restored from the fall-back slot", (long)c_state(), 1);
    ckh("[J7] ctx3 talker", c_talker(), T3_EID);
    ck("[J7] ctx3 tuid", (long)c_tuid(), 7);
    ck("[J7] ctx3 STREAMING_WAIT preserved", (long)c_flags(), 0x0008);

    // ---------------------------------------------------------------- //
    printf("\n[J8] ABORT recovers a load left half-pushed\n");
    {
        auto img = build_slot(30, US_EID, {R2});
        csr_wr(A_JNL_CTRL, 0x1);
        for (int i = 0; i < 4; i++) csr_wr(A_JNL_DATA, img[i]);
        uint32_t s = csr_rd(A_JNL_STAT);
        ck("[J8] busy mid-load", st_busy(s), 1);
        csr_wr(A_JNL_CTRL, 0x4);                       // abort
        s = csr_rd(A_JNL_STAT);
        ck("[J8] abort -> idle", st_busy(s), 0);
        ck("[J8] watermark preserved across abort", (long)csr_rd(A_JNL_SEQ), 10);
        // and the engine is usable again straight away
        ck("[J8] a fresh push still verifies", st_verdict(push_slot(img)), VD_ACCEPT);
        ck("[J8] watermark 30", (long)csr_rd(A_JNL_SEQ), 30);
    }

    printf("\npersistence journal: %ld checks, %ld failures\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
