/* SPDX-License-Identifier: Apache-2.0 */
/* Probe: Registrar LV + rJoinIn! (IEEE 802.1Q-2018 Table 10-4 lists only
 * "Stop leavetimer, IN"). Count Join indications over one LeaveAll cycle. */
#include <stdio.h>
#include <string.h>
#include "shish_lan/msrp.h"

static unsigned joins_new, joins_repeat, leaves;
static void talker(struct msrp_ctx *c, uint8_t p, const struct msrp_talker_adv *t, bool is_new)
{
    (void)c; (void)p; (void)t;
    if (is_new) { ++joins_new; } else { ++joins_repeat; }
}
static void left(struct msrp_ctx *c, uint8_t p, uint8_t type, const void *v)
{
    (void)c; (void)p; (void)type; (void)v;
    ++leaves;
}

static int rx(struct mrp_app *app, unsigned event, int leaveall)
{
    uint8_t pdu[40] = {0};
    pdu[1] = MSRP_ATTR_TYPE_TALKER_ADV; pdu[2] = 25; pdu[4] = 2 + 25 + 1 + 2;
    pdu[5] = leaveall ? 0x20 : 0; pdu[6] = 1;
    memcpy(pdu + 7, "\1\2\3\4\5\6\0\1", 8);
    pdu[7 + 25] = (uint8_t)(event * 36);
    return mrp_rx(app, 0, pdu, 5 + 30 + 2);
}

int main(void)
{
    struct msrp_ctx ctx = {.on_talker_advertise = talker, .on_leave = left};
    struct mrp_app *app = msrp_app_create(1, &ctx);
    mrp_port_configure(app, 0, 20, 500, 10000, 1, true);
    int a = rx(app, 0, 0);   /* rNew: MT -> IN, New indication */
    int b = rx(app, 4, 1);   /* LeaveAll + Mt: IN -> LV */
    int c = rx(app, 1, 0);   /* rJoinIn in LV: Table 10-4 says no indication */
    printf("rx=%d,%d,%d new_indications=%u repeated_join_indications=%u leaves=%u milan=%d\n",
           a, b, c, joins_new, joins_repeat, leaves, (int)app->ops->milan_rapid_leave);
    msrp_app_destroy(app);
    return 0;
}
