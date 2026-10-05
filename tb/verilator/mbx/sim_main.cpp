// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_main.cpp - the packet-mailbox fabric skeleton (KL_mbx and its leaves),
// graded through one bus adapter per build (#665 lane F0).
//
// Built twice from this file: HOST_P=0 reaches the window through KL_mbx_wb,
// HOST_P=1 through KL_mbx_axil, and every check of suite.hpp runs on both.
// The AXI4-Lite build then runs the adapter's own handshake checks
// (axil_checks.hpp), which a Wishbone host has no counterpart for.
// The same checks run on the firmware's host model (the host test's model
// arm), so the RTL and the model answer to one set of expectations.

#include "../../common/verilator_harness.hpp"
#include "Vtb_mbx_top.h"
#include "axil_checks.hpp"
#include "bench.hpp"
#include "suite.hpp"
#include "verilated.h"

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vtb_mbx_top> model;
    const unsigned host = argc > 1 && argv[1][0] == '1' ? 1u : 0u;
    milan::tb::Checker check{host == 0 ? "mbx (Wishbone host)" : "mbx (AXI4-Lite host)"};
    mbx_tb::Bench bench(model.get(), host);
    mbx_tb::Suite<mbx_tb::Bench> suite(bench, check);
    suite.run();
    if (host == 1) {
        mbx_tb::AxilChecks axil(bench, check);
        axil.run();
    }
    return check.report();
}
