// SPDX-License-Identifier: MIT
#include "acmp.h"
#include "wire.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

static struct acmp a;
static uint64_t clock64;
static bool room = true;
static unsigned send_delay, calls, hook;
static bool valid[16];
static unsigned checks;
static void check(bool ok) { ++checks; assert(ok); }
static void callback(unsigned kind) {
    ++calls;
    if (hook == kind) {
        hook = 0;
        check(!acmp_listener_registered(&a, 0, 0, true));
        check(!acmp_declaring(&a, 0));
    }
}
static bool send_frame(void *c, unsigned i, const uint8_t *f, size_t n) {
    (void)c; (void)i; (void)f; check(n == 70); callback(1);
    if (room) clock64 += send_delay;
    return room;
}
static uint32_t now_ms(void *c) { (void)c; callback(2); return (uint32_t)clock64; }
static void timer(void *c, unsigned i, bool b, uint32_t d) { (void)c; (void)i; (void)b; (void)d; callback(4); }
static void gptp(void *c, unsigned i, uint64_t *g, uint8_t *d) { (void)c; (void)i; *g=1; *d=0; callback(5); }
static uint32_t seed(void *c) { (void)c; callback(6); return 1; }
static void admit(void *c, unsigned i, unsigned s, bool b, uint64_t t) { (void)c; (void)i; (void)s; (void)b; (void)t; callback(7); }
static void publish(void *c, unsigned i, unsigned s, bool b, bool t, uint64_t id, bool m) { (void)c; (void)i; (void)s; (void)b; (void)t; (void)id; (void)m; callback(8); }
static bool locked(void *c, uint64_t *id) { (void)c; *id=0; callback(9); return false; }
static void source(void *c, unsigned s, struct acmp_source_state *out) {
    (void)c; check(s < 16); callback(3); memset(out, 0, sizeof *out);
    out->dest_mac_valid = valid[s];
    out->stream.stream_id = 0x10000u + s;
    out->stream.dest_mac = UINT64_C(0x91e0f0000000) + s;
    out->stream.vlan_id = 2;
}
static void srp(void *c, unsigned s, const struct acmp_stream *v) { (void)c; (void)s; (void)v; callback(10); }
static void notify(void *c, unsigned s) { (void)c; (void)s; callback(11); }
static const struct acmp_ports ports = {0, send_frame, now_ms, timer, gptp, seed, admit, publish};
static const struct acmp_env env = {0, locked, source, srp, notify, notify};
static struct acmp_config cfg;
static void reset(uint32_t interval) {
    memset(&cfg, 0, sizeof cfg); cfg.da_fresh_ms=interval; cfg.entity_id=1;
    cfg.n_sources=16; cfg.n_interfaces=4;
    for (unsigned s=0;s<16;++s) { cfg.source_interface[s]=s%4; valid[s]=true; }
    check(acmp_init(&a, &cfg, &ports, &env));
    room=true; send_delay=0; hook=0;
}
static void command(unsigned s, unsigned i, unsigned msg) {
    uint8_t f[70]={0};
    wire_put_be(f+12, 0x22f0, 2); f[14]=0xfc; f[15]=(uint8_t)msg;
    wire_put_be(f+16, 44, 2); wire_put_be(f+34, 1, 8); wire_put_be(f+50, s, 2);
    acmp_rx(&a, i, f, sizeof f);
}
static uint32_t random32(uint32_t *state) {
    *state ^= *state << 13; *state ^= *state >> 17; *state ^= *state << 5; return *state;
}
int main(void) {
    const uint32_t starts[]={0,1,UINT32_MAX-14999u,UINT32_MAX-1u,UINT32_MAX};
    const unsigned ages[]={0,1,14999,15000,15001};
    for (unsigned t=0;t<5;++t) for (unsigned j=0;j<5;++j) for (unsigned s=0;s<16;++s) {
        reset(15000); clock64=starts[t]; command(s,s%4,0); clock64 += ages[j];
        for (unsigned k=0;k<16;++k) check(acmp_declaring(&a,k)==(k==s && ages[j]<15000));
    }
    reset(15000); clock64=100;
    for (unsigned s=0;s<16;++s) {
        unsigned before=calls; check(acmp_listener_registered(&a,s%4,s,true)); check(calls==before);
        check(acmp_declaring(&a,s)); valid[s]=false; check(!acmp_declaring(&a,s));
        check(acmp_listener_registered(&a,s%4,s,false)); valid[s]=true; check(!acmp_declaring(&a,s));
    }
    for (unsigned s=16;s<=65535;++s) command(s,0,0);
    for (unsigned s=0;s<16;++s) check(!acmp_declaring(&a,s));
    reset(15000); clock64=UINT32_MAX-2u; room=false;
    for (unsigned s=0;s<9;++s) command(s,s%4,0);
    check(a.owed_count==8); check(a.busy_drops==1);
    for (unsigned s=0;s<16;++s) check(!acmp_declaring(&a,s));
    clock64 += 30000; room=true; send_delay=7;
    for (unsigned s=0;s<8;++s) { (void)acmp_poll(&a); check(acmp_declaring(&a,s)); }
    check(!acmp_declaring(&a,8)); clock64 += 15000;
    for (unsigned s=0;s<16;++s) check(!acmp_declaring(&a,s));
    reset(0); command(0,0,0); check(!acmp_declaring(&a,0));
    check(acmp_listener_registered(&a,0,0,true)); check(acmp_declaring(&a,0));
    reset(15000); clock64=100;
    hook=1; command(0,0,0); check(a.reentries==2);
    hook=2; check(acmp_declaring(&a,0)); check(a.reentries==4);
    hook=3; check(acmp_declaring(&a,0)); check(a.reentries==6);
    reset(15000); clock64=UINT32_MAX-1000u;
    uint64_t answered_at[16]={0}; bool answered[16]={0}, listener[16]={0};
    uint32_t rng=0x631124;
    for (unsigned n=0;n<100000;++n) {
        unsigned r=random32(&rng), s=(r>>8)%16, op=r%6;
        if (op==0) { command(s,s%4,0); answered[s]=true; answered_at[s]=clock64; }
        if (op==1) { listener[s]=!listener[s]; check(acmp_listener_registered(&a,s%4,s,listener[s])); }
        if (op==2) valid[s]=!valid[s];
        if (op==3) clock64 += (r>>16)%15002;
        if (op==4) command(s,(s+1)%4,0);
        if (op==5) command(s,s%4,4);
        for (unsigned k=0;k<16;++k) {
            bool fresh=answered[k] && clock64-answered_at[k]<15000;
            check(acmp_declaring(&a,k)==(valid[k] && (fresh || listener[k])));
        }
    }
    printf("PASS %u checks; 100000 model events; 16 sources; 4 interfaces; exact edges, wrap, queue, zero interval, guards\n",checks);
    return 0;
}
