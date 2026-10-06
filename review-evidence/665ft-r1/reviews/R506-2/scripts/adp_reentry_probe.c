// R506-2 probe: ADP ports that call back into the core while the core is
// calling them (adp.h states no rule either way). Each scenario prints the
// machine's state; adp_reentry_probe.py measures which exclusion rows' arcs it reaches.
#include <stdio.h>
#include <string.h>
#include "adp.h"
static struct adp A;
static int hook;          // which re-entrant call the next port call makes
static bool link_level = true;
static bool p_send(void *c, unsigned i, const uint8_t *f, size_t n) {
    (void)c; (void)i; (void)f; (void)n;
    if (hook == 1) { hook = 0; adp_link_change(&A, false); }    // a send port that reports the link it found down
    return true;
}
static void p_timer_start(void *c, unsigned i, uint32_t ms) {
    (void)c; (void)i; (void)ms;
    if (hook == 2) { hook = 0; adp_timer_expired(&A); }  // a timer port that expires an elapsed delay at once
}
static void p_timer_stop(void *c, unsigned i) { (void)c; (void)i; }
static void p_gptp(void *c, unsigned i, uint64_t *g, uint8_t *d) { (void)c; (void)i; *g = 1; *d = 0; }
static bool p_link(void *c, unsigned i) { (void)c; (void)i; return link_level; }
static uint32_t p_seed(void *c) { (void)c; return 7u; }
static const struct adp_ports PORTS = {0, p_send, p_timer_start, p_timer_stop, p_gptp, p_link, p_seed};
static const struct adp_entity ENT = {0x0011223344556677ull, 1, 0x001122334455ull, 0, 0, 0, 0, 0, 0};
static const char *st(void) { return A.state == ADP_STATE_DOWN ? "DOWN" : A.state == ADP_STATE_DELAY ? "DELAY" : "WAITING"; }
static const char *tm(void) { return A.timer == ADP_TIMER_NONE ? "NONE" : A.timer == ADP_TIMER_DELAY ? "DELAY" : "ADVERTISE"; }
static void fresh(void) { adp_init(&A, &ENT, &PORTS, 0, 0); hook = 0; link_level = true; adp_set_enable(&A, true); }
int main(void) {
    // S1: send port reports link down from inside the ENTITY_AVAILABLE send
    fresh(); hook = 1; adp_timer_expired(&A);
    printf("S1 after advertise with nested link-down: state=%s timer=%s link_up=%d\n", st(), tm(), A.link_up);
    uint32_t d = A.draws; adp_link_change(&A, true);
    printf("S1 link up again: state=%s draws+%u (row 1 arc 2: no DELAY entered)\n", st(), A.draws - d);
    // S2: send port reports link down from inside SHUTDOWN's ENTITY_DEPARTING send
    fresh(); hook = 1; adp_set_enable(&A, false);
    printf("S2 shutdown with nested link-down: state=%s enabled=%d (row 2 arc 2 reached inside)\n", st(), A.enabled);
    // S3: timer port expiring TMR_ADVERTISE inside timer_start
    fresh(); hook = 2; adp_timer_expired(&A);
    printf("S3 advertise, ADVERTISE expired inside timer_start: state=%s timer=%s stray=%u\n", st(), tm(), A.stray_expiries);
    // S4: timer port expiring TMR_DELAY inside timer_start (from WAITING via a GM change)
    fresh(); adp_timer_expired(&A); hook = 2; adp_gm_change(&A);
    printf("S4 gm change, DELAY expired inside timer_start: state=%s timer=%s stray=%u\n", st(), tm(), A.stray_expiries);
    return 0;
}
