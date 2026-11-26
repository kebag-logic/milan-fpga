#!/bin/sh
# Differential check of draw_model.py against the code at the reviewed head.
# Builds the stack core's real adp.c with a seed port whose body is the adapter's
# port_seed and mix, copied byte for byte out of sw/firmware/ctrl/adp/adp_mbx.c
# by sed (only the instance() lookup is replaced by a fixed entity), then prints
# the first draw of 4096 (mac, entity_id, sample, interface, kind) tuples; the
# Python model must print the same lines.
# Usage: draw_diff.sh <clone> <work dir>   (exit 0 when the outputs are identical)
set -eu
CLONE=$1
WORK=$2
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$WORK"
SRC=$CLONE/sw/firmware/ctrl/adp/adp_mbx.c
{
	printf '#include <stdint.h>\n#include <stdbool.h>\n#include <stdio.h>\n#include <string.h>\n#include "adp.h"\n'
	printf 'typedef uint32_t (*adp_mbx_clock_fn)(void *ctx);\nstatic struct adp_entity ent;\nstatic uint32_t clk;\n'
	printf 'static uint32_t clock_read(void *c) { (void)c; return clk; }\n'
	printf 'static uint32_t mbx_now_ms(void) { return 0; }\n'
	# the statics, mix() and port_seed() as they are at the head
	sed -n '/^static adp_mbx_clock_fn clock_fn;/,/^}$/p' "$SRC" | sed -n '1,3p'
	sed -n '/^static uint32_t mix(uint32_t x)/,/^}$/p' "$SRC"
	sed -n '/^static uint32_t port_seed(void \*ctx)/,/^}$/p' "$SRC" |
		sed 's/instance(ctx, seed_interface)->adp.entity/(\&ent); (void)ctx/'
	cat <<'EOF'
static void p_start(void *c, unsigned i, uint32_t d) { (void)c; (void)i; (void)d; }
static void p_stop(void *c, unsigned i) { (void)c; (void)i; }
static bool p_send(void *c, unsigned i, const uint8_t *f, size_t l) { (void)c; (void)i; (void)f; (void)l; return true; }
static void p_gptp(void *c, unsigned i, uint64_t *g, uint8_t *d) { (void)c; (void)i; *g = 0; *d = 0; }
static bool link;
static bool p_link(void *c, unsigned i) { (void)c; (void)i; return link; }
int main(void)
{
	struct adp_ports ports = {NULL, p_send, p_start, p_stop, p_gptp, p_link, port_seed};
	clock_fn = clock_read;
	uint64_t mac = 0x001B21A40000ull;
	for (unsigned k = 0; k < 4096u; ++k) {
		ent.mac = mac + k * 7u;
		ent.entity_id = ((ent.mac >> 24) << 40) | (0xFFFEull << 24) | (ent.mac & 0xFFFFFFu);
		clk = 1853117u + k * 131u;
		seed_interface = k & 1u;
		link = (k & 2u) != 0u;
		struct adp a;
		adp_init(&a, &ent, &ports, seed_interface, 0);
		adp_set_enable(&a, true);
		if (!link) {
			adp_link_change(&a, true);
		}
		printf("%u %u %u\n", k, (unsigned)a.last_draw, (unsigned)a.last_draw_ms);
	}
	return 0;
}
EOF
} > "$WORK/draw_diff.c"
STACK=$CLONE/third_party/tsn-c-stack
cc -std=c11 -O1 -Wall -Wextra -I"$STACK/include" "$WORK/draw_diff.c" "$STACK/src/adp.c" -o "$WORK/draw_diff"
"$WORK/draw_diff" > "$WORK/code.txt"
python3 -I - "$HERE" > "$WORK/model.txt" <<'EOF'
import sys
sys.path.insert(0, sys.argv[1])
import draw_model as m
mac = 0x001B21A40000
for k in range(4096):
    em = mac + k * 7
    eid = m.eui64(em)
    up = (k & 2) != 0
    mx = m.STARTUP_MAX if up else m.LINK_UP_MAX
    print(k, 1 if up else 2, m.draw(m.core_rng(em, eid, 1853117 + k * 131, k & 1), mx))
EOF
if cmp -s "$WORK/code.txt" "$WORK/model.txt"; then
	echo "draw_diff: IDENTICAL over $(wc -l < "$WORK/code.txt") tuples (code: stack adp.c + head port_seed/mix; model: draw_model.py)"
else
	echo "draw_diff: DIFFER"; diff "$WORK/code.txt" "$WORK/model.txt" | head; exit 1
fi
