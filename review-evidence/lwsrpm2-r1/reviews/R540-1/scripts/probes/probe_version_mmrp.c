/* SPDX-License-Identifier: Apache-2.0 */
/* Probe: a MAC PDU with a higher ProtocolVersion carries an unrecognised
 * attribute type before a valid MAC message (IEEE 802.1Q-2018 10.8.3.5 c) 1)). */
#include <stdio.h>
#include "shish_lan/mmrp.h"
#include "shish_lan/mrp.h"

static unsigned registered;
static void reg(struct mmrp_ctx *c, uint8_t p, const struct mmrp_mac *mac)
{
    (void)c; (void)p;
    printf("  MAC ..:%02x registered\n", ((const uint8_t *)mac)[5]);
    ++registered;
}

static void run(uint8_t version, uint8_t first_type, uint8_t first_len)
{
    struct mmrp_ctx ctx = {.on_mac_registered = reg};
    struct mrp_app *app = mmrp_app_create(1, &ctx);
    registered = 0;
    const uint8_t pdu[] = {
        version,
        first_type, first_len, 0x00, 0x01, 0x01, 0, 0, 0, 0, 0x07, 1 * 36, 0x00, 0x00,
        2, 6, 0x00, 0x01, 0x01, 0, 0x5e, 0, 0, 0x02, 1 * 36, 0x00, 0x00,
        0x00, 0x00,
    };
    int r = mrp_rx(app, 0, pdu, sizeof(pdu));
    printf("version=%u first_type=%u mrp_rx=%d registrations=%u\n", version, first_type, r, registered);
    mmrp_app_destroy(app);
}

int main(void)
{
    run(0, 2, 6);  /* control: two MAC messages */
    run(1, 2, 6);  /* control: higher version, known types */
    run(1, 9, 6);  /* higher version, unrecognised type 9 first */
    run(0, 9, 6);  /* same version, unrecognised type 9 first (malformed) */
    return 0;
}
