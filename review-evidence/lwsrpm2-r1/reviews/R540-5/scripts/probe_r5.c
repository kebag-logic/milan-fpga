/* SPDX-License-Identifier: Apache-2.0 */
/* Reviewer probe for pending Flush withdrawal, retry timing, observer continuity
 * and allocation-position bounds. Build: see scripts/run_probe.sh. */
#include <stdio.h>
#include <string.h>
#include "shish_lan/msrp.h"
#include "shish_lan/error.h"
#include "ports/timer.h"
#include "fault_alloc.h"

static unsigned checks, fails;
#define CHECK(c, ...) do { ++checks; if (!(c)) { ++fails; printf("FAIL %s:%d ", __func__, __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)

struct ind { char kind; uint8_t port, type; unsigned value; };
static struct ind log_[64];
static unsigned nlog;
static unsigned value_of(uint8_t t, const void *v)
{
    if (t == MSRP_ATTR_TYPE_LISTENER) {
        return ((const uint8_t *)v)[8];
    }
    return ((const struct msrp_talker_adv *)v)->max_frame_size;
}
static void rec(char k, uint8_t p, uint8_t t, const void *v)
{
    if (nlog < 64) {
        log_[nlog].kind = k; log_[nlog].port = p; log_[nlog].type = t;
        log_[nlog].value = value_of(t, v); ++nlog;
    }
}
static void on_join(struct mrp_app *a, uint8_t p, uint8_t t, const void *v, bool n)
{
    (void)a; rec(n ? 'N' : 'J', p, t, v);
}
static void on_leave(struct mrp_app *a, uint8_t p, uint8_t t, const void *v)
{
    (void)a; rec('L', p, t, v);
}
static uint32_t targets(const struct mrp_app *a, uint8_t p, uint8_t t, const void *v)
{
    (void)a; (void)t; (void)v; return p == 0 ? 6u : 0;
}
/* Port-0 indications as a compact string such as "L1:100 J1:101". */
static const char *p0(void)
{
    static char s[512];
    s[0] = 0;
    for (unsigned i = 0; i < nlog; ++i) {
        if (log_[i].port == 0) {
            char e[32];
            snprintf(e, sizeof(e), "%s%c%u:%u", s[0] ? " " : "", log_[i].kind, log_[i].type, log_[i].value);
            strncat(s, e, sizeof(s) - strlen(s) - 1);
        }
    }
    return s;
}
static struct mrp_app *bridge(void)
{
    struct msrp_ctx c = {0};
    struct mrp_app *base = msrp_app_create(1, &c);
    struct mrp_app_ops ops = *base->ops;
    ops.join_ind = on_join; ops.leave_ind = on_leave; ops.ctx = NULL;
    ops.map_join = targets; ops.map_leave = targets;
    mrp_app_destroy(base);
    struct mrp_app *a = mrp_app_create(&ops, 3);
    for (uint8_t p = 0; p < 3; ++p) {
        mrp_port_configure(a, p, 20, 60, 10000, 1, true);
        mrp_set_periodic(a, p, false);
    }
    nlog = 0;
    return a;
}
static void tick(unsigned n)
{
    while (n--) {
        shlan_timer_tick();
    }
}
/* type 1 Talker Advertise, 2 Talker Failed, 3 Listener; event 0 New 1 JoinIn 3 JoinMt 4 Mt 5 Lv. */
static size_t pdu_of(uint8_t *pdu, unsigned type, unsigned sid, unsigned value, unsigned event, bool la)
{
    size_t len;
    memset(pdu, 0, 64);
    if (type == 3) {
        len = 21; pdu[1] = 3; pdu[2] = 8; pdu[4] = 14;
        pdu[15] = (uint8_t)(36 * event); pdu[16] = (uint8_t)(value << 6);
    } else {
        len = 37; pdu[1] = 1; pdu[2] = 25; pdu[4] = 30;
        pdu[23] = (uint8_t)(value >> 8); pdu[24] = (uint8_t)value;
        pdu[32] = (uint8_t)(36 * event);
        if (type == 2) {
            memset(pdu + 32, 0, 14);
            pdu[1] = 2; pdu[2] = 34; pdu[4] = 39; pdu[40] = 1;
            pdu[41] = (uint8_t)(36 * event); len = 46;
        }
    }
    pdu[5] = la ? 0x20 : 0; pdu[6] = 1; pdu[14] = (uint8_t)sid;
    return len;
}
static int rx(struct mrp_app *a, unsigned type, unsigned sid, unsigned value, unsigned event, bool la)
{
    uint8_t pdu[64];
    size_t len = pdu_of(pdu, type, sid, value, event, la);
    return mrp_rx(a, 0, pdu, len);
}
struct stq { unsigned type, sid; int found; enum mrp_reg_state reg; unsigned value; };
static void stv(void *ctx, const struct mrp_attr_status *s)
{
    struct stq *q = ctx;
    if (s->attr_type == q->type && ((const uint8_t *)s->attr_val)[7] == q->sid) {
        q->found = 1; q->reg = s->reg; q->value = value_of(s->attr_type, s->attr_val);
    }
}
static struct stq state(struct mrp_app *a, uint8_t port, unsigned type, unsigned sid)
{
    struct stq q = {.type = type, .sid = sid};
    mrp_attr_visit(a, port, stv, &q);
    return q;
}
static unsigned old_value(unsigned type) { return type == 3 ? 2 : 100; }
/* Register, optionally move to LV by LeaveAll, then fail Flush at `fault`. */
static struct mrp_app *pending(unsigned type, unsigned fault, bool lv)
{
    struct mrp_app *a = bridge();
    rx(a, type, 1, old_value(type), 1, false);
    if (lv) {
        rx(a, type, 1, old_value(type), 4, true);
    }
    nlog = 0;
    allocation_fail_after(fault);
    mrp_port_role_change(a, 0, true);
    allocation_fail_after(0);
    return a;
}
static void done(struct mrp_app *a)
{
    mrp_app_destroy(a);
    CHECK(allocation_live() == 0, "leak %zu", allocation_live());
}

/* Allocation counts: the sweeps must cover every position. */
static void bounds(void)
{
    for (unsigned type = 1; type <= 3; ++type) {
        for (unsigned lv = 0; lv < 2; ++lv) {
            struct mrp_app *a = bridge();
            rx(a, type, 1, old_value(type), 1, false);
            if (lv) {
                rx(a, type, 1, old_value(type), 4, true);
            }
            allocation_fail_after(4);
            mrp_port_role_change(a, 0, true);
            CHECK(allocation_failures() == 0, "flush uses more than 3 allocations type %u", type);
            allocation_fail_after(0);
            done(a);
            a = pending(type, 1, lv);
            allocation_fail_after(7);
            CHECK(rx(a, type, 1, old_value(type) + 1, 1, false) == 0, "rx");
            CHECK(allocation_failures() == 0, "pending receive uses more than 6 allocations type %u", type);
            CHECK(!strcmp(p0(), type == 3 ? "L3:2 J3:3" : (type == 1 ? "L1:100 J1:101" : "L2:100 J2:101")), "order %s", p0());
            allocation_fail_after(0);
            done(a);
        }
    }
    for (unsigned lv = 0; lv < 2; ++lv) {
        for (unsigned old = 1; old <= 2; ++old) {
            struct mrp_app *a = bridge();
            rx(a, old, 1, 100, 1, false);
            if (lv) {
                rx(a, old, 1, 100, 4, true);
                CHECK(state(a, 0, old, 1).reg == MRP_REG_STATE_LV, "not LV");
            }
            allocation_fail_after(10);
            CHECK(rx(a, 3 - old, 1, 100, 1, false) == 0, "rx");
            CHECK(allocation_failures() == 0, "replacement uses more than 9 allocations");
            allocation_fail_after(0);
            done(a);
        }
    }
}
/* Retry timing: a failed Flush withdraws on the first tick, and each further failed tick retries. */
static void timing(void)
{
    for (unsigned repeats = 0; repeats <= 3; ++repeats) {
        struct mrp_app *a = pending(1, 2, false);
        for (unsigned r = 0; r < repeats; ++r) {
            allocation_fail_after(1);
            tick(1);
            CHECK(allocation_failures() == 1, "tick %u did not retry", r + 1);
        }
        allocation_fail_after(0);
        tick(1);
        CHECK(!strcmp(p0(), "L1:100"), "repeats %u got '%s'", repeats, p0());
        tick(200);
        CHECK(!strcmp(p0(), "L1:100"), "duplicate Leave '%s'", p0());
        done(a);
    }
}
static void interleavings(void)
{
    /* LeaveAll and JoinIn in one message after a pending Flush. */
    for (unsigned type = 1; type <= 3; ++type) {
        struct mrp_app *a = pending(type, 1, false);
        CHECK(rx(a, type, 1, old_value(type) + 1, 1, true) == 0, "rx");
        char want[64];
        snprintf(want, sizeof(want), "L%u:%u J%u:%u", type, old_value(type), type, old_value(type) + 1);
        CHECK(!strcmp(p0(), want), "LeaveAll+JoinIn type %u got '%s'", type, p0());
        tick(100);
        CHECK(!strcmp(p0(), want), "after ticks '%s'", p0());
        done(a);
    }
    /* Received New after a pending Flush indicates Leave then New. */
    {
        struct mrp_app *a = pending(1, 3, true);
        CHECK(rx(a, 1, 1, 100, 0, false) == 0, "rx");
        CHECK(!strcmp(p0(), "L1:100 N1:100"), "New got '%s'", p0());
        done(a);
    }
    /* Received Mt/Lv/In after a pending Flush: one Leave, no Join, no duplicate. */
    for (unsigned ev = 2; ev <= 5; ++ev) {
        if (ev == 3) {
            continue; /* JoinMt declares; covered with JoinIn and New. */
        }
        struct mrp_app *a = pending(1, 1, false);
        CHECK(rx(a, 1, 1, 100, ev, false) == 0, "rx");
        tick(200);
        CHECK(!strcmp(p0(), "L1:100"), "event %u got '%s'", ev, p0());
        CHECK(state(a, 0, 1, 1).reg == MRP_REG_STATE_MT, "not MT");
        done(a);
    }
    /* A second successful Flush completes the withdrawal once. */
    {
        struct mrp_app *a = pending(1, 1, false);
        mrp_port_role_change(a, 0, true);
        tick(200);
        CHECK(rx(a, 1, 1, 100, 1, false) == 0, "rx");
        CHECK(!strcmp(p0(), "L1:100 J1:100"), "second Flush got '%s'", p0());
        done(a);
    }
    /* Re-declare during pending Flush must not cancel it. */
    {
        struct mrp_app *a = pending(1, 1, false);
        mrp_port_role_change(a, 0, false);
        tick(1);
        CHECK(!strcmp(p0(), "L1:100"), "redeclare got '%s'", p0());
        done(a);
    }
    /* Reclaim must not drop a pending withdrawal. */
    {
        struct mrp_app *a = pending(3, 1, false);
        mrp_reclaim(a, 0);
        tick(1);
        CHECK(!strcmp(p0(), "L3:2"), "reclaim got '%s'", p0());
        done(a);
    }
    /* Destroy with a pending withdrawal releases everything. */
    {
        struct mrp_app *a = pending(2, 2, true);
        done(a);
    }
    /* Opposite Talker Join while the old Talker has a pending Flush. */
    for (unsigned old = 1; old <= 2; ++old) {
        for (unsigned fault = 0; fault <= 9; ++fault) {
            struct mrp_app *a = pending(old, 1, false);
            allocation_fail_after(fault);
            int r = rx(a, 3 - old, 1, 100, 1, false);
            allocation_fail_after(0);
            if (r < 0) {
                CHECK(rx(a, 3 - old, 1, 100, 1, false) == 0, "retry");
            }
            tick(200);
            char want[64];
            snprintf(want, sizeof(want), "L%u:100 J%u:100", old, 3 - old);
            CHECK(!strcmp(p0(), want), "opposite old %u fault %u got '%s'", old, fault, p0());
            done(a);
        }
    }
    /* Join reservation failure after the receive-completed Leave: no stale-timer duplicate. */
    for (unsigned fault = 4; fault <= 6; ++fault) {
        struct mrp_app *a = pending(1, 1, false);
        allocation_fail_after(fault);
        CHECK(rx(a, 1, 1, 101, 1, false) == -SHLAN_ERROR_NO_MEMORY, "rx");
        allocation_fail_after(0);
        tick(200);
        CHECK(!strcmp(p0(), "L1:100"), "fault %u after ticks '%s'", fault, p0());
        CHECK(rx(a, 1, 1, 101, 1, false) == 0, "retry");
        CHECK(!strcmp(p0(), "L1:100 J1:101"), "fault %u got '%s'", fault, p0());
        done(a);
    }
    /* Two pending attributes in one payload: the first failure stops the second. */
    {
        struct mrp_app *a = bridge();
        rx(a, 1, 1, 100, 1, false); rx(a, 1, 2, 100, 1, false);
        nlog = 0;
        allocation_fail_after(1);
        mrp_port_role_change(a, 0, true);   /* first attribute in list fails */
        allocation_fail_after(0);
        unsigned pending_count = nlog;
        uint8_t pdu[96], second[64];
        size_t len = pdu_of(pdu, 1, 1, 101, 1, false);
        size_t next = pdu_of(second, 1, 2, 101, 1, false);
        memcpy(pdu + len - 2, second + 1, next - 1);
        len += next - 3;
        allocation_fail_after(1);
        int r = mrp_rx(a, 0, pdu, len);
        allocation_fail_after(0);
        CHECK(r == -SHLAN_ERROR_NO_MEMORY, "r %d", r);
        CHECK(nlog == pending_count, "indications after stopped receive '%s'", p0());
        CHECK(mrp_rx(a, 0, pdu, len) == 0, "retry");
        tick(200);
        unsigned l = 0, j = 0;
        for (unsigned i = 0; i < nlog; ++i) {
            if (log_[i].port == 0) { l += log_[i].kind == 'L'; j += log_[i].kind == 'J'; }
        }
        CHECK(l == 2 && j == 2, "two attributes got '%s'", p0());
        done(a);
    }
}
/* A timer-completed pending withdrawal must leave ordinary registration behind. */
static void timer_completion(void)
{
    for (unsigned type = 1; type <= 3; ++type) {
        for (unsigned lv = 0; lv < 2; ++lv) {
            struct mrp_app *a = pending(type, 1, lv);
            tick(1);
            for (unsigned refresh = 0; refresh < 3; ++refresh) {
                CHECK(rx(a, type, 1, old_value(type), 1, false) == 0, "rx");
            }
            tick(30);
            char want[64];
            snprintf(want, sizeof(want), "L%u:%u J%u:%u", type, old_value(type), type, old_value(type));
            CHECK(!strcmp(p0(), want), "timer completion type %u lv %u got '%s'", type, lv, p0());
            done(a);
        }
    }
}
static enum mrp_reg_state oreg; static enum mrp_appl_state oappl; static unsigned ogaps, oflush_lv;
static void observer(void *ctx, const struct mrp_transition *t)
{
    (void)ctx;
    if (t->port_id != 0 || t->attr_type != 1) {
        return;
    }
    if (t->reg_from != oreg || t->appl_from != oappl) {
        ++ogaps;
    }
    if (t->event == MRP_EVENT_FLUSH && t->reg_from == MRP_REG_STATE_IN && t->reg_to == MRP_REG_STATE_LV) {
        ++oflush_lv;
    }
    oreg = t->reg_to; oappl = t->appl_to;
}
static void observers(void)
{
    for (unsigned path = 0; path < 3; ++path) {
        for (unsigned fault = 1; fault <= 3; ++fault) {
            struct mrp_app *a = bridge();
            oreg = MRP_REG_STATE_MT; oappl = MRP_APPL_STATE_VO; ogaps = oflush_lv = 0;
            mrp_set_observer(a, observer, NULL);
            rx(a, 1, 1, 100, 1, false);
            allocation_fail_after(fault);
            mrp_port_role_change(a, 0, true);
            CHECK(oflush_lv == 1 && oreg == MRP_REG_STATE_LV, "IN->LV not observed");
            allocation_fail_after(1);
            if (path == 2) {
                rx(a, 1, 1, 101, 1, false); /* failed receive retry */
            } else {
                tick(1);
            }
            allocation_fail_after(0);
            if (path == 0) {
                tick(1);
            } else {
                rx(a, 1, 1, 101, 1, false);
            }
            struct stq s = state(a, 0, 1, 1);
            CHECK(s.reg == oreg, "observer ends %d state %d", oreg, s.reg);
            CHECK(ogaps == 0, "path %u fault %u gaps %u", path, fault, ogaps);
            done(a);
        }
    }
}
int main(void)
{
    bounds();
    timing();
    interleavings();
    timer_completion();
    observers();
    printf("probe_r5 profile=%s checks=%u failures=%u\n", LWSRP_MILAN ? "ON" : "OFF", checks, fails);
    return fails != 0;
}
