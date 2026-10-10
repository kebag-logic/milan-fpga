// SPDX-License-Identifier: CERN-OHL-W-2.0
// KLJ2 adaptation only; the core owns all live values, maps and validation.
#include "aecp_nvm.h"
#include "nvm_store.h"
#include "wire.h"
#include <string.h>

static bool value(struct aecp_nvm *n, unsigned group, unsigned index, struct aecp_value *v)
{
	*v = (struct aecp_value){AECP_CHANGE_CONFIGURATION, 0, (uint16_t)index, 0};
	switch (group) {
	case NVM_G_CFG: return index == 0u;
	case NVM_G_RATE: v->kind = AECP_CHANGE_RATE; v->type = 2u; return true;
	case NVM_G_CLKS: v->kind = AECP_CHANGE_CLOCK; v->type = 36u; return true;
	case NVM_G_FMTI: v->kind = AECP_CHANGE_FORMAT; v->type = 5u; return true;
	case NVM_G_FMTO: v->kind = AECP_CHANGE_FORMAT; v->type = 6u; return true;
	case NVM_G_PTOF: v->kind = AECP_CHANGE_LATENCY; v->type = 6u; return true;
	case NVM_G_NAME:
		if (index >= n->name_count) return false;
		*v = n->names[index]; return true;
	default: return false; // DR5: SUID and MCR remain deliberately erased.
	}
}

static struct aecp_map *map(struct aecp_nvm *n, unsigned group, unsigned index)
{
	for (size_t k = 0; k < n->core->cfg.map_count; ++k) {
		struct aecp_map *m = &n->core->cfg.maps[k];
		if (m->configuration == n->core->configuration && m->index == index &&
		    m->type == (group == NVM_G_MAPI ? 14u : 15u)) return m;
	}
	return NULL;
}

static enum nvm_apply verdict(unsigned status)
{
	return status == AECP_SUCCESS ? NVM_APPLIED :
		status == AECP_ENTITY_MISBEHAVING ? NVM_FAULT : NVM_REFUSED;
}

static int model_ready(void *ctx)
{
	struct aecp_nvm *n = ctx;
	return n->core->cfg.model->count != 0u;
}

static enum nvm_apply refused(struct aecp_nvm *n, const struct aecp_map *m)
{
	aecp_map_refused(n->core, m);
	return NVM_REFUSED;
}

static enum nvm_apply apply(void *ctx, unsigned group, unsigned index, const uint8_t *p, unsigned len)
{
	struct aecp_nvm *n = ctx;
	if (group == NVM_G_MAPI || group == NVM_G_MAPO) {
		struct aecp_map *m = map(n, group, index);
		if (m == NULL || m->capacity > n->scratch_count) return NVM_FAULT;
		if (len != m->capacity * 8u) return refused(n, m);
		size_t count = 0;
		bool unused = false;
		for (size_t k = 0; k < m->capacity; ++k) {
			const uint8_t *r = p + k * 8u;
			bool erased = wire_be64(r) == UINT64_MAX;
			if (erased) unused = true;
			else {
				if (unused) return refused(n, m); // No map edit on malformed framing.
				n->scratch[count++] = (struct aecp_mapping){(uint16_t)wire_be16(r),
					(uint16_t)wire_be16(r + 2), (uint16_t)wire_be16(r + 4), (uint16_t)wire_be16(r + 6)};
			}
		}
		unsigned status = aecp_map_restore(n->core, m, n->scratch, count);
		return status == AECP_BAD_ARGUMENTS ? refused(n, m) : verdict(status);
	}
	struct aecp_value v;
	return value(n, group, index, &v) ? verdict(aecp_value_restore(n->core, v, p, len)) : NVM_REFUSED;
}

static enum nvm_apply settle(void *ctx)
{
	struct aecp_nvm *n = ctx;
	return verdict(aecp_restore_settle(n->core));
}

static int rollback(void *ctx, enum nvm_walk walk)
{
	struct aecp_nvm *n = ctx;
	return walk == NVM_W_BIND || aecp_restore_defaults(n->core) ? 0 : -1;
}

static int latch(void *ctx, unsigned group, unsigned index, uint8_t *p, unsigned len)
{
	struct aecp_nvm *n = ctx;
	if (group == NVM_G_MAPI || group == NVM_G_MAPO) {
		struct aecp_map *m = map(n, group, index);
		if (m == NULL || len != m->capacity * 8u) return 0;
		memset(p, 0xff, len);
		for (size_t k = 0; k < m->count; ++k) {
			const struct aecp_mapping *r = &m->rows[k];
			wire_put_be(p + 8u*k, r->stream, 2);
			wire_put_be(p + 8u*k + 2u, r->channel, 2);
			wire_put_be(p + 8u*k + 4u, r->cluster, 2);
			wire_put_be(p + 8u*k + 6u, r->cluster_channel, 2);
		}
		return 1;
	}
	struct aecp_value v;
	return value(n, group, index, &v) && aecp_value_latch(n->core, v, p, len);
}

static void release(void *ctx)
{
	struct aecp_nvm *n = ctx;
	n->released = true; // The application opens AECP after this callback returns.
}

void aecp_nvm_init(struct aecp_nvm *n, struct aecp *core, const struct aecp_value *names, size_t count,
		   struct aecp_mapping *scratch, size_t capacity)
{
	memset(n, 0, sizeof *n);
	n->core = core; n->names = names; n->name_count = count;
	n->scratch = scratch; n->scratch_count = capacity;
	n->port = (struct nvm_state){model_ready, apply, settle, rollback, latch, release, n};
}

static void mark(struct aecp_nvm *n, unsigned group, unsigned index)
{
	struct nvm_rec r = nvm_rec_of(group, index);
	if (r.ok) n->pending[r.id / 32u] |= 1u << (r.id % 32u);
}

void aecp_nvm_changed(struct aecp_nvm *n, enum aecp_change kind, uint16_t type, uint16_t index)
{
	switch (kind) {
	case AECP_CHANGE_CONFIGURATION: mark(n, NVM_G_CFG, 0); break;
	case AECP_CHANGE_RATE: mark(n, NVM_G_RATE, index); break;
	case AECP_CHANGE_CLOCK: mark(n, NVM_G_CLKS, index); break;
	case AECP_CHANGE_FORMAT: mark(n, type == 5u ? NVM_G_FMTI : NVM_G_FMTO, index); break;
	case AECP_CHANGE_LATENCY: mark(n, NVM_G_PTOF, index); break;
	case AECP_CHANGE_MAP: mark(n, type == 14u ? NVM_G_MAPI : NVM_G_MAPO, index); break;
	case AECP_CHANGE_NAME:
		for (size_t k = 0; k < n->name_count; ++k) {
			if (n->names[k].type == type && n->names[k].index == index) mark(n, NVM_G_NAME, (unsigned)k);
		}
		break;
	default: break;
	}
}

bool aecp_nvm_poll(struct aecp_nvm *n)
{
	for (unsigned id = 0; id < 256u; ++id) {
		uint32_t bit = 1u << (id % 32u);
		if ((n->pending[id / 32u] & bit) != 0u) {
			n->pending[id / 32u] &= ~bit;
			struct nvm_rec r = nvm_rec_by_id(id);
			nvm_store_changed(r.group, r.index);
			return true;
		}
	}
	return false;
}
