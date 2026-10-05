// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_check.c - see test_check.h.

#include "test_check.h"

#include <inttypes.h>
#include <stdio.h>

static unsigned long checks;
static unsigned long failures;

void check(const char *what, bool ok)
{
	checks++;
	if (!ok) {
		failures++;
		printf("  [FAIL] %s\n", what);
		fflush(stdout);
	}
}

void check_eq(const char *what, uint64_t got, uint64_t expected)
{
	checks++;
	if (got != expected) {
		failures++;
		printf("  [FAIL] %-56s got=0x%" PRIx64 " exp=0x%" PRIx64 "\n", what, got, expected);
		fflush(stdout);
	}
}

int check_report(const char *label)
{
	printf("== %s: checks: %lu   failures: %lu ==\n", label, checks, failures);
	printf("RESULT: %s\n", failures == 0 ? "PASS" : "FAIL");
	return failures == 0 ? 0 : 1;
}
