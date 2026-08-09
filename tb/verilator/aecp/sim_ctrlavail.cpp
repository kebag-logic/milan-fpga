/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * gh #59 - Milan v1.2 5.4.5.3 "Detection of departing controllers": the
 * entity monitors every registered controller, asks a silent one whether it
 * is still there with a CONTROLLER_AVAILABLE command (IEEE 1722.1-2021
 * 7.4.4), retries once with the SAME sequence id after 250 ms (9.3.2.6 /
 * 9.3.6), and on a second silence deregisters it and tells THAT CONTROLLER
 * ONLY with a u=1 DEREGISTER_UNSOLICITED_NOTIFICATION.
 *
 * This is the first sim in the tree where the entity SPEAKS FIRST, so the
 * harness is built around a free-running frame catcher with timestamps
 * rather than the usual command/response ping-pong: a deadline has to be
 * MEASURED, and a probe can land in the middle of somebody else's
 * transaction.
 *
 * The timers are parameter-shrunk so a full silent-eviction walk simulates:
 *   CLK_FREQ_HZ_P    100 000  -> 1 KL_aecp_timers millisecond = 100 cycles
 *   MONITOR_MIN_MS_P     100  <- the clause's 30 s floor
 *   MONITOR_RND_MS_P      50  <- ...and its 30 s random span (30..60 s)
 *   CA_ACK_MS_P           20  <- the 250 ms acknowledgement window
 * The LAW is in the RTL; only the DURATIONS move.
 *
 * Cases:
 *   [1] the probe lands on the deadline, every one of its 38 bytes pinned
 *   [2] a reply keeps the slot - including one carrying a NON-ZERO status
 *       ("no matter the value of the status code")
 *   [3] silence -> exactly ONE retry with the SAME sequence id -> exactly
 *       ONE deregistration, unicast to the departed controller only
 *   [3b] the co-registered survivor is untouched, and the re-registering
 *       controller answers from sequence zero
 *   [4] a controller that only ever READS is never probed
 *   [5] a refused registration force-expires the monitors and recovers -
 *       and the controller that ANSWERS is never evicted (5.4.2.21)
 *   [6] two silent controllers serialise: one probe outstanding at a time
 *   [7] consecutive monitor reloads differ and stay inside the range
 *
 * Exit 0 = pass.
 */

#include "VKL_aecp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>

/* --- the shrunk timer contract, mirrored from the Makefile's -G flags --- */
#define MS_CYC       100    /* CLK_FREQ_HZ_P 100 000 -> cycles per ms */
#define MON_MIN_MS   100
#define MON_RND_MS   50
#define ACK_MS       20
/* a reload of N expires on the (N+1)th tick, so the window is
 * [MIN+1, MIN+RND] ms; the slack covers arbitration + the 38-byte emission */
#define DEADLINE_LO  ((long)MON_MIN_MS * MS_CYC)
#define DEADLINE_HI  ((long)(MON_MIN_MS + MON_RND_MS + 3) * MS_CYC)

static VKL_aecp_top* dut;
static long checks = 0, fails = 0;
static long cyc = 0;

static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-58s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-58s = %ld\n", what, got); }
}

static const uint8_t ENT_MAC[6] = {0x02,0x00,0x00,0xff,0xfe,0x01};
static const uint8_t MAC_A[6]   = {0x68,0x05,0xca,0x00,0x00,0xa0};
static const uint8_t MAC_B[6]   = {0x68,0x05,0xca,0x00,0x00,0xb0};
static const uint8_t MAC_C[6]   = {0x68,0x05,0xca,0x00,0x00,0xc0};
static const uint8_t MAC_D[6]   = {0x68,0x05,0xca,0x00,0x00,0xd0};
static const uint8_t MAC_E[6]   = {0x68,0x05,0xca,0x00,0x00,0xe0};
static const uint64_t ENTITY_ID = 0x020000fffe000001ULL;
static const uint64_t CID_A     = 0x680500fffe0000a0ULL;
static const uint64_t CID_B     = 0x680500fffe0000b0ULL;
static const uint64_t CID_C     = 0x680500fffe0000c0ULL;
static const uint64_t CID_D     = 0x680500fffe0000d0ULL;
static const uint64_t CID_E     = 0x680500fffe0000e0ULL;

/* ------------------------------------------------------------------ */
/* frame catcher: every emitted frame is kept with the cycle it ENDED   */
/* on, so a deadline can be measured instead of merely observed.        */
/* ------------------------------------------------------------------ */
struct Frame { std::vector<uint8_t> b; long t; };
static std::vector<Frame> caught;
static std::vector<uint8_t> partial;
static size_t rd = 0;

static void step() {
    dut->eval();
    bool last = false;
    if (dut->m_axis_tvalid && dut->m_axis_tready) {
        for (int l = 0; l < 8; l++)
            if ((dut->m_axis_tkeep >> l) & 1)
                partial.push_back((dut->m_axis_tdata >> (8*l)) & 0xFF);
        last = dut->m_axis_tlast;
    }
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    cyc++;
    if (last) { caught.push_back({partial, cyc}); partial.clear(); }
}
static void pump(long n) { for (long i = 0; i < n; i++) step(); }
static bool have() { return rd < caught.size(); }
static Frame take() { return caught[rd++]; }
static bool wait_frame(long budget) {
    while (!have() && budget-- > 0) step();
    return have();
}
/* run n cycles and report how many frames the wire carried (consuming) */
static long quiet(long n) {
    size_t before = caught.size();
    pump(n);
    long k = (long)(caught.size() - before);
    rd = caught.size();
    return k;
}

static void put_be64(std::vector<uint8_t>& v, uint64_t x) {
    for (int i = 7; i >= 0; i--) v.push_back((x >> (8*i)) & 0xFF);
}
static void put_be16(std::vector<uint8_t>& v, uint16_t x) {
    v.push_back(x >> 8); v.push_back(x & 0xFF);
}

/* an AEM command from a controller to us */
static std::vector<uint8_t> aem_cmd(const uint8_t* smac, uint64_t cid,
                                    uint16_t cmd, uint16_t seq,
                                    const std::vector<uint8_t>& payload) {
    std::vector<uint8_t> f;
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
    while (f.size() < 60) f.push_back(0x00);
    return f;
}

/* the controller's answer to OUR probe: an AEM_RESPONSE whose
 * controller_entity_id is OURS (1722.1-2021 9.3.6's match rule) and whose
 * target_entity_id names the answering controller */
static std::vector<uint8_t> ca_response(const uint8_t* smac, uint64_t cid,
                                        uint16_t seq, int status) {
    std::vector<uint8_t> f;
    for (int i=0;i<6;i++) f.push_back(ENT_MAC[i]);
    for (int i=0;i<6;i++) f.push_back(smac[i]);
    put_be16(f, 0x22F0);
    f.push_back(0xFB);
    f.push_back(0x01);                          // AEM_RESPONSE
    f.push_back(((status & 0x1F) << 3) | 0x00); // status + cdl[10:8]
    f.push_back(12);                            // cdl[7:0]
    put_be64(f, cid);                           // target = the controller
    put_be64(f, ENTITY_ID);                     // controller field = US
    put_be16(f, seq);
    f.push_back(0x00);                          // u=0, command_type[14:8]
    f.push_back(0x03);                          // CONTROLLER_AVAILABLE
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
        step();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
}

static int  r_status(const std::vector<uint8_t>& b){ return b.size()>16 ? (b[16]>>3)&0x1F : -1; }
static int  r_cdl(const std::vector<uint8_t>& b){ return b.size()>17 ? (((b[16]&7)<<8)|b[17]) : -1; }
static int  r_cmd(const std::vector<uint8_t>& b){ return b.size()>37 ? (((b[36]&0x7F)<<8)|b[37]) : -1; }
static int  r_seq(const std::vector<uint8_t>& b){ return b.size()>35 ? ((b[34]<<8)|b[35]) : -1; }
static int  r_mtype(const std::vector<uint8_t>& b){ return b.size()>15 ? (b[15]&0x0F) : -1; }
static int  u_bit(const std::vector<uint8_t>& b){ return b.size()>36 ? (b[36]>>7)&1 : -1; }
static uint64_t be_at(const std::vector<uint8_t>& b, int off, int n) {
    if ((int)b.size() < off + n) return ~0ULL;
    uint64_t v = 0;
    for (int i = 0; i < n; i++) v = (v << 8) | b[off + i];
    return v;
}
static bool to_mac(const Frame& f, const uint8_t* m) {
    return f.b.size() >= 6 && memcmp(f.b.data(), m, 6) == 0;
}
static bool is_probe(const Frame& f) {
    return r_mtype(f.b) == 0 && r_cmd(f.b) == 3 && u_bit(f.b) == 0;
}
static bool is_dereg(const Frame& f) {
    return r_mtype(f.b) == 1 && r_cmd(f.b) == 0x25 && u_bit(f.b) == 1;
}

/* Controller B plays the LIVE controller for most of the walk, so its
 * probes are serviced automatically wherever the case under test is about
 * somebody else. [6] turns this off to let B go silent. */
static bool auto_answer_b = true;
static void service(const Frame& f) {
    if (auto_answer_b && is_probe(f) && to_mac(f, MAC_B))
        feed_rx(ca_response(MAC_B, CID_B, (uint16_t)r_seq(f.b), 0));
}
/* wait for the next SOLICITED response (want=0) or the next u=1 PUSH
 * (want=1), servicing anything else that lands meanwhile. A probe can
 * arrive in the middle of any transaction, so no wait may assume the next
 * frame on the wire is the one it asked for. */
static Frame await(int want, long budget) {
    while (budget-- > 0) {
        if (have()) {
            Frame f = take();
            if (r_mtype(f.b) == 1 && u_bit(f.b) == (want ? 1 : 0) && !is_dereg(f))
                return f;
            service(f);
            continue;
        }
        step();
    }
    Frame e; e.t = cyc; return e;
}
/* run n cycles, counting the frames addressed to `mac` and servicing the
 * rest */
static long run_count_to(const uint8_t* mac, long n) {
    long k = 0;
    for (long i = 0; i < n; i++) {
        step();
        while (have()) {
            Frame f = take();
            if (to_mac(f, mac)) k++; else service(f);
        }
    }
    return k;
}

/* drive one command and return its solicited response */
static Frame xact(const uint8_t* smac, uint64_t cid, uint16_t cmd,
                  uint16_t seq, const std::vector<uint8_t>& pl) {
    feed_rx(aem_cmd(smac, cid, cmd, seq, pl));
    return await(0, 8000);
}
static int reg_ctl(const uint8_t* smac, uint64_t cid, uint16_t seq) {
    return r_status(xact(smac, cid, 36, seq, {}).b);
}
static int dereg_ctl(const uint8_t* smac, uint64_t cid, uint16_t seq) {
    return r_status(xact(smac, cid, 37, seq, {}).b);
}
/* a READ_DESCRIPTOR (ENTITY/0) - the "controller that only ever reads" */
static std::vector<uint8_t> read_cmd(const uint8_t* smac, uint64_t cid, uint16_t seq) {
    std::vector<uint8_t> pl; put_be16(pl, 0); put_be16(pl, 0);
    put_be16(pl, 0); put_be16(pl, 0);
    return aem_cmd(smac, cid, 4, seq, pl);
}

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
    dut->pdelay_ns_i = 0; dut->as_parent_ckid_i = 0;
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
    dut->crf_cnt_locked_i = 0; dut->crf_cnt_unlocked_i = 0;
    dut->crf_cnt_intr_i = 0; dut->crf_cnt_seqerr_i = 0;
    dut->crf_cnt_mreset_i = 0; dut->crf_cnt_tu_i = 0;
    dut->crf_cnt_fmterr_i = 0; dut->crf_cnt_late_i = 0;
    dut->crf_cnt_early_i = 0; dut->crf_cnt_pdu_i = 0;
    for (int w = 0; w < 12; w++) dut->rxdiag_cnt_i[w] = 0;
    for (int w = 0; w < 5; w++)  dut->tkdiag_cnt_i[w] = 0;
    dut->n_aaf_sinks_i = 1;
    dut->talker_active_i = 0; dut->listener_observed_i = 0;
    dut->lstn_bound_v_i = 0; dut->out_streaming_v_i = 0;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|ENT_MAC[i]; dut->station_mac_i = m; }
    for (int i = 0; i < 8; i++) step();
    dut->rst_n = 1;
    /* let the boot-time signature settle: the reset-vs-live comparison
     * raises dirty flags with nobody registered, and they self-clear */
    pump(4000);
    rd = caught.size();

    printf("== gh #59 departing-controller detection - 1 ms = %d cycles ==\n", MS_CYC);
    printf("   monitor %d..%d ms, acknowledgement %d ms\n",
           MON_MIN_MS + 1, MON_MIN_MS + MON_RND_MS, ACK_MS + 1);

    /* --------------------------------------------------------------- */
    printf("\n[1] the probe lands on the deadline, bytes pinned\n");
    long probe1_seq = 0;
    {
        Frame r = xact(MAC_A, CID_A, 36, 0x1001, {});
        ck("[1] REGISTER A SUCCESS", r_status(r.b), 0);
        long t_reg = r.t;
        ck("[1] silent inside the monitor floor", quiet(DEADLINE_LO - 300), 0);
        ck("[1] a frame arrives before the ceiling",
           wait_frame(DEADLINE_HI - DEADLINE_LO + 900) ? 1 : 0, 1);
        Frame p = take();
        long dt = p.t - t_reg;
        printf("       (measured %ld cycles = %ld ms)\n", dt, dt / MS_CYC);
        ck("[1] deadline at or past the scaled 30 s floor", dt >= DEADLINE_LO, 1);
        ck("[1] deadline within the scaled 60 s ceiling", dt <= DEADLINE_HI, 1);

        /* the whole 38-byte AECPDU, field by field */
        ck("[1] frame is 38 bytes (12 + zero-length payload)", (long)p.b.size(), 38);
        ck("[1] dst MAC = controller A", to_mac(p, MAC_A) ? 1 : 0, 1);
        ck("[1] src MAC = our station",
           (p.b.size() >= 12 && memcmp(p.b.data()+6, ENT_MAC, 6) == 0) ? 1 : 0, 1);
        ck("[1] ethertype 0x22F0", (long)be_at(p.b, 12, 2), 0x22F0);
        ck("[1] subtype 0xFB (AECP)", (long)be_at(p.b, 14, 1), 0xFB);
        ck("[1] byte 15 = 0x00: sv 0, version 0, AEM_COMMAND", (long)be_at(p.b, 15, 1), 0x00);
        ck("[1] byte 16 = 0x00: status 0, cdl[10:8] 0", (long)be_at(p.b, 16, 1), 0x00);
        ck("[1] byte 17 = 0x0C: control_data_length 12", (long)be_at(p.b, 17, 1), 0x0C);
        ck("[1] target_entity_id = THE CONTROLLER (7.4.4)",
           be_at(p.b, 18, 8) == CID_A, 1);
        ck("[1] controller_entity_id = OURS", be_at(p.b, 26, 8) == ENTITY_ID, 1);
        ck("[1] byte 36 = 0x00: u bit CLEAR on a command", (long)be_at(p.b, 36, 1), 0x00);
        ck("[1] byte 37 = 0x03: CONTROLLER_AVAILABLE", (long)be_at(p.b, 37, 1), 0x03);
        probe1_seq = r_seq(p.b);
        ck("[1] the initiator sequence space starts at 0", probe1_seq, 0);
        ck("[1] diag: 1 probe sent", (long)(dut->ca_diag_o & 0xFFF), 1);
        ck("[1] diag: 0 evictions", (long)((dut->ca_diag_o >> 24) & 0xFF), 0);
    }

    /* --------------------------------------------------------------- */
    printf("\n[2] an answered probe keeps the slot - the status is IRRELEVANT\n");
    printf("[7] ...and consecutive reloads differ and stay in range\n");
    {
        feed_rx(ca_response(MAC_A, CID_A, (uint16_t)probe1_seq, 0));
        long t_ans = cyc;
        ck("[2] no retry follows an answered probe",
           quiet((long)(ACK_MS + 6) * MS_CYC), 0);
        ck("[2] diag: 1 reply seen", (long)((dut->ca_diag_o >> 12) & 0xFFF), 1);

        long iv[4];
        /* NOT_AUTHENTICATED and ENTITY_LOCKED replies prove liveness too */
        static const int st[4] = {0, 5, 0, 3};
        for (int k = 0; k < 4; k++) {
            ck("[2] the next probe arrives", wait_frame(DEADLINE_HI + 3000) ? 1 : 0, 1);
            Frame p = take();
            ck("[2] it is a CONTROLLER_AVAILABLE command", is_probe(p) ? 1 : 0, 1);
            ck("[2] addressed to controller A", to_mac(p, MAC_A) ? 1 : 0, 1);
            iv[k] = p.t - t_ans;
            feed_rx(ca_response(MAC_A, CID_A, (uint16_t)r_seq(p.b), st[k]));
            t_ans = cyc;
        }
        pump(200);   /* let the last witness pulse reach the tallies */
        ck("[2] a NON-ZERO status still proves liveness (no eviction)",
           (long)((dut->ca_diag_o >> 24) & 0xFF), 0);
        ck("[2] diag: 5 probes", (long)(dut->ca_diag_o & 0xFFF), 5);
        ck("[2] diag: 5 replies", (long)((dut->ca_diag_o >> 12) & 0xFFF), 5);

        int in_range = 0, differ = 0;
        for (int k = 0; k < 4; k++) {
            printf("       reload %d -> %ld cycles (%ld ms)\n", k, iv[k], iv[k] / MS_CYC);
            if (iv[k] >= DEADLINE_LO && iv[k] <= DEADLINE_HI) in_range++;
            if (k && iv[k] != iv[k-1]) differ++;
        }
        ck("[7] every reload inside the clause range", in_range, 4);
        ck("[7] consecutive reloads differ", differ, 3);
    }

    /* --------------------------------------------------------------- */
    printf("\n[3] silence -> ONE retry (same sequence id) -> ONE deregistration\n");
    printf("[4] ...while the READ-ONLY controller B is never probed\n");
    {
        ck("[3] REGISTER B SUCCESS", reg_ctl(MAC_B, CID_B, 0x2001), 0);
        /* A goes silent; B stays alive with READ_DESCRIPTORs well inside
         * the monitor floor - a read IS a valid AECP command (5.4.5.3) */
        std::vector<Frame> a_frames;
        long b_probes = 0, b_resp = 0;
        int reads = 0;
        long guard = 0;
        while ((long)a_frames.size() < 3 && guard < 12L * DEADLINE_HI) {
            for (long i = 0; i < 60L * MS_CYC; i++) { step(); guard++; }
            feed_rx(read_cmd(MAC_B, CID_B, (uint16_t)(0x2100 + reads)));
            reads++;
            while (have()) {
                Frame f = take();
                if (to_mac(f, MAC_A))      a_frames.push_back(f);
                else if (is_probe(f))      b_probes++;
                else                       b_resp++;
            }
        }
        /* the walk ends the instant the deregistration lands, which can be
         * mid-flight for B's last read response - drain it */
        for (long i = 0; i < 2000; i++) {
            step();
            while (have()) {
                Frame f = take();
                if (to_mac(f, MAC_A))      a_frames.push_back(f);
                else if (is_probe(f))      b_probes++;
                else                       b_resp++;
            }
        }
        ck("[3] exactly 3 frames reached the departed controller",
           (long)a_frames.size(), 3);
        ck("[4] B was read-only-but-heard, so B was NEVER probed", b_probes, 0);
        ck("[4] ...and every one of its reads was answered", b_resp, (long)reads);
        if (a_frames.size() >= 3) {
            Frame p1 = a_frames[0], p2 = a_frames[1], dg = a_frames[2];
            ck("[3] frame 1 = the CONTROLLER_AVAILABLE probe", is_probe(p1) ? 1 : 0, 1);
            ck("[3] frame 2 = the retry", is_probe(p2) ? 1 : 0, 1);
            ck("[3] the retry re-sends the SAME sequence id (9.3.6)",
               (r_seq(p2.b) == r_seq(p1.b)) ? 1 : 0, 1);
            ck("[3] ...and the probe used a fresh initiator sequence",
               (r_seq(p1.b) == (int)probe1_seq + 5) ? 1 : 0, 1);
            long gap = p2.t - p1.t;
            printf("       (retry gap %ld cycles = %ld ms)\n", gap, gap / MS_CYC);
            ck("[3] the retry is one acknowledgement window later",
               (gap >= (long)ACK_MS * MS_CYC &&
                gap <= (long)(ACK_MS + 4) * MS_CYC) ? 1 : 0, 1);
            ck("[3] frame 3 = DEREGISTER_UNSOLICITED_NOTIFICATION",
               is_dereg(dg) ? 1 : 0, 1);
            ck("[3] it is a RESPONSE (message_type 1)", r_mtype(dg.b), 1);
            ck("[3] u bit SET on the notification", u_bit(dg.b), 1);
            ck("[3] status SUCCESS", r_status(dg.b), 0);
            ck("[3] control_data_length 12 (no payload)", r_cdl(dg.b), 12);
            ck("[3] target_entity_id = OURS (it is OUR response)",
               be_at(dg.b, 18, 8) == ENTITY_ID, 1);
            ck("[3] controller_entity_id = the departed A",
               be_at(dg.b, 26, 8) == CID_A, 1);
            ck("[3] unicast to A's MAC and to nobody else",
               to_mac(dg, MAC_A) ? 1 : 0, 1);
            long dgap = dg.t - p2.t;
            ck("[3] the deregistration is one window after the retry",
               (dgap >= (long)ACK_MS * MS_CYC &&
                dgap <= (long)(ACK_MS + 4) * MS_CYC) ? 1 : 0, 1);
        } else {
            for (int k = 0; k < 15; k++) ck("[3] (skipped: no walk)", 0, 1);
        }
        ck("[3] diag: exactly 1 eviction", (long)((dut->ca_diag_o >> 24) & 0xFF), 1);
    }

    /* --------------------------------------------------------------- */
    printf("\n[3b] the survivor keeps its registration; A returns at sequence 0\n");
    {
        dut->talker_active_i = 1;          /* one push per registered slot */
        Frame f1 = await(1, 8000);
        ck("[3b] a push while only B is registered", (long)f1.b.size() > 0, 1);
        ck("[3b] ...and it went to B", to_mac(f1, MAC_B) ? 1 : 0, 1);
        ck("[3b] nothing is ever sent to the departed A",
           run_count_to(MAC_A, 6000), 0);
        ck("[3b] REGISTER A again", reg_ctl(MAC_A, CID_A, 0x3001), 0);
        dut->talker_active_i = 0;          /* the next edge */
        Frame g1 = await(1, 8000);
        ck("[3b] push 1 after the re-registration", (long)g1.b.size() > 0, 1);
        Frame g2 = await(1, 8000);
        ck("[3b] push 2 after the re-registration", (long)g2.b.size() > 0, 1);
        const Frame& fa = to_mac(g1, MAC_A) ? g1 : g2;
        const Frame& fb = to_mac(g1, MAC_A) ? g2 : g1;
        ck("[3b] A's push carries sequence 0 - a FRESH slot", r_seq(fa.b), 0);
        ck("[3b] B's push carries its own advanced sequence",
           (r_seq(fb.b) > 0) ? 1 : 0, 1);
        /* clean slate for the next case: an explicit DEREGISTER stops the
         * monitor, so the long silence below proves total quiet */
        ck("[3b] DEREGISTER A", dereg_ctl(MAC_A, CID_A, 0x3002), 0);
        ck("[3b] DEREGISTER B", dereg_ctl(MAC_B, CID_B, 0x3003), 0);
        ck("[3b] an empty table never probes anybody",
           quiet(3 * DEADLINE_HI), 0);
    }

    /* --------------------------------------------------------------- */
    printf("\n[5] a refused registration force-expires the monitors and recovers\n");
    {
        ck("[5] REGISTER A", reg_ctl(MAC_A, CID_A, 0x4001), 0);
        ck("[5] REGISTER B", reg_ctl(MAC_B, CID_B, 0x4002), 0);
        ck("[5] REGISTER C", reg_ctl(MAC_C, CID_C, 0x4003), 0);
        ck("[5] REGISTER D", reg_ctl(MAC_D, CID_D, 0x4004), 0);
        ck("[5] the table is full: E is refused with NO_RESOURCES",
           reg_ctl(MAC_E, CID_E, 0x4005), 8);
        /* the sweep: A, C and D stay silent; B answers every probe */
        long deregs = 0, b_probe = 0, b_dereg = 0, guard = 0;
        while (guard < 16L * DEADLINE_HI && deregs < 3) {
            step(); guard++;
            while (have()) {
                Frame f = take();
                if (is_probe(f)) {
                    if (to_mac(f, MAC_B)) {
                        b_probe++;
                        feed_rx(ca_response(MAC_B, CID_B, (uint16_t)r_seq(f.b), 0));
                    }
                } else if (is_dereg(f)) {
                    deregs++;
                    if (to_mac(f, MAC_B)) b_dereg++;
                }
            }
        }
        ck("[5] the sweep freed exactly the 3 silent slots", deregs, 3);
        ck("[5] B was probed by the sweep", (b_probe > 0) ? 1 : 0, 1);
        ck("[5] B ANSWERED, so B was never deregistered (5.4.2.21)", b_dereg, 0);
        ck("[5] the refused registration now succeeds",
           reg_ctl(MAC_E, CID_E, 0x4006), 0);
        ck("[5] diag: 4 evictions in total", (long)((dut->ca_diag_o >> 24) & 0xFF), 4);
    }

    /* --------------------------------------------------------------- */
    printf("\n[6] two silent controllers serialise: one probe outstanding\n");
    {
        /* registered now: B (which stops answering) and E (never answered) */
        auto_answer_b = false;
        std::vector<Frame> seq_frames;
        long guard = 0, deregs = 0, overlap = 0;
        const uint8_t* owner = nullptr;
        while (guard < 20L * DEADLINE_HI && deregs < 2) {
            step(); guard++;
            while (have()) {
                Frame f = take();
                if (!is_probe(f) && !is_dereg(f)) continue;
                const uint8_t* who = to_mac(f, MAC_B) ? MAC_B
                                   : to_mac(f, MAC_E) ? MAC_E : nullptr;
                if (!who) continue;
                if (owner && who != owner &&
                    !(seq_frames.size() && is_dereg(seq_frames.back())))
                    overlap++;      /* a transaction was interrupted */
                owner = who;
                seq_frames.push_back(f);
                if (is_dereg(f)) deregs++;
            }
        }
        ck("[6] both silent controllers were shed", deregs, 2);
        ck("[6] six frames: probe + retry + deregistration, twice",
           (long)seq_frames.size(), 6);
        ck("[6] the two transactions never interleave", overlap, 0);
        if (seq_frames.size() == 6) {
            ck("[6] 1: probe", is_probe(seq_frames[0]) ? 1 : 0, 1);
            ck("[6] 2: retry, same sequence id",
               (is_probe(seq_frames[1]) &&
                r_seq(seq_frames[1].b) == r_seq(seq_frames[0].b)) ? 1 : 0, 1);
            ck("[6] 3: deregistration", is_dereg(seq_frames[2]) ? 1 : 0, 1);
            ck("[6] 4: probe for the OTHER controller",
               (is_probe(seq_frames[3]) &&
                memcmp(seq_frames[3].b.data(), seq_frames[0].b.data(), 6) != 0) ? 1 : 0, 1);
            ck("[6] 5: its retry, same sequence id",
               (is_probe(seq_frames[4]) &&
                r_seq(seq_frames[4].b) == r_seq(seq_frames[3].b)) ? 1 : 0, 1);
            ck("[6] the two probes used DIFFERENT initiator sequences",
               (r_seq(seq_frames[3].b) != r_seq(seq_frames[0].b)) ? 1 : 0, 1);
            ck("[6] 6: its deregistration", is_dereg(seq_frames[5]) ? 1 : 0, 1);
        } else {
            for (int k = 0; k < 7; k++) ck("[6] (skipped: wrong frame count)", 0, 1);
        }
        ck("[6] diag: 6 evictions in total", (long)((dut->ca_diag_o >> 24) & 0xFF), 6);
        ck("[6] the table is empty and the wire is silent",
           quiet(3 * DEADLINE_HI), 0);
        ck("[6] a fresh registration is accepted after the shed-out",
           reg_ctl(MAC_A, CID_A, 0x6001), 0);
        ck("[6] DEREGISTER stops that monitor for good",
           dereg_ctl(MAC_A, CID_A, 0x6002), 0);
        ck("[6] no probe ever follows an explicit deregistration",
           quiet(3 * DEADLINE_HI), 0);
    }

    printf("\n----------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
