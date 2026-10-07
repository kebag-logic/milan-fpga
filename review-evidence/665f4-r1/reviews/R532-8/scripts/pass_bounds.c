// Print the composed pass bounds and their terms from the exact-head headers.
#include <stdio.h>
#include "ctrl_app.h"
int main(void)
{
	printf("MBX_N_IF=%u ACMP_MBX_PASS_MAX=%u MAAP_MBX_PASS_MAX=%u SRP_MBX_PASS_MAX=%u\n",
	       (unsigned)MBX_N_IF, (unsigned)ACMP_MBX_PASS_MAX, (unsigned)MAAP_MBX_PASS_MAX, (unsigned)SRP_MBX_PASS_MAX);
	printf("shared_event_reads=%u THREE=%u PASS_MAX=%u independent=%u\n",
	       (unsigned)(CTRL_LOOP_EVENTS_PER_PASS * (MBX_EV_WORDS + 2u)), (unsigned)CTRL_APP_THREE_PASS_MAX,
	       (unsigned)CTRL_APP_PASS_MAX,
	       (unsigned)(ACMP_MBX_PASS_MAX + MAAP_MBX_PASS_MAX + SRP_MBX_PASS_MAX -
			  2u * CTRL_LOOP_EVENTS_PER_PASS * (MBX_EV_WORDS + 2u)));
	printf("SRP terms: EVENT=%u RX=%u RX_RECORD=%u TX=%u POLL=%u frame=%u EVT_PASSES=%u\n",
	       (unsigned)SRP_MBX_EVENT_MAX, (unsigned)SRP_MBX_RX_MAX, (unsigned)SRP_MBX_RX_RECORD_MAX,
	       (unsigned)SRP_MBX_TX_MAX, (unsigned)SRP_MBX_POLL_MAX, (unsigned)MBX_CH_SRP_MAX_FRAME_BYTES,
	       (unsigned)CTRL_LOOP_EVT_PASSES);
	return 0;
}
