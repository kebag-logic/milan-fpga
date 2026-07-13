// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for ptp_ts_top's METADATA pipeline. Phase B (HW frame
// timestamps) found ZERO ts records on silicon while frames demonstrably passed
// both taps; this TB reproduces the block end-to-end at the two real ingress
// profiles and gates the fix:
//   * "slow" beats (one beat / 32 clks) = MII 100M into the 50 MHz datapath -
//     the SOP->counter->CDC-handshake timestamp returns BEFORE the ethertype
//     beat has even arrived (dest_req && is_ptp race);
//   * "fast" beats (back-to-back) = TX / GMII profile - on minimal frames the
//     handshake can complete AFTER tlast instead.
// Record contract (2 beats): HIGH = {ns[63:0]}, LOW = {40'0, seq[15:0], 7'0, dir}.
// The seq byte order captured here is the CONTRACT the kl-eth driver matches.

#include <verilated.h>
#include "Vptp_ts_top.h"
#include <cstdio>
#include <cstring>
#include <vector>

static Vptp_ts_top *top;
static vluint64_t t = 0;
static int fails = 0;
static bool verbose = false;

struct Rec { uint64_t ns, meta; };
static std::vector<Rec> recs;
static uint64_t rec_hi;
static bool rec_have_hi = false;
static int ts_ready_pulses = 0;

static void tick()
{
    // one common clock for both domains, exactly like the SoC hookup
    // (i_gtx_clk = ClockSignal(milan_cd) = axis domain).
    // Monitor convention: sample the handshake PRE-edge (low phase, inputs
    // settled) - that is what the posedge commits. Sampling post-edge misses
    // the beat consumed at a backpressure-release edge (the fifo shows the
    // NEXT head immediately after the pop).
    top->gtx_clk = 0; top->axis_clk = 0; top->eval(); t++;
    if (top->o_tx_ts_ready) ts_ready_pulses++;
    if (verbose && top->ts_m_axis_tvalid)
        printf("  t=%llu v=1 r=%d last=%d data=%016llx\n", (unsigned long long)t,
               (int)top->ts_m_axis_tready, (int)top->ts_m_axis_tlast,
               (unsigned long long)top->ts_m_axis_tdata);
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
    top->gtx_clk = 1; top->axis_clk = 1; top->eval(); t++;
}

static void frame_gptp(uint8_t *b, uint16_t seq)   // 68 bytes
{
    memset(b, 0, 68);
    const uint8_t hdr[14] = {0x01,0x80,0xC2,0,0,0x0E, 0x02,0,0,0,0,0x02, 0x88,0xF7};
    memcpy(b, hdr, 14);
    b[14] = 0x12;              // majorSdoId 1 | msgType 2 (pdelay_req)
    b[15] = 0x02;              // version 2
    b[16] = 0; b[17] = 54;     // messageLength
    b[44] = seq >> 8; b[45] = seq & 0xFF;
}

static void frame_ipv4(uint8_t *b)                 // 60 bytes, must NOT record
{
    memset(b, 0, 60);
    const uint8_t hdr[14] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 2,0,0,0,0,2, 0x08,0x00};
    memcpy(b, hdr, 14);
}

// drive one frame into the tx or rx tap; gap = idle cycles between beats.
// BE-lane convention (the real MAC-side datapath byte order, per the milan_dp
// harness and the silicon-proven classifier): FIRST wire byte in tdata[63:56];
// a partial tail therefore occupies the HIGH keep bits (rem=4 -> 0xF0).
static void send(const uint8_t *b, int len, bool tx, int gap)
{
    int nbeats = (len + 7) / 8;
    for (int i = 0; i < nbeats; i++) {
        uint64_t d = 0;
        for (int k = 0; k < 8 && 8 * i + k < len; k++)
            d |= (uint64_t)b[8 * i + k] << (8 * (7 - k));
        int rem = len - 8 * i;
        uint8_t keep = rem >= 8 ? 0xFF : (uint8_t)(0xFF << (8 - rem));
        bool last = i == nbeats - 1;
        if (tx) {
            top->s_axis_tx_tdata = d; top->s_axis_tx_tkeep = keep;
            top->s_axis_tx_tlast = last; top->s_axis_tx_tvalid = 1;
            do { tick(); } while (!top->s_axis_tx_tready);
            top->s_axis_tx_tvalid = 0;
        } else {
            top->s_axis_rx_tdata = d; top->s_axis_rx_tkeep = keep;
            top->s_axis_rx_tlast = last; top->s_axis_rx_tvalid = 1;
            do { tick(); } while (!top->s_axis_rx_tready);
            top->s_axis_rx_tvalid = 0;
        }
        for (int g = 0; g < gap; g++) tick();
    }
}

static void settle(int n) { for (int i = 0; i < n; i++) tick(); }

static void expect_recs(const char *name, size_t n)
{
    if (recs.size() != n) {
        printf("FAIL %s: %zu records (expected %zu)\n", name, recs.size(), n);
        fails++;
    } else {
        printf("PASS %s: %zu record(s)\n", name, n);
    }
}

static void check_rec(const char *name, size_t i, int dir, uint16_t seq)
{
    if (i >= recs.size()) { printf("FAIL %s: record %zu missing\n", name, i); fails++; return; }
    uint64_t m = recs[i].meta, ns = recs[i].ns;
    int rdir = m & 1;
    uint16_t rseq = (m >> 8) & 0xFFFF;
    uint16_t swab = (uint16_t)((seq >> 8) | (seq << 8));
    const char *conv = rseq == seq ? "wire-be16" : (rseq == swab ? "SWAPPED" : "??");
    if (rdir != dir || (rseq != seq && rseq != swab) || ns == 0) {
        printf("FAIL %s rec%zu: dir=%d seq=0x%04x(%s) ns=%llu (want dir=%d seq=0x%04x)\n",
               name, i, rdir, rseq, conv, (unsigned long long)ns, dir, seq);
        fails++;
    } else {
        printf("PASS %s rec%zu: dir=%d seq=0x%04x [%s] ns=%llu\n",
               name, i, rdir, rseq, conv, (unsigned long long)ns);
    }
}

int main(int argc, char **argv)
{
    Verilated::commandArgs(argc, argv);
    top = new Vptp_ts_top;

    top->gtx_resetn = 0; top->axis_resetn = 0;
    top->m_axis_tx_tready = 1; top->m_axis_rx_tready = 1;
    top->ts_m_axis_tready = 1;
    top->i_ptp_enable = 1;
    top->i_ptp_incr = 20u << 24;      // 20 ns/tick Q8.24 (50 MHz datapath)
    top->i_ptp_adj = 0;
    settle(8);
    top->gtx_resetn = 1; top->axis_resetn = 1;
    settle(8);

    uint8_t b[68];

    // 1: RX, slow beats (MII 100M profile - the silicon silence case)
    recs.clear();
    frame_gptp(b, 0x0102);
    send(b, 68, false, 32);
    settle(200);
    expect_recs("rx-slow #1 (first frame after reset)", 1);
    check_rec("rx-slow #1", 0, 0, 0x0102);

    // 2: RX slow again (stale-eth_type artifacts would pass here and hide #1)
    recs.clear();
    frame_gptp(b, 0x0203);
    send(b, 68, false, 32);
    settle(200);
    expect_recs("rx-slow #2", 1);
    check_rec("rx-slow #2", 0, 0, 0x0203);

    // 3: RX back-to-back beats (1G profile)
    recs.clear();
    frame_gptp(b, 0x0304);
    send(b, 68, false, 0);
    settle(200);
    expect_recs("rx-fast", 1);
    check_rec("rx-fast", 0, 0, 0x0304);

    // 4: TX back-to-back + the IRQ event
    recs.clear();
    int pulses0 = ts_ready_pulses;
    frame_gptp(b, 0x1122);
    send(b, 68, true, 0);
    settle(200);
    expect_recs("tx-fast", 1);
    check_rec("tx-fast", 0, 1, 0x1122);
    if (ts_ready_pulses == pulses0) { printf("FAIL tx: o_tx_ts_ready never pulsed\n"); fails++; }
    else printf("PASS tx: o_tx_ts_ready pulsed\n");

    // 5: non-PTP must not record NOR poison the next PTP frame
    recs.clear();
    uint8_t ip[60]; frame_ipv4(ip);
    send(ip, 60, false, 4);
    settle(100);
    frame_gptp(b, 0x0405);
    send(b, 68, false, 4);
    settle(200);
    expect_recs("ipv4+gptp pair", 1);
    check_rec("ipv4+gptp pair", 0, 0, 0x0405);

    // 6: backpressure on ts_m_axis while a record emits
    recs.clear();
    top->ts_m_axis_tready = 0;
    frame_gptp(b, 0x0506);
    send(b, 68, false, 0);
    settle(100);                       // record waits in the fifos
    top->ts_m_axis_tready = 1;
    settle(200);
    expect_recs("backpressured", 1);
    check_rec("backpressured", 0, 0, 0x0506);

    // 7: interleaved TX+RX (RR mux) - one of each, both must surface
    recs.clear();
    frame_gptp(b, 0x0708);
    send(b, 68, true, 0);
    frame_gptp(b, 0x0809);
    send(b, 68, false, 0);
    settle(300);
    expect_recs("tx+rx pair", 2);

    printf("======================================================================\n");
    printf(fails ? "PTP-TS METADATA: %d FAILURE(S)\n" : "PTP-TS METADATA: ALL PASS\n", fails);
    delete top;
    return fails ? 1 : 0;
}
