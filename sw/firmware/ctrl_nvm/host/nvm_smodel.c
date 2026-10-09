/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/*
 * nvm_smodel.c - the host model behind the state port (#665 lane F1).
 */
#include <string.h>

#include "../nvm_klj2.h"
#include "nvm_smodel.h"

struct sm_state {
	uint8_t value[NVM_ID_SPACE][NVM_PAYLOAD_MAX];
	uint8_t valid[NVM_ID_SPACE];
	uint8_t refuse[NVM_ID_SPACE];
	int ready;
	int fault_apply;
	unsigned int fault_apply_id;
	int fault_settle;
	int fault_rollback[2];
	int settled;
	int released;
	int d3_started;
	int last_id[2];
	struct nvm_smodel_count n;
};

static struct sm_state sm;

uint8_t nvm_smodel_default(unsigned int id, unsigned int j)
{
	return (uint8_t)(id * 7u + j * 3u + 0x5au);
}

/* The walk a record belongs to: the bindings, or D3 for every other id. */
static enum nvm_walk sm_walk(unsigned int id)
{
	struct nvm_rec r = nvm_rec_by_id(id);

	return (r.ok && r.group == NVM_G_BIND) ? NVM_W_BIND : NVM_W_D3;
}

static void sm_defaults(enum nvm_walk walk)
{
	unsigned int id;
	unsigned int j;

	for (id = 0; id < NVM_ID_SPACE; ++id) {
		if (sm_walk(id) != walk)
			continue;
		for (j = 0; j < NVM_PAYLOAD_MAX; ++j)
			sm.value[id][j] = nvm_smodel_default(id, j);
		sm.valid[id] = 0;
	}
}

void nvm_smodel_reset(void)
{
	memset(&sm, 0, sizeof(sm));
	sm_defaults(NVM_W_BIND);
	sm_defaults(NVM_W_D3);
	sm.ready = 1;
	sm.last_id[NVM_W_BIND] = -1;
	sm.last_id[NVM_W_D3] = -1;
}

void nvm_smodel_ready(int ready)
{
	sm.ready = ready;
}

void nvm_smodel_refuse(unsigned int id)
{
	sm.refuse[id % NVM_ID_SPACE] = 1;
}

void nvm_smodel_fault_apply(unsigned int id)
{
	sm.fault_apply = 1;
	sm.fault_apply_id = id;
}

void nvm_smodel_fault_settle(int on)
{
	sm.fault_settle = on;
}

void nvm_smodel_fault_rollback(enum nvm_walk walk)
{
	sm.fault_rollback[walk] = 1;
}

void nvm_smodel_set(unsigned int id, const uint8_t *value, unsigned int len)
{
	id %= NVM_ID_SPACE;
	memcpy(sm.value[id], value, len < NVM_PAYLOAD_MAX ? len : NVM_PAYLOAD_MAX);
	sm.valid[id] = 1;
}

const uint8_t *nvm_smodel_value(unsigned int id)
{
	return sm.value[id % NVM_ID_SPACE];
}

int nvm_smodel_valid(unsigned int id)
{
	return sm.valid[id % NVM_ID_SPACE];
}

const struct nvm_smodel_count *nvm_smodel_count(void)
{
	return &sm.n;
}

static int sm_ready(void *ctx)
{
	(void)ctx;
	return sm.ready;
}

/* Every binding before the D3 walk; each walk ascending; a format or map
 * record before the settle step, a name after it. */
static void sm_police(unsigned int group, int id)
{
	enum nvm_walk walk = (group == NVM_G_BIND) ? NVM_W_BIND : NVM_W_D3;

	if (sm.released || id <= sm.last_id[walk])
		sm.n.order++;
	if (walk == NVM_W_BIND && sm.d3_started)
		sm.n.order++;
	if (walk == NVM_W_D3)
		sm.d3_started = 1;
	if (group == NVM_G_NAME && !sm.settled)
		sm.n.order++;
	if (sm.settled && (group == NVM_G_FMTI || group == NVM_G_FMTO ||
			   group == NVM_G_MAPI || group == NVM_G_MAPO))
		sm.n.order++;
	sm.last_id[walk] = id;
}

static enum nvm_apply sm_apply(void *ctx, unsigned int group, unsigned int index,
			       const uint8_t *payload, unsigned int len)
{
	struct nvm_rec r = nvm_rec_of(group, index);

	(void)ctx;
	sm.n.applies++;
	if (!r.ok || r.plen != len) {
		sm.n.order++;
		return NVM_FAULT;
	}
	sm_police(group, r.id);
	if (sm.fault_apply && r.id == sm.fault_apply_id) {
		sm.n.faults++;
		return NVM_FAULT;
	}
	if (sm.refuse[r.id]) {
		sm.n.refused++;
		return NVM_REFUSED;
	}
	memcpy(sm.value[r.id], payload, len);
	sm.valid[r.id] = 1;
	sm.n.applied++;
	return NVM_APPLIED;
}

static enum nvm_apply sm_settle(void *ctx)
{
	(void)ctx;
	sm.n.settles++;
	if (sm.settled || sm.released)
		sm.n.order++;
	sm.settled = 1;
	sm.d3_started = 1;
	if (sm.fault_settle) {
		sm.n.faults++;
		return NVM_FAULT;
	}
	return NVM_APPLIED;
}

static int sm_rollback(void *ctx, enum nvm_walk walk)
{
	(void)ctx;
	if (walk == NVM_W_BIND)
		sm.n.unbinds++;
	else
		sm.n.rollbacks++;
	if (sm.released)
		sm.n.order++;
	if (sm.fault_rollback[walk])
		return -1;
	sm_defaults(walk);
	return 0;
}

static int sm_latch(void *ctx, unsigned int group, unsigned int index,
		    uint8_t *payload, unsigned int len)
{
	struct nvm_rec r = nvm_rec_of(group, index);

	(void)ctx;
	sm.n.latches++;
	if (!r.ok || r.plen != len || !sm.valid[r.id])
		return 0;
	memcpy(payload, sm.value[r.id], len);
	return 1;
}

static void sm_release(void *ctx)
{
	(void)ctx;
	sm.n.releases++;
	if (sm.released)
		sm.n.order++;
	sm.released = 1;
}

const struct nvm_state nvm_smodel_port = {
	sm_ready, sm_apply, sm_settle, sm_rollback, sm_latch, sm_release, 0,
};
