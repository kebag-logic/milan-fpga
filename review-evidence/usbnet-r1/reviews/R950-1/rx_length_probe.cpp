// Compare receive record lengths to the current documented bus contract.
#define main original_suite_main
#include "sim_main.cpp"
#undef main
int main(int argc,char **argv) {
 Verilated::commandArgs(argc,argv); auto b=mk(); b->host(HOST,3); b->drain_dn();
 for(int len : {1518,1519,2000,2001}) {
  b->up_words.clear(); b->rx_q.push_back(frame(BCAST,PEER,0x0800,len)); b->cycles(10000);
  bool ok; auto frames=b->up_frames(&ok); CHECK(ok,"record parse");
  std::printf("rx_length=%d emitted_records=%zu",len,frames.size());
  if(!frames.empty()) std::printf(" header_length=%u",b->up_words[0]&4095);
  std::printf("\n");
  if(len>1518) CHECK(frames.empty(),"documented maximum 1518: emitted input length %d",len);
 }
 std::printf("probe failures=%d\n",fails()); return fails()?1:0;
}
