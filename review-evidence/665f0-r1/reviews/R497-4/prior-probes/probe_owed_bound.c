// Reviewer probe (R496-3): the pass and the mailbox accesses in which a
// restart's ENTITY_AVAILABLE is committed when k ENTITY_DEPARTINGs are owed,
// measured through the driver, the model and the loop. Compared with the
// stated bound: ctrl_loop.h A3 ("committed in the first pass after the merge
// frees the room") and "the module's response is committed in the pass that
// takes it", ADP_MBX_EVT_ACCESSES for an event's response.
//
// Built against the head's own test_adp.c (its main renamed), so it uses the
// same fixture, model and app.
#define main test_adp_main
#include "test_adp.c"
#undef main

// Queue k owed DEPARTINGs behind a stalled ring and a restart whose
// TMR_DELAY is due. With `room_first`, the ring is released before the pass
// that takes the expiry; otherwise the expiry is taken while the ring is
// still full and the room returns afterwards.
static void probe(unsigned k, bool room_first)
{
	boot();
	mbx_model_bind(&model, NULL, NULL);
	mbx_model_set_link(&model, 0, true);
	settle();
	to_waiting();
	if (k == 0u) {          // baseline: the restart's DEPARTING leaves at once
		adp_mbx_set_enable(&app.adp, false);
		adp_mbx_set_enable(&app.adp, true);
	}
	mbx_model_tx_pause(&model, true);
	uint8_t filler[ADP_FRAME_BYTES];
	adp_build(adp0(), ADP_MSG_ENTITY_AVAILABLE, 0x0F0F0F0Fu, filler);
	while (mbx_tx_send(MBX_CH_ADP, 0, filler, sizeof filler) == MBX_STATUS_OK) {
	}
	for (unsigned i = 0; i < k; ++i) {
		adp_mbx_set_enable(&app.adp, false);
		adp_mbx_set_enable(&app.adp, true);
	}
	uint32_t owed = adp0()->departing_owed;
	const struct mbx_model_tmr_op *arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
	mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms);
	unsigned passes_before_room = 0;
	if (!room_first) {
		for (unsigned i = 0; i < 4u; ++i) {
			(void)pass();
			passes_before_room++;
		}
	}
	mbx_model_tx_pause(&model, false);
	uint32_t base = model.tx_sent;
	uint64_t acc = 0;
	unsigned p = 0;
	unsigned avail_pass = 0;
	uint64_t avail_acc = 0;
	for (p = 1; p <= k + 8u && avail_pass == 0u; ++p) {
		acc += pass();
		for (uint32_t j = base; j < model.tx_sent; ++j) {
			const struct mbx_model_tx *t = mbx_model_tx_frame(&model, j);
			if (t != NULL && (t->bytes[15] & 0x0Fu) == ADP_MSG_ENTITY_AVAILABLE &&
			    wire_be32(t->bytes + 50) == 0u) {
				avail_pass = p;
				avail_acc = acc;
			}
		}
	}
	printf("PROBE k=%u room_first=%d owed_departing=%u available_committed_in_pass=%u "
	       "(passes_after_room) accesses_from_room=%llu ADP_MBX_EVT_ACCESSES=%u ADP_MBX_PASS_MAX=%u "
	       "frames_after_room=%u passes_before_room=%u\n",
	       k, room_first ? 1 : 0, (unsigned)owed, avail_pass, (unsigned long long)avail_acc,
	       (unsigned)ADP_MBX_EVT_ACCESSES, (unsigned)ADP_MBX_PASS_MAX, (unsigned)(model.tx_sent - base),
	       passes_before_room);
}

int main(void)
{
	static const unsigned ks[] = {0u, 1u, 2u, 3u, 16u, 64u};
	for (unsigned i = 0; i < sizeof ks / sizeof ks[0]; ++i) {
		probe(ks[i], true);
		probe(ks[i], false);
	}
	return 0;
}
