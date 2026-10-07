/* SPDX-License-Identifier: Apache-2.0 */
/* Reviewer probes: receive-side behaviour at a given source tree. */
#include <stdio.h>
#include <string.h>
#include "shish_lan/msrp.h"
#include "shish_lan/mvrp.h"
#include "ports/timer.h"

static unsigned listener_inds, talker_inds, leave_inds;
static int last_decl = -1, last_frame = -1;
static void on_listener(struct msrp_ctx *c, uint8_t p, const struct msrp_stream_id *s,
                        enum msrp_listener_decl d, bool n)
{
    (void)c; (void)p; (void)s; (void)n; ++listener_inds; last_decl = (int)d;
}
static void on_talker(struct msrp_ctx *c, uint8_t p, const struct msrp_talker_adv *t, bool n)
{
    (void)c; (void)p; (void)n; ++talker_inds; last_frame = t->max_frame_size;
}
static void on_leave(struct msrp_ctx *c, uint8_t p, uint8_t t, const void *v)
{
    (void)c; (void)p; (void)t; (void)v; ++leave_inds;
}
static struct msrp_ctx ctx = { .on_talker_advertise = on_talker, .on_listener = on_listener,
                               .on_leave = on_leave };
static int fails;
#define CHECK(name, cond) do { int ok_ = (cond); printf("%s %s\n", ok_ ? "PASS" : "FAIL", name); fails += !ok_; } while (0)

/* Listener JoinIn for stream 01..08 with FourPacked declaration decl; la sets LeaveAll. */
static size_t listener_pdu(uint8_t *b, unsigned decl, int la)
{
    uint8_t p[] = {0, 3, 8, 0, 14, la ? 0x20 : 0, 1, 1, 2, 3, 4, 5, 6, 7, 8,
                   36, (uint8_t)(decl << 6), 0, 0, 0, 0};
    memcpy(b, p, sizeof(p));
    return sizeof(p);
}
/* Talker Advertise JoinIn with MaxFrameSize frame. */
static size_t talker_pdu(uint8_t *b, unsigned frame, int la)
{
    uint8_t p[1 + 4 + 2 + 25 + 1 + 2 + 2] = {0, 1, 25, 0, 30, la ? 0x20 : 0, 1};
    p[7] = 1; p[15] = 0x91; p[22] = 2;                        /* StreamID, DA, VID 2 */
    p[23] = (uint8_t)(frame >> 8); p[24] = (uint8_t)frame;    /* MaxFrameSize */
    p[26] = 1; p[27] = 0x70;                                  /* interval frames, PCP/rank */
    p[32] = 36;                                               /* JoinIn */
    memcpy(b, p, sizeof(p));
    return sizeof(p);
}

int main(void)
{
    uint8_t pdu[64]; size_t n;

    /* P1a: Listener declaration change arriving in the LeaveAll PDU itself. */
    struct mrp_app *a = msrp_app_create(1, &ctx);
    mrp_set_periodic(a, 0, false);
    n = listener_pdu(pdu, MSRP_LISTENER_DECL_READY, 0);
    CHECK("p1a-ready-accepted", mrp_rx(a, 0, pdu, n) == 0 && listener_inds == 1 && last_decl == 2);
    n = listener_pdu(pdu, MSRP_LISTENER_DECL_ASKING_FAILED, 1);
    CHECK("p1a-leaveall-pdu-accepted", mrp_rx(a, 0, pdu, n) == 0);
    printf("INFO p1a listener_inds=%u last_decl=%d\n", listener_inds, last_decl);
    CHECK("p1a-changed-declaration-indicated", listener_inds == 2 && last_decl == 1);
    n = listener_pdu(pdu, MSRP_LISTENER_DECL_ASKING_FAILED, 0);
    for (int i = 0; i < 5; ++i) { mrp_rx(a, 0, pdu, n); }
    printf("INFO p1a after 5 more JoinIn(AskingFailed): listener_inds=%u last_decl=%d\n", listener_inds, last_decl);
    CHECK("p1a-application-eventually-sees-asking-failed", last_decl == 1);
    mrp_app_destroy(a);

    /* P1b: change arriving after a received LeaveAll in a separate PDU. */
    listener_inds = 0; last_decl = -1;
    a = msrp_app_create(1, &ctx);
    mrp_set_periodic(a, 0, false);
    n = listener_pdu(pdu, MSRP_LISTENER_DECL_READY, 0);
    mrp_rx(a, 0, pdu, n);
    uint8_t la_only[] = {0, 3, 8, 0, 12, 0x20, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 0, 0, 0};
    CHECK("p1b-leaveall-only-accepted", mrp_rx(a, 0, la_only, sizeof(la_only)) == 0);
    n = listener_pdu(pdu, MSRP_LISTENER_DECL_ASKING_FAILED, 0);
    mrp_rx(a, 0, pdu, n);
    printf("INFO p1b listener_inds=%u last_decl=%d\n", listener_inds, last_decl);
    CHECK("p1b-changed-declaration-indicated", listener_inds == 2 && last_decl == 1);
    mrp_app_destroy(a);

    /* P1c: Talker TSpec change after a received LeaveAll. */
    a = msrp_app_create(1, &ctx);
    mrp_set_periodic(a, 0, false);
    n = talker_pdu(pdu, 100, 0);
    CHECK("p1c-talker-accepted", mrp_rx(a, 0, pdu, n) == 0 && talker_inds == 1 && last_frame == 100);
    n = talker_pdu(pdu, 200, 1);
    CHECK("p1c-leaveall-talker-accepted", mrp_rx(a, 0, pdu, n) == 0);
    printf("INFO p1c talker_inds=%u last_frame=%d\n", talker_inds, last_frame);
    CHECK("p1c-changed-tspec-indicated", talker_inds == 2 && last_frame == 200);
    mrp_app_destroy(a);

    /* P1d: same change while IN (control: existing changed-value contract). */
    talker_inds = 0;
    a = msrp_app_create(1, &ctx);
    mrp_set_periodic(a, 0, false);
    n = talker_pdu(pdu, 100, 0); mrp_rx(a, 0, pdu, n);
    n = talker_pdu(pdu, 200, 0); mrp_rx(a, 0, pdu, n);
    printf("INFO p1d talker_inds=%u last_frame=%d\n", talker_inds, last_frame);
    CHECK("p1d-control-in-change-indicated", talker_inds == 2 && last_frame == 200);
    mrp_app_destroy(a);

    /* P2: later-version unknown MSRP message whose vector carries a FourPacked octet,
     * bounded by AttributeListLength, followed by a valid Listener. */
    listener_inds = 0;
    a = msrp_app_create(1, &ctx);
    uint8_t later[] = {1, 9, 1, 0, 7, 0, 1, 7, 36, 64, 0, 0,
                       3, 8, 0, 14, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 36, 128, 0, 0, 0, 0};
    int r = mrp_rx(a, 0, later, sizeof(later));
    printf("INFO p2 rx=%d listener_inds=%u\n", r, listener_inds);
    CHECK("p2-later-unknown-stream-message-skipped-by-list-length", r == 0 && listener_inds == 1);
    mrp_app_destroy(a);

    /* P2b: same with a two-octet trailing extension inside AttributeListLength. */
    listener_inds = 0;
    a = msrp_app_create(1, &ctx);
    uint8_t later2[] = {1, 9, 1, 0, 8, 0, 1, 7, 36, 0, 0, 0xAA, 0xBB,
                        3, 8, 0, 14, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 36, 128, 0, 0, 0, 0};
    r = mrp_rx(a, 0, later2, sizeof(later2));
    printf("INFO p2b rx=%d listener_inds=%u\n", r, listener_inds);
    CHECK("p2b-later-unknown-stream-message-trailing-octets", r == 0 && listener_inds == 1);
    mrp_app_destroy(a);

    /* P2c: control, the author's well-formed unknown stream message. */
    listener_inds = 0;
    a = msrp_app_create(1, &ctx);
    uint8_t later3[] = {1, 9, 1, 0, 6, 0, 1, 7, 0, 0, 0,
                        3, 8, 0, 14, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 36, 128, 0, 0, 0, 0};
    r = mrp_rx(a, 0, later3, sizeof(later3));
    CHECK("p2c-control-well-formed-unknown-skipped", r == 0 && listener_inds == 1);
    mrp_app_destroy(a);

    printf("probe failures: %d\n", fails);
    return fails != 0;
}
