/* SPDX-License-Identifier: Apache-2.0 */
/* Repeat the interleaving with the unchanged production stream policy. */
#define main previous_r3_main
#include "probe_r3.c"
#undef main
int main(void)
{
    uint8_t b[128];
    for (unsigned type=1; type<=2; ++type) {
        for (unsigned lv=0; lv<2; ++lv) {
            for (int fault=0; fault<=3; ++fault) {
                struct mrp_app *a=bridge();
                size_t n=talker_pdu(b,type,1,1);
                CHECK("initial-registration",mrp_rx(a,0,b,n)==0);
                if (lv) { mrp_port_role_change(a,0,false); }
                log_buf[0]=0;
                probe_fail_at=fault;
                mrp_port_role_change(a,0,true);
                probe_fail_at=0;
                CHECK("receive-before-next-tick",mrp_rx(a,0,b,n)==0);
                for (unsigned i=0; i<32; ++i) {
                    shlan_timer_tick();
                    poll_all(a);
                    CHECK("continued-peer-join",mrp_rx(a,0,b,n)==0);
                }
                char leave[16],join[16];
                snprintf(leave,sizeof leave,"L%u@0",type);
                snprintf(join,sizeof join,"J%u@0",type);
                char *l=strstr(log_buf,leave), *j=strstr(log_buf,join);
                printf("NATIVE type=%u initial=%s fault=%d trace=[%s] reg=%s\n",type,
                    lv?"LV":"IN",fault,log_buf,mrp_reg_state_name(reg_of(a,0,type,1)));
                CHECK("flush-leave-precedes-fresh-join", l && j && l<j);
                mrp_app_destroy(a);
            }
        }
    }
    printf("native interleave failures=%d\n",fails);
    return fails!=0;
}
