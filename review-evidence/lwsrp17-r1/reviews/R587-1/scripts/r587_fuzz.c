/* SPDX-License-Identifier: Apache-2.0 */
/*
 * Reviewer-owned differential driver for lwSRP PR #18.
 * Usage: r587_fuzz <seed> <app 0=MSRP 1=MVRP 2=MMRP> <mode 0=roomy 1=tight> <steps>
 * Deterministic random declarations, withdrawals, received PDUs, timer ticks,
 * send refusals and transmit opportunities. Prints one line per call:
 *   C <step> <capacity> <result>
 *   S <rc> <len> <hex>
 *   O <step> <capacity>  (octets written past the declared capacity)
 *   R <step>             (a retried PDU differs from the refused one)
 * The same binary links against either the base or the head library.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "shish_lan/mmrp.h"
#include "shish_lan/msrp.h"
#include "shish_lan/mvrp.h"
#include "ports/timer.h"

static unsigned long long rng;
static unsigned rnd(unsigned n)
{
    rng = rng * 6364136223846793005ull + 1442695040888963407ull;
    return (unsigned)((rng >> 33) % n);
}

#define GUARD 4096u
static uint8_t storage[70000 + GUARD];
static uint8_t refused[70000];
static size_t refused_len;
static int have_refused;
static unsigned step;

static int send_fn(void *ctx, uint8_t port, const uint8_t *pdu, size_t len)
{
    (void)ctx; (void)port;
    int rc = rnd(8) == 0 ? -11 : 0;
    if (have_refused && (len != refused_len || memcmp(pdu, refused, len))) {
        printf("R %u\n", step);
    }
    have_refused = 0;
    if (rc) {
        memcpy(refused, pdu, len);
        refused_len = len;
        have_refused = 1;
    }
    printf("S %d %zu ", rc, len);
    for (size_t k = 0; k < len; ++k) {
        printf("%02x", pdu[k]);
    }
    printf("\n");
    return rc;
}

static struct msrp_talker_adv talker(unsigned uid)
{
    struct msrp_talker_adv t = {
        .stream_id = {{0x02, 0, 0, 0, 0, 0x10, (uint8_t)(uid >> 8), (uint8_t)uid}},
        .dest_mac = {0x91, 0xe0, 0xf0, 0x00, 0xfe, (uint8_t)uid},
        .vlan_id = 2, .max_frame_size = 224, .max_interval_frames = 1,
        .priority_and_rank = 0x60, .accumulated_latency = 2000,
    };
    return t;
}

static size_t rx_pdu(unsigned app, uint8_t *p)
{
    unsigned ev = rnd(6), la = rnd(10) == 0, v = rnd(24);
    size_t n = 0;
    p[n++] = 0;
    if (app == 0) {
        if (rnd(2)) {
            uint8_t m[] = {0x03, 0x08, 0x00, 0x0e, (uint8_t)(la << 5), 1,
                           0x02, 0, 0, 0, 0, 0x20, 0, (uint8_t)v, (uint8_t)(ev * 36), (uint8_t)(rnd(4) << 6), 0, 0};
            memcpy(p + n, m, sizeof(m)); n += sizeof(m);
        } else {
            uint8_t m[] = {0x04, 0x04, 0x00, 0x09, (uint8_t)(la << 5), 1,
                           (uint8_t)(5 + rnd(2)), (uint8_t)(2 + rnd(2)), 0, 2, (uint8_t)(ev * 36), 0, 0};
            memcpy(p + n, m, sizeof(m)); n += sizeof(m);
        }
    } else if (app == 1) {
        uint8_t m[] = {0x01, 0x02, (uint8_t)(la << 5), 1, 0, (uint8_t)(1 + v), (uint8_t)(ev * 36), 0, 0};
        memcpy(p + n, m, sizeof(m)); n += sizeof(m);
    } else {
        uint8_t m[] = {0x02, 0x06, (uint8_t)(la << 5), 1, 0x91, 0xe0, 0xf0, 1, 0, (uint8_t)v,
                       (uint8_t)(ev * 36), 0, 0};
        memcpy(p + n, m, sizeof(m)); n += sizeof(m);
    }
    p[n++] = 0; p[n++] = 0;
    return n;
}

static void op(struct mrp_app *a, unsigned app)
{
    unsigned v = rnd(24);
    int r = 0;
    switch (app * 10 + rnd(app == 0 ? 7 : 3)) {
    case 0: { struct msrp_talker_adv t = talker(v); r = msrp_declare_talker(a, 0, &t, rnd(2)); break; }
    case 1: { struct msrp_talker_adv t = talker(v); r = msrp_withdraw_talker(a, 0, &t.stream_id); break; }
    case 2: { struct msrp_stream_id s = {{0x02, 0, 0, 0, 0, (uint8_t)(0x20 + rnd(3)), 0, (uint8_t)v}};
              r = msrp_declare_listener(a, 0, &s, (enum msrp_listener_decl)(1 + rnd(3))); break; }
    case 3: { struct msrp_stream_id s = {{0x02, 0, 0, 0, 0, 0x20, 0, (uint8_t)v}};
              r = msrp_withdraw_listener(a, 0, &s); break; }
    case 4: { struct msrp_domain d = {(uint8_t)(5 + rnd(2)), (uint8_t)(2 + rnd(2)), 2};
              r = rnd(3) ? mrp_mad_join(a, 0, MSRP_ATTR_TYPE_DOMAIN, &d, false)
                         : mrp_mad_leave(a, 0, MSRP_ATTR_TYPE_DOMAIN, &d); break; }
    case 5: { struct msrp_talker_failed f = {talker(v), {0, 0, 0, 0, 0, 0, 0, 1, (uint8_t)(1 + rnd(9))}};
              r = rnd(3) ? mrp_mad_join(a, 0, MSRP_ATTR_TYPE_TALKER_FAILED, &f, rnd(2))
                         : mrp_mad_leave(a, 0, MSRP_ATTR_TYPE_TALKER_FAILED, &f); break; }
    case 6: case 12: case 22: { uint8_t p[64]; size_t n = rx_pdu(app, p); r = mrp_rx(a, 0, p, n); break; }
    case 10: r = mvrp_declare(a, 0, (uint16_t)(1 + v)); break;
    case 11: r = mvrp_withdraw(a, 0, (uint16_t)(1 + v)); break;
    case 20: case 21: {
        struct mmrp_mac m = {{0x91, 0xe0, 0xf0, 1, 0, (uint8_t)v}};
        if (v == 23) {
            r = rnd(2) ? mmrp_declare_svc(a, 0, MMRP_SVC_FORWARD_UNREGISTERED)
                       : mmrp_withdraw_svc(a, 0, MMRP_SVC_FORWARD_UNREGISTERED);
        } else {
            r = rnd(3) ? mmrp_declare_mac(a, 0, &m) : mmrp_withdraw_mac(a, 0, &m);
        }
        break;
    }
    default: break;
    }
    printf("X %u %d\n", step, r);
}

int main(int argc, char **argv)
{
    if (argc != 5) {
        return 2;
    }
    rng = strtoull(argv[1], NULL, 0);
    unsigned app = (unsigned)atoi(argv[2]), tight = (unsigned)atoi(argv[3]), steps = (unsigned)atoi(argv[4]);
    struct msrp_ctx sctx = {0};
    struct mvrp_ctx vctx = {0};
    struct mmrp_ctx mctx = {0};
    struct mrp_app *a = app == 0 ? msrp_app_create(1, &sctx) :
                        app == 1 ? mvrp_app_create(1, &vctx) : mmrp_app_create(1, &mctx);
    static const size_t roomy[] = {4000, 8000, 65535, 70000};
    static const size_t tight_msrp[] = {20, 40, 60, 80, 120, 150, 200, 300};
    static const size_t tight_other[] = {8, 12, 16, 20, 24, 31, 40, 64};
    for (step = 0; step < steps; ++step) {
        unsigned ops = rnd(4);
        while (ops--) {
            op(a, app);
        }
        size_t cap = tight ? (app == 0 ? tight_msrp[rnd(8)] : tight_other[rnd(8)]) : roomy[rnd(4)];
        if (have_refused) {
            cap = 70000; /* keep a retained PDU's storage large and unchanged */
        }
        memset(storage + cap, 0xA5, GUARD);
        int r = mrp_transmit(a, 0, storage, cap, send_fn, NULL);
        for (size_t k = 0; k < GUARD; ++k) {
            if (storage[cap + k] != 0xA5) {
                printf("O %u %zu\n", step, cap);
                break;
            }
        }
        printf("C %u %zu %d\n", step, cap, r);
        unsigned t = rnd(5) == 0 ? 300u + rnd(1200) : rnd(40);
        while (t--) {
            shlan_timer_tick();
        }
    }
    printf("END\n");
    return 0;
}
