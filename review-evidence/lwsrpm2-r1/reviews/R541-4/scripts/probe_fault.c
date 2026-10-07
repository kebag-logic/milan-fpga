/* SPDX-License-Identifier: Apache-2.0 */
/* Independent public-API fault sweeps. Compile with the replaceable allocation port. */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "shish_lan/msrp.h"
#include "shish_lan/mrp_pdu.h"
#include "ports/timer.h"
#include "fault_alloc.h"

static unsigned joins, leaves, policies, order_errors, failures, checks;
#define CHECK(x) do { ++checks; if (!(x)) { ++failures; printf("FAIL line %d: %s\n", __LINE__, #x); } } while (0)
static unsigned value(uint8_t t, const void *v)
{
    return t == 3 ? ((const unsigned char *)v)[8] : ((const struct msrp_talker_adv *)v)->max_frame_size;
}
static void join_cb(struct mrp_app *a, uint8_t p, uint8_t t, const void *v, bool n)
{
    (void)a; (void)p; (void)t; (void)v; (void)n;
    ++joins;
}
static void leave_cb(struct mrp_app *a, uint8_t p, uint8_t t, const void *v)
{
    (void)a; (void)p; (void)t; (void)v;
    ++leaves;
}
static uint32_t policy(const struct mrp_app *a, uint8_t p, uint8_t t, const void *v)
{
    (void)a; (void)p; (void)t; (void)v;
    ++policies;
    order_errors += policies != joins + leaves;
    return 6;
}
static int accept(void *c, uint8_t p, const uint8_t *b, size_t n)
{
    (void)c; (void)p; (void)b; (void)n;
    return 0;
}
static int refuse(void *c, uint8_t p, const uint8_t *b, size_t n)
{
    (void)c; (void)p; (void)b; (void)n;
    return -1;
}
static void ticks(unsigned n)
{
    while (n--) {
        shlan_timer_tick();
    }
}
static struct mrp_app *create(unsigned la)
{
    struct msrp_ctx ctx = {0};
    struct mrp_app *base = msrp_app_create(1, &ctx);
    CHECK(base != NULL);
    struct mrp_app_ops ops = *base->ops;
    mrp_app_destroy(base);
    ops.ctx = NULL;
    ops.join_ind = join_cb; ops.leave_ind = leave_cb;
    ops.map_join = policy; ops.map_leave = policy;
    struct mrp_app *a = mrp_app_create(&ops, 3);
    CHECK(a != NULL);
    for (uint8_t p = 0; p < 3; ++p) {
        CHECK(mrp_port_configure(a, p, 1, 10, p ? 10000 : la, 1, true) == 0);
        mrp_set_periodic(a, p, false);
    }
    joins = leaves = policies = order_errors = 0;
    return a;
}
static size_t pdu(struct mrp_app *a, uint8_t *b, uint8_t type, unsigned v, unsigned ev, bool la)
{
    struct msrp_talker_failed tf = {0};
    unsigned char listener[9] = {0};
    tf.talker.stream_id.bytes[7] = 42;
    tf.talker.vlan_id = 2;
    tf.talker.max_frame_size = (uint16_t)v;
    listener[7] = 42; listener[8] = (unsigned char)v;
    unsigned len = a->ops->attr_len(type), sub = type == 3;
    unsigned list = 2 + len + 1 + sub + 2;
    memset(b, 0, 128);
    b[1] = type; b[2] = (uint8_t)len; b[4] = (uint8_t)list;
    b[5] = la ? 0x20 : 0; b[6] = 1;
    CHECK(a->ops->encode_attr(type, type == 3 ? (void *)listener : (void *)&tf, b + 7, len) == (int)len);
    b[7 + len] = (uint8_t)(36 * ev);
    if (sub) {
        b[8 + len] = (uint8_t)(v << 6);
    }
    return 7 + list;
}
struct snapshot { unsigned type, v, found; enum mrp_reg_state reg; enum mrp_appl_state appl; };
static void visit(void *raw, const struct mrp_attr_status *s)
{
    struct snapshot *r = raw;
    if (s->attr_type == r->type) {
        r->v = value(s->attr_type, s->attr_val); r->reg = s->reg; r->appl = s->appl; ++r->found;
    }
}
static struct snapshot state(struct mrp_app *a, unsigned p, unsigned type)
{
    struct snapshot r = {.type = type};
    CHECK(mrp_attr_visit(a, p, visit, &r) >= 0);
    return r;
}
static void destroy(struct mrp_app *a)
{
    allocation_fail_after(0);
    CHECK(order_errors == 0);
    mrp_app_destroy(a);
    CHECK(allocation_live() == 0);
    ticks(20);
}
static void enter_lv(struct mrp_app *a, unsigned path, unsigned type, unsigned old)
{
    uint8_t b[128], tx[256];
    if (path == 1) {
        size_t n = pdu(a, b, type, old, 4, true);
        CHECK(mrp_rx(a, 0, b, n) == 0);
    } else if (path == 2) {
        ticks(6);
        CHECK(mrp_transmit(a, 0, tx, sizeof(tx), accept, NULL) == 1);
    }
    CHECK(state(a, 0, type).reg == (path ? MRP_REG_STATE_LV : MRP_REG_STATE_IN));
}
static void update_sweep(void)
{
    for (unsigned type = 1; type <= 3; ++type) {
        for (unsigned event = 1; event <= 3; event += 2) {
            for (unsigned path = 0; path < 3; ++path) {
                for (unsigned fail = 1; fail <= 3; ++fail) {
                    struct mrp_app *a = create(path == 2 ? 4 : 10000);
                    unsigned old = type == 3 ? 2 : 100, next = type == 3 ? 1 : 200;
                    uint8_t b[128]; size_t n = pdu(a, b, type, old, event, false);
                    CHECK(mrp_rx(a, 0, b, n) == 0);
                    enter_lv(a, path, type, old);
                    struct snapshot before = state(a, 0, type);
                    size_t live = allocation_live();
                    n = pdu(a, b, type, next, event, false);
                    allocation_fail_after(fail);
                    CHECK(mrp_rx(a, 0, b, n) == -12);
                    CHECK(joins == 1 && policies == 1 && leaves == 0);
                    CHECK(state(a, 0, type).v == old);
                    CHECK(state(a, 0, type).reg == before.reg);
                    CHECK(state(a, 0, type).appl == before.appl);
                    CHECK(allocation_live() == live);
                    for (unsigned p = 1; p < 3; ++p) { CHECK(state(a, p, type).v == old); }
                    CHECK(mrp_rx(a, 0, b, n) == 0);
                    CHECK(joins == 2 && policies == 2);
                    for (unsigned p = 0; p < 3; ++p) { CHECK(state(a, p, type).v == next); }
                    CHECK(mrp_rx(a, 0, b, n) == 0);
                    ticks(11);
                    CHECK(joins == 2 && leaves == 0 && state(a, 0, type).reg == MRP_REG_STATE_IN);
                    destroy(a);
                }
            }
        }
    }
    printf("completed 54 changed-value allocation cases\n");
}
static void unchanged_sweep(void)
{
    for (unsigned type = 1; type <= 3; ++type) {
        for (unsigned event = 1; event <= 3; event += 2) {
            for (unsigned path = 1; path <= 2; ++path) {
                struct mrp_app *a = create(path == 2 ? 4 : 10000);
                uint8_t b[128]; unsigned v = type == 3 ? 2 : 100;
                size_t n = pdu(a, b, type, v, event, false);
                CHECK(mrp_rx(a, 0, b, n) == 0);
                enter_lv(a, path, type, v);
                allocation_fail_after(1);
                CHECK(mrp_rx(a, 0, b, n) == 0);
                allocation_fail_after(0);
                ticks(11);
                CHECK(joins == 1 && leaves == 0 && policies == 1);
                CHECK(state(a, 0, type).reg == MRP_REG_STATE_IN);
                destroy(a);
            }
        }
    }
    printf("completed 12 unchanged LV recovery cases\n");
}
static void timer_and_queue(void)
{
    struct mrp_app *a = create(10000);
    uint8_t b[128], tx[256], saved[256];
    struct msrp_domain domain = {6, 3, 2};
    CHECK(mrp_mad_join(a, 1, 4, &domain, true) == 0);
    CHECK(mrp_transmit(a, 1, tx, sizeof(tx), refuse, NULL) == -1);
    memcpy(saved, tx, sizeof(tx));
    size_t n = pdu(a, b, 1, 100, 1, false);
    CHECK(mrp_rx(a, 0, b, n) == 0);
    n = pdu(a, b, 1, 200, 1, false);
    CHECK(mrp_rx(a, 0, b, n) == 0);
    n = pdu(a, b, 1, 200, 4, true);
    CHECK(mrp_rx(a, 0, b, n) == 0);
    ticks(9);
    for (unsigned i = 0; i < 5; ++i) {
        allocation_fail_after(i % 3 + 1); ticks(1);
        CHECK(leaves == 0 && state(a, 0, 1).reg == MRP_REG_STATE_LV);
    }
    ticks(1);
    CHECK(leaves == 1 && state(a, 0, 1).reg == MRP_REG_STATE_MT);
    allocation_fail_after(1);
    CHECK(mrp_transmit(a, 1, tx, sizeof(tx), accept, NULL) == 1);
    CHECK(memcmp(tx, saved, sizeof(tx)) == 0);
    CHECK(state(a, 1, 1).found == 0);
    allocation_fail_after(1);
    (void)mrp_transmit(a, 1, tx, sizeof(tx), accept, NULL);
    CHECK(state(a, 1, 1).found == 0);
    (void)mrp_transmit(a, 1, tx, sizeof(tx), accept, NULL);
    CHECK(state(a, 1, 1).v == 200 && state(a, 1, 1).appl == MRP_APPL_STATE_VO);
    CHECK(state(a, 2, 1).v == 200 && state(a, 2, 1).appl == MRP_APPL_STATE_VO);
    destroy(a);
    printf("completed repeated timer exhaustion and retained FIFO replay\n");
}
int main(void)
{
    update_sweep(); unchanged_sweep(); timer_and_queue();
    printf("checks=%u failures=%u live=%zu\n", checks, failures, allocation_live());
    return failures != 0;
}
