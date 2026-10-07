/* SPDX-License-Identifier: Apache-2.0 */
/* Reviewer probe for lwSRP PR #12 round 5 (R540-4).
 * Real MSRP application, three ports, reviewer-owned allocation port with
 * one-shot and persistent exhaustion, observer continuity and host-view checks.
 * Build: cc -std=c11 -DLWSRP_MILAN=<0|1> -I<src>/include -I<src> probe_r3.c
 *        <src>/src/ports/timer.c <src>/src/core/mrp_mad.c <src>/src/core/mrp_pdu.c
 *        <src>/src/modules/msrp.c
 */
#include <stdarg.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ports/alloc.h"
#include "ports/timer.h"
#include "shish_lan/error.h"
#include "shish_lan/mrp.h"
#include "shish_lan/msrp.h"

/* ---------------- allocation port ---------------- */
static unsigned a_count, a_fail_at, a_persist; static long a_live;
static void fault_once(unsigned n) { a_count = 0; a_fail_at = n; a_persist = 0; }
static void fault_from(unsigned n) { a_count = 0; a_fail_at = n; a_persist = 1; }
static void fault_none(void) { a_fail_at = 0; a_persist = 0; a_count = 0; }
static bool fail_now(void)
{
    if (!a_fail_at) { return false; }
    ++a_count;
    if (a_persist) { return a_count >= a_fail_at; }
    return a_count == a_fail_at;
}
void *shlan_malloc(size_t n) { if (fail_now()) { return NULL; } void *p = malloc(n); if (p) { ++a_live; } return p; }
void *shlan_calloc(size_t c, size_t n) { if (fail_now()) { return NULL; } void *p = calloc(c, n); if (p) { ++a_live; } return p; }
void shlan_free(void *p) { if (p) { --a_live; } free(p); }
int shlan_printf(const char *fmt, ...) { va_list ap; va_start(ap, fmt); int r = vprintf(fmt, ap); va_end(ap); return r; }

/* ---------------- result accounting ---------------- */
static unsigned checks, failures;
static char ctxname[160];
#define CHECK(cond, ...) do { ++checks; if (!(cond)) { ++failures; \
    printf("FAIL [%s] line %d: ", ctxname, __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)

/* ---------------- indication log ---------------- */
struct ind { uint8_t port, kind, type, sid; }; /* kind: 'J' join, 'N' new, 'L' leave */
static struct ind log_[256]; static unsigned nlog;
static void rec(uint8_t port, uint8_t kind, uint8_t type, const void *v)
{
    if (nlog < 256) { log_[nlog++] = (struct ind){port, kind, type, ((const uint8_t *)v)[7]}; }
}
static void on_ta(struct msrp_ctx *c, uint8_t p, const struct msrp_talker_adv *a, bool n) { (void)c; rec(p, n ? 'N' : 'J', 1, a); }
static void on_tf(struct msrp_ctx *c, uint8_t p, const struct msrp_talker_failed *a, bool n) { (void)c; rec(p, n ? 'N' : 'J', 2, a); }
static void on_li(struct msrp_ctx *c, uint8_t p, const struct msrp_stream_id *s, enum msrp_listener_decl d, bool n) { (void)c; (void)d; rec(p, n ? 'N' : 'J', 3, s); }
static void on_lv(struct msrp_ctx *c, uint8_t p, uint8_t t, const void *v) { (void)c; rec(p, 'L', t, v); }
static void on_dom(struct msrp_ctx *c, uint8_t p, const struct msrp_domain *d, bool n) { (void)c; (void)p; (void)d; (void)n; }
static struct msrp_ctx sctx = { on_ta, on_tf, on_li, on_lv, on_dom };

/* Count indications of kind for (port,type,sid); return index of first. */
static unsigned mark;
static unsigned count_ind(uint8_t port, uint8_t kind, uint8_t type, uint8_t sid, int *first)
{
    unsigned n = 0; if (first) { *first = -1; }
    for (unsigned i = mark; i < nlog; ++i) {
        bool k = kind == 'J' ? (log_[i].kind == 'J' || log_[i].kind == 'N') : log_[i].kind == kind;
        if (log_[i].port == port && k && log_[i].type == type && log_[i].sid == sid) {
            if (first && *first < 0) { *first = (int)i; }
            ++n;
        }
    }
    return n;
}

/* ---------------- observer continuity ---------------- */
struct seen { uint8_t port, type, sid; enum mrp_reg_state reg; bool valid; };
static struct seen seen_[64]; static unsigned nseen, obs_breaks;
static void observer(void *ctx, const struct mrp_transition *t)
{
    (void)ctx;
    uint8_t sid = ((const uint8_t *)t->attr_val)[7];
    for (unsigned i = 0; i < nseen; ++i) {
        if (seen_[i].port == t->port_id && seen_[i].type == t->attr_type && seen_[i].sid == sid) {
            if (seen_[i].reg != t->reg_from) {
                ++obs_breaks;
                printf("  observer gap [%s] port %u type %u sid %u: last reported %s, next from %s (%s)\n",
                       ctxname, t->port_id, t->attr_type, sid, mrp_reg_state_name(seen_[i].reg),
                       mrp_reg_state_name(t->reg_from), mrp_event_name(t->event));
            }
            seen_[i].reg = t->reg_to;
            return;
        }
    }
    if (nseen < 64) { seen_[nseen++] = (struct seen){t->port_id, t->attr_type, sid, t->reg_to, true}; }
}

/* ---------------- state queries ---------------- */
struct q { uint8_t type, sid; bool found; enum mrp_reg_state reg; enum mrp_appl_state appl; };
static void visit(void *ctx, const struct mrp_attr_status *s)
{
    struct q *q = ctx;
    if (s->attr_type == q->type && ((const uint8_t *)s->attr_val)[7] == q->sid) {
        q->found = true; q->reg = s->reg; q->appl = s->appl;
    }
}
static struct q query(struct mrp_app *a, uint8_t port, uint8_t type, uint8_t sid)
{
    struct q q = { .type = type, .sid = sid };
    mrp_attr_visit(a, port, visit, &q);
    return q;
}
/* Host view: joins minus leaves on the source port equals registration (IN or LV). */
static void host_view(struct mrp_app *a, uint8_t port, uint8_t type, uint8_t sid)
{
    int last = 0; /* 0 unregistered, 1 registered */
    for (unsigned i = 0; i < nlog; ++i) {
        if (log_[i].port == port && log_[i].type == type && log_[i].sid == sid) {
            last = log_[i].kind == 'L' ? 0 : 1;
        }
    }
    struct q q = query(a, port, type, sid);
    int reg = q.found && q.reg != MRP_REG_STATE_MT;
    CHECK(last == reg, "host view %d but registrar %s for port %u type %u sid %u", last,
          q.found ? mrp_reg_state_name(q.reg) : "absent", port, type, sid);
}

/* ---------------- PDU builder ---------------- */
static size_t msg(uint8_t *b, uint8_t type, uint8_t sid, uint8_t event, bool la, uint8_t tspec)
{
    uint8_t len = type == 1 ? 25 : type == 2 ? 34 : type == 3 ? 8 : 4;
    size_t list = 2u + len + 1u + (type == 3 ? 1u : 0u) + 2u;
    size_t o = 0;
    b[o++] = type; b[o++] = len; b[o++] = (uint8_t)(list >> 8); b[o++] = (uint8_t)list;
    b[o++] = la ? 0x20 : 0; b[o++] = 1;
    memset(b + o, 0, len);
    b[o + 7] = sid;
    if (type == 1 || type == 2) {
        b[o + 16] = 0; b[o + 17] = tspec; /* MaxFrameSize, big-endian */
    }
    if (type == 2) {
        b[o + 33] = 1; /* failure code */
    }
    o += len;
    b[o++] = (uint8_t)(event * 36u);
    if (type == 3) {
        b[o++] = (uint8_t)(2u << 6); /* Ready */
    }
    b[o++] = 0; b[o++] = 0;
    return o;
}
static size_t pdu1(uint8_t *b, uint8_t type, uint8_t sid, uint8_t event, bool la)
{
    size_t o = 0; b[o++] = 0;
    o += msg(b + o, type, sid, event, la, 100);
    b[o++] = 0; b[o++] = 0;
    return o;
}
/* LeaveAll-only message for one type (NumberOfValues zero). */
static size_t pdu_la(uint8_t *b, uint8_t type)
{
    uint8_t len = type == 1 ? 25 : type == 2 ? 34 : type == 3 ? 8 : 4;
    size_t list = 2u + len + 2u, o = 0;
    b[o++] = 0; b[o++] = type; b[o++] = len; b[o++] = (uint8_t)(list >> 8); b[o++] = (uint8_t)list;
    b[o++] = 0x20; b[o++] = 0; memset(b + o, 0, len); o += len;
    b[o++] = 0; b[o++] = 0; b[o++] = 0; b[o++] = 0;
    return o;
}
enum { EV_NEW = 0, EV_JOININ = 1, EV_IN = 2, EV_JOINMT = 3, EV_MT = 4, EV_LV = 5 };

static int accept_send(void *c, uint8_t p, const uint8_t *pdu, size_t n) { (void)c; (void)p; (void)pdu; (void)n; return 0; }
static void ticks(unsigned n) { while (n--) { shlan_timer_tick(); } }
static uint8_t txbuf[1500];
static void poll_all(struct mrp_app *a) { for (uint8_t p = 0; p < 3; ++p) { (void)mrp_transmit(a, p, txbuf, sizeof(txbuf), accept_send, NULL); } }

static struct mrp_app *dut(void)
{
    nlog = 0; mark = 0; nseen = 0; obs_breaks = 0;
    struct mrp_app *a = msrp_app_create(3, &sctx);
    for (uint8_t p = 0; p < 3; ++p) {
        mrp_port_configure(a, p, 20, 60, 10000, 1u + p, true);
        mrp_set_periodic(a, p, false);
    }
    mrp_set_observer(a, observer, NULL);
    return a;
}
static void teardown(struct mrp_app *a)
{
    fault_none();
    mrp_app_destroy(a);
    CHECK(a_live == 0, "live allocations after destroy: %ld", a_live);
    a_live = 0;
}
static bool leaving(enum mrp_appl_state s) { return s == MRP_APPL_STATE_LA || s == MRP_APPL_STATE_VO || s == MRP_APPL_STATE_LO; }

/* ---------------- P1: Flush retention ---------------- */
static unsigned obs_gap_cases;
static void flush_case(bool lv, unsigned nattr, unsigned fault, bool persistent, unsigned hold)
{
    snprintf(ctxname, sizeof(ctxname), "flush %s attrs=%u fault=%u %s hold=%u", lv ? "LV" : "IN", nattr, fault,
             persistent ? "persistent" : "once", hold);
    struct mrp_app *a = dut();
    uint8_t b[256];
    for (unsigned s = 1; s <= nattr; ++s) {
        size_t n = pdu1(b, 1, (uint8_t)s, EV_JOININ, false);
        CHECK(mrp_rx(a, 0, b, n) == 0, "setup rx");
    }
    poll_all(a); ticks(25); poll_all(a);
    if (lv) {
        size_t n = pdu_la(b, 1);
        CHECK(mrp_rx(a, 0, b, n) == 0, "LeaveAll rx");
    }
    for (unsigned s = 1; s <= nattr; ++s) {
        CHECK(query(a, 0, 1, (uint8_t)s).reg == (lv ? MRP_REG_STATE_LV : MRP_REG_STATE_IN), "setup state");
    }
    if (fault) { if (persistent) { fault_from(fault); } else { fault_once(fault); } }
    mrp_port_role_change(a, 0, true);
    for (unsigned s = 1; s <= nattr; ++s) { host_view(a, 0, 1, (uint8_t)s); }
    for (unsigned t = 0; t < hold; ++t) {
        ticks(1);
        for (unsigned s = 1; s <= nattr; ++s) { host_view(a, 0, 1, (uint8_t)s); }
    }
    fault_none();
    ticks(2); poll_all(a);
    for (unsigned s = 1; s <= nattr; ++s) {
        CHECK(count_ind(0, 'L', 1, (uint8_t)s, NULL) == 1, "sid %u leave indications %u (want 1)", s,
              count_ind(0, 'L', 1, (uint8_t)s, NULL));
        CHECK(query(a, 0, 1, (uint8_t)s).reg == MRP_REG_STATE_MT, "sid %u source not MT", s);
        for (uint8_t p = 1; p < 3; ++p) {
            struct q q = query(a, p, 1, (uint8_t)s);
            CHECK(q.found && leaving(q.appl), "sid %u port %u propagated withdrawal missing (appl %s)", s, p,
                  q.found ? mrp_appl_state_name(q.appl) : "absent");
        }
        host_view(a, 0, 1, (uint8_t)s);
    }
    /* Subsequent registration after recovery is indicated as a Join. */
    for (unsigned s = 1; s <= nattr; ++s) {
        size_t n = pdu1(b, 1, (uint8_t)s, EV_JOININ, false);
        CHECK(mrp_rx(a, 0, b, n) == 0, "re-registration rx");
        CHECK(count_ind(0, 'J', 1, (uint8_t)s, NULL) == 2, "sid %u joins %u after re-registration (want 2)", s,
              count_ind(0, 'J', 1, (uint8_t)s, NULL));
        CHECK(query(a, 0, 1, (uint8_t)s).reg == MRP_REG_STATE_IN, "sid %u not IN after re-registration", s);
        host_view(a, 0, 1, (uint8_t)s);
    }
    if (obs_breaks) { ++obs_gap_cases; }
    teardown(a);
}

/* Informational: a peer that keeps re-declaring every tick after a retained Flush. */
static void flush_with_peer_joins(bool rx_before_tick)
{
    snprintf(ctxname, sizeof(ctxname), "flush fault=1 then peer JoinIn each tick, %s", rx_before_tick ? "rx before tick" : "tick before rx");
    struct mrp_app *a = dut();
    uint8_t b[256]; size_t n = pdu1(b, 1, 1, EV_JOININ, false);
    CHECK(mrp_rx(a, 0, b, n) == 0, "setup");
    fault_once(1);
    mrp_port_role_change(a, 0, true);
    fault_none();
    for (unsigned t = 0; t < 30; ++t) {
        if (rx_before_tick) { (void)mrp_rx(a, 0, b, n); ticks(1); } else { ticks(1); (void)mrp_rx(a, 0, b, n); }
        poll_all(a);
        host_view(a, 0, 1, 1);
    }
    printf("  info [%s]: leaves=%u joins=%u reg=%s\n", ctxname, count_ind(0, 'L', 1, 1, NULL),
           count_ind(0, 'J', 1, 1, NULL), mrp_reg_state_name(query(a, 0, 1, 1).reg));
    teardown(a);
}

/* ---------------- P2: Flush retention then re-declaration before retry ---------------- */
static void flush_then_join(void)
{
    snprintf(ctxname, sizeof(ctxname), "flush-retained then rJoinIn");
    struct mrp_app *a = dut();
    uint8_t b[256]; size_t n = pdu1(b, 1, 1, EV_JOININ, false);
    CHECK(mrp_rx(a, 0, b, n) == 0, "setup");
    fault_once(1);
    mrp_port_role_change(a, 0, true);
    fault_none();
    CHECK(mrp_rx(a, 0, b, n) == 0, "rejoin");
    ticks(70); poll_all(a);
    host_view(a, 0, 1, 1);
    printf("  info [%s]: reg=%s joins=%u leaves=%u\n", ctxname, mrp_reg_state_name(query(a, 0, 1, 1).reg),
           count_ind(0, 'J', 1, 1, NULL), count_ind(0, 'L', 1, 1, NULL));
    teardown(a);
}

/* ---------------- P3: Replacement ordering ---------------- */
static void replacement_case(uint8_t old_type, bool lv, unsigned fault, bool persistent, int retry_mode)
{
    /* retry_mode 0: immediate identical retry; 1: tick(1) then retry; 2: persistent fault held over a tick, then retry. */
    snprintf(ctxname, sizeof(ctxname), "replace %u->%u %s fault=%u %s retry=%d", old_type, 3u - old_type,
             lv ? "LV" : "IN", fault, persistent ? "persistent" : "once", retry_mode);
    struct mrp_app *a = dut();
    uint8_t b[256]; uint8_t new_type = (uint8_t)(3u - old_type);
    size_t n = pdu1(b, old_type, 1, EV_JOININ, false);
    CHECK(mrp_rx(a, 0, b, n) == 0, "setup");
    poll_all(a); ticks(25); poll_all(a);
    if (lv) {
        size_t m = pdu_la(b, old_type);
        CHECK(mrp_rx(a, 0, b, m) == 0, "LeaveAll");
    }
    mark = nlog;
    n = pdu1(b, new_type, 1, EV_JOININ, false);
    if (fault) { if (persistent) { fault_from(fault); } else { fault_once(fault); } }
    int r = mrp_rx(a, 0, b, n);
    host_view(a, 0, old_type, 1); host_view(a, 0, new_type, 1);
    int lfirst, jfirst;
    if (r < 0) {
        CHECK(count_ind(0, 'J', new_type, 1, NULL) == 0, "new Join indicated by a failed receive");
        if (retry_mode >= 1) {
            ticks(1);
            host_view(a, 0, old_type, 1); host_view(a, 0, new_type, 1);
        }
        fault_none();
        r = mrp_rx(a, 0, b, n);
        CHECK(r == 0, "retry rc %d", r);
    }
    fault_none();
    ticks(1); poll_all(a); ticks(25); poll_all(a);
    unsigned leaves = count_ind(0, 'L', old_type, 1, &lfirst);
    unsigned joins = count_ind(0, 'J', new_type, 1, &jfirst);
    CHECK(leaves == 1, "old leaves %u", leaves);
    CHECK(joins == 1, "new joins %u", joins);
    CHECK(lfirst >= 0 && jfirst >= 0 && lfirst < jfirst, "order leave@%d join@%d", lfirst, jfirst);
    CHECK(query(a, 0, old_type, 1).reg == MRP_REG_STATE_MT, "old not MT");
    CHECK(query(a, 0, new_type, 1).reg == MRP_REG_STATE_IN, "new not IN");
    for (uint8_t p = 1; p < 3; ++p) {
        struct q o = query(a, p, old_type, 1), w = query(a, p, new_type, 1);
        CHECK(o.found && leaving(o.appl), "port %u old not withdrawn (%s)", p, o.found ? mrp_appl_state_name(o.appl) : "absent");
        CHECK(w.found && !leaving(w.appl), "port %u new not declared (%s)", p, w.found ? mrp_appl_state_name(w.appl) : "absent");
    }
    host_view(a, 0, old_type, 1); host_view(a, 0, new_type, 1);
    teardown(a);
}

/* ---------------- P4: receive stop ---------------- */
static void receive_stop_case(unsigned fault)
{
    snprintf(ctxname, sizeof(ctxname), "receive-stop fault=%u", fault);
    struct mrp_app *a = dut();
    uint8_t b[256]; size_t o = 0;
    b[o++] = 0;
    o += msg(b + o, 1, 1, EV_JOININ, false, 100);
    o += msg(b + o, 1, 2, EV_JOININ, false, 100); /* second message of the same type */
    b[o++] = 0; b[o++] = 0;
    fault_once(fault);
    int r = mrp_rx(a, 0, b, o);
    fault_none();
    unsigned j2 = count_ind(0, 'J', 1, 2, NULL);
    if (r < 0) {
        CHECK(j2 == 0, "later attribute indicated after failure");
        CHECK(!query(a, 0, 1, 2).found || query(a, 0, 1, 2).reg == MRP_REG_STATE_MT, "later attribute registered");
        CHECK(mrp_rx(a, 0, b, o) == 0, "retry");
    }
    CHECK(count_ind(0, 'J', 1, 1, NULL) == 1 && count_ind(0, 'J', 1, 2, NULL) == 1, "joins %u/%u",
          count_ind(0, 'J', 1, 1, NULL), count_ind(0, 'J', 1, 2, NULL));
    teardown(a);
}

/* ---------------- P5: Re-declare withdrawal under exhaustion ---------------- */
static void redeclare_case(unsigned fault)
{
    snprintf(ctxname, sizeof(ctxname), "redeclare persistent fault=%u", fault);
    struct mrp_app *a = dut();
    uint8_t b[256]; size_t n = pdu1(b, 1, 1, EV_JOININ, false);
    CHECK(mrp_rx(a, 0, b, n) == 0, "setup");
    mrp_port_role_change(a, 0, false);
    fault_from(fault);
    ticks(80);
    host_view(a, 0, 1, 1);
    fault_none(); ticks(2);
    CHECK(count_ind(0, 'L', 1, 1, NULL) == 1, "leaves %u", count_ind(0, 'L', 1, 1, NULL));
    host_view(a, 0, 1, 1);
    teardown(a);
}

/* ---------------- P6: LeaveAll in a later message after a failure ---------------- */
static void later_leaveall(void)
{
    snprintf(ctxname, sizeof(ctxname), "later LeaveAll after failure");
    struct mrp_app *a = dut();
    uint8_t b[256]; size_t n = pdu1(b, 1, 2, EV_JOININ, false);
    CHECK(mrp_rx(a, 0, b, n) == 0, "setup talker sid 2");
    size_t o = 0; b[o++] = 0;
    o += msg(b + o, 3, 1, EV_JOININ, false, 0); /* Listener: reservation fails */
    o += msg(b + o, 1, 2, EV_JOININ, true, 100); /* LeaveAll + JoinIn for registered Talker */
    b[o++] = 0; b[o++] = 0;
    fault_once(2);
    int r = mrp_rx(a, 0, b, o);
    fault_none();
    printf("  info [%s]: rc=%d talker sid2 reg after failed pass=%s\n", ctxname, r,
           mrp_reg_state_name(query(a, 0, 1, 2).reg));
    CHECK(mrp_rx(a, 0, b, o) == 0, "retry");
    CHECK(query(a, 0, 1, 2).reg == MRP_REG_STATE_IN, "talker not IN after retry");
    ticks(70);
    CHECK(count_ind(0, 'L', 1, 2, NULL) == 0, "talker withdrawn after retry");
    teardown(a);
}

int main(void)
{
    printf("profile LWSRP_MILAN=%d\n", LWSRP_MILAN);
    unsigned flush_cases = 0;
    for (unsigned lv = 0; lv < 2; ++lv) {
        for (unsigned nattr = 1; nattr <= 2; ++nattr) {
            for (unsigned fault = 0; fault <= 3u * nattr + 1u; ++fault) {
                flush_case(lv, nattr, fault, false, 0); ++flush_cases;
                if (fault) {
                    for (unsigned hold = 0; hold <= 3; ++hold) { flush_case(lv, nattr, fault, true, hold); ++flush_cases; }
                }
            }
        }
    }
    printf("flush cases %u; cases with observer gaps %u\n", flush_cases, obs_gap_cases);
    flush_then_join();
    flush_with_peer_joins(false);
    flush_with_peer_joins(true);
    unsigned rcases = 0;
    for (uint8_t old = 1; old <= 2; ++old) {
        for (unsigned lv = 0; lv < 2; ++lv) {
            for (unsigned fault = 0; fault <= 11; ++fault) {
                for (int mode = 0; mode < 2; ++mode) {
                    replacement_case(old, lv, fault, false, mode); ++rcases;
                    if (fault) { replacement_case(old, lv, fault, true, mode); ++rcases; }
                }
            }
        }
    }
    printf("replacement cases %u\n", rcases);
    for (unsigned f = 1; f <= 9; ++f) { receive_stop_case(f); }
    for (unsigned f = 1; f <= 3; ++f) { redeclare_case(f); }
    later_leaveall();
    printf("checks %u failures %u\n", checks, failures);
    return failures != 0;
}
