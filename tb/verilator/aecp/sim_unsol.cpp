/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Milan v1.2 Table 5.22 asynchronous push classes (VERSION 0x0024): the
 * notifications the entity volunteers WITHOUT a causing command -
 * GET_STREAM_INFO(STREAM_INPUT) for sink 0 and the CRF sink off the
 * change-signature dwell, GET_AVB_INFO off the gPTP identity signature
 * (1 Hz-bounded), GET_AS_PATH off {GM, parent}, GET_COUNTERS(CLOCK_DOMAIN)
 * off the media-lock tallies (Table 5.22's own 1/s-per-descriptor bound).
 * gh #60 adds: [9] the AVB_INTERFACE row's own 1 s window (a 5 Hz link
 * flap collapses to 1 immediate + 1 accumulated-totals window frame),
 * [10] per-sink STREAM_INPUT GET_COUNTERS pushes off the monitor's dirty
 * vector (per-descriptor windows), [11] the CRF sink's own GET_COUNTERS
 * push at index n_aaf_sinks with mask 0x0F3F, [12] the sink-0 push serving
 * the SAME mirror slice the solicited path serves even at clk_src=2 (the
 * retired in0_* payload took the datapath's active-source mux splice).
 * gh #58 D4 adds: [13] the 60 s lock auto-expiry u=1 LOCK_ENTITY push to
 * every registered controller (Milan 5.4.2.2 note) - and to nobody else.
 * Compiled against the deployed shape (gen/: inputs = [AAF, CRF]) with
 * CLK_FREQ_HZ_P=100000, so one KL_aecp_timers millisecond = 100 cycles and
 * the 16 ms dwell / 1000 ms windows / 60 s lock timer run in-sim for real.
 * Exit 0 = pass.
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

//! AEM command frame layout: 14 B Ethernet + 4 B AVTP common header + 8 B
//! target_entity_id + 8 B controller_entity_id + 2 B sequence_id + 2 B
//! u/command_type = 38 B ahead of the command_specific payload, and the whole
//! frame is padded up to the 60 B Ethernet minimum.
static const size_t AEM_HDR_BYTES = 38;
static const size_t ETH_MIN_BYTES = 60;

//! Widest AEM response this suite collects (a READ_DESCRIPTOR reply), used to
//! size the collector once instead of growing it a beat at a time.
static const size_t AEM_RESP_BYTES = 600;

//! One reusable stimulus buffer for the whole run. The builder below fills it
//! through a reference and clear() keeps its capacity, so the command bytes
//! cost ONE allocation for the entire simulation instead of a malloc plus
//! three or four reallocs on every transaction.
static std::vector<uint8_t> stim;

//! Fill `out` with an AEM command frame from an arbitrary controller and
//! hand back a reference to it, so a call site reads
//! `feed_rx(build_aem_cmd2(stim, ...))` and reuses one buffer.
static const std::vector<uint8_t>& build_aem_cmd2(std::vector<uint8_t>& out,
                                     const uint8_t* smac, uint64_t cid,
                                     uint16_t cmd, uint16_t seq,
                                     const std::vector<uint8_t>& payload) {
    size_t want = AEM_HDR_BYTES + payload.size();
    out.clear();                                // clear KEEPS the capacity
    out.reserve(want < ETH_MIN_BYTES ? ETH_MIN_BYTES : want);
    std::vector<uint8_t>& f = out;
    for (int i=0;i<6;i++) f.push_back(ENT_MAC[i]);
    for (int i=0;i<6;i++) f.push_back(smac[i]);
    put_be16(f, 0x22F0);
    f.push_back(0xFB);
    f.push_back(0x00);                          // AEM_COMMAND
    uint16_t cdl = 12 + (uint16_t)payload.size();
    f.push_back((cdl >> 8) & 0x7);
    f.push_back(cdl & 0xFF);
    put_be64(f, ENTITY_ID);
    put_be64(f, cid);
    put_be16(f, seq);
    f.push_back((cmd >> 8) & 0x7F);
    f.push_back(cmd & 0xFF);
    for (auto b : payload) f.push_back(b);
    while (f.size() < ETH_MIN_BYTES) f.push_back(0x00);
    return out;
}
//! Same, addressed from this suite's default controller.
static const std::vector<uint8_t>& build_aem_cmd(std::vector<uint8_t>& out,
                                    uint16_t cmd, uint16_t seq,
                                    const std::vector<uint8_t>& payload) {
    return build_aem_cmd2(out, CTL_MAC, CTLR_ID, cmd, seq, payload);
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
    b.reserve(AEM_RESP_BYTES);          // one allocation, not one per beat run
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
    feed_rx(build_aem_cmd(stim, cmd, seq++, pl));
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
    // the tapped lane's consumer is idle-ready; the gh #65 leg parks it
    dut->rx_tready_i = 1;
    dut->entity_id_i = ENTITY_ID; dut->entity_model_id_i = 0;
    dut->entity_caps_i = 0x00008588; dut->talker_sources_i = 1;
    dut->talker_caps_i = 0x4801; dut->listener_sinks_i = 2;
    dut->listener_caps_i = 0x4801; dut->controller_caps_i = 0;
    dut->available_index_i = 7; dut->association_id_i = 0;
    dut->gptp_gm_id_i = 0; dut->gptp_domain_i = 0;
    dut->pdelay_ns_i = 0x300;      // 768 ns: a measured value; since gh #64
                                   // J3 it no longer decides asCapable
    // gh #64 J3: asCapable is its own leased IEEE 802.1AS-2020 10.2.5.1
    // input. TRUE here = the healthy link every earlier case assumes.
    dut->as_capable_i = 1;
    dut->as_parent_ckid_i = 0;
    // gh #64 J4: nothing published -> the legacy [GM, parent] derivation,
    // which is what cases [4] and below expect on the wire
    for (int w = 0; w < 14; w++) dut->asp_path_i[w] = 0;
    dut->asp_count_i = 0; dut->asp_gen_i = 0;
    dut->link_up_i = 1;
    dut->lstn_bound_i = 0; dut->lstn_sid_i = 0; dut->lstn_dmac_i = 0;
    dut->lstn_vlan_i = 0; dut->lstn_pbsta_i = 0; dut->lstn_acmpsta_i = 0;
    dut->lstn_ta_reg_i = 0; dut->lstn_ta_fail_i = 0;
    dut->lstn_fail_code_i = 0; dut->lstn_fail_bridge_i = 0;
    dut->lstn_ta_vlan_i = 0; dut->lstn_ta_acclat_i = 0;
    dut->lstn1_bound_i = 0; dut->lstn1_sid_i = 0; dut->lstn1_dmac_i = 0;
    dut->in0_cnt_locked_i = 0; dut->in0_cnt_unlocked_i = 0;
    dut->rxdiag_dirty_p_i = 0; dut->crf_cnt_dirty_p_i = 0;
    dut->tkdiag_dirty_p_i = 0;
    for (int w = 0; w < 12; w++) dut->rxdiag_cnt_i[w] = 0;
    for (int w = 0; w < 5; w++)  dut->tkdiag_cnt_i[w] = 0;
    dut->n_aaf_sinks_i = N_AAF_SINKS_TB;
    // gh #58 stream-command law truth vectors: wake unbound / not streaming
    dut->lstn_bound_v_i = 0; dut->out_streaming_v_i = 0;
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
        feed_rx(build_aem_cmd(stim, 36, 0x5101, {}));
        ck("[1] REGISTER A", r_status(collect_resp()), 0);
        // a bind lands: bound + sid + dmac + vlan + ACMP status + the
        // registered Talker attribute, all within the dwell
        dut->lstn_bound_i   = 1;
        dut->lstn_sid_i     = 0xAAAA00FFFE000007ULL;
        dut->lstn_dmac_i    = 0x91E0F000FE07ULL;
        dut->lstn_vlan_i    = 0x002;
        dut->lstn_acmpsta_i = 0;
        dut->lstn_pbsta_i   = 3;      // PASSIVE/settled per our encoding
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
        ck("[1] flags CONNECTED, no STREAMING_WAIT", be_at(r, 42, 4), 0xF6000006);
        ck("[1] format = sink0 store word", be_at(r, 46, 8) == AAF_DEF, 1);
        ck("[1] stream_id = bound sid", be_at(r, 54, 8) == dut->lstn_sid_i, 1);
        ck("[1] acc latency = TA attribute", be_at(r, 62, 4), 500000);
        ck("[1] dest MAC = bound dmac", be_at(r, 66, 6) == dut->lstn_dmac_i, 1);
        ck("[1] vlan = TA vlan", be_at(r, 82, 2), 0x002);
        ck("[1] flags_ex REGISTERING", be_at(r, 89, 1), 1);
        ck("[1] {pbsta, acmpsta} byte", be_at(r, 90, 1), (3 << 5) | 0);
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
        // arrival order: AS_PATH (pend8, armed straight off the signature)
        // first, then AVB_IF GET_COUNTERS (pend3) and AVB_INFO (pend7) in
        // chain order - gh #60 F1 put a dirty stage in front of pend3, so
        // its arm lands one cycle behind pend8's and the arbiter has
        // already taken AS_PATH. The spec orders nothing between classes;
        // the content and the exactly-three law are what matter.
        auto r1 = collect_resp();
        auto r2 = collect_resp();
        auto r3 = collect_resp();
        ck("[4] three pushes", (r1.size()>0) + (r2.size()>0) + (r3.size()>0), 3);
        ck("[4] 1st = GET_AS_PATH", r_cmd(r1), 0x28);
        ck("[4] 1st index 0", be_at(r1, 38, 2), 0);
        ck("[4] 1st count 1 (foreign GM, no parent)", be_at(r1, 41, 1), 1);
        ck("[4] 1st path[0] = the GM", be_at(r1, 42, 8) == dut->gptp_gm_id_i, 1);
        ck("[4] 2nd = GET_COUNTERS", r_cmd(r2), 0x29);
        ck("[4] 2nd desc AVB_INTERFACE", be_at(r2, 38, 4), 0x00090000);
        ck("[4] 2nd GPTP_GM_CHANGED = 1", be_at(r2, 66, 4), 1);
        ck("[4] 3rd = GET_AVB_INFO", r_cmd(r3), 0x27);
        ck("[4] 3rd u-bit", u_bit(r3), 1);
        ck("[4] 3rd CDL 36 (one msrp mapping)", r_cdl(r3), 36);
        ck("[4] 3rd desc AVB_INTERFACE", be_at(r3, 38, 4), 0x00090000);
        ck("[4] 3rd gm id live", be_at(r3, 42, 8) == dut->gptp_gm_id_i, 1);
        ck("[4] 3rd pdelay live", be_at(r3, 50, 4), 0x300);
        ck("[4] 3rd flags AS_CAP|GPTP|SRP", be_at(r3, 55, 1), 0x07);
        ck("[4] 3rd mapping {A,3,vid 2}", be_at(r3, 58, 4), 0x06030002);
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
        feed_rx(build_aem_cmd(stim, 37, 0x5701, {}));
        ck("[7] DEREGISTER A", r_status(collect_resp()), 0);
        dut->lstn_sid_i       = 0xAAAA00FFFE000009ULL;
        dut->gptp_gm_id_i     = 0x001B21FFFE55AB00ULL;
        dut->in0_cnt_locked_i = 2;
        auto r = wait_push(105000);   // past every dwell and window
        ck("[7] silence after deregistration", r.size(), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[8] gh #58 D1: a REFUSED SET replays NOTHING; the accepted "
           "twin replays u=1\n");
    {
        const uint8_t MAC_B[6] = {0x68,0x05,0xCA,0x00,0x00,0xB0};
        const uint64_t CID_B = 0x680500FFFE0000B0ULL;
        const uint64_t AAF2  = 0x0205022000806000ULL;   // differing family value
        feed_rx(build_aem_cmd(stim, 36, 0x5801, {}));
        ck("[8] re-REGISTER A", r_status(collect_resp()), 0);
        // sink 0 binds (the level the datapath drives from acmpl_bound_v_w)
        dut->lstn_bound_v_i = 0x0001;
        std::vector<uint8_t> p2; put_be16(p2, 0x0005); put_be16(p2, 0);
        put_be64(p2, AAF2);
        feed_rx(build_aem_cmd2(stim, MAC_B, CID_B, 8, 0x5802, p2));
        auto r = collect_resp();
        ck("[8] bound SET refused STREAM_IS_RUNNING", r_status(r), 12);
        r = collect_resp(700);
        ck("[8] refusal -> NO u=1 replay to A", (long)r.size(), 0);
        {
            std::vector<uint8_t> g; put_be16(g, 0x0005); put_be16(g, 0);
            auto rf = xact(9, g);
            ck("[8] format untouched by the refusal",
               be_at(rf, 42, 8) == AAF_DEF, 1);
        }
        // this shape wakes with the identity map on stream 0 ch0..7, and
        // Milan 5.4.2.7 (gh #58 D2) refuses a shrink that would orphan
        // them: REMOVE ch2..7 first (the mandated controller order). The
        // REMOVE itself replays u=1 to A - drain it.
        {
            std::vector<uint8_t> rm; put_be16(rm, 0x000E); put_be16(rm, 0);
            put_be16(rm, 6); put_be16(rm, 0);
            for (uint16_t c = 2; c < 8; c++) {
                put_be16(rm, 0); put_be16(rm, c);       // stream 0, channel c
                put_be16(rm, c); put_be16(rm, 0);       // cluster c, cc 0
            }
            feed_rx(build_aem_cmd2(stim, MAC_B, CID_B, 45, 0x5806, rm));
            ck("[8] REMOVE the ch2..7 identity rows (5.4.2.7 blockers)",
               r_status(collect_resp()), 0);
            (void)collect_resp();                 // its u=1 replay to A
        }
        // unbind: the SAME differing SET is accepted and replayed to A
        dut->lstn_bound_v_i = 0;
        feed_rx(build_aem_cmd2(stim, MAC_B, CID_B, 8, 0x5803, p2));
        r = collect_resp();
        ck("[8] unbound SET SUCCESS", r_status(r), 0);
        r = collect_resp();
        ck("[8] replay (u=1) to A arrived", u_bit(r), 1);
        ck("[8] replay dst = A's MAC",
           r.size() >= 6 && memcmp(r.data(), CTL_MAC, 6) == 0, 1);
        ck("[8] replay is the SET_STREAM_FORMAT response", r_cmd(r), 8);
        ck("[8] replay status SUCCESS", r_status(r), 0);
        // restore: format back to the default (a GROW, never checked),
        // then the identity rows - each drains one more replay to A
        std::vector<uint8_t> p8; put_be16(p8, 0x0005); put_be16(p8, 0);
        put_be64(p8, AAF_DEF);
        feed_rx(build_aem_cmd2(stim, MAC_B, CID_B, 8, 0x5804, p8));
        ck("[8] restore default fmt", r_status(collect_resp()), 0);
        (void)collect_resp();                     // its replay to A
        {
            std::vector<uint8_t> ad; put_be16(ad, 0x000E); put_be16(ad, 0);
            put_be16(ad, 6); put_be16(ad, 0);
            for (uint16_t c = 2; c < 8; c++) {
                put_be16(ad, 0); put_be16(ad, c);
                put_be16(ad, c); put_be16(ad, 0);
            }
            feed_rx(build_aem_cmd2(stim, MAC_B, CID_B, 44, 0x5807, ad));
            ck("[8] re-ADD the identity rows (hygiene)",
               r_status(collect_resp()), 0);
            (void)collect_resp();                 // its u=1 replay to A
        }
        feed_rx(build_aem_cmd(stim, 37, 0x5805, {}));
        ck("[8] DEREGISTER A", r_status(collect_resp()), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[9] gh #60 F1: AVB_INTERFACE push clamped to 1/s under a "
           "5 Hz link flap\n");
    {
        feed_rx(build_aem_cmd(stim, 36, 0x5901, {}));
        ck("[9] REGISTER A", r_status(collect_resp()), 0);
        // baseline raw totals through the solicited arm
        std::vector<uint8_t> pl; put_be16(pl, 0x0009); put_be16(pl, 0);
        auto rb = xact(41, pl);
        ck("[9] solicited GET_COUNTERS(AVB_IF) SUCCESS", r_status(rb), 0);
        long up0 = (long)be_at(rb, 46, 4), dn0 = (long)be_at(rb, 50, 4);
        // first edge of the flap: the window rides out saturated, so it
        // pushes at once - the immediate frame
        dut->link_up_i = 0;
        auto p1 = collect_resp();
        ck("[9] first edge pushes at once", p1.size() > 0, 1);
        ck("[9] push desc AVB_INTERFACE", be_at(p1, 38, 4), 0x00090000);
        ck("[9] immediate frame LINK_DOWN +1", (long)be_at(p1, 50, 4), dn0 + 1);
        // 9 more edges at 5 Hz (one every 100 ms): all inside the window
        for (int e = 1; e < 10; e++) {
            run_cycles(10000);
            dut->link_up_i = e & 1;
        }
        // the window expires ~1 s after the immediate frame: ONE deferred
        // frame carrying the ACCUMULATED raw totals (5 downs + 5 ups all
        // counted - the totals never throttle, only the notifications)
        auto p2 = wait_push(15000);
        ck("[9] ONE window frame after the flap", p2.size() > 0, 1);
        ck("[9] accumulated LINK_DOWN total", (long)be_at(p2, 50, 4), dn0 + 5);
        ck("[9] accumulated LINK_UP total", (long)be_at(p2, 46, 4), up0 + 5);
        // flap over, dirty consumed: a further full window stays silent
        auto p3 = wait_push(101000);
        ck("[9] no third frame (flap ended)", (long)p3.size(), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[10] gh #60 F2: per-sink counter push - sink 1 arms its OWN "
           "descriptor\n");
    {
        // distinct mirror words: the pre-mux serves the PUSH's index while
        // it waits in IDLE, so this bus is "the pending sink's slice"
        for (int w = 0; w < 12; w++) dut->rxdiag_cnt_i[w] = 0x100 + w;
        dut->rxdiag_dirty_p_i = 0x0002; tick(); dut->rxdiag_dirty_p_i = 0;
        auto r = collect_resp();
        ck("[10] sink-1 push arrived", r.size() > 0, 1);
        ck("[10] u=1 GET_COUNTERS", (u_bit(r) == 1) && (r_cmd(r) == 0x29), 1);
        ck("[10] desc bytes 00 05 00 01", be_at(r, 38, 4), 0x00050001);
        ck("[10] valid mask 0xFFF", be_at(r, 42, 4), 0xFFF);
        ck("[10] CDL 148", r_cdl(r), 148);
        ck("[10] ML = mirror slice 0", be_at(r, 46, 4), 0x100);
        ck("[10] TV = mirror slice 10", be_at(r, 70, 4), 0x10A);
        ck("[10] TNV = mirror slice 11", be_at(r, 74, 4), 0x10B);
        ck("[10] UF = mirror slice 6", be_at(r, 78, 4), 0x106);
        ck("[10] FRX = mirror slice 9", be_at(r, 90, 4), 0x109);
        ck("[10] sink 0 quiet (exactly one frame)",
           (long)collect_resp(700).size(), 0);
        // per-descriptor windows: sink 1 is clamped now, sink 2's first
        // dirty still pushes at once
        dut->rxdiag_dirty_p_i = 0x0002; tick(); dut->rxdiag_dirty_p_i = 0;
        ck("[10] sink-1 second dirty clamped",
           (long)collect_resp(700).size(), 0);
        dut->rxdiag_dirty_p_i = 0x0004; tick(); dut->rxdiag_dirty_p_i = 0;
        r = collect_resp();
        ck("[10] sink-2 pushes immediately (own window)", r.size() > 0, 1);
        ck("[10] its desc bytes 00 05 00 02", be_at(r, 38, 4), 0x00050002);
        // sink 1's clamped dirty is OWED, not lost: it fires at window
        // expiry with the values current THEN
        r = wait_push(101000);
        ck("[10] sink-1 deferred frame at window expiry", r.size() > 0, 1);
        ck("[10] deferred frame desc 00 05 00 01", be_at(r, 38, 4), 0x00050001);
        ck("[10] then silence", (long)collect_resp(700).size(), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[11] gh #60 F2: CRF sink push at index n_aaf_sinks, mask "
           "0x0F3F\n");
    {
        dut->crf_cnt_locked_i   = 21;
        dut->crf_cnt_unlocked_i = 22;
        dut->crf_cnt_intr_i     = 23;
        dut->crf_cnt_seqerr_i   = 24;
        dut->crf_cnt_mreset_i   = 25;
        dut->crf_cnt_tu_i       = 26;
        dut->crf_cnt_fmterr_i   = 27;
        dut->crf_cnt_late_i     = 28;
        dut->crf_cnt_early_i    = 0x00010000;   // gh #61 G1: full 32 bits ride
        dut->crf_cnt_pdu_i      = 30;
        dut->crf_cnt_dirty_p_i = 1; tick(); dut->crf_cnt_dirty_p_i = 0;
        auto r = collect_resp();
        ck("[11] CRF push arrived", r.size() > 0, 1);
        ck("[11] u=1 GET_COUNTERS", (u_bit(r) == 1) && (r_cmd(r) == 0x29), 1);
        ck("[11] desc = STREAM_INPUT[n_aaf_sinks]", be_at(r, 38, 4),
           0x00050000 + N_AAF_SINKS_TB);
        ck("[11] valid mask 0x0F3F", be_at(r, 42, 4), 0xF3F);
        ck("[11] CDL 148", r_cdl(r), 148);
        ck("[11] ML", be_at(r, 46, 4), 21);
        ck("[11] MU", be_at(r, 50, 4), 22);
        ck("[11] SI", be_at(r, 54, 4), 23);
        ck("[11] SM", be_at(r, 58, 4), 24);
        ck("[11] MR", be_at(r, 62, 4), 25);
        ck("[11] TU", be_at(r, 66, 4), 26);
        ck("[11] TV/TNV unclaimed zero", be_at(r, 70, 4) | be_at(r, 74, 4), 0);
        ck("[11] UF", be_at(r, 78, 4), 27);
        ck("[11] LT", be_at(r, 82, 4), 28);
        ck("[11] ET rides the FULL width (65536, not a 16-bit slice)",
           be_at(r, 86, 4), 0x00010000);
        ck("[11] FRX", be_at(r, 90, 4), 30);
        ck("[11] exactly one frame", (long)collect_resp(700).size(), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[12] gh #60 F3: at clk_src=2 the sink-0 PUSH byte-equals the "
           "solicited answer\n");
    {
        std::vector<uint8_t> sc; put_be16(sc, 0x0024); put_be16(sc, 0);
        put_be16(sc, 2); put_be16(sc, 0);
        auto rs = xact(22, sc);
        ck("[12] SET_CLOCK_SOURCE(2) SUCCESS", r_status(rs), 0);
        // the active-source mux (a datapath fact, TB-driven here) now
        // carries CRF lock tallies - values deliberately DIFFERENT from
        // the sink-0 mirror slice, so any payload still reading the mux
        // is caught byte-red-handed
        dut->in0_cnt_locked_i = 77; dut->in0_cnt_unlocked_i = 66;
        auto rc = collect_resp();
        ck("[12] CLOCK_DOMAIN push still carries the mux", rc.size() > 0, 1);
        ck("[12] its desc CLOCK_DOMAIN/0", be_at(rc, 38, 4), 0x00240000);
        ck("[12] its LOCKED = mux value", be_at(rc, 46, 4), 77);
        ck("[12] its UNLOCKED = mux value", be_at(rc, 50, 4), 66);
        // sink 0's own mirror slice + dirty
        for (int w = 0; w < 12; w++) dut->rxdiag_cnt_i[w] = 0x300 + w;
        dut->rxdiag_dirty_p_i = 0x0001; tick(); dut->rxdiag_dirty_p_i = 0;
        auto rp = collect_resp();
        ck("[12] sink-0 push arrived", rp.size() > 0, 1);
        ck("[12] its desc 00 05 00 00", be_at(rp, 38, 4), 0x00050000);
        std::vector<uint8_t> gp; put_be16(gp, 0x0005); put_be16(gp, 0);
        auto rq = xact(41, gp);
        ck("[12] solicited GET_COUNTERS(IN,0) SUCCESS", r_status(rq), 0);
        long neq = 0;
        for (int w = 0; w < 12; w++)
            if (be_at(rp, 46 + 4 * w, 4) != be_at(rq, 46 + 4 * w, 4)) neq++;
        ck("[12] push == solicited on all 12 words (ML/MU included)", neq, 0);
        ck("[12] ML is the MIRROR value, never the mux splice",
           be_at(rp, 46, 4), 0x300);
    }

    // ---------------------------------------------------------------- //
    printf("\n[13] gh #58 D4: 60 s lock auto-expiry pushes u=1 LOCK_ENTITY "
           "to the registered controllers\n");
    {
        // A registered since [9]; add B; C locks WITHOUT registering
        const uint8_t MAC_B[6] = {0x68,0x05,0xCA,0x00,0x00,0xB0};
        const uint64_t CID_B = 0x680500FFFE0000B0ULL;
        const uint8_t MAC_C[6] = {0x68,0x05,0xCA,0x00,0x00,0xC0};
        const uint64_t CID_C = 0x680500FFFE0000C0ULL;
        feed_rx(build_aem_cmd2(stim, MAC_B, CID_B, 36, 0x5D01, {}));
        ck("[13] REGISTER B", r_status(collect_resp()), 0);
        std::vector<uint8_t> lk(16, 0);   // flags 0, locked_id 0, ENTITY/0
        feed_rx(build_aem_cmd2(stim, MAC_C, CID_C, 1, 0x5D02, lk));
        ck("[13] C LOCK SUCCESS", r_status(collect_resp()), 0);
        ck("[13] no push while the lock lives", (long)wait_push(2000).size(), 0);
        // 60 000 ticks x 100 cycles/ms; margin for the expiry pulse itself
        auto p1 = wait_push(6020000);
        ck("[13] expiry push 1 arrived", p1.size() > 0, 1);
        ck("[13] u=1", u_bit(p1), 1);
        ck("[13] cmd LOCK_ENTITY (0x0001)", r_cmd(p1), 1);
        ck("[13] status SUCCESS", r_status(p1), 0);
        ck("[13] CDL 28", r_cdl(p1), 28);
        ck("[13] flags bytes 38-41 = 00 00 00 01 (UNLOCK)", be_at(p1, 38, 4), 1);
        ck("[13] locked_id 0", be_at(p1, 42, 8) == 0, 1);
        ck("[13] desc ENTITY/0", be_at(p1, 50, 4), 0);
        ck("[13] first frame to A",
           p1.size() >= 6 && memcmp(p1.data(), CTL_MAC, 6) == 0, 1);
        auto p2 = collect_resp();
        ck("[13] expiry push 2 arrived", p2.size() > 0, 1);
        ck("[13] second frame to B",
           p2.size() >= 6 && memcmp(p2.data(), MAC_B, 6) == 0, 1);
        ck("[13] same UNLOCK shape to B",
           (r_cmd(p2) == 1) && (u_bit(p2) == 1) && (be_at(p2, 38, 4) == 1), 1);
        ck("[13] exactly 2 pushes - C never registered",
           (long)collect_resp(700).size(), 0);
        // the state really cleared: B locks IMMEDIATELY (a live lock would
        // answer ENTITY_LOCKED) and that lock pushes NOTHING
        feed_rx(build_aem_cmd2(stim, MAC_B, CID_B, 1, 0x5D03, lk));
        ck("[13] B locks immediately after expiry", r_status(collect_resp()), 0);
        ck("[13] a fresh LOCK pushes nothing", (long)collect_resp(700).size(), 0);
        // explicit UNLOCK: state clears with NO notification (the Milan
        // 5.4.2.2 note names only the AUTOMATIC unlock)
        std::vector<uint8_t> ul(16, 0); ul[3] = 0x01;
        feed_rx(build_aem_cmd2(stim, MAC_B, CID_B, 1, 0x5D04, ul));
        ck("[13] B explicit UNLOCK SUCCESS", r_status(collect_resp()), 0);
        ck("[13] explicit UNLOCK -> NO push", (long)wait_push(2000).size(), 0);
        feed_rx(build_aem_cmd(stim, 37, 0x5D05, {}));
        ck("[13] DEREGISTER A", r_status(collect_resp()), 0);
        feed_rx(build_aem_cmd2(stim, MAC_B, CID_B, 37, 0x5D06, {}));
        ck("[13] DEREGISTER B", r_status(collect_resp()), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[14] gh #64 J3: asCapable is a Table 5.22 push trigger, and "
           "the FALLING edge is the one that matters\n");
    {
        // Milan v1.2 Table 5.22 names asCapable a GET_AVB_INFO push trigger.
        // With the retired |pdelay| proxy the trigger could never fire on a
        // daemon death (pdelay is a stored CSR - it just sits there), so the
        // controller kept an AS_CAPABLE=true entity on screen forever. The
        // leased input falls when the lease lapses, and THAT is this edge.
        feed_rx(build_aem_cmd(stim, 36, 0x5E01, {}));
        ck("[14] REGISTER A", r_status(collect_resp()), 0);
        ck("[14] registration alone pushes nothing",
           (long)wait_push(2000).size(), 0);

        dut->as_capable_i = 0;
        auto r = wait_push(2000);
        ck("[14] asCapable fell -> a push arrived", r.size() > 0, 1);
        ck("[14] u-bit set", u_bit(r), 1);
        ck("[14] cmd GET_AVB_INFO", r_cmd(r), 0x27);
        ck("[14] desc AVB_INTERFACE", be_at(r, 38, 4), 0x00090000);
        // THE MUTATION CHECK: pdelay is unchanged and nonzero across this
        // whole case, so the proxy would have kept bit 0 set here.
        ck("[14] flags GPTP|SRP, AS_CAPABLE CLEAR", be_at(r, 55, 1), 0x06);
        ck("[14] pdelay unchanged on the wire", be_at(r, 50, 4), 0x900);
        ck("[14] exactly one frame for the edge",
           (long)collect_resp(700).size(), 0);

        // ...and the rising edge comes back, behind the 1 s window the
        // GET_AVB_INFO row shares with the pdelay term
        dut->as_capable_i = 1;
        ck("[14] rise held by the 1 s window", (long)collect_resp(700).size(), 0);
        r = wait_push(101000);
        ck("[14] asCapable rose -> a push arrived", r.size() > 0, 1);
        ck("[14] cmd GET_AVB_INFO", r_cmd(r), 0x27);
        ck("[14] flags GPTP|SRP|AS_CAPABLE", be_at(r, 55, 1), 0x07);
    }

    // ---------------------------------------------------------------- //
    printf("\n[15] gh #64 J4: a PUBLISH arms the GET_AS_PATH push, and the "
           "generation makes a re-publish an edge\n");
    {
        // publish [GM, bridge A, bridge B] - a depth the old two-entry
        // derivation could not express at all
        dut->asp_path_i[0] = 0xFEFE0210u; dut->asp_path_i[1] = 0x3CC0C6FFu;
        dut->asp_path_i[2] = 0xFE001122u; dut->asp_path_i[3] = 0xAABBCCFFu;
        dut->asp_count_i = 3; dut->asp_gen_i = 1;
        auto p1 = wait_push(2000);
        ck("[15] publish pushed", p1.size() > 0, 1);
        ck("[15] u-bit set", u_bit(p1), 1);
        ck("[15] cmd GET_AS_PATH", r_cmd(p1), 0x28);
        ck("[15] descriptor_index 0", be_at(p1, 38, 2), 0);
        ck("[15] CDL 40 (16 + 8*3)", r_cdl(p1), 40);
        ck("[15] count 3", be_at(p1, 40, 2), 3);
        // entry 0 comes from the LIVE grandmaster register, never from a
        // slot - so it tracks whatever ADP_GM holds at this point in the run
        ck("[15] path[0] = the live grandmaster",
           be_at(p1, 42, 8) == dut->gptp_gm_id_i, 1);
        ck("[15] path[1] = slot 1", be_at(p1, 50, 8), 0x3CC0C6FFFEFE0210ULL);
        ck("[15] path[2] = slot 2", be_at(p1, 58, 8), 0xAABBCCFFFE001122ULL);
        ck("[15] exactly one frame", (long)collect_resp(700).size(), 0);

        // A BARE GENERATION BUMP. Nothing about the identities changed; the
        // daemon simply re-published. Table 5.22 owes the controller that
        // event, and the payload must be byte-identical.
        dut->asp_gen_i = 2;
        auto p2 = wait_push(2000);
        ck("[15] generation bump pushed", p2.size() > 0, 1);
        ck("[15] cmd GET_AS_PATH", r_cmd(p2), 0x28);
        {
            bool same = (p1.size() == p2.size());
            // compare the whole payload from descriptor_index on; the
            // sequence_id legitimately advances, the bytes must not
            for (size_t i = 38; same && i < p1.size(); i++)
                same = (p1[i] == p2[i]);
            ck("[15] identical payload on the re-publish", same, 1);
        }
        ck("[15] sequence advanced", r_seq(p2) == r_seq(p1) + 1, 1);
        ck("[15] exactly one frame", (long)collect_resp(700).size(), 0);

        // withdrawing the publish is itself an edge, and lands the entity
        // back on the legacy derivation
        dut->asp_count_i = 0;
        auto p3 = wait_push(2000);
        ck("[15] withdraw pushed", p3.size() > 0, 1);
        ck("[15] cmd GET_AS_PATH", r_cmd(p3), 0x28);
        ck("[15] back to the legacy count 1 (foreign GM, no parent)",
           be_at(p3, 41, 1), 1);
        ck("[15] CDL back to 24", r_cdl(p3), 24);
        feed_rx(build_aem_cmd(stim, 37, 0x5E02, {}));
        ck("[15] DEREGISTER A", r_status(collect_resp()), 0);
    }

    printf("\n----------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
