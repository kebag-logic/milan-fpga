// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// The premise of the poll's skipped licence scan (#872, srp_mbx.c poll): a scan the poll skips, its interface not
// marked stale, would change no licence. Built with CTRL_SRP_LICENCE_CHECK, srp_mbx.c checks each skip against what the
// scan would have done and counts each that would have changed one. srp_arms.py compiles this after each SRP suite's
// own tests, so it reads the count over all of them.
#include <gtest/gtest.h>
#include <cstdio>

#include "srp_mbx.h"

TEST(SrpLicence, EverySkippedScanWasAFixedPoint) {
    std::printf("  licence scans run: %lu; skipped: %lu; skipped that would have changed a licence: %lu\n",
                srp_licence_scans, srp_licence_skips, srp_licence_unmarked);
    EXPECT_EQ(srp_licence_unmarked, 0u) << "a skipped licence scan would have changed a licence";
}
