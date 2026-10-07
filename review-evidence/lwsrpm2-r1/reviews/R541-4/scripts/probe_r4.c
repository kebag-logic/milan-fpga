/* SPDX-License-Identifier: Apache-2.0 */
/* A serialized receive may arrive between Flush and the next global tick. */
#define main previous_fault_main
#include "probe_fault.c"
#undef main

int main(void)
{
    for (unsigned type = 1; type <= 3; ++type) {
        for (unsigned lv = 0; lv <= 1; ++lv) {
            for (unsigned changed = 0; changed <= 1; ++changed) {
                for (unsigned fault = 0; fault <= 3; ++fault) {
                    struct mrp_app *a = create(10000);
                    uint8_t b[128], tx[3][256];
                    unsigned old = type == 3 ? 2 : 100;
                    size_t n = pdu(a, b, type, old, 1, false);
                    CHECK(mrp_rx(a, 0, b, n) == 0);
                    if (lv) {
                        n = pdu(a, b, type, old, 4, true);
                        CHECK(mrp_rx(a, 0, b, n) == 0);
                    }
                    allocation_fail_after(fault);
                    mrp_port_role_change(a, 0, true);
                    allocation_fail_after(0);
                    CHECK(state(a, 0, type).reg == (fault ? MRP_REG_STATE_LV : MRP_REG_STATE_MT));
                    n = pdu(a, b, type, changed ? old + 1 : old, 1, false);
                    int rx = mrp_rx(a, 0, b, n);
                    /* A refusal is acceptable only if documented for retry. */
                    CHECK(rx == 0);
                    ticks(2);
                    for (unsigned tick = 0; tick < 30; ++tick) {
                        for (unsigned port = 0; port < 3; ++port) {
                            CHECK(mrp_transmit(a, port, tx[port], sizeof(tx[port]), accept, NULL) >= 0);
                        }
                        CHECK(mrp_rx(a, 0, b, n) == 0);
                        ticks(1);
                    }
                    printf("INTERLEAVE type=%u initial=%s changed=%u fault=%u rx=%d leaves=%u joins=%u reg=%s\n",
                           type, lv ? "LV" : "IN", changed, fault, rx, leaves, joins,
                           mrp_reg_state_name(state(a, 0, type).reg));
                    CHECK(leaves == 1);
                    CHECK(joins == 2);
                    destroy(a);
                }
            }
        }
    }
    printf("interleave checks=%u failures=%u live=%zu\n", checks, failures, allocation_live());
    return failures != 0;
}
