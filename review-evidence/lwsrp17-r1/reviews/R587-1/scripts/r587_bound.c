/* SPDX-License-Identifier: Apache-2.0 */
/*
 * Reviewer probe: the 65535-octet MSRP bound and the in-place ordering cost.
 * Usage: r587_bound <order 0=list ascending 1=list descending> <values> <capacity> <out.bin>
 * Writes the offered PDU to out.bin and prints its length and the wall time.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "shish_lan/msrp.h"

static size_t got;
static FILE *out;

static int keep(void *ctx, uint8_t port, const uint8_t *pdu, size_t len)
{
    (void)ctx; (void)port;
    got = len;
    fwrite(pdu, 1, len, out);
    return 0;
}

int main(int argc, char **argv)
{
    if (argc != 5) {
        return 2;
    }
    unsigned order = (unsigned)atoi(argv[1]), values = (unsigned)atoi(argv[2]);
    size_t cap = (size_t)strtoull(argv[3], NULL, 0);
    static uint8_t storage[1u << 18];
    if (cap > sizeof(storage)) {
        return 2;
    }
    out = fopen(argv[4], "wb");
    struct msrp_ctx ctx = {0};
    struct mrp_app *a = msrp_app_create(1, &ctx);
    for (unsigned k = 0; k < values; ++k) {
        unsigned uid = order ? k : values - 1u - k;
        struct msrp_talker_adv t = {
            .stream_id = {{0x02, 0, 0, 0, 0, 0x10, (uint8_t)(uid >> 8), (uint8_t)uid}},
            .dest_mac = {0x91, 0xe0, 0xf0, 0x00, 0xfe, 0},
            .vlan_id = 2, .max_frame_size = 224, .max_interval_frames = 1,
            .priority_and_rank = 0x60, .accumulated_latency = 2000,
        };
        if (msrp_declare_talker(a, 0, &t, true) != 0) {
            return 3;
        }
    }
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    int r = mrp_transmit(a, 0, storage, cap, keep, NULL);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    fclose(out);
    printf("result=%d len=%zu ms=%.2f\n", r, got,
           (t1.tv_sec - t0.tv_sec) * 1e3 + (t1.tv_nsec - t0.tv_nsec) / 1e6);
    msrp_app_destroy(a);
    return 0;
}
