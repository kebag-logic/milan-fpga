// Reviewer-owned measurement of the issue body's zero-bank-write acceptance.
#include <cstdint>
#include <cstdio>
#include <vector>
#include "VKL_gptp_rx_parser.h"
#include "verilated.h"
using B=std::vector<uint8_t>;
static VKL_gptp_rx_parser d;
static int writes, events;
void tick(){ d.clk_i=0; d.eval(); d.clk_i=1; d.eval(); writes+=!!d.bank_we_o; events+=!!d.ev_valid_o; }
void word(B &b,int p,uint64_t v,int n){ for(int i=n-1;i>=0;--i){b[p+i]=v&255;v>>=8;} }
B frame(int type,int len){
 B b(len+14,0); word(b,0,0x0180c200000eULL,6); word(b,6,0x020000000001ULL,6);
 word(b,12,0x88f7,2); b[14]=0x10|type; b[15]=2; word(b,16,len,2);
 word(b,20,0x0208,2); word(b,34,0xaabbccfffe001122ULL,8); word(b,42,1,2);
 word(b,44,0x3500+type,2); b[47]=0xfd;
 if(type==8){word(b,58,3,2);word(b,60,28,2);word(b,62,0x0080c2,3);word(b,65,1,3);}
 return b;
}
int main(int argc,char **argv){
 Verilated::commandArgs(argc,argv); d.local_clock_valid_i=1; d.local_clock_id_i=0x1122334455667788ULL;
 puts("type,length,error_byte,drops,events,writes_before,writes_on,writes_after,total_writes,zero_write_acceptance");
 const int types[]={0,8,2,3}, lens[]={44,76,54,54}; const char *names[]={"sync","fu","pdreq","pdresp"};
 int failed=0, checks=0;
 for(int a=0;a<4;a++){
  B f=frame(types[a],lens[a]);
  for(int pos: {-1,0,20,29,40,int(f.size()-1)}){
   d.rst_n=0; d.rx_valid_i=0; d.rx_sof_i=0;d.rx_eof_i=0;d.rx_err_i=0; tick();tick(); d.rst_n=1;
   writes=events=0; int before=0,on=0;
   for(int i=0;i<int(f.size());i++){
    int w=writes; d.rx_valid_i=1;d.rx_sof_i=i==0;d.rx_eof_i=i==int(f.size()-1);d.rx_data_i=f[i];d.rx_err_i=i==pos; tick();
    if(i==pos){before=w;on=writes-w;}
   }
   d.rx_valid_i=d.rx_sof_i=d.rx_eof_i=d.rx_err_i=0; for(int i=0;i<4;i++)tick();
   bool ok=pos<0 ? (d.drop_cnt_o==0 && events==1) : (d.drop_cnt_o==1 && events==0 && writes==0);
   checks++; failed+=!ok;
   printf("%s,%zu,%d,%u,%d,%d,%d,%d,%d,%s\n",names[a],f.size(),pos,unsigned(d.drop_cnt_o),events,before,on,writes-before-on,writes,ok?"PASS":"FAIL");
  }
 }
 printf("%d checks: %d PASS, %d FAIL\n",checks,checks-failed,failed);return failed?1:0;
}
