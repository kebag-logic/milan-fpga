/* Probe: does a received MSRP Listener LeaveAll change Talker Advertise state?
 * Build against an exported HEAD snapshot (see run-probe-rla.sh). */
#include <stdio.h>
#include <string.h>
#include "shish_lan/mrp.h"
#include "shish_lan/mrp_pdu.h"
#include "shish_lan/msrp.h"

static void show(void *ctx, const struct mrp_attr_status *st)
{
    printf("  %s type=%u appl=%s reg=%s\n", (const char *)ctx, st->attr_type,
           mrp_appl_state_name(st->appl), mrp_reg_state_name(st->reg));
}

/* One MSRP message: type, FirstValue length, AttributeListLength, one vector. */
static size_t message(uint8_t *b, uint8_t type, uint8_t len, uint8_t la, uint16_t nv,
                      uint8_t event, int subtype)
{
    size_t o = 0, body;
    b[o++] = type; b[o++] = len;
    size_t all = o; o += 2;
    uint16_t vh = mrp_vh_encode(la, nv);
    b[o++] = (uint8_t)(vh >> 8); b[o++] = (uint8_t)vh;
    memset(b + o, 0, len); b[o + 7] = 0x42; o += len;      /* StreamID ...42 */
    if (nv) { b[o++] = mrp_three_pack(event, 0, 0); }
    if (nv && subtype) { b[o++] = 0x80; }                    /* Listener Ready */
    b[o++] = 0; b[o++] = 0;                                  /* list EndMark */
    body = o - all - 2;
    b[all] = (uint8_t)(body >> 8); b[all + 1] = (uint8_t)body;
    return o;
}

static int rx(struct mrp_app *app, uint8_t type, uint8_t len, uint8_t la, uint16_t nv, int sub)
{
    uint8_t pdu[128]; size_t o = 0;
    pdu[o++] = MRP_PROTOCOL_VERSION;
    o += message(pdu + o, type, len, la, nv, MRP_ATTR_EVENT_JOININ, sub);
    pdu[o++] = 0; pdu[o++] = 0;                              /* PDU EndMark */
    return mrp_rx(app, 0, pdu, o);
}

int main(void)
{
    struct msrp_ctx ctx;
    memset(&ctx, 0, sizeof ctx);
    struct mrp_app *app = msrp_app_create(2, &ctx);
    if (!app) { puts("create failed"); return 2; }
    printf("talker JoinIn rc=%d\n", rx(app, MSRP_ATTR_TYPE_TALKER_ADV, 25, MRP_LA_NULL, 1, 0));
    mrp_attr_visit(app, 0, show, "after-talker");
    printf("listener JoinIn (no LeaveAll) rc=%d\n", rx(app, MSRP_ATTR_TYPE_LISTENER, 8, MRP_LA_NULL, 1, 1));
    mrp_attr_visit(app, 0, show, "control");
    printf("listener LeaveAll (no values) rc=%d\n", rx(app, MSRP_ATTR_TYPE_LISTENER, 8, MRP_LA_ALL, 0, 1));
    mrp_attr_visit(app, 0, show, "after-listener-LA");
    msrp_app_destroy(app);
    return 0;
}
