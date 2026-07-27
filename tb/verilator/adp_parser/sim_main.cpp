/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for KL_adp_parser.sv - the ADP receive
 * decapsulator. Until this suite existed the module had NO Verilator
 * coverage: its only testbench is the Vivado xsim one under
 * tb/utests/adp/kl-adp-parser/, so nothing in CI ever compiled the file,
 * which is precisely how an uncast enum assignment (%Error-ENUMVALUE at
 * KL_adp_parser.sv:81) survived. The Makefile deliberately omits -Wno-fatal
 * so that error is a BUILD FAILURE here, not a warning.
 *
 * STREAM CONTRACT (taken from the xsim stimulus, not invented): the beats
 * carry the frame starting at the ETHERTYPE - avtp_control_subtype's
 * avtp_packet_gen pushes ether_type[15:8], ether_type[7:0], subtype and
 * nothing before them - big-endian, byte 8n in tdata[63:56]. 70 bytes, so
 * nine beats, and the parser's `MAX_DATA_CNT_C = 8` counts the ninth.
 *
 *   [0..1]  EtherType 0x22F0        [38..41] available_index
 *   [2]     subtype   0xFA          [42..49] gptp_grandmaster_id
 *   [3]     h|ver|message_type[3:0] [50]     gptp_domain_number
 *   [4]     valid_time[4:0]|cdl[10:8]  [51]  reserved
 *   [5]     cdl[7:0]                [52..53] current_configuration_index
 *   [6..13]  entity_id              [54..55] identify_control_index
 *   [14..21] entity_model_id        [56..57] interface_index
 *   [22..25] entity_capabilities    [58..65] association_id
 *   [26..27] talker_stream_sources  [66..69] reserved
 *   [28..29] talker_capabilities
 *   [30..31] listener_stream_sinks
 *   [32..33] listener_capabilities
 *   [34..37] controller_capabilities
 *
 * Checks:
 *   adp01  AVAILABLE frame: every field byte-exact, available strobe only
 *   adp02  DEPARTING frame: departing strobe only, fields byte-exact
 *   adp03  DISCOVER  frame: discover  strobe only, fields byte-exact
 *   adp04  RESERVED (code 3, the named 4th member): valid, NO strobe
 *   adp05  code 0xF - OUTSIDE the enum's four members: valid, NO strobe, and
 *          the raw wire code SURVIVES on rcv_entity_info_o.adp_message_type.
 *          This is the check that pins the "cast, do not clamp" decision at
 *          KL_adp_parser.sv:81 - a guard folding 4..15 into RESERVED fails it.
 *   adp06  every reserved code 4..15 behaves the same way (no strobe, raw)
 *   adp07  back-to-back frames with no idle gap: the second parses too, and
 *          its values differ from the first (the field checks are not vacuous)
 *   adp08  entity_info_valid is exactly ONE cycle per frame, and no strobe
 *          fires before the frame completes
 *   adp09  association_id[15:0] lands ONE CYCLE AFTER the valid strobe - a
 *          real quirk of the FSM (case 8 assigns it on the same edge that
 *          clears the counter), pinned so it cannot silently change
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vadp_parser_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <vector>

static Vadp_parser_wrap* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-46s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    }
}

// ---------------------------------------------------------------- stimulus --

struct Adp {
    uint8_t  msg_type;      // RAW 4-bit wire code (not necessarily an enum member)
    uint8_t  valid_time;    // 5 bits
    uint16_t cdl;           // 11 bits
    uint64_t entity_id, entity_model_id;
    uint32_t entity_caps;
    uint16_t tss, tcap, lss, lcap;
    uint32_t ccap, avail_idx;
    uint64_t gm_id;
    uint8_t  domain, rsv0;
    uint16_t cfg_idx, ident_idx, if_idx;
    uint64_t assoc_id;
    uint32_t rsv1;
};

static const int FRAME_BYTES = 70;
static const int NBEATS      = (FRAME_BYTES + 7) / 8;   // 9

static void put(uint8_t* b, int off, int n, uint64_t v) {
    for (int i = 0; i < n; i++) b[off + i] = (uint8_t)(v >> (8 * (n - 1 - i)));
}

static void build(const Adp& a, uint8_t* b) {
    memset(b, 0, NBEATS * 8);
    b[0] = 0x22; b[1] = 0xF0;                      // EtherType
    b[2] = 0xFA;                                   // subtype ADP
    b[3] = (uint8_t)(a.msg_type & 0x0F);           // h=0, ver=0, message_type
    b[4] = (uint8_t)((a.valid_time << 3) | ((a.cdl >> 8) & 0x07));
    b[5] = (uint8_t)(a.cdl & 0xFF);
    put(b,  6, 8, a.entity_id);
    put(b, 14, 8, a.entity_model_id);
    put(b, 22, 4, a.entity_caps);
    put(b, 26, 2, a.tss);
    put(b, 28, 2, a.tcap);
    put(b, 30, 2, a.lss);
    put(b, 32, 2, a.lcap);
    put(b, 34, 4, a.ccap);
    put(b, 38, 4, a.avail_idx);
    put(b, 42, 8, a.gm_id);
    b[50] = a.domain; b[51] = a.rsv0;
    put(b, 52, 2, a.cfg_idx);
    put(b, 54, 2, a.ident_idx);
    put(b, 56, 2, a.if_idx);
    put(b, 58, 8, a.assoc_id);
    put(b, 66, 4, a.rsv1);
}

static uint64_t beat(const uint8_t* b, int k) {
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) v = (v << 8) | b[8 * k + i];
    return v;
}

//! deterministic, non-trivial field values (xorshift64* - fixed seed, so a
//! failure is reproducible and the frames are not all-zero/all-ones)
static uint64_t rng_s = 0x2026072700ADFA01ULL;
static uint64_t rnd() {
    rng_s ^= rng_s >> 12; rng_s ^= rng_s << 25; rng_s ^= rng_s >> 27;
    return rng_s * 0x2545F4914F6CDD1DULL;
}

static Adp mkadp(uint8_t mt) {
    Adp a;
    a.msg_type   = mt;
    a.valid_time = (uint8_t)(rnd() & 0x1F);
    a.cdl        = (uint16_t)(rnd() & 0x7FF);
    a.entity_id  = rnd();  a.entity_model_id = rnd();
    a.entity_caps = (uint32_t)rnd();
    a.tss  = (uint16_t)rnd(); a.tcap = (uint16_t)rnd();
    a.lss  = (uint16_t)rnd(); a.lcap = (uint16_t)rnd();
    a.ccap = (uint32_t)rnd(); a.avail_idx = (uint32_t)rnd();
    a.gm_id = rnd();
    a.domain = (uint8_t)rnd(); a.rsv0 = (uint8_t)rnd();
    a.cfg_idx = (uint16_t)rnd(); a.ident_idx = (uint16_t)rnd();
    a.if_idx = (uint16_t)rnd();
    a.assoc_id = rnd();
    a.rsv1 = (uint32_t)rnd();
    return a;
}

// ------------------------------------------------------------------ engine --

//! everything sampled on the cycle rcv_entity_info_o.entity_info_valid is high
struct Snap {
    bool     seen = false;
    int      valid_cycles = 0;    // how many cycles entity_info_valid was high
    int      disc = 0, avail = 0, dep = 0;   // strobe cycle counts
    uint8_t  msg_type = 0;
    uint8_t  valid_time = 0;
    uint64_t entity_id = 0, entity_model_id = 0;
    uint32_t entity_caps = 0;
    uint16_t tss = 0, tcap = 0, lss = 0, lcap = 0;
    uint32_t ccap = 0, avail_idx = 0;
    uint64_t gm_id = 0;
    uint8_t  domain = 0;
    uint16_t cfg_idx = 0, ident_idx = 0, if_idx = 0;
    uint64_t assoc_at_valid = 0;  // [15:0] still belongs to the PREVIOUS frame
    uint64_t assoc_after = 0;     // one cycle later: complete
    int      strobe_before_end = 0;
};

static void grab(Snap& s) {
    s.seen = true;
    s.msg_type        = dut->adp_message_type_o;
    s.valid_time      = dut->valid_time_o;
    s.entity_id       = dut->entity_id_o;
    s.entity_model_id = dut->entity_model_id_o;
    s.entity_caps     = dut->entity_capabilities_o;
    s.tss             = dut->talker_stream_sources_o;
    s.tcap            = dut->talker_capabilities_o;
    s.lss             = dut->listener_stream_sinks_o;
    s.lcap            = dut->listener_capabilities_o;
    s.ccap            = dut->controller_capabilities_o;
    s.avail_idx       = dut->available_index_o;
    s.gm_id           = dut->gptp_grandmaster_id_o;
    s.domain          = dut->gptp_domain_number_o;
    s.cfg_idx         = dut->current_configuration_index_o;
    s.ident_idx       = dut->identify_control_index_o;
    s.if_idx          = dut->interface_index_o;
    s.assoc_at_valid  = dut->association_id_o;
}

//! Drive `n` frames back to back (gap = idle cycles between them) through the
//! AXI4-Stream slave port, returning one Snap per frame.
static std::vector<Snap> drive(const std::vector<Adp>& frames, int gap) {
    std::vector<Snap> out(frames.size());
    std::vector<std::vector<uint8_t>> bytes;
    for (auto& a : frames) { bytes.emplace_back(NBEATS * 8); build(a, bytes.back().data()); }

    size_t fi = 0;          // frame cursor
    int    bi = 0;          // beat cursor within the frame
    int    idle = 0;        // idle cycles still owed before the next frame
    size_t done = 0;        // frames whose valid strobe has been seen
    int    post = -1;       // 0 = capture association_id next cycle
    size_t post_fi = 0;

    //! keep clocking for a few cycles after the LAST valid strobe: the
    //! association_id[15:0] write lands on the edge that ends the valid
    //! cycle, so the complete value is only readable the cycle after.
    int tail = 3;
    for (int c = 0; c < 4000; c++) {
        if (done >= frames.size() && tail-- <= 0) break;
        bool tv = false;
        if (idle > 0) { idle--; }
        else if (fi < frames.size()) {
            tv = true;
            dut->s_tdata = beat(bytes[fi].data(), bi);
            dut->s_tlast = (bi == NBEATS - 1);
        }
        if (!tv) { dut->s_tdata = 0; dut->s_tlast = 0; }
        dut->s_tvalid = tv;

        dut->clk = 0; dut->eval();

        // --- sample (pre-edge) --------------------------------------------
        if (post == 0) { out[post_fi].assoc_after = dut->association_id_o; post = 1; }
        if (dut->entity_info_valid_o) {
            size_t which = done < frames.size() ? done : frames.size() - 1;
            Snap& s = out[which];
            s.valid_cycles++;
            if (!s.seen) grab(s);
            post = 0; post_fi = which;
        }
        {
            size_t which = done < frames.size() ? done : frames.size() - 1;
            Snap& s = out[which];
            if (dut->rcv_adp_discover_o)  s.disc++;
            if (dut->rcv_adp_available_o) s.avail++;
            if (dut->rcv_adp_departing_o) s.dep++;
            if (!dut->entity_info_valid_o &&
                (dut->rcv_adp_discover_o || dut->rcv_adp_available_o ||
                 dut->rcv_adp_departing_o))
                s.strobe_before_end++;
        }
        bool hs         = tv && dut->s_tready;
        bool frame_over = dut->entity_info_valid_o;

        dut->clk = 1; dut->eval();

        if (hs) {
            if (++bi == NBEATS) { bi = 0; fi++; idle = gap; }
        }
        if (frame_over) done++;
    }
    dut->s_tvalid = 0; dut->s_tlast = 0; dut->s_tdata = 0;
    for (int c = 0; c < 4; c++) { dut->clk = 0; dut->eval(); dut->clk = 1; dut->eval(); }
    return out;
}

static void reset() {
    dut->rst_n = 0; dut->s_tvalid = 0; dut->s_tlast = 0; dut->s_tdata = 0;
    for (int c = 0; c < 4; c++) { dut->clk = 0; dut->eval(); dut->clk = 1; dut->eval(); }
    dut->rst_n = 1;
    for (int c = 0; c < 2; c++) { dut->clk = 0; dut->eval(); dut->clk = 1; dut->eval(); }
}

//! Full field comparison for one parsed frame against the bytes that were sent.
static void check_fields(const char* tag, const Adp& a, const Snap& s) {
    char n[128];
#define CK(field, got, exp) \
    do { snprintf(n, sizeof n, "%s: %s", tag, field); ck(n, (got), (exp)); } while (0)
    CK("entity_info_valid seen",     s.seen ? 1 : 0,       1);
    if (!s.seen) return;
    CK("adp_message_type (RAW wire)", s.msg_type,          a.msg_type & 0x0F);
    CK("valid_time",                 s.valid_time,         a.valid_time);
    CK("entity_id",                  s.entity_id,          a.entity_id);
    CK("entity_model_id",            s.entity_model_id,    a.entity_model_id);
    CK("entity_capabilities",        s.entity_caps,        a.entity_caps);
    CK("talker_stream_sources",      s.tss,                a.tss);
    CK("talker_capabilities",        s.tcap,               a.tcap);
    CK("listener_stream_sinks",      s.lss,                a.lss);
    CK("listener_capabilities",      s.lcap,               a.lcap);
    CK("controller_capabilities",    s.ccap,               a.ccap);
    CK("available_index",            s.avail_idx,          a.avail_idx);
    CK("gptp_grandmaster_id",        s.gm_id,              a.gm_id);
    CK("gptp_domain_number",         s.domain,             a.domain);
    CK("current_configuration_index", s.cfg_idx,           a.cfg_idx);
    CK("identify_control_index",     s.ident_idx,          a.ident_idx);
    CK("interface_index",            s.if_idx,             a.if_idx);
    CK("association_id[63:16] @valid", s.assoc_at_valid >> 16, a.assoc_id >> 16);
    CK("association_id complete @valid+1", s.assoc_after,   a.assoc_id);
    CK("entity_info_valid is 1 cycle", s.valid_cycles,     1);
    CK("no strobe before frame end", s.strobe_before_end,  0);
#undef CK
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vadp_parser_wrap;

    printf("== KL_adp_parser Verilator suite ==\n");

    // ---- adp01/02/03: the three legal message types ----------------------
    struct { const char* tag; uint8_t code; int d, a, p; } legal[] = {
        {"adp01 AVAILABLE", 0, 0, 1, 0},
        {"adp02 DEPARTING", 1, 0, 0, 1},
        {"adp03 DISCOVER",  2, 1, 0, 0},
    };
    for (auto& L : legal) {
        reset();
        Adp a = mkadp(L.code);
        std::vector<Snap> s = drive({a}, /*gap=*/3);
        check_fields(L.tag, a, s[0]);
        char n[128];
        snprintf(n, sizeof n, "%s: discover strobe cycles",  L.tag); ck(n, s[0].disc,  L.d);
        snprintf(n, sizeof n, "%s: available strobe cycles", L.tag); ck(n, s[0].avail, L.a);
        snprintf(n, sizeof n, "%s: departing strobe cycles", L.tag); ck(n, s[0].dep,   L.p);
    }

    // ---- adp04: RESERVED (3) is a NAMED member and still strobes nothing --
    {
        reset();
        Adp a = mkadp(3);
        std::vector<Snap> s = drive({a}, 3);
        check_fields("adp04 RESERVED(3)", a, s[0]);
        ck("adp04: no discover strobe",  s[0].disc,  0);
        ck("adp04: no available strobe", s[0].avail, 0);
        ck("adp04: no departing strobe", s[0].dep,   0);
    }

    // ---- adp05: 0xF is OUTSIDE the enum. THE DECISION CHECK. -------------
    // The cast at KL_adp_parser.sv:81 is a static cast, NOT a clamp: the raw
    // wire code must come back out untouched. A guard folding 4..15 into
    // RESERVED (=3) fails exactly this line and nothing else - which is what
    // makes it mutation evidence for the decision rather than for the cast.
    {
        reset();
        Adp a = mkadp(0xF);
        std::vector<Snap> s = drive({a}, 3);
        ck("adp05: entity_info_valid still raised",  s[0].seen ? 1 : 0, 1);
        ck("adp05: RESERVED wire code 0xF SURVIVES", s[0].msg_type,     0xF);
        ck("adp05: no discover strobe",              s[0].disc,         0);
        ck("adp05: no available strobe",             s[0].avail,        0);
        ck("adp05: no departing strobe",             s[0].dep,          0);
        check_fields("adp05 code 0xF", a, s[0]);
    }

    // ---- adp06: every reserved code 4..15 behaves identically ------------
    for (uint8_t code = 4; code <= 15; code++) {
        reset();
        Adp a = mkadp(code);
        std::vector<Snap> s = drive({a}, 2);
        char n[96];
        snprintf(n, sizeof n, "adp06 code 0x%X: raw code preserved", code);
        ck(n, s[0].msg_type, code);
        snprintf(n, sizeof n, "adp06 code 0x%X: zero strobes", code);
        ck(n, s[0].disc + s[0].avail + s[0].dep, 0);
        snprintf(n, sizeof n, "adp06 code 0x%X: entity_info_valid raised", code);
        ck(n, s[0].seen ? 1 : 0, 1);
    }

    // ---- adp07: back-to-back frames, zero idle gap -----------------------
    {
        reset();
        Adp a0 = mkadp(0), a1 = mkadp(2), a2 = mkadp(1);
        std::vector<Snap> s = drive({a0, a1, a2}, /*gap=*/0);
        check_fields("adp07 f0", a0, s[0]);
        check_fields("adp07 f1", a1, s[1]);
        check_fields("adp07 f2", a2, s[2]);
        ck("adp07 f0: available strobe", s[0].avail, 1);
        ck("adp07 f1: discover strobe",  s[1].disc,  1);
        ck("adp07 f2: departing strobe", s[2].dep,   1);
        // NEGATIVE / teeth: the three frames must actually carry different
        // payloads, or every field comparison above would pass on a parser
        // that simply latched once and never updated.
        ck("adp07: f0 != f1 entity_id (checks not vacuous)",
           (s[0].entity_id != s[1].entity_id) ? 1 : 0, 1);
        ck("adp07: f1 != f2 entity_id (checks not vacuous)",
           (s[1].entity_id != s[2].entity_id) ? 1 : 0, 1);
        ck("adp07: f0 != f1 association_id",
           (s[0].assoc_after != s[1].assoc_after) ? 1 : 0, 1);
        // and a stale-by-one-frame parser (the classic re-arm bug) would
        // report f0's entity_id on f1: assert it does not.
        ck("adp07: NOT stale-by-one-frame",
           (s[1].entity_id == s[0].entity_id) ? 1 : 0, 0);
    }

    // ---- adp08/adp09 are folded into check_fields (valid_cycles == 1,
    //      strobe_before_end == 0, association_id split across the edge).

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
