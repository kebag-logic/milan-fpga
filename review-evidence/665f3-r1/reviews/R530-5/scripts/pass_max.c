/* pass_max.c - print the composed pass bounds of ctrl_app.h (reviewer receipt). */
#include <stdio.h>
#include "ctrl_app.h"
int main(void)
{
	printf("MBX_N_IF %u\n", (unsigned)MBX_N_IF);
	printf("ACMP_MBX_PASS_MAX %u\n", (unsigned)ACMP_MBX_PASS_MAX);
	printf("CTRL_APP_MAAP_PASS_SHARE %u\n", (unsigned)CTRL_APP_MAAP_PASS_SHARE);
	printf("CTRL_APP_PASS_MAX %u\n", (unsigned)CTRL_APP_PASS_MAX);
	printf("MAAP_MBX_PASS_MAX %u\n", (unsigned)MAAP_MBX_PASS_MAX);
	printf("CTRL_LOOP_EVT_PASSES %u ACMP_MBX_RX_PASSES %u ADP_RX_PASSES %u OWED_PASSES %u\n",
	       (unsigned)CTRL_LOOP_EVT_PASSES, (unsigned)ACMP_MBX_RX_PASSES,
	       (unsigned)CTRL_LOOP_RX_PASSES(MBX_CH_ADP_RX_WORDS), (unsigned)ACMP_MBX_OWED_PASSES);
	printf("CTRL_APP_MAAP_FIRST_SLOT %u last MAAP slot %u of %u\n", (unsigned)CTRL_APP_MAAP_FIRST_SLOT,
	       (unsigned)(CTRL_APP_MAAP_FIRST_SLOT + MBX_N_IF - 1u), (unsigned)MBX_N_TIMERS);
	return 0;
}
