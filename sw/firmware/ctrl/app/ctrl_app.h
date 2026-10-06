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
// F0 composes the ADP slice and F3 the ACMP module (with the ADP channel's
// AVAILABLE and DEPARTING tapped for the listener's discovery, acmp_mbx.h).
// Each later lane (MAAP, SRP through lwSRP, AECP) adds its adapter here and
// nowhere else.
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

#ifdef __cplusplus
extern "C" {
#endif

// The fabric timer slot of interface 0's ADP machine, and of interface 0's
// ACMP sinks, which follow ADP's.
#define CTRL_APP_ADP_FIRST_SLOT 0u
#define CTRL_APP_ACMP_FIRST_SLOT (CTRL_APP_ADP_FIRST_SLOT + MBX_N_IF)

struct ctrl_app {
	struct ctrl_pool pool;
	struct ctrl_loop loop;
	struct adp_mbx adp;
	struct acmp_mbx acmp;
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

#ifdef __cplusplus
}
#endif

#endif // CTRL_APP_H
