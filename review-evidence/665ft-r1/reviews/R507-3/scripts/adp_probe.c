/* Reproduce the README's conditional ADP exclusion claims through public calls. */
#include "adp.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

struct rig { struct adp core; int mode; int armed; };
static bool send_port(void *v, unsigned i, const uint8_t *f, size_t n) {
    struct rig *r = v;
    (void)i; (void)n;
    unsigned message = f[ADP_HEADER_BYTES + 1] & 15;
    if ((r->mode == 1 && message == ADP_MSG_ENTITY_AVAILABLE) ||
        (r->mode == 2 && message == ADP_MSG_ENTITY_DEPARTING))
        adp_link_change(&r->core, false);
    return r->mode != 5 && r->mode != 6;
}
static void timer_start_port(void *v, unsigned i, uint32_t ms) {
    struct rig *r = v;
    (void)i; (void)ms;
    if (r->armed && ((r->mode == 3 && r->core.timer == ADP_TIMER_ADVERTISE) ||
                     (r->mode == 4 && r->core.timer == ADP_TIMER_DELAY))) {
        r->armed = 0;
        adp_timer_expired(&r->core);
    }
}
static void stop_port(void *v, unsigned i) { (void)v; (void)i; }
static void gptp_port(void *v, unsigned i, uint64_t *gm, uint8_t *domain) {
    (void)v; (void)i; *gm = 0; *domain = 0;
}
static bool link_port(void *v, unsigned i) {
    struct rig *r = v;
    (void)i;
    if (r->mode == 5 || r->mode == 6) {
        adp_link_change(&r->core, true);
        adp_timer_expired(&r->core);
        return false;
    }
    return true;
}
static uint32_t seed_port(void *v) { (void)v; return 1; }
int main(int argc, char **argv) {
    assert(argc == 2);
    struct rig r = {.mode = atoi(argv[1]), .armed = 1};
    const struct adp_entity entity = {.entity_id = 1};
    const struct adp_ports ports = {.ctx = &r, .send = send_port,
        .timer_start = timer_start_port, .timer_stop = stop_port,
        .gptp = gptp_port, .link_up = link_port, .seed = seed_port};
    adp_init(&r.core, &entity, &ports, 0, 0);
    if (r.mode == 4) r.armed = 0;
    adp_set_enable(&r.core, true);
    if (r.mode <= 4) adp_timer_expired(&r.core);
    if (r.mode == 1) {
        assert(r.core.state == ADP_STATE_WAITING && !r.core.link_up);
        assert(r.core.timer == ADP_TIMER_ADVERTISE);
        adp_link_change(&r.core, true);
        assert(r.core.state == ADP_STATE_WAITING);
    } else if (r.mode == 2) {
        adp_set_enable(&r.core, false);
        assert(r.core.state == ADP_STATE_DOWN && !r.core.link_up);
    } else if (r.mode == 3) {
        assert(r.core.state == ADP_STATE_WAITING && r.core.timer == ADP_TIMER_NONE);
        assert(r.core.stray_expiries == 1);
    } else if (r.mode == 4) {
        r.armed = 1;
        adp_gm_change(&r.core);
        assert(r.core.state == ADP_STATE_DELAY && r.core.timer == ADP_TIMER_NONE);
        assert(r.core.stray_expiries == 1);
    } else {
        assert(r.core.state == ADP_STATE_DOWN && r.core.available_owed);
        if (r.mode == 6) adp_set_enable(&r.core, false);
        assert(!adp_poll(&r.core));
        assert(!r.core.available_owed);
    }
    printf("case %d: expected state=%d timer=%d owed=%d stray=%u\n", r.mode,
           r.core.state, r.core.timer, r.core.available_owed, r.core.stray_expiries);
}
