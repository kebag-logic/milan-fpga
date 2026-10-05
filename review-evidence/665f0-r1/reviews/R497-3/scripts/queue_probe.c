/* Reviewer probe: public ADP calls, captured wire fields and bus accesses. */
#define main standing_suite_main
#include "test_adp.c"
#undef main

static void deeper_queue(void)
{
	struct adp a;
	fresh(&a, true);
	adp_set_enable(&a, true);
	adp_timer_expired(&a);
	fk.room = false;
	for (unsigned k = 0; k < 6u; ++k) {
		adp_set_enable(&a, false);
		adp_set_enable(&a, true);
		adp_timer_expired(&a);
	}
	check("Q1 six departures survive six restarts and expired startup timers", a.departing_owed == 6u && fk.sends == 1u);
	adp_link_change(&a, false);
	check("Q2 link loss drops only the owed AVAILABLE", !a.available_owed && a.departing_owed == 6u);
	adp_link_change(&a, true);
	adp_timer_expired(&a);
	adp_gm_change(&a);
	uint8_t frame[ADP_FRAME_BYTES];
	discover(frame, ADP_MSG_ENTITY_DISCOVER, 0);
	adp_rx(&a, frame, sizeof frame);
	adp_timer_expired(&a);
	check("Q3 GM, DISCOVER and stray expiry preserve both obligations", a.available_owed && a.departing_owed == 6u);
	fk.room = true;
	for (unsigned k = 0; k < 6u; ++k) {
		unsigned before = fk.sends;
		check("Q4 each poll sends exactly one oldest departure", adp_poll(&a) && fk.sends == before + 1u &&
		      took(k + 1u, ADP_MSG_ENTITY_DEPARTING, k == 0u ? 1u : 0u));
	}
	check("Q5 AVAILABLE follows all six departures with index zero", !adp_poll(&a) && took(7, ADP_MSG_ENTITY_AVAILABLE, 0));
	check("Q6 final schedule and empty queue", a.state == ADP_STATE_WAITING && a.timer == ADP_TIMER_ADVERTISE &&
	      a.available_index == 1u && a.departing_owed == 0u && !a.available_owed);
}

static void measured_poll(void)
{
	boot();
	mbx_model_set_link(&model, 0, true);
	settle();
	to_waiting();
	mbx_model_tx_pause(&model, true);
	uint8_t filler[ADP_FRAME_BYTES];
	adp_build(adp0(), ADP_MSG_ENTITY_AVAILABLE, 0xABCDu, filler);
	while (mbx_tx_send(MBX_CH_ADP, 0, filler, sizeof filler) == MBX_STATUS_OK) {}
	adp_mbx_set_enable(&app.adp, false);
	adp_mbx_set_enable(&app.adp, true);
	const struct mbx_model_tmr_op *arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
	mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms);
	(void)ctrl_loop_service(&app.loop);
	check("Q7 two obligations are present through the real mailbox adapter", adp0()->departing_owed == 1u && adp0()->available_owed);
	mbx_model_tx_pause(&model, false);
	uint32_t sent = model.tx_sent;
	uint64_t before = model.reads + model.writes;
	bool owed = adp_poll(adp0());
	uint64_t cost = model.reads + model.writes - before;
	printf("DEPARTING poll: %llu accesses; poll budget %u\n", (unsigned long long)cost, ADP_MBX_POLL_MAX);
	check("Q8 departure costs exactly 28 accesses and sends one frame", cost == 28u && cost <= ADP_MBX_POLL_MAX && owed && model.tx_sent == sent + 1u && model_sent(sent, ADP_MSG_ENTITY_DEPARTING, 1));
	before = model.reads + model.writes;
	owed = adp_poll(adp0());
	cost = model.reads + model.writes - before;
	printf("AVAILABLE poll: %llu accesses; poll budget %u\n", (unsigned long long)cost, ADP_MBX_POLL_MAX);
	check("Q9 AVAILABLE costs 31 accesses, finishes obligations and restarts the timer", cost == 31u && !owed && model_sent(sent + 1u, ADP_MSG_ENTITY_AVAILABLE, 0) && adp0()->timer == ADP_TIMER_ADVERTISE);
}

int main(void)
{
	deeper_queue();
	measured_poll();
	return check_report("reviewer queue ordering and access bound");
}
