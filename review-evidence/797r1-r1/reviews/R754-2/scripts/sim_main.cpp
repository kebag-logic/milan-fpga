// Independent bit-level measurement of milan_csr behind a flat-vector wrapper.
#include "Vtb_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#define IB IN_BITS
#define OB OUT_BITS
static Vtb_top *t; static uint64_t cyc=0;
static uint32_t base_in[(IB+31)/32];
static uint32_t cur_out_or[(OB+31)/32], cur_out_xor[(OB+31)/32];
static uint32_t ref_out[(OB+31)/32]; static bool track=false;
static void apply_in(){ for(unsigned i=0;i<(IB+31)/32;i++) t->all_in[i]=base_in[i]; }
static void tick(){ t->aclk=0; t->eval(); t->aclk=1; t->eval(); cyc++;
  if(track){ for(unsigned i=0;i<(OB+31)/32;i++) cur_out_or[i]|=(t->all_out[i]^ref_out[i]); } }
static void hard_reset(){ apply_in(); t->aresetn=0; t->awvalid=0;t->wvalid=0;t->arvalid=0;t->bready=1;t->rready=1;
  for(int i=0;i<4;i++) tick(); t->aresetn=1; for(int i=0;i<530;i++) tick(); }
static bool wr(uint16_t a,uint32_t d){ t->awaddr=a;t->wdata=d;t->awvalid=1;t->wvalid=1; int n=0; t->eval();
  while(!t->awready){ tick(); t->eval(); if(++n>200){t->awvalid=0;t->wvalid=0;return false;} }
  tick(); t->awvalid=0;t->wvalid=0; t->eval(); tick(); tick(); return true; }
static bool rd(uint16_t a,uint32_t &v){ t->araddr=a;t->arvalid=1;int n=0; t->eval();
  while(!t->arready){ tick(); t->eval(); if(++n>200){t->arvalid=0;return false;} }
  tick(); t->arvalid=0; t->eval(); n=0;
  while(!t->rvalid){ tick(); t->eval(); if(++n>200) return false; }
  v=t->rdata; tick(); t->eval(); return true; }
static void set_port(unsigned pos,unsigned w,bool val){ for(unsigned i=0;i<w;i++){ unsigned b=pos+i; if(val) base_in[b/32]|=1u<<(b%32); else base_in[b/32]&=~(1u<<(b%32)); } }
int main(int argc,char**argv){ Verilated::commandArgs(argc,argv); t=new Vtb_top; t->aclk=0;
  std::string mode=argv[1];
  // handshake baseline positions passed as triples: pos width name via stdin file argv[2]
  FILE*f=fopen(argv[2],"r"); std::vector<unsigned> hs; std::vector<std::pair<std::string,std::pair<unsigned,unsigned>>> ports;
  char nm[128]; unsigned pos,w; int ish;
  while(fscanf(f,"%127s %u %u %d",nm,&pos,&w,&ish)==4){ ports.push_back({nm,{pos,w}}); if(ish){hs.push_back(pos);hs.push_back(w);} }
  fclose(f);
  auto baseline=[&](){ memset(base_in,0,sizeof(base_in)); for(size_t i=0;i<hs.size();i+=2) set_port(hs[i],hs[i+1],true); };
  unsigned AMAX=0x1000;
  if(mode=="reset"){ // reset value, inputs low then high
    for(int pat=0;pat<2;pat++){ memset(base_in,pat?0xFF:0,sizeof(base_in)); if(!pat) baseline(); hard_reset();
      for(unsigned a=0;a<AMAX;a+=4){ uint32_t v=0xDEADBEEF; bool ok=rd(a,v); printf("reset %d 0x%03X 0x%08X %d\n",pat,a,v,ok); } } }
  if(mode=="word"){ // write all-ones/zero/pattern from a fresh reset, inputs low
    baseline();
    for(unsigned a=0;a<AMAX;a+=4){ hard_reset(); uint32_t r0=0,r1=0,r2=0,r3=0; rd(a,r0);
      bool ok=wr(a,0xFFFFFFFF); for(int i=0;i<8;i++) tick(); rd(a,r1);
      ok&=wr(a,0); for(int i=0;i<8;i++) tick(); rd(a,r2);
      ok&=wr(a,0xA5A55A5A); for(int i=0;i<8;i++) tick(); rd(a,r3);
      printf("word 0x%03X rst=0x%08X w1=0x%08X w0=0x%08X wp=0x%08X ok=%d\n",a,r0,r1,r2,r3,ok); } }
  if(mode=="bit"){ // single-bit write: which output bits move, and readback
    baseline();
    for(unsigned a=0;a<AMAX;a+=4) for(int b=0;b<32;b++){ hard_reset();
      for(unsigned i=0;i<(OB+31)/32;i++){ ref_out[i]=t->all_out[i]; cur_out_or[i]=0; }
      uint32_t rb=0,r0=0; rd(a,r0); for(unsigned i=0;i<(OB+31)/32;i++){ ref_out[i]=t->all_out[i]; }
      track=true; wr(a,1u<<b); for(int i=0;i<12;i++) tick(); track=false; rd(a,rb);
      printf("bit 0x%03X %d r0=0x%08X rb=0x%08X out=",a,b,r0,rb);
      for(unsigned i=0;i<OB;i++) if(cur_out_or[i/32]>>(i%32)&1) printf("%u,",i); printf("\n"); } }
  if(mode=="input"){ // walk one input port high: which read words move
    baseline(); hard_reset(); std::vector<uint32_t> ref; for(unsigned a=0;a<AMAX;a+=4){uint32_t v=0; rd(a,v); ref.push_back(v);}
    for(auto&p:ports){ baseline(); set_port(p.second.first,p.second.second,true); hard_reset(); int k=0;
      for(unsigned a=0;a<AMAX;a+=4,k++){ uint32_t v=0; rd(a,v); if(v!=ref[k]) printf("input %s 0x%03X ref=0x%08X val=0x%08X xor=0x%08X\n",p.first.c_str(),a,ref[k],v,v^ref[k]); } } }

  if(mode=="directed"){
    auto pn=[&](const char*n)->std::pair<unsigned,unsigned>{ for(auto&p:ports) if(p.first==n) return p.second; printf("NOPORT %s\n",n); return {0,0}; };
    auto R=[&](const char*tag,uint16_t a){ uint32_t v=0xBAD; bool ok=rd(a,v); printf("%-44s rd 0x%03X = 0x%08X%s\n",tag,a,v,ok?"":" TIMEOUT"); return v; };
    auto W=[&](const char*tag,uint16_t a,uint32_t d){ bool ok=wr(a,d); for(int i=0;i<8;i++) tick(); printf("%-44s wr 0x%03X <= 0x%08X%s\n",tag,a,d,ok?"":" TIMEOUT"); };
    baseline(); hard_reset();
    puts("--- ETH_GUARD / PHY_RESET / LINK_CTRL");
    R("guard reset",0x7D8); R("phy reset",0x11C); W("guarded PHY_RESET write",0x11C,0xFFFFFFFE); R("dropped?",0x11C);
    W("guarded LINK_CTRL write",0x71C,0xFFFFFFFF); R("bit1 masked?",0x71C);
    W("wrong key",0x7D8,0x554E4C4C); R("guard stays",0x7D8); W("unlock",0x7D8,0x554E4C4B); R("guard clear",0x7D8);
    W("unguarded PHY_RESET",0x11C,0xFFFFFFFE); R("stored incl reserved",0x11C); W("unguarded LINK_CTRL",0x71C,0xFFFFFFFF); R("bit1 stored",0x71C);
    W("re-arm any value",0x7D8,0); R("guard set",0x7D8); W("guarded LINK_CTRL rewrite",0x71C,0x2); R("bit1 masked again",0x71C); R("phy unchanged while guarded",0x11C);
    puts("--- IRQ W1C"); baseline(); hard_reset();
    { auto p=pn("i_evt_link_change"); set_port(p.first,p.second,true); apply_in(); tick(); tick(); set_port(p.first,p.second,false); apply_in(); tick(); }
    R("status[1] latched",0x010); R("raw[1] latched",0x018); W("w1c bit0 (structural)",0x010,1); R("still set",0x010); W("w1c bit1",0x010,2); R("cleared",0x010); R("raw also clear",0x018);
    puts("--- STRM_SEL / SRP alias"); baseline(); { auto p=pn("i_lwsrp_status"); set_port(p.first,p.second,true);} hard_reset();
    R("LWSRP_STATUS flat",0x694); R("SRP dir0 idx0 lsn0=0",0x85C); W("sel talker idx0",0x800,0x100); R("SEL readback",0x800); R("SRP dir1 idx0",0x85C);
    W("sel lsn0 dir0 idx0",0x800,0x200); R("SEL readback bit9 hidden",0x800); R("SRP lsn0=1",0x85C); W("sel lsn0 + dir1",0x800,0x300); R("SRP lsn0+dir1 row",0x85C);
    W("sel idx1 out of range",0x800,0x1); R("SRP out of range",0x85C); R("0x86C out of range",0x86C); R("FMT_LO out of range",0x824);
    puts("--- talker window, idx 0 poison and aliases"); baseline(); hard_reset(); W("sel talker idx0",0x800,0x100);
    for(uint16_t a: {0x810,0x814,0x818,0x81C,0x820,0x824,0x828,0x82C,0x830,0x854,0x858,0x85C,0x860,0x864,0x868,0x86C}) R("talker word",a);
    W("write CTRL[0] alias",0x810,0xFFFFFFFF); R("AAF_CTRL flat merge",0x654); R("CTRL readback",0x810);
    W("write DMAC_LO alias",0x81C,0x12345678); R("AAF_DMLO flat",0x658); W("write DMAC_HI alias",0x820,0xABCD1234); R("AAF_DMHI flat",0x65C); R("DMAC_HI window reads low16",0x820);
    W("snap talker",0x804,1); R("busy after done",0x804); R("CNT0 poison after snap",0x830); R("STATE after snap",0x82C); R("PDUS after snap",0x858);
    puts("--- listener snap"); baseline(); hard_reset(); W("sel listener0",0x800,0); W("snap",0x804,1); R("CNT0",0x830); R("STATE",0x82C);
    puts("--- CHMAP gate and snap"); baseline(); hard_reset(); W("refused word",0x908,0x1234); R("word",0x908); R("stat",0x90C); W("arm",0x900,1); W("accepted word",0x908,0xFFFF1234); R("word low16",0x908); R("stat",0x90C);
    R("snap reset",0x910); R("loop poison",0x914); W("snap go",0x910,1); for(int i=0;i<30;i++) tick(); R("snap after timeout",0x910); R("loop after timeout",0x914);
    puts("--- PPS at PPS_P=0"); baseline(); hard_reset(); W("pps en",0x548,1); R("pps ctrl",0x548); R("pps width",0x55C);
    puts("--- PP"); baseline(); { auto p=pn("i_pp_ack"); set_port(p.first,p.second,false);} hard_reset(); R("stat",0x924); W("spaddr doorbell",0x928,0xFFFFFFFF); R("spaddr",0x928); R("busy",0x924); W("ignored while busy",0x928,0x00000123); R("spaddr stored anyway",0x928); W("nvm sel",0x934,0xFFFFFFFF); R("nvm sel",0x934);
    puts("--- read-table grouping: AAF_CTRL[0]=1, out-of-range talker row"); baseline(); hard_reset(); W("AAF_CTRL[0]=1",0x654,1); W("sel talker idx1 out of range",0x800,0x101); R("STRMW_CTRL, stream does not exist",0x810); W("sel talker idx0",0x800,0x100); R("STRMW_CTRL, stream exists",0x810);
    puts("--- unmapped"); baseline(); hard_reset(); for(uint16_t a: {0x808,0x80C,0x8E8,0x8F0,0x918,0x940,0xFFC,0x1000,0x7F4,0x7F8,0x7FC,0x20C,0x234,0x2FC,0x4A0,0x784,0x78C,0x79C}) R("gap",a);
    W("gap write",0x7F4,0xFFFFFFFF); R("gap ignores",0x7F4); W("CBS gap write",0x410,0xFFFFFFFF); R("CBS+0x10 ignores",0x410); W("CBS_CTRL0",0x40C,0xFFFFFFFF); R("CBS_CTRL0 only bit0",0x40C);
  }
  delete t; return 0; }
