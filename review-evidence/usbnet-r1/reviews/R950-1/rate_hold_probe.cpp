// Reuse the exact-head frame driver; add an independent token-envelope check.
#define main original_suite_main
#include "sim_main.cpp"
#undef main
int main(int argc,char **argv) {
 Verilated::commandArgs(argc,argv);
 auto b=mk(); b->host(HOST,3); b->drain_dn();
 b->d->inject_en_i=0;
 for(int i=0;i<4;++i) b->rec(0,frame(PEER,HOST,0x0800,1000,-1,{},uint8_t(i)));
 b->drain_dn(); b->cycles(40000);
 CHECK(b->out.empty(),"held injection emits no frame");
 auto enabled=b->ncyc; b->d->inject_en_i=1;
 unsigned previous_complete=0;
 for(int cycle=0;cycle<15000;++cycle) {
  b->cycles(1);
  unsigned complete=unsigned(b->out.size())-unsigned(b->in_mac_lo);
  if(complete!=previous_complete) {
   auto elapsed=b->ncyc-enabled; double allowed=3200.0+0.1*double(elapsed);
   std::printf("wire_complete=%u elapsed=%llu wire_octets=%u envelope=%.1f\n",complete,(unsigned long long)elapsed,complete*1024,allowed);
   CHECK(double(complete*1024)<=allowed+1.0,"completed wire envelope: %u > %.1f",complete*1024,allowed);
   previous_complete=complete;
  }
 }
 CHECK(b->out.size()==4,"all four frames eventually transmit");
 for(size_t i=0;i<b->out.size();++i) {
  auto elapsed=b->out[i].first-enabled;
  double allowed=3200.0+0.1*double(elapsed);
  unsigned sent=unsigned(i+1)*1024;
  std::printf("frame=%zu elapsed=%llu charged_octets=%u envelope=%.1f\n",i+1,(unsigned long long)elapsed,sent,allowed);
  CHECK(double(sent)<=allowed+1.0,"token envelope after held grant: %u > %.1f",sent,allowed);
 }
 std::printf("probe failures=%d\n",fails()); return fails()?1:0;
}
