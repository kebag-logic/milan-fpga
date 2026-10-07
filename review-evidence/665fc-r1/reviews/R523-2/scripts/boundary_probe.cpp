#include <cstdint>
#include <cstdio>
#include <memory>
#include <vector>
#include "mbx_contract.h"
#include "frames.hpp"
#ifdef MODEL
#include "model_bench.hpp"
#else
#include "verilated.h"
#include "Vtb_mbx_top.h"
#include "bench.hpp"
#endif
static unsigned checks=0,failures=0;
void check(bool ok,const char* s){++checks;if(!ok){++failures;std::printf("FAIL %s\n",s);}}
constexpr uint64_t mac=0x021122334455ull, base=0x91E0F0000100ull;
uint32_t cr(unsigned c,uint32_t r){return MBX_CH_BASE+c*MBX_CH_STRIDE+r;}
template<class B> void setup(B& b){b.reset();b.write(MBX_REG_OWN_EID_LO,0x55667788);b.write(MBX_REG_OWN_EID_HI,0x11223344);for(unsigned i=0;i<MBX_N_IF;++i){b.write(MBX_IFF_BASE+i*MBX_IFF_STRIDE+MBX_IFF_REG_OWN_MAC_LO,uint32_t(mac+i));b.write(MBX_IFF_BASE+i*MBX_IFF_STRIDE+MBX_IFF_REG_OWN_MAC_HI,mac>>32);}b.write(MBX_REG_MAAP_BASE_LO,uint32_t(base));b.write(MBX_REG_MAAP_BASE_HI,base>>32);b.write(MBX_REG_MAAP_COUNT,8);b.write(MBX_REG_FILTER_EN,31);}
std::vector<uint8_t> frame(unsigned len,unsigned type,unsigned dst){auto f=mbx_tb::maap(type,base,8);mbx_tb::put_be(f,0,dst==0?mac:dst==1?mbx_tb::kMaapMac:mac+99,6);f[15]=type;f.resize(len);return f;}
template<class B> void run(B& b){
 // Independent expected tuple, identity and size outcomes, every prefix and low nibble.
 for(unsigned n=1;n<=66;++n)for(unsigned t=0;t<16;++t)for(unsigned d=0;d<3;++d){setup(b);auto f=frame(n,t,d);b.send_frame(f,0);check(b.drain_rx(),"prefix drains");bool tuple=n>=15&&(d==1||(d==0&&n>=16&&t==2));bool identity=n>=34&&t>=1&&t<=3;bool accepted=tuple&&identity&&n<=64;check(b.read(MBX_REG_FILTER_MISMATCH)==unsigned(n>=15&&!tuple),"prefix mismatch exactly once");for(unsigned c=0;c<MBX_N_CH;++c)check(b.read(cr(c,MBX_CH_REG_RX_HEAD))==(c==MBX_CH_MAAP&&accepted?2+(n+3)/4:0),"prefix publication");check(b.read(cr(MBX_CH_MAAP,MBX_CH_REG_RX_DROP))==unsigned(tuple&&identity&&n>64),"size distinct from mismatch");}
 // The high nibble is not part of message_type.
 for(unsigned t=0;t<256;++t){setup(b);b.send_frame(frame(42,t,0),0);check(b.drain_rx(),"high-nibble drains");check(b.read(cr(MBX_CH_MAAP,MBX_CH_REG_RX_PASS))==unsigned((t&15)==2),"low nibble only");check(b.read(MBX_REG_FILTER_MISMATCH)==unsigned((t&15)!=2),"low-nibble mismatch");}
 // Both subtype-free tuples keep the old 15-byte boundary behavior.
 for(unsigned et:{unsigned(mbx_tb::kEtherMsrp),unsigned(mbx_tb::kEtherMvrp)})for(unsigned n:{14u,15u,16u}){setup(b);auto f=mbx_tb::mrp(et,{0,1});f.resize(n);b.send_frame(f,0);check(b.drain_rx(),"MRP drains");check(b.read(cr(MBX_CH_SRP,MBX_CH_REG_RX_HEAD))==(n>=15?2+(n+3)/4:0),"MRP byte-14 classification preserved");check(b.read(MBX_REG_FILTER_MISMATCH)==0,"MRP no mismatch");}
 setup(b);auto bad=frame(15,2,2);for(unsigned i=0;i<65540;++i){b.send_frame(bad,0);check(b.drain_rx(),"saturation stream drains");}check(b.read(MBX_REG_FILTER_MISMATCH)==65535,"mismatch saturates");b.reset();check(b.read(MBX_REG_FILTER_MISMATCH)==0,"reset clears saturation");
}
#ifndef MODEL
void raw_tick(Vtb_mbx_top* d){d->clk_i=0;d->eval();d->clk_i=1;d->eval();}
void raw_checks(mbx_tb::Bench& b){auto* d=b.dut();auto good=frame(42,2,0);
 // A pause at every prefix, then reset. No stale classification survives.
 for(unsigned stop=0;stop<=17;++stop){setup(b);for(unsigned i=0;i<stop;++i){d->rx_valid_i=1;d->rx_data_i=good[i];d->rx_last_i=0;d->rx_if_i=0;d->clk_i=0;d->eval();check(d->rx_ready_o!=0||i>=16,"first sixteen bytes need no drain");if(!d->rx_ready_o){raw_tick(d);d->clk_i=0;d->eval();}check(d->rx_ready_o!=0,"post-decision drains");raw_tick(d);}d->rx_valid_i=0;for(unsigned i=0;i<5;++i)raw_tick(d);setup(b);b.send_frame(good,0);check(b.drain_rx(),"reset recovery drains");check(b.read(cr(MBX_CH_MAAP,MBX_CH_REG_RX_PASS))==1,"reset recovery publishes exactly one");check(b.read(MBX_REG_FILTER_MISMATCH)==0,"reset no stale mismatch");}
 // A valid frame offered directly, with a gap after every byte, records every byte.
 setup(b);for(unsigned i=0;i<good.size();++i){d->rx_valid_i=1;d->rx_data_i=good[i];d->rx_last_i=i+1==good.size();d->rx_if_i=0;d->clk_i=0;d->eval();check(d->rx_ready_o,"gapped frame ready");raw_tick(d);d->rx_valid_i=0;for(unsigned g=0;g<3;++g)raw_tick(d);}b.idle(12);check(b.read(cr(MBX_CH_MAAP,MBX_CH_REG_RX_HEAD))==13,"gapped frame publishes");for(unsigned i=0;i<good.size();++i){auto w=b.read(MBX_CH_MAAP_RX_BASE+8+4*(i/4));check(((w>>(8*(i%4)))&255)==good[i],"gapped byte exact");}}
#endif
int main(int argc,char** argv){
#ifdef MODEL
 (void)argc;(void)argv;auto m=std::make_unique<mbx_model>();mbx_tb::ModelBench b(m.get());run(b);
#else
 Verilated::commandArgs(argc,argv);auto m=std::make_unique<Vtb_mbx_top>();mbx_tb::Bench b(m.get(),argc>1?unsigned(argv[1][0]-'0'):0);run(b);raw_checks(b);
#endif
 std::printf("Independent boundary probe: %u checks, %u failures; interfaces=%u\n",checks,failures,unsigned(MBX_N_IF));return failures?1:0;}
