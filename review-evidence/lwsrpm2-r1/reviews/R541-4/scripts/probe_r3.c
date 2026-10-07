/* SPDX-License-Identifier: Apache-2.0 */
/* Reviewer probes (R540-3): allocation-fault sweeps over Flush!, Talker
 * replacement and multi-event receive. Linked with probe_alloc.c. */
#include <stdio.h>
#include <string.h>
#include "shish_lan/error.h"
#include "shish_lan/msrp.h"
#include "ports/timer.h"

extern int probe_fail_at; /* fail the Nth following calloc/malloc; 0 disables */

static char log_buf[512];
static void logp(const char *s) { if (strlen(log_buf) + strlen(s) + 2 < sizeof(log_buf)) { strcat(log_buf, s); strcat(log_buf, " "); } }
static void on_ta(struct msrp_ctx *c, uint8_t p, const struct msrp_talker_adv *t, bool n)
{ (void)c; (void)t; (void)n; char b[16]; snprintf(b, sizeof b, "J1@%u", p); logp(b); }
static void on_tf(struct msrp_ctx *c, uint8_t p, const struct msrp_talker_failed *t, bool n)
{ (void)c; (void)t; (void)n; char b[16]; snprintf(b, sizeof b, "J2@%u", p); logp(b); }
static void on_li(struct msrp_ctx *c, uint8_t p, const struct msrp_stream_id *s, enum msrp_listener_decl d, bool n)
{ (void)c; (void)s; (void)n; char b[16]; snprintf(b, sizeof b, "J3.%d@%u", (int)d, p); logp(b); }
static void on_lv(struct msrp_ctx *c, uint8_t p, uint8_t t, const void *v)
{ (void)c; (void)v; char b[16]; snprintf(b, sizeof b, "L%u@%u", t, p); logp(b); }
static struct msrp_ctx ctx = { .on_talker_advertise = on_ta, .on_talker_failed = on_tf,
                               .on_listener = on_li, .on_leave = on_lv };
static int fails;
#define CHECK(name, cond) do { int ok_ = (cond); printf("%s %s\n", ok_ ? "PASS" : "FAIL", name); fails += !ok_; } while (0)

/* Talker Advertise (type 1) or Talker Failed (type 2) for stream id byte sid. */
static size_t talker_pdu(uint8_t *b, unsigned type, unsigned sid, unsigned event)
{
    unsigned alen = type == 1 ? 25u : 34u;
    size_t n = 0;
    b[n++] = 0; b[n++] = (uint8_t)type; b[n++] = (uint8_t)alen;
    b[n++] = 0; b[n++] = (uint8_t)(2 + alen + 1 + 2);
    b[n++] = 0; b[n++] = 1;
    uint8_t v[34] = {0};
    v[7] = (uint8_t)sid; v[8] = 0x91; v[15] = 2; v[17] = 100; v[19] = 1; v[20] = 0x70;
    if (type == 2) { v[33] = 1; }
    memcpy(b + n, v, alen); n += alen;
    b[n++] = (uint8_t)(event * 36u);
    b[n++] = 0; b[n++] = 0; b[n++] = 0; b[n++] = 0;
    return n;
}
/* One PDU: Listener Ready for stream sid_l, then Talker Advertise JoinIn for sid_t. */
static size_t mixed_pdu(uint8_t *b, unsigned sid_l, unsigned sid_t)
{
    size_t n = 0;
    b[n++] = 0;
    uint8_t li[] = {3, 8, 0, 14, 0, 1, 0, 0, 0, 0, 0, 0, 0, (uint8_t)sid_l, 36, (uint8_t)(2u << 6), 0, 0};
    memcpy(b + n, li, sizeof li); n += sizeof li;
    uint8_t t[64];
    size_t tn = talker_pdu(t, 1, sid_t, 1);
    memcpy(b + n, t + 1, tn - 3); n += tn - 3; /* drop the version and the PDU EndMark */
    b[n++] = 0; b[n++] = 0;
    return n;
}

static int accept(void *c, uint8_t p, const uint8_t *d, size_t n) { (void)c; (void)p; (void)d; (void)n; return 0; }

struct sig { char s[512]; };
static void visit_sig(void *c, const struct mrp_attr_status *st)
{
    struct sig *g = c; char b[48];
    const uint8_t *v = st->attr_val;
    snprintf(b, sizeof b, "%u:t%u.s%u.%s.%s ", st->port_id, st->attr_type, st->attr_type == 4 ? 0u : v[7],
             mrp_appl_state_name(st->appl), mrp_reg_state_name(st->reg));
    if (strlen(g->s) + strlen(b) + 1 < sizeof g->s) { strcat(g->s, b); }
}
static void signature(struct mrp_app *a, struct sig *g)
{
    g->s[0] = 0;
    for (uint8_t p = 0; p < 3; ++p) { mrp_attr_visit(a, p, visit_sig, g); }
}
static int reg_of(struct mrp_app *a, uint8_t port, uint8_t type, unsigned sid);
struct find { uint8_t type; unsigned sid; int reg; };
static void visit_find(void *c, const struct mrp_attr_status *st)
{
    struct find *f = c;
    if (st->attr_type == f->type && ((const uint8_t *)st->attr_val)[7] == f->sid) { f->reg = (int)st->reg; }
}
static int reg_of(struct mrp_app *a, uint8_t port, uint8_t type, unsigned sid)
{
    struct find f = {type, sid, -1};
    mrp_attr_visit(a, port, visit_find, &f);
    return f.reg;
}
static struct mrp_app *bridge(void)
{
    struct mrp_app *a = msrp_app_create(3, &ctx);
    for (uint8_t p = 0; p < 3; ++p) {
        mrp_port_configure(a, p, 20, 60, 10000, 1, true);
        mrp_set_periodic(a, p, false);
    }
    log_buf[0] = 0;
    return a;
}
static void poll_all(struct mrp_app *a)
{
    uint8_t tx[512];
    for (uint8_t p = 0; p < 3; ++p) { while (mrp_transmit(a, p, tx, sizeof tx, accept, NULL) == 1) { } }
}

int main(void)
{
    uint8_t pdu[128]; size_t n;

    /* F1: Flush! (mrp_port_role_change flush=true) under allocation faults.
     * Control k=0: immediate Leave indication and MT. For k>0 record whether the
     * flush is applied, reported or retried, and how long recovery takes when
     * the host keeps polling every port and ticking. */
    for (int k = 0; k <= 4; ++k) {
        struct mrp_app *a = bridge();
        n = talker_pdu(pdu, 1, 1, 1);
        mrp_rx(a, 0, pdu, n);
        poll_all(a);
        log_buf[0] = 0;
        probe_fail_at = k;
        mrp_port_role_change(a, 0, true);
        int left = probe_fail_at; /* nonzero: the fault was not reached */
        probe_fail_at = 0;
        int reg_now = reg_of(a, 0, 1, 1);
        int recovered = strstr(log_buf, "L1@0") ? 0 : -1;
        char first[128]; snprintf(first, sizeof first, "%s", log_buf);
        for (int t = 1; t <= 20000 && recovered < 0; ++t) {
            poll_all(a);
            shlan_timer_tick();
            if (strstr(log_buf, "L1@0")) { recovered = t; }
        }
        printf("INFO f1 k=%d fault_reached=%d immediate_log=[%s] reg_after_flush=%s leave_after_ticks=%d\n",
               k, k > 0 && left == 0, first, reg_now >= 0 ? mrp_reg_state_name((enum mrp_reg_state)reg_now) : "none",
               recovered);
        if (k == 0) {
            CHECK("f1-control-flush-immediate", recovered == 0 && reg_now == MRP_REG_STATE_MT);
        } else if (left == 0) {
            CHECK("f1-faulted-flush-applied-or-retried-within-1-tick", recovered >= 0 && recovered <= 1);
        }
        mrp_app_destroy(a);
    }

    /* F2: Talker Advertise replaced by Talker Failed (same StreamID) under faults.
     * Normal order is Leave(TA) before Join(TF). Sweep the fault position. */
    struct sig control;
    char control_log[512] = "";
    for (int k = 0; k <= 8; ++k) {
        struct mrp_app *a = bridge();
        n = talker_pdu(pdu, 1, 1, 1);
        mrp_rx(a, 0, pdu, n);
        poll_all(a);
        log_buf[0] = 0;
        n = talker_pdu(pdu, 2, 1, 1);
        probe_fail_at = k;
        int r = mrp_rx(a, 0, pdu, n);
        int left = probe_fail_at;
        probe_fail_at = 0;
        char first[256]; snprintf(first, sizeof first, "%s", log_buf);
        int r2 = 0;
        if (r < 0) { r2 = mrp_rx(a, 0, pdu, n); } /* documented identical retry */
        for (int t = 0; t < 80; ++t) { poll_all(a); shlan_timer_tick(); }
        poll_all(a);
        struct sig g; signature(a, &g);
        if (k == 0) { control = g; snprintf(control_log, sizeof control_log, "%s", log_buf); }
        char *l1 = strstr(log_buf, "L1@0"), *j2 = strstr(log_buf, "J2@0");
        printf("INFO f2 k=%d fault_reached=%d rx=%d retry=%d first=[%s] full=[%s]\n", k, k > 0 && left == 0, r, r2, first, log_buf);
        if (k == 0 || left == 0) {
            char name[64];
            snprintf(name, sizeof name, "f2-k%d-leave-ta-before-join-tf", k);
            CHECK(name, l1 && j2 && l1 < j2);
            snprintf(name, sizeof name, "f2-k%d-converges-to-control", k);
            CHECK(name, strcmp(g.s, control.s) == 0);
        }
        mrp_app_destroy(a);
    }
    printf("INFO f2 control state=[%s] log=[%s]\n", control.s, control_log);

    /* F3: multi-event PDU (Listener for a Talker registered on port 1, then a new
     * Talker) under every fault position; retry per contract and compare. */
    for (int k = 0; k <= 12; ++k) {
        struct mrp_app *a = bridge();
        n = talker_pdu(pdu, 1, 1, 1);
        mrp_rx(a, 1, pdu, n);
        poll_all(a);
        log_buf[0] = 0;
        n = mixed_pdu(pdu, 1, 2);
        probe_fail_at = k;
        int r = mrp_rx(a, 0, pdu, n);
        int left = probe_fail_at;
        probe_fail_at = 0;
        int r2 = 0;
        if (r < 0) { r2 = mrp_rx(a, 0, pdu, n); }
        for (int t = 0; t < 80; ++t) { poll_all(a); shlan_timer_tick(); }
        struct sig g; signature(a, &g);
        if (k == 0) { control = g; }
        printf("INFO f3 k=%d fault_reached=%d rx=%d retry=%d log=[%s]\n", k, k > 0 && left == 0, r, r2, log_buf);
        if (k == 0 || left == 0) {
            char name[64];
            snprintf(name, sizeof name, "f3-k%d-converges-to-control", k);
            CHECK(name, r2 == 0 && strcmp(g.s, control.s) == 0);
            if (strcmp(g.s, control.s) != 0) { printf("INFO f3 k=%d state=[%s]\n", k, g.s); }
        }
        mrp_app_destroy(a);
    }
    printf("INFO f3 control state=[%s]\n", control.s);

    printf("probe failures: %d\n", fails);
    return fails != 0;
}
