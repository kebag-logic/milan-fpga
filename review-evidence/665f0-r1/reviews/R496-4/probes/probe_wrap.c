// R496-4 reviewer probe (disposable): 2^32 + 3 coalesced SHUTDOWNs through the
// public API. The two owed ENTITY_DEPARTINGs and the oldest index must be
// unchanged, departing_coalesced must wrap modulo 2^32 as adp.h states, and with
// room the wire must carry DEPARTING 1, DEPARTING 0, then AVAILABLE 0.
#include <stdio.h>
#include "adp.h"
static int room = 1, n;
static unsigned char msg[8];
static unsigned idx[8];
static bool s(void *c, unsigned i, const uint8_t *f, size_t l)
{
	(void)c; (void)i; (void)l;
	if (!room) return false;
	if (n < 8) { msg[n] = f[15] & 15u; idx[n] = ((unsigned)f[50] << 24) | ((unsigned)f[51] << 16) | ((unsigned)f[52] << 8) | f[53]; }
	n++;
	return true;
}
static void t0(void *c, unsigned i, uint32_t ms) { (void)c; (void)i; (void)ms; }
static void t1(void *c, unsigned i) { (void)c; (void)i; }
static void g(void *c, unsigned i, uint64_t *gm, uint8_t *d) { (void)c; (void)i; *gm = 1; *d = 0; }
static bool lu(void *c, unsigned i) { (void)c; (void)i; return true; }
static uint32_t sd(void *c) { (void)c; return 7; }
int main(void)
{
	static const struct adp_entity e = {.entity_id = 5};
	static const struct adp_ports p = {0, s, t0, t1, g, lu, sd};
	struct adp a;
	adp_init(&a, &e, &p, 0, 0);
	adp_set_enable(&a, true);
	adp_timer_expired(&a);                 // AVAILABLE 0 sent, index now 1
	room = 0;
	adp_set_enable(&a, false);             // DEPARTING 1 owed
	adp_set_enable(&a, true);
	adp_set_enable(&a, false);             // DEPARTING 0 queued
	unsigned long long pairs = (1ull << 32) + 3u;
	for (unsigned long long k = 0; k < pairs; ++k) {
		adp_set_enable(&a, true);
		adp_set_enable(&a, false);
	}
	printf("after %llu coalesced pairs: owed=%u index=%u coalesced=%u (expect 2, 1, %u)\n", pairs,
	       a.departing_owed, a.departing_index, a.departing_coalesced, (unsigned)(pairs & 0xFFFFFFFFu));
	int ok = a.departing_owed == 2u && a.departing_index == 1u && a.departing_coalesced == (uint32_t)pairs;
	adp_set_enable(&a, true);
	room = 1;
	(void)adp_poll(&a);
	(void)adp_poll(&a);
	adp_timer_expired(&a);
	printf("wire: %d frames: %u/%u %u/%u %u/%u %u/%u (msg/index; 0=AVAILABLE 1=DEPARTING)\n", n, msg[0], idx[0], msg[1],
	       idx[1], msg[2], idx[2], msg[3], idx[3]);
	ok = ok && n == 4 && msg[1] == 1 && idx[1] == 1 && msg[2] == 1 && idx[2] == 0 && msg[3] == 0 && idx[3] == 0 &&
	     a.state == ADP_STATE_WAITING;
	printf("%s\n", ok ? "PASS" : "FAIL");
	return !ok;
}
