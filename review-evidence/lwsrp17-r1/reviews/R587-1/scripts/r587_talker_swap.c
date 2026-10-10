/* SPDX-License-Identifier: Apache-2.0 */
/*
 * Reviewer probe: a Talker Failed <-> Talker Advertise change for one stream.
 * Usage: r587_talker_swap [reverse]  (reverse: Advertise first, then Failed)
 * Prints every transmitted PDU, then feeds each post-change PDU to a fresh
 * receiver that first applied PDU 0 (the original declaration), and prints
 * its indications.
 */
#include <stdio.h>
#include <string.h>
#include "shish_lan/msrp.h"
#include "ports/timer.h"

static uint8_t pdus[16][512];
static size_t lens[16];
static unsigned n_pdus;

static int keep(void *ctx, uint8_t port, const uint8_t *pdu, size_t len)
{
    (void)ctx; (void)port;
    if (n_pdus < 16 && len <= sizeof(pdus[0])) {
        memcpy(pdus[n_pdus], pdu, len);
        lens[n_pdus++] = len;
    }
    return 0;
}

static void on_ta(struct msrp_ctx *c, uint8_t p, const struct msrp_talker_adv *a, bool is_new)
{
    (void)c; (void)p; (void)a;
    printf("   ind: TalkerAdvertise join new=%d\n", is_new);
}
static void on_tf(struct msrp_ctx *c, uint8_t p, const struct msrp_talker_failed *a, bool is_new)
{
    (void)c; (void)p; (void)a;
    printf("   ind: TalkerFailed join new=%d\n", is_new);
}
static void on_leave(struct msrp_ctx *c, uint8_t p, uint8_t type, const void *v)
{
    (void)c; (void)p; (void)v;
    printf("   ind: leave type %u\n", type);
}

static struct msrp_talker_adv talker(void)
{
    struct msrp_talker_adv t = {
        .stream_id = {{0x02, 0, 0, 0, 0, 0x10, 0, 1}},
        .dest_mac = {0x91, 0xe0, 0xf0, 0x00, 0xfe, 1},
        .vlan_id = 2, .max_frame_size = 224, .max_interval_frames = 1,
        .priority_and_rank = 0x60, .accumulated_latency = 2000,
    };
    return t;
}

static void hex(const uint8_t *p, size_t n)
{
    for (size_t k = 0; k < n; ++k) {
        printf("%02x", p[k]);
    }
    printf("\n");
}

int main(int argc, char **argv)
{
    bool reverse = argc > 1 && strcmp(argv[1], "reverse") == 0;
    static uint8_t buf[1500];
    struct msrp_ctx tctx = {0};
    struct mrp_app *tx = msrp_app_create(1, &tctx);
    struct msrp_talker_failed f = {talker(), {0, 0, 0, 0, 0, 0, 0, 1, 2}};
    struct msrp_talker_adv t = talker();
    if (reverse) {
        printf("declare TA: %d\n", msrp_declare_talker(tx, 0, &t, true));
    } else {
        printf("declare TF: %d\n", mrp_mad_join(tx, 0, MSRP_ATTR_TYPE_TALKER_FAILED, &f, true));
    }
    printf("tx: %d\n", mrp_transmit(tx, 0, buf, sizeof(buf), keep, NULL));
    for (int k = 0; k < 30; ++k) { shlan_timer_tick(); }
    printf("tx: %d\n", mrp_transmit(tx, 0, buf, sizeof(buf), keep, NULL));
    for (int k = 0; k < 30; ++k) { shlan_timer_tick(); }
    if (reverse) {
        printf("withdraw TA: %d\n", msrp_withdraw_talker(tx, 0, &t.stream_id));
        printf("declare TF: %d\n", mrp_mad_join(tx, 0, MSRP_ATTR_TYPE_TALKER_FAILED, &f, true));
    } else {
        printf("withdraw TF: %d\n", mrp_mad_leave(tx, 0, MSRP_ATTR_TYPE_TALKER_FAILED, &f));
        printf("declare TA: %d\n", msrp_declare_talker(tx, 0, &t, true));
    }
    unsigned first = n_pdus;
    for (int round = 0; round < 3; ++round) {
        printf("tx: %d\n", mrp_transmit(tx, 0, buf, sizeof(buf), keep, NULL));
        for (int k = 0; k < 30; ++k) { shlan_timer_tick(); }
    }
    for (unsigned k = 0; k < n_pdus; ++k) {
        printf("pdu %u: ", k);
        hex(pdus[k], lens[k]);
    }
    /* Receivers: register TF from the first PDU, then apply each later PDU. */
    for (unsigned k = first; k < n_pdus; ++k) {
        struct msrp_ctx rctx = {.on_talker_advertise = on_ta, .on_talker_failed = on_tf, .on_leave = on_leave};
        struct mrp_app *rx = msrp_app_create(1, &rctx);
        printf("receiver: pdu 0 -> %d\n", mrp_rx(rx, 0, pdus[0], lens[0]));
        printf("receiver: pdu %u -> %d\n", k, mrp_rx(rx, 0, pdus[k], lens[k]));
        for (int j = 0; j < 400; ++j) { shlan_timer_tick(); }
        printf("receiver: after timers\n");
        msrp_app_destroy(rx);
    }
    msrp_app_destroy(tx);
    return 0;
}
