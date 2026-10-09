// SPDX-License-Identifier: CERN-OHL-W-2.0
// Command bodies: IEEE 1722.1-2021 7.4, Milan v1.2 5.4.2.
#include "aecp_internal.h"

struct aecp_descriptor *aecp_find(struct aecp *a, uint16_t cfg, uint16_t type, uint16_t index)
{
	for (size_t n = 0; n < a->cfg.model->count; ++n) {
		struct aecp_descriptor *d = &a->cfg.model->descriptors[n];
		if (d->configuration == cfg && d->type == type && d->index == index) {
			return d;
		}
	}
	return NULL;
}

bool aecp_foreign_lock(const struct aecp *a)
{
	return a->locked && a->lock_owner != a->requester;
}

bool aecp_overridden(const struct aecp *a, const struct aecp_descriptor *d, unsigned bit)
{
	return (a->cfg.events[(size_t)(d - a->cfg.model->descriptors)].overrides & bit) != 0u;
}

void aecp_override(struct aecp *a, const struct aecp_descriptor *d, unsigned bit)
{
	a->cfg.events[(size_t)(d - a->cfg.model->descriptors)].overrides |= (uint8_t)bit;
}

void aecp_note(struct aecp *a, enum aecp_change kind, uint16_t type, uint16_t index)
{
	a->in_port = true;
	a->ports->changed(a->ports->ctx, kind, type, index);
	a->in_port = false;
	a->notify = true;
}

bool aecp_stream_read(struct aecp *a, uint16_t type, uint16_t index, struct aecp_stream_info *out)
{
	struct aecp_descriptor *d = aecp_find(a, a->configuration, type, index);
	memset(out, 0, sizeof *out);
	if (d == NULL || d->length < 128u) {
		return false;
	}
	unsigned interface = (unsigned)wire_be16(d->value + 126u);
	if (interface >= a->cfg.interfaces) {
		return false;
	}
	a->in_port = true;
	bool ok = a->ports->stream(a->ports->ctx, interface, type, index, out);
	a->in_port = false;
	return ok;
}

static unsigned running(struct aecp *a, uint16_t type, uint16_t index)
{
	struct aecp_stream_info info;
	if (!aecp_stream_read(a, type, index, &info)) return AECP_ENTITY_MISBEHAVING;
	return (type == 5u ? info.bound : info.running) ? AECP_STREAM_IS_RUNNING : AECP_SUCCESS;
}

static unsigned any_running(struct aecp *a)
{
	for (size_t n = 0; n < a->cfg.model->count; ++n) {
		struct aecp_descriptor *d = &a->cfg.model->descriptors[n];
		if (d->configuration == a->configuration && (d->type == 5u || d->type == 6u)) {
			unsigned status = running(a, d->type, d->index);
			if (status != AECP_SUCCESS) return status;
		}
	}
	return AECP_SUCCESS;
}

static unsigned descriptor(struct aecp *a, const uint8_t *in, size_t len, uint8_t *out, size_t *bytes)
{
	*bytes = 8u;
	if (len < 8u) {
		return AECP_BAD_ARGUMENTS;
	}
	memcpy(out, in, 8u);
	out[2] = out[3] = 0;
	uint16_t cfg = (uint16_t)wire_be16(in);
	uint16_t type = (uint16_t)wire_be16(in + 4);
	// IEEE 7.4.5.1/2: root descriptors ignore this field on receipt.
	if (type == 0u || type == 1u) {
		cfg = 0u;
		out[0] = out[1] = 0;
	}
	if (cfg >= a->cfg.model->configurations) {
		return AECP_BAD_ARGUMENTS;
	}
	struct aecp_descriptor *d = aecp_find(a, cfg, type, (uint16_t)wire_be16(in + 6));
	if (d == NULL) {
		return AECP_NO_SUCH_DESCRIPTOR;
	}
	if (d->length > AECP_FRAME_BYTES - 42u) {
		return AECP_NO_RESOURCES;
	}
	memcpy(out + 4, d->value, d->length);
	*bytes = 4u + d->length;
	return AECP_SUCCESS;
}

static unsigned configuration(struct aecp *a, bool set, const uint8_t *in, size_t len,
			      uint8_t *out, size_t *bytes)
{
	*bytes = 4u;
	unsigned status = AECP_SUCCESS;
	if (set) {
		if (len < 4u) {
			status = AECP_BAD_ARGUMENTS;
		} else if ((status = any_running(a)) != AECP_SUCCESS) {
			// Refuse both a running stream and an unprovable observation.
		} else if (aecp_foreign_lock(a)) {
			status = AECP_ENTITY_LOCKED;
		} else if (wire_be16(in + 2) >= a->cfg.model->configurations) {
			status = AECP_BAD_ARGUMENTS;
		} else {
			struct aecp_descriptor *entity = aecp_find(a, 0, 0, 0);
			bool changed = a->configuration != wire_be16(in + 2) || !aecp_overridden(a, entity, 1u);
			a->configuration = (uint16_t)wire_be16(in + 2);
			// ENTITY may be represented in every configuration's descriptor list.
			for (size_t n = 0; n < a->cfg.model->count; ++n) {
				struct aecp_descriptor *d = &a->cfg.model->descriptors[n];
				if (d->type == 0u && d->length >= 312u) {
					wire_put_be(d->value + 310, a->configuration, 2);
				}
			}
			aecp_override(a, entity, 1u);
			if (changed) {
				aecp_note(a, AECP_CHANGE_CONFIGURATION, 0, 0);
			}
		}
	}
	wire_put_be(out + 2, a->configuration, 2);
	return status;
}

unsigned aecp_name_offset(uint16_t type, uint16_t name)
{
	if (type == 0u) {
		return name < 2u ? 48u + 132u * name : 0u;
	}
	switch (type) {
	case 1: case 2: case 3: case 4: case 5: case 6: case 7: case 8:
	case 9: case 10: case 11: case 20: case 21: case 22: case 24: case 25:
	case 26: case 27: case 28: case 29: case 30: case 31: case 32: case 33:
	case 34: case 35: case 36: case 37: case 38: case 39:
		return name == 0u ? 4u : 0u;
	default:
		return 0u;
	}
}

static unsigned names(struct aecp *a, bool set, const uint8_t *in, size_t len,
		      uint8_t *out, size_t *bytes)
{
	*bytes = 72u;
	if (len < (set ? 72u : 8u)) {
		return AECP_BAD_ARGUMENTS;
	}
	memcpy(out, in, 8u);
	uint16_t type = (uint16_t)wire_be16(in), index = (uint16_t)wire_be16(in + 2);
	uint16_t cfg = (uint16_t)wire_be16(in + 6);
	if (cfg >= a->cfg.model->configurations) {
		return AECP_BAD_ARGUMENTS;
	}
	struct aecp_descriptor *d = aecp_find(a, cfg, type, index);
	if (d == NULL) {
		return AECP_NO_SUCH_DESCRIPTOR;
	}
	unsigned offset = aecp_name_offset(type, (uint16_t)wire_be16(in + 4));
	if (offset == 0u || offset + 64u > d->length) {
		return AECP_BAD_ARGUMENTS;
	}
	unsigned status = AECP_SUCCESS;
	if (set) {
		if (aecp_foreign_lock(a)) {
			status = AECP_ENTITY_LOCKED;
		} else if (memcmp(d->value + offset, in + 8, 64u) != 0) {
			memcpy(d->value + offset, in + 8, 64u);
			aecp_note(a, AECP_CHANGE_NAME, type, index);
		}
	}
	memcpy(out + 8, d->value + offset, 64u);
	return status;
}

// Value/list fields in IEEE 7.2 AUDIO_UNIT, STREAM and CLOCK_DOMAIN.
unsigned aecp_scalar_validate(struct aecp *a, const struct aecp_descriptor *d, enum aecp_change kind, const uint8_t *value)
{
	bool format = kind == AECP_CHANGE_FORMAT;
	bool rate = kind == AECP_CHANGE_RATE;
	unsigned width = format ? 8u : (rate ? 4u : 2u);
	unsigned field = format ? 82u : (rate ? 140u : 72u);
	if (d->length < field + 4u) {
		return AECP_ENTITY_MISBEHAVING;
	}
	size_t start = (size_t)wire_be16(d->value + field);
	size_t count = (size_t)wire_be16(d->value + field + 2u);
	if (start > d->length || count * width > d->length - start) {
		return AECP_ENTITY_MISBEHAVING;
	}
	if (format) {
		a->in_port = true;
		bool supported = a->ports->format(a->ports->ctx, d->type, d->index, wire_be64(value));
		a->in_port = false;
		return supported ? AECP_SUCCESS : AECP_BAD_ARGUMENTS;
	}
	for (size_t n = 0; n < count; ++n) {
		if (memcmp(d->value + start + n * width, value, width) == 0) {
			return AECP_SUCCESS;
		}
	}
	return AECP_BAD_ARGUMENTS;
}

static unsigned scalar(struct aecp *a, uint16_t cmd, const uint8_t *in, size_t len,
		       uint8_t *out, size_t *bytes)
{
	bool format = cmd == 8u || cmd == 9u;
	bool rate = cmd == 20u || cmd == 21u;
	bool set = (cmd & 1u) == 0u;
	unsigned width = format ? 8u : (rate ? 4u : 2u);
	unsigned offset = format ? 74u : (rate ? 136u : 70u);
	unsigned list_offset = format ? 82u : (rate ? 140u : 72u);
	*bytes = format ? 12u : 8u;
	// SET_CLOCK_SOURCE includes its reserved halfword (IEEE 7.4.23.1).
	if (len < (set ? *bytes : 4u)) {
		return AECP_BAD_ARGUMENTS;
	}
	memcpy(out, in, 4u);
	uint16_t type = (uint16_t)wire_be16(in), index = (uint16_t)wire_be16(in + 2);
	if (format ? (type != 5u && type != 6u) : type != (rate ? 2u : 36u)) {
		return AECP_NOT_SUPPORTED;
	}
	struct aecp_descriptor *d = aecp_find(a, a->configuration, type, index);
	if (d != NULL && d->length >= offset + width) {
		memcpy(out + 4, d->value + offset, width);
	}
	if (d == NULL) {
		return AECP_NO_SUCH_DESCRIPTOR;
	}
	if (set && format) {
		unsigned state = running(a, type, index);
		if (state != AECP_SUCCESS) return state;
	}
	if (set && aecp_foreign_lock(a)) {
		return AECP_ENTITY_LOCKED;
	}
	if (d->length < list_offset + 4u) {
		return AECP_ENTITY_MISBEHAVING;
	}
	if (!set) {
		return AECP_SUCCESS;
	}
	enum aecp_change kind = format ? AECP_CHANGE_FORMAT : (rate ? AECP_CHANGE_RATE : AECP_CHANGE_CLOCK);
	unsigned status = aecp_scalar_validate(a, d, kind, in + 4);
	if (status != AECP_SUCCESS) {
		return status;
	}
	if (format && !aecp_maps_allow_format(a, type, index, wire_be64(in + 4))) {
		return AECP_BAD_ARGUMENTS;
	}
	if (!aecp_overridden(a, d, 1u) || memcmp(d->value + offset, in + 4, width) != 0) {
		memcpy(d->value + offset, in + 4, width);
		aecp_override(a, d, 1u);
		aecp_note(a, kind, type, index);
	}
	memcpy(out + 4, d->value + offset, width);
	return AECP_SUCCESS;
}

static unsigned stream_info(struct aecp *a, bool set, const uint8_t *in, size_t len,
			    uint8_t *out, size_t *bytes)
{
	*bytes = set ? 84u : 56u;
	if (len < (set ? 84u : 4u)) {
		return AECP_BAD_ARGUMENTS;
	}
	memcpy(out, in, 4u);
	uint16_t type = (uint16_t)wire_be16(in), index = (uint16_t)wire_be16(in + 2);
	if (type != 5u && type != 6u) {
		return AECP_NOT_SUPPORTED;
	}
	struct aecp_descriptor *d = aecp_find(a, a->configuration, type, index);
	if (d == NULL) {
		return AECP_NO_SUCH_DESCRIPTOR;
	}
	struct aecp_stream_info info;
	if (!aecp_stream_read(a, type, index, &info)) {
		return AECP_ENTITY_MISBEHAVING;
	}
	// IEEE 7.4.15.1: report current fields even when the SET is refused.
	uint32_t flags = info.flags;
	if (set) {
		flags |= 0x80000000u; // The descriptor supplies the current format.
		if (type == 6u) flags &= ~0x08000000u; // Failure information is input-only.
	}
	wire_put_be(out + 4, flags, 4);
	memcpy(out + 8, d->value + 74, 8u);
	wire_put_be(out + 16, info.stream_id, 8);
	wire_put_be(out + 24, type == 6u && aecp_overridden(a, d, 2u) ? a->cfg.latency[index] : info.latency, 4);
	wire_put_be(out + 28, info.dest_mac, 6);
	if (!set || type == 5u) {
		out[34] = info.failure_code;
		wire_put_be(out + 36, info.failure_bridge_id, 8);
	}
	wire_put_be(out + 44, info.vlan, 2);
	if (set) {
		if (type == 5u) {
			return AECP_NOT_SUPPORTED;
		}
		if (info.running) {
			return AECP_STREAM_IS_RUNNING;
		}
		if (aecp_foreign_lock(a)) {
			return AECP_ENTITY_LOCKED;
		}
		uint32_t requested = (uint32_t)wire_be32(in + 4);
		// Milan 5.4.2.9: refuse unsupported XXX_VALID sub-commands.
		// IEEE 7.4.15.1: SAVED_STATE and STREAMING_WAIT are ignored.
		if ((requested & 0xdaf80000u) != 0u) {
			return AECP_NOT_SUPPORTED;
		}
		if ((requested & 0x20000000u) == 0u) {
			wire_put_be(out + 4, flags & ~0x20000000u, 4);
			return AECP_SUCCESS;
		}
		uint32_t latency = (uint32_t)wire_be32(in + 24);
		if ((latency & 0x80000000u) != 0u) {
			return AECP_BAD_ARGUMENTS;
		}
		if (!aecp_overridden(a, d, 2u) || a->cfg.latency[index] != latency) {
			a->cfg.latency[index] = latency;
			aecp_override(a, d, 2u);
			aecp_note(a, AECP_CHANGE_LATENCY, type, index);
		}
		wire_put_be(out + 4, flags | 0x20000000u, 4);
		wire_put_be(out + 24, latency, 4); // Milan preserves the requested latency.
		return AECP_SUCCESS;
	}
	wire_put_be(out + 48, info.flags_ex, 4);
	out[52] = (uint8_t)((info.probing_status << 5) | (info.acmp_status & 31u));
	return AECP_SUCCESS;
}

static unsigned counters(struct aecp *a, const uint8_t *in, size_t len, uint8_t *out, size_t *bytes)
{
	*bytes = 136u;
	if (len < 4u) {
		return AECP_BAD_ARGUMENTS;
	}
	memcpy(out, in, 4u);
	uint16_t type = (uint16_t)wire_be16(in), index = (uint16_t)wire_be16(in + 2);
	if (type != 5u && type != 6u && type != 9u && type != 36u) {
		return AECP_NOT_SUPPORTED;
	}
	struct aecp_descriptor *d = aecp_find(a, a->configuration, type, index);
	if (d == NULL) {
		return AECP_NO_SUCH_DESCRIPTOR;
	}
	unsigned interface = type == 9u ? index : 0u;
	if ((type == 5u || type == 6u) && d->length >= 128u) {
		interface = (unsigned)wire_be16(d->value + 126u);
	}
	struct aecp_counters snapshot = {0};
	a->in_port = true;
	bool ok = a->ports->counters(a->ports->ctx, interface, type, index, &snapshot);
	a->in_port = false;
	if (!ok) {
		return AECP_ENTITY_MISBEHAVING;
	}
	wire_put_be(out + 4, snapshot.valid, 4);
	for (unsigned n = 0; n < 32u; ++n) {
		wire_put_be(out + 8u + 4u * n, snapshot.value[n], 4);
	}
	return AECP_SUCCESS;
}

static unsigned avb(struct aecp *a, bool path, const uint8_t *in, size_t len, uint8_t *out, size_t *bytes)
{
	*bytes = path ? 4u : 20u;
	if (len < 4u) {
		return AECP_BAD_ARGUMENTS;
	}
	memcpy(out, in, path ? 2u : 4u);
	if (!path && wire_be16(in) != 9u) {
		return AECP_NOT_SUPPORTED;
	}
	uint16_t index = (uint16_t)wire_be16(in + (path ? 0u : 2u));
	if (aecp_find(a, a->configuration, 9u, index) == NULL) {
		return AECP_NO_SUCH_DESCRIPTOR;
	}
	if (index >= a->cfg.interfaces) {
		return AECP_ENTITY_MISBEHAVING;
	}
	if (path) {
		uint64_t sequence[AECP_PATH_ITEMS];
		size_t count = 0;
		a->in_port = true;
		bool ok = a->ports->path(a->ports->ctx, index, index, sequence, AECP_PATH_ITEMS, &count);
		a->in_port = false;
		if (!ok || count > AECP_PATH_ITEMS) {
			return AECP_ENTITY_MISBEHAVING;
		}
		wire_put_be(out + 2, count, 2);
		for (size_t n = 0; n < count; ++n) {
			wire_put_be(out + 4u + 8u * n, sequence[n], 8);
		}
		*bytes += 8u * count;
	} else {
		struct aecp_avb_info info = {0};
		a->in_port = true;
		bool ok = a->ports->avb(a->ports->ctx, index, index, &info);
		a->in_port = false;
		if (!ok) {
			return AECP_ENTITY_MISBEHAVING;
		}
		wire_put_be(out + 4, info.gm_id, 8);
		wire_put_be(out + 12, info.propagation_delay, 4);
		out[16] = info.domain;
		out[17] = info.flags;
		wire_put_be(out + 18, 1, 2);
		out[20] = 6u; // IEEE 802.1Q SR Class A traffic class
		out[21] = info.class_priority;
		wire_put_be(out + 22, info.class_vlan, 2);
		*bytes = 24u;
	}
	return AECP_SUCCESS;
}

static unsigned lock(struct aecp *a, const uint8_t *in, size_t len, uint8_t *out, size_t *bytes)
{
	*bytes = 16u;
	if (len < 16u) {
		return AECP_BAD_ARGUMENTS;
	}
	memcpy(out, in, 16u);
	if (wire_be32(in + 12) != 0u) {
		return AECP_NOT_SUPPORTED;
	}
	unsigned status = AECP_SUCCESS;
	if (aecp_foreign_lock(a)) {
		status = AECP_ENTITY_LOCKED;
	} else {
		bool take = (wire_be32(in) & 1u) == 0u;
		a->notify = take != a->locked;
		a->locked = take;
		a->lock_owner = take ? a->requester : 0u;
		a->lock_deadline = a->now + 60000u;
	}
	wire_put_be(out + 4, a->lock_owner, 8);
	return status;
}

static unsigned control(struct aecp *a, bool set, const uint8_t *in, size_t len, uint8_t *out, size_t *bytes)
{
	*bytes = 5u;
	if (len < (set ? 5u : 4u)) {
		return AECP_BAD_ARGUMENTS;
	}
	memcpy(out, in, 4u);
	out[4] = a->identify;
	if (wire_be16(in) != 26u) {
		return AECP_NOT_SUPPORTED;
	}
	if (set && aecp_foreign_lock(a)) {
		return AECP_ENTITY_LOCKED;
	}
	uint16_t index = (uint16_t)wire_be16(in + 2);
	struct aecp_descriptor *d = aecp_find(a, a->configuration, 26u, index);
	if (d == NULL) {
		return AECP_NO_SUCH_DESCRIPTOR;
	}
	// Milan 5.3.12: IDENTIFY CONTROL, CONTROL_LINEAR_UINT8, one value.
	if (d->length < 109u || wire_be64(d->value + 82u) != 0x90e0f00000000001ull) {
		return AECP_NOT_SUPPORTED;
	}
	if (set) {
		if (in[4] != 0u && in[4] != 255u) {
			return AECP_BAD_ARGUMENTS;
		}
		if (a->identify != in[4]) {
			a->identify = in[4];
			d->value[108] = in[4];
			aecp_note(a, AECP_CHANGE_IDENTIFY, 26u, index);
		}
	}
	out[4] = a->identify;
	return AECP_SUCCESS;
}

static bool dynamic_member(uint16_t cmd)
{
	switch (cmd) {
	case 7: case 9: case 11: case 13: case 15: case 17: case 19:
	case 21: case 23: case 29: case 41: case 72: case 74:
		return true;
	default:
		return false;
	}
}

static unsigned dynamic(struct aecp *a, unsigned interface, const uint8_t *in, size_t len,
			uint8_t *out, size_t *bytes)
{
	*bytes = 0;
	if (len > 512u) {
		return AECP_BAD_ARGUMENTS;
	}
	for (size_t at = 0; at < len;) {
		if (len - at < 8u) {
			return AECP_BAD_ARGUMENTS;
		}
		size_t size = (size_t)wire_be16(in + at);
		if (size > len - at - 8u || !dynamic_member((uint16_t)wire_be16(in + at + 6))) {
			return AECP_BAD_ARGUMENTS;
		}
		at += 8u + size;
	}
	for (size_t at = 0; at < len;) {
		size_t size = (size_t)wire_be16(in + at);
		size_t result_bytes = 0;
		uint16_t cmd = (uint16_t)wire_be16(in + at + 6);
		uint8_t result[AECP_FRAME_BYTES];
		unsigned status = aecp_command(a, interface, cmd, in + at + 8, size, result, &result_bytes);
		if (in[at + 4] != 0u) {
			status = AECP_BAD_ARGUMENTS;
		} else if (status == AECP_NOT_IMPLEMENTED) {
			status = AECP_NOT_SUPPORTED;
		}
		if (*bytes + 8u + result_bytes <= 512u) {
			wire_put_be(out + *bytes, result_bytes, 2);
			out[*bytes + 4] = (uint8_t)status;
			wire_put_be(out + *bytes + 6, cmd, 2);
			memcpy(out + *bytes + 8, result, result_bytes);
			*bytes += 8u + result_bytes;
		}
		at += 8u + size;
	}
	return AECP_SUCCESS;
}

unsigned aecp_command(struct aecp *a, unsigned interface, uint16_t cmd,
		      const uint8_t *in, size_t len, uint8_t *out, size_t *bytes)
{
	memset(out, 0, AECP_FRAME_BYTES - 38u);
	*bytes = len;
	switch (cmd) {
	case 0:
		*bytes = 16u;
		if (len < 16u) {
			return AECP_BAD_ARGUMENTS;
		}
		memcpy(out, in, 16u);
		memset(out + 4, 0, 8u);
		return AECP_NOT_SUPPORTED;
	case 1: return lock(a, in, len, out, bytes);
	case 2:
		*bytes = 20u;
		wire_put_be(out, a->locked ? 2u : 0u, 4);
		wire_put_be(out + 12, a->lock_owner, 8);
		return AECP_SUCCESS;
	case 4: return descriptor(a, in, len, out, bytes);
	case 6: case 7: return configuration(a, cmd == 6u, in, len, out, bytes);
	case 8: case 9: case 20: case 21: case 22: case 23:
		return scalar(a, cmd, in, len, out, bytes);
	case 14: case 15: return stream_info(a, cmd == 14u, in, len, out, bytes);
	case 16: case 17: return names(a, cmd == 16u, in, len, out, bytes);
	case 24: case 25: return control(a, cmd == 24u, in, len, out, bytes);
	case 34: case 35:
		*bytes = 4u;
		if (len < 4u) {
			return AECP_BAD_ARGUMENTS;
		}
		memcpy(out, in, 4u);
		if (wire_be16(in) != 5u) {
			return AECP_NOT_SUPPORTED;
		}
		if (aecp_foreign_lock(a)) {
			return AECP_ENTITY_LOCKED;
		}
		if (aecp_find(a, a->configuration, 5u, (uint16_t)wire_be16(in + 2)) == NULL) {
			return AECP_NO_SUCH_DESCRIPTOR;
		}
		a->start_pending = true;
		a->in_port = true;
		a->ports->start(a->ports->ctx, (uint16_t)wire_be16(in + 2), cmd == 34u);
		a->in_port = false;
		return AECP_SUCCESS;
	case 38:
		*bytes = 4u;
		memcpy(out, in, len < 4u ? len : 4u);
		return AECP_BAD_ARGUMENTS; // IEEE 7.4.39.2: unsolicited-only opcode
	case 39: case 40: return avb(a, cmd == 40u, in, len, out, bytes);
	case 41: return counters(a, in, len, out, bytes);
	case 43: case 44: case 45: return aecp_map_command(a, cmd, in, len, out, bytes);
	case 75: return dynamic(a, interface, in, len, out, bytes);
	default:
		memcpy(out, in, len);
		return AECP_NOT_IMPLEMENTED;
	}
}
