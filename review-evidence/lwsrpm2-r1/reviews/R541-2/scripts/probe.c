/* SPDX-License-Identifier: Apache-2.0 */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include "shish_lan/mrp.h"
#include "shish_lan/mrp_pdu.h"
#include "shish_lan/msrp.h"
#include "shish_lan/mvrp.h"
#include "shish_lan/mmrp.h"
#include "ports/timer.h"
static int fail_next, calls, policy_ready, policy_saw_ready;
void *shlan_malloc(size_t n) { return malloc(n); }
void *shlan_calloc(size_t n, size_t s) {
    if (fail_next) { fail_next = 0; return NULL; }
    return calloc(n, s);
}
void shlan_free(void *p) { free(p); }
int shlan_printf(const char *f, ...) { (void)f; return 0; }
static void join(struct mrp_app *a,uint8_t p,uint8_t t,const void *v,bool n) {
    (void)a; (void)p; (void)t; (void)v; (void)n; calls++; policy_ready = 1;
}
static void leave(struct mrp_app *a,uint8_t p,uint8_t t,const void *v) {
    (void)a; (void)p; (void)t; (void)v;
}
static uint32_t policy(const struct mrp_app *a,uint8_t p,uint8_t t,const void *v) {
    (void)a; (void)t; (void)v; policy_saw_ready = policy_ready;
    return p == 0 && policy_ready ? 2u : 0u;
}
static struct mrp_app *app(unsigned kind, unsigned ports, int custom_policy) {
    struct mvrp_ctx v = {0}; struct mmrp_ctx m = {0}; struct msrp_ctx s = {0};
    struct mrp_app *base = kind == 0 ? mvrp_app_create(1,&v) :
        kind == 1 ? mmrp_app_create(1,&m) : msrp_app_create(1,&s);
    assert(base);
    struct mrp_app_ops ops = *base->ops;
    ops.join_ind = join; ops.leave_ind = leave; ops.ctx = NULL;
    if (custom_policy) { ops.map_join = policy; ops.map_leave = NULL; }
    mrp_app_destroy(base);
    struct mrp_app *a = mrp_app_create(&ops,(uint8_t)ports);
    assert(a); return a;
}
static int send_ok(void *c,uint8_t p,const uint8_t *b,size_t n) {
    (void)c; (void)p; (void)b; (void)n; return 0;
}
static int frame_value;
static void visit(void *c,const struct mrp_attr_status *s) {
    (void)c;
    if (s->attr_type == 1) { frame_value = ((const struct msrp_talker_adv *)s->attr_val)->max_frame_size; }
}
static int value(struct mrp_app *a,uint8_t p) {
    frame_value = -1; mrp_attr_visit(a,p,visit,NULL); return frame_value;
}
static int callback_order(void) {
    struct mrp_app *a = app(0,2,1);
    uint8_t wire[] = {0,1,2,0,1,0,2,0,0,0,0,0};
    int rc = mrp_rx(a,0,wire,sizeof(wire));
    int target = mrp_attr_visit(a,1,NULL,NULL);
    printf("callback-order: receive=%d indications=%d policy_saw_indication=%d target_instances=%d expected=1\n",rc,calls,policy_saw_ready,target);
    mrp_app_destroy(a); return !(rc == 0 && target == 1 && policy_saw_ready);
}
static int allocation_retry(int inject) {
    struct mrp_app *a = app(2,2,0);
    uint8_t wire[37] = {0,1,25,0,30,0,1}; wire[14]=1; wire[24]=100;
    assert(mrp_rx(a,0,wire,sizeof(wire)) == 0);
    assert(value(a,0) == 100 && value(a,1) == 100);
    wire[24]=200; wire[32]=36; /* Same identity, updated JoinIn. */
    fail_next=inject;
    int first = mrp_rx(a,0,wire,sizeof(wire));
    int after = value(a,1);
    int retry = mrp_rx(a,0,wire,sizeof(wire));
    uint8_t out[256];
    for (unsigned n=0;n<100;++n) { shlan_timer_tick(); mrp_transmit(a,1,out,sizeof(out),send_ok,NULL); }
    int source_value=value(a,0), target=value(a,1);
    printf("allocation-retry: first=%d target_after_failure=%d retry=%d source=%d target=%d expected=200 indications=%d\n",first,after,retry,source_value,target,calls);
    mrp_app_destroy(a); return !((inject ? first < 0 : first == 0) && retry == 0 && source_value == 200 && target == 200);
}
static unsigned attrs, las;
static void attr(void *c,uint8_t t,enum mrp_attr_event e,const void *v) { (void)c;(void)t;(void)e;(void)v;attrs++; }
static void la(void *c,uint8_t t) { (void)c;(void)t;las++; }
static int atomic(void) {
    struct mrp_app *a=app(2,1,0);
    uint8_t pdu[] = {0,3,8,0,14,0x20,1,1,2,3,4,5,6,0,1,0,128,0,0,
        4,4,0,9,0,2,254,7,0,2,0,0,0,0,0};
    int r=mrpdu_parse(pdu,sizeof(pdu),a->ops,attr,la,NULL);
    printf("atomic-invalid-final-domain: rc=%d attributes=%u leavealls=%u expected=0,0\n",r,attrs,las);
    mrp_app_destroy(a); return !(r<0 && attrs==0 && las==0);
}
static size_t message(uint8_t *b,int stream,uint8_t type,uint8_t alen,
                      const uint8_t *fv,unsigned count,unsigned event) {
    unsigned h=stream?4:2;
    unsigned sub=stream&&type==3?(count+3)/4:0;
    unsigned list=2+alen+(count+2)/3+sub+2;
    b[0]=type;b[1]=alen;
    if (stream) { b[2]=(uint8_t)(list>>8);b[3]=(uint8_t)list; }
    b[h]=(uint8_t)(count>>8);b[h+1]=(uint8_t)count;
    memcpy(b+h+2,fv,alen);
    memset(b+h+2+alen,event,(count+2)/3);
    if (sub) { memset(b+h+2+alen+(count+2)/3,170,sub); }
    b[h+list-2]=0;b[h+list-1]=0;
    return h+list;
}
static int extensions(void) {
    int errors=0;
    for (unsigned k=0;k<3;++k) {
        uint8_t b[128]={1},ext[]={0,0,255},fv[8]={0};
        unsigned type=k==0?1:k==1?2:4,alen=k==0?2:k==1?6:4;
        if (k==0) { fv[1]=2; }
        if (k==1) { fv[5]=1; }
        if (k==2) { fv[0]=5;fv[1]=2;fv[3]=2; }
        size_t n=1;
        n+=message(b+n,k==2,9,3,ext,4,255);
        n+=message(b+n,k==2,(uint8_t)type,(uint8_t)alen,fv,2,0);
        b[n++]=0;b[n++]=0;
        struct mrp_app *a=app(k,1,0); calls=0;
        int r=mrp_rx(a,0,b,n),instances=mrp_attr_visit(a,0,NULL,NULL);
        printf("extension-application-%u: rc=%d indications=%d following_instances=%d expected=2\n",k,r,calls,instances);
        errors+=!(r==0&&calls==2&&instances==2); mrp_app_destroy(a);
        a=app(k,1,0);calls=0;b[0]=0;
        r=mrp_rx(a,0,b,n); errors+=!(r<0&&calls==0);
        printf("current-version-application-%u: rc=%d indications=%d expected=0\n",k,r,calls);
        mrp_app_destroy(a);
    }
    return errors!=0;
}
static int overflow(void) {
    int errors=0;
    for (unsigned type=1;type<=3;++type) {
        unsigned alen=type==1?25:type==2?34:8;
        uint8_t fv[34]={0},b[128]={0}; fv[6]=255;fv[7]=255;
        size_t n=1+message(b+1,1,(uint8_t)type,(uint8_t)alen,fv,2,0);
        b[n++]=0;b[n++]=0;
        struct mrp_app *a=app(2,1,0); calls=0;
        int r=mrp_rx(a,0,b,n);
        printf("stream-overflow-type-%u: rc=%d indications=%d expected=0\n",type,r,calls);
        errors+=!(r<0&&calls==0&&mrp_attr_visit(a,0,NULL,NULL)==0);
        mrp_app_destroy(a);
        fv[7]=254;n=1+message(b+1,1,(uint8_t)type,(uint8_t)alen,fv,2,0);b[n++]=0;b[n++]=0;
        a=app(2,1,0);calls=0;r=mrp_rx(a,0,b,n);
        printf("stream-maximum-control-type-%u: rc=%d indications=%d expected=2\n",type,r,calls);
        errors+=!(r==0&&calls==2); mrp_app_destroy(a);
    }
    return errors!=0;
}
static enum mrp_appl_state last_appl;
static enum mrp_reg_state last_reg;
static void state_visit(void *c,const struct mrp_attr_status *s) {
    (void)c;if (s->attr_type==1) { last_appl=s->appl;last_reg=s->reg; }
}
static int send_no(void *c,uint8_t p,const uint8_t *b,size_t n) {
    (void)c;(void)p;(void)b;(void)n;return -1;
}
static int retention(void) {
    struct mrp_app *a=app(2,3,0);
    uint8_t out[2][256],saved[2][256];
    struct msrp_domain d={6,3,2};
    for (uint8_t p=1;p<3;++p) {
        memset(out[p-1],0,256);
        assert(mrp_mad_join(a,p,4,&d,true)==0);
        assert(mrp_transmit(a,p,out[p-1],256,send_no,NULL)<0);
        memcpy(saved[p-1],out[p-1],256);
    }
    uint8_t wire[37]={0,1,25,0,30,0,1};wire[14]=1;wire[24]=100;
    assert(mrp_rx(a,0,wire,sizeof(wire))==0);
    assert(value(a,1)==-1 && value(a,2)==-1);
    assert(mrp_transmit(a,1,out[0],256,send_ok,NULL)==1);
    assert(value(a,1)==100);
    wire[24]=200;wire[32]=36;assert(mrp_rx(a,0,wire,sizeof(wire))==0);
    mrp_port_role_change(a,0,true);assert(mrp_reclaim(a,0)==1);
    memset(wire,255,sizeof(wire));
    assert(mrp_transmit(a,2,out[1],256,send_ok,NULL)==1);
    int errors=0;
    for (uint8_t p=1;p<3;++p) {
        mrp_attr_visit(a,p,state_visit,NULL);
        int v=value(a,p),same=!memcmp(saved[p-1],out[p-1],256);
        printf("retention-port-%u: value=%d applicant=%d exact_bytes=%d expected=200,0,1\n",p,v,last_appl,same);
        errors+=!(v==200&&last_appl==MRP_APPL_STATE_VO&&same);
    }
    mrp_app_destroy(a);return errors!=0;
}
static int recovery(void) {
    int errors=0;
    for (unsigned event=1;event<=3;event+=2) {
        struct mrp_app *a=app(0,1,0);calls=0;
        uint8_t b[]={0,1,2,0,1,0,2,0,0,0,0,0};
        assert(mrp_rx(a,0,b,sizeof(b))==0);b[7]=180;
        assert(mrp_rx(a,0,b,sizeof(b))==0);
        for (unsigned n=0;n<30;++n) { shlan_timer_tick(); }
        b[7]=(uint8_t)(36*event);assert(mrp_rx(a,0,b,sizeof(b))==0);
        for (unsigned n=0;n<70;++n) { shlan_timer_tick(); }
        mrp_attr_visit(a,0,state_visit,NULL);
        printf("recovery-event-%u: indications=%d registrar=%d expected=1,0\n",event,calls,last_reg);
        errors+=!(calls==1&&last_reg==MRP_REG_STATE_IN);mrp_app_destroy(a);
    }
    return errors!=0;
}
int main(int argc,char **argv) {
    if (argc!=2) { return 2; }
    if (!strcmp(argv[1],"order")) { return callback_order(); }
    if (!strcmp(argv[1],"allocation")) { return allocation_retry(1); }
    if (!strcmp(argv[1],"allocation-control")) { return allocation_retry(0); }
    if (!strcmp(argv[1],"atomic")) { return atomic(); }
    if (!strcmp(argv[1],"extensions")) { return extensions(); }
    if (!strcmp(argv[1],"overflow")) { return overflow(); }
    if (!strcmp(argv[1],"retention")) { return retention(); }
    if (!strcmp(argv[1],"recovery")) { return recovery(); }
    return 2;
}
