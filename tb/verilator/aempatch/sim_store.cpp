/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * KL_aecp_aem_store write-port ARBITRATION, tested at the RAM directly.
 *
 * WHY A SECOND EXECUTABLE. The frame-level suite (sim_main.cpp) can never
 * collide the store's two write masters: the patch port only accepts commands
 * while the ADP advertiser is down, and the AECP engine discards commands in
 * exactly that state. That is the design working — but it means the arbiter
 * is UNTESTED there, and a mutation campaign proved it: flipping the priority
 * to "patch wins" left sim_main.cpp fully green. This file is the check that
 * mutation earned (mutation anchor: "[S3] the patch byte did NOT land").
 *
 * The property has two halves and BOTH matter:
 *   * the SET_* write-back wins the cycle — live controller traffic outranks
 *     a boot-time restore;
 *   * the losing patch byte is NOT DROPPED, it is NOT ACKED. pw_ack_o is the
 *     whole contract; a store that swallowed the byte and acked anyway would
 *     leave a descriptor field half-restored, which is the one failure mode a
 *     persistence port must not have.
 *
 * Exit 0 = all pass.
 */

#include "VKL_aecp_aem_store.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

static VKL_aecp_aem_store* dut;
static long checks = 0, fails = 0;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-56s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-56s = %ld\n", what, got); }
}

//! one read: address in, one clock, byte out
static int rd(uint16_t a) {
    dut->addr_i = a; dut->rd_i = 1;
    tick();
    dut->rd_i = 0;
    dut->eval();
    return dut->data_o;
}
static void idle() {
    dut->wr_i = 0; dut->pw_wr_i = 0; dut->rd_i = 0;
    tick();
}

// two byte addresses inside the descriptor image, far apart
#define ADDR_A 0x0280
#define ADDR_B 0x0300

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_aecp_aem_store;

    dut->rst_n = 0;
    dut->addr_i = 0; dut->rd_i = 0;
    dut->wr_addr_i = 0; dut->wr_i = 0; dut->wr_data_i = 0;
    dut->pw_addr_i = 0; dut->pw_wr_i = 0; dut->pw_data_i = 0;
    dut->factory_reset_i = 0;
    for (int i = 0; i < 4; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) tick();

    printf("== AEM store write-port arbitration (builder vs saved-state patch) ==\n");

    printf("\n[S0] each master alone reaches the RAM\n");
    dut->wr_i = 1; dut->wr_addr_i = ADDR_A; dut->wr_data_i = 0xA1;
    dut->eval();
    ck("[S0] no patch request -> no ack", dut->pw_ack_o, 0);
    tick();
    idle();
    ck("[S0] builder byte landed", rd(ADDR_A), 0xA1);

    dut->pw_wr_i = 1; dut->pw_addr_i = ADDR_B; dut->pw_data_i = 0xB1;
    dut->eval();
    ck("[S0] uncontended patch request is ACKED", dut->pw_ack_o, 1);
    tick();
    idle();
    ck("[S0] patch byte landed", rd(ADDR_B), 0xB1);

    printf("\n[S1] the builder wins a contended cycle\n");
    dut->wr_i = 1;    dut->wr_addr_i = ADDR_A; dut->wr_data_i = 0xA2;
    dut->pw_wr_i = 1; dut->pw_addr_i = ADDR_B; dut->pw_data_i = 0xB2;
    dut->eval();
    //! mutation anchor: flip the store's write mux to "patch wins" and this
    //! ack, and [S3] below, are what go red
    ck("[S1] contended patch request is NOT acked", dut->pw_ack_o, 0);
    tick();
    idle();
    ck("[S1] the builder byte landed", rd(ADDR_A), 0xA2);

    printf("\n[S2] and the loser is not silently swallowed\n");
    ck("[S2] the patch byte did NOT land (still the [S0] value)",
       rd(ADDR_B), 0xB1);

    printf("\n[S3] the retried byte lands on the next free cycle\n");
    //! this is what KL_aem_patch does: hold the byte until pw_ack_o
    dut->wr_i = 0;
    dut->pw_wr_i = 1; dut->pw_addr_i = ADDR_B; dut->pw_data_i = 0xB2;
    dut->eval();
    ck("[S3] now acked", dut->pw_ack_o, 1);
    tick();
    idle();
    ck("[S3] the patch byte landed on retry", rd(ADDR_B), 0xB2);

    printf("\n[S4] same-address collision resolves to the builder too\n");
    dut->wr_i = 1;    dut->wr_addr_i = ADDR_A; dut->wr_data_i = 0xA3;
    dut->pw_wr_i = 1; dut->pw_addr_i = ADDR_A; dut->pw_data_i = 0xB3;
    dut->eval();
    ck("[S4] patch not acked on the same address", dut->pw_ack_o, 0);
    tick();
    idle();
    ck("[S4] the RAM holds the builder's byte", rd(ADDR_A), 0xA3);

    printf("\n[S5] a read is never disturbed by either write\n");
    dut->wr_i = 1;    dut->wr_addr_i = ADDR_A; dut->wr_data_i = 0xA4;
    dut->pw_wr_i = 0;
    ck("[S5] read of the OTHER address is clean", rd(ADDR_B), 0xB2);
    idle();
    ck("[S5] and the write still happened", rd(ADDR_A), 0xA4);

    printf("\n----------------------------------------------------------\n");
    printf("aem store arbitration: %ld checks, %ld failures\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
