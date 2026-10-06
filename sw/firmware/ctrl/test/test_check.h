// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_check.h - the counting checks of the firmware's C host tests. The
// tally line is the shape scripts/suite_tally.py reads
// (`checks: N   failures: M`), and a failure prints its name, so a planted
// defect is reported by the check it reddened.

#ifndef TEST_CHECK_H
#define TEST_CHECK_H

#include <stdbool.h>
#include <stdint.h>

void check(const char *what, bool ok);
void check_eq(const char *what, uint64_t got, uint64_t expected);
int check_report(const char *label);

#endif // TEST_CHECK_H
