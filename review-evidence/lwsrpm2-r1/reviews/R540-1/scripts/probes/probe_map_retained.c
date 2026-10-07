/* SPDX-License-Identifier: Apache-2.0 */
/* Probe: a two-port stream application. Port 1 holds a refused (retained)
 * PDU while port 0 registers a Talker. Does the propagated declaration reach
 * port 1 once its output is accepted? */
#include <stdio.h>
#include <string.h>
#include "shish_lan/msrp.h"
#include "ports/timer.h"

static int refuse;
static unsigned talker_vectors_on_port1;
static int send_pdu(void *ctx, uint8_t port, const uint8_t *pdu, size_t len)
{
    (void)ctx;
    if (refuse) { return -105; }
    /* Count Talker Advertise messages in the accepted PDU for port 1. */
    for (size_t i = 1; port == 1 && i + 1 < len; ++i) {
        if (pdu[i] == MSRP_ATTR_TYPE_TALKER_ADV && pdu[i + 1] == 25) { ++talker_vectors_on_port1; }
    }
    return 0;
}

static void visit(void *ctx, const struct mrp_attr_status *st)
{
    if (st->attr_type == MSRP_ATTR_TYPE_TALKER_ADV) { ++*(unsigned *)ctx; }
}

int main(int argc, char **argv)
{
    struct msrp_ctx ctx = {0};
    struct mrp_app *app = msrp_app_create(2, &ctx);
    for (uint8_t p = 0; p < 2; ++p) { mrp_port_configure(app, p, 20, 500, 10000, 1 + p, true); }
    static uint8_t buf1[256], buf0[256];
    struct msrp_stream_id sid = {{9, 9, 9, 9, 9, 9, 0, 1}};
    /* Give port 1 something to send, then refuse it so the PDU is retained. */
    msrp_declare_listener(app, 1, &sid, MSRP_LISTENER_DECL_READY);
    refuse = argc < 2; (void)argv; /* any argument selects the control run */
    int t1 = mrp_transmit(app, 1, buf1, sizeof buf1, send_pdu, NULL);
    /* Port 0 receives a Talker Advertise New. */
    uint8_t pdu[40] = {0};
    pdu[1] = MSRP_ATTR_TYPE_TALKER_ADV; pdu[2] = 25; pdu[4] = 30;
    pdu[6] = 1; memcpy(pdu + 7, "\1\2\3\4\5\6\0\1", 8); pdu[32] = 0; /* New */
    int r = mrp_rx(app, 0, pdu, 37);
    unsigned on_port1_before = 0;
    mrp_attr_visit(app, 1, visit, &on_port1_before);
    /* Driver progress: accept output and poll for a while. */
    refuse = 0;
    for (unsigned n = 0; n < 300; ++n) {
        (void)mrp_transmit(app, 1, buf1, sizeof buf1, send_pdu, NULL);
        (void)mrp_transmit(app, 0, buf0, sizeof buf0, send_pdu, NULL);
        shlan_timer_tick();
    }
    unsigned on_port1_after = 0;
    mrp_attr_visit(app, 1, visit, &on_port1_after);
    printf("refused_transmit=%d rx=%d port1_talker_instances_before=%u after=%u talker_messages_sent_on_port1=%u\n",
           t1, r, on_port1_before, on_port1_after, talker_vectors_on_port1);
    msrp_app_destroy(app);
    return 0;
}
