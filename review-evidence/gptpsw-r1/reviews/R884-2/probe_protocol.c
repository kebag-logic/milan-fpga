/* Independent API-level wire stimuli for the published gPTP core. */
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "gptp.h"

static const uint64_t own = 0x001122fffe334455ULL;
static const uint64_t peer = 0x006677fffe8899aaULL;
static unsigned requests, failures;
static struct gptp_port p;
static void be(uint8_t *f, unsigned at, uint64_t v, unsigned n) {
  for (unsigned i=0;i<n;i++) f[at+i]=(uint8_t)(v>>(8*(n-1-i)));
}
static void ts(uint8_t *f, unsigned at, uint64_t ns) {
  be(f,at,ns/1000000000ULL,6); be(f,at+6,ns%1000000000ULL,4);
}
static bool send_frame(void *ctx,unsigned port,const uint8_t *f,unsigned n) {
  (void)ctx;(void)port;(void)n; if ((f[14]&15)==2) requests++; return true;
}
static void rate(void *ctx,unsigned port,int32_t v) {(void)ctx;(void)port;(void)v;}
static void step(void *ctx,unsigned port,int64_t v) {(void)ctx;(void)port;(void)v;}
static void frame(uint8_t *f,unsigned type,unsigned length,uint64_t src,unsigned seq) {
  memset(f,0,160); const uint8_t da[]={1,0x80,0xc2,0,0,0xe}; memcpy(f,da,6);
  be(f,12,0x88f7,2); f[14]=(uint8_t)(0x10|type); f[15]=0x12;
  be(f,16,length,2);be(f,34,src,8);be(f,42,1,2);be(f,44,seq,2);
  f[46]=5;f[47]=0;
}
static void init(unsigned priority) {
  struct gptp_config c={.clock_id=own,.priority1=(uint8_t)priority,.priority2=248,.phc_clk_hz=50000000};
  struct gptp_hal h={NULL,send_frame,rate,step}; requests=0;
  gptp_port_init(&p,0,&c,&h,0);gptp_port_link(&p,true);
}
static void resp(uint64_t source,bool fu,uint64_t t,bool stamp,uint64_t arrival) {
  uint8_t f[160];frame(f,fu?10:3,54,source,p.pd.seq);f[20]=fu?0:2;f[47]=0x7f;
  ts(f,48,t);be(f,58,own,8);be(f,66,1,2);
  if(stamp) gptp_port_ts(&p,false,3,p.pd.seq,arrival,true);
  gptp_port_rx(&p,f,68);
}
static void exchange(uint64_t t) {
  gptp_port_ts(&p,true,2,p.pd.seq,t,true);
  resp(peer,false,t+500,true,t+31000);resp(peer,true,t+30500,false,0);
}
static void ready(unsigned priority) {
  init(priority);exchange(1000000000ULL);gptp_port_tick(&p,1000);exchange(2000000000ULL);
  if(!p.pd.as_capable) { puts("SETUP FAILED"); failures++; }
}
static void announce(void) {
  uint8_t f[160];frame(f,11,76,peer,1);f[61]=100;f[62]=248;f[63]=0x22;
  be(f,64,0x436a,2);f[66]=248;be(f,67,peer,8);f[77]=0xa0;
  be(f,78,8,2);be(f,80,8,2);be(f,82,peer,8);gptp_port_rx(&p,f,90);
}
static void sync_frame(unsigned seq,uint64_t t) {
  uint8_t f[160];frame(f,0,44,peer,seq);f[20]=2;f[46]=0;f[47]=(uint8_t)-3;
  gptp_port_ts(&p,false,0,(uint16_t)seq,t,true);gptp_port_rx(&p,f,58);
}
static void follow(unsigned seq,uint64_t t,bool valid_tlv) {
  uint8_t f[160];frame(f,8,valid_tlv?76:44,peer,seq);f[46]=2;f[47]=(uint8_t)-3;ts(f,48,t);
  if(valid_tlv) {be(f,58,3,2);be(f,60,28,2);f[63]=0x80;f[64]=0xc2;f[67]=1;}
  gptp_port_rx(&p,f,valid_tlv?90:58);
}
static void check(const char *name,bool ok) {printf("%s: %s\n",name,ok?"PASS":"FAIL");failures+=!ok;}
int main(void) {
  for(unsigned priority=248;priority<=255;priority+=7) {
    ready(priority);announce();sync_frame(1,2000000000ULL);follow(1,1999999500ULL,true);
    check("setup completed pair establishes sync",p.pub.sync_ok && p.ctr.sync_used==1);
    for(unsigned i=1;i<=6;i++) {gptp_port_tick(&p,1000+120*i);sync_frame(i+1,2000000000ULL+120000000ULL*i);}
    printf("after 720 ms without Follow_Up: priority=%u role=%u sync_ok=%u used=%u rto_sync=%u\n",priority,p.role,p.pub.sync_ok,p.ctr.sync_used,p.ctr.rto_sync);
    check("loss of completed pairs must expire synchronization",priority==248?p.role!=GPTP_ROLE_SLAVE:!p.pub.sync_ok);
  }
  init(248);
  for(unsigned i=0;i<3;i++) {
    uint64_t t=1000000000ULL*(i+1);exchange(t);resp(peer+1,false,t+600,true,t+32000);
    printf("late second responder exchange %u: multi_run=%u ceased=%u\n",i+1,p.pd.multi_run,p.pd.ceased);
    if(i<2)gptp_port_tick(&p,1000*(i+1));
  }
  check("three completed exchanges with two responders must cease requests",p.pd.ceased);
  ready(248);announce();sync_frame(1,2000000000ULL);follow(1,1999999500ULL,false);
  printf("Follow_Up without required TLV: used=%u sync_ok=%u\n",p.ctr.sync_used,p.pub.sync_ok);
  check("Follow_Up without required information TLV must not discipline PHC",p.ctr.sync_used==0);
  printf("total failed assertions=%u\n",failures);return failures?1:0;
}
