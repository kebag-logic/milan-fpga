#include "VKL_aaf_packetizer.h"
#include <cstdint>
#include <cstdio>
#include <vector>
static VKL_aaf_packetizer d;
static std::vector<unsigned> bytes;
static unsigned frames=0;
static void tick() {
  d.clk_i=0; d.eval();
  if(d.m_axis_tvalid && d.m_axis_tready) {
    for(unsigned i=0;i<8;i++) if(d.m_axis_tkeep & (1u<<i)) bytes.push_back((d.m_axis_tdata>>(8*i))&255);
    if(d.m_axis_tlast) frames++;
  }
  d.clk_i=1; d.eval();
}
static void idle(unsigned n) { while(n--) tick(); }
static bool write(unsigned addr,uint32_t val) {
  d.tctx_wr_en_i=1; d.tctx_wr_addr_i=addr; d.tctx_wr_data_i=val;
  for(unsigned n=0;n<100;n++) {
    d.clk_i=0; d.eval(); bool ready=d.tctx_wr_rdy_o;
    tick(); if(ready) { d.tctx_wr_en_i=0; idle(4); return true; }
  }
  return false;
}
static uint64_t frame() {
  bytes.clear(); frames=0;
  for(int i=0;i<6;i++) { d.pair_valid_i=1; tick(); d.pair_valid_i=0; idle(10); }
  for(int n=0;n<2000 && !frames;n++) tick();
  if(frames!=1 || bytes.size()<30) return 0;
  uint64_t sid=0; for(int i=22;i<30;i++) sid=(sid<<8)|bytes[i];
  return sid;
}
int main() {
  const uint64_t mac=0x0a0b0c0d0e0full;
  const uint64_t initial=(mac<<16)|1, moved=(mac<<16)|8;
  d.rst_n=0; d.m_axis_tready=1; d.station_mac_i=mac;
  d.dest_mac_i=0x91e0f0000100ull; d.vlan_vid_i=2; d.vlan_pcp_i=3;
  d.pair_slot_i=1; d.pair_l_i=0x112233; d.pair_r_i=0x445566;
  d.stream_id_i[2]=uint32_t(initial); d.stream_id_i[3]=uint32_t(initial>>32);
  idle(4); d.rst_n=1; idle(30);
  if(!write(16,5|(2u<<5)) || !write(17,0xf0000101u) || !write(18,(1u<<16)|0x91e0u)) return 3;
  d.stream_en_i=2;
  const auto before=frame();
  d.stream_id_i[2]=uint32_t(moved); d.stream_id_i[3]=uint32_t(moved>>32);
  const auto after=frame();
  d.stream_en_i=0; idle(20); if(!write(18,0x91e0u)) return 3;
  d.stream_en_i=2;
  const auto fallback=frame();
  printf("PARENT before: published=%016llx wire=%016llx\n",(unsigned long long)initial,(unsigned long long)before);
  printf("PARENT moved, explicit UID 1: published=%016llx wire=%016llx\n",(unsigned long long)moved,(unsigned long long)after);
  printf("PARENT moved, default UID: published=%016llx wire=%016llx\n",(unsigned long long)moved,(unsigned long long)fallback);
  bool setup=before==initial && fallback==moved;
  printf("PARENT setup=%s post-move-agreement=%s\n",setup?"PASS":"FAIL",after==moved?"PASS":"FAIL");
  return !setup?3:after==moved?0:1;
}
