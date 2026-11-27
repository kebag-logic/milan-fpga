/* Independent checks for IEEE 802.1Q-2018 10.8.2.8 and the type-word boundary. */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "shish_lan/mrp.h"
#include "shish_lan/msrp.h"
#include "shish_lan/mrp_pdu.h"
#include "ports/timer.h"

static unsigned failures, values, leavealls, frames;
static uint8_t saved[1500];
static size_t saved_len;
#define CHECK(x) do { if (!(x)) { printf("FAIL line %u: %s\n", (unsigned)__LINE__, #x); ++failures; } } while (0)
static int capture(void *c, uint8_t p, const uint8_t *b, size_t n)
{ (void)c; (void)p; ++frames; memcpy(saved,b,n); saved_len=n; return 0; }
static void value(void *c,uint8_t t,enum mrp_attr_event e,const void *v)
{ (void)c;(void)t;(void)e;(void)v;++values; }
static void leaveall(void *c,uint8_t t) { (void)c;(void)t;++leavealls; }
static void joined(struct mrp_app *a,uint8_t p,uint8_t t,const void *v,bool n)
{ (void)a;(void)p;(void)t;(void)v;(void)n; }
static void left(struct mrp_app *a,uint8_t p,uint8_t t,const void *v)
{ (void)a;(void)p;(void)t;(void)v; }
static uint8_t attr_len(uint8_t t) { return t ? 1 : 0; }
static int encode(uint8_t t,const void *v,uint8_t *b,size_t n)
{ (void)t;if(n<1)return -1;b[0]=*(const uint8_t *)v;return 1; }
static int decode(uint8_t t,uint32_t o,const uint8_t *b,size_t n,void *v)
{ (void)t;if(n<1)return -1;*(uint8_t *)v=(uint8_t)(b[0]+o);return 1; }
static int compare(uint8_t t,const void *a,const void *b) { (void)t;return memcmp(a,b,1); }

static void empty_leaveall(void)
{
    struct msrp_ctx ctx={0};
    struct mrp_app *app=msrp_app_create(1,&ctx);
    CHECK(app != NULL);
    if(!app)return;
    CHECK(mrp_port_configure(app,0,1,60,4,7,true)==0);
    for(unsigned i=0;i<6;i++)shlan_timer_tick();
    uint8_t pdu[1500];
    CHECK(mrp_transmit(app,0,pdu,sizeof(pdu),capture,NULL)==1);
    size_t at=1;
    CHECK(saved[0]==0);
    for(unsigned type=1;type<=4;type++) {
        unsigned len=app->ops->attr_len((uint8_t)type);
        CHECK(saved[at]==type && saved[at+1]==len);
        CHECK(((unsigned)saved[at+2]*256+saved[at+3])==len+4);
        CHECK(saved[at+4]==0x20 && saved[at+5]==0);
        for(unsigned k=0;k<len;k++)CHECK(saved[at+6+k]==0);
        CHECK(saved[at+6+len]==0 && saved[at+7+len]==0);
        at+=8+len;
    }
    CHECK(at+2==saved_len && saved[at]==0 && saved[at+1]==0);
    values=leavealls=0;
    CHECK(mrpdu_parse(saved,saved_len,app->ops,value,leaveall,NULL)==0);
    CHECK(values==0 && leavealls==4);
    at=1;
    for(unsigned type=1;type<=4;type++) {
        unsigned len=saved[at+1];
        memset(saved+at+6,0xff,len); /* Zero-count FirstValue is ignored. */
        at+=8+len;
    }
    values=leavealls=0;
    CHECK(mrpdu_parse(saved,saved_len,app->ops,value,leaveall,NULL)==0);
    CHECK(values==0 && leavealls==4);
    /* A first vector whose declared FirstValue is truncated is rejected atomically. */
    values=leavealls=0;
    CHECK(mrpdu_parse(saved,7,app->ops,value,leaveall,NULL)<0);
    CHECK(values==0 && leavealls==0);
    msrp_app_destroy(app);
    puts("checked: all four empty MSRP LeaveAll vectors; ignored FirstValue; required FirstValue length");
}

static void type_case(const uint8_t *types, size_t count)
{
    struct mrp_app_ops ops={0};
    ops.join_ind=joined;ops.leave_ind=left;ops.attr_len=attr_len;
    ops.encode_attr=encode;ops.decode_attr=decode;ops.attr_cmp=compare;
    ops.ethertype=MRP_ETHERTYPE_MMRP;
    struct mrp_app *app=mrp_app_create(&ops,1);
    CHECK(app!=NULL);if(!app)return;
    CHECK(mrp_port_configure(app,0,1,60,1000,7,true)==0);
    uint8_t v=9, pdu[1500];
    for(unsigned i=0;i<count;i++)CHECK(mrp_mad_join(app,0,types[i],&v,true)==0);
    shlan_timer_tick();
    CHECK(mrp_transmit(app,0,pdu,sizeof(pdu),capture,NULL)==1);
    size_t at=1;
    for(unsigned i=0;i<count;i++) {
        CHECK(saved[at]==types[i] && saved[at+1]==1);
        CHECK(saved[at+2]==0 && saved[at+3]==1 && saved[at+4]==9);
        CHECK(saved[at+6]==0 && saved[at+7]==0);
        at+=8;
    }
    CHECK(at+2==saved_len);
    mrp_app_destroy(app);
}
static void type_words(void)
{
    const uint8_t edges[]={1,31,32,63,64,95,96,127,128,159,160,191,192,223,224,255};
    const uint8_t sparse[]={1,64,129,224,255};
    type_case(edges,sizeof(edges));
    type_case(sparse,sizeof(sparse));
    puts("checked: eight type-word boundaries and empty words followed by occupied words");
}
int main(void)
{
    empty_leaveall();type_words();
    printf("failures=%u frames=%u\n",failures,frames);
    return failures?1:0;
}
