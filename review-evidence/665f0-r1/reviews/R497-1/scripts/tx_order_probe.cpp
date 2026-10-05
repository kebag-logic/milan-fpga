#include <cstdio>
#include "verilated.h"
#include "bench.hpp"
#include "mbx_contract.h"
int main() {
  Vtb_mbx_top dut; mbx_tb::Bench b(&dut,0); b.reset(); b.tx_ready_pattern(0);
  const unsigned base[]=MBX_CH_TX_BASE_TBL;
  unsigned head[MBX_N_CH]={};
  auto commit=[&](unsigned ch) {
    unsigned start=base[ch]+4*head[ch];
    b.write(start,(14u<<MBX_TXREC_W0_LEN_LSB)|(MBX_TX_KIND<<MBX_TXREC_W0_KIND_LSB));
    b.write(start+4,0);
    for(unsigned i=0;i<4;i++)b.write(start+8+4*i,0);
    head[ch]+=6;
    b.write(MBX_CH_BASE+MBX_CH_STRIDE*ch+MBX_CH_REG_TX_HEAD,head[ch]);
    std::printf("COMMIT channel=%u\n",ch);
  };
  commit(MBX_CH_ACMP); b.idle(20); // Prior frame occupies transmitter while next pair commits.
  commit(MBX_CH_ACMP); commit(MBX_CH_AECP);
  b.tx_ready_pattern(0xff);
  if(!b.wait_tx(3))return 2;
  for(const auto& f:b.tx_frames)std::printf("WIRE channel=%u\n",f.channel);
  bool ordered=b.tx_frames[1].channel==MBX_CH_ACMP && b.tx_frames[2].channel==MBX_CH_AECP;
  std::printf("COMMIT_ORDER_PRESERVED=%u bus_timeouts=%u\n",ordered,b.bus_timeouts);
  return ordered ? 0 : 1;
}
