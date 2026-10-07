/* SPDX-License-Identifier: Apache-2.0 */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "shish_lan/mrp.h"
#include "shish_lan/mrp_pdu.h"
#include "shish_lan/mvrp.h"
#include "shish_lan/mmrp.h"
#include "shish_lan/msrp.h"
#include "ports/timer.h"

static unsigned joins, maps;
static enum mrp_reg_state reg;
static void vlan(struct mvrp_ctx *ctx,uint8_t p,uint16_t v,bool n) {
    (void)ctx;(void)p;(void)n;++joins;printf(" vlan=%u",v);
}
static void listener(struct msrp_ctx *ctx,uint8_t p,const struct msrp_stream_id *id,enum msrp_listener_decl d,bool n) {
    (void)ctx;(void)p;(void)d;(void)n;++joins;
    printf(" unique_id=%u",((unsigned)id->bytes[6]<<8)|id->bytes[7]);
}
static void domain(struct msrp_ctx *ctx,uint8_t p,const struct msrp_domain *d,bool n) {
    (void)ctx;(void)p;(void)n;++joins;printf(" class=%u priority=%u",d->class_id,d->priority);
}
static uint32_t map(const struct mrp_app *a,uint8_t p,uint8_t t,const void *v) {
    (void)a;(void)p;(void)t;(void)v;++maps;return 0;
}
static void snapshot(void *ctx,const struct mrp_attr_status *s) {
    (void)ctx;reg=s->reg;
}
static int version_probe(int variant) {
    struct mvrp_ctx ctx={.on_vlan_registered=vlan};
    struct mrp_app *a=mvrp_app_create(1,&ctx);
    uint8_t known[]={1,1,2,0,1,0,2,0,0,0,0,0};
    uint8_t unknown[]={1,2,1,0,1,7,0,0,0,1,2,0,1,0,2,0,0,0,0,0};
    uint8_t event[]={1,1,2,0,1,0,9,216,0,1,0,2,0,0,0,0,0};
    uint8_t *p=variant==0?known:variant==1?unknown:event;
    size_t n=variant==0?sizeof known:variant==1?sizeof unknown:sizeof event;
    joins=0;printf("future-%s:",variant==0?"known":variant==1?"unknown-type":"unknown-event");
    int rc=mrp_rx(a,0,p,n);int count=mrp_attr_visit(a,0,0,0);
    printf(" rc=%d joins=%u attributes=%d expected_rc=0 expected_joins=1\n",rc,joins,count);
    int failed=rc!=0||joins!=1||count!=1;mvrp_app_destroy(a);return failed;
}
static void service(struct mmrp_ctx *ctx,uint8_t p,uint8_t v) {
    (void)ctx;(void)p;++joins;printf(" service=%u",v);
}
static int mmrp_version_probe(void) {
    struct mmrp_ctx ctx={.on_svc_registered=service};
    struct mrp_app *a=mmrp_app_create(1,&ctx);
    uint8_t p[]={1,3,1,0,1,7,0,0,0,1,1,0,1,1,0,0,0,0,0};
    joins=0;printf("future-mmrp-unknown-type:");int rc=mrp_rx(a,0,p,sizeof p);
    printf(" rc=%d joins=%u expected_rc=0 expected_joins=1\n",rc,joins);
    int failed=rc!=0||joins!=1;mmrp_app_destroy(a);return failed;
}

static int overflow_probe(int is_domain) {
    struct msrp_ctx ctx={.on_listener=listener,.on_domain=domain};
    struct mrp_app *a=msrp_app_create(1,&ctx);
    uint8_t lp[]={0,3,8,0,14,0,2,1,2,3,4,5,6,255,255,0,160,0,0,0,0};
    uint8_t dp[]={0,4,4,0,9,0,2,5,7,0,2,0,0,0,0,0};
    joins=0;printf("overflow-%s:",is_domain?"domain-priority":"listener-unique-id");
    int rc=mrp_rx(a,0,is_domain?dp:lp,is_domain?sizeof dp:sizeof lp);
    int count=mrp_attr_visit(a,0,0,0);
    printf(" rc=%d joins=%u attributes=%d expected_rc=negative expected_joins=0\n",rc,joins,count);
    int failed=rc>=0||joins||count;msrp_app_destroy(a);return failed;
}
static int recovery_probe(void) {
    struct mvrp_ctx ctx={.on_vlan_registered=vlan};
    struct mrp_app *proto=mvrp_app_create(1,&ctx);struct mrp_app_ops ops=*proto->ops;
    mvrp_app_destroy(proto);ops.map_join=map;struct mrp_app *a=mrp_app_create(&ops,1);
    uint8_t p[]={0,1,2,0,1,0,2,0,0,0,0,0};
    joins=maps=0;printf("lv-rejoin:");mrp_rx(a,0,p,sizeof p);
    p[7]=5*36;mrp_rx(a,0,p,sizeof p);mrp_attr_visit(a,0,snapshot,0);
    printf(" before=%s",mrp_reg_state_name(reg));p[7]=36;mrp_rx(a,0,p,sizeof p);mrp_attr_visit(a,0,snapshot,0);
    printf(" after=%s joins=%u map_calls=%u table_expected_joins=1 table_expected_map_calls=1\n",mrp_reg_state_name(reg),joins,maps);
    int failed=joins!=1||maps!=1;mvrp_app_destroy(a);return failed;
}
static int boundary_controls(void) {
    struct msrp_ctx ctx={.on_listener=listener,.on_domain=domain};
    struct mrp_app *a=msrp_app_create(1,&ctx);
    uint8_t lp[]={0,3,8,0,14,0,2,1,2,3,4,5,6,255,254,0,160,0,0,0,0};
    joins=0;printf("legal-listener-range:");int rc=mrp_rx(a,0,lp,sizeof lp);
    printf(" rc=%d joins=%u expected_rc=0 expected_joins=2\n",rc,joins);
    int failed=rc!=0||joins!=2;msrp_app_destroy(a);
    a=msrp_app_create(1,&ctx);lp[6]=1;lp[14]=255;lp[16]=128;
    joins=0;printf("legal-listener-maximum:");rc=mrp_rx(a,0,lp,sizeof lp);
    printf(" rc=%d joins=%u expected_rc=0 expected_joins=1\n",rc,joins);
    failed+=rc!=0||joins!=1;msrp_app_destroy(a);
    a=msrp_app_create(1,&ctx);uint8_t dp[]={0,4,4,0,9,0,2,5,6,0,2,0,0,0,0,0};
    joins=0;printf("legal-domain-range:");rc=mrp_rx(a,0,dp,sizeof dp);
    printf(" rc=%d joins=%u expected_rc=0 expected_joins=2\n",rc,joins);
    failed+=rc!=0||joins!=2;msrp_app_destroy(a);return failed?1:0;
}
static int invalid_then_valid(void) {
    struct msrp_ctx ctx={.on_listener=listener,.on_domain=domain};
    struct mrp_app *a=msrp_app_create(1,&ctx);
    uint8_t p[]={0,4,4,0,9,0,1,5,8,0,2,0,0,0,
                  3,8,0,14,0,1,1,2,3,4,5,6,0,1,0,128,0,0,0,0};
    joins=0;printf("invalid-domain-then-listener:");int rc=mrp_rx(a,0,p,sizeof p);
    printf(" rc=%d joins=%u expected_no_later_indication\n",rc,joins);
    int failed=joins!=0;msrp_app_destroy(a);return failed;
}

int main(int argc,char **argv) {
    if(argc!=2){return 2;}
    if(!strcmp(argv[1],"versions")){int f=version_probe(0);f+=version_probe(1);f+=version_probe(2);f+=mmrp_version_probe();return f?1:0;}
    if(!strcmp(argv[1],"overflow")){int f=overflow_probe(0);f+=overflow_probe(1);return f?1:0;}
    if(!strcmp(argv[1],"controls")){return boundary_controls();}
    if(!strcmp(argv[1],"invalid-then-valid")){return invalid_then_valid();}
    if(!strcmp(argv[1],"rejoin")){return recovery_probe();}
    return 2;
}
