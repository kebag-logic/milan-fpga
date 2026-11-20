"""fanaddr.py TREE: attempt 2's notice cut in TREE's aecp.c: a fan-out recipient's frame takes its interface's source
MAC only where its buffer holds another interface's. Scratch writer of the committed change."""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / 'sw/firmware/ctrl/aecp/aecp.c'; t = p.read_text()
old_addr = t[t.index("// A recipient's fields of a notice's frame (Milan v1.2 5.4.5.1"):t.index("// A notice to every recipient from a->recipient on")]
new_addr = """// A recipient's fields of a notice's frame (Milan v1.2 5.4.5.1; IEEE 1722.1-2021 7.5.2, 9.2.1.1): its MAC as the
// destination, its entity ID as the controller_entity_id and its sequence_id, each byte stored once from the two words
// that hold it (#665: through the put helpers' calls these were a third of a recipient's cost).
static inline void address(uint8_t *f, const struct aecp_registration *r)
{
	const uint32_t mac_hi = (uint32_t)(r->mac >> 32), mac_lo = (uint32_t)r->mac;
	const uint32_t id_hi = (uint32_t)(r->controller >> 32), id_lo = (uint32_t)r->controller;
	f[0] = (uint8_t)(mac_hi >> 8);
	f[1] = (uint8_t)mac_hi;
	f[2] = (uint8_t)(mac_lo >> 24);
	f[3] = (uint8_t)(mac_lo >> 16);
	f[4] = (uint8_t)(mac_lo >> 8);
	f[5] = (uint8_t)mac_lo;
	f[26] = (uint8_t)(id_hi >> 24);
	f[27] = (uint8_t)(id_hi >> 16);
	f[28] = (uint8_t)(id_hi >> 8);
	f[29] = (uint8_t)id_hi;
	f[30] = (uint8_t)(id_lo >> 24);
	f[31] = (uint8_t)(id_lo >> 16);
	f[32] = (uint8_t)(id_lo >> 8);
	f[33] = (uint8_t)id_lo;
	f[34] = (uint8_t)(r->sequence >> 8);
	f[35] = (uint8_t)r->sequence;
}

// A notice's frame's source, its interface's MAC (IEEE 1722.1-2021 9.2.1.1). A buffer keeps it from one recipient to
// the next, so a walk stores it only where the buffer last held another interface's (#665: every recipient paid for
// it).
static inline void source(uint8_t *f, uint64_t mac)
{
	const uint32_t hi = (uint32_t)(mac >> 32), lo = (uint32_t)mac;
	f[6] = (uint8_t)(hi >> 8);
	f[7] = (uint8_t)hi;
	f[8] = (uint8_t)(lo >> 24);
	f[9] = (uint8_t)(lo >> 16);
	f[10] = (uint8_t)(lo >> 8);
	f[11] = (uint8_t)lo;
}

"""
t = t.replace(old_addr, new_addr)
reps = [
("""	unsigned held = 0; // the recipient of the frame the fan port holds uncommitted, and its registration
	struct aecp_registration *held_r = NULL;
""",
"""	unsigned held = 0; // the recipient of the frame the fan port holds uncommitted, and its registration
	struct aecp_registration *held_r = NULL;
	unsigned frame_if = ~0u, other_if = ~0u; // the interface whose MAC each buffer's source holds, none at first
"""),
("""			address(frame, r, a->cfg.mac[i]);
""",
"""			if (frame_if != i) {
				source(frame, a->cfg.mac[i]);
				frame_if = i;
			}
			address(frame, r);
"""),
("""				uint8_t *next = other;
				other = frame;
				frame = next;
""",
"""				uint8_t *next = other;
				other = frame;
				frame = next;
				const unsigned next_if = other_if;
				other_if = frame_if;
				frame_if = next_if;
"""),
]
for a, b in reps:
    assert t.count(a) == 1, a[:50]
    t = t.replace(a, b)
p.write_text(t)
print('written')

m = Path(sys.argv[1]) / 'sw/firmware/ctrl/test/aecp_fan_mutants.py'; u = m.read_text()
a = """     'address(frame, r, a->cfg.mac[i]);',
     'address(frame, r, a->cfg.mac[0]);',"""
b = """     'source(frame, a->cfg.mac[i]);',
     'source(frame, a->cfg.mac[0]);',"""
assert u.count(a) == 1
m.write_text(u.replace(a, b))
print('mutant re-anchored')

p = Path(sys.argv[1]) / 'sw/firmware/ctrl/aecp/aecp.c'; t = p.read_text()
reps = [
("""	const uint32_t id_hi = (uint32_t)(r->controller >> 32), id_lo = (uint32_t)r->controller;
	f[0] = (uint8_t)(mac_hi >> 8);""",
 """	const uint32_t id_hi = (uint32_t)(r->controller >> 32), id_lo = (uint32_t)r->controller;
	const uint16_t sequence = r->sequence; // read once: the byte stores could alias it
	f[0] = (uint8_t)(mac_hi >> 8);"""),
("""	f[34] = (uint8_t)(r->sequence >> 8);
	f[35] = (uint8_t)r->sequence;
}""",
 """	f[34] = (uint8_t)(sequence >> 8);
	f[35] = (uint8_t)sequence;
}"""),
("""	unsigned frame_if = ~0u, other_if = ~0u; // the interface whose MAC each buffer's source holds, none at first
""",
 """	unsigned frame_if = ~0u, other_if = ~0u; // the interface whose MAC each buffer's source holds, none at first
	// the port's calls and context, read once for the walk: a frame's byte stores could alias them (#665)
	void *const ctx = a->ports->ctx;
	enum aecp_fan (*const fan_to)(void *, unsigned, const uint8_t *, size_t) = a->ports->fan;
	bool (*const send)(void *, unsigned, const uint8_t *, size_t, uint32_t) = a->ports->send;
"""),
("""			const enum aecp_fan taken = fan ? a->ports->fan(a->ports->ctx, i, frame, bytes) :
				a->ports->send(a->ports->ctx, i, frame, bytes, a->tx_cookie) ? AECP_FAN_TAKEN : AECP_FAN_REFUSED;""",
 """			const enum aecp_fan taken = fan ? fan_to(ctx, i, frame, bytes) :
				send(ctx, i, frame, bytes, a->tx_cookie) ? AECP_FAN_TAKEN : AECP_FAN_REFUSED;"""),
]
for a, b in reps:
    assert t.count(a) == 1, a[:50]
    t = t.replace(a, b)
p.write_text(t)
print('hoisted')

m = Path(sys.argv[1]) / 'sw/firmware/ctrl/test/aecp_fan_mutants.py'; u = m.read_text()
a = "     '\\tf[35] = (uint8_t)r->sequence;\\n',"
b = "     '\\tf[35] = (uint8_t)sequence;\\n',"
assert u.count(a) == 1, a
m.write_text(u.replace(a, b))
print('sequence mutant re-anchored')

# the harness's notice-fan-out-as-it-was plant: FAN_NOW is today's walk, from `unsigned k = *at;` to the walk's end
src = (Path(sys.argv[1]) / 'sw/firmware/ctrl/aecp/aecp.c').read_text()
a = src.index('\tunsigned k = *at;\n\t// the port')
b = src.index('\tif (fan) {\n\t\t// a queue with no room', a)
walk = src[a:b]
lines = walk.splitlines(keepends=True)
lit = 'FAN_NOW = (' + ('\n           '.join(repr(l) for l in lines)) + ')\n'
q = Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget/poll_items.py'; u = q.read_text()
i = u.index('FAN_NOW = (')
j = u.index('#: The walk as it was before the cut', i)
u = u[:i] + lit + u[j:]
q.write_text(u)
print('FAN_NOW re-anchored,', len(lines), 'lines')
