/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking harness for KL_lwsrp_rx.sv — the lwSRP receive chain
 * (monitor tap -> packet FIFO -> streaming walker -> registrar).
 *
 * Bridge-side MRPDUs are hand-built the way a real 802.1Q bridge emits them
 * (multi-value vectors, multiple messages per PDU, LeaveAll headers, padding)
 * and driven through the un-backpressurable monitor tap at full beat rate.
 *
 * Contract under test (docs/LWSRP_FPGA_ARCHITECTURE.md §1/§6):
 *  - Listener Ready/AskingFailed/ReadyFailed for OUR StreamID register with
 *    the four-packed declaration; listener_ready only on Ready/ReadyFailed.
 *  - THE +k TRAP: value k of a vector is FirstValue incremented k times —
 *    vectors spanning our StreamID at an offset must match at exactly k,
 *    picking the right three-packed AND four-packed positions.
 *  - Vectors not covering our StreamID are ignored.
 *  - Lv / LeaveAll arm the 600 ms leave timer; un-refreshed registration
 *    ages out; a JoinIn before expiry cancels it. LeaveAll storms don't
 *    wedge the parser and pulse rx_leaveall_p_o once per PDU.
 *  - Domain: {class 6, prio 3, our VID} keeps domain_ok; a class-6 mismatch
 *    clears it (boundary); a match or age-out restores it; class-B ignored.
 *  - TalkerFailed covering our StreamID captures the failure code sticky;
 *    a TalkerAdvertise re-declare clears it; foreign StreamIDs are ignored.
 *  - Framing: endmark-terminated parsing (AttributeListLength never trusted),
 *    zero-padding tolerated, malformed/truncated PDUs abort silently and the
 *    next frame parses clean; non-SRP frames never enter the FIFO.
 */

#include "VKL_lwsrp_rx.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static VKL_lwsrp_rx* dut;
static long checks = 0, fails = 0;
static long la_pulses = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-46s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    }
}

static const uint64_t STATION = 0x020000000002ULL;
static const uint16_t UID     = 0;
static const uint64_t OUR_SID = (STATION << 16) | UID;
static const uint16_t VID     = 2;
static const uint64_t BRIDGE  = 0x3CC0C6000001ULL;

static void lo() { dut->clk_i = 0; dut->eval(); }
static void hi() {
    dut->clk_i = 1; dut->eval();
    if (dut->rx_leaveall_p_o) la_pulses++;
}
static void step() { lo(); hi(); }
static void tick() { dut->tick_1khz_i = 1; step(); dut->tick_1khz_i = 0; step(); }
static void ticks(int n) { for (int i = 0; i < n; i++) tick(); }

static void put_be(std::vector<uint8_t>& b, uint64_t v, int n) {
    for (int i = n - 1; i >= 0; i--) b.push_back((v >> (8 * i)) & 0xFF);
}

// ---- MRPDU builders ------------------------------------------------------

// MRP AttributeEvents / Listener declarations
enum { EV_NEW = 0, EV_JOININ = 1, EV_IN = 2, EV_JOINMT = 3, EV_MT = 4, EV_LV = 5 };
enum { D_IGN = 0, D_ASKFAIL = 1, D_READY = 2, D_READYFAIL = 3 };

struct Vec {
    int lva = 0;
    int nv  = 1;
    std::vector<uint8_t> fv;
    std::vector<int> evts;               // per value; padded with 0
    std::vector<int> pars;               // listener only
};

struct Msg {
    int type;
    int len;
    bool msrp;                           // has AttributeListLength
    std::vector<Vec> vecs;
};

static std::vector<uint8_t> encode_msg(const Msg& m) {
    std::vector<uint8_t> body;
    for (const auto& v : m.vecs) {
        put_be(body, (uint64_t)((v.lva << 13) | v.nv), 2);
        body.insert(body.end(), v.fv.begin(), v.fv.end());
        int ne = (v.nv + 2) / 3;
        for (int i = 0; i < ne; i++) {
            int e0 = (3*i   < (int)v.evts.size()) ? v.evts[3*i]   : 0;
            int e1 = (3*i+1 < (int)v.evts.size()) ? v.evts[3*i+1] : 0;
            int e2 = (3*i+2 < (int)v.evts.size()) ? v.evts[3*i+2] : 0;
            body.push_back((uint8_t)(e0*36 + e1*6 + e2));
        }
        if (m.msrp && m.type == 3) {
            int np = (v.nv + 3) / 4;
            for (int i = 0; i < np; i++) {
                int p0 = (4*i   < (int)v.pars.size()) ? v.pars[4*i]   : 0;
                int p1 = (4*i+1 < (int)v.pars.size()) ? v.pars[4*i+1] : 0;
                int p2 = (4*i+2 < (int)v.pars.size()) ? v.pars[4*i+2] : 0;
                int p3 = (4*i+3 < (int)v.pars.size()) ? v.pars[4*i+3] : 0;
                body.push_back((uint8_t)(p0*64 + p1*16 + p2*4 + p3));
            }
        }
    }
    put_be(body, 0, 2);                  // vector-list EndMark
    std::vector<uint8_t> out;
    out.push_back((uint8_t)m.type);
    out.push_back((uint8_t)m.len);
    if (m.msrp) put_be(out, body.size(), 2);   // AttributeListLength
    out.insert(out.end(), body.begin(), body.end());
    return out;
}

static std::vector<uint8_t> frame(bool msrp, const std::vector<Msg>& msgs,
                                  int pad_to = 60) {
    std::vector<uint8_t> f;
    put_be(f, msrp ? 0x0180C200000EULL : 0x0180C2000021ULL, 6);
    put_be(f, BRIDGE, 6);
    put_be(f, msrp ? 0x22EA : 0x88F5, 2);
    f.push_back(0);                      // ProtocolVersion
    for (const auto& m : msgs) {
        auto mb = encode_msg(m);
        f.insert(f.end(), mb.begin(), mb.end());
    }
    put_be(f, 0, 2);                     // message-list EndMark
    while ((int)f.size() < pad_to) f.push_back(0);
    return f;
}

// FirstValue helpers
static std::vector<uint8_t> fv_listener(uint64_t base_sid) {
    std::vector<uint8_t> v; put_be(v, base_sid, 8); return v;
}
static std::vector<uint8_t> fv_domain(int cls, int prio, int vid) {
    std::vector<uint8_t> v;
    v.push_back(cls); v.push_back(prio); put_be(v, vid, 2);
    return v;
}
static std::vector<uint8_t> fv_talker(uint64_t sid) {          // 25 B
    std::vector<uint8_t> v; put_be(v, sid, 8);
    for (int i = 0; i < 17; i++) v.push_back(0xA0 + i);
    return v;
}
static std::vector<uint8_t> fv_tfail(uint64_t sid, uint8_t code) { // 34 B
    auto v = fv_talker(sid);
    put_be(v, BRIDGE << 16, 8);          // BridgeID
    v.push_back(code);
    return v;
}

static Msg msg_listener(const Vec& v) { return {3, 8,  true,  {v}}; }
static Msg msg_domain(const Vec& v)   { return {4, 4,  true,  {v}}; }
static Msg msg_tadv(const Vec& v)     { return {1, 25, true,  {v}}; }
static Msg msg_tfail(const Vec& v)    { return {2, 34, true,  {v}}; }
static Msg msg_vid(const Vec& v)      { return {1, 2,  false, {v}}; }

// drive the monitor tap at full rate (no backpressure exists)
static void feed(const std::vector<uint8_t>& f) {
    size_t n = f.size();
    for (size_t off = 0; off < n; off += 8) {
        uint64_t d = 0; uint8_t k = 0;
        for (int l = 0; l < 8 && off + l < n; l++) {
            d |= (uint64_t)f[off + l] << (8 * l);
            k |= 1 << l;
        }
        dut->rx_tvalid_i = 1; dut->rx_tdata_i = d; dut->rx_tkeep_i = k;
        dut->rx_tlast_i = (off + 8 >= n);
        step();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0;
    step();
}

// feed + wait until the walker has cleanly parsed it
static void feed_parse(const std::vector<uint8_t>& f, const char* what) {
    uint16_t before = dut->pdu_cnt_o;
    feed(f);
    int guard = 4000;
    while (dut->pdu_cnt_o == before && guard--) step();
    ck(what, dut->pdu_cnt_o, (uint16_t)(before + 1));
}

// feed something that must NOT parse cleanly; settle the walker
static void feed_noparse(const std::vector<uint8_t>& f, const char* what) {
    uint16_t before = dut->pdu_cnt_o;
    feed(f);
    for (int i = 0; i < 3000; i++) step();
    ck(what, dut->pdu_cnt_o, before);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_lwsrp_rx;

    dut->rst_n = 0; dut->enable_i = 0; dut->tick_1khz_i = 0;
    dut->rx_tvalid_i = 0; dut->rx_tdata_i = 0; dut->rx_tkeep_i = 0;
    dut->rx_tlast_i = 0;
    dut->station_mac_i = STATION; dut->unique_id_i = UID; dut->vid_i = VID;
    for (int i = 0; i < 4; i++) step();
    dut->rst_n = 1; dut->enable_i = 1;
    for (int i = 0; i < 2; i++) step();

    printf("== KL_lwsrp_rx harness (lwSRP ingress+walker+registrar) ==\n");

    // 0) baseline
    ck("idle: not registered", dut->listener_reg_o, 0);
    ck("idle: not ready", dut->listener_ready_o, 0);
    ck("idle: domain ok", dut->domain_ok_o, 1);
    ck("idle: no failure", dut->tfail_valid_o, 0);

    // 1) single-value Listener Ready for our StreamID
    {
        Vec v; v.fv = fv_listener(OUR_SID); v.evts = {EV_JOININ}; v.pars = {D_READY};
        feed_parse(frame(true, {msg_listener(v)}), "ready: clean parse");
        ck("ready: registered", dut->listener_reg_o, 1);
        ck("ready: listener_ready", dut->listener_ready_o, 1);
        ck("ready: declaration", dut->listener_decl_o, D_READY);
        ck("ready: rx_pdus counted", dut->rx_pdus_o, 1);
    }

    // 2) THE +k TRAP: our StreamID at value index 5 of a 9-value vector
    //    (event byte 1 position 2; param byte 1 position 1); every other
    //    value carries contradicting data that must NOT be picked up.
    {
        Vec v; v.nv = 9; v.fv = fv_listener(OUR_SID - 5);
        v.evts = {EV_LV, EV_LV, EV_LV, EV_LV, EV_LV, EV_JOININ, EV_LV, EV_LV, EV_LV};
        v.pars = {D_ASKFAIL, D_ASKFAIL, D_ASKFAIL, D_ASKFAIL,
                  D_ASKFAIL, D_READYFAIL, D_ASKFAIL, D_ASKFAIL, D_ASKFAIL};
        feed_parse(frame(true, {msg_listener(v)}), "+k: clean parse");
        ck("+k: still registered", dut->listener_reg_o, 1);
        ck("+k: declaration readyfail", dut->listener_decl_o, D_READYFAIL);
        ck("+k: ready (readyfail counts)", dut->listener_ready_o, 1);
    }

    // 3) larger offset crossing packed-byte boundaries: k = 11 of 13
    //    (event byte 3 position 2; param byte 2 position 3)
    {
        Vec v; v.nv = 13; v.fv = fv_listener(OUR_SID - 11);
        v.evts.assign(13, EV_MT); v.evts[11] = EV_IN;
        v.pars.assign(13, D_IGN); v.pars[11] = D_ASKFAIL;
        feed_parse(frame(true, {msg_listener(v)}), "k11: clean parse");
        ck("k11: registered (In refresh)", dut->listener_reg_o, 1);
        ck("k11: declaration askfail", dut->listener_decl_o, D_ASKFAIL);
        ck("k11: NOT ready (askfail)", dut->listener_ready_o, 0);
    }

    // 4) vector not covering our StreamID: no effect
    {
        Vec v; v.nv = 4; v.fv = fv_listener(OUR_SID + 1);
        v.evts.assign(4, EV_JOININ); v.pars.assign(4, D_READY);
        feed_parse(frame(true, {msg_listener(v)}), "miss-above: clean parse");
        Vec w; w.nv = 4; w.fv = fv_listener(OUR_SID - 4);
        w.evts.assign(4, EV_JOININ); w.pars.assign(4, D_READY);
        feed_parse(frame(true, {msg_listener(w)}), "miss-below: clean parse");
        ck("miss: declaration unchanged", dut->listener_decl_o, D_ASKFAIL);
    }

    // 5) Lv arms the leave timer: registered until 600 ms pass
    {
        Vec v; v.fv = fv_listener(OUR_SID); v.evts = {EV_LV}; v.pars = {D_IGN};
        feed_parse(frame(true, {msg_listener(v)}), "lv: clean parse");
        ck("lv: still registered", dut->listener_reg_o, 1);
        ticks(300);
        ck("lv: registered at 300 ms", dut->listener_reg_o, 1);
        // a JoinIn before expiry cancels the leave
        Vec r; r.fv = fv_listener(OUR_SID); r.evts = {EV_JOININ}; r.pars = {D_READY};
        feed_parse(frame(true, {msg_listener(r)}), "lv-cancel: clean parse");
        ticks(400);
        ck("lv-cancel: still registered", dut->listener_reg_o, 1);
        ck("lv-cancel: ready again", dut->listener_ready_o, 1);
        // now let it actually expire
        feed_parse(frame(true, {msg_listener(v)}), "lv2: clean parse");
        ticks(601);
        ck("lv-expiry: deregistered", dut->listener_reg_o, 0);
        ck("lv-expiry: not ready", dut->listener_ready_o, 0);
    }

    // 6) LeaveAll: pulse + ages the registration out unless re-declared
    {
        Vec r; r.fv = fv_listener(OUR_SID); r.evts = {EV_JOININ}; r.pars = {D_READY};
        feed_parse(frame(true, {msg_listener(r)}), "la-setup: clean parse");
        ck("la-setup: ready", dut->listener_ready_o, 1);
        long la0 = la_pulses;
        Vec v; v.lva = 1; v.fv = fv_listener(OUR_SID); v.evts = {EV_MT}; v.pars = {D_IGN};
        feed_parse(frame(true, {msg_listener(v)}), "leaveall: clean parse");
        ck("leaveall: one pulse", la_pulses - la0, 1);
        ck("leaveall: still registered", dut->listener_reg_o, 1);
        ticks(601);
        ck("leaveall: aged out", dut->listener_reg_o, 0);
        // re-register, then LeaveAll + refresh before expiry -> survives
        feed_parse(frame(true, {msg_listener(r)}), "la2-setup: clean parse");
        feed_parse(frame(true, {msg_listener(v)}), "la2: clean parse");
        ticks(300);
        feed_parse(frame(true, {msg_listener(r)}), "la2-refresh: clean parse");
        ticks(400);
        ck("la2: refresh survived", dut->listener_reg_o, 1);
    }

    // 7) LeaveAll storm: parser never wedges, one pulse per PDU
    {
        long la0 = la_pulses;
        uint16_t before = dut->pdu_cnt_o;
        for (int i = 0; i < 10; i++) {
            Vec v; v.lva = 1; v.fv = fv_listener(OUR_SID);
            v.evts = {EV_JOININ}; v.pars = {D_READY};
            feed(frame(true, {msg_listener(v)}));
        }
        for (int i = 0; i < 8000 &&
                        dut->pdu_cnt_o != (uint16_t)(before + 10); i++) step();
        ck("storm: all 10 parsed", dut->pdu_cnt_o, (uint16_t)(before + 10));
        ck("storm: 10 pulses", la_pulses - la0, 10);
        ck("storm: registered", dut->listener_reg_o, 1);
    }

    // 8) Domain sanity
    {
        Vec ok; ok.fv = fv_domain(6, 3, VID); ok.evts = {EV_JOININ};
        feed_parse(frame(true, {msg_domain(ok)}), "domain-ok: clean parse");
        ck("domain-ok: ok", dut->domain_ok_o, 1);
        Vec bad; bad.fv = fv_domain(6, 2, VID); bad.evts = {EV_JOININ};
        feed_parse(frame(true, {msg_domain(bad)}), "domain-prio: clean parse");
        ck("domain-prio: boundary", dut->domain_ok_o, 0);
        feed_parse(frame(true, {msg_domain(ok)}), "domain-heal: clean parse");
        ck("domain-heal: ok again", dut->domain_ok_o, 1);
        Vec badv; badv.fv = fv_domain(6, 3, 5); badv.evts = {EV_JOININ};
        feed_parse(frame(true, {msg_domain(badv)}), "domain-vid: clean parse");
        ck("domain-vid: boundary", dut->domain_ok_o, 0);
        ticks(20001);
        ck("domain-age: boundary aged out", dut->domain_ok_o, 1);
        Vec clsb; clsb.fv = fv_domain(5, 2, 7); clsb.evts = {EV_JOININ};
        feed_parse(frame(true, {msg_domain(clsb)}), "domain-b: clean parse");
        ck("domain-b: class B ignored", dut->domain_ok_o, 1);
    }

    // 9) TalkerFailed capture + TalkerAdvertise clear
    {
        Vec f1; f1.fv = fv_tfail(OUR_SID, 0x08); f1.evts = {EV_JOININ};
        feed_parse(frame(true, {msg_tfail(f1)}), "tfail: clean parse");
        ck("tfail: sticky valid", dut->tfail_valid_o, 1);
        ck("tfail: code", dut->tfail_code_o, 0x08);
        Vec f2; f2.fv = fv_tfail(OUR_SID + 7, 0x01); f2.evts = {EV_JOININ};
        feed_parse(frame(true, {msg_tfail(f2)}), "tfail-foreign: clean parse");
        ck("tfail-foreign: code unchanged", dut->tfail_code_o, 0x08);
        Vec adv; adv.fv = fv_talker(OUR_SID); adv.evts = {EV_JOININ};
        feed_parse(frame(true, {msg_tadv(adv)}), "tadv: clean parse");
        ck("tadv: failure cleared", dut->tfail_valid_o, 0);
    }

    // 10) multi-message PDU (Domain + Listener in one MRPDU)
    {
        ticks(601);   // scrub any pending listener state
        Vec d; d.fv = fv_domain(6, 3, VID); d.evts = {EV_JOININ};
        Vec l; l.fv = fv_listener(OUR_SID); l.evts = {EV_NEW}; l.pars = {D_READY};
        feed_parse(frame(true, {msg_domain(d), msg_listener(l)}),
                   "multi-msg: clean parse");
        ck("multi-msg: registered", dut->listener_reg_o, 1);
        ck("multi-msg: ready", dut->listener_ready_o, 1);
    }

    // 11) MVRP PDU with LeaveAll: pulses, content otherwise ignored
    {
        long la0 = la_pulses;
        Vec v; v.lva = 1; v.fv = {0x00, 0x02}; v.evts = {EV_JOININ};
        feed_parse(frame(false, {msg_vid(v)}), "mvrp-la: clean parse");
        ck("mvrp-la: pulse", la_pulses - la0, 1);
        ck("mvrp-la: listener untouched", dut->listener_reg_o, 1);
    }

    // 12) robustness: bad version, truncation, foreign frames
    {
        uint16_t reg_before = dut->listener_reg_o;
        // bad protocol version
        auto f = frame(true, {});
        f[14] = 7;
        feed_noparse(f, "bad-version: not counted");
        // truncated mid-vector (cut a listener PDU at 20 bytes)
        Vec v; v.fv = fv_listener(OUR_SID); v.evts = {EV_LV}; v.pars = {D_IGN};
        auto t = frame(true, {msg_listener(v)});
        t.resize(20);
        feed_noparse(t, "truncated: not counted");
        ck("truncated: no state change", dut->listener_reg_o, reg_before);
        // non-SRP frame: never enters the FIFO
        uint16_t pdus = dut->rx_pdus_o;
        std::vector<uint8_t> other;
        put_be(other, 0x91E0F0010000ULL, 6); put_be(other, BRIDGE, 6);
        put_be(other, 0x22F0, 2);
        while (other.size() < 60) other.push_back(0x55);
        feed(other);
        for (int i = 0; i < 200; i++) step();
        ck("foreign: not accepted", dut->rx_pdus_o, pdus);
        // ...and the parser still works after all that
        Vec r; r.fv = fv_listener(OUR_SID); r.evts = {EV_JOININ}; r.pars = {D_READY};
        feed_parse(frame(true, {msg_listener(r)}), "recovery: clean parse");
        ck("recovery: ready", dut->listener_ready_o, 1);
    }

    // 13) disable clears registration state
    {
        dut->enable_i = 0; step(); step();
        ck("disable: deregistered", dut->listener_reg_o, 0);
        ck("disable: not ready", dut->listener_ready_o, 0);
        ck("disable: failure cleared", dut->tfail_valid_o, 0);
        dut->enable_i = 1; step(); step();
    }

    // ================================================================== //
    // TA registrar (listener side): TalkerAdvertise/Failed on the BOUND
    // stream id (the walker's second match context)
    // ================================================================== //
    printf("-- listener-side TA registrar --\n");
    {
        const uint64_t BOUND = 0x0200000000010000ULL;   // another talker
        dut->lsid_i = BOUND; dut->lsid_en_i = 1;
        step(); step();
        ck("ta: idle unregistered", dut->ta_registered_o, 0);

        // TalkerAdvertise JoinIn covering the bound sid registers it
        Vec v; v.fv = fv_talker(BOUND); v.evts = {EV_JOININ};
        feed_parse(frame(true, {msg_tadv(v)}), "ta: adv parse");
        ck("ta: registered", dut->ta_registered_o, 1);
        ck("ta: no failure", dut->ta_failed_o, 0);

        // +k range: bound sid at index 2 of a 5-value vector
        dut->lsid_en_i = 0; step(); step();
        dut->lsid_en_i = 1;   // (drop/re-arm to reset nothing — enable keeps)
        Vec k; k.nv = 5; k.fv = fv_talker(BOUND - 2);
        k.evts = {EV_MT, EV_MT, EV_JOININ, EV_MT, EV_MT};
        feed_parse(frame(true, {msg_tadv(k)}), "ta: +k parse");
        ck("ta: +k registered", dut->ta_registered_o, 1);

        // Lv arms the 600 ms leave window; expiry deregisters
        Vec l; l.fv = fv_talker(BOUND); l.evts = {EV_LV};
        feed_parse(frame(true, {msg_tadv(l)}), "ta: lv parse");
        ck("ta: still registered in leave window", dut->ta_registered_o, 1);
        ticks(599);
        ck("ta: window not lapsed at 599", dut->ta_registered_o, 1);
        ticks(2);
        ck("ta: deregistered after leave", dut->ta_registered_o, 0);

        // re-register, then LeaveAll ages it out the same way
        Vec r2; r2.fv = fv_talker(BOUND); r2.evts = {EV_JOININ};
        feed_parse(frame(true, {msg_tadv(r2)}), "ta: re-adv parse");
        ck("ta: re-registered", dut->ta_registered_o, 1);
        Vec la; la.lva = 1; la.fv = fv_talker(BOUND); la.evts = {EV_MT};
        feed_parse(frame(true, {msg_tadv(la)}), "ta: leaveall parse");
        ticks(601);
        ck("ta: aged out after LeaveAll", dut->ta_registered_o, 0);

        // TalkerFailed registers the failure with its code
        Vec tf; tf.fv = fv_tfail(BOUND, 0x08); tf.evts = {EV_JOININ};
        feed_parse(frame(true, {msg_tfail(tf)}), "ta: tfail parse");
        ck("ta: failed registered", dut->ta_failed_o, 1);
        ck("ta: failure code", dut->ta_fail_code_o, 0x08);
        ck("ta: adv not registered", dut->ta_registered_o, 0);

        // a foreign talker's advertise must not register
        Vec fo; fo.fv = fv_talker(BOUND + 0x100); fo.evts = {EV_JOININ};
        feed_parse(frame(true, {msg_tadv(fo)}), "ta: foreign parse");
        ck("ta: foreign ignored", dut->ta_registered_o, 0);

        // binding dropped -> everything forgotten
        dut->lsid_en_i = 0; step(); step();
        ck("ta: unbind clears failure", dut->ta_failed_o, 0);
    }

    printf("== %ld checks, %ld failures ==\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
