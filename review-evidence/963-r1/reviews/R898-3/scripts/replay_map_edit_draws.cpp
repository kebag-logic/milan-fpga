// Standalone replay of the seeded draws and the reference model ("definition") of
// sw/firmware/ctrl/test/test_aecp.cpp Core.MapEditsAreTheirDefinitionRowForRow at a18f0996.
// No firmware is compiled: it recomputes, from the test's own RNG and model, how many edits carry
// each illegal kind and how many output edits are refused at an unread existing stream's illegal mapping.
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <utility>
#include <vector>
struct aecp_mapping { uint16_t stream, channel, cluster, cluster_channel; };
int main(int argc,char**argv){
    const uint16_t PAST=argc>1?uint16_t(atoi(argv[1])):8; // any value >= 4 (the test asserts >= 4)
    constexpr uint16_t ILLEGAL=65535;
    uint16_t past[2]={PAST,PAST};
    auto illegal=[&](bool in,const aecp_mapping &r){return r.stream==ILLEGAL||r.channel==past[in];};
    auto same=[](const aecp_mapping &x,const aecp_mapping &y){
        return x.stream==y.stream&&x.channel==y.channel&&x.cluster==y.cluster&&x.cluster_channel==y.cluster_channel;};
    struct Outcome { unsigned status=0; std::vector<aecp_mapping> rows; unsigned reads=0; bool unread=false; };
    auto definition=[&](bool in,bool add,const std::vector<aecp_mapping> &held,size_t room,
                        const std::vector<aecp_mapping> &owned,const std::vector<aecp_mapping> &edit,bool running){
        auto key=[in](const aecp_mapping &r){
            return in?std::make_pair(r.cluster,r.cluster_channel):std::make_pair(r.stream,r.channel);};
        auto holds=[&](auto first,auto last,const aecp_mapping &r){
            return std::any_of(first,last,[&](const aecp_mapping &x){return same(x,r);});};
        Outcome o{0,held,0};
        size_t additions=0;
        std::vector<uint16_t> observed;
        for(size_t n=0;n<edit.size();++n){
            const aecp_mapping &r=edit[n];
            bool refused=illegal(in,r);
            const bool unread=std::find(observed.begin(),observed.end(),r.stream)==observed.end();
            o.unread=refused&&!in&&r.stream!=ILLEGAL&&unread;
            if(!refused&&!in){
                if(unread){observed.push_back(r.stream);++o.reads;}
                refused=running||std::any_of(owned.begin(),owned.end(),
                                             [&](const aecp_mapping &x){return x.stream==r.stream&&x.channel==r.channel;});
            }
            for(size_t k=0;add&&k<n;++k)refused=refused||(key(edit[k])==key(r)&&!same(edit[k],r));
            for(auto &x:held)refused=refused||(add&&key(x)==key(r)&&!same(x,r));
            refused=refused||(!add&&!holds(held.begin(),held.end(),r));
            if(refused){o.status=7;return o;}
            additions+=add&&!holds(held.begin(),held.end(),r)&&!holds(edit.begin(),edit.begin()+n,r);
        }
        if(additions>room){o.status=8;return o;}
        return o;
    };
    uint32_t seed=0x904u;
    auto next=[&]{seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed;};
    auto legal=[&]{return aecp_mapping{uint16_t(next()%2),uint16_t(next()%4),uint16_t(next()%4),0};};
    auto wide=[&]{return aecp_mapping{uint16_t(next()%8),uint16_t(next()%1024),uint16_t(next()%1024),uint16_t(next()%4)};};
    constexpr unsigned ABSENT=4000;
    unsigned carriers[2]={0,0},unread[2]={0,0},refused_illegal_new=0;
    for(unsigned c=0;c<2*ABSENT;++c){
        const bool in=next()%2,add=next()%2;
        std::vector<aecp_mapping> held,lawful,owned,edit;
        for(unsigned n=next()%9;n--;){
            unsigned pick=next()%20;
            aecp_mapping r=pick<12||held.empty()?legal():pick<15?held[next()%held.size()]:pick<17?legal():wide();
            if(pick==15||pick==16)r.cluster_channel=1;
            held.push_back(r);
            if(pick<12||(pick<15&&r.cluster_channel==0&&r.stream<2&&r.channel<4&&r.cluster<4))lawful.push_back(r);
        }
        for(unsigned n=next()%4;n--;)owned.push_back(next()%3?legal():wide());
        for(unsigned n=next()%11;n--;){
            unsigned pick=next()%10;
            if(!edit.empty()&&pick<3)edit.push_back(edit[next()%edit.size()]);
            else if(!lawful.empty()&&pick<(add?5u:8u))edit.push_back(lawful[next()%lawful.size()]);
            else edit.push_back(legal());
        }
        bool carries=false;
        if(!edit.empty()&&next()%8==0){
            const size_t at=next()%edit.size();
            edit[at]=c<ABSENT?aecp_mapping{ILLEGAL,0,0,0}:aecp_mapping{uint16_t(next()%2),past[in],0,0};
            carries=true;
        }
        const size_t room=next()%3;
        const bool streaming=!in&&next()%10==0;
        const Outcome want=definition(in,add,held,room,owned,edit,streaming);
        const unsigned half=c<ABSENT?0:1;
        carriers[half]+=carries;
        unread[half]+=want.unread;
        refused_illegal_new+=half&&carries&&want.status==7;
    }
    std::printf("past=%u carriers no-stream=%u existing-stream=%u packed=%u\n",PAST,carriers[0],carriers[1],
                carriers[0]*100000u+carriers[1]);
    std::printf("unread-refusals first-half=%u second-half=%u total=%u\n",unread[0],unread[1],unread[0]+unread[1]);
    std::printf("second-half carriers refused (status 7)=%u\n",refused_illegal_new);
    return 0;
}
