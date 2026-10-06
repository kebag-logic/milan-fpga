// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_debug.c - the debug sink (see ctrl_debug.h). vsnprintf is the C11
// library's bounded formatter; the bare-metal C library the SoC links
// carries it, and it writes into the one static line buffer below.

#include "ctrl_debug.h"

#include <stdio.h>

static ctrl_debug_sink_fn bound_sink;
static void *bound_ctx;
static char line[CTRL_DEBUG_LINE_BYTES + 1u];
static uint32_t discarded;
static uint32_t truncated;

void ctrl_debug_bind(ctrl_debug_sink_fn sink, void *ctx)
{
	bound_sink = sink;
	bound_ctx = ctx;
}

int ctrl_debug_vprintf(const char *fmt, va_list ap)
{
	int want = vsnprintf(line, sizeof line, fmt, ap);
	if (want < 0 || bound_sink == NULL) {
		discarded++;
		return want < 0 ? want : 0;
	}
	size_t len = (size_t)want;
	if (len > CTRL_DEBUG_LINE_BYTES) {
		len = CTRL_DEBUG_LINE_BYTES;
		truncated++;
	}
	bound_sink(bound_ctx, line, len);
	return (int)len;
}

uint32_t ctrl_debug_discarded(void)
{
	return discarded;
}

uint32_t ctrl_debug_truncated(void)
{
	return truncated;
}
