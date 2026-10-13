// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// MAAP ports on the FC mailbox. No port may call back synchronously (#678).
#ifndef CTRL_MAAP_MBX_H
#define CTRL_MAAP_MBX_H

#include "maap.h"
#include "acmp.h"
#include "ctrl_loop.h"

#ifdef __cplusplus
extern "C" {
#endif

// Bounds count bus transactions, not target CPU time. See maap/README.md. An
// allocation reported writes the range filter (3) and DA_GATE (1).
// F3b dispatch queries may read the clock once per source. Poll also
// allows one write for a changed declaration gate.
#define MAAP_MBX_EVENT_MAX (49u + ACMP_MAX_SOURCES)
#define MAAP_MBX_RX_MAX (48u + ACMP_MAX_SOURCES)
#define MAAP_MBX_POLL_MAX (49u + ACMP_MAX_SOURCES)
#define MAAP_MBX_PASS_MAX (CTRL_LOOP_EVENTS_PER_PASS * (6u + MAAP_MBX_EVENT_MAX) + \
	CTRL_LOOP_RX_PER_PASS * (20u + MAAP_MBX_RX_MAX) + MBX_N_IF * MAAP_MBX_POLL_MAX)

typedef void (*maap_allocation_fn)(void *ctx, unsigned interface, uint64_t base,
				 uint16_t count, bool valid);

struct maap_mbx_if {
	struct maap core;
	uint8_t slot;
	uint16_t tag;
	bool armed;
	bool link;
	uint32_t stale_expiries;
};

struct maap_mbx {
	struct maap_ports ports;
	struct maap_mbx_if ifs[MBX_N_IF];
	maap_allocation_fn allocation;
	void *allocation_ctx;
	uint32_t foreign_if;
	struct acmp *acmp;
	uint32_t published_gate[MBX_N_IF];
	uint32_t demand;
};

// Bind the declaration owner before attaching the adapter. No owner means
// no demand, so every DA_GATE remains closed.
void maap_mbx_bind_acmp(struct maap_mbx *m, struct acmp *acmp);

// Every interface owns its own MAC, machine and timer slot. allocation must
// be supplied and returns without waiting or calling any protocol core. count
// is the entity's talker sources, one address each, at most the publication
// block's MBX_N_PUB_SOURCES: before each allocation is reported, the adapter
// writes the interface's DA_GATE (valid range and cached ACMP demand).
bool maap_mbx_init(struct maap_mbx *m, const uint64_t mac[MBX_N_IF], uint16_t count,
		   unsigned first_slot, maap_allocation_fn allocation, void *ctx);
bool maap_mbx_attach(struct maap_mbx *m, struct ctrl_loop *loop);
// Called after ctrl_loop_open. False refuses a supplied range outside B.4.
bool maap_mbx_start(struct maap_mbx *m, uint64_t preferred);
void maap_mbx_stop(struct maap_mbx *m);

#ifdef __cplusplus
}
#endif
#endif
