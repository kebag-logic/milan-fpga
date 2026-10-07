/* SPDX-License-Identifier: Apache-2.0 */
/* Exercise the void topology API through the same propagation allocator. */
#define main fault_matrix_main
#include "probe_fault.c"
#undef main

int main(void)
{
    for (unsigned fail = 0; fail <= 3; ++fail) {
        struct mrp_app *a = create(10000);
        uint8_t b[128], tx[3][256];
        size_t n = pdu(a, b, 1, 100, 1, false);
        CHECK(mrp_rx(a, 0, b, n) == 0);
        allocation_fail_after(fail);
        mrp_port_role_change(a, 0, true);
        printf("flush fail_slot=%u immediate reg=%s leave_indications=%u\n", fail,
               mrp_reg_state_name(state(a, 0, 1).reg), leaves);
        /* Ordinary dispatch polls every port. A peer continues its unchanged Join. */
        for (unsigned i = 0; i < 30; ++i) {
            ticks(1);
            for (uint8_t p = 0; p < 3; ++p) {
                CHECK(mrp_transmit(a, p, tx[p], sizeof(tx[p]), accept, NULL) >= 0);
            }
            CHECK(mrp_rx(a, 0, b, n) == 0);
        }
        printf("flush fail_slot=%u after_dispatch reg=%s leaves=%u joins=%u policies=%u\n", fail,
               mrp_reg_state_name(state(a, 0, 1).reg), leaves, joins, policies);
        CHECK(leaves == 1);
        CHECK(joins == 2);
        destroy(a);
    }
    printf("flush checks=%u failures=%u live=%zu\n", checks, failures, allocation_live());
    return failures != 0;
}
