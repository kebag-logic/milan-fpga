// SPDX-License-Identifier: CERN-OHL-W-2.0
// Wire values are predicted from injected events and commanded mappings.
#include "Vloopback_wrap.h"
#include "../../common/verilator_harness.hpp"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <map>
#include <vector>
#include <cstdlib>

namespace {
constexpr int kPeriod = 1024;
using Frame = std::array<uint32_t, 8>;
uint32_t sample(int s, int c, int f) {
    return 0x800000u | (unsigned(s) << 20) | (unsigned(c) << 17) | unsigned(f);
}
// An unset control reads as zero; a malformed one stops the run instead.
int env_int(const char* name) {
    const char* text = std::getenv(name);
    if (!text) return 0;
    char* end = nullptr;
    const long value = std::strtol(text, &end, 10);
    if (end == text || *end != '\0') {
        std::fprintf(stderr, "%s=%s is not a decimal integer\n", name, text);
        std::exit(2);
    }
    return int(value);
}
uint32_t stamp(int f) { return uint32_t(0xFFF00000ull + uint64_t(f)*62500/3); }
struct Beat { uint64_t data; uint8_t keep; bool last; };
class Bench {
    milan::tb::Model<Vloopback_wrap> model;
    Vloopback_wrap* d = model.get();
    uint64_t cycles = 0;
    int failures = 0;
    int checks = 0;
    int packets = 0;
    unsigned feed = (1u << NSTREAMS)-1;
    std::array<uint8_t, NSTREAMS> seq{};
    std::array<uint8_t, 64> map{};
    std::array<int, 8> outputs{};
    std::map<std::pair<int,int>, Frame> injected;
    std::deque<Beat> incoming;
    std::deque<Frame> expected_wire;
    std::vector<uint8_t> wire;
    Frame expected{};
    int valid_from = 1;
    bool events = true;
    // Sweep the prediction-horizon rate error with worst-sign marker jitter.
    // Environment controls leave the standard mutation oracle unchanged.
    int stamp_ppm = env_int("STAMP_PPM");
    int stamp_jitter = env_int("STAMP_JITTER_NS");
    int capture_offset(int frame) const {
        if (!stamp_ppm && !stamp_jitter) return 0;
        int ramp = (frame % 65) - 32;
        int ppm = stamp_ppm * ramp / 32;
        int rate = int((int64_t(LEAD+1)*62500*std::abs(ppm)+2999999)/3000000);
        return (ramp < 0 ? -1 : 1) * (rate + stamp_jitter);
    }
    void check(bool ok, const char* label, uint32_t got=0, uint32_t want=0) {
        ++checks;
        if (!ok && failures++ < 12) {
            std::printf("FAIL %s frame=%llu phase=%llu got=%06x want=%06x\n", label,
                static_cast<unsigned long long>(cycles/kPeriod+1), static_cast<unsigned long long>(cycles%kPeriod), got, want);
        }
    }
    void packet(int s, int first) {
        std::vector<uint8_t> f(38+6*8*4);
        f[0]=0x91; f[1]=0xE0; f[2]=0xF0;
        f[6]=2; f[11]=2; f[12]=0x22; f[13]=0xF0;
        f[14]=2; f[15]=0x81; f[16]=seq[s]++;
        uint64_t sid=0x0200000000020000ull+unsigned(s);
        for (int b=0;b<8;++b) f[18+b]=uint8_t(sid>>(56-8*b));
        uint32_t ts=stamp(first);
        for(int b=0;b<4;++b) f[26+b]=uint8_t(ts>>(24-8*b));
        f[30]=2; f[31]=0x50; f[32]=8; f[33]=32; f[34]=0; f[35]=192;
        for(int e=0;e<6;++e) {
            Frame values{};
            for(int c=0;c<8;++c) {
                uint32_t v=sample(s,c,first+e); values[c]=v;
                int o=38+4*(e*8+c);
                f[o]=uint8_t(v>>16); f[o+1]=uint8_t(v>>8); f[o+2]=uint8_t(v);
            }
            injected[{s,first+e}]=values;
        }
        for(size_t o=0;o<f.size();o+=8) {
            Beat b{}; b.last=o+8>=f.size();
            for(size_t n=0;n<8 && o+n<f.size();++n) {b.data|=uint64_t(f[o+n])<<(8*n);b.keep|=1u<<n;}
            incoming.push_back(b);
        }
    }
    Frame predict(int frame) {
        Frame result{};
        if (frame<valid_from || !events) return result;
        for(int c=0;c<8;++c) {
            int dest=outputs[c];
            if(dest<0 || dest>=CHANNELS) continue;
            auto e=map[FIRST+dest];
            if ((e&0xC0)!=0x80) continue;
            auto it=injected.find({(e>>3)&7,frame-1});
            if(it!=injected.end()) result[c]=it->second[e&7];
        }
        return result;
    }
    void decode() {
        if (!d->tx_valid_o) return;
        for(int n=0;n<8;++n) if(d->tx_keep_o&(1u<<n)) wire.push_back(uint8_t(d->tx_data_o>>(8*n)));
        if(!d->tx_last_o) return;
        size_t payload=(wire.size()>14 && wire[12]==0x81) ? 42 : 38;
        check(wire.size()==payload+192,"WIRE_LENGTH");
        check(expected_wire.size()>=6,"WIRE_EVENT_COUNT");
        if(wire.size()==payload+192 && expected_wire.size()>=6) {
            for(int e=0;e<6;++e) {
                Frame want=expected_wire.front(); expected_wire.pop_front();
                for(int c=0;c<8;++c) {
                    size_t o=payload+4*(e*8+c);
                    uint32_t got=(uint32_t(wire[o])<<16)|(uint32_t(wire[o+1])<<8)|wire[o+2];
                    check(got==want[c],"WIRE_SAMPLE",got,want[c]);
                    check(wire[o+3]==0,"WIRE_PAD");
                }
            }
        }
        ++packets; wire.clear();
    }
public:
    void step() {
        int frame=int(cycles/kPeriod)+1;
        int phase=int(cycles%kPeriod);
        if(phase==400 && frame%6==0)
            for(int s=0;s<NSTREAMS;++s) if(feed&(1u<<s)) packet(s,frame+12);
        d->ev_i=events && phase==0; d->close_i=events && phase==250; d->tick_i=phase==300;
        if(events) d->frame_ns_i=stamp(frame)+uint32_t(phase>=250 ? capture_offset(frame) : 0);
        d->rx_valid_i=0; d->rx_last_i=0;
        if(cycles%8==0 && !incoming.empty()) {
            Beat b=incoming.front(); incoming.pop_front();
            d->rx_valid_i=1; d->rx_data_i=b.data; d->rx_keep_i=b.keep; d->rx_last_i=b.last;
        }
        if(phase==300) {expected=predict(frame);expected_wire.push_back(expected);}
        d->clk=0;d->eval();decode(); d->clk=1;d->eval();
        if(d->pair_valid_o) {
            int c=2*d->pair_slot_o;
            check(c<8,"PAIR_INDEX");
            if(c<8) {
                check(d->pair_l_o==expected[c],"COPY_SAMPLE_L",d->pair_l_o,expected[c]);
                check(d->pair_r_o==expected[c+1],"COPY_SAMPLE_R",d->pair_r_o,expected[c+1]);
            }
        }
        ++cycles;
    }
    void until(int frame,int phase=200) {while(cycles<uint64_t(frame-1)*kPeriod+phase)step();}
    void setmap(int dest,int s,int ch,bool en=true) {
        map[FIRST+dest]=en ? uint8_t(0x80|(s<<3)|ch) : 0;
        for(int n=0;n<16;++n) d->map_i[n]=uint32_t(map[4*n])|(uint32_t(map[4*n+1])<<8)
            |(uint32_t(map[4*n+2])<<16)|(uint32_t(map[4*n+3])<<24);
    }
    void invalidate() {
        valid_from=int(cycles/kPeriod)+1+LEAD+2;
        d->invalidate_i=1;step();d->invalidate_i=0;
    }
    void output(int c,int dest) {
        outputs[c]=dest;d->out_write_i=1;d->out_addr_i=c;
        d->out_word_i=dest<0 ? 0 : 0x1600|((dest&1)<<11)|((dest/8)<<4)|((dest%8)/2);
        step();d->out_write_i=0;
    }
    int run() {
        d->rst_n=0;
        for(int i=0;i<8;++i){d->clk=0;d->eval();d->clk=1;d->eval();}
        d->rst_n=1;
        for(int c=0;c<CHANNELS;++c) setmap(c,(c/8+1)%NSTREAMS,7-c%8);
        for(int c=0;c<8;++c)output(c,c);
        until(80);
        check(d->pdus_o>0,"REAL_RX_ACCEPTANCE");
        check(stamp(40)>stamp(60),"TIMESTAMP_WRAP_DURING_LIVE_AUDIO");
        // Visit every destination, including destination 62 and invalid 63.
        for(int base=0;base<CHANNELS;base+=8) {
            for(int c=0;c<8;++c)output(c,base+c);
            until(int(cycles/kPeriod)+1+18);
        }
        for(int c=0;c<8;++c)output(c,c%2); // output fan-out
        setmap(0,NSTREAMS-1,2);setmap(1,NSTREAMS-1,2);invalidate();
        until(int(cycles/kPeriod)+1+20);
        setmap(0,0,0,false);invalidate(); // REMOVE
        until(int(cycles/kPeriod)+1+20);
        setmap(0,0,6);invalidate(); // replacement
        until(int(cycles/kPeriod)+1+20);
        // Edit while the scheduled copy is active; no mixed map publishes.
        until(int(cycles/kPeriod)+2,4*NSTREAMS+12);
        setmap(0,0,5);invalidate();
        until(int(cycles/kPeriod)+1+20);
        // Domain loss during live traffic clears retained frames immediately.
        events=false; feed=0; incoming.clear(); injected.clear(); invalidate();
        until(int(cycles/kPeriod)+1+8);
        events=true; invalidate();
        until(int(cycles/kPeriod)+1+8);
        feed=(1u<<NSTREAMS)-1;
        until(int(cycles/kPeriod)+1+40);
        // Reset during activity: neither RAM has reset contents. Only newly
        // accepted packets may reappear once the scheduler restarts.
        feed=0; incoming.clear(); injected.clear();
        d->rst_n=0;
        for(int i=0;i<8;++i) step();
        d->rst_n=1; expected_wire.clear(); wire.clear();
        valid_from=int(cycles/kPeriod)+1+LEAD+2;
        for(int c=0;c<8;++c) output(c,c%2);
        until(int(cycles/kPeriod)+1+30);
        feed=(1u<<NSTREAMS)-1;
        until(int(cycles/kPeriod)+1+40);
        // Missing receive data, beyond both queue and frame-tag wraps.
        feed=0;until(int(cycles/kPeriod)+1+2300);
        events=false;until(int(cycles/kPeriod)+1+8);
        events=true;invalidate();
        until(int(cycles/kPeriod)+1+8); // allow the shared row flush to finish
        feed=(1u<<NSTREAMS)-1;
        until(int(cycles/kPeriod)+1+40);
        // Invalidate all retained pages at bind loss. Future source rows go too.
        feed=0;incoming.clear();d->flush_i=(1u<<NSTREAMS)-1;
        for(auto& entry:injected)entry.second.fill(0);
        invalidate();d->flush_i=0;
        until(int(cycles/kPeriod)+1+24);
        check(packets>100,"WIRE_COVERAGE");
        // The count is in a shape the sweep's tally reads (scripts/suite_tally.py).
        std::printf("%s input-loopback streams=%d channels=%d lead=%d: %d checks, %d failures, packets=%d\n",
            failures?"FAIL":"PASS",NSTREAMS,CHANNELS,LEAD,checks,failures,packets);
        return failures?1:0;
    }
};
}
int main(int argc,char**argv){Verilated::commandArgs(argc,argv);Bench b;return b.run();}
