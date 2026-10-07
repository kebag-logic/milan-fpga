// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// acmp_if2.cpp - the `acmpif2` arm's own part (#665 lane F3): its tally label
// and the re-entry trap the core's host build calls. The arm builds
// test_acmp_mbx.cpp again, with the firmware and the host model, on the
// contract elaborated for two AVB interfaces (gen_mailbox.py
// --variant-interfaces 2), so the adapter's per-interface wiring (slots,
// tags, the gPTP pair, the bound-talker table, the latency paths) is graded
// at two interfaces as well as at the tracked one.

#include "fw_gtest.hpp"
#include "mbx_contract.h"

static_assert(MBX_N_IF == 2u, "the acmpif2 arm builds the contract's two-interface variant");

FW_TALLY_LABEL("ctrl ACMP adapter on the two-interface contract (host model)");

extern "C" void ctrl_reentry_assert(const char* module) {
    static_cast<void>(module);
}
