/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Milan v1.2 Table 5.22 asynchronous push classes (VERSION 0x0024): the
 * four notifications the entity volunteers WITHOUT a causing command -
 * GET_STREAM_INFO(STREAM_INPUT) for sink 0 and the CRF sink off the
 * change-signature dwell, GET_AVB_INFO off the gPTP identity signature
 * (1 Hz-bounded), GET_AS_PATH off {GM, parent}, GET_COUNTERS(CLOCK_DOMAIN)
 * off the media-lock tallies (Table 5.22's own 1/s-per-descriptor bound).
 * Compiled against the deployed shape (gen/: inputs = [AAF, CRF]) with
 * CLK_FREQ_HZ_P=100000, so one KL_aecp_timers millisecond = 100 cycles and
 * the 16 ms dwell / 1000 ms windows run in-sim for real. Exit 0 = pass.
 */

#include "VKL_aecp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>

#define N_AAF_SINKS_TB 1      /* deployed gen/ shape: inputs = [AAF, CRF] */

static VKL_aecp_top* dut;
static long checks = 0, fails = 0;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}
static void run_cycles(int n) { for (int i = 0; i < n; i++) tick(); }
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-52s = %ld\n", what, got); }
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
    f.push_back(0xFB);
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

static std::vector<uint8_t> collect_resp(int budget = 6000) {
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
static int r_cdl(const std::vector<uint8_t>& b){ return b.size()>17 ? (((b[16]&7)<<8)|b[17]) : -1; }
static int r_cmd(const std::vector<uint8_t>& b){ return b.size()>37 ? (((b[36]&0x7F)<<8)|b[37]) : -1; }
static int r_seq(const std::vector<uint8_t>& b){ return b.size()>35 ? ((b[34]<<8)|b[35]) : -1; }
static int u_bit(const std::vector<uint8_t>& b){ return b.size()>36 ? (b[36]>>7)&1 : -1; }
static uint64_t be_at(const std::vector<uint8_t>& b, int off, int n) {
    if ((int)b.size() < off + n) return ~0ULL;   // short frame: poison value
    uint64_t v = 0;
    for (int i = 0; i < n; i++) v = (v << 8) | b[off + i];
    return v;
}
//! wait with AXIS backpressure held, so a push firing mid-wait PARKS at the
//! stream boundary instead of draining unobserved, then collect it
static std::vector<uint8_t> wait_push(int cycles) {
    dut->m_axis_tready = 0;
    run_cycles(cycles);
    return collect_resp();
}

static uint16_t seq = 0x5000;
static std::vector<uint8_t> xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
    feed_rx(aem_cmd(cmd, seq++, pl));
    return collect_resp();
}

// the deployed gen/ shape's defaults (AEM_STRIN_FMT_C): 8ch AAF + CRF
static const uint64_t AAF_DEF = 0x0205022002006000ULL;
static const uint64_t CRF48   = 0x041060010000BB80ULL;

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_aecp_top;

    dut->rst_n = 0; dut->enable_i = 1;
    dut->srp_domain_vid_i = 0x002;
    dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    dut->entity_id_i = ENTITY_ID; dut->entity_model_id_i = 0;
    dut->entity_caps_i = 0x00008588; dut->talker_sources_i = 1;
    dut->talker_caps_i = 0x4801; dut->listener_sinks_i = 2;
    dut->listener_caps_i = 0x4801; dut->controller_caps_i = 0;
    dut->available_index_i = 7; dut->association_id_i = 0;
    dut->gptp_gm_id_i = 0; dut->gptp_domain_i = 0;
    dut->pdelay_ns_i = 0x300;      // 768 ns: nonzero so [5]'s jitter case
                                   // cannot flip asCapable
    dut->as_parent_ckid_i = 0;
    dut->link_up_i = 1;
    dut->lstn_bound_i = 0; dut->lstn_sid_i = 0; dut->lstn_dmac_i = 0;
    dut->lstn_vlan_i = 0; dut->lstn_pbsta_i = 0; dut->lstn_acmpsta_i = 0;
    dut->lstn_ta_reg_i = 0; dut->lstn_ta_fail_i = 0;
    dut->lstn_fail_code_i = 0; dut->lstn_fail_bridge_i = 0;
    dut->lstn_ta_vlan_i = 0; dut->lstn_ta_acclat_i = 0;
    dut->lstn1_bound_i = 0; dut->lstn1_sid_i = 0; dut->lstn1_dmac_i = 0;
    dut->in0_cnt_locked_i = 0; dut->in0_cnt_unlocked_i = 0;
    dut->in0_cnt_dirty_p_i = 0; dut->tkdiag_dirty_p_i = 0;
    for (int w = 0; w < 12; w++) dut->rxdiag_cnt_i[w] = 0;
    for (int w = 0; w < 5; w++)  dut->tkdiag_cnt_i[w] = 0;
    dut->n_aaf_sinks_i = N_AAF_SINKS_TB;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|ENT_MAC[i]; dut->station_mac_i = m; }
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    // let the boot-time signature settle (reset prev = 0 vs live init
    // values raises a dirty with nobody registered: it must self-clear)
    run_cycles(3000);

    printf("== Table 5.22 asynchronous pushes — 1 ms = 100 cycles ==\n");

    // ---------------------------------------------------------------- //
    printf("\n[1] STREAM_INPUT[0] stream-info push: dwell gate + content\n");
    {
        feed_rx(aem_cmd(36, 0x5101, {}));
        ck("[1] REGISTER A", r_status(collect_resp()), 0);
        // a bind lands: bound + sid + dmac + vlan + ACMP status + the
        // registered Talker attribute, all within the dwell
        dut->lstn_bound_i   = 1;
        dut->lstn_sid_i     = 0xAAAA00FFFE000007ULL;
        dut->lstn_dmac_i    = 0x91E0F000FE07ULL;
        dut->lstn_vlan_i    = 0x002;
        dut->lstn_acmpsta_i = 0;
        dut->lstn_pbsta_i   = 2;      // PASSIVE/settled per our encoding
        dut->lstn_ta_reg_i  = 1;
        dut->lstn_ta_acclat_i = 500000;
        dut->lstn_ta_vlan_i = 0x002;
        auto r = collect_resp(700);   // < 16 ms: the dwell must hold it
        ck("[1] no push inside the settle dwell", r.size(), 0);
        r = wait_push(2000);          // past 16 ms, backpressured
        ck("[1] push arrived after settle", r.size() > 0, 1);
        ck("[1] push u-bit set", u_bit(r), 1);
        ck("[1] push cmd GET_STREAM_INFO", r_cmd(r), 15);
        ck("[1] push status SUCCESS", r_status(r), 0);
        ck("[1] push CDL 68 (full 56-byte payload)", r_cdl(r), 68);
        ck("[1] push desc STREAM_INPUT idx 0", be_at(r, 38, 4), 0x00050000);
        // no STREAMING_WAIT: power-on state is STARTED (started_in_r
        // resets 0xFFFF; Milan STOP_STREAMING is what clears it)
        ck("[1] flags CONNECTED, no STREAMING_WAIT", be_at(r, 42, 4), 0xF6000000);
        ck("[1] format = sink0 store word", be_at(r, 46, 8) == AAF_DEF, 1);
        ck("[1] stream_id = bound sid", be_at(r, 54, 8) == dut->lstn_sid_i, 1);
        ck("[1] acc latency = TA attribute", be_at(r, 62, 4), 500000);
        ck("[1] dest MAC = bound dmac", be_at(r, 66, 6) == dut->lstn_dmac_i, 1);
        ck("[1] vlan = TA vlan", be_at(r, 82, 2), 0x002);
        ck("[1] flags_ex REGISTERING", be_at(r, 89, 1), 1);
        ck("[1] {pbsta, acmpsta} byte", be_at(r, 90, 1), (2 << 5) | 0);
        ck("[1] push seq 0", r_seq(r), 0);
        r = collect_resp(700);
        ck("[1] exactly one push", r.size(), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[2] burst coalescing: two changes, one settled frame\n");
    {
        dut->lstn_sid_i = 0xAAAA00FFFE000008ULL;   // change 1
        run_cycles(500);                            // 5 ms: inside the dwell
        dut->lstn_ta_acclat_i = 750000;             // change 2 reloads it
        auto r = collect_resp(700);
        ck("[2] still held (dwell reloaded)", r.size(), 0);
        r = wait_push(2000);
        ck("[2] one push after the burst", r.size() > 0, 1);
        ck("[2] it carries the SETTLED sid", be_at(r, 54, 8) == dut->lstn_sid_i, 1);
        ck("[2] it carries the SETTLED latency", be_at(r, 62, 4), 750000);
        ck("[2] push seq 1", r_seq(r), 1);
        r = collect_resp(700);
        ck("[2] no second frame for the burst", r.size(), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[3] CRF Media Clock Input push: its own descriptor + record\n");
    {
        dut->lstn1_bound_i = 1;
        dut->lstn1_sid_i   = 0xBBBB00FFFE0000C5ULL;
        dut->lstn1_dmac_i  = 0x91E0F000FEC5ULL;
        auto r = wait_push(2200);
        ck("[3] CRF push arrived", r.size() > 0, 1);
        ck("[3] desc STREAM_INPUT idx 1 (n_aaf_sinks)", be_at(r, 38, 4), 0x00050001);
        // cross-check the same descriptor through the SOLICITED arms:
        // the push must serve the byte-identical format word
        {
            std::vector<uint8_t> pl; put_be16(pl, 0x0005); put_be16(pl, 1);
            auto rs = xact(15, pl);          // GET_STREAM_INFO(IN,1)
            ck("[3] solicited GSI(IN,1) SUCCESS", r_status(rs), 0);
            ck("[3] solicited fmt == pushed fmt",
               be_at(rs, 46, 8) == be_at(r, 46, 8), 1);
            auto rf = xact(9, pl);           // GET_STREAM_FORMAT(IN,1)
            ck("[3] GET_FMT(IN,1) == pushed fmt",
               be_at(rf, 42, 8) == be_at(r, 46, 8), 1);
        }
        ck("[3] format = CRF store word", be_at(r, 46, 8) == CRF48, 1);
        ck("[3] stream_id = CRF bind record", be_at(r, 54, 8) == dut->lstn1_sid_i, 1);
        ck("[3] dest MAC = CRF record", be_at(r, 66, 6) == dut->lstn1_dmac_i, 1);
        ck("[3] no TA attribute on the CRF sink (lat 0)", be_at(r, 62, 4), 0);
        ck("[3] push seq 2", r_seq(r), 2);
        r = collect_resp(700);
        ck("[3] exactly one push", r.size(), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[4] GM change: counters + GET_AVB_INFO + GET_AS_PATH triple\n");
    {
        dut->gptp_gm_id_i = 0x001B21FFFE55AA00ULL;
        // chain order: AVB_IF GET_COUNTERS (pend3), then AVB_INFO (pend7),
        // then AS_PATH (pend8)
        auto r1 = collect_resp();
        auto r2 = collect_resp();
        auto r3 = collect_resp();
        ck("[4] three pushes", (r1.size()>0) + (r2.size()>0) + (r3.size()>0), 3);
        ck("[4] 1st = GET_COUNTERS", r_cmd(r1), 0x29);
        ck("[4] 1st desc AVB_INTERFACE", be_at(r1, 38, 4), 0x00090000);
        ck("[4] 1st GPTP_GM_CHANGED = 1", be_at(r1, 66, 4), 1);
        ck("[4] 2nd = GET_AVB_INFO", r_cmd(r2), 0x27);
        ck("[4] 2nd u-bit", u_bit(r2), 1);
        ck("[4] 2nd CDL 36 (one msrp mapping)", r_cdl(r2), 36);
        ck("[4] 2nd desc AVB_INTERFACE", be_at(r2, 38, 4), 0x00090000);
        ck("[4] 2nd gm id live", be_at(r2, 42, 8) == dut->gptp_gm_id_i, 1);
        ck("[4] 2nd pdelay live", be_at(r2, 50, 4), 0x300);
        ck("[4] 2nd flags AS_CAP|GPTP|SRP", be_at(r2, 55, 1), 0x07);
        ck("[4] 2nd mapping {A,3,vid 2}", be_at(r2, 58, 4), 0x06030002);
        ck("[4] 3rd = GET_AS_PATH", r_cmd(r3), 0x28);
        ck("[4] 3rd index 0", be_at(r3, 38, 2), 0);
        ck("[4] 3rd count 1 (foreign GM, no parent)", be_at(r3, 41, 1), 1);
        ck("[4] 3rd path[0] = the GM", be_at(r3, 42, 8) == dut->gptp_gm_id_i, 1);
        ck("[4] seqs 3,4,5", (r_seq(r1)==3) && (r_seq(r2)==4) && (r_seq(r3)==5), 1);
        auto r = collect_resp(700);
        ck("[4] no fourth frame", r.size(), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[5] GET_AVB_INFO bound: pdelay jitter silent, real change 1 Hz\n");
    {
        dut->pdelay_ns_i = 0x340;     // +64 ns: inside the 256 ns quantum
        run_cycles(3000);
        auto r = collect_resp(700);
        ck("[5] quantum jitter never pushes", r.size(), 0);
        dut->pdelay_ns_i = 0x900;     // a real move
        r = collect_resp(700);
        ck("[5] real change held by the 1 s window", r.size(), 0);
        r = wait_push(101000);        // > 1000 ms
        ck("[5] pushed at window expiry", r.size() > 0, 1);
        ck("[5] cmd GET_AVB_INFO", r_cmd(r), 0x27);
        ck("[5] carries the LIVE pdelay", be_at(r, 50, 4), 0x900);
        ck("[5] push seq 6", r_seq(r), 6);
    }

    // ---------------------------------------------------------------- //
    printf("\n[6] CLOCK_DOMAIN counters push: media lock, 1/s bound\n");
    {
        dut->in0_cnt_locked_i = 1;    // MEDIA_LOCKED fires
        auto r = collect_resp();
        ck("[6] first lock pushes at once (fresh window)", r.size() > 0, 1);
        ck("[6] cmd GET_COUNTERS", r_cmd(r), 0x29);
        ck("[6] desc CLOCK_DOMAIN idx 0", be_at(r, 38, 4), 0x00240000);
        ck("[6] CDL 148 (full-size)", r_cdl(r), 148);
        ck("[6] valid mask LOCKED|UNLOCKED", be_at(r, 42, 4), 3);
        ck("[6] LOCKED = 1", be_at(r, 46, 4), 1);
        ck("[6] UNLOCKED = 0", be_at(r, 50, 4), 0);
        ck("[6] push seq 7", r_seq(r), 7);
        dut->in0_cnt_unlocked_i = 1;  // unlock inside the window
        r = collect_resp(700);
        ck("[6] second event rate-limited", r.size(), 0);
        r = wait_push(101000);
        ck("[6] pushed at window expiry", r.size() > 0, 1);
        ck("[6] UNLOCKED now 1", be_at(r, 50, 4), 1);
        ck("[6] push seq 8", r_seq(r), 8);
    }

    // ---------------------------------------------------------------- //
    printf("\n[7] deregistration drains every class\n");
    {
        feed_rx(aem_cmd(37, 0x5701, {}));
        ck("[7] DEREGISTER A", r_status(collect_resp()), 0);
        dut->lstn_sid_i       = 0xAAAA00FFFE000009ULL;
        dut->gptp_gm_id_i     = 0x001B21FFFE55AB00ULL;
        dut->in0_cnt_locked_i = 2;
        auto r = wait_push(105000);   // past every dwell and window
        ck("[7] silence after deregistration", r.size(), 0);
    }

    printf("\n----------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
