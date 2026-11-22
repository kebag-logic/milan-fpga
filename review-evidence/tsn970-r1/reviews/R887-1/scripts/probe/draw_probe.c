// SPDX-License-Identifier: MIT
// Reviewer probe: measure the ADP core's first-advertise delay after LINK_UP and after a
// startup with the link up, for one tree's src/adp.c, and the spread of many entities' first
// ENTITY_AVAILABLEs after one common link-up (storm-avoidance check).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "adp.h"

struct ctx { bool link; uint32_t last_delay; uint32_t seed; unsigned sends; uint64_t gm; uint8_t last[ADP_FRAME_BYTES]; };
static bool p_send(void *c, unsigned i, const uint8_t *f, size_t n) { (void)i; struct ctx *x = c; x->sends++; memcpy(x->last, f, n < ADP_FRAME_BYTES ? n : ADP_FRAME_BYTES); return true; }
static void p_start(void *c, unsigned i, uint32_t d) { (void)i; ((struct ctx *)c)->last_delay = d; }
static void p_stop(void *c, unsigned i) { (void)c; (void)i; }
static void p_gptp(void *c, unsigned i, uint64_t *gm, uint8_t *dom) { (void)i; *gm = ((struct ctx *)c)->gm; *dom = 0; }
static bool p_link(void *c, unsigned i) { (void)i; return ((struct ctx *)c)->link; }
static uint32_t p_seed(void *c) { return ((struct ctx *)c)->seed; }

static uint64_t sm(uint64_t *s) { uint64_t z = (*s += 0x9E3779B97F4A7C15ull); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ull; z = (z ^ (z >> 27)) * 0x94D049BB133111EBull; return z ^ (z >> 31); }

int main(void)
{
	uint64_t s = 970;
	struct ctx x; struct adp_ports ports = {&x, p_send, p_start, p_stop, p_gptp, p_link, p_seed};
	struct adp_entity e; memset(&e, 0, sizeof e); e.entity_id = 0x0011223344556677ull; e.mac = 0x001122334455ull;
	struct adp a;
	// 1. one entity, 100000 LINK_UPs and 100000 startups with the link up
	uint32_t lmax = 0, smax = 0, dmax = 0; unsigned lin = 0, sin = 0;
	for (unsigned k = 0; k < 100000u; ++k) {
		memset(&x, 0, sizeof x); x.seed = (uint32_t)sm(&s); x.link = false;
		adp_init(&a, &e, &ports, 0, 0); adp_set_enable(&a, true); adp_link_change(&a, true);
		if (x.last_delay > lmax) lmax = x.last_delay; if (x.last_delay <= 500u) lin++;
		adp_timer_expired(&a); adp_timer_expired(&a); if (x.last_delay > dmax) dmax = x.last_delay;
		memset(&x, 0, sizeof x); x.seed = (uint32_t)sm(&s); x.link = true;
		adp_init(&a, &e, &ports, 0, 0); adp_set_enable(&a, true);
		if (x.last_delay > smax) smax = x.last_delay; if (x.last_delay <= 500u) sin++;
	}
	printf("single entity: LINK_UP draw max %u ms (%u of 100000 <= 500 ms); startup draw max %u ms (%u of 100000 <= 500 ms); TMR_ADVERTISE redraw max %u ms\n", lmax, lin, smax, sin, dmax);
	// 2. GM change inside the delay (DELAY): ignored, frame carries the new GM at build
	memset(&x, 0, sizeof x); x.seed = 5; x.gm = 0xA; adp_init(&a, &e, &ports, 0, 0); adp_set_enable(&a, true); adp_link_change(&a, true);
	uint32_t before = x.last_delay; x.gm = 0xB; adp_gm_change(&a);
	printf("gm change in DELAY: delay unchanged %s, state %d; ", x.last_delay == before ? "yes" : "NO", (int)a.state);
	adp_timer_expired(&a);
	unsigned long long gm = 0; for (int i = 0; i < 8; ++i) gm = (gm << 8) | x.last[14 + 40 + i];
	printf("first frame gm 0x%llX sends %u\n", gm, x.sends);
	// 3. GM change in WAITING: new delay of the 0..4 s kind, then a new AVAILABLE
	x.gm = 0xC; adp_gm_change(&a); printf("gm change in WAITING: state %d last_draw kind %d delay %u; ", (int)a.state, (int)a.last_draw, x.last_delay);
	adp_timer_expired(&a); gm = 0; for (int i = 0; i < 8; ++i) gm = (gm << 8) | x.last[14 + 40 + i];
	printf("re-advertise gm 0x%llX sends %u index field %u\n", gm, x.sends, (unsigned)((x.last[50] << 24) | (x.last[51] << 16) | (x.last[52] << 8) | x.last[53]));
	// 4. N entities on one common link-up: spread of first ENTITY_AVAILABLEs
	unsigned Ns[] = {8, 64, 256, 1024};
	for (unsigned n = 0; n < 4; ++n) {
		unsigned N = Ns[n]; unsigned *bin1 = calloc(4001, sizeof *bin1); unsigned *bin10 = calloc(401, sizeof *bin10); uint32_t mx = 0;
		for (unsigned k = 0; k < N; ++k) {
			struct adp_entity f = e; f.entity_id = sm(&s); memset(&x, 0, sizeof x); x.seed = (uint32_t)sm(&s);
			adp_init(&a, &f, &ports, 0, 0); adp_set_enable(&a, true); adp_link_change(&a, true);
			bin1[x.last_delay]++; bin10[x.last_delay / 10]++; if (x.last_delay > mx) mx = x.last_delay;
		}
		unsigned m1 = 0, m10 = 0; for (unsigned i = 0; i <= 4000; ++i) if (bin1[i] > m1) m1 = bin1[i];
		for (unsigned i = 0; i <= 400; ++i) if (bin10[i] > m10) m10 = bin10[i];
		printf("%u entities, one link-up: last first-AVAILABLE at %u ms, most in one 1 ms slot %u, most in one 10 ms window %u\n", N, mx, m1, m10);
		free(bin1); free(bin10);
	}
	return 0;
}
