/* SPDX-License-Identifier: Apache-2.0 */
/* Reviewer probes: deferred propagation, retention and allocation failure.
 * Linked with probe_alloc.c instead of the hosted allocation port. */
#include <stdio.h>
#include <string.h>
#include "shish_lan/error.h"
#include "shish_lan/msrp.h"
#include "ports/timer.h"

extern int probe_fail_at; /* fail the Nth following calloc/malloc; 0 disables */

static unsigned talker_inds, leave_inds;
static void on_talker(struct msrp_ctx *c, uint8_t p, const struct msrp_talker_adv *t, bool n)
{
    (void)c; (void)t; (void)n; if (p == 0) { ++talker_inds; }
}
static void on_leave(struct msrp_ctx *c, uint8_t p, uint8_t t, const void *v)
{
    (void)c; (void)t; (void)v; if (p == 0) { ++leave_inds; }
}
static struct msrp_ctx ctx = { .on_talker_advertise = on_talker, .on_leave = on_leave };
static int fails;
#define CHECK(name, cond) do { int ok_ = (cond); printf("%s %s\n", ok_ ? "PASS" : "FAIL", name); fails += !ok_; } while (0)

static size_t talker_pdu(uint8_t *b, unsigned event)
{
    uint8_t p[37] = {0, 1, 25, 0, 30, 0, 1};
    p[7] = 1; p[15] = 0x91; p[22] = 2; p[24] = 100; p[26] = 1; p[27] = 0x70;
    p[32] = (uint8_t)(event * 36u);
    memcpy(b, p, sizeof(p));
    return sizeof(p);
}
struct st { unsigned count; enum mrp_appl_state appl; enum mrp_reg_state reg; };
static void visit(void *c, const struct mrp_attr_status *s)
{
    struct st *st = c;
    if (s->attr_type == 1) { ++st->count; st->appl = s->appl; st->reg = s->reg; }
}
static struct st state(struct mrp_app *a, uint8_t p)
{
    struct st st = {0};
    mrp_attr_visit(a, p, visit, &st);
    return st;
}
static int accept(void *c, uint8_t p, const uint8_t *d, size_t n) { (void)c; (void)p; (void)d; (void)n; return 0; }
static int refuse(void *c, uint8_t p, const uint8_t *d, size_t n) { (void)c; (void)p; (void)d; (void)n; return -1; }

static struct mrp_app *bridge(void)
{
    struct mrp_app *a = msrp_app_create(3, &ctx);
    for (uint8_t p = 0; p < 3; ++p) {
        mrp_port_configure(a, p, 20, 60, 10000, 1, true);
        mrp_set_periodic(a, p, false);
    }
    talker_inds = leave_inds = 0;
    return a;
}
static void retain(struct mrp_app *a, uint8_t port, uint8_t *tx, size_t n)
{
    struct msrp_domain d = {6, 3, 2};
    mrp_mad_join(a, port, MSRP_ATTR_TYPE_DOMAIN, &d, true);
    mrp_transmit(a, port, tx, n, refuse, NULL);
}

int main(void)
{
    uint8_t pdu[64], tx1[256], tx2[256]; size_t n;

    /* M1: three ports; port 1 retains; Join then timer/immediate Leave propagate. */
    struct mrp_app *a = bridge();
    retain(a, 1, tx1, sizeof(tx1));
    n = talker_pdu(pdu, 1);
    CHECK("m1-join-rx", mrp_rx(a, 0, pdu, n) == 0 && talker_inds == 1);
    CHECK("m1-free-port-declares-now", state(a, 2).count == 1);
    CHECK("m1-retaining-port-deferred", state(a, 1).count == 0);
    n = talker_pdu(pdu, 5);
    CHECK("m1-leave-rx", mrp_rx(a, 0, pdu, n) == 0);
    shlan_timer_tick(); for (int i = 0; i < 70; ++i) { shlan_timer_tick(); }
    CHECK("m1-leave-indicated", leave_inds == 1);
    CHECK("m1-retaining-port-still-deferred", state(a, 1).count == 0);
    CHECK("m1-commit", mrp_transmit(a, 1, tx1, sizeof(tx1), accept, NULL) == 1);
    struct st s1 = state(a, 1), s2 = state(a, 2);
    printf("INFO m1 port1 appl=%s port2 appl=%s\n", mrp_appl_state_name(s1.appl), mrp_appl_state_name(s2.appl));
    CHECK("m1-replayed-in-order-matches-free-port", s1.count == 1 && s1.appl == s2.appl);
    mrp_app_destroy(a);

    /* M2: source-side queue allocation fails on the second destination. */
    a = bridge();
    n = talker_pdu(pdu, 1);
    probe_fail_at = 3; /* instance, port 1 work, port 2 work */
    int r = mrp_rx(a, 0, pdu, n);
    probe_fail_at = 0;
    printf("INFO m2 rx=%d inds=%u p0reg=%s\n", r, talker_inds, mrp_reg_state_name(state(a, 0).reg));
    CHECK("m2-error-returned", r == -SHLAN_ERROR_NO_MEMORY);
    CHECK("m2-no-indication", talker_inds == 0);
    CHECK("m2-registrar-not-in", state(a, 0).reg != MRP_REG_STATE_IN);
    mrp_transmit(a, 1, tx1, sizeof(tx1), accept, NULL);
    mrp_transmit(a, 2, tx2, sizeof(tx2), accept, NULL);
    CHECK("m2-no-partial-propagation", state(a, 1).count == 0 && state(a, 2).count == 0);
    CHECK("m2-retry-succeeds", mrp_rx(a, 0, pdu, n) == 0 && talker_inds == 1 &&
          state(a, 1).count == 1 && state(a, 2).count == 1);
    mrp_app_destroy(a);

    /* M3: destination allocation fails during replay; work is retained for the next poll. */
    a = bridge();
    retain(a, 1, tx1, sizeof(tx1));
    n = talker_pdu(pdu, 1);
    mrp_rx(a, 0, pdu, n);
    probe_fail_at = 1;
    r = mrp_transmit(a, 1, tx1, sizeof(tx1), accept, NULL);
    probe_fail_at = 0;
    CHECK("m3-commit-accepted", r == 1);
    CHECK("m3-replay-retained", state(a, 1).count == 0);
    mrp_transmit(a, 1, tx1, sizeof(tx1), accept, NULL);
    CHECK("m3-next-poll-replays", state(a, 1).count == 1);
    mrp_app_destroy(a);

    /* M4: leave-timer propagation allocation fails; the registrar retries. */
    a = bridge();
    n = talker_pdu(pdu, 1); mrp_rx(a, 0, pdu, n);
    n = talker_pdu(pdu, 5);
    probe_fail_at = LWSRP_MILAN ? 1 : 0;
    r = mrp_rx(a, 0, pdu, n);
    probe_fail_at = 0;
    if (LWSRP_MILAN) {
        CHECK("m4-milan-error-returned", r == -SHLAN_ERROR_NO_MEMORY && leave_inds == 0 &&
              state(a, 0).reg == MRP_REG_STATE_IN);
        CHECK("m4-milan-retry", mrp_rx(a, 0, pdu, n) == 0 && leave_inds == 1);
    } else {
        for (int i = 0; i < 59; ++i) { shlan_timer_tick(); }
        probe_fail_at = 1;
        shlan_timer_tick(); /* the leave timer expires on this tick */
        probe_fail_at = 0;
        printf("INFO m4 after failing expiry leave_inds=%u reg=%s\n", leave_inds,
               mrp_reg_state_name(state(a, 0).reg));
        CHECK("m4-timer-failure-keeps-lv", leave_inds == 0 && state(a, 0).reg == MRP_REG_STATE_LV);
        shlan_timer_tick(); shlan_timer_tick();
        CHECK("m4-timer-retry", leave_inds == 1 && state(a, 0).reg == MRP_REG_STATE_MT);
    }
    CHECK("m4-ports-withdrawn", state(a, 1).appl != MRP_APPL_STATE_QA && state(a, 2).appl != MRP_APPL_STATE_QA);
    mrp_app_destroy(a);

    /* M5: destroy with queued work (leak check by the sanitizer at exit). */
    a = bridge();
    retain(a, 1, tx1, sizeof(tx1));
    n = talker_pdu(pdu, 1); mrp_rx(a, 0, pdu, n);
    mrp_app_destroy(a);

    printf("probe failures: %d\n", fails);
    return fails != 0;
}
