/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * adp_advertiser.sv — ENTITY_DISCOVER response DELAY conformance harness.
 *
 * IEEE Std 1722.1-2021 6.2.4.2.2 randomDeviceDelay(): "The randomDeviceDelay
 * function returns the number of milliseconds that the device should wait
 * between the firing of the re-announce timer or being requested to send an
 * ENTITY_ADVERTISE message and sending the message. The randomDeviceDelay
 * function generates a random delay with a uniform distribution across the
 * range of zero (0) to 1/5 of the valid time of the ATDECC Entity in
 * milliseconds (see 6.2.2.5)."
 *
 * 6.2.2.5 makes valid_time a field "in units of 2 s", so the VALID TIME is
 * 2*valid_time seconds and the bound is 0.4*valid_time seconds. The engine
 * instantiates DISC_DLY_BASE = MILAN_CLK_FREQ_HZ/5 = 0.2 s, so in cycles:
 *
 *     bound(valid_time) = 2 * valid_time * DISC_DLY_BASE
 *
 * THE BOUND SCALES WITH valid_time AND THE OLD ENVELOPE DID NOT. This harness
 * runs the module with a REALISTIC BASE:MASK ratio (1000 : 4095 = 4.1x; the
 * shipped builds sit between 3.36x @100 MHz and 6.71x @50 MHz) and measures
 * real draws, so it BITES the pre-2026-07-30 fixed envelope at valid_time 1
 * and 2 while passing it at valid_time >= 3 - which is exactly where the old
 * code was and was not conformant. The main harness (sim_main.cpp) keeps its
 * own tiny delay parameters for turnaround; the numbers only mean something
 * about the clause here.
 *
 * Exit 0 = pass, non-zero = fail.
 */

#include "Vadp_advertiser.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

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

// must match the -G overrides in the Makefile
static const uint32_t BASE = 1000;
static const uint32_t MASK = 4095;

static void lo() { dut->clk_i = 0; dut->eval(); }
static void hi() { dut->clk_i = 1; dut->eval(); }
static void step() { lo(); hi(); }

//! drive one ENTITY_DISCOVER and return the cycles until the response starts.
//! The engine loads disc_dly_r on the cycle the pulse is sampled and needs two
//! more cycles to reach S_SEND, so the measurement is delay + 2.
static uint32_t measure_delay(uint32_t timeout) {
    // start from a provably idle engine, or the measurement would time a frame
    // that was already in flight (a 0-cycle "delay" that means nothing)
    dut->m_axis_tready = 1;
    for (int k = 0; k < 64; k++) { lo(); if (!dut->m_axis_tvalid) { hi(); break; } hi(); }
    dut->rcv_discover_i = 1; step(); dut->rcv_discover_i = 0;
    for (uint32_t c = 0; c < timeout; c++) {
        lo();
        if (dut->m_axis_tvalid) {
            // drain the frame so the next draw starts from idle
            dut->m_axis_tready = 1;
            for (int k = 0; k < 40; k++) {
                bool last = dut->m_axis_tlast && dut->m_axis_tvalid;
                hi(); lo();
                if (last) break;
            }
            hi();
            return c;
        }
        hi();
    }
    return timeout;   // never fired -> caller flags it
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vadp_advertiser;

    dut->rst_n = 0; dut->enable_i = 0; dut->m_axis_tready = 1;
    dut->link_level_i = 1; dut->tick_i = 0;
    dut->link_up_i = dut->link_down_i = dut->shutdown_i = 0;
    dut->gm_change_i = dut->info_changed_i = dut->rcv_discover_i = 0;
    dut->station_mac_i = 0x001BC5AABBCCULL;
    dut->entity_id_i = 0xDEAD00BEEF00FEEDULL;
    dut->entity_model_id_i = 0x001BC5FFFE000101ULL;
    dut->entity_capabilities_i = 0xC588;
    dut->talker_stream_sources_i = 8; dut->talker_capabilities_i = 1;
    dut->listener_stream_sinks_i = 8; dut->listener_capabilities_i = 1;
    dut->controller_capabilities_i = 0;
    dut->gptp_grandmaster_id_i = 0x0011223344556677ULL;
    dut->gptp_domain_number_i = 0;
    dut->current_configuration_index_i = 0;
    dut->identify_control_index_i = 0;
    dut->interface_index_i = 0;
    dut->association_id_i = 0;
    dut->valid_time_i = 10;
    for (int i = 0; i < 4; i++) step();
    dut->rst_n = 1; dut->enable_i = 1;
    for (int i = 0; i < 2; i++) step();
    dut->link_up_i = 1; step(); dut->link_up_i = 0;
    // drain the link-up ENTITY_AVAILABLE
    for (int k = 0; k < 40; k++) { lo(); bool l = dut->m_axis_tvalid && dut->m_axis_tlast; hi(); if (l) break; }

    printf("== adp_advertiser discover-DELAY conformance (6.2.4.2.2) ==\n");
    printf("   DISC_DLY_BASE=%u  DISC_DLY_MASK=%u  (old envelope = [%u, %u])\n",
           BASE, MASK, BASE, BASE + MASK);

    const int VTS[] = {1, 2, 3, 4, 10, 31};
    const int DRAWS = 24;
    for (int v = 0; v < 6; v++) {
        uint32_t vt    = VTS[v];
        uint32_t bound = 2 * vt * BASE;          // 0.4 * valid_time seconds
        dut->valid_time_i = vt;
        for (int i = 0; i < 4; i++) step();
        uint32_t mn = 0xFFFFFFFFu, mx = 0, over = 0, none = 0;
        for (int d = 0; d < DRAWS; d++) {
            uint32_t got = measure_delay(4 * (BASE + MASK) + 64);
            if (got >= 4 * (BASE + MASK) + 64) { none++; continue; }
            uint32_t dly = (got >= 2) ? got - 2 : 0;   // strip the 2-cycle launch
            if (dly < mn) mn = dly;
            if (dly > mx) mx = dly;
            if (dly > bound) over++;
        }
        printf("   valid_time %2u: bound %6u  draws [%6u, %6u]  over-bound %u\n",
               vt, bound, mn, mx, over);
        char tag[96];
        snprintf(tag, sizeof tag, "vt %u: every draw within the 6.2.4.2.2 bound", vt);
        ck(tag, over, 0);
        snprintf(tag, sizeof tag, "vt %u: a response always came", vt);
        ck(tag, none, 0);
        snprintf(tag, sizeof tag, "vt %u: delay is RANDOM, not fixed", vt);
        ck(tag, mx != mn, 1);
        if (vt >= 4) {   // the shipped range: the envelope must be UNCHANGED
            snprintf(tag, sizeof tag, "vt %u: floor still DISC_DLY_BASE (no-op proof)", vt);
            ck(tag, mn >= BASE, 1);
            snprintf(tag, sizeof tag, "vt %u: ceiling still BASE+MASK (no-op proof)", vt);
            ck(tag, mx <= BASE + MASK, 1);
        } else {         // the shrunken arm: floor halves, envelope /8
            snprintf(tag, sizeof tag, "vt %u: floor is DISC_DLY_BASE/2", vt);
            ck(tag, mn >= BASE / 2, 1);
            snprintf(tag, sizeof tag, "vt %u: ceiling is BASE/2 + MASK/8", vt);
            ck(tag, mx <= BASE / 2 + MASK / 8, 1);
        }
    }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
