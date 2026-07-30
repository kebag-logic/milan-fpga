/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * ADP ADVERTISE STATE MACHINE — TIMING CONTRACT (adp_advertiser.sv).
 *
 * tb/verilator/adp locks the ADPDU BYTES. This suite locks WHEN the bytes come
 * out, which is where the 2026-07-29/30 "the advertiser goes dormant on
 * silicon" episode actually lived. The wire capture refuted dormancy (ADPDUs at
 * exactly 10.000 s spacing, available_index 2681->2683 = 7.4 h unbroken, ADP
 * DIAG 0 = no departs and no re-arms, TXARB_DIAG 0xA7000000 = no arbiter lock
 * anywhere in the 8-mux TX chain), and what was left was a period twice as slow
 * as the clause:
 *
 *   Milan v1.2 Table 5.50 : "TMR_ADVERTISE - ADP advertise timer expired. This
 *                            is a timer with a fixed value of 5 seconds",
 *                            restarted on every send by 5.6.3.5.9, under the
 *                            5.6.3 "The PAAD-AE shall implement an independent
 *                            instance of the Advertise state machine".
 *   IEEE 1722.1-2021 Fig 6-2: "reannounceTimerTimeout = currentTime + MAX(1,
 *                            entityInfo.valid_time / 2)" (NOTE: valid_time is
 *                            in units of 2 s, the MAX returns SECONDS).
 *
 * The engine takes the faster of the two: period = MIN(5, MAX(1, vt/2)) s.
 * A 5 s passive discovery pass against a 10 s advertiser hits 1/0/1 - which is
 * the whole "dormancy". Every case below states the clause it locks.
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vadp_advertiser.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vadp_advertiser* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-52s got=%llu exp=%llu\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    }
}

static const uint64_t ENTITY_ID   = 0x0200000000020000ULL;
static const uint64_t MODEL_ID    = 0x001BC5FFFE000101ULL;
static const uint64_t STATION_MAC = 0x020000000002ULL;
static uint64_t GPTP_GM     = 0x0011223344556677ULL;
static uint8_t  GPTP_DOMAIN = 0;
static uint8_t  VALID_TIME  = 10;          // the bench value

//! the clause rule under test, computed independently of the RTL
static int adv_period(int vt) {
    int half = vt / 2;                     // 1722.1 Fig 6-2: valid_time / 2
    if (half < 1) half = 1;                //   MAX(1, ..)
    if (half > 5) half = 5;                // Milan Table 5.50: fixed 5 s
    return half;
}

static void apply_fields() {
    dut->station_mac_i                 = STATION_MAC;
    dut->valid_time_i                  = VALID_TIME;
    dut->entity_id_i                   = ENTITY_ID;
    dut->entity_model_id_i             = MODEL_ID;
    dut->entity_capabilities_i         = 0x0000C588u;
    dut->talker_stream_sources_i       = 4;
    dut->talker_capabilities_i         = 0x4801;
    dut->listener_stream_sinks_i       = 5;
    dut->listener_capabilities_i       = 0x4801;
    dut->controller_capabilities_i     = 0;
    dut->gptp_grandmaster_id_i         = GPTP_GM;
    dut->gptp_domain_number_i          = GPTP_DOMAIN;
    dut->current_configuration_index_i = 0;
    dut->identify_control_index_i      = 0;
    dut->interface_index_i             = 0;
    dut->association_id_i              = 0;
}

static void clear_events() {
    dut->link_up_i = dut->link_down_i = dut->shutdown_i = 0;
    dut->gm_change_i = dut->info_changed_i = dut->rcv_discover_i = dut->tick_i = 0;
}

static void lo() { dut->clk_i = 0; dut->eval(); }
static void hi() { dut->clk_i = 1; dut->eval(); }
static void step() { lo(); hi(); }
static void pulse(CData& s) { s = 1; step(); s = 0; }
static void tick() { pulse(dut->tick_i); }

//! Capture one whole frame if it STARTS within `maxc` cycles; else return {}.
static std::vector<uint8_t> capture(int maxc = 64) {
    std::vector<uint8_t> b;
    bool started = false;
    for (int c = 0; c < maxc || started; c++) {
        dut->m_axis_tready = 1;
        lo();
        if (dut->m_axis_tvalid) {
            started = true;
            for (int l = 0; l < 8; l++)
                if ((dut->m_axis_tkeep >> l) & 1)
                    b.push_back((dut->m_axis_tdata >> (8 * l)) & 0xFF);
            bool last = dut->m_axis_tlast;
            hi();
            if (last) return b;
        } else {
            hi();
        }
    }
    return b;
}

//! true if no frame starts in `cycles`
static bool silent_for(int cycles) {
    for (int c = 0; c < cycles; c++) { lo(); if (dut->m_axis_tvalid) { hi(); return false; } hi(); }
    return true;
}

//! Advance ticks one at a time (draining nothing) until a frame appears;
//! returns the number of ticks it took, or -1 if `limit` ticks produced none.
//! Each tick is followed by a short settle window because the pending request
//! reaches the serialiser on the next cycle.
static int ticks_to_frame(std::vector<uint8_t>& f, int limit = 40, int settle = 24) {
    for (int t = 1; t <= limit; t++) {
        tick();
        f = capture(settle);
        if (!f.empty()) return t;
    }
    return -1;
}

static uint64_t be(const std::vector<uint8_t>& b, int off, int n) {
    uint64_t v = 0; for (int i = 0; i < n; i++) v = (v << 8) | b[off + i]; return v;
}
static int  msg_of(const std::vector<uint8_t>& b) { return b.size() >= 16 ? (b[15] & 0x0F) : -1; }
static uint32_t idx_of(const std::vector<uint8_t>& b) { return b.size() >= 54 ? (uint32_t)be(b, 50, 4) : 0; }

//! reset into a known state: enabled, link up, nothing pending
static void boot(bool enable, bool link_level) {
    dut->rst_n = 0; dut->enable_i = 0; dut->m_axis_tready = 1;
    clear_events(); apply_fields(); dut->link_level_i = link_level;
    for (int i = 0; i < 4; i++) step();
    dut->rst_n = 1;
    dut->enable_i = enable ? 1 : 0;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vadp_advertiser;

    printf("== adp_advertiser: ADVERTISE STATE MACHINE TIMING ==\n");

    // ================================================================== //
    // A1) STARTUP WITH LINK UP IS A LEVEL, NOT AN EVENT.                  //
    //     Milan v1.2 5.6.3.5.2 "Startup of the PAAD-AE with link status    //
    //     up": start TMR_DELAY, go to DELAY (-> send). No pulse exists in  //
    //     that clause and no timer tick is required. This is the cold-boot //
    //     half of the bench complaint ("the advertiser arms before link-up //
    //     on every boot and stays dormant until toggled"): with a LEVEL    //
    //     arm there is no pulse to swallow and no toggle to need.          //
    //     BITES the pre-fix RTL: it could only arm on link_up_i or after   //
    //     REARM_TICKS_C ticks of the dormancy watchdog, so with neither a  //
    //     pulse nor a tick it stayed silent forever.                       //
    // ================================================================== //
    printf("\n-- [A1] cold boot, link already up: advertise with NO pulse and NO tick\n");
    {
        boot(/*enable=*/true, /*link_level=*/true);
        auto f = capture(64);
        ck("A1 ADPDU emitted from the level alone", f.size(), 82);
        ck("A1 message_type AVAILABLE", msg_of(f), 0);
        ck("A1 available_index == 1", idx_of(f), 1);
        ck("A1 advertised valid_time field untouched",
           f.size() >= 17 ? (f[16] >> 3) : 0xFF, VALID_TIME);
        ck("A1 no depart invented", dut->depart_cnt_o, 0);
        //! the STARTUP arm is a LEVEL arm, so it is honestly counted (this is
        //! the documented reading change: rearm_cnt == 1 on a clean boot)
        ck("A1 rearm_cnt witnesses the STARTUP arm", dut->rearm_cnt_o, 1);
    }

    // ================================================================== //
    // A2) THE RE-ANNOUNCE PERIOD IS THE CLAUSE PERIOD, for every           //
    //     valid_time. Milan Table 5.50 (fixed 5 s) + 1722.1 Fig 6-2        //
    //     (MAX(1, valid_time/2) s) -> MIN(5, MAX(1, vt/2)).                //
    //     BITES the pre-fix RTL at every value except vt <= 3: it used     //
    //     valid_time itself (vt 31 -> 31 s, vt 10 -> 10.000 s as measured  //
    //     on the wire, vt 5 -> 5 s where 1722.1 asks 2 s).                 //
    // ================================================================== //
    printf("\n-- [A2] re-announce period == MIN(5, MAX(1, valid_time/2)) s\n");
    {
        const int vts[] = { 31, 10, 5, 4, 2, 1 };
        for (int v : vts) {
            VALID_TIME = (uint8_t)v; apply_fields();
            step();
            (void)capture(64);                    // drain any frame in flight
            std::vector<uint8_t> f;
            int t1 = ticks_to_frame(f, 40);
            char nm[96];
            snprintf(nm, sizeof nm, "A2 vt=%2d: first period == %d tick(s)", v, adv_period(v));
            ck(nm, (uint64_t)t1, (uint64_t)adv_period(v));
            snprintf(nm, sizeof nm, "A2 vt=%2d: periodic frame is a full AVAILABLE", v);
            ck(nm, (f.size() == 82 && msg_of(f) == 0) ? 1 : 0, 1);
            // the period must be STABLE, not just right once
            int t2 = ticks_to_frame(f, 40);
            snprintf(nm, sizeof nm, "A2 vt=%2d: period repeats identically", v);
            ck(nm, (uint64_t)t2, (uint64_t)adv_period(v));
            snprintf(nm, sizeof nm, "A2 vt=%2d: field still advertises valid_time", v);
            ck(nm, f.size() >= 17 ? (f[16] >> 3) : 0xFF, (uint64_t)v);
        }
        VALID_TIME = 10; apply_fields(); step();
    }

    // ================================================================== //
    // A3) LONG RUN — the minutes-scale question the bench asked, answered  //
    //     in simulation. ARITHMETIC against the real widths and reloads:   //
    //       valid_time 10 -> period 5 ticks; tick_i is 1 s in the          //
    //         integration (ADP_TICK_DIV = MILAN_CLK_FREQ_HZ), so 720 ticks //
    //         = 12 MINUTES of silicon wall time = 144 ADPDUs. The bench    //
    //         symptom appeared "minutes later", so the run outlives it.    //
    //       adv_tick_cnt_r is 5 bits and reloads at period-1 = 4: 144 laps //
    //         with the count never exceeding 4 (the old valid_time reload   //
    //         ran to 30 and made the 5-bit wrap a live question).          //
    //       depart_cnt_o / rearm_cnt_o are 8 bits and must NOT move once   //
    //         at all: 144 frames of proof that nothing departs or re-arms. //
    //       available_index_o is 32 bits: +1 per ADPDU (6.2.2.15), never   //
    //         reset, never repeated - 144 strictly increasing values.      //
    //     BITES the pre-fix RTL: at a 10-tick period the same 720 ticks    //
    //     yield 72 frames, so the count, the index and the spacing all     //
    //     disagree.                                                       //
    // ================================================================== //
    printf("\n-- [A4] long run: 720 ticks (= 12 min of silicon) at valid_time 10\n");
    {
        const int TICKS = 720, PER = adv_period(10);
        uint32_t idx = dut->available_index_o, frames = 0;
        bool idx_ok = true, shape_ok = true, spacing_ok = true;
        uint8_t d0 = dut->depart_cnt_o, r0 = dut->rearm_cnt_o;
        int since = 0;
        for (int t = 0; t < TICKS; t++) {
            tick();
            since++;
            auto f = capture(24);
            if (!f.empty()) {
                frames++;
                if (f.size() != 82 || msg_of(f) != 0) shape_ok = false;
                if (idx_of(f) != ++idx) idx_ok = false;
                if (since != PER) spacing_ok = false;
                since = 0;
            }
        }
        printf("   long run: %u frames over %d ticks, last index %u\n", frames, TICKS, idx);
        ck("A4 ADPDUs kept coming for the whole run", frames, (uint32_t)(TICKS / PER));
        ck("A4 every frame a well-formed AVAILABLE", shape_ok ? 1 : 0, 1);
        ck("A4 available_index +1 per ADPDU, never reset", idx_ok ? 1 : 0, 1);
        ck("A4 spacing was the clause period every single time", spacing_ok ? 1 : 0, 1);
        ck("A4 no departs over 12 min", dut->depart_cnt_o, d0);
        ck("A4 no re-arms needed over 12 min", dut->rearm_cnt_o, r0);
    }

    // ================================================================== //
    // A5) GM_CHANGE — Milan Table 5.50 "GM_CHANGE - The ID of the current  //
    //     Grandmaster has changed" -> 5.6.3.5.7 (TMR_DELAY -> advertise);  //
    //     1722.1 Fig 6-5 UPDATE GM on "currentGrandmasterID !=             //
    //     advertisedGrandmasterID". The advertised GM is the field a Milan  //
    //     listener tests in 5.6.4.5.2 step 2b before keeping a talker      //
    //     discovered, so publishing a stale one is not cosmetic.           //
    //     BITES the pre-fix RTL: the event only existed as the gm_change_i //
    //     PORT, which milan_datapath ties to 1'b0 - a GM election reached   //
    //     the wire only at the next periodic re-announce.                  //
    // ================================================================== //
    printf("\n-- [A5] GM_CHANGE advertises itself, with no pulse and no software poke\n");
    {
        (void)capture(64);
        GPTP_GM = 0xFEDCBA9876543210ULL; GPTP_DOMAIN = 3;
        apply_fields();
        auto f = capture(64);                       // via TMR_DELAY, no tick
        ck("A5 GM change alone produced an ADPDU", f.size(), 82);
        ck("A5 it carries the NEW grandmaster id", f.size() >= 62 ? be(f, 54, 8) : 0, GPTP_GM);
        ck("A5 it carries the NEW domain number", f.size() >= 63 ? f[62] : 0xFF, GPTP_DOMAIN);
        ck("A5 message_type AVAILABLE", msg_of(f), 0);
        //! the advertised record is updated by the send, so the level must not
        //! re-fire: a rewrite of the SAME value is not an event (this is what
        //! keeps a polling gptp2csr.sh from turning into an ADP storm)
        apply_fields();
        ck("A5 no storm: the same GM value re-written is not an event",
           silent_for(64) ? 1 : 0, 1);
        //! and a domain-only change is an event too
        GPTP_DOMAIN = 4; apply_fields();
        auto f2 = capture(64);
        ck("A5 a domain-only change is also GM_CHANGE", f2.size(), 82);
        ck("A5 domain-only change carries the new domain",
           f2.size() >= 63 ? f2[62] : 0xFF, GPTP_DOMAIN);
    }

    // ================================================================== //
    // A6) LINK BOUNCE — Milan 5.6.3.5.6 (WAITING/LINK_DOWN -> DOWN) and    //
    //     5.6.3.5.3 (DOWN/LINK_UP -> DELAY -> advertise). Recovery must    //
    //     need no CSR write and no pulse: the LEVEL is enough, and a       //
    //     link-down depart must NOT arm the post-shutdown quiet hold (the  //
    //     clause re-advertises as soon as the link is back).               //
    //     BITES the pre-fix RTL on the level-only leg (no link_up_i pulse  //
    //     -> silence until the 2-tick watchdog, if link_level even held).  //
    // ================================================================== //
    printf("\n-- [A6] link bounce: DEPARTING on down, self-advertise on up (level only)\n");
    {
        (void)capture(64); (void)silent_for(64);      // quiesce before the bounce
        uint8_t d0 = dut->depart_cnt_o;
        dut->link_level_i = 0;
        pulse(dut->link_down_i);
        auto fd = capture(64);
        ck("A6 link down emits ENTITY_DEPARTING", msg_of(fd), 1);
        ck("A6 depart witnessed once", dut->depart_cnt_o, (uint64_t)(d0 + 1));
        ck("A6 depart_src == link_down", dut->depart_src_o, 1);
        ck("A6 silent while the link is down (ticks do nothing)",
           (tick(), tick(), tick(), silent_for(64)) ? 1 : 0, 1);
        dut->link_level_i = 1;                      // LEVEL only: no pulse
        auto fu = capture(64);
        ck("A6 link up re-advertises with no pulse and no CSR write", fu.size(), 82);
        ck("A6 recovery message_type AVAILABLE", msg_of(fu), 0);
        ck("A6 no extra depart on the way back", dut->depart_cnt_o, (uint64_t)(d0 + 1));
        // and the periodic contract resumes at the clause period
        std::vector<uint8_t> fp;
        ck("A6 periodic resumes at the clause period",
           (uint64_t)ticks_to_frame(fp, 40), (uint64_t)adv_period(VALID_TIME));
    }

    // ================================================================== //
    // A7) THE SILENCE LEVERS ARE STILL HONEST. Milan Table 5.49 has one    //
    //     silent state (DOWN, "The link is down") and enable_i = 0 is this //
    //     project's ADP_CTRL[0]; a commanded SHUTDOWN (5.6.3.5.8) sends    //
    //     ENTITY_DEPARTING and is then held quiet for REARM_TICKS_C ticks  //
    //     before the level re-arms - the established 2026-07-13 behaviour, //
    //     unchanged, so a controller does not see AVAILABLE contradict the //
    //     DEPARTING it just took.                                         //
    // ================================================================== //
    printf("\n-- [A7] enable=0 and commanded SHUTDOWN keep their meaning\n");
    {
        (void)capture(64); (void)silent_for(64);      // quiesce
        dut->enable_i = 0;
        ck("A7 enable=0 is silence (even with the link up)",
           (tick(), tick(), tick(), silent_for(64)) ? 1 : 0, 1);
        dut->enable_i = 1;
        auto fe = capture(64);
        ck("A7 re-enable arms from the level", fe.size(), 82);
        (void)capture(8);
        uint8_t d0 = dut->depart_cnt_o;
        pulse(dut->shutdown_i);
        auto fs = capture(64);
        ck("A7 SHUTDOWN emits ENTITY_DEPARTING", msg_of(fs), 1);
        ck("A7 depart_src == shutdown", dut->depart_src_o, 2);
        ck("A7 depart counted", dut->depart_cnt_o, (uint64_t)(d0 + 1));
        ck("A7 quiet hold: no AVAILABLE within the first hold tick",
           (tick(), silent_for(32)) ? 1 : 0, 1);
        tick();                                     // hold expires
        auto fr = capture(64);
        ck("A7 then the level re-arms it", fr.size(), 82);
        ck("A7 re-arm message_type AVAILABLE", msg_of(fr), 0);
    }

    // ================================================================== //
    // A8) DISCOVER STILL WORKS AFTER ALL OF THE ABOVE, and is still        //
    //     DELAYED (Milan 5.6.3.5.4 "Start the TMR_DELAY timer (random      //
    //     value between 0 and 4 seconds)"), never instant.                //
    // ================================================================== //
    printf("\n-- [A8] discover response is still delayed, coalesced and index-coherent\n");
    {
        (void)capture(64);
        uint32_t i0 = dut->available_index_o;
        pulse(dut->rcv_discover_i);
        bool instant = false;
        for (int c = 0; c < 3; c++) { lo(); if (dut->m_axis_tvalid) instant = true; hi(); }
        ck("A8 no INSTANT answer (TMR_DELAY exists)", instant ? 1 : 0, 0);
        auto f = capture(64);
        ck("A8 the delayed response arrives", f.size(), 82);
        ck("A8 response bumps available_index by exactly 1", idx_of(f), i0 + 1);
        for (int i = 0; i < 8; i++) pulse(dut->rcv_discover_i);
        auto fb = capture(64);
        ck("A8 a burst coalesces into one response", fb.size(), 82);
        ck("A8 no second response follows the coalesced one",
           silent_for(64) ? 1 : 0, 1);
    }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
