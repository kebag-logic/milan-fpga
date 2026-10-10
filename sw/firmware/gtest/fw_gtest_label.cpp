// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// fw_gtest_label.cpp - the tally label of a firmware test binary none of whose
// test files names one.
//
// The tests of the tsn-c-stack submodule (#697) are the stack's own and carry
// no FW_TALLY_LABEL. A binary built from them alone takes its label from this
// file, compiled with FW_GTEST_LABEL set to it (fw_gtest.label_object).

#include "fw_gtest.hpp"

#ifndef FW_GTEST_LABEL
#error "FW_GTEST_LABEL: the binary's tally label, a string literal (fw_gtest.label_object)"
#endif

FW_TALLY_LABEL(FW_GTEST_LABEL)
