// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_app.h - the control-plane firmware composed for bare metal: the static
// pool behind lwSRP's port, the debug sink, the event loop and the protocol
// adapters, wired in the order the contract requires (#665 lane F0).
//
// One object holds the whole firmware state, so a platform declares it (and
// the pool's arena) statically and nothing is ever allocated at run time
// except from the pool. The same composition runs on the target and on the
// host against the mailbox model; only mbx_hal.h and the sink differ.
//
// F0 composes the ADP slice, F2 the MAAP owner and F3 the ACMP module (with
// the ADP channel's AVAILABLE and DEPARTING tapped for the listener's
// discovery, acmp_mbx.h). MAAP and ACMP are each composed only when the
// configuration supplies them. Each later lane (SRP through lwSRP, AECP) adds
// its adapter here and nowhere else.
//
// THE ATTACH ORDER. ADP, then ACMP (it stands in front of ADP's handler of the
// adp channel), then MAAP, all before the open, so the open enables every
// bound channel's receive interrupt and filter with the events'
// (ctrl_loop_open). Each owns MBX_N_IF fabric timer slots of its own.
//
// THE BOOT ORDER. ctrl_app_compose() binds every module into the loop and
// touches no mailbox register; ctrl_app_open() brings the mailbox up in the
// contract's order and starts the protocols. A platform runs the saved-state
// restore between the two (acmp_nvm.h), so the bindings it restores are in
// place before any channel opens. ctrl_app_start() is the two with nothing
// between.

#ifndef CTRL_APP_H
#define CTRL_APP_H

#include <stdbool.h>
#include <stddef.h>

#include "acmp_mbx.h"
#include "adp_mbx.h"
#include "ctrl_debug.h"
#include "ctrl_loop.h"
#include "ctrl_pool.h"
#include "maap_mbx.h"

#ifdef __cplusplus
extern "C" {
#endif

// The fabric timer slot of interface 0's ADP machine, of interface 0's ACMP
// sinks, which follow ADP's, and of interface 0's MAAP machine, which follows
// ACMP's: three disjoint runs of MBX_N_IF slots.
#define CTRL_APP_ADP_FIRST_SLOT 0u
#define CTRL_APP_ACMP_FIRST_SLOT (CTRL_APP_ADP_FIRST_SLOT + MBX_N_IF)
#define CTRL_APP_MAAP_FIRST_SLOT (CTRL_APP_ACMP_FIRST_SLOT + MBX_N_IF)

// A pass of the three-way composition costs at most CTRL_APP_PASS_MAX mailbox
// accesses: a pass of ADP and ACMP (ACMP_MBX_PASS_MAX, acmp_mbx.h), whose
// terms already hold every event record's own words, plus MAAP's share
// (maap_mbx.h): its costliest action on each of the pass's events, its two
// records of the maap channel (the largest, 64 bytes) with its costliest
// handler, and its poll on every interface. Each pass count of acmp_mbx.h and
// maap/README.md holds in the composed loop with this pass in place of its own.
#define CTRL_APP_MAAP_RX_RECORD_MAX (2u + MBX_RX_HDR_WORDS + MBX_CH_MAAP_MAX_FRAME_BYTES / 4u)
#define CTRL_APP_MAAP_PASS_SHARE                                                                                   \
	(CTRL_LOOP_EVENTS_PER_PASS * MAAP_MBX_EVENT_MAX +                                                          \
	 CTRL_LOOP_RX_PER_PASS * (CTRL_APP_MAAP_RX_RECORD_MAX + MAAP_MBX_RX_MAX) + MBX_N_IF * MAAP_MBX_POLL_MAX)
#define CTRL_APP_PASS_MAX (ACMP_MBX_PASS_MAX + CTRL_APP_MAAP_PASS_SHARE)

struct ctrl_app {
	struct ctrl_pool pool;
	struct ctrl_loop loop;
	struct adp_mbx adp;
	struct acmp_mbx acmp;
	struct maap_mbx maap;
};

struct ctrl_app_config {
	const struct adp_entity *entity;
	uint16_t current_configuration_index;
	void *arena;                            // the pool's static arena
	size_t arena_bytes;
	const struct ctrl_pool_class *classes;  // the pool's size classes
	unsigned n_classes;
	ctrl_debug_sink_fn sink;                // shlan_printf's destination
	void *sink_ctx;
	// The entity's STREAM_INPUTs and STREAM_OUTPUTs and their owners (the
	// lock, the sources, SRP, the store, the notifier); NULL for an entity
	// with no stream, which composes no ACMP.
	const struct acmp_config *acmp;
	const struct acmp_env *acmp_env;
	// The stream-address port (maap_csr_allocation on the existing datapath
	// CSR window) and its context; NULL composes no MAAP. MAAP claims the
	// entity's declared talker sources, from maap_preferred when it is not 0
	// (a range inside the B.4 pool, else the composition is refused).
	maap_allocation_fn maap_allocation;
	void *maap_ctx;
	uint64_t maap_preferred;
};

// Bind everything into the loop; no mailbox access. False when the pool
// cannot be carved, a binding does not fit or a module refuses its
// configuration.
bool ctrl_app_compose(struct ctrl_app *app, const struct ctrl_app_config *cfg);

// Bring the mailbox up and start the protocols. False, with nothing opened,
// when the bitstream carries another contract.
bool ctrl_app_open(struct ctrl_app *app, const struct ctrl_app_config *cfg);

// ctrl_app_compose() then ctrl_app_open().
bool ctrl_app_start(struct ctrl_app *app, const struct ctrl_app_config *cfg);

// Explicit F2 composition: ctrl_app_start() with cfg's MAAP fields replaced by
// allocation, ctx and preferred. False, with nothing opened, when allocation
// is NULL. ctrl_app_start() composes MAAP only when cfg supplies it.
bool ctrl_app_start_maap(struct ctrl_app *app, const struct ctrl_app_config *cfg,
			 maap_allocation_fn allocation, void *ctx, uint64_t preferred);

#ifdef __cplusplus
}
#endif

#endif // CTRL_APP_H
