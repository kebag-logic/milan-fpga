/* SPDX-License-Identifier: Apache-2.0 */
/* Probe: stored value sizes stay within the 48-byte attribute store. */
#include <stdio.h>
#include "shish_lan/msrp.h"
int main(void)
{
    printf("talker_adv=%zu talker_failed=%zu domain=%zu listener=9 store=48 parse_buffer=64\n",
           sizeof(struct msrp_talker_adv), sizeof(struct msrp_talker_failed), sizeof(struct msrp_domain));
    return sizeof(struct msrp_talker_failed) > 48;
}
