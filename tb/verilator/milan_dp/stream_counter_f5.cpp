// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reuse the firmware's real mailbox fixture and generated descriptor image.
// Appended to test_aecp.cpp by stream_counter_f5.py.
#include <map>
#include <tuple>

TEST_F(Mailbox, StreamCounterWindows)
{
    const char* omitted=std::getenv("COUNTERS_OMIT_CHECK");
    const bool cadence=!omitted || std::strcmp(omitted,"CADENCE")!=0;
    const bool rate=!omitted || std::strcmp(omitted,"RATE")!=0;
    receive(36,{},CTLR);receive(36,{},CTLR+1);
    std::vector<std::pair<unsigned,unsigned>> streams;
    for(auto&d:descriptors)if(d.type==5 || d.type==6)streams.emplace_back(d.type,d.index);
    ASSERT_FALSE(streams.empty());
    using Key=std::tuple<unsigned,unsigned,uint64_t>;
    std::map<Key,std::vector<uint32_t>> departures;
    uint32_t seen=fabric.tx_sent;
    const uint32_t origin=fabric.now_ms;
    ON_CALL(mock,Counters).WillByDefault([&](unsigned,uint16_t,uint16_t,aecp_counters*v){
        v->valid=0xf3f;for(unsigned n=0;n<32;++n)v->value[n]=fabric.now_ms;return true;
    });
    for(unsigned t=0;t<5000;++t){
        if(t%10==0)for(auto [type,index]:streams)aecp_changed(&adapter.core,type,index,8);
        if(t==2000)mbx_model_tx_pause(&fabric,true);
        if(t==2002)mbx_model_tx_pause(&fabric,false);
        service(100);
        while(seen<fabric.tx_sent){
            auto*f=mbx_model_tx_frame(&fabric,seen++);ASSERT_NE(f,nullptr);
            if(get(f->bytes+36,2)!=0x8029)continue;
            Key key{get(f->bytes+38,2),get(f->bytes+40,2),get(f->bytes+26,8)};
            departures[key].push_back(f->now_ms-origin);
        }
        mbx_model_advance_ms(&fabric,1);
    }
    for(auto [type,index]:streams)for(uint64_t recipient:{CTLR,CTLR+1}){
        auto&times=departures[{type,index,recipient}];
        if(cadence){EXPECT_GE(times.size(),5u)<<"[F5 CADENCE] recipient total "<<type<<":"<<index;}
        unsigned bins[5]{};
        uint32_t min_gap=5000;
        uint32_t max_gap=0;
        for(size_t n=0;n<times.size();++n){
            ASSERT_LT(times[n],5000u);++bins[times[n]/1000];
            if(n){min_gap=std::min(min_gap,times[n]-times[n-1]);
                  max_gap=std::max(max_gap,times[n]-times[n-1]);}
        }
        for(unsigned window=0;window<5;++window){
            if(cadence){EXPECT_GE(bins[window],1u)<<"[F5 CADENCE] window "<<type<<":"<<index;}
            if(rate){EXPECT_LE(bins[window],1u)<<"[F5 RATE] window "<<type<<":"<<index;}
            printf("F5,%u,%u,%u,%u,%u,%u,%u\n",type,index,
                   unsigned(recipient-CTLR),window,bins[window],min_gap,max_gap);
        }
        if(rate){EXPECT_GE(min_gap,1000u)<<"[F5 RATE] Milan 5.4.5.2 Table 5.22 spacing";}
        if(cadence){EXPECT_LE(max_gap,1003u)<<"[F5 CADENCE] 1000 ms plus 2 ms stall and one service pass";}
    }
}
