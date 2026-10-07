/* SPDX-License-Identifier: Apache-2.0 */
/* Reviewer probes (R540-3): discriminate surviving plants y01, y02 and y07.
 * Linked with probe_alloc.c. */
#include <stdio.h>
#include <string.h>
#include "shish_lan/error.h"
#include "shish_lan/msrp.h"
#include "shish_lan/mvrp.h"
#include "ports/timer.h"

extern int probe_fail_at;
static unsigned talker_inds;
static void on_ta(struct msrp_ctx *c, uint8_t p, const struct msrp_talker_adv *t, bool n)
{ (void)c; (void)p; (void)t; (void)n; ++talker_inds; }
static struct msrp_ctx ctx = { .on_talker_advertise = on_ta };
static int fails;
#define CHECK(name, cond) do { int ok_ = (cond); printf("%s %s\n", ok_ ? "PASS" : "FAIL", name); fails += !ok_; } while (0)

struct find { uint8_t type; unsigned sid; int appl; };
static void visit_find(void *c, const struct mrp_attr_status *st)
{
    struct find *f = c;
    if (st->attr_type == f->type && ((const uint8_t *)st->attr_val)[7] == f->sid) { f->appl = (int)st->appl; }
}
static int appl_of(struct mrp_app *a, uint8_t port, uint8_t type, unsigned sid)
{
    struct find f = {type, sid, -1};
    mrp_attr_visit(a, port, visit_find, &f);
    return f.appl;
}
static int declared(struct mrp_app *a, uint8_t port, uint8_t type, unsigned sid)
{
    int s = appl_of(a, port, type, sid);
    return s >= 0 && s != MRP_APPL_STATE_VO && s != MRP_APPL_STATE_AO && s != MRP_APPL_STATE_QO;
}
static struct mrp_app *bridge(void)
{
    struct mrp_app *a = msrp_app_create(3, &ctx);
    for (uint8_t p = 0; p < 3; ++p) {
        mrp_port_configure(a, p, 20, 60, 10000, 1, true);
        mrp_set_periodic(a, p, false);
    }
    talker_inds = 0;
    return a;
}
/* Talker Advertise JoinIn messages for stream ids s1 and (if nonzero) s2. */
static size_t talkers(uint8_t *b, unsigned s1, unsigned s2)
{
    size_t n = 0;
    b[n++] = 0;
    for (int i = 0; i < 2; ++i) {
        unsigned sid = i ? s2 : s1;
        if (!sid) { continue; }
        uint8_t m[] = {1, 25, 0, 30, 0, 1, 0, 0, 0, 0, 0, 0, 0, (uint8_t)sid, 0x91, 0, 0, 0, 0, 0, 0, 2, 0, 100,
                       0, 1, 0x70, 0, 0, 0, 0, 36, 0, 0};
        memcpy(b + n, m, sizeof m); n += sizeof m;
    }
    b[n++] = 0; b[n++] = 0;
    return n;
}

int main(void)
{
    uint8_t pdu[128]; size_t n;

    /* y02: Talker from port 0 must not be declared back on port 0 (policy excludes the source). */
    struct mrp_app *a = bridge();
    n = talkers(pdu, 1, 0);
    CHECK("q1-rx", mrp_rx(a, 0, pdu, n) == 0);
    CHECK("q1-propagated-to-1-and-2", declared(a, 1, 1, 1) && declared(a, 2, 1, 1));
    CHECK("q1-not-declared-on-source", !declared(a, 0, 1, 1));
    /* Listener from port 2 for that stream goes only toward the Talker (port 0), not port 1. */
    uint8_t li[] = {0, 3, 8, 0, 14, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 36, 2u << 6, 0, 0, 0, 0};
    CHECK("q2-listener-rx", mrp_rx(a, 2, li, sizeof li) == 0);
    CHECK("q2-listener-toward-talker", declared(a, 0, 3, 1));
    CHECK("q2-listener-not-to-port-1", !declared(a, 1, 3, 1));
    mrp_app_destroy(a);

    /* y01: a reservation failure on the first message stops the rest of the payload. */
    a = bridge();
    n = talkers(pdu, 1, 2);
    probe_fail_at = 2; /* first instance, then the first reservation fails */
    int r = mrp_rx(a, 0, pdu, n);
    probe_fail_at = 0;
    printf("INFO q3 rx=%d talker_inds=%u stream2_appl_port1=%d\n", r, talker_inds, appl_of(a, 1, 1, 2));
    CHECK("q3-error-reported", r == -SHLAN_ERROR_NO_MEMORY);
    CHECK("q3-later-message-not-applied", talker_inds == 0 && !declared(a, 1, 1, 2));
    CHECK("q3-retry", mrp_rx(a, 0, pdu, n) == 0 && talker_inds == 2);
    mrp_app_destroy(a);

    /* y07: an application without propagation policy reserves nothing, so a
     * second allocation fault cannot refuse a VLAN registration. */
    struct mvrp_ctx vctx = {0};
    a = mvrp_app_create(3, &vctx);
    uint8_t vlan[] = {0, 1, 2, 0, 1, 0, 2, 36, 0, 0, 0, 0};
    probe_fail_at = 2;
    r = mrp_rx(a, 0, vlan, sizeof vlan);
    probe_fail_at = 0;
    printf("INFO q4 rx=%d\n", r);
    CHECK("q4-no-policy-no-reservation", r == 0);
    mrp_app_destroy(a);

    printf("probe failures: %d\n", fails);
    return fails != 0;
}
