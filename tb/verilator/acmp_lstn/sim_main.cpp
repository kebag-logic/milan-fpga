/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for KL_acmp_listener (Milan v1.2 listener
 * SM, pipewire acmp-milan-v12.c contract). Runs at a 10 kHz scaled clock so
 * the 200 ms / 4 s / 10 s timers are simulable. Exit 0 = all pass.
 */

#include "VKL_acmp_listener.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>

static VKL_acmp_listener* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-46s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-46s = %ld\n", what, got); }
}
static void ckh(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-46s got=%llx exp=%llx\n", what,
                              (unsigned long long)got, (unsigned long long)exp); }
    else            { printf("  [ ok ] %-46s = %llx\n", what, (unsigned long long)got); }
}

// partial response frame currently being assembled (survives across helpers)
static std::vector<uint8_t> partial;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}

// advance one clock, harvesting any active output beat first
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

static void run(int n) {
    for (int i = 0; i < n; i++) tick_collect(nullptr);
}

// wait for the next complete output frame (empty = none within budget)
static std::vector<uint8_t> wait_frame(int budget = 4000) {
    std::vector<uint8_t> f;
    for (int c = 0; c < budget; c++)
        if (tick_collect(&f)) return f;
    return {};
}

// ------------------------------------------------------------------ identity
static const uint64_t US_EID  = 0x020000FFFE000003ULL;  // this listener
static const uint8_t  US_MAC[6] = {0x02,0x00,0x00,0x00,0x00,0x03};
static const uint64_t TK_EID  = 0x020000FFFE000001ULL;  // bound talker
static const uint64_t TK2_EID = 0x020000FFFE000002ULL;
static const uint64_t CT_EID  = 0x680500FFFE0000AAULL;  // controller
static const uint64_t TK_SID  = 0x0200000000010000ULL;  // {talker MAC, uid 0}

static void put_be(std::vector<uint8_t>& v, uint64_t x, int n) {
    for (int i = n-1; i >= 0; i--) v.push_back((x >> (8*i)) & 0xFF);
}

// 70-byte ACMP frame
static std::vector<uint8_t> acmp(uint8_t msg, uint8_t status,
                                 uint64_t sid, uint64_t ctlr, uint64_t talker,
                                 uint64_t lstnr, uint16_t tuid, uint16_t luid,
                                 const uint8_t* dmac, uint16_t seq,
                                 uint16_t flags, uint16_t vlan) {
    std::vector<uint8_t> f = {0x91,0xE0,0xF0,0x01,0x00,0x00,
                              0xAA,0xBB,0xCC,0x00,0x00,0x01,
                              0x22,0xF0, 0xFC};
    f.push_back(msg & 0xF);
    f.push_back((status << 3) | 0);          // status | cdl_hi (cdl=44)
    f.push_back(44);
    put_be(f, sid, 8);
    put_be(f, ctlr, 8);
    put_be(f, talker, 8);
    put_be(f, lstnr, 8);
    put_be(f, tuid, 2);
    put_be(f, luid, 2);
    for (int i = 0; i < 6; i++) f.push_back(dmac ? dmac[i] : 0);
    put_be(f, 0, 2);                          // connection_count
    put_be(f, seq, 2);
    put_be(f, flags, 2);
    put_be(f, vlan, 2);
    put_be(f, 0, 2);                          // reserved
    return f;
}

// minimal ADP frame (>= 26 bytes classified; padded to 82)
static std::vector<uint8_t> adp(uint8_t msg, uint64_t eid) {
    std::vector<uint8_t> f = {0x91,0xE0,0xF0,0x01,0x00,0x00,
                              0x02,0x00,0x00,0x00,0x00,0x01,
                              0x22,0xF0, 0xFA};
    f.push_back(msg & 0xF);
    f.push_back(0x1F); f.push_back(56);       // valid_time/cdl-ish
    put_be(f, eid, 8);                         // entity_id at wire byte 18
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
    // classification cycle
    tick_collect(nullptr);
    tick_collect(nullptr);
}

// response accessors (wire bytes)
static int r_msg(const std::vector<uint8_t>& b){ return b.size()>15 ? b[15]&0xF : -1; }
static int r_sta(const std::vector<uint8_t>& b){ return b.size()>16 ? b[16]>>3 : -1; }
static uint64_t r_be(const std::vector<uint8_t>& b, int off, int n) {
    uint64_t v = 0;
    for (int i = 0; i < n; i++) v = (v << 8) | b[off+i];
    return v;
}

// scaled-clock timer values (cycles): 1 ms = 10 cycles
static const int MS = 10;

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_acmp_listener;

    dut->rst_n = 0; dut->enable_i = 1;
    dut->entity_id_i = US_EID;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|US_MAC[i]; dut->station_mac_i = m; }
    dut->tick_1s_i = 0;
    dut->ta_registered_i = 0; dut->ta_failed_i = 0;
    dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) tick();

    printf("== KL_acmp_listener — Milan v1.2 listener SM ==\n");

    // ---------------------------------------------------------------- //
    printf("\n[1] reset + GET_RX_STATE unbound\n");
    ck("[1] state UNBOUND", dut->state_o, 0);
    ck("[1] inactive", dut->stream_active_o, 0);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x100, 0, 0));
    auto r = wait_frame();
    ck("[1] GET_RX_STATE answered", r.size(), 70);
    ck("[1] msg GET_RX_STATE_RESPONSE", r_msg(r), 11);
    ck("[1] SUCCESS", r_sta(r), 0);
    ck("[1] count 0", (long)r_be(r, 60, 2), 0);
    ckh("[1] talker 0", r_be(r, 34, 8), 0);
    ck("[1] flags 0", (long)r_be(r, 64, 2), 0);

    // sink 1 (CRF): valid but ALWAYS unbound (la_avdecc fatal-enumeration
    // field report: UNKNOWN_ID for an advertised sink is inconsistent)
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x100, 0, 0));
    r = wait_frame();
    ck("[1b] sink1 GET_RX_STATE SUCCESS", r_sta(r), 0);
    ck("[1b] sink1 count 0", (long)r_be(r, 60, 2), 0);
    ckh("[1b] sink1 talker 0", r_be(r, 34, 8), 0);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 2, nullptr, 0x100, 0, 0));
    r = wait_frame();
    ck("[1b] sink2 UNKNOWN_ID", r_sta(r), 1);

    // ---------------------------------------------------------------- //
    printf("\n[2] BIND_RX -> response + probe, PRB_W_RESP\n");
    feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 0, nullptr, 0x101,
              0x0002 /*FAST_CONNECT requested*/, 0));
    r = wait_frame();
    ck("[2] BIND_RESP", r_msg(r), 7);
    ck("[2] SUCCESS", r_sta(r), 0);
    ck("[2] count 1", (long)r_be(r, 60, 2), 1);
    ckh("[2] stream_id zero", r_be(r, 18, 8), 0);
    ckh("[2] dmac zero", r_be(r, 54, 6), 0);
    ck("[2] FAST_CONNECT cleared", (long)r_be(r, 64, 2), 0);
    ck("[2] vlan zero", (long)r_be(r, 66, 2), 0);
    auto p = wait_frame();
    ck("[2] PROBE_TX follows", p.size(), 70);
    ck("[2] probe msg CONNECT_TX_COMMAND", r_msg(p), 0);
    ckh("[2] probe controller", r_be(p, 26, 8), CT_EID);
    ckh("[2] probe talker", r_be(p, 34, 8), TK_EID);
    ckh("[2] probe listener us", r_be(p, 42, 8), US_EID);
    ck("[2] probe seq 0", (long)r_be(p, 62, 2), 0);
    ckh("[2] probe stream_id 0", r_be(p, 18, 8), 0);
    ck("[2] state PRB_W_RESP", dut->state_o, 3);
    ckh("[2] bound sid derived", dut->bound_sid_o, TK_SID);
    ck("[2] probing ACTIVE", dut->probing_o, 2);
    ck("[2] probe_count 1", dut->probe_count_o, 1);

    // ---------------------------------------------------------------- //
    printf("\n[2b] sink1 stays unbound-shaped while sink0 is mid-ladder\n");
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x100, 0, 0));
    r = wait_frame();
    ck("[2b] sink1 SUCCESS", r_sta(r), 0);
    ck("[2b] sink1 count 0", (long)r_be(r, 60, 2), 0);
    ckh("[2b] sink1 talker 0 (sink0 state masked)", r_be(r, 34, 8), 0);
    ck("[2b] sink1 flags 0", (long)r_be(r, 64, 2), 0);

    printf("\n[3] GET_RX_STATE while probing: STREAMING_WAIT\n");
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x102, 0, 0));
    r = wait_frame();
    ck("[3] count 1", (long)r_be(r, 60, 2), 1);
    ckh("[3] talker bound", r_be(r, 34, 8), TK_EID);
    ck("[3] STREAMING_WAIT", (long)r_be(r, 64, 2), 0x0008);
    ckh("[3] dest_mac zeroed", r_be(r, 54, 6), 0);
    ck("[3] state unchanged", dut->state_o, 3);

    // ---------------------------------------------------------------- //
    printf("\n[4] probe response SUCCESS -> SETTLED_NO_RSV\n");
    {
        const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x01};
        feed(acmp(1, 0, TK_SID, CT_EID, TK_EID, US_EID, 0, 0, dm, 0, 0, 2));
    }
    ck("[4] state SETTLED_NO_RSV", dut->state_o, 6);
    ck("[4] active", dut->stream_active_o, 1);
    ck("[4] declares Listener attr", dut->lstn_declare_o, 1);
    ckh("[4] sid authoritative", dut->bound_sid_o, TK_SID);
    ck("[4] vlan 2", dut->stream_vlan_o, 2);
    ckh("[4] dmac captured", dut->stream_dmac_o, 0x91E0F000FE01ULL);
    ck("[4] probing COMPLETED", dut->probing_o, 3);

    // ---------------------------------------------------------------- //
    printf("\n[5] TalkerAdvertise registered -> SETTLED_RSV_OK\n");
    dut->ta_registered_i = 1;
    run(4);
    ck("[5] state SETTLED_RSV_OK", dut->state_o, 7);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x103, 0, 0));
    r = wait_frame();
    ck("[5] settled flags = stored SW (0)", (long)r_be(r, 64, 2), 0);
    ck("[5] count 1", (long)r_be(r, 60, 2), 1);
    ckh("[5] dest_mac echoes the learned MAAP addr", r_be(r, 54, 6),
        0x91E0F000FE01ull);

    // ---------------------------------------------------------------- //
    printf("\n[6] TalkerFailed while settled -> SETTLED_NO_RSV and back\n");
    dut->ta_failed_i = 1;
    run(4);
    ck("[6] back to SETTLED_NO_RSV", dut->state_o, 6);
    dut->ta_failed_i = 0;
    dut->ta_registered_i = 0;
    run(4);
    ck("[6] no change on ta_reg fall here", dut->state_o, 6);
    dut->ta_registered_i = 1;
    run(4);
    ck("[6] re-registered -> RSV_OK", dut->state_o, 7);

    // ---------------------------------------------------------------- //
    printf("\n[7] reservation lost (ta fall), talker not visible -> PRB_W_AVAIL\n");
    dut->ta_registered_i = 0;
    run(4);
    ck("[7] state PRB_W_AVAIL", dut->state_o, 1);
    ck("[7] deactivated", dut->stream_active_o, 0);
    ck("[7] declare withdrawn", dut->lstn_declare_o, 0);
    ck("[7] probing PASSIVE", dut->probing_o, 1);

    // ---------------------------------------------------------------- //
    printf("\n[8] ADP AVAILABLE -> DELAY -> probe ladder to RETRY\n");
    feed(adp(0, TK_EID));
    run(4);
    ck("[8] tk_avail", dut->tk_avail_o, 1);
    ck("[8] state PRB_W_DELAY", dut->state_o, 2);
    // random delay <= 1024 ms; wait up to 1100 ms for the probe
    p = wait_frame(1100 * MS);
    ck("[8] probe sent after delay", p.size(), 70);
    ck("[8] state PRB_W_RESP", dut->state_o, 3);
    // no answer: 200 ms -> resend (RESP2)
    p = wait_frame(250 * MS);
    ck("[8] probe resent", p.size(), 70);
    ck("[8] state PRB_W_RESP2", dut->state_o, 4);
    long seq2 = (long)r_be(p, 62, 2);
    ck("[8] fresh sequence id", seq2 >= 2, 1);
    // no answer again: 200 ms -> RETRY with LISTENER_TALKER_TIMEOUT
    run(250 * MS);
    ck("[8] state PRB_W_RETRY", dut->state_o, 5);
    ck("[8] status LISTENER_TALKER_TIMEOUT", dut->acmp_status_o, 7);

    // ---------------------------------------------------------------- //
    printf("\n[9] RETRY expiry (talker visible) -> DELAY -> probe -> error resp\n");
    p = wait_frame(4200 * MS + 1100 * MS);   // 4 s retry + <=1.024 s delay
    ck("[9] re-probe emitted", p.size(), 70);
    ck("[9] state PRB_W_RESP", dut->state_o, 3);
    // talker answers with TALKER_NO_BANDWIDTH (5)
    feed(acmp(1, 5, 0, CT_EID, TK_EID, US_EID, 0, 0, nullptr, 1, 0, 0));
    ck("[9] state PRB_W_RETRY", dut->state_o, 5);
    ck("[9] status stored (5)", dut->acmp_status_o, 5);

    // ---------------------------------------------------------------- //
    printf("\n[10] ADP DEPARTING in RETRY -> PRB_W_AVAIL\n");
    feed(adp(1, TK_EID));
    run(4);
    ck("[10] tk_avail dropped", dut->tk_avail_o, 0);
    ck("[10] state PRB_W_AVAIL", dut->state_o, 1);

    // ---------------------------------------------------------------- //
    printf("\n[11] rebind-same = response only; rebind-different = re-probe\n");
    long pc = dut->probe_count_o;
    feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 0, nullptr, 0x104, 0, 0));
    r = wait_frame();
    ck("[11] rebind-same BIND_RESP", r_msg(r), 7);
    ck("[11] state stays PRB_W_AVAIL", dut->state_o, 1);
    ck("[11] no new probe", dut->probe_count_o, pc);
    feed(acmp(6, 0, 0, CT_EID, TK2_EID, US_EID, 0, 0, nullptr, 0x105, 0, 0));
    r = wait_frame();
    ck("[11] rebind-diff BIND_RESP", r_msg(r), 7);
    p = wait_frame();
    ck("[11] probe to new talker", p.size(), 70);
    ckh("[11] probe talker T2", r_be(p, 34, 8), TK2_EID);
    ck("[11] state PRB_W_RESP", dut->state_o, 3);
    ckh("[11] bound talker T2", dut->bound_talker_o, TK2_EID);

    // ---------------------------------------------------------------- //
    printf("\n[12] settle on T2 then UNBIND_RX -> UNBOUND\n");
    {
        const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x02};
        feed(acmp(1, 0, 0x0200000000020000ULL, CT_EID, TK2_EID, US_EID, 0, 0,
                  dm, 2, 0, 2));
    }
    ck("[12] settled", dut->state_o, 6);
    feed(acmp(8, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x106, 0x0008, 0));
    r = wait_frame();
    ck("[12] UNBIND_RESP", r_msg(r), 9);
    ck("[12] SUCCESS", r_sta(r), 0);
    ckh("[12] talker zeroed", r_be(r, 34, 8), 0);
    ck("[12] count 0", (long)r_be(r, 60, 2), 0);
    ck("[12] SW cleared", (long)r_be(r, 64, 2), 0);
    ck("[12] state UNBOUND", dut->state_o, 0);
    ck("[12] inactive", dut->stream_active_o, 0);
    ck("[12] probing DISABLED", dut->probing_o, 0);
    ckh("[12] binding cleared", dut->bound_talker_o, 0);

    // ---------------------------------------------------------------- //
    printf("\n[13] bad listener_unique_id + foreign frames\n");
    feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 5, nullptr, 0x107, 0, 0));
    r = wait_frame();
    ck("[13] BIND luid=5 LISTENER_UNKNOWN_ID", r_sta(r), 1);
    ck("[13] state UNBOUND still", dut->state_o, 0);
    feed(acmp(6, 0, 0, CT_EID, TK_EID, 0x1111222233334444ULL, 0, 0,
              nullptr, 0x108, 0, 0));
    r = wait_frame(600);
    ck("[13] foreign listener ignored", r.size(), 0);

    // ---------------------------------------------------------------- //
    printf("\n[14] NO_TK lapse in SETTLED_NO_RSV (talker invisible) -> PRB_W_AVAIL\n");
    feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 0, nullptr, 0x109, 0, 0));
    (void)wait_frame(); (void)wait_frame();          // response + probe
    feed(acmp(1, 0, TK_SID, CT_EID, TK_EID, US_EID, 0, 0, nullptr, 3, 0, 2));
    ck("[14] settled", dut->state_o, 6);
    run(10100 * MS);                                  // 10 s NO_TK
    ck("[14] state PRB_W_AVAIL", dut->state_o, 1);
    ck("[14] probing PASSIVE", dut->probing_o, 1);

    // ---------------------------------------------------------------- //
    printf("\n[15] ADP availability age-out (63 s)\n");
    feed(adp(0, TK_EID));
    run(4);
    ck("[15] visible again", dut->tk_avail_o, 1);
    for (int s = 0; s < 64; s++) { dut->tick_1s_i = 1; tick_collect(nullptr);
                                   dut->tick_1s_i = 0; run(3); }
    ck("[15] aged out", dut->tk_avail_o, 0);

    printf("\n======================================================================\n");

    // ---------------------------------------------------------------- //
    printf("\n[W] TX-grant watchdog: wedged arbiter must not deafen the SM\n");
    {
        uint16_t cc0 = dut->cmd_count_o;
        // raw feed with tready HELD LOW (feed()/tick_collect force it high)
        auto f = acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x900, 0, 0);
        dut->m_axis_tready = 0;
        for (size_t off = 0; off < f.size(); off += 8) {
            uint64_t d = 0; uint8_t keep = 0;
            for (int l = 0; l < 8; l++)
                if (off + l < f.size()) { d |= (uint64_t)f[off+l] << (8*l); keep |= (1<<l); }
            dut->rx_tvalid_i = 1; dut->rx_tdata_i = d;
            dut->rx_tkeep_i = keep; dut->rx_tlast_i = (off + 8 >= f.size());
            tick();
        }
        dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
        tick(); tick(); tick();
        ck("[W] command accepted", dut->cmd_count_o, (long)(cc0 + 1));
        // walker now sits in RESPOND_S; run past the 2^20-cycle watchdog
        for (int i = 0; i < (1 << 20) + 200; i++) tick();
        ck("[W] wedge counted", dut->tx_wedge_cnt_o, 1);
        dut->m_axis_tready = 1;
        for (int i = 0; i < 10; i++) tick();
        // the listener must be alive again: next command accepted + answered
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x901, 0, 0));
        auto rw = wait_frame();
        ck("[W] next GET_RX_STATE answered", rw.size(), 70);
        ck("[W] cmd_count advanced", dut->cmd_count_o, (long)(cc0 + 2));
    }


    // ---------------------------------------------------------------- //
    printf("\n[Z] zero-gap frames: command right behind another frame\n");
    // Silicon RX FIFOs compress inter-frame gaps under DMA stalls; a
    // command draining gaplessly behind an AAF frame must still be
    // accepted (task #29). EXPECTED TO FAIL until the always-armed
    // capture lands - kept as the repro.
    {
        uint16_t cc0 = dut->cmd_count_o;
        // 88-byte AAF-ish frame (foreign dst/subtype: walker must ignore)
        std::vector<uint8_t> aaf(88, 0);
        const uint8_t ad[6]={0x91,0xE0,0xF0,0x00,0xFE,0x01};
        for (int i=0;i<6;i++) aaf[i]=ad[i];
        aaf[12]=0x22; aaf[13]=0xF0; aaf[14]=0x02; aaf[15]=0x81;
        auto cmd = acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0xA01, 0, 0);
        // drive both frames back-to-back with ZERO idle beats
        auto drive = [&](const std::vector<uint8_t>& f, bool hold_after) {
            for (size_t off = 0; off < f.size(); off += 8) {
                uint64_t d = 0; uint8_t keep = 0;
                for (int l = 0; l < 8; l++)
                    if (off + l < f.size()) { d |= (uint64_t)f[off+l] << (8*l); keep |= (1<<l); }
                dut->rx_tvalid_i = 1; dut->rx_tdata_i = d;
                dut->rx_tkeep_i = keep; dut->rx_tlast_i = (off + 8 >= f.size());
                tick();
            }
            if (!hold_after) { dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; }
        };
        drive(aaf, true);          // tlast beat, then IMMEDIATELY...
        drive(cmd, false);         // ...the command, no idle cycle
        for (int i = 0; i < 30; i++) tick_collect(nullptr);
        ck("[Z] zero-gap command accepted", dut->cmd_count_o, (long)(cc0 + 1));
    }

    // ---------------------------------------------------------------- //
    printf("\n[S1] CRF sink-1 real bind record (no probe SM, no MSRP)\n");
    {
        // sink0 state as [Z] left it: the S1 record must not disturb it
        long st0 = dut->state_o, act0 = dut->stream_active_o;
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x1FF, 0, 0));
        auto r = wait_frame();
        long cnt0 = (long)r_be(r, 60, 2);

        // fast-connect bind: command carries the stream_id + dest_mac
        const uint8_t cdm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x08};
        feed(acmp(6, 0, 0x020000000001000BULL, CT_EID, TK_EID, US_EID,
                  0x000B, 1, cdm, 0x200, 0, 0));
        r = wait_frame();
        ck("[S1] BIND_RESP", r_msg(r), 7);
        ck("[S1] SUCCESS", r_sta(r), 0);
        ck("[S1] count 1", (long)r_be(r, 60, 2), 1);
        ck("[S1] s1_bound_o", dut->s1_bound_o, 1);
        ckh("[S1] s1_sid = command sid", dut->s1_sid_o, 0x020000000001000BULL);
        ckh("[S1] s1_dmac = command dmac", dut->s1_dmac_o, 0x91E0F0002A08ULL);
        ck("[S1] sink0 SM untouched", dut->state_o, st0);
        ck("[S1] sink0 activity untouched", dut->stream_active_o, act0);

        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x201, 0, 0));
        r = wait_frame();
        ck("[S1] state SUCCESS", r_sta(r), 0);
        ck("[S1] state count 1", (long)r_be(r, 60, 2), 1);
        ckh("[S1] state talker", r_be(r, 34, 8), TK_EID);
        ck("[S1] state tuid", (long)r_be(r, 50, 2), 0x000B);
        ckh("[S1] state dmac", r_be(r, 54, 6), 0x91E0F0002A08ULL);

        // zero-sid bind falls back to {talker EID(FFFE-squeezed), tuid}
        feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0x0001, 1, nullptr,
                  0x202, 0, 0));
        r = wait_frame();
        ck("[S1] zero-sid rebind SUCCESS", r_sta(r), 0);
        ckh("[S1] fallback sid {eid,tuid}", dut->s1_sid_o,
            0x0200000000010001ULL);

        // sink0 GET_RX_STATE remains independent (whatever [Z] left)
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x203, 0, 0));
        r = wait_frame();
        ck("[S1] sink0 state count unchanged", (long)r_be(r, 60, 2), cnt0);

        // unbind clears the record
        feed(acmp(8, 0, 0, CT_EID, TK_EID, US_EID, 0, 1, nullptr, 0x204, 0, 0));
        r = wait_frame();
        ck("[S1] UNBIND_RESP", r_msg(r), 9);
        ck("[S1] UNBIND SUCCESS", r_sta(r), 0);
        ck("[S1] s1 cleared", dut->s1_bound_o, 0);
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x205, 0, 0));
        r = wait_frame();
        ck("[S1] post-unbind count 0", (long)r_be(r, 60, 2), 0);
        ckh("[S1] post-unbind talker 0", r_be(r, 34, 8), 0);

        // uid >= 2 still LISTENER_UNKNOWN_ID
        feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 2, nullptr, 0x206, 0, 0));
        r = wait_frame();
        ck("[S1] uid2 bind UNKNOWN_ID", r_sta(r), 1);
        ck("[S1] uid2 left s1 alone", dut->s1_bound_o, 0);
    }

    printf("KL_acmp_listener: %ld checks, %ld failures\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
