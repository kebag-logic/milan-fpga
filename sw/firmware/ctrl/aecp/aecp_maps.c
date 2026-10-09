// SPDX-License-Identifier: CERN-OHL-W-2.0
// Atomic dynamic map edits and fixed partitions, Milan v1.2 5.4.2.26-.28.
#include "aecp_internal.h"
#include "aecp_state.h"

static unsigned channels(uint64_t format)
{
	return (format >> 56) == 2u ? (unsigned)((format >> 22) & 1023u) : 0u;
}

bool aecp_maps_allow_format(struct aecp *a, uint16_t type, uint16_t index, uint64_t format)
{
	for (size_t n = 0; n < a->cfg.map_count; ++n) {
		const struct aecp_map *m = &a->cfg.maps[n];
		if (m->configuration != a->configuration || m->type != (type == 5u ? 14u : 15u)) {
			continue;
		}
		for (size_t k = 0; k < m->count; ++k) {
			if (m->rows[k].stream == index && m->rows[k].channel >= channels(format)) {
				return false;
			}
		}
	}
	return true;
}

static struct aecp_mapping decode(const uint8_t *p)
{
	return (struct aecp_mapping){(uint16_t)wire_be16(p), (uint16_t)wire_be16(p + 2),
		(uint16_t)wire_be16(p + 4), (uint16_t)wire_be16(p + 6)};
}

static void encode(uint8_t *p, const struct aecp_mapping *r)
{
	wire_put_be(p, r->stream, 2);
	wire_put_be(p + 2, r->channel, 2);
	wire_put_be(p + 4, r->cluster, 2);
	wire_put_be(p + 6, r->cluster_channel, 2);
}

static bool equal(const struct aecp_mapping *a, const struct aecp_mapping *b)
{
	return a->stream == b->stream && a->channel == b->channel &&
	       a->cluster == b->cluster && a->cluster_channel == b->cluster_channel;
}

static bool conflict(bool input, const struct aecp_mapping *a, const struct aecp_mapping *b)
{
	bool same = input ? (a->cluster == b->cluster && a->cluster_channel == b->cluster_channel) :
		(a->stream == b->stream && a->channel == b->channel);
	return same && !equal(a, b);
}

static size_t position(const struct aecp_map *m, const struct aecp_mapping *r)
{
	for (size_t n = 0; n < m->count; ++n) {
		if (equal(&m->rows[n], r)) {
			return n;
		}
	}
	return m->count;
}

static bool valid(struct aecp *a, const struct aecp_descriptor *port, const struct aecp_mapping *r, bool live)
{
	uint16_t type = port->type == 14u ? 5u : 6u;
	struct aecp_descriptor *stream = aecp_find(a, a->configuration, type, r->stream);
	if (stream == NULL || stream->length < 82u || r->channel >= channels(wire_be64(stream->value + 74))) {
		return false;
	}
	unsigned ncluster = (unsigned)wire_be16(port->value + 12);
	unsigned base = (unsigned)wire_be16(port->value + 14);
	if (r->cluster >= ncluster || base + r->cluster > UINT16_MAX) {
		return false;
	}
	struct aecp_descriptor *cluster = aecp_find(a, a->configuration, 20u, (uint16_t)(base + r->cluster));
	if (cluster == NULL || cluster->length < 86u || r->cluster_channel >= wire_be16(cluster->value + 84)) {
		return false;
	}
	if (type == 6u && live) {
		struct aecp_stream_info info;
		if (!aecp_stream_read(a, type, r->stream, &info) || info.running) {
			return false;
		}
	}
	return true;
}

// Partition maxima come from the advertised format lists, never the current
// format or current map. A SET cannot silently repartition GET_AUDIO_MAP.
static size_t stream_width(const struct aecp_descriptor *d)
{
	if (d->length < 86u) {
		return 0;
	}
	size_t start = (size_t)wire_be16(d->defaults + 82), count = (size_t)wire_be16(d->defaults + 84);
	if (start > d->length || 8u * count > d->length - start) {
		return 0;
	}
	size_t width = 0;
	for (size_t n = 0; n < count; ++n) {
		size_t v = channels(wire_be64(d->defaults + start + 8u * n));
		if (v > width) {
			width = v;
		}
	}
	return width;
}

static size_t coordinate(struct aecp *a, const struct aecp_descriptor *port, const struct aecp_mapping *r)
{
	size_t value = port->type == 14u ? r->cluster_channel : r->channel;
	if (port->type == 14u) {
		unsigned base = (unsigned)wire_be16(port->value + 14);
		for (unsigned n = 0; n < r->cluster; ++n) {
			struct aecp_descriptor *d = aecp_find(a, a->configuration, 20u, (uint16_t)(base + n));
			if (d != NULL && d->length >= 86u) {
				value += (size_t)wire_be16(d->defaults + 84);
			}
		}
	} else {
		for (size_t n = 0; n < a->cfg.model->count; ++n) {
			struct aecp_descriptor *d = &a->cfg.model->descriptors[n];
			if (d->configuration == a->configuration && d->type == 6u && d->index < r->stream) {
				value += stream_width(d);
			}
		}
	}
	return value;
}

unsigned aecp_map_command(struct aecp *a, uint16_t cmd, const uint8_t *in, size_t len,
			  uint8_t *out, size_t *bytes)
{
	*bytes = cmd == 43u ? 12u : 8u;
	if (len < 8u) {
		return AECP_BAD_ARGUMENTS;
	}
	memcpy(out, in, cmd == 43u ? 6u : 4u);
	uint16_t type = (uint16_t)wire_be16(in), index = (uint16_t)wire_be16(in + 2);
	if (type != 14u && type != 15u) {
		return AECP_NOT_SUPPORTED;
	}
	struct aecp_descriptor *port = aecp_find(a, a->configuration, type, index);
	if (port == NULL) {
		return AECP_NO_SUCH_DESCRIPTOR;
	}
	if (port->length < 20u) {
		return AECP_ENTITY_MISBEHAVING;
	}
	if (wire_be16(port->value + 16) != 0u) {
		return AECP_NOT_SUPPORTED;
	}
	struct aecp_map *m = NULL;
	for (size_t n = 0; n < a->cfg.map_count; ++n) {
		struct aecp_map *v = &a->cfg.maps[n];
		if (v->configuration == a->configuration && v->type == type && v->index == index) {
			m = v;
			break;
		}
	}
	if (m == NULL || m->page_channels == 0u || m->page_channels > AECP_MAP_PAGE) {
		return AECP_ENTITY_MISBEHAVING;
	}
	if (cmd == 43u) {
		struct aecp_mapping end = {UINT16_MAX, 0, (uint16_t)wire_be16(port->value + 12), 0};
		size_t width = coordinate(a, port, &end);
		size_t pages = (width + m->page_channels - 1u) / m->page_channels;
		// A zero-cluster model port still has an enumerable empty partition.
		if (pages == 0u) {
			pages = 1u;
		}
		wire_put_be(out + 6, pages, 2);
		size_t page = (size_t)wire_be16(in + 4), count = 0;
		if (page >= pages) {
			return AECP_BAD_ARGUMENTS;
		}
		for (size_t n = 0; n < m->count; ++n) {
			if (coordinate(a, port, &m->rows[n]) / m->page_channels == page) {
				encode(out + 12u + 8u * count++, &m->rows[n]);
			}
		}
		wire_put_be(out + 8, count, 2);
		*bytes += count * 8u;
		return AECP_SUCCESS;
	}
	if (aecp_foreign_lock(a)) {
		return AECP_ENTITY_LOCKED;
	}
	size_t count = (size_t)wire_be16(in + 4);
	if (count > AECP_MAP_PAGE || count * 8u > len - 8u) {
		return AECP_BAD_ARGUMENTS;
	}
	wire_put_be(out + 4, count, 2);
	memcpy(out + 8, in + 8, count * 8u);
	*bytes = 8u + count * 8u;
	size_t additions = 0;
	for (size_t n = 0; n < count; ++n) {
		struct aecp_mapping r = decode(in + 8u + n * 8u);
		if (!valid(a, port, &r, true)) {
			return AECP_BAD_ARGUMENTS;
		}
		bool duplicate = false;
		for (size_t k = 0; k < n; ++k) {
			struct aecp_mapping earlier = decode(in + 8u + k * 8u);
			if (cmd == 44u && conflict(type == 14u, &r, &earlier)) {
				return AECP_BAD_ARGUMENTS;
			}
			duplicate |= equal(&r, &earlier);
		}
		size_t found = position(m, &r);
		if (cmd == 45u && found == m->count) {
			return AECP_BAD_ARGUMENTS;
		}
		if (cmd == 44u) {
			for (size_t k = 0; k < m->count; ++k) {
				if (conflict(type == 14u, &r, &m->rows[k])) {
					return AECP_BAD_ARGUMENTS;
				}
			}
			additions += !duplicate && found == m->count;
		}
	}
	if (additions > m->capacity - m->count) {
		return AECP_NO_RESOURCES;
	}
	bool changed = false;
	for (size_t n = 0; n < count; ++n) {
		struct aecp_mapping r = decode(in + 8u + n * 8u);
		size_t found = position(m, &r);
		if (cmd == 44u && found == m->count) {
			m->rows[m->count++] = r;
			changed = true;
		} else if (cmd == 45u && found < m->count) {
			memmove(m->rows + found, m->rows + found + 1u, (m->count - found - 1u) * sizeof *m->rows);
			--m->count;
			changed = true;
		}
	}
	if (changed) {
		aecp_note(a, AECP_CHANGE_MAP, type, index);
	}
	return AECP_SUCCESS;
}

unsigned aecp_map_restore(struct aecp *a, struct aecp_map *m, const struct aecp_mapping *rows, size_t count)
{
	if (a->open || a->in_port) return AECP_ENTITY_MISBEHAVING;
	struct aecp_descriptor *port = aecp_find(a, m->configuration, m->type, m->index);
	if (port == NULL || port->length < 20u || m->configuration != a->configuration)
		return AECP_ENTITY_MISBEHAVING;
	if (wire_be16(port->value + 16) != 0u || count > m->capacity) return AECP_BAD_ARGUMENTS;
	for (size_t n = 0; n < count; ++n) {
		if (!valid(a, port, &rows[n], false)) return AECP_BAD_ARGUMENTS;
		for (size_t k = 0; k < n; ++k) {
			if (conflict(m->type == 14u, &rows[n], &rows[k])) return AECP_BAD_ARGUMENTS;
		}
	}
	// No mutation before every row passes. Repeated identical mappings are a set.
	m->count = 0;
	for (size_t n = 0; n < count; ++n) {
		if (position(m, &rows[n]) == m->count) m->rows[m->count++] = rows[n];
	}
	a->cfg.events[(size_t)(port - a->cfg.model->descriptors)].overrides &= (uint8_t)~4u;
	return AECP_SUCCESS;
}

unsigned aecp_restore_settle(struct aecp *a)
{
	if (a->open || a->in_port) return AECP_ENTITY_MISBEHAVING;
	// Boot-only clipping (#658): accepted map records were already checked
	// against restored formats. Any remaining orphan belongs to a reset set.
	for (size_t n = 0; n < a->cfg.map_count; ++n) {
		struct aecp_map *m = &a->cfg.maps[n];
		if (m->configuration != a->configuration) continue;
		struct aecp_descriptor *port = aecp_find(a, m->configuration, m->type, m->index);
		if (port == NULL) return AECP_ENTITY_MISBEHAVING;
		if (aecp_overridden(a, port, 4u)) {
			// A refused saved set retains the reset set and reverts formats
			// it would orphan (materialization 8.4). Absent map records use
			// the distinct #658 default-clip rule below.
			for (size_t k = 0; k < m->default_count; ++k) {
				const struct aecp_mapping *r = &m->defaults[k];
				struct aecp_descriptor *d = aecp_find(a, a->configuration,
					m->type == 14u ? 5u : 6u, r->stream);
				if (d == NULL || d->length < 82u) return AECP_ENTITY_MISBEHAVING;
				if (r->channel >= channels(wire_be64(d->value + 74))) {
					memcpy(d->value + 74, d->defaults + 74, 8);
					a->cfg.events[(size_t)(d - a->cfg.model->descriptors)].overrides &= (uint8_t)~1u;
				}
			}
			m->count = m->default_count;
			for (size_t k = 0; k < m->count; ++k) m->rows[k] = m->defaults[k];
		}
		for (size_t k = 0; k < m->count;) {
			struct aecp_descriptor *d = aecp_find(a, a->configuration,
				m->type == 14u ? 5u : 6u, m->rows[k].stream);
			if (d == NULL || d->length < 82u) return AECP_ENTITY_MISBEHAVING;
			if (m->rows[k].channel >= channels(wire_be64(d->value + 74))) {
				memmove(m->rows + k, m->rows + k + 1u, (m->count - k - 1u) * sizeof *m->rows);
				--m->count;
			} else ++k;
		}
	}
	return AECP_SUCCESS;
}

void aecp_map_refused(struct aecp *a, const struct aecp_map *m)
{
	struct aecp_descriptor *d = aecp_find(a, m->configuration, m->type, m->index);
	if (!a->open && !a->in_port && d != NULL) aecp_override(a, d, 4u);
}
