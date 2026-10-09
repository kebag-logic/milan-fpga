/* Reviewer-owned input controls. Compile with the reviewed core and example. */
#include "adp_port.h"
#include <stdio.h>

int main(void)
{
    unsigned failures = 0;
    for (unsigned control = 0; control < 4; ++control) {
        struct example_adp_port p;
        const struct adp_entity entity = {.entity_id = 1, .mac = 0x020000000001ULL};
        example_adp_init(&p, &entity);
        example_adp_link(&p, true);
        adp_set_enable(&p.core, true);
        adp_timer_expired(&p.core);
        if (p.core.state != ADP_STATE_WAITING) return 2;
        unsigned char frame[ADP_FRAME_BYTES];
        adp_build(&p.core, ADP_MSG_ENTITY_DISCOVER, 0, frame);
        size_t len = sizeof frame;
        if (control == 1) frame[15] |= 0x10; /* Unsupported AVTP version. */
        if (control == 2) len = 26;         /* Truncated ADPDU. */
        if (control == 3) frame[17] = 0;    /* Incorrect control_data_length. */
        adp_rx(&p.core, frame, len);
        const int rejected = p.core.state == ADP_STATE_WAITING && p.core.discarded == 1;
        printf("control=%u length=%zu version=%u state=%u discarded=%u rejected=%d\n",
               control, len, (unsigned)(frame[15] >> 4), (unsigned)p.core.state,
               p.core.discarded, rejected);
        if (control == 0 && p.core.state != ADP_STATE_DELAY) return 3;
        if (control != 0 && !rejected) ++failures;
    }
    printf("malformed input controls accepted: %u/3\n", failures);
    return failures != 0;
}
