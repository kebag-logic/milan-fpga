// SPDX-License-Identifier: CERN-OHL-W-2.0
// aaf_talker_i2s harness: SDOUT tied 1 -> samples 0xFFFFFF; checks the AAF
// frame byte-exactly (header + payload + seq + cadence) on the AXIS master.
#include "Vaaf_talker_i2s.h"
#include "verilated.h"
#include <cstdio>
#include <vector>
static Vaaf_talker_i2s* dut; static long checks=0, fails=0;
static void ck(const char* w, unsigned long g, unsigned long e){checks++;if(g!=e){fails++;printf("  [FAIL] %-30s got=0x%lx exp=0x%lx\n",w,g,e);}}
static void step(){dut->clk_i=0;dut->eval();dut->clk_i=1;dut->eval();}
static std::vector<unsigned char> collect(int maxc){std::vector<unsigned char> b;for(int c=0;c<maxc;c++){dut->m_axis_tready=1;dut->clk_i=0;dut->eval();bool v=dut->m_axis_tvalid;bool l=dut->m_axis_tlast;unsigned long long d=dut->m_axis_tdata;unsigned k=dut->m_axis_tkeep;dut->clk_i=1;dut->eval();if(v){for(int i=0;i<8;i++)if((k>>i)&1)b.push_back((d>>(8*i))&0xFF);if(l)return b;}}return b;}
static unsigned long be(std::vector<unsigned char>&b,int o,int n){unsigned long v=0;for(int i=0;i<n;i++)v=(v<<8)|b[o+i];return v;}
int main(int argc,char**argv){Verilated::commandArgs(argc,argv);dut=new Vaaf_talker_i2s;
 dut->rst_n=0;dut->enable_i=0;dut->adv_i=1;  // tie 1 = legacy clk/2^N rate (golden checks)
 dut->i2s_sdout_i=1;dut->m_axis_tready=1;
 dut->dest_mac_i=0x91E0F000FE01ULL;dut->station_mac_i=0x020000000002ULL;dut->vlan_vid_i=2;dut->ptp_ns_i=0x11223344;dut->transit_ns_i=2000000;  // was a localparam; now the AECP presentation-offset register drives it
 for(int i=0;i<8;i++)step(); dut->rst_n=1; dut->enable_i=1;
 printf("== aaf_talker_i2s ==\n");
 auto f=collect(200000);
 ck("frame length 90",f.size(),90);
 if(f.size()==90){
  ck("dst",be(f,0,6),0x91E0F000FE01UL); ck("src",be(f,6,6),0x020000000002UL);
  ck("tpid",be(f,12,2),0x8100); ck("tci pcp3 vid2",be(f,14,2),0x6002);
  ck("etype",be(f,16,2),0x22F0); ck("subtype AAF",f[18],0x02);
  ck("sv|tv",f[19],0x81); ck("seq0",f[20],0);
  ck("stream_id",be(f,22,8),0x0200000000020000UL);
  ck("format INT32",f[34],0x02); ck("nsr 48k",f[35]>>4,0x5);
  ck("ch=2",f[36],0x02); ck("depth 32",f[37],0x20);
  ck("sdlen 48",be(f,38,2),48);
  bool pay=true; for(int i=0;i<12;i++){int o=42+i*4; if(!(f[o]==0xFF&&f[o+1]==0xFF&&f[o+2]==0xFF&&f[o+3]==0x00))pay=false;}
  ck("payload 12x FFFFFF00",pay,1);
  ck("timestamp = ptp+2ms",be(f,30,4),0x11223344UL+2000000UL);
 }
 auto f2=collect(200000);
 ck("frame2 length",f2.size(),90); if(f2.size()==90) ck("seq1",f2[20],1);
 printf("aaf: %ld checks, %ld failures\nRESULT: %s\n",checks,fails,fails?"FAIL":"PASS");
 return fails?1:0;}
