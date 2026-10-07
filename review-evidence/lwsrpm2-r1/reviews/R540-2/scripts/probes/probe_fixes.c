/* SPDX-License-Identifier: Apache-2.0 */
/* Reviewer probes for the round-3 receive fixes, using cases not in the upstream tests. */
#include <stdio.h>
#include <string.h>
#include "shish_lan/mmrp.h"
#include "shish_lan/msrp.h"
#include "shish_lan/mvrp.h"

static unsigned inds;
static void on_listener(struct msrp_ctx *c, uint8_t p, const struct msrp_stream_id *s,
                        enum msrp_listener_decl d, bool n)
{
    (void)c; (void)p; (void)s; (void)d; (void)n; ++inds;
}
static void on_domain(struct msrp_ctx *c, uint8_t p, const struct msrp_domain *d, bool n)
{
    (void)c; (void)p; (void)d; (void)n; ++inds;
}
static void on_vlan(struct mvrp_ctx *c, uint8_t p, uint16_t v, bool n)
{
    (void)c; (void)p; (void)v; (void)n; ++inds;
}
static void on_mac(struct mmrp_ctx *c, uint8_t p, const struct mmrp_mac *m)
{
    (void)c; (void)p; (void)m; ++inds;
}
static int fails;
#define CHECK(name, cond) do { int ok_ = (cond); printf("%s %s\n", ok_ ? "PASS" : "FAIL", name); fails += !ok_; } while (0)
static unsigned count(struct mrp_app *a) { return (unsigned)mrp_attr_visit(a, 0, NULL, NULL); }

int main(void)
{
    struct msrp_ctx sc = { .on_listener = on_listener, .on_domain = on_domain };
    struct mvrp_ctx vc = { .on_vlan_registered = on_vlan };
    struct mmrp_ctx mc = { .on_mac_registered = on_mac };
    struct mrp_app *a;
    int r;

    /* Listener vector of three values from unique ID 0xFFFE: the third wraps. A valid Listener precedes it. */
    inds = 0; a = msrp_app_create(1, &sc);
    uint8_t wrap[] = {0, 3, 8, 0, 14, 0, 1, 9, 9, 9, 9, 9, 9, 0, 1, 36, 128, 0, 0,
                      3, 8, 0, 14, 0, 3, 1, 2, 3, 4, 5, 6, 0xFF, 0xFE, 43, 168, 0, 0, 0, 0};
    r = mrp_rx(a, 0, wrap, sizeof(wrap));
    CHECK("listener-three-value-wrap-rejected-atomically", r < 0 && inds == 0 && count(a) == 0);
    wrap[32] = 0xFD; /* last value is now 0xFFFF */
    r = mrp_rx(a, 0, wrap, sizeof(wrap));
    CHECK("listener-three-value-maximum-accepted", r == 0 && inds == 4 && count(a) == 4);
    mrp_app_destroy(a);

    /* Domain class 251 with six values overflows the class octet after a valid Listener. */
    inds = 0; a = msrp_app_create(1, &sc);
    uint8_t dom[] = {0, 3, 8, 0, 14, 0, 1, 9, 9, 9, 9, 9, 9, 0, 1, 36, 128, 0, 0,
                     4, 4, 0, 10, 0, 6, 251, 0, 0, 2, 37, 37, 0, 0, 0, 0};
    r = mrp_rx(a, 0, dom, sizeof(dom));
    CHECK("domain-class-overflow-rejected-atomically", r < 0 && inds == 0 && count(a) == 0);
    mrp_app_destroy(a);

    /* VLAN: later version, unknown type 7 with AttributeLength 4, then VID 5. */
    inds = 0; a = mvrp_app_create(1, &vc);
    uint8_t vlan[] = {1, 7, 4, 0, 1, 1, 2, 3, 4, 36, 0, 0,
                      1, 2, 0, 1, 0, 5, 36, 0, 0, 0, 0};
    r = mrp_rx(a, 0, vlan, sizeof(vlan));
    CHECK("vlan-later-unknown-length4-skipped", r == 0 && inds == 1 && count(a) == 1);
    vlan[0] = 0;
    mrp_app_destroy(a); inds = 0; a = mvrp_app_create(1, &vc);
    r = mrp_rx(a, 0, vlan, sizeof(vlan));
    CHECK("vlan-current-unknown-rejected", r < 0 && inds == 0 && count(a) == 0);
    mrp_app_destroy(a);

    /* MAC: later version, unknown type 5 with AttributeLength 3, then one MAC. */
    inds = 0; a = mmrp_app_create(1, &mc);
    uint8_t mac[] = {1, 5, 3, 0, 1, 1, 2, 3, 36, 0, 0,
                     2, 6, 0, 1, 0x01, 0x00, 0x5E, 0, 0, 1, 36, 0, 0, 0, 0};
    r = mrp_rx(a, 0, mac, sizeof(mac));
    CHECK("mac-later-unknown-length3-skipped", r == 0 && inds == 1 && count(a) == 1);
    mrp_app_destroy(a);

    /* MAC: later version, unknown event 250 in the first vector, valid second vector. */
    inds = 0; a = mmrp_app_create(1, &mc);
    uint8_t ev[] = {1, 2, 6, 0, 1, 0x01, 0x00, 0x5E, 0, 0, 2, 250,
                    0, 1, 0x01, 0x00, 0x5E, 0, 0, 3, 36, 0, 0, 0, 0};
    r = mrp_rx(a, 0, ev, sizeof(ev));
    CHECK("mac-later-unknown-event-vector-skipped", r == 0 && inds == 1 && count(a) == 1);
    mrp_app_destroy(a);

    printf("probe failures: %d\n", fails);
    return fails != 0;
}
