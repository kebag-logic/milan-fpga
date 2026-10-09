// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// acmp_nvm.h - the listener's bindings on the saved-state store's state port
// (#665 lane F3; the store is lane F1's, sw/firmware/ctrl_nvm).
//
// The store (nvm_store.h) restores and saves through one state port
// (nvm_state.h), one call per record. The binding group belongs to the ACMP
// listener, every other group to the entity's other owners. acmp_nvm is that
// port: the binding group's records go to the ACMP core, every other call is
// forwarded unchanged to the integrator's port for the rest.
//
//   apply     a binding record: acmp_restore_binding (a saved binding starts
//             its sink in PRB_W_AVAIL with discovery running, Milan v1.2
//             5.5.3.5.2: the fast connect); APPLIED, or REFUSED for a record
//             the core cannot take (a sink the configuration does not have, a
//             payload of another length). It never answers FAULT: a binding's
//             rule is judged from its own bytes.
//   rollback  NVM_W_BIND drops every restored binding (acmp_restore_rollback)
//             and succeeds; NVM_W_D3 is the others'.
//   latch     a binding record: the sink's record now (acmp_binding_latch),
//             all zeros for an unbound sink, which is how an unbind is saved.
//   model_ready, settle, release: the others'.
//
// THE BOOT ORDER a platform runs: ctrl_app_compose(), acmp_nvm_init() on the
// app's ACMP core, nvm_store_boot() with acmp_nvm's port, nvm_store_service()
// bound as a centisecond consumer of the loop (ctrl_loop_add_tick), then
// ctrl_app_open(). The ACMP env's persist port calls
// nvm_store_changed(NVM_G_BIND, sink). The store decides what is written:
// while a slot it could not read holds its writer (ctrl_nvm/README.md, "Boot"
// item 9), a binding change is marked and not saved.

#ifndef ACMP_NVM_H
#define ACMP_NVM_H

#include "acmp.h"
#include "nvm_state.h"

#ifdef __cplusplus
extern "C" {
#endif

struct acmp_nvm {
	struct acmp *acmp;
	unsigned bind_group;                    // the store's binding group (nvm_klj2.h NVM_G_BIND)
	const struct nvm_state *others;         // every other group's owners
	struct nvm_state port;                  // the state port the store boots and saves with
};

void acmp_nvm_init(struct acmp_nvm *n, struct acmp *acmp, unsigned bind_group, const struct nvm_state *others);

#ifdef __cplusplus
}
#endif

#endif // ACMP_NVM_H
