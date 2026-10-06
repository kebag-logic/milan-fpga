// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// model_main.cpp - the mailbox suite (suite.hpp) on the firmware's host model
// (sw/firmware/ctrl/host/mbx_model.c), graded by the RTL benches' own Checker
// (#665 lane FC).
//
// The host test's model arm already runs the suite on the model built against
// the tracked contract header. This driver exists for `make run-if2`: the
// model compiled against the two-interface variant of the contract
// (gen_mailbox.py --variant-interfaces 2, written into the build directory),
// so the per-interface own-MAC checks run on two real interfaces on the model
// as on the RTL through both adapters, against one set of expectations.

#include <cstdio>
#include <memory>

#include "../../common/verilator_harness.hpp"
#include "model_bench.hpp"
#include "suite.hpp"

int main() {
    char label[64];
    std::snprintf(label, sizeof label, "mbx (host model, %u interfaces)", static_cast<unsigned>(MBX_N_IF));
    milan::tb::Checker check{label};
    const auto model = std::make_unique<mbx_model>();
    mbx_tb::ModelBench bench(model.get());
    mbx_tb::Suite<mbx_tb::ModelBench> suite(bench, check);
    suite.run();
    return check.report();
}
