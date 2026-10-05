// SPDX-License-Identifier: CERN-OHL-W-2.0
// axil_stress.cpp - reviewer probe for PR #668 (#665 F0): the bus adapters
// under master behaviour the mailbox suite's bench never produces.
//   AXI4-Lite (tb_mbx_top HOST_P=1): AW before W, W before AW, BREADY and
//   RREADY held low (VALID and payload must hold), AR offered in the same
//   cycle as AW+W (both must complete, none lost), back-to-back reads.
//   Wishbone (HOST_P=0): two classic cycles back to back with STB held.
// Built against the head's own RTL list with tb/verilator/mbx/tb_mbx_top.sv.
#include <cstdint>
#include <cstdio>
#include "Vtb_mbx_top.h"
#include "verilated.h"

static Vtb_mbx_top* d;
static unsigned fails = 0, checks = 0;
static void ck(const char* what, bool ok) { ++checks; if (!ok) { ++fails; std::printf("[FAIL] %s\n", what); } else std::printf("[ok] %s\n", what); }
static void half_low() { d->clk_i = 0; d->eval(); }
static void rise() { d->clk_i = 1; d->eval(); }
static void step() { half_low(); rise(); }
enum : uint32_t { OWN_LO = 0x20, OWN_HI = 0x24, MAAP_LO = 0x2C, DEADLINE = 0x38, ID = 0x0 };

static void idle_inputs() {
    d->wb_cyc_i = 0; d->wb_stb_i = 0; d->s_awvalid_i = 0; d->s_wvalid_i = 0; d->s_arvalid_i = 0;
    d->s_bready_i = 0; d->s_rready_i = 0; d->tx_ready_i = 1; d->rx_valid_i = 0; d->ms_tick_p_i = 0;
}
static void reset() { idle_inputs(); d->rst_n = 0; for (int i = 0; i < 4; ++i) step(); d->rst_n = 1; step(); }

// a polite AXI read (for checking results), RREADY high
static uint32_t axil_read(uint32_t a) {
    d->s_arvalid_i = 1; d->s_araddr_i = a; d->s_rready_i = 1;
    bool taken = false; uint32_t v = 0xDEADBEEF;
    for (int i = 0; i < 20; ++i) {
        half_low();
        bool hs = d->s_arready_o, rv = d->s_rvalid_o; if (rv) v = d->s_rdata_o;
        rise();
        if (hs) { taken = true; d->s_arvalid_i = 0; }
        if (taken && rv) break;
    }
    d->s_rready_i = 0; return v;
}

static void axi_tests() {
    reset();
    // S1: AW three cycles before W
    {
        d->s_awvalid_i = 1; d->s_awaddr_i = OWN_LO; d->s_bready_i = 1;
        bool aw_done = false, w_done = false, b = false;
        for (int i = 0; i < 30 && !b; ++i) {
            if (i == 3) { d->s_wvalid_i = 1; d->s_wdata_i = 0xA5A50001; d->s_wstrb_i = 0xF; }
            half_low();
            bool awhs = d->s_awvalid_i && d->s_awready_o, whs = d->s_wvalid_i && d->s_wready_o, bv = d->s_bvalid_o;
            rise();
            if (awhs) { aw_done = true; d->s_awvalid_i = 0; }
            if (whs) { w_done = true; d->s_wvalid_i = 0; }
            if (aw_done && w_done && bv) b = true;
        }
        d->s_bready_i = 0;
        ck("S1 AW three cycles before W completes with a B response", b);
        ck("S1 and the write lands", axil_read(OWN_LO) == 0xA5A50001);
    }
    // S2: W three cycles before AW
    {
        d->s_wvalid_i = 1; d->s_wdata_i = 0x5A5A0002; d->s_wstrb_i = 0xF; d->s_bready_i = 1;
        bool aw_done = false, w_done = false, b = false;
        for (int i = 0; i < 30 && !b; ++i) {
            if (i == 3) { d->s_awvalid_i = 1; d->s_awaddr_i = OWN_HI; }
            half_low();
            bool awhs = d->s_awvalid_i && d->s_awready_o, whs = d->s_wvalid_i && d->s_wready_o, bv = d->s_bvalid_o;
            rise();
            if (awhs) { aw_done = true; d->s_awvalid_i = 0; }
            if (whs) { w_done = true; d->s_wvalid_i = 0; }
            if (aw_done && w_done && bv) b = true;
        }
        d->s_bready_i = 0;
        ck("S2 W three cycles before AW completes with a B response", b);
        ck("S2 and the write lands", axil_read(OWN_HI) == 0x5A5A0002);
    }
    // S3: BREADY low for 6 cycles after BVALID rises: BVALID holds, nothing new is taken
    {
        d->s_awvalid_i = 1; d->s_wvalid_i = 1; d->s_awaddr_i = MAAP_LO; d->s_wdata_i = 0x11112222; d->s_wstrb_i = 0xF;
        d->s_bready_i = 0;
        int i = 0; bool taken = false;
        for (; i < 10 && !taken; ++i) { half_low(); taken = d->s_awready_o && d->s_wready_o; rise(); }
        d->s_awvalid_i = 0; d->s_wvalid_i = 0;
        int rise_at = -1; for (int k = 0; k < 10 && rise_at < 0; ++k) { half_low(); if (d->s_bvalid_o) rise_at = k; else rise(); }
        bool held = rise_at >= 0;
        d->s_arvalid_i = 1; d->s_araddr_i = ID;   // a read offered while B waits must not be taken
        bool read_taken = false;
        for (int k = 0; k < 6; ++k) { half_low(); held = held && d->s_bvalid_o && d->s_bresp_o == 0; read_taken |= d->s_arready_o; rise(); }
        ck("S3 BVALID holds while BREADY is low", held);
        ck("S3 no read is accepted while a B response is outstanding", !read_taken);
        d->s_arvalid_i = 0;
        d->s_bready_i = 1; half_low(); bool hs = d->s_bvalid_o; rise(); d->s_bready_i = 0; half_low();
        ck("S3 the B handshake completes once BREADY rises, and BVALID falls", hs && !d->s_bvalid_o); rise();
        ck("S3 the write lands", axil_read(MAAP_LO) == 0x11112222);
    }
    // S4: RREADY low for 6 cycles: RVALID and RDATA hold
    {
        d->s_arvalid_i = 1; d->s_araddr_i = OWN_LO; d->s_rready_i = 0;
        bool taken = false; for (int i = 0; i < 10 && !taken; ++i) { half_low(); taken = d->s_arready_o; rise(); }
        d->s_arvalid_i = 0;
        int seen = -1; for (int k = 0; k < 10 && seen < 0; ++k) { half_low(); if (d->s_rvalid_o) seen = k; else rise(); }
        bool held = seen >= 0; uint32_t first = d->s_rdata_o;
        for (int k = 0; k < 6; ++k) { half_low(); held = held && d->s_rvalid_o && d->s_rdata_o == first; rise(); }
        ck("S4 RVALID and RDATA hold while RREADY is low", held);
        ck("S4 RDATA is the register", first == 0xA5A50001);
        d->s_rready_i = 1; half_low(); rise(); d->s_rready_i = 0; half_low();
        ck("S4 RVALID falls after the R handshake", !d->s_rvalid_o); rise();
    }
    // S5: AR in the same cycle as AW+W (write wins, read follows, both complete)
    {
        d->s_awvalid_i = 1; d->s_wvalid_i = 1; d->s_awaddr_i = DEADLINE; d->s_wdata_i = 0xCAFE0005; d->s_wstrb_i = 0xF;
        d->s_arvalid_i = 1; d->s_araddr_i = DEADLINE; d->s_bready_i = 1; d->s_rready_i = 1;
        bool w_taken = false, r_taken = false, b = false, r = false; uint32_t rd = 0;
        for (int i = 0; i < 40 && !(b && r); ++i) {
            half_low();
            bool whs = d->s_awvalid_i && d->s_awready_o && d->s_wready_o, rhs = d->s_arvalid_i && d->s_arready_o;
            bool bv = d->s_bvalid_o, rv = d->s_rvalid_o; if (rv) rd = d->s_rdata_o;
            rise();
            if (whs) { w_taken = true; d->s_awvalid_i = 0; d->s_wvalid_i = 0; }
            if (rhs) { r_taken = true; d->s_arvalid_i = 0; }
            if (w_taken && bv) b = true;
            if (r_taken && rv) r = true;
        }
        d->s_bready_i = 0; d->s_rready_i = 0;
        ck("S5 a write and a read offered together both complete", b && r);
        ck("S5 the write was ordered first: the read returns the new value", rd == 0xCAFE0005);
    }
    // S6: ARVALID held high across ten reads, RREADY high
    {
        d->s_arvalid_i = 1; d->s_araddr_i = OWN_HI; d->s_rready_i = 1;
        unsigned got = 0, good = 0;
        for (int i = 0; i < 60 && got < 10; ++i) {
            half_low(); bool rv = d->s_rvalid_o; uint32_t v = d->s_rdata_o; rise();
            if (rv) { ++got; good += v == 0x5A5A0002; }
        }
        d->s_arvalid_i = 0; d->s_rready_i = 0; step(); step();
        ck("S6 ten back-to-back reads with ARVALID held all return the register", got == 10 && good == 10);
    }
}

static void wb_tests() {
    reset();
    // W1: two classic writes back to back, STB held across the first ACK
    d->wb_cyc_i = 1; d->wb_stb_i = 1; d->wb_we_i = 1; d->wb_sel_i = 0xF;
    d->wb_adr_i = OWN_LO >> 2; d->wb_dat_i = 0x01020304;
    unsigned acks = 0;
    for (int i = 0; i < 20 && acks < 2; ++i) {
        half_low(); bool ack = d->wb_ack_o; rise();
        if (ack) { ++acks; d->wb_adr_i = OWN_HI >> 2; d->wb_dat_i = 0x05060708; }
    }
    d->wb_cyc_i = 0; d->wb_stb_i = 0; step();
    auto wbr = [](uint32_t a) {
        d->wb_cyc_i = 1; d->wb_stb_i = 1; d->wb_we_i = 0; d->wb_adr_i = a >> 2; uint32_t v = 0;
        for (int i = 0; i < 20; ++i) { half_low(); bool ack = d->wb_ack_o; v = d->wb_dat_o; rise(); if (ack) break; }
        d->wb_cyc_i = 0; d->wb_stb_i = 0; step(); return v;
    };
    ck("W1 two back-to-back classic cycles are both acknowledged", acks == 2);
    ck("W1 the first write lands", wbr(OWN_LO) == 0x01020304);
    ck("W1 the second write lands at its own address", wbr(OWN_HI) == 0x05060708);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    d = new Vtb_mbx_top;
    const bool axi = argc > 1 && argv[1][0] == '1';
    if (axi) axi_tests(); else wb_tests();
    std::printf("== adapter stress (%s): checks: %u   failures: %u ==\n", axi ? "AXI4-Lite" : "Wishbone", checks, fails);
    delete d;
    return fails ? 1 : 0;
}
