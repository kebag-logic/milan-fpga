// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reuse the firmware's real mailbox fixture and generated descriptor image.
// Appended to test_aecp.cpp by stream_counter_f5.py.
#include <map>
#include <tuple>

namespace {
struct F5CounterGaps {
    size_t count=0;
    uint32_t min_ms=5000;
    uint32_t max_ms=0;
    uint32_t tail_ms=0;
    bool refresh=false;
    bool spacing=true;
};

F5CounterGaps f5_counter_gaps(const std::vector<uint32_t>& times,uint32_t start_ms)
{
    F5CounterGaps result;
    uint32_t last=0;
    for(const uint32_t at:times) {
        if(at<start_ms || at>=5000) continue;
        if(result.count) {
            result.min_ms=std::min(result.min_ms,at-last);
            result.max_ms=std::max(result.max_ms,at-last);
        }
        ++result.count;
        last=at;
    }
    result.tail_ms=5000-(result.count ? last : start_ms);
    result.spacing=result.min_ms>=1000;
    result.refresh=result.count>=2 && result.max_ms<=1003 && result.tail_ms<=1003;
    return result;
}

void f5_check_counter_gaps(const std::vector<uint32_t>& times,unsigned type,unsigned index,unsigned recipient)
{
    const char* omitted=std::getenv("COUNTERS_OMIT_CHECK");
    const auto gaps=f5_counter_gaps(times,0);
    if(!omitted || std::strcmp(omitted,"RATE")!=0) {
        EXPECT_TRUE(gaps.spacing)<<"[F5 RATE] Milan 5.4.5.2 Table 5.22 spacing";
    }
    if(!omitted || std::strcmp(omitted,"CADENCE")!=0) {
        EXPECT_TRUE(gaps.refresh)<<"[F5 CADENCE] every gap and final wait <= 1000 ms plus 2 ms stall and one service pass";
    }
    bool stable=true;
    for(uint32_t start_ms=0;start_ms<=1000;++start_ms) {
        const auto shifted=f5_counter_gaps(times,start_ms);
        stable &= shifted.refresh==gaps.refresh && shifted.spacing==gaps.spacing;
    }
    if(!omitted || std::strcmp(omitted,"PHASE")!=0) {
        EXPECT_TRUE(stable)<<"[F5 PHASE] measurement starts through one second preserve verdict";
    }
    printf("F5_GAPS,%u,%u,%u,%zu,%u,%u,%u\n",type,index,recipient,gaps.count,gaps.min_ms,gaps.max_ms,gaps.tail_ms);
    unsigned bins[5]{};
    for(const auto at:times) {
        ASSERT_LT(at,5000u);
        ++bins[at/1000];
        printf("F5_NOTE,%u,%u,%u,%u\n",type,index,recipient,at);
    }
    // Fixed bins describe the capture; they never decide its verdict.
    for(unsigned window=0;window<5;++window)
        printf("F5,%u,%u,%u,%u,%u,%u,%u\n",type,index,recipient,window,bins[window],gaps.min_ms,gaps.max_ms);
}
} // namespace

TEST_F(Mailbox, StreamCounterGaps)
{
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
        f5_check_counter_gaps(departures[{type,index,recipient}],type,index,unsigned(recipient-CTLR));
    }
}
