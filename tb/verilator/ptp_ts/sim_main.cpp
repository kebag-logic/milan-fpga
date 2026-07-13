// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for ptp_ts_top's METADATA pipeline (2026-07-13
// synchronous-capture redesign). Beyond the original race reproductions this
// is the INTERFERENCE suite: gPTP event frames embedded in line-rate non-PTP
// floods, event+general and event+event back-to-back, general-message storms,
// backpressured record bursts, runts and VLAN lookalikes - with a GOLDEN
// timestamp model: both clocks are common and INCR is 20 ns/cycle, so the
// DELTA between any two records must equal (sop_cycle_B - sop_cycle_A) * 20 ns
// EXACTLY. Any mis-pairing of timestamp to frame shifts a delta by a whole
// frame time and fails loudly.
//
// Record contract (2 beats): beat0 = ns[63:0] (disciplined PHC);
// beat1 = {40'0, seq[15:0], msgType[3:0], 2'0, marker=1, dir}. seq is the frame's
// big-endian sequenceId verbatim; only EVENT messages (msgType[3]==0) record.
// LE-lane convention (the real MAC-side order): first wire byte in tdata[7:0];
// partial tail keep is low-aligned (rem=4 -> 0x0F).

#include <verilated.h>
#include "Vptp_ts_top.h"
#include <cstdio>
#include <cstring>
#include <vector>

static Vptp_ts_top *top;
static vluint64_t cyc = 0;          // TB cycle counter == PHC ticks (20 ns each)
static int fails = 0;
static const uint64_t NS_PER_CYC = 20;

struct Rec { uint64_t ns, meta; };
static std::vector<Rec> recs;
static uint64_t rec_hi;
static bool rec_have_hi = false;
static int ts_ready_pulses = 0;

static void tick()
{
    // sample pre-edge (what the posedge commits), then clock both domains
    top->gtx_clk = 0; top->axis_clk = 0; top->eval();
    if (top->o_tx_ts_ready) ts_ready_pulses++;
    if (top->ts_m_axis_tvalid && top->ts_m_axis_tready) {
        if (!rec_have_hi) {
            rec_hi = top->ts_m_axis_tdata;
            rec_have_hi = true;
            if (top->ts_m_axis_tlast) { printf("!! 1-beat record\n"); fails++; rec_have_hi = false; }
        } else {
            if (!top->ts_m_axis_tlast) { printf("!! >2-beat record\n"); fails++; }
            recs.push_back({rec_hi, (uint64_t)top->ts_m_axis_tdata});
            rec_have_hi = false;
        }
    }
    top->gtx_clk = 1; top->axis_clk = 1; top->eval();
    cyc++;
}

// ---- frame builders (wire-order byte arrays) --------------------------------
static void gptp(uint8_t *b, uint8_t msgtype, uint16_t seq)   // 68 B
{
    memset(b, 0, 68);
    const uint8_t hdr[14] = {0x01,0x80,0xC2,0,0,0x0E, 2,0,0,0,0,2, 0x88,0xF7};
    memcpy(b, hdr, 14);
    b[14] = (uint8_t)(0x10 | (msgtype & 0xF));   // majorSdoId 1 | msgType
    b[15] = 0x02;
    b[16] = 0; b[17] = 54;
    b[44] = seq >> 8; b[45] = seq & 0xFF;
}

static void ipv4(uint8_t *b, int len, uint8_t marker)          // len >= 16
{
    memset(b, 0, len);
    const uint8_t hdr[14] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 2,0,0,0,0,2, 0x08,0x00};
    memcpy(b, hdr, 14);
    for (int i = 14; i < len; i++) b[i] = (uint8_t)(marker ^ i);
}

static void vlan_gptp_lookalike(uint8_t *b)                    // 72 B, 0x8100 tagged
{
    memset(b, 0, 72);
    const uint8_t hdr[14] = {0x01,0x80,0xC2,0,0,0x0E, 2,0,0,0,0,2, 0x81,0x00};
    memcpy(b, hdr, 14);
    b[14] = 0x60; b[15] = 0x00;          // PCP 3
    b[16] = 0x88; b[17] = 0xF7;          // inner ethertype 88F7 - must NOT match
    b[18] = 0x12; b[19] = 0x02; b[21] = 54;
    b[48] = 0xAA; b[49] = 0x55;
}

// ---- frame driver: returns the SOP-accept cycle -----------------------------
// gap = idle cycles inserted between beats (0 = line rate)
static uint64_t send(const uint8_t *b, int len, bool tx, int gap)
{
    int nbeats = (len + 7) / 8;
    uint64_t sop_cyc = 0;
    for (int i = 0; i < nbeats; i++) {
        uint64_t d = 0;
        for (int k = 0; k < 8 && 8 * i + k < len; k++)
            d |= (uint64_t)b[8 * i + k] << (8 * k);
        int rem = len - 8 * i;
        uint8_t keep = rem >= 8 ? 0xFF : (uint8_t)((1u << rem) - 1);
        bool last = i == nbeats - 1;
        if (tx) {
            top->s_axis_tx_tdata = d; top->s_axis_tx_tkeep = keep;
            top->s_axis_tx_tlast = last; top->s_axis_tx_tvalid = 1;
            do { if (i == 0) sop_cyc = cyc; tick(); } while (!top->s_axis_tx_tready);
            top->s_axis_tx_tvalid = 0;
        } else {
            top->s_axis_rx_tdata = d; top->s_axis_rx_tkeep = keep;
            top->s_axis_rx_tlast = last; top->s_axis_rx_tvalid = 1;
            do { if (i == 0) sop_cyc = cyc; tick(); } while (!top->s_axis_rx_tready);
            top->s_axis_rx_tvalid = 0;
        }
        for (int g = 0; g < gap; g++) tick();
    }
    return sop_cyc;
}

static void settle(int n) { for (int i = 0; i < n; i++) tick(); }

// ---- checkers ---------------------------------------------------------------
static void expect_recs(const char *name, size_t n)
{
    if (recs.size() != n) { printf("FAIL %s: %zu records (expected %zu)\n", name, recs.size(), n); fails++; }
    else                  { printf("PASS %s: %zu record(s)\n", name, n); }
}

static void check_rec(const char *name, size_t i, int dir, int mtype, uint16_t seq)
{
    if (i >= recs.size()) { printf("FAIL %s: record %zu missing\n", name, i); fails++; return; }
    uint64_t m = recs[i].meta;
    int rdir = m & 1, rmk = (m >> 1) & 1, rmt = (m >> 4) & 0xF;
    uint16_t rseq = (m >> 8) & 0xFFFF;
    bool ok = rdir == dir && rmk == 1 && rmt == mtype && rseq == seq && recs[i].ns != 0;
    printf("%s %s rec%zu: dir=%d mt=%d seq=0x%04x ns=%llu\n", ok ? "PASS" : "FAIL",
           name, i, rdir, rmt, rseq, (unsigned long long)recs[i].ns);
    if (!ok) fails++;
}

// golden pairing: record deltas must equal SOP-cycle deltas exactly
static void check_delta(const char *name, size_t ia, size_t ib,
                        uint64_t sop_a, uint64_t sop_b)
{
    if (ia >= recs.size() || ib >= recs.size()) return;   // counted elsewhere
    uint64_t want = (sop_b - sop_a) * NS_PER_CYC;
    uint64_t got  = recs[ib].ns - recs[ia].ns;
    bool ok = got == want;
    printf("%s %s delta rec%zu->rec%zu: got %llu ns want %llu ns\n",
           ok ? "PASS" : "FAIL", name, ia, ib,
           (unsigned long long)got, (unsigned long long)want);
    if (!ok) fails++;
}

int main(int argc, char **argv)
{
    Verilated::commandArgs(argc, argv);
    top = new Vptp_ts_top;

    top->gtx_resetn = 0; top->axis_resetn = 0;
    top->m_axis_tx_tready = 1; top->m_axis_rx_tready = 1;
    top->ts_m_axis_tready = 1;
    top->i_ptp_enable = 1;
    top->i_ptp_incr = (uint32_t)NS_PER_CYC << 24;
    top->i_ptp_adj = 0;
    settle(8);
    top->gtx_resetn = 1; top->axis_resetn = 1;
    settle(8);

    uint8_t b[80], f[80];

    // 1: single event frames - slow beats (MII profile) and line rate
    recs.clear();
    gptp(b, 2, 0x0102);
    uint64_t s1 = send(b, 68, false, 32);
    gptp(b, 2, 0x0203);
    uint64_t s2 = send(b, 68, false, 0);
    settle(60);
    expect_recs("baseline slow+fast", 2);
    check_rec("baseline", 0, 0, 2, 0x0102);
    check_rec("baseline", 1, 0, 2, 0x0203);
    check_delta("baseline", 0, 1, s1, s2);

    // 2: INTERFERENCE SANDWICH - event frame at line rate inside an IPv4 flood
    recs.clear();
    ipv4(f, 64, 0x11);
    uint64_t ref_sop = 0, evt_sop = 0;
    gptp(b, 2, 0x1111);
    ref_sop = send(b, 68, false, 0);           // reference event, quiet wire
    settle(40);
    for (int i = 0; i < 5; i++) send(f, 64, false, 0);
    gptp(b, 2, 0x2222);
    evt_sop = send(b, 68, false, 0);           // embedded back-to-back in flood
    for (int i = 0; i < 5; i++) send(f, 64, false, 0);
    settle(80);
    expect_recs("flood sandwich", 2);
    check_rec("flood sandwich", 1, 0, 2, 0x2222);
    check_delta("flood sandwich", 0, 1, ref_sop, evt_sop);

    // 3: event + general back-to-back (pdelay_resp + resp_fup share a seq)
    recs.clear();
    gptp(b, 3, 0x0777);                        // Pdelay_Resp (event)
    uint64_t s3 = send(b, 68, false, 0);
    gptp(b, 0xA, 0x0777);                      // Pdelay_Resp_Follow_Up (general)
    send(b, 68, false, 0);
    settle(60);
    expect_recs("resp+fup pair", 1);
    check_rec("resp+fup pair", 0, 0, 3, 0x0777);

    // 4: event + event back-to-back (sync,sync) - exact per-frame pairing
    recs.clear();
    gptp(b, 0, 0x0501);
    uint64_t s4a = send(b, 68, false, 0);
    gptp(b, 0, 0x0502);
    uint64_t s4b = send(b, 68, false, 0);
    settle(60);
    expect_recs("sync+sync b2b", 2);
    check_rec("sync+sync b2b", 0, 0, 0, 0x0501);
    check_rec("sync+sync b2b", 1, 0, 0, 0x0502);
    check_delta("sync+sync b2b", 0, 1, s4a, s4b);

    // 5: general storm - announces must record NOTHING
    recs.clear();
    for (int i = 0; i < 10; i++) { gptp(b, 0xB, (uint16_t)(0x0900 + i)); send(b, 68, false, 0); }
    settle(80);
    expect_recs("announce storm", 0);

    // 6: backpressured burst - 3 event records queue and drain intact
    recs.clear();
    top->ts_m_axis_tready = 0;
    uint64_t s6[3];
    for (int i = 0; i < 3; i++) { gptp(b, 2, (uint16_t)(0x0601 + i)); s6[i] = send(b, 68, false, 0); }
    settle(120);
    top->ts_m_axis_tready = 1;
    settle(120);
    expect_recs("backpressured burst", 3);
    for (int i = 0; i < 3; i++) check_rec("backpressured burst", i, 0, 2, (uint16_t)(0x0601 + i));
    check_delta("backpressured burst", 0, 2, s6[0], s6[2]);

    // 7: TX direction + IRQ pulse per record
    recs.clear();
    int p0 = ts_ready_pulses;
    gptp(b, 0, 0x1122);
    send(b, 68, true, 0);
    gptp(b, 0, 0x1123);
    send(b, 68, true, 0);
    settle(80);
    expect_recs("tx sync x2", 2);
    check_rec("tx sync x2", 0, 1, 0, 0x1122);
    check_rec("tx sync x2", 1, 1, 0, 0x1123);
    if (ts_ready_pulses - p0 != 2) { printf("FAIL tx: %d o_tx_ts_ready pulses (want 2)\n", ts_ready_pulses - p0); fails++; }
    else printf("PASS tx: 2 o_tx_ts_ready pulses\n");

    // 8: TX+RX simultaneous storms with embedded events (RR mux under load)
    recs.clear();
    {
        // drive both taps concurrently: floods + one event each
        uint8_t gtx_[80], grx_[80];
        gptp(gtx_, 0, 0x0801); gptp(grx_, 2, 0x0802);
        std::vector<uint64_t> txb, rxb;
        uint8_t fl[64]; ipv4(fl, 64, 0x33);
        auto pack = [](const uint8_t *src, int len, std::vector<uint64_t> &v, std::vector<uint8_t> &k, std::vector<uint8_t> &l) {
            int nb = (len + 7) / 8;
            for (int i = 0; i < nb; i++) {
                uint64_t d = 0;
                for (int j = 0; j < 8 && 8*i+j < len; j++) d |= (uint64_t)src[8*i+j] << (8*j);
                int rem = len - 8*i;
                v.push_back(d);
                k.push_back(rem >= 8 ? 0xFF : (uint8_t)((1u << rem) - 1));
                l.push_back(i == nb-1);
            }
        };
        std::vector<uint64_t> tv, rv; std::vector<uint8_t> tk, rk, tl, rl;
        for (int i = 0; i < 3; i++) pack(fl, 64, tv, tk, tl);
        pack(gtx_, 68, tv, tk, tl);
        for (int i = 0; i < 3; i++) pack(fl, 64, tv, tk, tl);
        for (int i = 0; i < 3; i++) pack(fl, 64, rv, rk, rl);
        pack(grx_, 68, rv, rk, rl);
        for (int i = 0; i < 3; i++) pack(fl, 64, rv, rk, rl);
        size_t ti = 0, ri = 0;
        while (ti < tv.size() || ri < rv.size()) {
            if (ti < tv.size()) {
                top->s_axis_tx_tdata = tv[ti]; top->s_axis_tx_tkeep = tk[ti];
                top->s_axis_tx_tlast = tl[ti]; top->s_axis_tx_tvalid = 1;
            } else top->s_axis_tx_tvalid = 0;
            if (ri < rv.size()) {
                top->s_axis_rx_tdata = rv[ri]; top->s_axis_rx_tkeep = rk[ri];
                top->s_axis_rx_tlast = rl[ri]; top->s_axis_rx_tvalid = 1;
            } else top->s_axis_rx_tvalid = 0;
            top->eval();
            bool ta = top->s_axis_tx_tvalid && top->s_axis_tx_tready;
            bool ra = top->s_axis_rx_tvalid && top->s_axis_rx_tready;
            tick();
            if (ta) ti++;
            if (ra) ri++;
        }
        top->s_axis_tx_tvalid = 0; top->s_axis_rx_tvalid = 0;
        settle(150);
    }
    expect_recs("tx+rx storm", 2);
    {   // order across directions is mux-arbitration-dependent; find each
        bool have_tx = false, have_rx = false;
        for (auto &r : recs) {
            if ((r.meta & 1) == 1 && ((r.meta >> 8) & 0xFFFF) == 0x0801 && ((r.meta >> 4) & 0xF) == 0) have_tx = true;
            if ((r.meta & 1) == 0 && ((r.meta >> 8) & 0xFFFF) == 0x0802 && ((r.meta >> 4) & 0xF) == 2) have_rx = true;
        }
        if (have_tx && have_rx) printf("PASS tx+rx storm: both records correct\n");
        else { printf("FAIL tx+rx storm: tx=%d rx=%d\n", have_tx, have_rx); fails++; }
    }

    // 9: runts + malformed must not record NOR wedge the pipeline
    recs.clear();
    ipv4(f, 16, 0x44); send(f, 16, false, 0);       // 2 beats: no ethertype... (16B has bytes 12-13!) still non-PTP
    ipv4(f, 40, 0x55); send(f, 40, false, 0);       // eth_type beat present, no seq beat
    memcpy(f, b, 68); f[12] = 0x88; f[13] = 0xF7; f[14] = 0x12;
    send(f, 40, false, 0);                          // PTP-looking but truncated before seq
    gptp(b, 2, 0x0901);
    uint64_t s9 = send(b, 68, false, 0);            // then a good one
    settle(80);
    expect_recs("runts then good", 1);
    check_rec("runts then good", 0, 0, 2, 0x0901);
    (void)s9;

    // 10: VLAN-tagged 88F7 lookalike must not match (gPTP is untagged)
    recs.clear();
    vlan_gptp_lookalike(f);
    send(f, 72, false, 0);
    settle(60);
    expect_recs("vlan lookalike", 0);

    printf("======================================================================\n");
    printf(fails ? "PTP-TS METADATA (interference suite): %d FAILURE(S)\n"
                 : "PTP-TS METADATA (interference suite): ALL PASS\n", fails);
    delete top;
    return fails ? 1 : 0;
}
