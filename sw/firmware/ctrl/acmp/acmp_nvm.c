// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// acmp_nvm.c - the listener's bindings on the store's state port (see
// acmp_nvm.h).

#include "acmp_nvm.h"

static int model_ready(void *ctx)
{
	struct acmp_nvm *n = ctx;
	return n->others->model_ready(n->others->ctx);
}

static enum nvm_apply apply(void *ctx, unsigned int group, unsigned int index, const uint8_t *payload,
			    unsigned int len)
{
	struct acmp_nvm *n = ctx;
	if (group != n->bind_group) {
		return n->others->apply(n->others->ctx, group, index, payload, len);
	}
	return acmp_restore_binding(n->acmp, index, payload, len) == ACMP_RESTORE_APPLIED ? NVM_APPLIED : NVM_REFUSED;
}

static enum nvm_apply settle(void *ctx)
{
	struct acmp_nvm *n = ctx;
	return n->others->settle(n->others->ctx);
}

static int rollback(void *ctx, enum nvm_walk walk)
{
	struct acmp_nvm *n = ctx;
	if (walk != NVM_W_BIND) {
		return n->others->rollback(n->others->ctx, walk);
	}
	acmp_restore_rollback(n->acmp);
	return 0;
}

static int latch(void *ctx, unsigned int group, unsigned int index, uint8_t *payload, unsigned int len)
{
	struct acmp_nvm *n = ctx;
	if (group != n->bind_group) {
		return n->others->latch(n->others->ctx, group, index, payload, len);
	}
	return len == ACMP_BINDING_BYTES && acmp_binding_latch(n->acmp, index, payload) ? 1 : 0;
}

static void release(void *ctx)
{
	struct acmp_nvm *n = ctx;
	n->others->release(n->others->ctx);
}

void acmp_nvm_init(struct acmp_nvm *n, struct acmp *acmp, unsigned bind_group, const struct nvm_state *others)
{
	n->acmp = acmp;
	n->bind_group = bind_group;
	n->others = others;
	n->port.model_ready = model_ready;
	n->port.apply = apply;
	n->port.settle = settle;
	n->port.rollback = rollback;
	n->port.latch = latch;
	n->port.release = release;
	n->port.ctx = n;
}
