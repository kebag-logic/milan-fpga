// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// model_suite.cpp - the mailbox suite's checks (tb/verilator/mbx/suite.hpp),
// the ones the RTL passes through both bus adapters, run on the host model
// (#665 lane F0). A difference between the model and the RTL fails here or
// there; the firmware's host tests may then rely on the model.

#include <memory>

#include "verilator_harness.hpp"
#include "model_bench.hpp"
#include "suite.hpp"

int main() {
    const auto model = std::make_unique<mbx_model>();
    milan::tb::Checker check{"mbx (host model)"};
    mbx_tb::ModelBench bench(model.get());
    mbx_tb::Suite<mbx_tb::ModelBench> suite(bench, check);
    suite.run();
    return check.report();
}
