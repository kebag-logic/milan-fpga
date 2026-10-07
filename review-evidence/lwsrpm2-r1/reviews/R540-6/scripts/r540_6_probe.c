/* SPDX-License-Identifier: Apache-2.0 */
/* Internal reviewer probe for pending Flush storage paths. Public interface
 * plus the repository fault-injecting allocation port. Each scenario runs a
 * no-fault control (fault 0) and every Flush reservation fault (1..3), and
 * compares the recorded indication sequence against the documented rule. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "shish_lan/msrp.h"
#include "shish_lan/error.h"
#include "ports/timer.h"
#include "fault_alloc.h"

static unsigned checks, failures, scenario;
static char tag[160];
#define CHECK(x) do { ++checks; if (!(x)) { ++failures; \
    printf("FAIL %s line=%d: %s\n", tag, __LINE__, #x); } } while (0)

/* Indication log: port, kind (type for Join, 10+type for Leave), value. */
static unsigned n_ind, ind_port[64], ind_kind[64], ind_val[64];
static unsigned n_map, map_port[64], map_type[64], map_val[64];
static unsigned obs_lv_mt_val, obs_lv_mt_count;
static uint32_t (*prod_leave)(const struct mrp_app *, uint8_t, uint8_t, const void *);

static unsigned val(unsigned type, const void *v)
{
    if (type == MSRP_ATTR_TYPE_LISTENER) {
        return ((const uint8_t *)v)[8];
    }
    return ((const struct msrp_talker_adv *)v)->max_frame_size;
}
static void joined(struct mrp_app *a, uint8_t p, uint8_t t, const void *v, bool n)
{
    (void)a; (void)n;
    if (t == MSRP_ATTR_TYPE_DOMAIN || n_ind >= 64) { return; }
    ind_port[n_ind] = p; ind_kind[n_ind] = t; ind_val[n_ind++] = val(t, v);
}
static void left(struct mrp_app *a, uint8_t p, uint8_t t, const void *v)
{
    (void)a;
    if (t == MSRP_ATTR_TYPE_DOMAIN || n_ind >= 64) { return; }
    ind_port[n_ind] = p; ind_kind[n_ind] = 10u + t; ind_val[n_ind++] = val(t, v);
}
static uint32_t mapped_leave(const struct mrp_app *a, uint8_t p, uint8_t t, const void *v)
{
    if (n_map < 64) { map_port[n_map] = p; map_type[n_map] = t; map_val[n_map++] = val(t, v); }
    return prod_leave(a, p, t, v);
}
static void observe(void *ctx, const struct mrp_transition *t)
{
    (void)ctx;
    if (t->port_id == 0 && t->reg_from == MRP_REG_STATE_LV && t->reg_to == MRP_REG_STATE_MT) {
        obs_lv_mt_val = val(t->attr_type, t->attr_val);
        ++obs_lv_mt_count;
    }
}
/* One-value MSRP PDU: type 1 TA, 2 TF, 3 Listener; sid is the last StreamID
 * octet; value is MaxFrameSize (Talkers) or the Listener declaration. */
static size_t wire(uint8_t *b, unsigned type, unsigned sid, unsigned value, unsigned event, unsigned la)
{
    unsigned n = type == 1 ? 25 : type == 2 ? 34 : 8;
    unsigned list = 2 + n + 1 + (type == 3) + 2;
    memset(b, 0, 96);
    b[1] = (uint8_t)type; b[2] = (uint8_t)n; b[4] = (uint8_t)list; b[5] = la ? 32 : 0; b[6] = 1;
    b[7] = 0x11; b[14] = (uint8_t)sid;
    if (type == 3) { b[16] = (uint8_t)(value << 6); }
    else { b[23] = (uint8_t)(value >> 8); b[24] = (uint8_t)value; }
    b[7 + n] = (uint8_t)(36 * event);
    return list + 7;
}
static struct mrp_app *setup(void)
{
    struct msrp_ctx ctx = {0};
    struct mrp_app *tmp = msrp_app_create(3, &ctx);
    struct mrp_app_ops ops = *tmp->ops;
    mrp_app_destroy(tmp);
    ops.join_ind = joined; ops.leave_ind = left; ops.ctx = NULL;
    prod_leave = ops.map_leave; ops.map_leave = mapped_leave;
    struct mrp_app *a = mrp_app_create(&ops, 3);
    for (unsigned p = 0; p < 3; p++) {
        if (mrp_port_configure(a, p, 20, 60, 10000, 1, true) != 0) { abort(); }
        mrp_set_periodic(a, p, false);
    }
    mrp_set_observer(a, observe, NULL);
    n_ind = n_map = obs_lv_mt_count = obs_lv_mt_val = 0;
    return a;
}
static void rx(struct mrp_app *a, unsigned port, unsigned type, unsigned sid, unsigned value, unsigned event, unsigned la)
{
    uint8_t b[96];
    size_t len = wire(b, type, sid, value, event, la);
    CHECK(mrp_rx(a, (uint8_t)port, b, len) == 0);
}
static void tick(unsigned n)
{
    while (n--) { shlan_timer_tick(); }
}
static void finish(struct mrp_app *a)
{
    allocation_fail_after(0);
    mrp_app_destroy(a);
    CHECK(allocation_live() == 0);
}
static void flush0(struct mrp_app *a, unsigned fault)
{
    allocation_fail_after(fault);
    mrp_port_role_change(a, 0, true);
    CHECK(allocation_failures() == (fault ? 1u : 0u));
    allocation_fail_after(0);
}
/* Count Leave indications on port 0 for one type and return the last value. */
static unsigned leaves0(unsigned type, unsigned *last)
{
    unsigned c = 0;
    for (unsigned i = 0; i < n_ind; i++) {
        if (ind_port[i] == 0 && ind_kind[i] == 10u + type) { ++c; *last = ind_val[i]; }
    }
    return c;
}
static unsigned map_leaves0(unsigned type, unsigned *last)
{
    unsigned c = 0;
    for (unsigned i = 0; i < n_map; i++) {
        if (map_port[i] == 0 && map_type[i] == type) { ++c; *last = map_val[i]; }
    }
    return c;
}
static int index0(unsigned kind)
{
    for (unsigned i = 0; i < n_ind; i++) {
        if (ind_port[i] == 0 && ind_kind[i] == kind) { return (int)i; }
    }
    return -1;
}

static int accept_tx(void *ctx, uint8_t p, const uint8_t *b, size_t n)
{
    unsigned *mfs = ctx;
    (void)p;
    /* Walk MSRP messages: type, length, two-octet list length, vectors. */
    size_t off = 1;
    while (off + 4 <= n && !(b[off] == 0 && b[off + 1] == 0)) {
        unsigned type = b[off], list = (unsigned)(b[off + 2] << 8 | b[off + 3]);
        unsigned values = (unsigned)((b[off + 4] & 0x1f) << 8 | b[off + 5]);
        if (type == 1 && values >= 1 && off + 6 + 18 <= n) {
            *mfs = (unsigned)(b[off + 6 + 16] << 8 | b[off + 6 + 17]);
        }
        off += 4 + list;
    }
    return 0;
}
static int last0(unsigned kind)
{
    int r = -1;
    for (unsigned i = 0; i < n_ind; i++) {
        if (ind_port[i] == 0 && ind_kind[i] == kind) { r = (int)i; }
    }
    return r;
}
/* S1: LeaveAll, Re-declare and transmitted LeaveAll on the source port keep
 * the pending snapshot after a cross-port refresh; exactly one Leave. */
static void s1(void)
{
    for (unsigned t = 1; t <= 2; t++) for (unsigned f = 0; f <= 3; f++) for (unsigned how = 0; how < 3; how++) {
        snprintf(tag, sizeof tag, "S1 type=%u fault=%u path=%s", t, f, how == 0 ? "rLA-other" : how == 1 ? "redeclare" : "txLA");
        ++scenario;
        struct mrp_app *a = setup();
        rx(a, 0, t, 1, 100, 1, 0);              /* register X=100 on port 0 */
        flush0(a, f);
        rx(a, 1, t, 1, 200, 1, 0);              /* propagate X=200 into port 0 */
        if (how == 0) { rx(a, 0, t, 2, 150, 1, 1); }
        else if (how == 1) { mrp_port_role_change(a, 0, false); }
        else {
            /* Flush! makes the LeaveAll machine active (10.7.5.22): transmit it. */
            uint8_t pdu[512];
            unsigned mfs = 0;
            CHECK(mrp_transmit(a, 0, pdu, sizeof pdu, accept_tx, &mfs) == 1);
            CHECK(pdu[5] == 32);
        }
        tick(1);
        unsigned v = 0, mv = 0, c = leaves0(t, &v), mc = map_leaves0(t, &mv);
        /* Y may legitimately leave after LeaveAll timers; count X only by value. */
        unsigned cx = 0;
        for (unsigned i = 0; i < n_ind; i++) {
            if (ind_port[i] == 0 && ind_kind[i] == 10u + t && (ind_val[i] == 100 || ind_val[i] == 200)) { ++cx; v = ind_val[i]; }
        }
        (void)c; (void)mc;
        CHECK(cx == 1);
        CHECK(v == 100);
        CHECK(mc == 1);
        CHECK(mv == 100);
        printf("%s x_leaves=%u x_value=%u\n", tag, cx, v);
        finish(a);
    }
}
/* S2: a later successful Flush, reclaim, a propagated Leave from another
 * port, and source-port transmission all keep the snapshot. */
static void s2(void)
{
    for (unsigned t = 1; t <= 3; t++) for (unsigned f = 0; f <= 3; f++) for (unsigned how = 0; how < 4; how++) {
        static const char *names[] = {"second-flush-ok", "reclaim", "remote-leave", "transmit"};
        snprintf(tag, sizeof tag, "S2 type=%u fault=%u path=%s", t, f, names[how]);
        ++scenario;
        struct mrp_app *a = setup();
        unsigned old = t == 3 ? 2 : 100, other = t == 3 ? 1 : 200;
        if (t == 3) { rx(a, 0, 1, 1, 100, 1, 0); }   /* Talker routes Listener to port 0 */
        rx(a, 0, t, 1, old, 1, 0);
        flush0(a, f);
        if (t == 3) { rx(a, 0, 1, 1, 100, 1, 0); }
        rx(a, 1, t, 1, other, 1, 0);
        unsigned tx_mfs = 0;
        if (how == 0) { mrp_port_role_change(a, 0, true); }
        else if (how == 1) { (void)mrp_reclaim(a, 0); }
        else if (how == 2) {
            /* Port 1 registration withdrawn by a successful Flush there. */
            mrp_port_role_change(a, 1, true);
        } else {
            uint8_t pdu[512];
            CHECK(mrp_transmit(a, 0, pdu, sizeof pdu, accept_tx, &tx_mfs) >= 0);
            if (f == 0) { tick(20); CHECK(mrp_transmit(a, 0, pdu, sizeof pdu, accept_tx, &tx_mfs) >= 0); }
            if (t == 1) { CHECK(tx_mfs == 200); }
        }
        tick(1);
        unsigned v = 0, mv = 0;
        unsigned c = leaves0(t, &v), mc = map_leaves0(t, &mv);
        CHECK(c == 1);
        CHECK(v == old);
        CHECK(mc == 1);
        CHECK(mv == old);
        tick(61);
        CHECK(leaves0(t, &v) == 1);
        printf("%s leaves=%u value=%u policy=%u/%u tx_mfs=%u\n", tag, c, v, mc, mv, tx_mfs);
        finish(a);
    }
}
/* S3: opposite Talker received while the old Talker owes a Flush Leave.
 * Order Leave(old) / Join(new) is compared with the no-fault control. */
static void s3(void)
{
    for (unsigned old_t = 1; old_t <= 2; old_t++) for (unsigned ev = 0; ev <= 3; ev += 1) {
        if (ev == 2) { continue; }              /* rIn does not register */
        int control = -2;
        for (unsigned f = 0; f <= 3; f++) {
            unsigned new_t = 3 - old_t;
            snprintf(tag, sizeof tag, "S3 old=%u new=%u event=%s fault=%u", old_t, new_t,
                     ev == 0 ? "New" : ev == 1 ? "JoinIn" : "JoinMt", f);
            ++scenario;
            struct mrp_app *a = setup();
            rx(a, 0, old_t, 1, 100, 1, 0);
            flush0(a, f);
            rx(a, 1, old_t, 1, 200, 1, 0);      /* cross-port refresh of old type */
            rx(a, 0, new_t, 1, 300, ev, 0);
            int li = index0(10u + old_t), ji = index0(new_t);
            int leave_first_before_tick = li >= 0 && ji >= 0 && li < ji;
            tick(1);
            li = index0(10u + old_t); ji = index0(new_t);
            unsigned v = 0, c = leaves0(old_t, &v);
            int order = li >= 0 && ji >= 0 ? (li < ji ? 1 : 0) : -1;
            if (f == 0) { control = order; }
            CHECK(c == 1);
            CHECK(v == 100);
            printf("%s leave_before_join=%d (before tick %d) control=%d leaves=%u value=%u\n",
                   tag, order, leave_first_before_tick, control, c, v);
            if (ev != 0) { CHECK(order == 1); }
            else if (order != control) {
                printf("NOTE %s order differs from no-fault control\n", tag);
            }
            finish(a);
        }
    }
}
/* S4: observer value reported for the pending LV-to-MT completion. */
static void s4(void)
{
    for (unsigned f = 0; f <= 3; f++) {
        snprintf(tag, sizeof tag, "S4 fault=%u", f);
        ++scenario;
        struct mrp_app *a = setup();
        rx(a, 0, 1, 1, 100, 1, 0);
        rx(a, 0, 1, 1, 100, 4, 1);              /* LV via received LeaveAll */
        flush0(a, f);
        rx(a, 1, 1, 1, 200, 1, 0);
        tick(1);
        unsigned v = 0, c = leaves0(1, &v);
        CHECK(c == 1);
        CHECK(v == 100);
        printf("%s leave=%u observer_lv_mt=%u count=%u\n", tag, v, obs_lv_mt_val, obs_lv_mt_count);
        finish(a);
    }
}
/* S5: refresh BEFORE the Flush (inherited shared Applicant/Registrar value).
 * Retained and immediate Flush must indicate the same value. */
static void s5(void)
{
    unsigned control = 0;
    for (unsigned f = 0; f <= 3; f++) {
        snprintf(tag, sizeof tag, "S5 fault=%u", f);
        ++scenario;
        struct mrp_app *a = setup();
        rx(a, 0, 1, 1, 100, 1, 0);
        rx(a, 1, 1, 1, 200, 1, 0);              /* refresh before Flush */
        flush0(a, f);
        tick(1);
        unsigned v = 0, c = leaves0(1, &v);
        if (f == 0) { control = v; }
        CHECK(c == 1);
        CHECK(v == control);
        printf("%s leave=%u control=%u\n", tag, v, control);
        finish(a);
    }
}
/* S6: Milan-relevant rLv and every received event on the source port after
 * a cross-port refresh, at every Flush fault and every receive retry fault. */
static void s6(void)
{
    for (unsigned t = 1; t <= 3; t++) for (unsigned ev = 0; ev <= 5; ev++) for (unsigned f = 1; f <= 3; f++) for (unsigned rf = 0; rf <= 3; rf++) {
        snprintf(tag, sizeof tag, "S6 type=%u event=%u fault=%u retry_fault=%u", t, ev, f, rf);
        ++scenario;
        struct mrp_app *a = setup();
        unsigned old = t == 3 ? 2 : 100, other = t == 3 ? 1 : 200, next = t == 3 ? 3 : 300;
        if (t == 3) { rx(a, 0, 1, 1, 100, 1, 0); }
        rx(a, 0, t, 1, old, 1, 0);
        flush0(a, f);
        if (t == 3) { rx(a, 0, 1, 1, 100, 1, 0); }
        rx(a, 1, t, 1, other, 1, 0);
        uint8_t b[96];
        size_t len = wire(b, t, 1, next, ev, 0);
        allocation_fail_after(rf);
        int r = mrp_rx(a, 0, b, len);
        unsigned injected = allocation_failures();
        allocation_fail_after(0);
        if (r < 0) {
            CHECK(r == -SHLAN_ERROR_NO_MEMORY);
            CHECK(mrp_rx(a, 0, b, len) == 0);
        }
        tick(1);
        unsigned v = 0, c = leaves0(t, &v);
        CHECK(c == 1);
        CHECK(v == old);
        int li = index0(10u + t), ji = last0(t);
        unsigned declaring = ev == 0 || ev == 1 || ev == 3;
        if (declaring) { CHECK(ji > li); }
        (void)injected;
        tick(61);
        CHECK(leaves0(t, &v) == 1 + 0u);
        finish(a);
    }
    printf("S6 completed through scenario %u\n", scenario);
}
int main(void)
{
    s1(); s2(); s3(); s4(); s5(); s6();
    printf("%s internal pending-storage probe: %u scenarios, %u checks, %u failures\n",
           failures ? "FAIL" : "PASS", scenario, checks, failures);
    return failures ? 1 : 0;
}
