"""notice_cut.py TREE: attempt 2's notice cut, into TREE (scratch writer of the committed change).
aecp.c's fan_out: a recipient's frame takes its interface's source MAC only where its buffer holds another interface's;
the port's calls and context and a registration's sequence_id are read once. The plants that anchor on the changed
lines are re-anchored to the same defect: aecp_fan_mutants.py's notice-source-of-the-first-interface and
notice-sequence-low-byte-unwritten, and poll_items.py's FAN_NOW (the walk notice-fan-out-as-it-was replaces, now from the read-once lines)."""
import sys
from pathlib import Path
T = Path(sys.argv[1])


def edit(path, reps):
    p = T / path; t = p.read_text()
    for a, b in reps:
        assert t.count(a) == 1, (path, a[:60])
        t = t.replace(a, b)
    p.write_text(t)


aecp = (T / 'sw/firmware/ctrl/aecp/aecp.c').read_text()
old_addr = aecp[aecp.index("// A recipient's fields of a notice's frame (Milan v1.2 5.4.5.1"):
                aecp.index("// A notice to every recipient from a->recipient on")]
new_addr = """// A recipient's fields of a notice's frame (Milan v1.2 5.4.5.1; IEEE 1722.1-2021 7.5.2, 9.2.1.1): its MAC as the
// destination, its entity ID as the controller_entity_id and its sequence_id, each byte stored once from the words
// that hold it, each read before the stores, which could alias it (#665: through the put helpers' calls these were a
// third of a recipient's cost).
static inline void address(uint8_t *f, const struct aecp_registration *r)
{
	const uint32_t mac_hi = (uint32_t)(r->mac >> 32), mac_lo = (uint32_t)r->mac;
	const uint32_t id_hi = (uint32_t)(r->controller >> 32), id_lo = (uint32_t)r->controller;
	const uint16_t sequence = r->sequence;
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
	f[34] = (uint8_t)(sequence >> 8);
	f[35] = (uint8_t)sequence;
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
edit('sw/firmware/ctrl/aecp/aecp.c', [
    (old_addr, new_addr),
    ("""	unsigned k = *at;
	while (!owed && k < total) {""",
     """	// the port's calls and context, read once for the walk: a frame's byte stores could alias them (#665)
	void *const ctx = a->ports->ctx;
	enum aecp_fan (*const fan_to)(void *, unsigned, const uint8_t *, size_t) = a->ports->fan;
	bool (*const send)(void *, unsigned, const uint8_t *, size_t, uint32_t) = a->ports->send;
	unsigned frame_if = ~0u, other_if = ~0u; // the interface whose MAC each buffer's source holds, none at first
	unsigned k = *at;
	while (!owed && k < total) {"""),
    ("""			address(frame, r, a->cfg.mac[i]);
			const enum aecp_fan taken = fan ? a->ports->fan(a->ports->ctx, i, frame, bytes) :
				a->ports->send(a->ports->ctx, i, frame, bytes, a->tx_cookie) ? AECP_FAN_TAKEN : AECP_FAN_REFUSED;""",
     """			if (frame_if != i) {
				source(frame, a->cfg.mac[i]);
				frame_if = i;
			}
			address(frame, r);
			const enum aecp_fan taken = fan ? fan_to(ctx, i, frame, bytes) :
				send(ctx, i, frame, bytes, a->tx_cookie) ? AECP_FAN_TAKEN : AECP_FAN_REFUSED;"""),
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
])
edit('sw/firmware/ctrl/test/aecp_fan_mutants.py', [
    ("""     'address(frame, r, a->cfg.mac[i]);',
     'address(frame, r, a->cfg.mac[0]);',""",
     """     'source(frame, a->cfg.mac[i]);',
     'source(frame, a->cfg.mac[0]);',"""),
    ("""     '\\tf[35] = (uint8_t)r->sequence;\\n',""", """     '\\tf[35] = (uint8_t)sequence;\\n',"""),
])
src = (T / 'sw/firmware/ctrl/aecp/aecp.c').read_text()
a = src.index("\t// the port's calls and context, read once")
b = src.index('\tif (fan) {\n\t\t// a queue with no room', a)
lines = src[a:b].splitlines(keepends=True)
def pieces(line):
    out = []
    while len(repr(line)) > 104:
        cut = line.rfind(' ', 0, 90) + 1 or 90
        out.append(line[:cut]); line = line[cut:]
    return out + [line]
lit = 'FAN_NOW = (' + '\n           '.join(repr(x) for l in lines for x in pieces(l)) + ')\n'
q = T / 'tb/verilator/ctrl_service_budget/poll_items.py'; u = q.read_text()
i = u.index('FAN_NOW = ('); j = u.index('#: The walk as it was before the cut', i)
q.write_text(u[:i] + lit + u[j:])
print('notice cut written; FAN_NOW', len(lines), 'lines')
