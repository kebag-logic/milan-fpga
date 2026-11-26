// SPDX-License-Identifier: MIT
#include "adp.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

struct port { unsigned samples; uint32_t sample, delay; bool link; };
static bool send_frame(void *c, unsigned i, const uint8_t *f, size_t n)
{ (void)c; (void)i; (void)f; assert(n == 82); return true; }
static void start(void *c, unsigned i, uint32_t d)
{ (void)i; ((struct port *)c)->delay = d; }
static void stop(void *c, unsigned i) { (void)c; (void)i; }
static void gm(void *c, unsigned i, uint64_t *g, uint8_t *d)
{ (void)c; (void)i; *g = 1; *d = 0; }
static bool link(void *c, unsigned i) { (void)i; return ((struct port *)c)->link; }
static uint32_t seed(void *c)
{ struct port *p = c; ++p->samples; return p->sample; }
static const struct adp_entity entity = {
    .entity_id = 0x1122334455667788ull, .mac = 0x001B921122AAull
};
int main(void)
{
    struct port p = {.sample = 40000};
    struct adp_ports ports = {&p, send_frame, start, stop, gm, link, seed};
    struct adp a, other;
    adp_init(&a, &entity, &ports, 0, 0);
    adp_init(&other, &entity, &ports, 1, 0);
    assert(p.samples == 0);
    adp_set_enable(&a, true);
    adp_set_enable(&other, true);
    assert(p.samples == 0);
    for (unsigned n = 1; n <= 100; ++n) {
        adp_link_change(&a, true);
        assert(p.samples == n && a.last_draw_ms <= 4000);
        uint32_t state = a.rng;
        adp_link_change(&a, true);
        assert(p.samples == n && a.rng == state);
        adp_timer_expired(&a);
        assert(p.delay == 5000);
        uint8_t f[82] = {0};
        f[12] = 0x22; f[13] = 0xf0; f[14] = 0xfa; f[15] = 2; f[17] = 56;
        adp_rx(&a, f, sizeof f);
        assert(a.state == ADP_STATE_DELAY && p.samples == n);
        adp_timer_expired(&a);
        adp_gm_change(&a);
        assert(a.state == ADP_STATE_DELAY && p.samples == n);
        adp_timer_expired(&a);
        adp_timer_expired(&a);
        assert(a.state == ADP_STATE_DELAY && p.samples == n);
        adp_link_change(&a, false);
    }
    adp_link_change(&other, true);
    assert(p.samples == 101);
    adp_set_enable(&a, false);
    adp_link_change(&a, true);
    assert(p.samples == 101);
    p.link = true;
    adp_set_enable(&a, true);
    assert(p.samples == 102 && a.last_draw == ADP_DRAW_STARTUP && a.last_draw_ms <= 2000);
    puts("PASS: 100 rises, duplicate/disabled events, other interface, startup, DISCOVER, GM_CHANGE, advertise expiry; advertise period 5000 ms");
    for (unsigned startup = 0; startup < 2; ++startup) {
        unsigned bins[16] = {0}, seen[4001] = {0}, distinct = 0;
        for (uint32_t k = 0; k < 4096; ++k) {
            p.link = startup != 0; p.sample = 40000;
            adp_init(&a, &entity, &ports, 0, 0);
            adp_set_enable(&a, true);
            if (!startup) adp_link_change(&a, true);
            adp_link_change(&a, false);
            p.sample = 90000 + k;
            adp_link_change(&a, true);
            assert(a.last_draw_ms <= 4000);
            unsigned ms = a.last_draw_ms;
            if (!seen[ms]++) ++distinct;
            ++bins[ms * 16 / 4001];
        }
        unsigned sq = 0;
        for (unsigned i = 0; i < 16; ++i) {
            int d = (int)bins[i] - 256;
            sq += (unsigned)(d * d);
        }
        assert(distinct >= 2400 && sq * 16 / 256 <= 490);
        printf("history_startup=%u boots=4096 distinct=%u chi_square_x16=%u bins=", startup, distinct, sq * 16 / 256);
        for (unsigned i = 0; i < 16; ++i) printf("%s%u", i ? "," : "", bins[i]);
        puts("");
    }
    return 0;
}
