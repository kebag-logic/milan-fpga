/* SPDX-License-Identifier: Apache-2.0 */
/* Probe: a VLAN PDU with a higher ProtocolVersion carries an unrecognised
 * attribute type before a valid VID message (IEEE 802.1Q-2018 10.8.3.5 c) 1)). */
#include <stdio.h>
#include <string.h>
#include "shish_lan/mvrp.h"
#include "shish_lan/mrp.h"

static unsigned registered;
static void reg(struct mvrp_ctx *c, uint8_t p, uint16_t vid, bool n)
{
    (void)c; (void)p; (void)n;
    printf("  VID %u registered\n", vid);
    ++registered;
}

static int run(uint8_t version, uint8_t first_type)
{
    struct mvrp_ctx ctx = {.on_vlan_registered = reg};
    struct mrp_app *app = mvrp_app_create(1, &ctx);
    registered = 0;
    const uint8_t pdu[] = {
        version,
        first_type, 2, 0x00, 0x01, 0x00, 0x09, 1 * 36, 0x00, 0x00, /* first message, JoinIn x1 */
        1, 2, 0x00, 0x01, 0x00, 0x02, 1 * 36, 0x00, 0x00,        /* VID 2, JoinIn x1 */
        0x00, 0x00,
    };
    int r = mrp_rx(app, 0, pdu, sizeof(pdu));
    printf("version=%u first_type=%u mrp_rx=%d registrations=%u\n", version, first_type, r, registered);
    mvrp_app_destroy(app);
    return r;
}

int main(void)
{
    run(0, 1);  /* control: two known messages */
    run(1, 1);  /* control: higher version, known types */
    run(1, 7);  /* higher version, unknown type 7 first */
    run(0, 7);  /* same version, unknown type 7 first (malformed) */
    return 0;
}
