// Reviewer probe: randomized differential test of KL_srp_encoder against an
// independent model of the merge table written from docs 10 sec. 3.
// Usage: Vsrp_sim <seed> <cycles> <swap_percent>
#include <verilated.h>
#include "Vsrp_tb_wrap.h"
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <map>
#include <random>
#include <vector>
using namespace std;
static const int NEW=0,JIN=1,IN=2,JMT=3,MT=4,LV=5;
struct Ev{int app,type,ev,fp;array<uint8_t,34> v;};
static int alen(int app,int t){if(app)return 2;switch(t){case 1:return 25;case 2:return 34;case 3:return 8;default:return 4;}}
struct Ent{int app,type,ev,fp;array<uint8_t,34> v;};
static bool same(const Ent&e,const Ev&o){
  if(e.app!=o.app||e.type!=o.type)return false;
  int n=o.app?2:(o.type==4?4:8);
  return memcmp(e.v.data(),o.v.data(),n)==0;}
static bool isS(int e){return e==IN||e==MT;}
// doc table of 10 sec. 3, written independently of merge_ev_f
static void merge(Ent&e,const Ev&o){
  int oe=e.ev,ne=o.ev;
  int res;
  if(ne==NEW||ne==LV)res=ne;
  else if(ne==JIN||ne==JMT)res=(oe==NEW)?NEW:ne;
  else res=isS(oe)?ne:oe;
  bool keepfp=isS(ne)&&!isS(oe);
  e.ev=res; if(!keepfp)e.fp=o.fp; e.v=o.v;
}
static mt19937_64 rng;
static int R(int n){return int(rng()%uint64_t(n));}
static Ev gen(){
  Ev e{};e.v.fill(0);
  int k=R(100);
  int evs[6]={NEW,JIN,IN,JMT,MT,LV};
  e.ev=evs[R(6)];
  if(k<25){e.app=0;e.type=4;int i=R(4);e.v[0]=6+i;e.v[1]=3+i;e.v[2]=0;e.v[3]=2;if(R(4)==0){e.v[1]=5+i;e.v[3]=5;}}
  else if(k<50){e.app=1;e.type=1;e.v[0]=R(3);e.v[1]=2+R(3);}
  else if(k<75){e.app=0;e.type=3;e.fp=R(4);for(int i=0;i<7;i++)e.v[i]=0xA0+i;e.v[7]=0x10+R(6);}
  else if(k<97){e.app=0;e.type=1+R(2);int s=R(5);for(int i=0;i<7;i++)e.v[i]=0xB0+i;e.v[7]=0x20+s;
    e.v[8]=0x91;e.v[9]=0xE0;e.v[10]=0xF0;e.v[11]=0;e.v[12]=0;e.v[13]=s+(R(8)==0?9:0);e.v[14]=0;e.v[15]=2;e.v[24]=7;}
  else {e.app=R(2);e.type=e.app?2:(R(2)?0:5);}
  return e;}
static bool validT(const Ev&e){return e.app?e.type==1:(e.type>=1&&e.type<=4);}
int main(int argc,char**argv){
  uint64_t seed=strtoull(argv[1],0,0);long cycles=atol(argv[2]);int swp=atoi(argv[3]);rng.seed(seed);
  Verilated::commandArgs(argc,argv);
  Vsrp_tb_wrap*d=new Vsrp_tb_wrap;
  auto edge=[&]{d->clk_i=1;d->eval();d->clk_i=0;d->eval();};
  d->rst_n=0;d->clk_i=0;d->dom_link_up_i=0;for(int i=0;i<8;i++)edge();d->rst_n=1;
  const uint8_t mac[6]={2,0,0,0,0,1};uint64_t m=0;for(int i=0;i<6;i++)m=(m<<8)|mac[i];d->enc_own_mac_i=m;
  vector<Ent> T[2];
  struct Exp{int app;vector<Ent> e;};deque<Exp> pend;
  bool have=false;Ev cur{};deque<Ev> parked;long wait=0,maxwait=0;
  long acc=0,hit=0,frames=0,vecs=0,errs=0,drops=0,dupframes=0,hitlast=0;
  int lapr=0;int txst=0;int txdelay=0;vector<uint8_t> fr;int slot=0;
  auto err=[&](const char*s,long c){if(errs++<20)printf("ERR %s at %ld\n",s,c);};
  for(long c=0;c<cycles;c++){
    // offer
    if(have&&R(100)<swp){parked.push_back(cur);have=false;}
    if(!have){ if(!parked.empty()&&R(2)){cur=parked.front();parked.pop_front();have=true;}
      else if(R(100)<70){cur=gen();have=true;wait=0;} }
    d->enc_ev_valid_i=have;
    if(have){d->enc_ev_app_i=cur.app;d->enc_ev_attr_type_i=cur.type;d->enc_ev_event_i=cur.ev;d->enc_ev_fourpack_i=cur.fp;
      for(int w=0;w<9;w++)d->enc_ev_value_i[w]=0;
      for(int i=0;i<34;i++){int bit=271-8*i-7;d->enc_ev_value_i[bit/32]|=uint32_t(cur.v[i])<<(bit%32);
        if(bit%32>24)d->enc_ev_value_i[bit/32+1]|=uint32_t(cur.v[i])>>(32-bit%32);}
    }else d->enc_ev_value_i[0]=0;
    int jt=0;if(R(60)==0)jt|=1;if(R(60)==0)jt|=2;d->enc_join_tick_i=jt;
    int la=0;if(R(300)==0)la|=1;if(R(300)==0)la|=2;d->enc_leaveall_i=la;
    if(!lapr&&R(800)==0)lapr=1;d->enc_la_prepare_i=lapr;
    // tx face
    d->enc_txreq_ready_i=0;d->ser_req_i=0;
    if(txst==0&&d->enc_txreq_valid_o){ if(txdelay==0)txdelay=1+R(R(10)==0?400:8); if(--txdelay==0){d->enc_txreq_ready_i=1;slot=d->enc_txreq_slot_o;txst=1;} }
    else if(txst==1){d->ser_slot_i=slot;d->ser_req_i=1;d->ser_ready_i=1;txst=2;fr.clear();}
    d->eval();
    bool commit=d->dbg_commit_o;int c0=d->enc_dbg_cnt_msrp_o,c1=d->enc_dbg_cnt_mvrp_o;
    bool rdy=d->enc_ev_ready_o;bool drop=d->enc_ev_drop_o;
    bool sv=d->ser_valid_o,sl=d->ser_last_o;uint8_t sd=d->ser_data_o;
    bool ladone=d->enc_la_done_o;
    if(txst==2&&sv){fr.push_back(sd);}
    if(have&&rdy){
      if(!validT(cur)){drops++;if(!drop)err("no drop strobe",c);}
      else{acc++;auto&t=T[cur.app];bool f=false;
        for(size_t i=0;i<t.size();i++)if(same(t[i],cur)){merge(t[i],cur);f=true;hit++;if(i+1==t.size())hitlast++;break;}
        if(!f)t.push_back(Ent{cur.app,cur.type,cur.ev,cur.fp,cur.v});}
      if(wait>maxwait)maxwait=wait;have=false;wait=0;
    }else if(have)wait++;
    if(ladone)lapr=0;
    vector<Ent> s0,s1;if(commit){s0=T[0];s1=T[1];}
    edge();
    if(commit){
      int n0=d->enc_dbg_cnt_msrp_o,n1=d->enc_dbg_cnt_mvrp_o;
      int app=-1; if(c0&&n0==0)app=0; else if(c1&&n1==0)app=1; else if(!c0&&!c1)app=-2; else app=0;
      if(app==-1)err("commit app unknown",c);
      if(app==-2)app=0;
      pend.push_back(Exp{app,app?s1:s0});T[app].clear();
      if(int(T[0].size())>12||int(T[1].size())>12)err("model overflow",c);
    }
    if(int(T[0].size())!=d->enc_dbg_cnt_msrp_o){err("msrp cnt differs",c);}
    if(int(T[1].size())!=d->enc_dbg_cnt_mvrp_o){err("mvrp cnt differs",c);}
    if(txst==2&&sv&&sl){
      txst=0;d->ser_ready_i=0;frames++;
      if(pend.empty()){err("frame without commit",c);continue;}
      Exp x=pend.front();pend.pop_front();
      bool msrp=fr[12]==0x22&&fr[13]==0xEA;
      if(msrp!=(x.app==0))err("frame application",c);
      // independent parse: expand each VectorAttribute
      size_t i=15;vector<Ent> got;bool bad=false;
      while(i+1<fr.size()&&!(fr[i]==0&&fr[i+1]==0)){
        int t=fr[i],al=fr[i+1];i+=2;if(msrp)i+=2;
        while(i+1<fr.size()&&!(fr[i]==0&&fr[i+1]==0)){
          int nov=((fr[i]&0x1F)<<8)|fr[i+1];i+=2;vecs++;
          vector<uint8_t> fv(fr.begin()+i,fr.begin()+i+al);i+=al;
          vector<int> e3;for(int k=0;k<(nov+2)/3;k++){int b=fr[i++];e3.push_back(b/36);e3.push_back((b/6)%6);e3.push_back(b%6);}
          vector<int> e4;if(msrp&&t==3)for(int k=0;k<(nov+3)/4;k++){int b=fr[i++];e4.push_back(b>>6);e4.push_back((b>>4)&3);e4.push_back((b>>2)&3);e4.push_back(b&3);}
          for(int k=0;k<nov;k++){Ent e{};e.app=!msrp;e.type=t;e.ev=e3[k];e.fp=(msrp&&t==3)?e4[k]:0;e.v.fill(0);
            memcpy(e.v.data(),fv.data(),al);
            auto add=[&](int off,int len,int inc){uint64_t cy=inc;for(int b=off+len-1;b>=off&&cy;b--){cy+=e.v[b];e.v[b]=cy&255;cy>>=8;}};
            if(!msrp)add(0,2,k);else if(t==4){e.v[0]+=k;e.v[1]+=k;}else if(t==3)add(0,8,k);else{add(0,8,k);add(8,6,k);}
            got.push_back(e);}
        }
        i+=2;
      }
      // uniqueness
      for(size_t a=0;a<got.size();a++)for(size_t b=a+1;b<got.size();b++){
        Ev o{};o.app=got[b].app;o.type=got[b].type;o.v=got[b].v;if(same(got[a],o)){dupframes++;bad=true;}}
      if(got.size()!=x.e.size())bad=true;
      else for(size_t a=0;a<got.size();a++){const Ent&g=got[a];const Ent&w=x.e[a];
        int al2=alen(w.app,w.type);
        if(g.type!=w.type||g.ev!=w.ev||(w.type==3&&!w.app&&g.fp!=w.fp)||memcmp(g.v.data(),w.v.data(),al2))bad=true;}
      if(bad){err("frame differs from model",c);if(errs<6){printf("  got %zu want %zu:",got.size(),x.e.size());for(auto&g:got)printf(" t%d/%d/%02x%02x",g.type,g.ev,g.v[1],g.v[7]);printf(" | ");for(auto&g:x.e)printf(" t%d/%d/%02x%02x",g.type,g.ev,g.v[1],g.v[7]);puts("");}}
    }
  }
  printf("seed=%llu cycles=%ld swap=%d accepted=%ld merged=%ld merged_last=%ld drops=%ld frames=%ld vectors=%ld dup_frames=%ld maxwait=%ld errors=%ld\n",(unsigned long long)seed,cycles,swp,acc,hit,hitlast,drops,frames,vecs,dupframes,maxwait,errs);
  return errs?1:0;
}
