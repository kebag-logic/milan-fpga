// adp_reentry_r3.c - R506-3 probe: ports that break #678's no-callback rule,
// one scenario per run (argv[1] = A1, A2, B1, B2, C1, C2). Prints the state
// the machine is left in; the driver reads adp.c's arcs from gcov.
#include <stdio.h>
#include <string.h>
#include "adp.h"

static struct adp m;
static const char *sc;
static int send_room = 1, reenter_send = 0, reenter_timer = 0, link_cb = 0;
static int timer_running = 0;

static bool p_send(void *c, unsigned i, const uint8_t *f, size_t n) {
	(void)c; (void)i; (void)n;
	if (reenter_send && f[ADP_HEADER_BYTES + 1] == reenter_send - 1) {
		reenter_send = 0;
		adp_link_change(&m, false);
	}
	return send_room;
}
static void p_timer_start(void *c, unsigned i, uint32_t ms) {
	(void)c; (void)i; (void)ms;
	timer_running = 1;
	if (reenter_timer && m.timer == (enum adp_timer)reenter_timer) {
		reenter_timer = 0;
		timer_running = 0;
		adp_timer_expired(&m);
	}
}
static void p_timer_stop(void *c, unsigned i) { (void)c; (void)i; timer_running = 0; }
static void p_gptp(void *c, unsigned i, uint64_t *g, uint8_t *d) { (void)c; (void)i; *g = 1; *d = 0; }
static bool p_link(void *c, unsigned i) {
	(void)c; (void)i;
	if (link_cb) {
		link_cb = 0;
		adp_link_change(&m, true);         // reports up from inside the core's call
		send_room = 0;
		timer_running = 0;
		adp_timer_expired(&m);              // expires the TMR_DELAY just started
		return false;                       // then answers down
	}
	return true;
}
static uint32_t p_seed(void *c) { (void)c; return 7; }

static const struct adp_ports ports = {0, p_send, p_timer_start, p_timer_stop, p_gptp, p_link, p_seed};
static const struct adp_entity ent = {0x0011223344556677ull, 1, 0x001122334455ull, 0, 0, 0, 0, 0, 0};

static void show(void) {
	printf("%s state=%d timer=%d port_timer_running=%d link_up=%d enabled=%d available_owed=%d stray=%u\n",
	       sc, (int)m.state, (int)m.timer, timer_running, (int)m.link_up, (int)m.enabled,
	       (int)m.available_owed, m.stray_expiries);
}

int main(int argc, char **argv) {
	sc = argc > 1 ? argv[1] : "?";
	adp_init(&m, &ent, &ports, 0, 0);
	if (!strcmp(sc, "A1")) {            // link down from inside the AVAILABLE send, then link up
		adp_set_enable(&m, true);
		reenter_send = 1 + ADP_MSG_ENTITY_AVAILABLE;
		adp_timer_expired(&m);
		show();
		adp_link_change(&m, true);
	} else if (!strcmp(sc, "A2")) {     // link down from inside SHUTDOWN's DEPARTING send
		adp_set_enable(&m, true);
		reenter_send = 1 + ADP_MSG_ENTITY_DEPARTING;
		adp_set_enable(&m, false);
	} else if (!strcmp(sc, "B1")) {     // TMR_ADVERTISE expired inside timer_start
		adp_set_enable(&m, true);
		reenter_timer = ADP_TIMER_ADVERTISE;
		adp_timer_expired(&m);
	} else if (!strcmp(sc, "B2")) {     // TMR_DELAY expired inside timer_start on a GM change
		adp_set_enable(&m, true);
		adp_timer_expired(&m);
		reenter_timer = ADP_TIMER_DELAY;
		adp_gm_change(&m);
	} else if (!strcmp(sc, "C1") || !strcmp(sc, "C2")) {  // link port calling back twice
		link_cb = 1;
		adp_set_enable(&m, true);
		show();
		if (!strcmp(sc, "C2"))
			adp_set_enable(&m, false);
		adp_poll(&m);
	}
	show();
	return 0;
}
