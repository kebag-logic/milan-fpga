/* SPDX-License-Identifier: Apache-2.0 */
/* Independent public-interface oracle. No private implementation access. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "shish_lan/msrp.h"
#include "shish_lan/error.h"
#include "ports/timer.h"
#include "fault_alloc.h"
static unsigned checks, cases, count, focus, scenario, mismatches;
static unsigned kinds[32], values[32];
static enum mrp_reg_state regs[3][5];
static enum mrp_appl_state appls[3][5];
#define CHECK(x) do { ++checks; if (!(x)) { fprintf(stderr,"FAIL scenario=%u line=%u: %s\n",scenario,__LINE__,#x); exit(1); } } while (0)
static unsigned val(unsigned type, const void *v) {
    return type == 3 ? ((const unsigned char *)v)[8] : ((const struct msrp_talker_adv *)v)->max_frame_size;
}
static void joined(struct mrp_app *a,uint8_t p,uint8_t t,const void *v,bool n) {
    (void)a;(void)n;
    if (p==0 && (t==focus || focus==0)) { CHECK(count<32); kinds[count]=t; values[count++]=val(t,v); }
}
static void left(struct mrp_app *a,uint8_t p,uint8_t t,const void *v) {
    (void)a;
    if (p==0 && (t==focus || focus==0)) { CHECK(count<32); kinds[count]=10+t; values[count++]=val(t,v); }
}
static void observe(void *ctx,const struct mrp_transition *t) {
    (void)ctx;
    CHECK(t->reg_from==regs[t->port_id][t->attr_type]);
    CHECK(t->appl_from==appls[t->port_id][t->attr_type]);
    regs[t->port_id][t->attr_type]=t->reg_to;
    appls[t->port_id][t->attr_type]=t->appl_to;
}
static size_t wire(uint8_t *b,unsigned type,unsigned value,unsigned event,unsigned la) {
    unsigned n=type==1?25:type==2?34:8;
    unsigned list=2+n+1+(type==3)+2;
    memset(b,0,80); b[1]=type;b[2]=n;b[4]=list;b[5]=la?32:0;b[6]=1;
    b[7]=0x11;b[14]=1;
    if(type==3) { b[16]=value<<6; } else { b[23]=value>>8;b[24]=value; }
    b[7+n]=36*event;
    return list+7;
}
static struct mrp_app *setup(unsigned type) {
    struct msrp_ctx ctx={0}; struct mrp_app *tmp=msrp_app_create(3,&ctx);CHECK(tmp);
    struct mrp_app_ops ops=*tmp->ops;mrp_app_destroy(tmp);
    ops.join_ind=joined;ops.leave_ind=left;ops.ctx=NULL;
    struct mrp_app *a=mrp_app_create(&ops,3);CHECK(a);
    for(unsigned p=0;p<3;p++) { CHECK(mrp_port_configure(a,p,20,60,10000,1,true)==0);mrp_set_periodic(a,p,false);
        for(unsigned t=0;t<5;t++) { regs[p][t]=MRP_REG_STATE_MT;appls[p][t]=MRP_APPL_STATE_VO; }
    }
    focus=type;count=0;mrp_set_observer(a,observe,NULL);
    /* The production Listener policy needs a registered Talker destination. */
    if(type==3) { uint8_t b[80];size_t len=wire(b,1,100,1,0);CHECK(mrp_rx(a,1,b,len)==0); }
    return a;
}
static void finish(struct mrp_app *a) { allocation_fail_after(0);mrp_app_destroy(a);CHECK(allocation_live()==0);cases++; }
static void interleave(void) {
    for(unsigned t=1;t<=3;t++) for(unsigned lv=0;lv<2;lv++)
    for(unsigned changed=0;changed<2;changed++) for(unsigned ev=0;ev<6;ev++)
    for(unsigned f=1;f<=3;f++) for(unsigned la=0;la<2;la++) {
        scenario++;struct mrp_app *a=setup(t);uint8_t b[80];unsigned old=t==3?2:100,next=old+changed;
        size_t len=wire(b,t,old,1,0);CHECK(mrp_rx(a,0,b,len)==0);CHECK(count==1);
        if(lv) {len=wire(b,t,old,4,1);CHECK(mrp_rx(a,0,b,len)==0);CHECK(regs[0][t]==MRP_REG_STATE_LV);}
        count=0;allocation_fail_after(f);mrp_port_role_change(a,0,true);
        CHECK(allocation_failures()==1);CHECK(count==0);CHECK(regs[0][t]==MRP_REG_STATE_LV);
        len=wire(b,t,next,ev,la);allocation_fail_after(f);CHECK(mrp_rx(a,0,b,len)==-SHLAN_ERROR_NO_MEMORY);
        CHECK(allocation_failures()==1);CHECK(count==0);CHECK(regs[0][t]==MRP_REG_STATE_LV);
        allocation_fail_after(0);CHECK(mrp_rx(a,0,b,len)==0);
        unsigned declaring=ev==0||ev==1||ev==3;
        CHECK(count==1+declaring);CHECK(kinds[0]==10+t);CHECK(values[0]==old);
        if(declaring) {CHECK(kinds[1]==t);CHECK(values[1]==next);CHECK(regs[0][t]==MRP_REG_STATE_IN);}
        else {CHECK(regs[0][t]==MRP_REG_STATE_MT);}
        for(unsigned k=0;k<61;k++) shlan_timer_tick();CHECK(count==1+declaring);
        finish(a);
    }
}
static void recovery(void) {
    for(unsigned t=1;t<=3;t++) for(unsigned ev=1;ev<=3;ev+=2) {
        scenario++;struct mrp_app *a=setup(t);uint8_t b[80];unsigned old=t==3?2:100;
        size_t len=wire(b,t,old,1,0);CHECK(mrp_rx(a,0,b,len)==0);
        len=wire(b,t,old,4,1);CHECK(mrp_rx(a,0,b,len)==0);CHECK(regs[0][t]==MRP_REG_STATE_LV);
        len=wire(b,t,old,ev,0);CHECK(mrp_rx(a,0,b,len)==0);CHECK(regs[0][t]==MRP_REG_STATE_IN);
        for(unsigned k=0;k<61;k++) shlan_timer_tick();CHECK(count==1);finish(a);
    }
}
static void deadline(void) {
    for(unsigned t=1;t<=3;t++) for(unsigned f=1;f<=3;f++) for(unsigned repeats=0;repeats<3;repeats++) {
        scenario++;struct mrp_app *a=setup(t);uint8_t b[80];unsigned old=t==3?2:100;
        size_t len=wire(b,t,old,1,0);CHECK(mrp_rx(a,0,b,len)==0);count=0;
        allocation_fail_after(f);mrp_port_role_change(a,0,true);CHECK(allocation_failures()==1);CHECK(count==0);
        for(unsigned k=0;k<repeats;k++) {allocation_fail_after(f);shlan_timer_tick();CHECK(allocation_failures()==1);CHECK(count==0);}
        allocation_fail_after(0);shlan_timer_tick();CHECK(count==1);CHECK(kinds[0]==10+t);CHECK(values[0]==old);
        finish(a);
    }
}
static void cross_port(void) {
    for(unsigned t=1;t<=3;t++) for(unsigned f=0;f<=3;f++)
    for(unsigned lv=0;lv<2;lv++) for(unsigned by_receive=0;by_receive<2;by_receive++) {
        scenario++;struct mrp_app *a=setup(t);uint8_t b[80];
        unsigned old=t==3?2:100,other=t==3?1:200,next=t==3?3:300;
        /* Listener mapping to port 0 requires a Talker registered there. */
        if(t==3) {size_t n=wire(b,1,100,1,0);CHECK(mrp_rx(a,0,b,n)==0);}
        size_t len=wire(b,t,old,1,0);CHECK(mrp_rx(a,0,b,len)==0);
        if(lv) {len=wire(b,t,old,4,1);CHECK(mrp_rx(a,0,b,len)==0);}
        count=0;
        allocation_fail_after(f);mrp_port_role_change(a,0,true);CHECK(allocation_failures()==(f?1:0));CHECK(count==(f?0:1));
        /* Flush also withdraws the Listener-routing Talker. Restore that
         * distinct type before receiving the remote Listener update. */
        allocation_fail_after(0);
        if(t==3) {size_t n=wire(b,1,100,1,0);CHECK(mrp_rx(a,0,b,n)==0);}
        len=wire(b,t,other,1,0);CHECK(mrp_rx(a,1,b,len)==0);
        CHECK(count==(f?0:1));
        if(by_receive) {len=wire(b,t,next,1,0);CHECK(mrp_rx(a,0,b,len)==0);}
        else {shlan_timer_tick();}
        CHECK(count==1+by_receive);CHECK(kinds[0]==10+t);
        printf("cross-port type=%u fault=%u initial=%s recovery=%s expected=%u withdrawal=%u\n",t,f,lv?"LV":"IN",by_receive?"receive":"tick",old,values[0]);
        if(values[0]!=old) {mismatches++;}
        if(by_receive) {CHECK(values[1]==next);}
        finish(a);
    }
}
static int accepted(void *ctx,uint8_t p,const uint8_t *b,size_t n) {
    (void)ctx;(void)p;(void)b;(void)n;return 0;
}
static void reject_second(void *ctx,const struct mrp_attr_status *s) {
    (void)ctx;CHECK(((const uint8_t *)s->attr_val)[7]!=2);
}
static void edges(void) {
    for(unsigned old=1;old<=2;old++) for(unsigned fault=0;fault<=9;fault++) {
        scenario++;struct mrp_app *a=setup(old);focus=0;uint8_t b[80],tx[256];unsigned next=3-old;
        size_t len=wire(b,old,100,1,0);CHECK(mrp_rx(a,0,b,len)==0);
        len=wire(b,old,100,4,1);CHECK(mrp_rx(a,0,b,len)==0);CHECK(regs[0][old]==MRP_REG_STATE_LV);count=0;
        len=wire(b,next,200,1,0);allocation_fail_after(fault);int rc=mrp_rx(a,0,b,len);
        CHECK(allocation_failures()==(fault?1:0));CHECK(rc==(fault>0&&fault<=7?-SHLAN_ERROR_NO_MEMORY:0));
        CHECK(count==(fault>0&&fault<=4?0:fault>=5&&fault<=7?1:2));
        allocation_fail_after(0);CHECK(mrp_rx(a,0,b,len)==0);
        CHECK(count==2);CHECK(kinds[0]==10+old);CHECK(values[0]==100);CHECK(kinds[1]==next);CHECK(values[1]==200);
        CHECK(regs[0][old]==MRP_REG_STATE_MT);CHECK(regs[0][next]==MRP_REG_STATE_IN);
        for(unsigned p=1;p<3;p++) CHECK(mrp_transmit(a,p,tx,sizeof(tx),accepted,NULL)>=0);
        finish(a);
    }
    for(unsigned fault=1;fault<=4;fault++) {
        scenario++;struct mrp_app *a=setup(1);uint8_t b[160],second[80];
        /* This check uses two identities of one type; the continuity oracle
         * above deliberately tracks one identity per type. */
        mrp_set_observer(a,NULL,NULL);
        size_t n=wire(b,1,100,1,0),m=wire(second,1,100,1,0);second[14]=2;
        memcpy(b+n-2,second+1,m-1);n+=m-3;
        allocation_fail_after(fault);CHECK(mrp_rx(a,0,b,n)==-SHLAN_ERROR_NO_MEMORY);
        CHECK(allocation_failures()==1);CHECK(count==0);
        for(unsigned p=0;p<3;p++) CHECK(mrp_attr_visit(a,p,reject_second,NULL)>=0);
        allocation_fail_after(0);CHECK(mrp_rx(a,0,b,n)==0);CHECK(count==2);finish(a);
    }
}
int main(int argc,char **argv) {
    if(argc>1 && strcmp(argv[1],"cross-port")==0) {cross_port();}
    else {interleave();recovery();deadline();edges();}
    printf("%s independent production-policy probe: %u cases, %u checks, %u value mismatches\n",mismatches?"FAIL":"PASS",cases,checks,mismatches);return mismatches?1:0;
}
