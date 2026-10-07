/* SPDX-License-Identifier: Apache-2.0 */
/* Probe: a Talker registered on port 0 is propagated to port 1. Its Leave
 * timer expires while port 1 holds a refused PDU. Is the withdrawal
 * propagated to port 1 once its output is accepted? */
#include <stdio.h>
#include <string.h>
#include "shish_lan/msrp.h"
#include "ports/timer.h"

static int refuse;
static int send_pdu(void *ctx, uint8_t port, const uint8_t *pdu, size_t len)
{
    (void)ctx; (void)port; (void)pdu; (void)len;
    return refuse ? -105 : 0;
}

static void visit(void *ctx, const struct mrp_attr_status *st)
{
    if (st->attr_type == MSRP_ATTR_TYPE_TALKER_ADV) { *(enum mrp_appl_state *)ctx = st->appl; }
}

static void rx(struct mrp_app *app, uint8_t event)
{
    uint8_t pdu[40] = {0};
    pdu[1] = MSRP_ATTR_TYPE_TALKER_ADV; pdu[2] = 25; pdu[4] = 30;
    pdu[6] = 1; memcpy(pdu + 7, "\1\2\3\4\5\6\0\1", 8); pdu[32] = (uint8_t)(event * 36);
    (void)mrp_rx(app, 0, pdu, 37);
}

static void poll(struct mrp_app *app, uint8_t *b0, uint8_t *b1, unsigned ticks)
{
    for (unsigned n = 0; n < ticks; ++n) {
        (void)mrp_transmit(app, 0, b0, 256, send_pdu, NULL);
        (void)mrp_transmit(app, 1, b1, 256, send_pdu, NULL);
        shlan_timer_tick();
    }
}

int main(int argc, char **argv)
{
    (void)argv;
    struct msrp_ctx ctx = {0};
    struct mrp_app *app = msrp_app_create(2, &ctx);
    for (uint8_t p = 0; p < 2; ++p) { mrp_port_configure(app, p, 20, 500, 10000, 1 + p, true); }
    static uint8_t b0[256], b1[256];
    rx(app, 0);                 /* New on port 0: propagated to port 1 */
    poll(app, b0, b1, 200);     /* port 1 declares and goes quiet */
    enum mrp_appl_state before = MRP_APPL_STATE_COUNT, after = MRP_APPL_STATE_COUNT;
    mrp_attr_visit(app, 1, visit, &before);
    struct msrp_stream_id sid = {{9, 9, 9, 9, 9, 9, 0, 1}};
    msrp_declare_listener(app, 1, &sid, MSRP_LISTENER_DECL_READY);
    refuse = argc < 2;          /* any argument selects the control run */
    (void)mrp_transmit(app, 1, b1, 256, send_pdu, NULL);
    rx(app, 5);                 /* Lv on port 0: LV, Leave timer 5 s */
    for (unsigned n = 0; n < 600; ++n) {
        (void)mrp_transmit(app, 0, b0, 256, send_pdu, NULL);
        shlan_timer_tick();     /* port 1 keeps its retained PDU */
    }
    refuse = 0;
    poll(app, b0, b1, 300);
    mrp_attr_visit(app, 1, visit, &after);
    printf("port1 Talker applicant before=%s after=%s (declaring states: VP VN AN AA QA AP QP)\n",
           mrp_appl_state_name(before), mrp_appl_state_name(after));
    msrp_app_destroy(app);
    return 0;
}
