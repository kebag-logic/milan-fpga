#include <stdio.h>
#include "ctrl_app.h"
int main(void) {
    printf("THREE=%u PASS=%u MAAP_PASS=%u ACMP_PASS=%u EVT=%u ACMPRX=%u ADPRX=%u OWED=%u LAT_TALKER=%u\n",
           (unsigned)CTRL_APP_THREE_PASS_MAX, (unsigned)CTRL_APP_PASS_MAX, (unsigned)MAAP_MBX_PASS_MAX,
           (unsigned)ACMP_MBX_PASS_MAX, (unsigned)CTRL_LOOP_EVT_PASSES, (unsigned)ACMP_MBX_RX_PASSES,
           (unsigned)CTRL_LOOP_RX_PASSES(MBX_CH_ADP_RX_WORDS), (unsigned)ACMP_MBX_OWED_PASSES,
           (unsigned)ACMP_MBX_LAT_TALKER);
    return 0;
}
