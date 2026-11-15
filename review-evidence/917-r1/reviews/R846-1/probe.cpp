#include <cstdio>
#include <memory>
#include "../../common/verilator_harness.hpp"
#ifdef REVIEW_MODEL
#include "model_bench.hpp"
#else
#include "Vtb_mbx_top.h"
#include "bench.hpp"
#include "verilated.h"
#endif
#include "suite_probe.hpp"

template<class B> void probes(B& b, milan::tb::Checker& ck) {
    using namespace mbx_tb;
    Suite<B> s(b,ck);
    const unsigned c=MBX_CH_AECP, burst=MBX_CH_AECP_RATE_BURST, refill=MBX_CH_AECP_RATE_REFILL_MS;
    auto send=[&](const std::vector<std::uint8_t>& f){b.send_frame(f,0); b.drain_rx();};
    auto count=[&](unsigned reg){return s.rd(ch_reg(c,reg));};
    auto burn=[&](){s.restart(); s.open(1u<<c); for(unsigned i=0;i<burst;i++){send(s.aecp_read(i)); s.release(c,s.peek(c));}};
    burn();
    auto held=s.aecp_read(100), later=s.aecp_read(101);
    unsigned h=s.rx_head(c);
    send(held);
    ck.dec("P0 held head unpublished",s.rx_head(c),h);
    auto runt=held; runt.resize(13); send(runt);
    auto truncated=held; truncated.resize(21); send(truncated);
    auto foreign=held; put_be(foreign,18,kForeignEid,8); send(foreign);
    ck.dec("P0 malformed and identity-filtered followers are not rate drops",count(MBX_CH_REG_RATE_DROP),0);
    ck.dec("P0 malformed and identity-filtered followers are not size drops",count(MBX_CH_REG_RX_DROP),0);
    send(later);
    ck.dec("P0 valid follower counted once",count(MBX_CH_REG_RATE_DROP),1);
    s.wr(MBX_REG_FILTER_EN,0); send(later);
    ck.dec("P0 disabled follower uncounted",count(MBX_CH_REG_RATE_DROP),1);
    b.ms(refill);
    ck.dec("P0 accepted held frame commits after disable",s.rx_pass(c),burst+1);
    ck.that("P0 held payload survives all followers",s.same_bytes(s.peek(c).bytes,held));
    s.release(c,s.peek(c)); b.ms(2*refill);
    ck.dec("P0 disabled channel commits held record only once",s.rx_pass(c),burst+1);

    burn();
    unsigned total=0; bool intact=true, bounded=true; unsigned wrap16=0, wrapring=0;
    for(unsigned i=0;i<4000;i++) {
        auto f=s.aecp_read(static_cast<std::uint16_t>(i));
        f.resize(64+i%5,static_cast<std::uint8_t>(i));
        unsigned old=s.rx_head(c); send(f);
        bounded=bounded && s.rx_head(c)==old;
        b.ms(refill);
        unsigned now=s.rx_head(c);
        wrap16 += now<old;
        wrapring += (now % MBX_CH_AECP_RX_WORDS)<(old % MBX_CH_AECP_RX_WORDS);
        auto r=s.peek(c); intact=intact && s.same_bytes(r.bytes,f);
        s.release(c,r); total++;
    }
    ck.that("P1 every empty-bucket record waits for refill",bounded);
    ck.that("P1 every held record survives physical and 16-bit wrap",intact);
    ck.that("P1 exercised 16-bit counter wrap",wrap16>0);
    ck.that("P1 exercised physical ring wrap",wrapring>0);
    ck.dec("P1 exactly 4000 releases committed",s.rx_pass(c),burst+total);
    ck.dec("P1 empty ring at end",s.rx_head(c),s.rx_tail_[c]);
    ck.dec("P1 no space drops",count(MBX_CH_REG_RX_DROP),0);
    ck.dec("P1 no rate drops",count(MBX_CH_REG_RATE_DROP),0);

    s.restart(); s.open(1u<<c);
    unsigned words=2+(held.size()+3)/4, n=MBX_CH_AECP_RX_WORDS/words;
    std::vector<std::vector<std::uint8_t>> queued;
    for(unsigned i=0;i<n;i++) {
        auto f=s.aecp_read(static_cast<std::uint16_t>(200+i));
        send(f); queued.push_back(f);
        if(i>=burst && i+1<n) b.ms(refill);
    }
    ck.dec("P2 last fitting record remains held",s.rx_pass(c),n-1);
    send(later);
    ck.dec("P2 held storage counts against full ring",count(MBX_CH_REG_RX_DROP),1);
    ck.dec("P2 space refusal precedes rate refusal",count(MBX_CH_REG_RATE_DROP),0);
    b.ms(refill); intact=true;
    for(const auto& f:queued){auto r=s.peek(c); intact=intact&&s.same_bytes(r.bytes,f);s.release(c,r);}
    ck.that("P2 all full-ring records intact including held last",intact);

#ifndef REVIEW_MODEL
    burn(); send(held);
    b.send_bytes(std::vector<std::uint8_t>(later.begin(),later.begin()+40),0,false);
    b.drain_rx(); b.ms(refill);
    ck.dec("P3 refill commits older record during follower receive",s.rx_pass(c),burst+1);
    b.send_bytes(std::vector<std::uint8_t>(later.begin()+40,later.end()),0,true);
    b.drain_rx();
    ck.dec("P3 follower now waits for next token",s.rx_pass(c),burst+1);
    ck.that("P3 older record survives mid-frame release",s.same_bytes(s.peek(c).bytes,held));
    s.release(c,s.peek(c)); b.ms(refill);
    ck.dec("P3 next refill commits follower",s.rx_pass(c),burst+2);
    ck.that("P3 follower payload intact",s.same_bytes(s.peek(c).bytes,later));
    ck.dec("P3 no token beside held record",b.hold_with_token,0);
#endif
}
int main(int argc,char**argv){
    milan::tb::Checker ck{"independent held-record boundaries"};
#ifdef REVIEW_MODEL
    (void)argc;(void)argv;
    auto model=std::make_unique<mbx_model>(); mbx_tb::ModelBench b(model.get());
#else
    Verilated::commandArgs(argc,argv);
    const milan::tb::Model<Vtb_mbx_top> model;
    mbx_tb::Bench b(model.get(),argc>1 && argv[1][0]=='1'?1u:0u);
#endif
    probes(b,ck); return ck.report();
}
