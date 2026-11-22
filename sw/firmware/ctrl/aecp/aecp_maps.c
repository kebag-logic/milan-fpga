// SPDX-License-Identifier: CERN-OHL-W-2.0
// Atomic dynamic map edits and fixed partitions, Milan v1.2 5.4.2.26-.28.
#include "aecp_internal.h"
#include "aecp_state.h"
#define AECP_ENTITY_SHAPE_ONLY // the image's constants, not its tables (aecp_shape.py)
#include "aecp_entity_gen.h"
#include <stddef.h>

static unsigned channels(uint64_t format)
{
	return (format >> 56) == 2u ? (unsigned)((format >> 22) & 1023u) : 0u;
}

// channels() of the big-endian format at p, from the three bytes it reads:
// the first, and the fifth and sixth, which hold the ten bits of the channel
// count. An edit checks each of its mappings' stream formats, so it reads no
// 64-bit word to do it (#665).
static unsigned format_channels(const uint8_t *p)
{
	return p[0] == 2u ? (unsigned)p[4] << 2 | (unsigned)p[5] >> 6 : 0u;
}

bool aecp_maps_allow_format(struct aecp *a, uint16_t type, uint16_t index, uint64_t format)
{
	uint16_t port_type = type == 5u ? 14u : 15u;
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
	// Static AUDIO_MAP descriptors constrain format changes too (Milan 5.4.2.7).
	for (size_t n = 0; n < a->cfg.model->count; ++n) {
		struct aecp_descriptor *port = &a->cfg.model->descriptors[n];
		if (port->configuration != a->configuration || port->type != port_type) continue;
		if (port->length < 20u) return false;
		unsigned count = (unsigned)wire_be16(port->value + 16), base = (unsigned)wire_be16(port->value + 18);
		for (unsigned k = 0; k < count; ++k) {
			if (base + k > UINT16_MAX) return false;
			struct aecp_descriptor *map = aecp_find(a, a->configuration, 23u, (uint16_t)(base + k));
			if (map == NULL || map->length < 8u) return false;
			size_t offset = (size_t)wire_be16(map->value + 4), rows = (size_t)wire_be16(map->value + 6);
			if (offset > map->length || rows * 8u > map->length - offset) return false;
			for (size_t r = 0; r < rows; ++r) {
				const uint8_t *record = map->value + offset + 8u*r;
				if (wire_be16(record) == index && wire_be16(record + 2) >= channels(format)) return false;
			}
		}
	}
	return true;
}

static void encode(uint8_t *p, const struct aecp_mapping *r)
{
	aecp_put16(p, r->stream);
	aecp_put16(p + 2, r->channel);
	aecp_put16(p + 4, r->cluster);
	aecp_put16(p + 6, r->cluster_channel);
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

// Output stream channels have one owner across output ports: a map is
// another's unless it is in another configuration, not an output port's, or
// the port's own.
static bool foreign(const struct aecp *a, const struct aecp_descriptor *port, const struct aecp_map *other)
{
	return !(other->configuration != a->configuration || other->type != 15u || other->index == port->index);
}

// What legal() reads of a port, read once for all of an edit's mappings
// (#665): its streams' descriptor type, its cluster count and its first
// cluster's index.
struct geometry {
	uint16_t streams;
	unsigned clusters;
	unsigned base;
};

static struct geometry geometry(const struct aecp_descriptor *port)
{
	return (struct geometry){port->type == 14u ? 5u : 6u, (unsigned)wire_be16(port->value + 12),
		(unsigned)wire_be16(port->value + 14)};
}

// Every check of a mapping that reads nothing: its stream, stream channel,
// cluster and cluster channel are the port's.
static bool legal(struct aecp *a, const struct geometry *g, const struct aecp_mapping *r)
{
	struct aecp_descriptor *stream = aecp_find(a, a->configuration, g->streams, r->stream);
	if (stream == NULL || stream->length < 82u || r->channel >= format_channels(stream->value + 74)) {
		return false;
	}
	if (r->cluster >= g->clusters || g->base + r->cluster > UINT16_MAX) {
		return false;
	}
	struct aecp_descriptor *cluster = aecp_find(a, a->configuration, 20u, (uint16_t)(g->base + r->cluster));
	return cluster != NULL && cluster->length >= 86u && r->cluster_channel < wire_be16(cluster->value + 84);
}

static bool valid(struct aecp *a, const struct aecp_descriptor *port, const struct aecp_mapping *r)
{
	struct geometry g = geometry(port);
	if (!legal(a, &g, r)) {
		return false;
	}
	for (size_t n = 0; port->type != 14u && n < a->cfg.map_count; ++n) {
		const struct aecp_map *other = &a->cfg.maps[n];
		if (!foreign(a, port, other)) continue;
		for (size_t k = 0; k < other->count; ++k) {
			if (other->rows[k].stream == r->stream && other->rows[k].channel == r->channel) return false;
		}
	}
	return true;
}

// One ADD or REMOVE_AUDIO_MAPPINGS (#904): each mapping decoded once into two
// words, its stream and stream channel and its cluster and cluster channel,
// and held in a table by its key, a slot a key, so the command, its port's map
// and the other output ports' maps are each one pass of lookups (IEEE
// 1722.1-2021 7.4.45, 7.4.46; Milan v1.2 5.4.2.27, 5.4.2.28). Its work is
// bounded for every legal-length edit, refused or not (#894's egress ruling of
// 2026-11-13, item 3): a mapping its port's geometry refuses ends the table,
// as an ADD's earlier conflict does, since its turn refuses the edit at the
// latest; a REMOVE's other values of a held key are linked from the key's
// first, so a lookup visits its key's slot and a map's row its key's mappings,
// never a run of one key's values. A key's slot is its position in the port's
// key domain (#894's ruling of 2026-11-14, item 1): its stream or cluster
// times the most channels a key's stream or cluster has, plus its channel, so
// no two keys share one, at every geometry the builder accepts. The domain is
// the build's shape, which the shape header states in every unit an image
// compiles (srp_entity.py, through aecp_shape.py's key_domain; a host arm given
// none takes aecp_entity_gen.h's, the same derivation): at an output port a
// STREAM_OUTPUT and a channel of a format it advertises, at an input port one
// of its clusters and a channel of it. A mapping is refused at its turn where
// its port's geometry refuses it, as before, and also where its key lies
// outside the domain, which no format or cluster of the build lets a legal
// mapping do; so no key outside it forms an index (the key's words are
// little-endian on every target). The table's declared slots are held, at
// compile time, to every position place() forms, MAP_FIRSTS x MAP_CHANNELS
// (MAP_DOMAIN; the assertion after struct edit). Apart from that, the table
// keeps at least the 256 slots it held before (MAP_FLOOR), a layout choice
// (#909): the edit's stack frame, and the data cache's view of it, stays where
// every measured cost was taken; at 1x1/1if a table of the domain's 64 moves
// the frame 192 B and the largest legal command's record from 91,625 CPU
// cycles to 98,720 (#894).
#define MAP_MOST(x, y) ((x) > (y) ? (x) : (y))
#define MAP_FIRSTS MAP_MOST(AECP_ENTITY_KEY_STREAMS, AECP_ENTITY_KEY_CLUSTERS)
#define MAP_CHANNELS MAP_MOST(AECP_ENTITY_KEY_STREAM_CHANNELS, AECP_ENTITY_KEY_CLUSTER_CHANNELS)
#define MAP_DOMAIN (MAP_FIRSTS * MAP_CHANNELS)
#define MAP_FLOOR 256u
#define MAP_SLOTS MAP_MOST(MAP_DOMAIN, MAP_FLOOR)
#define MAP_IDLE_WORDS MAP_MOST((MAP_FIRSTS + 31u) / 32u, 1u)
_Static_assert(AECP_MAP_PAGE < 256u, "a slot holds a mapping's index plus one");
// The work an edit does, counted where a test asks for it (AECP_MAP_WORK,
// test_aecp.cpp): each slot and each held mapping a lookup visits. No image
// counts it.
#ifdef AECP_MAP_WORK
unsigned aecp_map_work;
#define VISIT() (++aecp_map_work)
#else
#define VISIT() ((void)0)
#endif
// EARLIER: an earlier mapping of its key differs; FOUND: its port's map holds
// it; BARRED: a row it may not join holds its key, another value of it in its
// port's map for an ADD, or any in another output port's map; ILLEGAL: its
// port's geometry refuses it, or its key lies outside the domain.
enum { EARLIER = 1u, FOUND = 2u, BARRED = 4u, ILLEGAL = 8u };
#if defined(__BYTE_ORDER__) && __BYTE_ORDER__ != __ORDER_LITTLE_ENDIAN__
#error "a held mapping's words are its coordinates in little-endian order (place, look)"
#endif
struct edit {
	bool input;
	union held {
		struct aecp_mapping r;
		uint32_t w[2]; // the stream and its channel, then the cluster and its channel
	} rows[AECP_MAP_PAGE];
	uint8_t slot[MAP_SLOTS];       // 0, or one plus a key's first mapping
	uint8_t next[AECP_MAP_PAGE];   // a REMOVE's next mapping of the key with another value, plus one
	uint8_t rep[AECP_MAP_PAGE];    // the first mapping equal to each
	uint8_t flags[AECP_MAP_PAGE];
	uint8_t copies[AECP_MAP_PAGE]; // each distinct mapping's occurrences
	uint32_t idle[MAP_IDLE_WORDS]; // the streams the running check found idle, a bit each (idle)
	size_t from;                   // the rows of its port's map a REMOVE can take (mark), from one
	size_t to;                     // to one past another
};
_Static_assert(sizeof ((struct edit *)0)->slot / sizeof ((struct edit *)0)->slot[0] >= (size_t)MAP_DOMAIN,
	       "the table holds every position place() forms");
#ifdef AECP_MAP_WORK
// Where the work is counted, an edit starts from the table an earlier one
// left (test_aecp.cpp, Core.MapEditWorkReadsOnlyWhatItCleared): each slot
// its first mapping's, each mapping a copy marked EARLIER and linked to the
// one after it, and each row a value no legal mapping holds. A read of
// what an edit did not clear then finds a mapping, refuses one, or walks the
// table up to its end. No image fills it.
static void stale(struct edit *e)
{
	memset(e, 0xff, sizeof *e);
	memset(e->slot, 1, sizeof e->slot);
	for (size_t n = 0; n < AECP_MAP_PAGE; ++n) {
		e->next[n] = n + 2u < AECP_MAP_PAGE ? (uint8_t)(n + 2u) : 0u;
		e->rep[n] = 0u;
		e->flags[n] = EARLIER;
		e->copies[n] = 1u;
	}
	e->from = e->to = 0u;
}
#endif

// What a port's mappings may not share with different values: the cluster
// channel an input port writes, the stream channel an output port reads.
static uint32_t key(bool input, const union held *h)
{
	return h->w[input];
}

static bool same(const union held *x, const union held *y)
{
	return x->w[0] == y->w[0] && x->w[1] == y->w[1];
}

// The slot of x's key, its position in the domain, or MAP_SLOTS for a key
// outside it. The slot holds the key's first mapping, or 0.
static size_t place(const struct edit *e, const union held *x)
{
	uint32_t k = key(e->input, x);
	size_t first = k & 0xFFFFu;
	size_t channel = k >> 16;
	VISIT();
	return first < MAP_FIRSTS && channel < MAP_CHANNELS ? first * MAP_CHANNELS + channel : MAP_SLOTS;
}

// The check a legal mapping of an output port reads its port for, after every
// other of its own: its stream must not be running, observed briefly as a
// running check (#943). Each stream is observed once an edit, at the first of
// its mappings to reach the check, and held idle for the rest (#963): one found
// running or unanswered refuses the edit at that mapping, as before, so a later
// mapping of the stream is only ever checked after it was found idle in the same
// record, which nothing else runs beside. So an edit observes each stream it
// maps once, not each mapping: a REMOVE or ADD of 63 at 8x8/1if's output map
// made 63 observations, most of its pass, which was over THE SHARE. A mapping
// that reaches the check has its key in the domain (place), so its stream is
// below MAP_FIRSTS; one that is not is observed every time, never held.
static bool idle(struct aecp *a, struct edit *e, const struct aecp_descriptor *port, const struct aecp_mapping *r)
{
	if (port->type == 14u) {
		return true;
	}
	const bool held = r->stream < MAP_FIRSTS;
	uint32_t *word = &e->idle[held ? r->stream / 32u : 0u];
	const uint32_t bit = held ? 1u << (r->stream % 32u) : 0u;
	if ((*word & bit) == 0u) {
		struct aecp_stream_info info = {.brief = true};
		if (!aecp_stream_read(a, 6u, r->stream, &info) || info.running) {
			return false;
		}
		*word |= bit;
	}
	return true;
}

// A mapping copied a coordinate at a time. A whole one is a call of memcpy on
// the image, a map's rows being 2-byte aligned, and an edit copies one for
// each row it reads (#894).
static void assign(struct aecp_mapping *to, const struct aecp_mapping *from)
{
	to->stream = from->stream;
	to->channel = from->channel;
	to->cluster = from->cluster;
	to->cluster_channel = from->cluster_channel;
}

// A map's row looked up: each held mapping of its key is marked `match` where
// it equals the row and `other` where it differs. Returns one plus the first
// equal one with an occurrence left, else 0. A row whose key lies outside the
// domain holds no mapping's key.
static size_t look(struct edit *e, const struct aecp_mapping *r, unsigned other, unsigned match)
{
	// the row's words as a held mapping's, in registers, not copied (#894)
	union held x = {.w = {r->stream | (uint32_t)r->channel << 16, r->cluster | (uint32_t)r->cluster_channel << 16}};
	size_t left = 0, s = place(e, &x);
	for (size_t v = s < MAP_SLOTS ? e->slot[s] : 0u; v != 0u; v = e->next[v - 1u]) {
		VISIT();
		bool is = same(&e->rows[v - 1u], &x);
		e->flags[v - 1u] |= (uint8_t)(is ? match : other);
		if (is && left == 0u && e->copies[v - 1u] != 0u) {
			left = v;
		}
	}
	return left;
}

// Each row of a map looked up. The pass that marks its port's own rows FOUND
// holds their reach: from the first equal to a held mapping to one past the
// last (#894). A pass that marks nothing is a REMOVE's: each held mapping
// removes the first rows equal to it, one an occurrence, as each in turn did,
// and the rows kept keep their order. Only a row in the reach can be one, so
// a row before it stays in place and a row after it moves down unread.
static void mark(struct edit *e, struct aecp_map *m, unsigned other, unsigned match)
{
	struct aecp_mapping *rows = m->rows; // read once: a mark's byte stores could alias them
	size_t count = m->count;
	size_t from = count;
	size_t to = 0;
	size_t k = match != 0u ? 0u : e->from;
	size_t kept = k;
	size_t end = match != 0u ? count : e->to;
	for (; k < end; ++k) {
		size_t v = look(e, &rows[k], other, match);
		if (match != 0u) {
			if (v != 0u) {
				from = from == count ? k : from;
				to = k + 1u;
			}
		} else if (v != 0u) {
			--e->copies[v - 1u];
		} else if (kept++ != k) {
			assign(&rows[kept - 1u], &rows[k]); // a row kept in its place is not copied
		}
	}
	if (match == FOUND) {
		e->from = from;
		e->to = to;
	} else if (match == 0u) {
		for (; k < count; ++k) {
			assign(&rows[kept++], &rows[k]);
		}
		m->count = kept;
	}
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
	memset(out, 0, *bytes); // the fixed body; the map rows are written whole (#665)
	if (len < 8u) {
		return AECP_BAD_ARGUMENTS;
	}
	// the descriptor's type and index, and GET_AUDIO_MAP's page, echoed a byte at a time, not by a call (#894)
	for (size_t k = 0; k < (cmd == 43u ? 6u : 4u); ++k) {
		out[k] = in[k];
	}
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
		aecp_put16(out + 6, pages);
		size_t page = (size_t)wire_be16(in + 4), count = 0;
		if (page >= pages) {
			return AECP_BAD_ARGUMENTS;
		}
		for (size_t n = 0; n < m->count; ++n) {
			if (coordinate(a, port, &m->rows[n]) / m->page_channels == page) {
				encode(out + 12u + 8u * count++, &m->rows[n]);
			}
		}
		aecp_put16(out + 8, count);
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
	aecp_put16(out + 4, count);
	memcpy(out + 8, in + 8, count * 8u);
	*bytes = 8u + count * 8u;
	// an edit that is checked costs what its mappings do, so each is paced (THE PACE, aecp_mbx.h)
	a->edited_ms = a->now;
	bool adding = cmd == 44u;
	struct edit e;
#ifdef AECP_MAP_WORK
	stale(&e);
#endif
	// What the edit reads before it writes is cleared, and only that (#894):
	// the slots place() forms, MAP_DOMAIN of them, and the streams found idle
	// (#963), here, and each mapping's link, marks and occurrences at its turn
	// in the table, which no read reaches past.
	memset(e.slot, 0, MAP_DOMAIN);
	memset(e.idle, 0, sizeof e.idle);
	e.input = type == 14u;
	// The mappings in order: the first held equal to each is its own, and a held
	// one of its key that differs is an earlier conflict. A mapping its port's
	// geometry refuses, or whose key is outside the domain, or an ADD's earlier
	// conflict, is refused at its turn at the latest, so the table ends there.
	// The geometry's check comes first, and the key's slot only after it.
	size_t steps = count;
	struct geometry g = geometry(port);
	for (size_t n = 0; n < steps; ++n) {
		uint32_t first = wire_be32(in + 8u + n * 8u), second = wire_be32(in + 12u + n * 8u);
		e.rows[n].r = (struct aecp_mapping){(uint16_t)(first >> 16), (uint16_t)first, (uint16_t)(second >> 16),
			(uint16_t)second};
		e.rep[n] = (uint8_t)n;
		e.next[n] = e.flags[n] = e.copies[n] = 0u;
		size_t s = legal(a, &g, &e.rows[n].r) ? place(&e, &e.rows[n]) : MAP_SLOTS;
		if (s == MAP_SLOTS) {
			e.flags[n] = ILLEGAL;
			steps = n + 1u;
			break;
		}
		uint8_t *at = &e.slot[s];
		if (*at == 0u) {
			*at = (uint8_t)(n + 1u);
		} else if (same(&e.rows[*at - 1u], &e.rows[n])) {
			e.rep[n] = (uint8_t)(*at - 1u);
		} else {
			e.flags[n] = EARLIER;
			if (adding) {
				steps = n + 1u;
				break;
			}
			e.next[n] = e.next[*at - 1u];
			e.next[*at - 1u] = (uint8_t)(n + 1u);
		}
		++e.copies[e.rep[n]];
	}
	for (struct aecp_map *v = a->cfg.maps; v < a->cfg.maps + a->cfg.map_count; ++v) {
		if (v == m) {
			mark(&e, m, adding ? BARRED : 0u, FOUND);
		} else if (!e.input && foreign(a, port, v)) {
			mark(&e, v, BARRED, BARRED);
		}
	}
	// Each mapping's checks in its turn, so the port is read as each was before.
	size_t additions = 0;
	for (size_t n = 0; n < steps; ++n) {
		unsigned held = e.flags[e.rep[n]];
		if ((e.flags[n] & ILLEGAL) != 0u || !idle(a, &e, port, &e.rows[n].r) || (held & BARRED) != 0u ||
		    (adding ? (e.flags[n] & EARLIER) != 0u : (held & FOUND) == 0u)) {
			return AECP_BAD_ARGUMENTS;
		}
		additions += adding && e.rep[n] == n && (held & FOUND) == 0u;
	}
	if (additions > m->capacity - m->count) {
		return AECP_NO_RESOURCES;
	}
	// The mappings that change the map, each once, in command order: an ADD's additions, a REMOVE's every distinct
	// mapping, each held (else it was refused). Nothing reads e.rep after this but the additions, so it takes their
	// positions (#923).
	size_t changes = 0;
	for (size_t n = 0; n < count; ++n) {
		if (e.rep[n] == n && (!adding || (e.flags[n] & FOUND) == 0u)) {
			e.rep[changes++] = (uint8_t)n;
		}
	}
	// The integrator's store takes the edit before the map does, all or none: a refusal there changes nothing here
	// (#923; Milan v1.2 5.4.2.27, 5.4.2.28)
	if (changes != 0u && a->ports->edit != NULL) {
		aecp_port_begin(a);
		unsigned status = a->ports->edit(a->ports->ctx, !adding, type, index, in + 8, e.rep, changes);
		aecp_port_end(a);
		if (status != AECP_SUCCESS) {
			return status;
		}
	}
	size_t was = m->count;
	if (adding) {
		for (size_t k = 0; k < changes; ++k) {
			assign(&m->rows[m->count++], &e.rows[e.rep[k]].r);
		}
	} else {
		mark(&e, m, 0u, 0u);
	}
	if (m->count != was) {
		aecp_note(a, AECP_CHANGE_MAP, type, index);
	}
	return AECP_SUCCESS;
}

unsigned aecp_map_restore(struct aecp *a, struct aecp_map *m, const struct aecp_mapping *rows, size_t count)
{
	if (!aecp_enter(a) || a->open) return AECP_ENTITY_MISBEHAVING;
	struct aecp_descriptor *port = aecp_find(a, m->configuration, m->type, m->index);
	if (port == NULL || port->length < 20u || m->configuration != a->configuration)
		return AECP_ENTITY_MISBEHAVING;
	if (wire_be16(port->value + 16) != 0u || count > m->capacity) return AECP_BAD_ARGUMENTS;
	for (size_t n = 0; n < count; ++n) {
		if (!valid(a, port, &rows[n])) return AECP_BAD_ARGUMENTS;
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
	if (!aecp_enter(a) || a->open) return AECP_ENTITY_MISBEHAVING;
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

// A reset-set row the restored formats keep, as aecp_restore_settle and the datapath's boot clip keep it.
static bool kept(struct aecp *a, const struct aecp_map *m, const struct aecp_mapping *r)
{
	struct aecp_descriptor *d = aecp_find(a, a->configuration, m->type == 14u ? 5u : 6u, r->stream);
	return d != NULL && d->length >= 82u && r->channel < channels(wire_be64(d->value + 74));
}

// Whether a port's map is its reset set as the store holds it, row for row.
static bool unmoved(struct aecp *a, const struct aecp_map *m)
{
	size_t k = 0;
	for (size_t n = 0; n < m->default_count; ++n) {
		if (!kept(a, m, &m->defaults[n])) {
			continue;
		}
		if (k == m->count || !equal(&m->rows[k], &m->defaults[n])) {
			return false;
		}
		++k;
	}
	return k == m->count;
}

// A port's reset set the store holds (held), or none, as its map.
static void reset(struct aecp *a, struct aecp_map *m, bool held)
{
	m->count = 0;
	for (size_t n = 0; held && n < m->default_count; ++n) {
		if (kept(a, m, &m->defaults[n])) {
			m->rows[m->count++] = m->defaults[n];
		}
	}
}

// One port's reset set as the store holds it (defaults) or its map through the edit port, its records in the
// response buffer, which nothing holds before AECP opens: a set of at most a page's mappings fits it.
_Static_assert(AECP_MAP_PAGE * 8u <= AECP_FRAME_BYTES, "a page of mappings fits the response buffer");
static unsigned commit(struct aecp *a, const struct aecp_map *m, bool remove, bool defaults)
{
	if (m->capacity > AECP_MAP_PAGE) {
		return AECP_ENTITY_MISBEHAVING;
	}
	size_t count = 0;
	for (size_t n = 0; n < (defaults ? m->default_count : m->count); ++n) {
		const struct aecp_mapping *r = defaults ? &m->defaults[n] : &m->rows[n];
		if (!defaults || kept(a, m, r)) {
			encode(a->response + 8u * count++, r);
		}
	}
	unsigned status = AECP_SUCCESS;
	if (count != 0u) {
		aecp_port_begin(a);
		status = a->ports->edit(a->ports->ctx, remove, m->type, m->index, a->response, NULL, count);
		aecp_port_end(a);
	}
	return status;
}

void aecp_restore_commit(struct aecp *a)
{
	if (!aecp_enter(a) || a->open || a->ports->edit == NULL) return;
	struct aecp_map *end = a->cfg.maps + a->cfg.map_count;
	for (struct aecp_map *m = a->cfg.maps; m < end; ++m) {
		if (m->configuration == a->configuration && !unmoved(a, m) && commit(a, m, true, true) != AECP_SUCCESS) {
			reset(a, m, true);
		}
	}
	for (struct aecp_map *m = a->cfg.maps; m < end; ++m) {
		if (m->configuration == a->configuration && !unmoved(a, m) && commit(a, m, false, false) != AECP_SUCCESS) {
			reset(a, m, commit(a, m, false, true) == AECP_SUCCESS);
		}
	}
}

void aecp_map_refused(struct aecp *a, const struct aecp_map *m)
{
	if (!aecp_enter(a)) return;
	struct aecp_descriptor *d = aecp_find(a, m->configuration, m->type, m->index);
	if (!a->open && d != NULL) aecp_override(a, d, 4u);
}
