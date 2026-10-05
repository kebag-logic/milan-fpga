// Reviewer probe (R496-2): centiseconds carried across passes must survive a
// second TICK record taken while some are still owed (ctrl_loop.h, THE TICK:
// "lose no tick when the core is late"). A late core: the event ring holds a
// full backlog, 40 centiseconds coalesce into one TICK record; after the first
// pass (16 of them dispatched, 24 carried) one more centisecond passes, so a
// second TICK record is posted while 24 are still owed. Every one of the 41
// must reach the consumer. Exit 0 when they do, 1 otherwise.
#include <stdio.h>

#include "ctrl_loop.h"
#include "mbx.h"
#include "mbx_model.h"

static struct mbx_model model;
static unsigned ticks;

static void tick(void)
{
	ticks++;
}

int main(void)
{
	static struct ctrl_loop l;
	mbx_model_reset(&model);
	mbx_model_bind(&model, NULL, NULL);
	ctrl_loop_init(&l);
	if (!ctrl_loop_add_tick(&l, tick) || !ctrl_loop_open(&l, 0)) {
		printf("setup failed\n");
		return 2;
	}
	while (ctrl_loop_service(&l) != 0u) {
	}
	ticks = 0;
	for (unsigned s = 0; s < MBX_EVT_WORDS / MBX_EV_WORDS; ++s) {
		mbx_timer_arm(s % MBX_N_TIMERS, 0x300u, mbx_now_ms());
	}
	mbx_model_advance_ms(&model, 40u * MBX_TICK_MS);
	unsigned passes = 0;
	unsigned carried_when_second_posted = 0;
	unsigned delivered = 0;
	for (; passes < 64u; ++passes) {
		unsigned work = ctrl_loop_service(&l);
		if (passes == 0u) {
			// the 40-centisecond record has been taken by now (the ring's 16
			// timer records first, 8 per pass, so it may take two passes)
		}
		if (carried_when_second_posted == 0u && l.ticks_owed != 0u && l.stats.ticks >= 16u) {
			carried_when_second_posted = l.ticks_owed;
			mbx_model_advance_ms(&model, MBX_TICK_MS);   // one more centisecond: a second TICK record
			delivered = 1u;
		}
		if (work == 0u) {
			break;
		}
	}
	unsigned expected = 40u + delivered;
	printf("carried when the second TICK was posted: %u; delivered %u of %u; passes %u\n",
	       carried_when_second_posted, ticks, expected, passes + 1u);
	return (carried_when_second_posted != 0u && ticks == expected) ? 0 : 1;
}
