// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mbx_plat_host.c - mbx_hal.h on the host: every access goes to the mailbox
// model bound by mbx_model_bind(), which counts it. The firmware above is the
// target's, unchanged; only these three functions differ.

#include "mbx_hal.h"
#include "mbx_model.h"

static struct mbx_model *bound_model;
static void (*bound_wait)(void *ctx);
static void *bound_wait_ctx;
static mbx_host_trace_fn trace_fn;
static void *trace_ctx;

void mbx_host_trace(mbx_host_trace_fn fn, void *ctx)
{
	trace_fn = fn;
	trace_ctx = ctx;
}

void mbx_model_bind(struct mbx_model *m, void (*wait)(void *ctx), void *ctx)
{
	bound_model = m;
	bound_wait = wait;
	bound_wait_ctx = ctx;
}

uint32_t mbx_hal_read32(uint32_t byte_offset)
{
	uint32_t value = mbx_model_read(bound_model, byte_offset);
	if (trace_fn != NULL) {
		trace_fn(trace_ctx, false, byte_offset, value);
	}
	return value;
}

void mbx_hal_write32(uint32_t byte_offset, uint32_t value)
{
	if (trace_fn != NULL) {
		trace_fn(trace_ctx, true, byte_offset, value);
	}
	mbx_model_write(bound_model, byte_offset, value, 0xFu);
}

void mbx_hal_wait(void)
{
	if (bound_wait != NULL) {
		bound_wait(bound_wait_ctx);
	}
}
