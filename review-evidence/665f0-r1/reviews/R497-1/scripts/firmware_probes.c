#include <stdio.h>
#include <string.h>
#include "ctrl_app.h"
#include "mbx_model.h"
#include "mbx_hal.h"
#include "wire.h"
static struct mbx_model m;
static struct ctrl_app app;
static _Alignas(max_align_t) unsigned char arena[2048];
static const struct ctrl_pool_class classes[]={{32,8}};
static const struct adp_entity e={.entity_id=0x1122334455667788ull,.entity_model_id=0x123456789abcdef0ull,.mac=0x001122334455ull,.entity_capabilities=0xc588};
static void boot(void){
 mbx_model_reset(&m); mbx_model_bind(&m,NULL,NULL); mbx_model_set_link(&m,0,true);
 const struct ctrl_app_config cfg={&e,0,arena,sizeof arena,classes,1,NULL,NULL};
 if(!ctrl_app_start(&app,&cfg)){puts("SETUP FAILED");return;}
 (void)ctrl_loop_service(&app.loop);
}
static void expiry(void){mbx_model_advance_ms(&m,m.timers[0].deadline_ms-m.now_ms);(void)ctrl_loop_service(&app.loop);}
static unsigned received;
static void rx(void *ctx,const struct mbx_frame *f){(void)ctx;(void)f;received++;}
int main(void){
 boot();expiry();
 adp_mbx_set_enable(&app.adp,false);
 const struct mbx_model_tx *dep=mbx_model_tx_frame(&m,m.tx_sent-1);
 printf("DEPARTING message_type=%u wire_available_index=%u internal_available_index=%u\n",dep->bytes[15],wire_be32(dep->bytes+50),app.adp.ifs[0].adp.available_index);
 unsigned bad=(wire_be32(dep->bytes+50)!=0);
 boot(); mbx_model_tx_pause(&m,true);
 unsigned char frame[82];adp_build(&app.adp.ifs[0].adp,ADP_MSG_ENTITY_AVAILABLE,0,frame);
 unsigned fills=0;while(mbx_tx_send(MBX_CH_ADP,0,frame,sizeof frame)==MBX_STATUS_OK)fills++;
 expiry();unsigned work=ctrl_loop_service(&app.loop);
 printf("TX-WAIT filled=%u work=%u pending=%u timer_armed=%u irq=%u tick_ctl=%u\n",fills,work,app.adp.ifs[0].adp.pending,m.timers[0].armed,mbx_model_irq(&m),m.tick_ctl);
 mbx_model_tx_pause(&m,false); mbx_model_advance_ms(&m,100);
 printf("TX-RECOVERED free_words=%u pending=%u irq=%u timer_armed=%u (wait has no wake source)\n",MBX_CH_ADP_TX_WORDS-(unsigned)(uint16_t)(m.ch[0].tx_head-m.ch[0].tx_tail),app.adp.ifs[0].adp.pending,mbx_model_irq(&m),m.timers[0].armed);
 bad+=(work==0 && app.adp.ifs[0].adp.pending!=0 && !mbx_model_irq(&m) && !m.timers[0].armed);
 (void)ctrl_loop_service(&app.loop);printf("EXPLICIT REPOLL pending=%u timer_armed=%u\n",app.adp.ifs[0].adp.pending,m.timers[0].armed);
 // Unmodified F0 loop and legal burst, last record cannot reach its callback in two passes.
 static struct ctrl_loop loop;mbx_model_reset(&m);ctrl_loop_init(&loop);ctrl_loop_bind_rx(&loop,MBX_CH_ADP,rx,NULL);ctrl_loop_open(&loop,e.entity_id);
 memset(frame,0,sizeof frame);wire_put_be(frame,0x91e0f0010000ull,6);wire_put_be(frame+12,0x22f0,2);frame[14]=0xfa;frame[15]=2;wire_put_be(frame+16,56,2);
 for(unsigned k=0;k<8;k++)if(!mbx_model_rx(&m,frame,sizeof frame,0)){puts("SETUP FAILED burst");return 2;}
 for(unsigned pass=1;pass<=4;pass++){unsigned long long before=m.reads+m.writes;(void)ctrl_loop_service(&loop);printf("QUEUED RX pass=%u delivered=%u mailbox_accesses=%llu\n",pass,received,(unsigned long long)(m.reads+m.writes)-before);if(pass==2)bad+=(received<8);}
 printf("CONFIRMED_DEFECT_PROBES=%u\n",bad);return bad?1:0;
}
