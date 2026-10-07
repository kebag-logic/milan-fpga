/* SPDX-License-Identifier: Apache-2.0 */
/* Reviewer probes (R540-3): R541-2-F1 changed-value retry under every fault
 * position, and R541-2-F2 policy after indication. Linked with probe_alloc.c. */
#include <stdio.h>
#include <string.h>
#include "shish_lan/error.h"
#include "shish_lan/msrp.h"
#include "ports/timer.h"

extern int probe_fail_at;
static int fails;
#define CHECK(name, cond) do { int ok_ = (cond); printf("%s %s\n", ok_ ? "PASS" : "FAIL", name); fails += !ok_; } while (0)
static struct msrp_ctx ctx;

static size_t talker_pdu(uint8_t *b, unsigned frame)
{
    uint8_t p[37] = {0, 1, 25, 0, 30, 0, 1};
    p[7] = 1; p[15] = 0x91; p[22] = 2; p[23] = (uint8_t)(frame >> 8); p[24] = (uint8_t)frame;
    p[26] = 1; p[27] = 0x70; p[32] = 36;
    memcpy(b, p, sizeof(p));
    return sizeof(p);
}
struct fv { int frame; int appl; };
static void visit(void *c, const struct mrp_attr_status *s)
{
    struct fv *f = c;
    if (s->attr_type == 1) { f->frame = ((const struct msrp_talker_adv *)s->attr_val)->max_frame_size; f->appl = s->appl; }
}
static struct fv value(struct mrp_app *a, uint8_t p)
{
    struct fv f = {-1, -1};
    mrp_attr_visit(a, p, visit, &f);
    return f;
}
static int accept(void *c, uint8_t p, const uint8_t *d, size_t n) { (void)c; (void)p; (void)d; (void)n; return 0; }

static unsigned host_joined;
static void host_join(struct mrp_app *a, uint8_t p, uint8_t t, const void *v, bool n)
{ (void)a; (void)p; (void)t; (void)v; (void)n; ++host_joined; }
static uint32_t policy(const struct mrp_app *a, uint8_t p, uint8_t t, const void *v)
{ (void)a; (void)p; (void)t; (void)v; return host_joined ? 2u : 0u; }

int main(void)
{
    uint8_t pdu[64], tx[256];
    /* R541-2-F1: Talker 100 -> 200 with a failure at each allocation position. */
    for (int k = 0; k <= 4; ++k) {
        struct mrp_app *a = msrp_app_create(2, &ctx);
        for (uint8_t p = 0; p < 2; ++p) { mrp_port_configure(a, p, 20, 60, 10000, 1, true); mrp_set_periodic(a, p, false); }
        size_t n = talker_pdu(pdu, 100);
        mrp_rx(a, 0, pdu, n);
        n = talker_pdu(pdu, 200);
        probe_fail_at = k;
        int r = mrp_rx(a, 0, pdu, n);
        int left = probe_fail_at;
        probe_fail_at = 0;
        int r2 = r < 0 ? mrp_rx(a, 0, pdu, n) : 0;
        for (int t = 0; t < 100; ++t) { mrp_transmit(a, 1, tx, sizeof tx, accept, NULL); shlan_timer_tick(); }
        printf("INFO f1 k=%d fault_reached=%d rx=%d retry=%d source=%d destination=%d\n", k, k > 0 && left == 0, r, r2,
               value(a, 0).frame, value(a, 1).frame);
        char name[64];
        snprintf(name, sizeof name, "r541-2-f1-k%d-destination-holds-200", k);
        CHECK(name, r2 == 0 && value(a, 0).frame == 200 && value(a, 1).frame == 200);
        mrp_app_destroy(a);
    }
    /* R541-2-F2: policy enables port 1 only once the host indication has run. */
    struct mrp_app *proto = msrp_app_create(1, &ctx);
    struct mrp_app_ops ops = *proto->ops;
    mrp_app_destroy(proto);
    ops.join_ind = host_join; ops.map_join = policy; ops.map_leave = NULL; ops.ctx = NULL;
    struct mrp_app *a = mrp_app_create(&ops, 2);
    size_t n = talker_pdu(pdu, 100);
    host_joined = 0;
    CHECK("r541-2-f2-rx", mrp_rx(a, 0, pdu, n) == 0 && host_joined == 1);
    CHECK("r541-2-f2-policy-saw-indication", value(a, 1).frame == 100);
    mrp_app_destroy(a);
    printf("probe failures: %d\n", fails);
    return fails != 0;
}
