// Reviewer probe (R496-3): three legs of adp.h's owed-frame rule that no
// check of the head exercises, run on the core over the head's own fake
// ports (test_adp.c, its main renamed). Built once against the head's adp.c
// and once against each planted copy; the printed wire differs.
//
//   L1 "every SHUTDOWN's DEPARTING stays owed ... across any ... link change":
//      SHUTDOWN behind a full path, restart, LINK DOWN while the restart runs.
//   L2 "an owed AVAILABLE is dropped only by a link loss or a SHUTDOWN":
//      a GPTP GM change while the AVAILABLE is owed in DELAY.
//   L3 "an owed AVAILABLE is dropped by a link loss": the link drops and
//      returns before any poll; the next AVAILABLE must wait for its TMR_DELAY.
#define main test_adp_main
#include "test_adp.c"
#undef main

static void wire(const char *leg)
{
	printf("%s wire:", leg);
	for (unsigned k = 0; k < fk.sends && k < 16u; ++k) {
		printf(" %s(%u)", fk.msg[k] == ADP_MSG_ENTITY_AVAILABLE ? "AVAILABLE" : "DEPARTING", (unsigned)fk.index[k]);
	}
	printf("\n");
}

int main(void)
{
	struct adp a;

	advertise_then_depart_owed(&a);           // AVAILABLE(0) sent, DEPARTING(1) owed, restart in DELAY
	adp_link_change(&a, false);
	fk.link = true;
	fk.room = true;
	adp_link_change(&a, true);
	for (unsigned k = 0; k < 4u; ++k) {
		(void)adp_poll(&a);
	}
	adp_timer_expired(&a);
	(void)adp_poll(&a);
	wire("L1");
	printf("L1 departing_owed=%u state=%d -> %s\n", (unsigned)a.departing_owed, (int)a.state,
	       took(1, ADP_MSG_ENTITY_DEPARTING, 1) ? "DEPARTING(1) delivered" : "DEPARTING(1) LOST");

	fresh(&a, true);
	adp_set_enable(&a, true);
	fk.room = false;
	adp_timer_expired(&a);                    // AVAILABLE owed in DELAY, no timer
	adp_gm_change(&a);
	fk.room = true;
	for (unsigned k = 0; k < 4u; ++k) {
		(void)adp_poll(&a);
	}
	wire("L2");
	printf("L2 state=%d timer=%d available_owed=%d -> %s\n", (int)a.state, (int)a.timer, (int)a.available_owed,
	       (a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_NONE && !a.available_owed)
		       ? "WEDGED: DELAY with no timer and nothing owed"
		       : "advances");

	fresh(&a, true);
	adp_set_enable(&a, true);
	fk.room = false;
	adp_timer_expired(&a);                    // AVAILABLE owed in DELAY, no timer
	adp_link_change(&a, false);
	fk.link = true;
	adp_link_change(&a, true);                // 5.6.3.5.3: a fresh TMR_DELAY
	fk.room = true;
	(void)adp_poll(&a);
	wire("L3");
	printf("L3 sends_before_TMR_DELAY=%u timer=%d -> %s\n", fk.sends, (int)a.timer,
	       fk.sends == 0u ? "waits for its TMR_DELAY" : "AVAILABLE SENT WITHOUT ITS TMR_DELAY");
	return 0;
}
