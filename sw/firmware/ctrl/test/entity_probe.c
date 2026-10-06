// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// entity_probe.c - print the ENTITY_AVAILABLE the ADP slice builds from one
// shape's generated entity header (adp_entity_gen.h, from adp_entity.py), as
// hex on one line, so the host test can compare its fields with what the
// fabric is programmed and compiled with for the same shape (#665 lane F0).

#include <stdio.h>

#include "adp.h"
#include "adp_entity_gen.h"

static bool no_send(void *ctx, unsigned interface, const uint8_t *frame, size_t len)
{
	(void)ctx;
	(void)interface;
	(void)frame;
	(void)len;
	return false;
}

static void no_timer(void *ctx, unsigned interface, uint32_t delay_ms)
{
	(void)ctx;
	(void)interface;
	(void)delay_ms;
}

static void no_stop(void *ctx, unsigned interface)
{
	(void)ctx;
	(void)interface;
}

static void zero_gptp(void *ctx, unsigned interface, uint64_t *gm_id, uint8_t *domain)
{
	(void)ctx;
	(void)interface;
	*gm_id = 0;
	*domain = 0;
}

static bool link_down(void *ctx, unsigned interface)
{
	(void)ctx;
	(void)interface;
	return false;
}

static uint32_t zero_seed(void *ctx)
{
	(void)ctx;
	return 0;
}

int main(void)
{
	static const struct adp_entity entity = ADP_ENTITY_GEN_INIT;
	static const struct adp_ports ports = {NULL, no_send, no_timer, no_stop, zero_gptp, link_down, zero_seed};
	struct adp a;
	uint8_t frame[ADP_FRAME_BYTES];
	adp_init(&a, &entity, &ports, 0, 0);
	adp_build(&a, ADP_MSG_ENTITY_AVAILABLE, 0, frame);
	for (unsigned k = 0; k < ADP_FRAME_BYTES; ++k) {
		printf("%02x", frame[k]);
	}
	printf("\n");
	return 0;
}
