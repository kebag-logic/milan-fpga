"""cut1.py CLONE [--sum]: the work cut on the largest legal AECP record's path, into CLONE's aecp_maps.c. Scratch."""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / 'sw/firmware/ctrl/aecp/aecp_maps.c'
t = p.read_text()
rep = [
("""static unsigned channels(uint64_t format)
{
	return (format >> 56) == 2u ? (unsigned)((format >> 22) & 1023u) : 0u;
}
""",
"""static unsigned channels(uint64_t format)
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
"""),
("""// Every check of a mapping that reads nothing: its stream, stream channel,
// cluster and cluster channel are the port's.
static bool legal(struct aecp *a, const struct aecp_descriptor *port, const struct aecp_mapping *r)
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
	return cluster != NULL && cluster->length >= 86u && r->cluster_channel < wire_be16(cluster->value + 84);
}
""",
"""// What legal() reads of a port, read once for all of an edit's mappings
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
	return cluster != NULL && cluster->length >= 86u && r->cluster_channel < CLUSTER_CHANNELS(cluster);
}
"""),
("""static bool valid(struct aecp *a, const struct aecp_descriptor *port, const struct aecp_mapping *r)
{
	if (!legal(a, port, r)) {""",
"""static bool valid(struct aecp *a, const struct aecp_descriptor *port, const struct aecp_mapping *r)
{
	struct geometry g = geometry(port);
	if (!legal(a, &g, r)) {"""),
("""	size_t steps = count;
	for (size_t n = 0; n < steps; ++n) {""",
"""	size_t steps = count;
	struct geometry g = geometry(port);
	for (size_t n = 0; n < steps; ++n) {"""),
("""		size_t s = legal(a, port, &e.rows[n].r) ? place(&e, &e.rows[n]) : MAP_SLOTS;""",
 """		size_t s = legal(a, &g, &e.rows[n].r) ? place(&e, &e.rows[n]) : MAP_SLOTS;"""),
]
SUM = '--sum' in sys.argv
if SUM:
    rep[1] = (rep[1][0], rep[1][1].replace('CLUSTER_CHANNELS(cluster)', 'be16(cluster->value + 84)'))
    rep[0] = (rep[0][0], rep[0][1] + """
// A big-endian 16-bit field, as wire_be16 reads it. Written as a sum, the
// compiler keeps its two byte loads: written as an OR, it forms the byte-swapped
// halfword and swaps it back, ten instructions on this hart for five. An edit
// reads four for each of its mappings and one for each mapping's cluster (#665).
static unsigned be16(const uint8_t *p)
{
	return p[0] * 256u + p[1];
}
""")
    rep.append(("""		uint32_t first = wire_be32(in + 8u + n * 8u), second = wire_be32(in + 12u + n * 8u);
		e.rows[n].r = (struct aecp_mapping){(uint16_t)(first >> 16), (uint16_t)first, (uint16_t)(second >> 16),
			(uint16_t)second};""",
"""		const uint8_t *p = in + 8u + n * 8u; // its stream, stream channel, cluster and cluster channel
		e.rows[n].r = (struct aecp_mapping){(uint16_t)be16(p), (uint16_t)be16(p + 2), (uint16_t)be16(p + 4),
			(uint16_t)be16(p + 6)};"""))
else:
    rep[1] = (rep[1][0], rep[1][1].replace('CLUSTER_CHANNELS(cluster)', 'wire_be16(cluster->value + 84)'))
for a, b in rep:
    assert t.count(a) == 1, a[:60]
    t = t.replace(a, b)
p.write_text(t)
print('cut written', 'with sums' if SUM else '')
