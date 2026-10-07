/* SPDX-License-Identifier: Apache-2.0 */
#include <stdio.h>
#include <string.h>
#include "shish_lan/msrp.h"
#include "shish_lan/mrp_pdu.h"
#include "ports/timer.h"
struct capture { struct mrp_app *app; unsigned messages; int refuse; };
struct snapshot { unsigned talkers; enum mrp_appl_state state; };
static void wire(void *ctx, uint8_t type, enum mrp_attr_event event, const void *value) {
    struct capture *c = ctx; (void)event; (void)value;
    if (type == MSRP_ATTR_TYPE_TALKER_ADV) { ++c->messages; }
}
static int send_frame(void *ctx, uint8_t port, const uint8_t *pdu, size_t len) {
    struct capture *c = ctx; (void)port;
    if (c->refuse) { return -105; }
    return mrpdu_parse(pdu, len, c->app->ops, wire, NULL, c);
}
static void visit(void *ctx, const struct mrp_attr_status *s) {
    struct snapshot *snap = ctx;
    if (s->attr_type == MSRP_ATTR_TYPE_TALKER_ADV) { ++snap->talkers; snap->state = s->appl; }
}
static void tick(unsigned n) { while (n--) { shlan_timer_tick(); } }
static int receive_talker(struct mrp_app *app, int leave) {
    uint8_t pdu[37] = {0, 1, 25, 0, 30, 0, 1};
    pdu[14] = 1; /* Stream unique ID. */
    pdu[32] = leave ? 180 : 0;
    return mrp_rx(app, 0, pdu, sizeof pdu);
}
static struct snapshot run_case(int leave, int retained) {
    struct msrp_ctx ctx = {0};
    struct mrp_app *app = msrp_app_create(2, &ctx);
    struct capture capture = {.app = app};
    uint8_t buffer[1500];
    struct snapshot result = {0};
    for (unsigned p = 0; p < 2; ++p) { mrp_port_configure(app, p, 20, 60, 1000, 1, true); }
    int before = 0;
    if (leave) {
        before = receive_talker(app, 0);
        for (unsigned k = 0; k < 60; ++k) { mrp_transmit(app, 1, buffer, sizeof buffer, send_frame, &capture); tick(1); }
    }
    struct msrp_domain domain = {.class_id = 6, .priority = 3, .vid = 2};
    int declare = mrp_mad_join(app, 1, MSRP_ATTR_TYPE_DOMAIN, &domain, true);
    tick(20); capture.refuse = retained;
    int first_tx = mrp_transmit(app, 1, buffer, sizeof buffer, send_frame, &capture);
    int receive = receive_talker(app, leave);
    if (leave) { tick(61); }
    capture.refuse = 0; capture.messages = 0;
    for (unsigned k = 0; k < 300; ++k) { mrp_transmit(app, 1, buffer, sizeof buffer, send_frame, &capture); tick(1); }
    mrp_attr_visit(app, 1, visit, &result);
    printf("%s %s: setup_rx=%d declare=%d first_tx=%d rx=%d target_talkers=%u state=%s messages=%u\n",
           leave ? "leave" : "join", retained ? "retained" : "control", before, declare, first_tx,
           receive, result.talkers, result.talkers ? mrp_appl_state_name(result.state) : "absent", capture.messages);
    msrp_app_destroy(app);
    return result;
}
int main(void) {
    struct snapshot jc = run_case(0, 0), jr = run_case(0, 1);
    struct snapshot lc = run_case(1, 0), lr = run_case(1, 1);
    if (jc.talkers != 1 || lc.talkers != 1 || lc.state != MRP_APPL_STATE_VO) { return 2; }
    return jr.talkers != jc.talkers || lr.state != lc.state;
}
