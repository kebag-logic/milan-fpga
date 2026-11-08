// SPDX-License-Identifier: MIT
#include "acmp.h"
#include "wire.h"
#include <string.h>

static bool room;
static uint32_t clock;
static volatile uint8_t *const uart = (volatile uint8_t *)0x10000000u;

static void put(const char *s) { while (*s) *uart = (uint8_t)*s++; }
static void num(uint32_t v)
{
    char b[11];
    int i = 10;
    b[i] = 0;
    do { b[--i] = (char)('0' + v % 10u); v /= 10u; } while (v);
    put(b + i);
}
static inline uint32_t instret(void)
{
    uint32_t v;
    __asm__ volatile("csrr %0, minstret" : "=r"(v));
    return v;
}
static bool send(void *c, unsigned i, const uint8_t *f, size_t n) { (void)c; (void)i; (void)f; (void)n; return room; }
static uint32_t now(void *c) { (void)c; return clock; }
static void timer(void *c, unsigned i, bool a, uint32_t d) { (void)c; (void)i; (void)a; (void)d; }
static void gptp(void *c, unsigned i, uint64_t *g, uint8_t *d) { (void)c; (void)i; *g = 1; *d = 0; }
static uint32_t seed(void *c) { (void)c; return 7; }
static void admit(void *c, unsigned i, unsigned s, bool b, uint64_t t) { (void)c; (void)i; (void)s; (void)b; (void)t; }
static void publish(void *c, unsigned i, unsigned s, bool b, bool st, uint64_t id, bool m)
{ (void)c; (void)i; (void)s; (void)b; (void)st; (void)id; (void)m; }
static bool locked(void *c, uint64_t *h) { (void)c; *h = 0; return false; }
static void source(void *c, unsigned i, struct acmp_source_state *o)
{ (void)c; (void)i; memset(o, 0, sizeof *o); o->dest_mac_valid = true; o->stream.stream_id = 5; }
static void srp(void *c, unsigned s, const struct acmp_stream *st) { (void)c; (void)s; (void)st; }
static void note(void *c, unsigned s) { (void)c; (void)s; }

static const struct acmp_ports ports = {0, send, now, timer, gptp, seed, admit, publish};
static const struct acmp_env env = {0, locked, source, srp, note, note};
static struct acmp core;
static uint8_t frame[ACMP_FRAME_BYTES];

static void cmd(uint8_t msg, uint64_t talker, uint64_t listener, uint16_t tuid, uint16_t luid, uint16_t seq)
{
    memset(frame, 0, sizeof frame);
    wire_put_be(frame, 0x91E0F0010000ull, 6);
    wire_put_be(frame + 12, 0x22f0, 2);
    frame[14] = 0xfc;
    frame[15] = msg;
    wire_put_be(frame + 16, 44, 2);
    wire_put_be(frame + 26, 0x1112131415161718ull, 8);
    wire_put_be(frame + 34, talker, 8);
    wire_put_be(frame + 42, listener, 8);
    wire_put_be(frame + 50, tuid, 2);
    wire_put_be(frame + 52, luid, 2);
    wire_put_be(frame + 62, seq, 2);
}

static uint32_t overhead;
static uint32_t rx_cost(void)
{
    uint32_t t0 = instret();
    (void)acmp_rx(&core, 0, frame, sizeof frame);
    uint32_t t1 = instret();
    return t1 - t0 - overhead;
}
static void report(const char *name, uint32_t v) { put(name); put(" "); num(v); put("\n"); }

static void fresh(void)
{
    struct acmp_config cfg = {.entity_id = 1, .n_interfaces = 1, .n_sinks = ACMP_MAX_SINKS, .n_sources = ACMP_MAX_SOURCES};
    (void)acmp_init(&core, &cfg, &ports, &env);
    acmp_open(&core);
    room = true;
}
static void owe(unsigned n)
{
    room = false;
    for (unsigned k = 0; k < n; ++k) {
        cmd(10, 0, 1, 0, 0, (uint16_t)(0x100 + k));
        (void)acmp_rx(&core, 0, frame, sizeof frame);
    }
}

int main(void)
{
    uint32_t t0 = instret();
    uint32_t t1 = instret();
    overhead = t1 - t0;
    report("csr_pair_overhead", overhead);
    uint32_t worst = 0, v;
#define STEP(name) do { v = rx_cost(); report(name, v); if (v > worst) worst = v; } while (0)
    fresh(); cmd(10, 0, 1, 0, 0, 1); STEP("get_rx_state_sent");
    fresh(); owe(7); cmd(10, 0, 1, 0, 0, 2); STEP("get_rx_state_owed_behind_7");
    fresh(); owe(8); cmd(10, 0, 1, 0, 0, 3); STEP("get_rx_state_behind_full_set");
    fresh(); owe(8); cmd(6, 2, 1, 0, 15, 4); STEP("bind_rx_behind_full_set");
    fresh(); owe(8); cmd(0, 1, 2, 15, 0, 5); STEP("probe_tx_behind_full_set");
    fresh(); cmd(6, 2, 1, 0, 15, 6); STEP("bind_rx_sent");
    fresh(); owe(6); cmd(6, 2, 1, 0, 15, 7); STEP("bind_rx_owed_behind_6");
    fresh(); owe(7); cmd(6, 2, 1, 0, 15, 8); STEP("bind_rx_behind_7");
    fresh(); cmd(0, 1, 2, 15, 0, 9); STEP("probe_tx_sent");
    fresh(); owe(7); cmd(0, 1, 2, 15, 0, 10); STEP("probe_tx_owed_behind_7");
    fresh(); cmd(4, 1, 2, 15, 0, 11); STEP("get_tx_state_sent");
    fresh(); cmd(8, 2, 1, 0, 15, 12); STEP("unbind_rx_sent");
    report("worst_acmp_rx_step", worst);
    fresh(); owe(8); room = true;
    t0 = instret(); (void)acmp_poll(&core); t1 = instret();
    report("poll_one_owed_frame", t1 - t0 - overhead);
#ifdef LANE
    t0 = instret(); v = acmp_rx_ready(&core); t1 = instret();
    report("rx_ready_query", t1 - t0 - overhead);
#endif
    put("done\n");
    return 0;
}
