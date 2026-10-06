// Independent review probe: receiving interface, truncated identity, tags and saturation.
#include <cstdint>
#include <cstdio>
#include <memory>
#include <vector>
#include "mbx_contract.h"
#include "frames.hpp"
#include "../../common/verilator_harness.hpp"
#ifdef PROBE_MODEL
#include "model_bench.hpp"
#else
#include "bench.hpp"
#endif
constexpr std::uint64_t eid = 0x1020304050607080ull;
constexpr std::uint64_t mac0 = 0x0222446688AAull;
constexpr std::uint64_t mac1 = 0x02AB13579BDFull;
template<class B> int probe(B& b) {
  milan::tb::Checker ck{"R523 boundaries"};
  auto reg = [](unsigned ch, unsigned off) { return MBX_CH_BASE+ch*MBX_CH_STRIDE+off; };
  auto setup = [&]() {
    b.reset();
    b.write(MBX_REG_OWN_EID_LO,static_cast<std::uint32_t>(eid));
    b.write(MBX_REG_OWN_EID_HI,static_cast<std::uint32_t>(eid>>32));
    for (unsigned i=0;i<MBX_N_IF;++i) {
      const auto m=i==0?mac0:mac1;
      b.write(MBX_IFF_BASE+i*MBX_IFF_STRIDE+MBX_IFF_REG_OWN_MAC_LO,static_cast<std::uint32_t>(m));
      b.write(MBX_IFF_BASE+i*MBX_IFF_STRIDE+MBX_IFF_REG_OWN_MAC_HI,static_cast<std::uint32_t>(m>>32));
    }
    b.write(MBX_REG_FILTER_EN,31);
  };
  auto offer = [&](std::vector<std::uint8_t> f,unsigned iface,bool pass,unsigned delta) {
    unsigned heads[MBX_N_CH];
    for (unsigned c=0;c<MBX_N_CH;++c) heads[c]=b.read(reg(c,MBX_CH_REG_RX_HEAD));
    const auto before=b.read(MBX_REG_FILTER_MISMATCH);
    b.send_frame(f,iface);
    ck.that("ingress completes",b.drain_rx(10000));
    for (unsigned c=0;c<MBX_N_CH;++c) {
      auto h=b.read(reg(c,MBX_CH_REG_RX_HEAD));
      ck.that("only expected AECP ring moves",(h!=heads[c])==(pass&&c==MBX_CH_AECP));
      if (h!=heads[c]) b.write(reg(c,MBX_CH_REG_RX_TAIL),h);
    }
    ck.dec("tuple mismatch delta",b.read(MBX_REG_FILTER_MISMATCH)-before,delta);
    b.ms(20);
  };
  setup();
  for (unsigned i=0;i<2;++i) {
    auto m=i==0?mac0:mac1;
    // Complete only the selected identity, and one byte short of it.
    for (unsigned response=0;response<2;++response) {
      const unsigned n=response?34:26;
      auto f=mbx_tb::aecp(response,response?~eid:eid,response?eid:~eid,m);
      f.resize(n-1); offer(f,i,false,0);
      f=mbx_tb::aecp(response,response?~eid:eid,response?eid:~eid,m);
      f.resize(n); offer(f,i,true,0);
    }
    for (unsigned bit=0;bit<48;++bit)
      offer(mbx_tb::aecp(0,eid,~eid,m^(1ull<<bit)),i,false,1);
    offer(mbx_tb::aecp(0,eid,~eid,i==0?mac1:mac0),i,false,1);
    for (auto tpid:{0x8100u,0x88A8u,0x88E7u}) {
      auto f=mbx_tb::tagged(mbx_tb::aecp(1,~eid,eid,m));
      f[12]=static_cast<std::uint8_t>(tpid>>8); f[13]=static_cast<std::uint8_t>(tpid);
      offer(f,i,false,0);
      offer(mbx_tb::tagged(f),i,false,0);
    }
  }
  // The same foreign destination, truncated at every header byte, alternates
  // with an accepted frame so stale destination and mismatch state is exposed.
  for (unsigned n=1;n<=15;++n) {
    auto f=mbx_tb::aecp(0,eid,~eid,0x02FFFFFFFFFEull); f.resize(n);
    offer(f,0,false,n>=15?1:0);
    offer(mbx_tb::aecp(0,eid,~eid,mac0),0,true,0);
  }
  setup();
  b.write(MBX_REG_FILTER_EN,0);
  auto wrong=mbx_tb::aecp(0,eid,~eid,0x02FFFFFFFFFEull); wrong.resize(15);
  for (unsigned k=0;k<65534;++k) {
    b.send_frame(wrong,k&1u);
    if (!b.drain_rx(200)) { ck.that("saturation ingress completes",false); break; }
  }
  ck.dec("counter reaches 65534",b.read(MBX_REG_FILTER_MISMATCH),65534);
  b.send_frame(wrong,0); ck.that("65535 completes",b.drain_rx(200));
  ck.dec("counter reaches 65535",b.read(MBX_REG_FILTER_MISMATCH),65535);
  b.send_frame(wrong,1); ck.that("65536 completes",b.drain_rx(200));
  ck.dec("counter saturates without wrapping",b.read(MBX_REG_FILTER_MISMATCH),65535);
  b.write(MBX_REG_FILTER_MISMATCH,0);
  ck.dec("nonzero counter is read only",b.read(MBX_REG_FILTER_MISMATCH),65535);
  b.reset();
  ck.dec("reset clears nonzero counter",b.read(MBX_REG_FILTER_MISMATCH),0);
  for (unsigned i=0;i<MBX_N_IF;++i) {
    ck.dec("reset clears programmed own MAC low",b.read(MBX_IFF_BASE+i*MBX_IFF_STRIDE+MBX_IFF_REG_OWN_MAC_LO),0);
    ck.dec("reset clears programmed own MAC high",b.read(MBX_IFF_BASE+i*MBX_IFF_STRIDE+MBX_IFF_REG_OWN_MAC_HI),0);
  }
  ck.dec("no host timeout",b.bus_timeouts,0);
  return ck.report();
}
int main(int argc,char** argv) {
#ifdef PROBE_MODEL
  (void)argc; (void)argv;
  auto m=std::make_unique<mbx_model>(); mbx_tb::ModelBench b(m.get());
#else
  Verilated::commandArgs(argc,argv);
  const milan::tb::Model<Vtb_mbx_top> m;
  mbx_tb::Bench b(m.get(),argc>1&&argv[1][0]=='1'?1:0);
#endif
  return probe(b);
}
