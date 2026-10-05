// R496-4 reviewer probe (disposable, not part of the tree).
//
// Drives the ADP core (sw/firmware/ctrl/adp/adp.c) with a seeded random input
// sequence over fake ports and prints a trace. Built twice by
// run_probes.sh: once against the head's adp.c and once against a reference
// copy whose owed-DEPARTING queue is unbounded (the cap's `<
// ADP_DEPARTING_OWED_MAX` replaced by `!= UINT32_MAX`, the round-3 rule).
//
// Mode "drain": after every input, while the port has room, poll until
// nothing is owed. Then the two builds see the same inputs at the same
// quiescent points, and compare_traces.py checks the coalescing claim of
// adp.h: the head's wire equals the reference's with back-to-back identical
// ENTITY_DEPARTINGs collapsed, and every state but the counters agrees.
//
// Mode "free": room and polls are random inputs too (partial drains). Only
// head invariants are checked here, in C:
//   I1 departing_owed <= ADP_DEPARTING_OWED_MAX;
//   I2 while a DEPARTING is owed, available_index is 0, and a DEPARTING sent
//      while another was still owed behind it is followed by one carrying 0;
//   I3 conservation: SHUTDOWNs acted on == DEPARTINGs sent + owed + coalesced;
//   I4 no ENTITY_AVAILABLE is sent while a DEPARTING is owed;
//   I5 a poll sends at most one frame.
//
// Usage: probe <drain|free> <seed> <steps>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "adp.h"

static struct {
	bool room;
	bool link;
	unsigned sends_this_call;
	unsigned long sent;
	unsigned long avail_sent;
	unsigned long dep_sent;
	int timer_running;
} fk;

static int drain_mode;
static struct adp A;
static unsigned long fails;

static bool f_send(void *ctx, unsigned i, const uint8_t *f, size_t len)
{
	(void)ctx;
	(void)i;
	(void)len;
	if (!fk.room) {
		return false;
	}
	uint8_t msg = f[15] & 0x0Fu;
	uint32_t idx = ((uint32_t)f[14 + 36] << 24) | ((uint32_t)f[14 + 37] << 16) | ((uint32_t)f[14 + 38] << 8) |
		       f[14 + 39];
	if (msg == ADP_MSG_ENTITY_AVAILABLE && A.departing_owed != 0u) {
		printf("FAIL I4 AVAILABLE sent with %u DEPARTING owed\n", A.departing_owed);
		fails++;
	}
	printf("W %s %u\n", msg == ADP_MSG_ENTITY_AVAILABLE ? "AV" : "DE", idx);
	fk.sent++;
	fk.sends_this_call++;
	if (msg == ADP_MSG_ENTITY_AVAILABLE) {
		fk.avail_sent++;
	} else {
		fk.dep_sent++;
	}
	return true;
}
static void f_start(void *ctx, unsigned i, uint32_t ms)
{
	(void)ctx;
	(void)i;
	(void)ms;
	fk.timer_running = 1;
}
static void f_stop(void *ctx, unsigned i)
{
	(void)ctx;
	(void)i;
	fk.timer_running = 0;
}
static void f_gptp(void *ctx, unsigned i, uint64_t *gm, uint8_t *dom)
{
	(void)ctx;
	(void)i;
	*gm = 0x0011223344556677ull;
	*dom = 0;
}
static bool f_link(void *ctx, unsigned i)
{
	(void)ctx;
	(void)i;
	return fk.link;
}
static uint32_t f_seed(void *ctx)
{
	(void)ctx;
	return 0x12345u;
}

static const struct adp_entity ent = {.entity_id = 0x0001020304050607ull, .entity_model_id = 1, .mac = 0x020000000001ull};
static const struct adp_ports ports = {0, f_send, f_start, f_stop, f_gptp, f_link, f_seed};

static uint64_t rs;
static unsigned rnd(unsigned n)
{
	rs ^= rs << 13;
	rs ^= rs >> 7;
	rs ^= rs << 17;
	return (unsigned)(rs % n);
}

static unsigned long acted_shutdowns;

static void check_inv(const char *after)
{
	if (A.departing_owed > ADP_DEPARTING_OWED_MAX) {
		printf("FAIL I1 departing_owed %u after %s\n", A.departing_owed, after);
		fails++;
	}
	if (A.departing_owed != 0u && A.available_index != 0u) {
		printf("FAIL I2 available_index %u with a DEPARTING owed after %s\n", A.available_index, after);
		fails++;
	}
	unsigned long acct = fk.dep_sent + A.departing_owed + A.departing_coalesced;
	if (acted_shutdowns != acct) {
		printf("FAIL I3 SHUTDOWNs %lu != sent %lu + owed %u + coalesced %u after %s\n", acted_shutdowns, fk.dep_sent,
		       A.departing_owed, A.departing_coalesced, after);
		fails++;
	}
}

static void poll_once(void)
{
	uint32_t owed_before = A.departing_owed;
	uint32_t idx_next = A.departing_index;
	unsigned long before = fk.dep_sent;
	fk.sends_this_call = 0;
	(void)adp_poll(&A);
	if (fk.sends_this_call > 1u) {
		printf("FAIL I5 a poll sent %u frames\n", fk.sends_this_call);
		fails++;
	}
	if (fk.dep_sent != before && owed_before >= 2u && A.departing_index != 0u) {
		printf("FAIL I2 the DEPARTING queued behind index %u carries %u\n", idx_next, A.departing_index);
		fails++;
	}
}

static void drain(void)
{
	if (!drain_mode || !fk.room) {
		return;
	}
	for (unsigned k = 0; k < 16u; ++k) {
		if (!adp_poll(&A)) {
			return;
		}
	}
	printf("FAIL drain did not finish\n");
	fails++;
}

int main(int argc, char **argv)
{
	if (argc != 4) {
		return 2;
	}
	drain_mode = strcmp(argv[1], "drain") == 0;
	rs = strtoull(argv[2], 0, 0) * 0x9E3779B97F4A7C15ull + 1u;
	unsigned long steps = strtoul(argv[3], 0, 0);
	fk.room = true;
	fk.link = true;
	adp_init(&A, &ent, &ports, 0, 0);
	uint8_t disc[82];
	memset(disc, 0, sizeof disc);
	disc[12] = 0x22;
	disc[13] = 0xF0;
	disc[14] = 0xFA;
	disc[15] = ADP_MSG_ENTITY_DISCOVER;
	for (unsigned long s = 0; s < steps; ++s) {
		unsigned op = rnd(drain_mode ? 9u : 10u);
		// bias toward SHUTDOWN/restart pairs and a stalled port so the cap is reached
		const char *name = "?";
		switch (op) {
		case 0:
			name = "enable";
			adp_set_enable(&A, true);
			break;
		case 1:
			name = "disable";
			if (A.enabled && A.state != ADP_STATE_DOWN) {
				acted_shutdowns++;
			}
			adp_set_enable(&A, false);
			break;
		case 2:
			name = "link-up";
			fk.link = true;
			adp_link_change(&A, true);
			break;
		case 3:
			name = "link-down";
			if (rnd(3) == 0) {
				fk.link = false;
				adp_link_change(&A, false);
			}
			break;
		case 4:
			name = "gm";
			adp_gm_change(&A);
			break;
		case 5:
			name = "discover";
			adp_rx(&A, disc, sizeof disc);
			break;
		case 6:
			name = "expire";
			adp_timer_expired(&A);
			break;
		case 7:
			name = "room";
			fk.room = rnd(2) == 0;
			break;
		case 8:
			name = "expire";
			adp_timer_expired(&A);
			break;
		default:
			name = "poll";
			poll_once();
			break;
		}
		drain();
		check_inv(name);
		printf("S %s st=%d tm=%d en=%d ai=%u ao=%d dueD=%d room=%d\n", name, (int)A.state, (int)A.timer,
		       (int)A.enabled, A.available_index, (int)A.available_owed, A.departing_owed != 0u, (int)fk.room);
	}
	printf("END sent=%lu dep=%lu av=%lu shutdowns=%lu coalesced=%u owed=%u fails=%lu\n", fk.sent, fk.dep_sent,
	       fk.avail_sent, acted_shutdowns, A.departing_coalesced, A.departing_owed, fails);
	return fails != 0u;
}
