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
// F0 composes the ADP slice. Each later lane (MAAP, ACMP, SRP through lwSRP,
// AECP) adds its adapter here and nowhere else.

#ifndef CTRL_APP_H
#define CTRL_APP_H

#include <stdbool.h>
#include <stddef.h>

#include "adp_mbx.h"
#include "ctrl_debug.h"
#include "ctrl_loop.h"
#include "ctrl_pool.h"
#include "maap_mbx.h"

#ifdef __cplusplus
extern "C" {
#endif

// The fabric timer slot of interface 0's ADP machine.
#define CTRL_APP_ADP_FIRST_SLOT 0u

struct ctrl_app {
	struct ctrl_pool pool;
	struct ctrl_loop loop;
	struct adp_mbx adp;
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
};

// Bind everything, bring the mailbox up and start the protocols. False, with
// nothing opened, when the pool cannot be carved, a binding does not fit or
// the bitstream carries another contract.
bool ctrl_app_start(struct ctrl_app *app, const struct ctrl_app_config *cfg);

// Explicit F2 composition. The default entry above remains ADP-only.
// allocation is the stream-address port (maap_csr_allocation on the existing
// datapath CSR window). The count is the entity's declared talker sources.
bool ctrl_app_start_maap(struct ctrl_app *app, const struct ctrl_app_config *cfg,
			 maap_allocation_fn allocation, void *ctx, uint64_t preferred);

#ifdef __cplusplus
}
#endif

#endif // CTRL_APP_H
