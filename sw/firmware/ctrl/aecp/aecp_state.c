// SPDX-License-Identifier: CERN-OHL-W-2.0
// Saved-state owner: SAVED_STATE_MATERIALIZATION 8.3-8.6 and #658 ruling.
#include "aecp_state.h"
#include "aecp_internal.h"

static bool field(struct aecp *a, struct aecp_value v, struct aecp_descriptor **d,
		  unsigned *offset, unsigned *width, unsigned *bit)
{
	*d = aecp_find(a, a->configuration, v.type, v.index);
	*bit = 1u;
	switch (v.kind) {
	case AECP_CHANGE_CONFIGURATION:
		*d = aecp_find(a, 0, 0, 0); *offset = 310u; *width = 2u; break;
	case AECP_CHANGE_FORMAT:
		if (v.type != 5u && v.type != 6u) return false;
		*offset = 74u; *width = 8u; break;
	case AECP_CHANGE_RATE:
		if (v.type != 2u) return false;
		*offset = 136u; *width = 4u; break;
	case AECP_CHANGE_CLOCK:
		if (v.type != 36u) return false;
		*offset = 70u; *width = 2u; break;
	case AECP_CHANGE_LATENCY:
		if (v.type != 6u) return false;
		*offset = 0u; *width = 4u; *bit = 2u; break;
	case AECP_CHANGE_NAME:
		*offset = aecp_name_offset(v.type, v.name); *width = 64u; *bit = 0u;
		if (*offset == 0u) return false;
		break;
	default:
		return false;
	}
	return *d != NULL && (*d)->length >= *offset + *width;
}

unsigned aecp_value_restore(struct aecp *a, struct aecp_value v, const uint8_t *p, size_t bytes)
{
	if (!aecp_enter(a) || a->open) return AECP_ENTITY_MISBEHAVING;
	struct aecp_descriptor *d;
	unsigned offset, width, bit;
	if (!field(a, v, &d, &offset, &width, &bit)) return AECP_ENTITY_MISBEHAVING;
	if (bytes != width) return AECP_BAD_ARGUMENTS;
	unsigned status = AECP_SUCCESS;
	if (v.kind == AECP_CHANGE_CONFIGURATION) {
		if (wire_be16(p) >= a->cfg.model->configurations) return AECP_BAD_ARGUMENTS;
		a->configuration = (uint16_t)wire_be16(p);
	} else if (v.kind == AECP_CHANGE_LATENCY) {
		if ((p[0] & 0x80u) != 0u) return AECP_BAD_ARGUMENTS;
		a->cfg.latency[v.index] = (uint32_t)wire_be32(p);
	} else if (v.kind != AECP_CHANGE_NAME) {
		status = aecp_scalar_validate(a, d, v.kind, p);
	}
	if (status != AECP_SUCCESS) return status;
	if (v.kind != AECP_CHANGE_LATENCY) memcpy(d->value + offset, p, width);
	aecp_override(a, d, bit);
	return AECP_SUCCESS;
}

bool aecp_value_latch(struct aecp *a, struct aecp_value v, uint8_t *p, size_t bytes)
{
	if (!aecp_enter(a)) return false;
	struct aecp_descriptor *d;
	unsigned offset, width, bit;
	if (!field(a, v, &d, &offset, &width, &bit) || bytes != width ||
	    (bit != 0u && !aecp_overridden(a, d, bit))) return false;
	if (v.kind == AECP_CHANGE_LATENCY) wire_put_be(p, a->cfg.latency[v.index], 4);
	else memcpy(p, d->value + offset, width);
	return true;
}

bool aecp_restore_defaults(struct aecp *a)
{
	if (!aecp_enter(a) || a->open) return false;
	for (size_t n = 0; n < a->cfg.model->count; ++n) {
		struct aecp_descriptor *d = &a->cfg.model->descriptors[n];
		memcpy(d->value, d->defaults, d->length);
		a->cfg.events[n].overrides = 0;
		if (d->type == 6u) a->cfg.latency[d->index] = 0;
	}
	struct aecp_descriptor *d = aecp_find(a, 0, 0, 0);
	a->configuration = (uint16_t)wire_be16(d->defaults + 310);
	for (size_t n = 0; n < a->cfg.map_count; ++n) {
		struct aecp_map *m = &a->cfg.maps[n];
		m->count = m->default_count;
		for (size_t k = 0; k < m->count; ++k) m->rows[k] = m->defaults[k];
	}
	return true;
}
