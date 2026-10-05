// Independent boundary/recovery probe for the ADP owed-frame contract.
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "adp.h"
#include "wire.h"
struct fixture { bool room; bool up; unsigned n; uint8_t type[8]; uint32_t ix[8]; };
static bool send_frame(void *p,unsigned i,const uint8_t *f,size_t n) {
    struct fixture *x=p; (void)i; assert(n==82);
    if (!x->room) return false;
    assert(x->n<8); x->type[x->n]=f[15]; x->ix[x->n++]=wire_be32(f+50); return true;
}
static void start(void *p,unsigned i,uint32_t ms) {(void)p;(void)i;assert(ms<=5000);}
static void stop(void *p,unsigned i) {(void)p;(void)i;}
static void gm(void *p,unsigned i,uint64_t *g,uint8_t *d) {(void)p;(void)i;*g=7;*d=0;}
static bool link(void *p,unsigned i) {(void)i;return ((struct fixture*)p)->up;}
static uint32_t seed(void *p) {(void)p;return 17;}
static const struct adp_entity e={.entity_id=123,.mac=234};
static void scenario(uint32_t initial,unsigned shuts,unsigned flaps) {
    struct fixture x={.room=true,.up=true};
    struct adp_ports ports={&x,send_frame,start,stop,gm,link,seed};
    struct adp a; adp_init(&a,&e,&ports,0,0); adp_set_enable(&a,true);
    // Boundary setup of the running index; all subsequent events use public API.
    a.available_index=initial; adp_timer_expired(&a);
    uint32_t oldest=initial+1u;
    assert(x.n==1 && x.ix[0]==initial);
    x.room=false;
    for(unsigned s=0;s<shuts;s++) {
        adp_set_enable(&a,false); adp_set_enable(&a,true); adp_timer_expired(&a);
        assert(a.departing_owed==(s==0?1u:2u));
        assert(a.departing_index==oldest && a.available_index==0);
        assert(a.departing_coalesced==(s<2?0u:s-1u));
        assert(a.available_owed && adp_poll(&a) && x.n==1);
        if(flaps) {
            adp_link_change(&a,false); assert(!a.available_owed && a.departing_owed>0);
            adp_link_change(&a,true); adp_timer_expired(&a);
            adp_gm_change(&a); assert(a.available_owed);
        }
    }
    unsigned owed=shuts==1?1:2;
    x.room=true;
    for(unsigned k=0;k<owed;k++) {
        assert(adp_poll(&a)); assert(x.n==k+2);
        assert(x.type[k+1]==1 && x.ix[k+1]==(k?0:oldest));
    }
    assert(!adp_poll(&a)); assert(x.n==owed+2);
    assert(x.type[x.n-1]==0 && x.ix[x.n-1]==0);
    assert(a.state==ADP_STATE_WAITING && a.timer==ADP_TIMER_ADVERTISE);
    // Milan Table 5.54: a departure removes discovery once; the repeat is inert.
    bool discovered=true; unsigned departed=0;
    for(unsigned j=1;j<x.n-1;j++) if(x.type[j]==1 && discovered) {discovered=false;departed++;}
    assert(!discovered && departed==1);
    printf("PASS initial=%u shutdowns=%u link_flaps=%u owed=%u coalesced=%u recovery_polls=%u\n",
        initial,shuts,flaps,owed,a.departing_coalesced,owed+1);
}
int main(void) {
    const uint32_t idx[]={0,1,UINT32_MAX-1u,UINT32_MAX};
    const unsigned runs[]={1,2,3,64,100001};
    for(unsigned i=0;i<4;i++) for(unsigned j=0;j<5;j++) for(unsigned f=0;f<2;f++) scenario(idx[i],runs[j],f);
    struct fixture x={.room=false,.up=true}; struct adp_ports p={&x,send_frame,start,stop,gm,link,seed};
    struct adp a; adp_init(&a,&e,&p,0,0);
    for(unsigned s=0;s<2;s++) {adp_set_enable(&a,true);adp_set_enable(&a,false);}
    a.departing_coalesced=UINT32_MAX;
    adp_set_enable(&a,true);adp_set_enable(&a,false);
    assert(a.departing_owed==2 && a.departing_coalesced==0);
    puts("PASS diagnostic wrap is documented modulo 2^32; queue remains two");
    puts("RESULT: PASS (40 recovery scenarios and one diagnostic boundary)");
}
